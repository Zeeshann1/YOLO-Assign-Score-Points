#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/26 16:34
# @Author  : Qiguangnan
# @File    : litF.py
import json
import time
import socket
from pathlib import Path
import base64
import os
import cv2
import numpy as np
import redis

from utilsg.minio_base import minio_client
import configg.global_config
import requests
from logger import logger
from configg.global_config import SAVE_RESULT_LOCAL, QUALITY_JPG, GLOBAL_USE_NGINXURL


def get_host_ip():  ## 获取本机 IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 8080))
    ip = s.getsockname()[0]
    s.close()
    return ip
# def get_host_ip():  ## 获取本机 IP
#     from netifaces import interfaces, ifaddresses, AF_INET
#     for ifaceName in interfaces():
#         addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
#         if '127.0.0.1' not in addresses and '172.17.0.1' not in addresses and 'No IP addr' not in addresses:
#             ip = ' '.join(addresses)
#             return ip
#     return None


url_ip = get_host_ip()  ## 本机的 ip
if not SAVE_RESULT_LOCAL:
    ptr_minio_class = minio_client(
        url_minio=configg.global_config.get_minio_url(),
        access_key=configg.global_config.get_minio_access_key(),
        secret_key=configg.global_config.get_minio_secret_key())
if not SAVE_RESULT_LOCAL or GLOBAL_USE_NGINXURL:
    redis_queue_response_result = redis.Redis(
        host=configg.global_config.get_redis_url_host(),
        port=configg.global_config.get_redis_port(),
        password=configg.global_config.get_redis_password(),
        db=configg.global_config.get_redis_db_ai_result())


def uploaded_images(data_img, path, filename, dir_local="/home/data/"):
    '''
    :param data_img:
    :param path:
    :param filename:
    :param is_local:
    :param dir_local:   linux:  /var/www/html  , windows : "I:\\nginx\\data\\"
    :return:
    '''
    if SAVE_RESULT_LOCAL:
        # save to local and return the path
        path_dir = os.path.join(dir_local, path)
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
        full_path = os.path.join(path_dir, filename)
        f = open(full_path, "wb+")
        data_encode = np.array(data_img)
        str_encode = data_encode.tostring()
        f.write(str_encode)
        f.close()
        # usr_local_url = "http://" + url_ip + ":8888/image/" + path + "/" + filename
        # usr_local_url = f"http://{url_ip}:8888/image/{path}/{filename}"
        if GLOBAL_USE_NGINXURL:
            full_path = f"http://{url_ip}/image/{path}/{filename}"
        return full_path
    else:
        # sent to minio server
        path_filename = f"{path}_{filename}"
        data_encode = np.array(data_img)
        str_encode = data_encode.tostring()
        status_return, url_minio_image = ptr_minio_class.put_images(
            str_encode, "image", path_filename)
        return url_minio_image


def upload_redis_or_save_json_local(jsonScoreNow,
                                    path,
                                    call_back_url,
                                    filename="scoreinfo.json",
                                    dir_local="./",
                                    up_callback=True,
                                    file_lock=None):
    # print(jsonScoreNow)
    if file_lock is not None:
        file_lock.acquire()
    str_json = json.dumps(jsonScoreNow, ensure_ascii=False)
    # sent result by call back
    headers = {
        "Content-Type": "application/json",
    }

    if SAVE_RESULT_LOCAL:
        # save the result to local
        path_dir = os.path.join(configg.SCORE_ROOT_PATH, path)
        try:
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)
        except Exception as e:
            logger.info("failed created {0} error:{1}".format(path_dir, e))
        try:
            full_path = os.path.join(path_dir, filename)
            logger.info("save file {}".format(full_path))
            f = open(full_path, "w+", encoding='utf-8')
            f_r = f.write(str_json)
            f.close()
            if GLOBAL_USE_NGINXURL:
                # sent to redis
                key_result = jsonScoreNow["flag"] + "_" + jsonScoreNow[
                    "exper_id"]
                redis_queue_response_result.set(key_result, str_json)
        except Exception as e:
            logger.info("save file : {} failed: {}".format(full_path, e))
        try:
            if up_callback:
                json_imgbase64 = json.loads(str_json)
                for item in json_imgbase64['score_pts_info']:
                    # imgPath = score_json_path.with_name(f'{item["id"]}.jpg')
                    if not GLOBAL_USE_NGINXURL and os.path.exists(
                            item['images_url']):
                        # item['images_url'] = f"http://{url_ip}/image/{item['images_url'][len(configg.SCORE_ROOT_PATH):]}"
                        item['images_url'] = img2base64(item['images_url'])
                n_repost = 0
                while n_repost < 3:
                    r = requests.post(
                        url=call_back_url,
                        data=json.dumps(json_imgbase64),
                        headers=headers,
                        timeout=10,
                        verify=False)
                    rj = json.loads(r.text)
                    if rj["code"] == 200:
                        break
                    else:
                        logger.error('分数推送异常url local:{}'.format(call_back_url))
                    n_repost += 1
                logger.info('分数推送成功::{}'.format(rj))
                print("分数推送成功")
        except Exception as e:
            logger.debug(f'分数推送失败:{str(e)}')
            print(e)
            print("分数推送失败")
    else:
        # sent to redis
        key_result = jsonScoreNow["flag"] + "_" + jsonScoreNow["exper_id"]
        redis_queue_response_result.set(key_result, str_json)
        try:
            if up_callback:
                n_repost = 0
                print(str_json)
                while n_repost < 3:
                    r = requests.post(
                        url=call_back_url,
                        data=str_json,
                        headers=headers,
                        timeout=10,
                        verify=False)
                    rj = json.loads(r.text)
                    if rj["code"] == 200:
                        break
                    else:
                        logger.error("分数推送异常url：{}".format(call_back_url))
                    n_repost += 1
                logger.info('分数推送成功::{}'.format(rj))
        except Exception as e:
            logger.debug(f'分数推送失败:{str(e)}')
    if file_lock is not None:
        file_lock.release()


def mkdir(path):
    path = Path(path)
    if path.exists():
        return
    if not path.parent.exists():
        mkdir(path.parent)
    path.mkdir()


def ts2ft(timeStamp=None, format="%Y-%m-%d %H:%M:%S"):
    if timeStamp is not None:
        return time.strftime(format, time.localtime(timeStamp))
    else:
        return time.strftime(format, time.localtime())


def ft2ts(format_time, format='%Y-%m-%d %H:%M:%S'):  ## 格式化时间转时间戳
    return time.mktime(time.strptime(format_time, format))


def img2base64(imagPath):  # 图片转成base64
    with open(imagPath, 'rb') as f:
        image_base64 = str(base64.b64encode(f.read()), encoding='utf-8')
    return image_base64


def encode_image_jpg(image):
    params = (cv2.IMWRITE_JPEG_QUALITY, QUALITY_JPG)
    _, base_img = cv2.imencode(".jpg", image, params)
    return base_img
