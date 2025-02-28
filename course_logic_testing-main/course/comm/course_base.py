#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/29 11:10
# @Author  : eli.wang
# @File    : course_base.py

from .anchorBox import pt_in_polygon
from .anchorBox import center_point
import traceback
import numpy as np
import torch
import requests
import cv2
import time
from .plotBox import Plot
from utilsg.litF import uploaded_images, encode_image_jpg, upload_redis_or_save_json_local, ts2ft
from configg.global_config import SCORE_ROOT_PATH, GLOBAL_USE_RTMP
from config import EXP_MAP
from utilsg.ffmpeg_video import FfmpegRtmp
import configg
import os
from pathlib import Path
from configg.global_config import experimental_site_top as est
from configg.global_config import experimental_site_front as esf
from configg.global_config import experimental_site_side as ess
from logger import logger


class ConfigModel:
    def __init__(self):
        self.w_top = 1920
        self.h_top = 1080
        self.w_side = 1920
        self.h_side = 1080
        self.w_front = 1920
        self.h_front = 1080
        self.center_area_top = None
        self.center_area_side = None
        self.center_area_front = None
        self.set_center_area = False

        self.preds_top = None
        self.preds_side = None
        self.preds_front = None
        self.call_back_url = ""
        self.real_back_url = ""
        self.video_back_url = ""

        self.device = 'cuda:0'

        self.score_list = []  # 已经得到的得分点
        self.faulty_score_list = []  # 错误操作id列表
        self.exper_score_ids = []
        self.part_index = 0  # 模块化练习时的索引
        self.exercise_interaction = {}
        self.file_lock = None
    def set_file_lock(self, file_lock):
        self.file_lock = file_lock
    def setDefaultInfo(self,
                       student_flag,
                       experiment_id_now,
                       exper_score_ids,
                       call_back_url,
                       real_back_url="",
                       video_back_url="",
                       request_code="",
                       is_mp4=False,
                       is_teach=True):
        self.student_flag = student_flag
        self.experiment_id_now = experiment_id_now
        self.config_model = EXP_MAP[experiment_id_now]
        self.cam_use = self.config_model["camUse"]
        self.exper_score_ids = exper_score_ids
        self.path_save = self.student_flag + "_" + self.experiment_id_now
        self.call_back_url = call_back_url
        self.is_mp4 = is_mp4
        self.EN_CH_map = self.get_EN_CH_map()
        self.labels = self.config_model["labelInfo"]
        self.plot = Plot(labels=self.labels, EN_CH_map=self.EN_CH_map)
        self.real_back_url = real_back_url
        self.video_back_url = video_back_url
        self.real_status = True
        self.video_status = True
        self.is_teach = is_teach

        if len(real_back_url) < 7:
            self.real_status = False
        if len(video_back_url) < 7:
            self.video_status = False

        path_temp = os.path.join(configg.SCORE_ROOT_PATH, self.path_save)
        self.save_path = Path(path_temp)
        # 得分点标记
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False
        self.scorePoint8 = False
        self.scorePoint9 = False
        self.scorePoint10 = False
        self.scorePoint11 = False
        self.scorePoint12 = False
        self.scorePoint13 = False
        self.scorePoint14 = False
        self.scorePoint15 = False
        self.scorePoint16 = False
        self.scorePoint17 = False
        self.scorePoint18 = False
        self.scorePoint19 = False
        self.scorePoint20 = False
        self.scorePoint21 = False

        self.scoreTime1 = time.time()
        self.scoreTime2 = time.time()
        self.scoreTime3 = time.time()
        self.scoreTime4 = time.time()
        self.scoreTime5 = time.time()
        self.scoreTime6 = time.time()
        self.scoreTime7 = time.time()
        self.scoreTime8 = time.time()
        self.scoreTime9 = time.time()
        self.scoreTime10 = time.time()
        self.scoreTime11 = time.time()
        self.scoreTime12 = time.time()
        self.scoreTime13 = time.time()
        self.lastTime = time.time()

        # self.flag1 = False
        # self.flag2 = False
        # self.flag3 = False
        # self.flag4 = False
        # self.flag5 = False
        # self.flag6 = False
        # self.flag7 = False
        # self.flag8 = False

        self.set_center_box = False
        self.culture_dish_top_box = None
        self.corn_beaker_top_box = None
        self.score_list = []  # 已经得到的得分点
        self.shape_top = None
        self.shape_front = None
        self.shape_side = None

        # 针对生物需要用电子目前采集，设置2个变量
        self.img_urls = []  # 所有拍摄的图像urls，目前默认按只有一个图像处理，取第一个地址进行下载并赋值img_bio
        self.img_bio = None  # 不为None ，说明有图像urls，且图像正常

        self.score_interaction = [
        ]  # 评分点的交互信息 格式如下；可以根据评分点情况结合realtime_interaction进行赋分判断
        # [
        #     {"id": 3,
        #      "student_answer": ["ioioio#学生填写答案"],
        #      "teacher_answer": ["ioioiio#标注答案"],
        #      "imgurl": ["#该评分点学生端拍摄图像地址"],
        #      "judge_type": "0-default,无该参数时的默认值,1-填空选择比对，2-没有标准答案，3-需与评分点内智能赋分得到示数进行比较"
        #      },
        #     {"id": 5,
        #      "student_answer": ["ioioio"],
        #      "teacher_answer": ["ioioiio"],
        #      "imgurl": [],
        #      "judge_type": "0-default,无该参数时的默认值,1-填空选择比对，2-没有标准答案，3-需与评分点内智能赋分得到示数进行比较"
        #      }
        # ]
        self.realtime_interaction = False  # 当实时流或视频文件场景，相关评分点有交互信息传入时为True（比如显微镜图片，填空题答案等）
        self.exercise_interaction = {}
        self.part_index = 0

        self.jsonResultScore = {
            "status": True,
            "msg": "ok",
            "ids": [],
            "score_pts_info": [],
            "error_pts_info": {},
            "exper_id": experiment_id_now,
            "flag": student_flag,
            "request_code": request_code
        }
        #print('getting')

        # 结果推流变量设置
        self.rtmp_url_video_top = configg.get_rtmp_video_url(
        ) + "EXPID_" + experiment_id_now + "/STDID_" + student_flag + "_top"
        self.rtmp_url_video_front = configg.get_rtmp_video_url(
        ) + "EXPID_" + experiment_id_now + "/STDID_" + student_flag + "_front"
        self.rtmp_url_video_side = configg.get_rtmp_video_url(
        ) + "EXPID_" + experiment_id_now + "/STDID_" + student_flag + "_side"

        if GLOBAL_USE_RTMP and self.video_status:
            if "top" in self.cam_use:
                self.rtmp_top = FfmpegRtmp(
                    rtmpurl=configg.get_rtmp_video_url(),
                    appname="EXPID_" + experiment_id_now,
                    rtmpfile="STDID_" + student_flag + "_top")
            else:
                self.rtmp_top = None
                self.rtmp_url_video_top = ""
            if "front" in self.cam_use:
                self.rtmp_front = FfmpegRtmp(
                    rtmpurl=configg.get_rtmp_video_url(),
                    appname="EXPID_" + experiment_id_now,
                    rtmpfile="STDID_" + student_flag + "_front")
            else:
                self.rtmp_front = None
                self.rtmp_url_video_front = ""
            if "side" in self.cam_use:
                self.rtmp_side = FfmpegRtmp(
                    rtmpurl=configg.get_rtmp_video_url(),
                    appname="EXPID_" + experiment_id_now,
                    rtmpfile="STDID_" + student_flag + "_side")
            else:
                self.rtmp_side = None
                self.rtmp_url_video_side = ""
        else:
            self.rtmp_top = None
            self.rtmp_side = None
            self.rtmp_front = None
            self.rtmp_url_video_top = ""
            self.rtmp_url_video_front = ""
            self.rtmp_url_video_side = ""

        self.init_jsonScore()

    def setpartInfo(self,
                    exercise_interaction
                    ):
        self.exper_score_ids = exercise_interaction["exper_score_ids"]
        self.score_list = []  # 已经得到的得分点
        self.faulty_score_list = []  # 错误操作id列表
        self.part_index = exercise_interaction["task_student_one"]["part"]
        self.exercise_interaction = exercise_interaction
        self.call_back_url = exercise_interaction["call_back_url"]
        self.real_back_url = exercise_interaction["real_back_url"]
        self.video_back_url = exercise_interaction["video_back_url"]
        if len(self.real_back_url) < 7:
            self.real_status = False
        else:
            self.real_status = True
        if len(self.video_back_url) < 7:
            self.video_status = False
        else:
            self.video_status = True
        self.score_list = []  # 已经得到的得分点
        self.faulty_score_list = []  # 错误操作id列表
        self.jsonResultScore["score_pts_info"].clear()
        self.jsonResultScore["error_pts_info"] = {}
        self.jsonResultScore["ids"].clear()
        self.init_jsonScore()

    def init_jsonScore(self):
        self.jsonResultScore["rtmp_url_top"] = self.rtmp_url_video_top
        self.jsonResultScore["rtmp_url_front"] = self.rtmp_url_video_front
        self.jsonResultScore["rtmp_url_side"] = self.rtmp_url_video_side
        # print(self.jsonResultScore)

        for item in self.exper_score_ids:
            if item in self.config_model["scorePointInfo"]:
                score_now = self.config_model["scorePointInfo"][item]
                score_one_origin = {
                    "id": item,
                    "score_status": False,
                    "str_pts": score_now["info"],
                    "images_url": "",
                    "time": "",
                    "conf": 0.0,
                    "frame_num": 0,
                    "object": []
                }
                if self.is_mp4 and "type" in score_now.keys(
                ) and score_now["type"] != 0:  # todo 目前只针对视频文件处理
                    score_one_origin["type"] = score_now["type"]
                    # score_one_origin["images_url"] = "https://www.baidu.com/img/bd_logo1.png"
                self.jsonResultScore["score_pts_info"].append(score_one_origin)
        logger.info(f"score init sucess: {self.jsonResultScore} \n")
        if self.video_status:
            upload_redis_or_save_json_local(
                jsonScoreNow=self.jsonResultScore,
                path=self.path_save,
                call_back_url=self.video_back_url,
                filename="scoreinfo.json",
                dir_local=SCORE_ROOT_PATH,
                up_callback=self.video_status,
                file_lock=self.file_lock)
        elif self.real_status and not self.video_status:
            upload_redis_or_save_json_local(
                jsonScoreNow=self.jsonResultScore,
                path=self.path_save,
                call_back_url=self.real_back_url,
                filename="scoreinfo.json",
                dir_local=SCORE_ROOT_PATH,
                up_callback=self.real_status,
                file_lock=self.file_lock)
        else:
            upload_redis_or_save_json_local(
                jsonScoreNow=self.jsonResultScore,
                path=self.path_save,
                call_back_url=self.call_back_url,
                filename="scoreinfo.json",
                dir_local=SCORE_ROOT_PATH,
                up_callback=False,
                file_lock=self.file_lock)

    def down_url_img(self, url=""):
        try:
            img = None
            file = requests.get(url)
            img = cv2.imdecode(np.frombuffer(file.content, np.uint8), 1)
            return True, img
        except:
            return False, None

    def set_realtime_interaction(self, score_interaction):
        self.score_interaction = score_interaction
        self.realtime_interaction = True

    def set_shape_value(self, top_shape, front_shape, side_shape, img_urls,
                        img_bio, score_interaction):
        self.shape_top = top_shape
        self.shape_front = front_shape
        self.shape_side = side_shape
        self.img_urls = img_urls
        self.img_bio = img_bio
        self.score_interaction = score_interaction
        if len(self.score_interaction) > 0:
            self.realtime_interaction = True

        if GLOBAL_USE_RTMP and self.video_status:
            if "top" in self.cam_use and self.shape_top is not None:
                self.rtmp_top = FfmpegRtmp(
                    rtmpurl=configg.get_rtmp_video_url(),
                    appname="EXPID_" + self.experiment_id_now,
                    rtmpfile="STDID_" + self.student_flag + "_top",
                    width=self.shape_top[1],
                    height=self.shape_top[0])
            else:
                self.rtmp_top = None
                self.rtmp_url_video_top = ""
            if "front" in self.cam_use and self.shape_front is not None:
                self.rtmp_front = FfmpegRtmp(
                    rtmpurl=configg.get_rtmp_video_url(),
                    appname="EXPID_" + self.experiment_id_now,
                    rtmpfile="STDID_" + self.student_flag + "_front",
                    width=self.shape_front[1],
                    height=self.shape_front[0])
            else:
                self.rtmp_front = None
                self.rtmp_url_video_front = ""
            if "side" in self.cam_use and self.shape_side is not None:
                self.rtmp_side = FfmpegRtmp(
                    rtmpurl=configg.get_rtmp_video_url(),
                    appname="EXPID_" + self.experiment_id_now,
                    rtmpfile="STDID_" + self.student_flag + "_side",
                    width=self.shape_side[1],
                    height=self.shape_side[0])
            else:
                self.rtmp_side = None
                self.rtmp_url_video_side = ""
        else:
            self.rtmp_top = None
            self.rtmp_side = None
            self.rtmp_front = None
            self.rtmp_url_video_top = ""
            self.rtmp_url_video_front = ""
            self.rtmp_url_video_side = ""

    def get_EN_CH_map(self):
        en_ch_map = {}
        for item in self.config_model["modelInfo"]:
            en_ch_map[item] = self.config_model["modelInfo"][item]["CH_name"]
        return en_ch_map

    # def assignScore(self, index, img, object, conf, time_frame, num_frame, name_save, preds, *args, **kwargs):
    def assignScore(self,
                    index: int,
                    img,
                    time_frame,
                    object,
                    preds=None,
                    num_frame=None,
                    conf=0.6,
                    name_save=None,
                    *args,
                    **kwargs):
        if num_frame is None:
            num_frame = self.num_frame
        if name_save is None:
            name_save = f'{index}.jpg'
        if index not in self.score_list:
            self.score_list.append(index)  # 将该得分加入已得分数
            exec(f'self.scorePoint{index} = True')  # 将该得分点设置为True 不在判断该得分点
        # else:
        #     return
        #print(index)
        if str(index) not in self.exper_score_ids:
            # print("{} index not in {}".format(index,self.exper_score_ids))
            return
        if preds is not None:
            self.plot(preds, img)
        t_upload_result = time.time()
        #print(img.shape)
        # upload drawed image to minio or save to local dir
        cv2.imwrite(self.call_back_url+'score'+str(index)+'.jpg',img)
        
        '''
        print("upload test ")
        if torch.is_tensor(conf):
            conf = conf.cpu().numpy().tolist()
        dataimg = encode_image_jpg(img)
        image_url = uploaded_images(
            data_img=dataimg,
            path=self.path_save,
            filename=name_save,
            dir_local=SCORE_ROOT_PATH)
        i_index = self.exper_score_ids.index(str(index))
        self.jsonResultScore["score_pts_info"][i_index]["score_status"] = True
        self.jsonResultScore["score_pts_info"][i_index][
            "images_url"] = image_url
        if self.is_mp4:
            self.jsonResultScore["score_pts_info"][i_index]["time"] = int(
                time_frame)
        else:
            self.jsonResultScore["score_pts_info"][i_index]["time"] = ts2ft(
                time_frame / 1000)
        self.jsonResultScore["score_pts_info"][i_index]["conf"] = conf
        self.jsonResultScore["score_pts_info"][i_index][
            "frame_num"] = num_frame
        self.jsonResultScore["score_pts_info"][i_index]["object"] = [
        ]  # object
        # call callback server ,sent now score to client and save to redis
        upload_redis_or_save_json_local(
            jsonScoreNow=self.jsonResultScore,
            path=self.path_save,
            call_back_url=self.real_back_url,
            filename="scoreinfo.json",
            dir_local=SCORE_ROOT_PATH,
            up_callback=self.real_status,
            file_lock=self.file_lock)
        # up_callback=not self.is_mp4)  # todo
        # exec(f'self.scorePoint{index} = True')  # 将该得分点设置为True 不在判断该得分点
        self.post_assign(index, img, object, conf, time_frame, num_frame,
                         name_save, preds, *args, **kwargs)
        '''
        return True

    def post_assign(self, index, img0, object, conf, time_frame, num_frame,
                    name_save, preds, *args, **kwargs):
        '''
        赋分后会调用该方法
        '''
        pass

    def assignError(self,
                    index: int,
                    img,
                    time_frame,
                    object,
                    preds=None,
                    num_frame=None,
                    conf=0.6,
                    name_save=None,
                    *args,
                    **kwargs):
        if num_frame is None:
            num_frame = self.num_frame
        if name_save is None:
            name_save = f'{index}_error.jpg'
        if index not in self.faulty_score_list:
            self.faulty_score_list.append(index)  # 将该得分加入已得分数

        if preds is not None:
            self.plot(preds, img)
        # upload drawed image to minio or save to local dir
        cv2.imwrite(self.call_back_url+'error'+str(index)+'.jpg',img)
        
        '''
        print("upload test ")
        if torch.is_tensor(conf):
            conf = conf.cpu().numpy().tolist()
        dataimg = encode_image_jpg(img)
        image_url = uploaded_images(
            data_img=dataimg,
            path=self.path_save,
            filename=name_save,
            dir_local=SCORE_ROOT_PATH)
        i_index = str(index)  # self.exper_score_ids.index(str(index))
        score_now = self.config_model["faultPointInfo"][i_index]

        if self.is_mp4:
            time_client = int(time_frame)
        else:
            time_client = ts2ft(time_frame / 1000)
        score_one_origin = {
            "id": i_index,
            "score_status": True,
            "str_pts": score_now["info"],
            "images_url": image_url,
            "time": time_client,
            "conf": conf,
            "frame_num": num_frame,
            "object": []
        }

        self.jsonResultScore["error_pts_info"][
            i_index] = score_one_origin  # object
        # call callback server ,sent now score to client and save to redis
        upload_redis_or_save_json_local(
            jsonScoreNow=self.jsonResultScore,
            path=self.path_save,
            call_back_url=self.real_back_url,
            filename="scoreinfo.json",
            dir_local=SCORE_ROOT_PATH,
            up_callback=self.real_status,
            file_lock=self.file_lock)
        self.post_error(index, img, time_frame, object, preds, num_frame, conf,
                        name_save, *args, **kwargs)
        '''
        return True

    def post_error(self, index, img, time_frame, object, preds, num_frame,
                   conf, name_save, *args, **kwargs):
        """
        错误点赋分后调用

        """
        ...

    def retracementScore(self, index, *args, **kwargs):  # 回撤分数
        if index in self.score_list:
            self.score_list.remove(index)
        if str(index) not in self.exper_score_ids:
            exec(f'self.scorePoint{index} = False')  # 将该得分点设置为True 不在判断该得分点
            return
        i_index = self.exper_score_ids.index(str(index))
        self.jsonResultScore["score_pts_info"][i_index]["score_status"] = True
        # call callback server ,sent now score to client and save to redis
        upload_redis_or_save_json_local(
            jsonScoreNow=self.jsonResultScore,
            path=self.path_save,
            call_back_url=self.real_back_url,
            filename="scoreinfo.json",
            dir_local=SCORE_ROOT_PATH,
            up_callback=self.real_status)
        # up_callback=not self.is_mp4)
        # exec(f'self.scorePoint{index} = False')
        self.post_retrace(index, *args, **kwargs)
        return True

    def post_retrace(self, index, *args, **kwargs):
        '''
        撤回分数后会调用该方法
        :param index:
        :return:
        '''
        pass

    def end_video_sent(self):
        try:
            self.end()
        except:
            logger.error(traceback.format_exc())
        upload_redis_or_save_json_local(
            jsonScoreNow=self.jsonResultScore,
            path=self.path_save,
            call_back_url=self.call_back_url,
            filename="scoreinfo.json",
            dir_local=SCORE_ROOT_PATH,
            file_lock=self.file_lock)
        if self.video_status:
            self.rtmp_release_fun()

    def assign_labels(self, imgOne, predsOne, label_names):
        '''#COMMENT BY HUBOHENG
        predsOne: torch tensor of boxes,[xmin,ymin,xmax,ymax,score,class],
          for example 
            [[100,100,200,200,0.95,0],
             [300,300,400,400,0.9,1],]
        label_names: your class labels 
          for example
            ['头',  '光源_前视',  '光屏_前视', '光源板_前视',  '光具座_前视',  '凸透镜_前视', 
             '像_前视',  '桌面整洁_前视', '光源_顶视', '光屏_顶视', '光源板_顶视', '像_顶视', 
             '光具座_顶视', '凸透镜_顶视',  '桌面整洁_顶视',  '凸透镜_镜身_前视', '光屏_屏身_前视']
        '''
        label_rect_info = []
        objects = []
        # for item_label in self.config_model["labelInfo"]:
        for item_label in self.config_model["modelInfo"].keys():
            #print('item_label',item_label)
            if "index" in self.config_model["modelInfo"][item_label].keys():
                i = self.config_model["modelInfo"][item_label]["index"]
            else:
                i = label_names.index(item_label)
            max_cn = self.config_model["modelInfo"][item_label]["max_cn"]
            #print('max_cn',max_cn)
            conf_thresh = self.config_model["modelInfo"][item_label]["conf"]
            if predsOne is None:
                ca = torch.tensor([])
            else:
                #print(i)
                ca = predsOne[predsOne[:, -1] == i]
                #print(ca)
                ca = ca[ca[:, 4] > conf_thresh]
                #print(ca.dtype)
                if max_cn != 0 and ca.shape[0] > max_cn:
                    ca = ca[ca[:, 4].argsort(descending=True)][:max_cn]
                    #ca = ca[np.argsort(-ca[:, 4])][:max_cn]
                #print(ca)
                if ca.shape[0] != 0:
                    xyxycpu = []
                    confcpu = []
                    for *xyxy, in ca:
                        xyxycpu.append([
                            xyxy[0].cpu().numpy().tolist(),
                            xyxy[1].cpu().numpy().tolist(),
                            xyxy[2].cpu().numpy().tolist(),
                            xyxy[3].cpu().numpy().tolist()
                        ])
                        confcpu.append(xyxy[4].cpu().numpy().tolist())
                    objects.append({
                        "cls": item_label,
                        "pos": xyxycpu,
                        "conf": confcpu
                    })
            label_rect_info.append(ca)
        return label_rect_info, objects

    def rtmp_push_fun(self,
                      top_img=None,
                      front_img=None,
                      side_img=None,
                      top_preds=None,
                      front_preds=None,
                      side_preds=None):
        if self.video_status:
            if "top" in self.cam_use:
                if top_preds is not None:
                    self.plot(top_preds, top_img)
                if self.rtmp_top is not None:
                    self.rtmp_top.write_img_ffmpeg(top_img)
                elif self.shape_top is not None:
                    self.rtmp_top = FfmpegRtmp(
                        rtmpurl=configg.get_rtmp_video_url(),
                        appname="EXPID_" + self.experiment_id_now,
                        rtmpfile="STDID_" + self.student_flag + "_top",
                        width=self.shape_top[1],
                        height=self.shape_top[0])
            if "side" in self.cam_use:
                if side_preds is not None:
                    self.plot(side_preds, side_img)
                if self.rtmp_side is not None:
                    self.rtmp_side.write_img_ffmpeg(side_img)
                elif self.shape_side is not None:
                    self.rtmp_side = FfmpegRtmp(
                        rtmpurl=configg.get_rtmp_video_url(),
                        appname="EXPID_" + self.experiment_id_now,
                        rtmpfile="STDID_" + self.student_flag + "_side",
                        width=self.shape_side[1],
                        height=self.shape_side[0])
            if "front" in self.cam_use:
                if front_preds is not None:
                    self.plot(front_preds, front_img)
                if self.rtmp_front is not None:
                    self.rtmp_front.write_img_ffmpeg(front_img)
                elif self.shape_front is not None:
                    self.rtmp_front = FfmpegRtmp(
                        rtmpurl=configg.get_rtmp_video_url(),
                        appname="EXPID_" + self.experiment_id_now,
                        rtmpfile="STDID_" + self.student_flag + "_top",
                        width=self.shape_front[1],
                        height=self.shape_front[0])

    def rtmp_release_fun(self):
        if "top" in self.cam_use:
            if self.rtmp_top != None:
                self.rtmp_top.release_pipe_ffmpeg()
        if "side" in self.cam_use:
            if self.rtmp_side is not None:
                self.rtmp_side.release_pipe_ffmpeg()
        if "front" in self.cam_use:
            if self.rtmp_front is not None:
                self.rtmp_front.release_pipe_ffmpeg()

    def run_one_result_process(
            self, frame_top, frame_front, frame_side, pred_top, pred_front,
            pred_side, time_top, time_front, time_side, num_frame_top,
            num_frame_front, num_frame_side, path_save, names_label):
        self.time_top = time_top
        self.time_front = time_front
        self.time_side = time_side
        self.num_frame_top = num_frame_top
        self.num_frame_front = num_frame_front
        self.num_frame_side = num_frame_side
        self.frame_top = frame_top
        self.frame_front = frame_front
        self.frame_side = frame_side

        front_true = False
        top_true = False
        side_true = False
        if self.time_top:
            self.secs = self.time_top / 1000
            self.num_frame = self.num_frame_top
        elif self.time_front:
            self.secs = self.time_front / 1000
            self.num_frame = self.num_frame_front
        elif self.time_side:
            self.secs = self.time_side / 1000
            self.num_frame = self.num_frame_side

        if not self.set_center_area:  # 设置操作区域
            self.setCenterArea(est, esf, ess, pred_top, pred_front, pred_side)

        n = 0
        for cam in self.cam_use:
            if cam == "top" and pred_top != None and pred_top.shape[0]:
                self.preds_top, self.objects_top = self.assign_labels(
                    frame_top, pred_top, names_label)
                top_true = True
                n += 1
            elif cam == "front" and pred_front != None and pred_front.shape[0]:
                self.preds_front, self.objects_front = self.assign_labels(
                    frame_front, pred_front, names_label)
                front_true = True
                n += 1
            elif cam == 'side' and pred_side != None and pred_side.shape[0]:
                self.preds_side, self.objects_side = self.assign_labels(
                    frame_side, pred_side, names_label)
                side_true = True
                n += 1

        self.rtmp_push_fun(
            top_img=frame_top,
            front_img=frame_front,
            side_img=frame_side,
            top_preds=self.preds_top,
            front_preds=self.preds_front,
            side_preds=self.preds_side)

        if n != len(self.cam_use):  # 有空值
            return

        try:
            self.score_process(top_true, front_true, side_true)  # 进入赋分逻辑
        except:
            logger.error(traceback.format_exc())

    def setCenterArea(self,
                      est,
                      esf,
                      ess,
                      pred_top,
                      pred_front,
                      pred_side=None):  # 设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
        for cam in self.cam_use:
            if cam == 'top':
                if self.frame_top is None:
                    return
                self.h_top, self.w_top = self.frame_top.shape[:2]
                if pred_top is not None:
                    self.device = pred_top.device
                self.center_area_top = (
                    np.array(est) * [self.w_top, self.h_top]).astype(np.int32)
            elif cam == 'front':
                if self.frame_front is None:
                    return
                self.h_front, self.w_front = self.frame_front.shape[:2]
                if pred_front is not None:
                    self.device = pred_front.device
                self.center_area_front = (
                    np.array(esf) * [self.w_front, self.h_front]).astype(
                        np.int32)
            elif cam == 'side':
                if self.frame_side is None:
                    return
                self.h_side, self.w_side = self.frame_side.shape[:2]
                if pred_side is not None:
                    self.device = pred_side.device
                self.center_area_side = (
                    np.array(ess) * [self.w_side, self.h_side]).astype(
                        np.int32)
        self.set_center_area = True

    def score_process(self, top_true, front_true, side_true):
        '''
        该方法为赋分过程，图片每一帧都会调用该方法
        :return:
        '''
        ...

    def desk_is_clearn(self, views_items=None, center_areas=None, views=None):
        if views is None:
            for view_items, center_box in zip(views_items, center_areas):
                for items in view_items:
                    if items.shape[0] != 0:
                        for item in items:
                            item_box = item[:4]
                            if pt_in_polygon(center_point(item_box), center_box) > 0:
                                return False
            return True
        else:
            for view, view_items, center_box in zip(views, views_items, center_areas):
                for items in view_items:
                    for item in items:
                        item_box = item[:4]
                        if view == "front":
                            if (pt_in_polygon(center_point(item_box), center_box) > 0
                                    and self.h_front - item_box[3] > self.h_front * 0.15):
                                return False
                        elif pt_in_polygon(center_point(item_box), center_box) > 0:
                            return False
            return True

    def duration(self,
                 first_secs,
                 duration_secs,
                 pre_secs=None,
                 reclock_secs=None):
        '''
        持续时间判断
        :param first_secs: 第一次记录一个动作的起始时间 单位： 秒
        :param duration_secs: 该动作需要持续的时间 单位： 秒
        :param pre_secs: # 上一次记录该动作时的时间 单位： 秒
        :param reclock_secs: # 两次记录超过该时间需要重新计算 单位： 秒
        :return: first_secs: 第一次记录时的时间 pre_secs 前一次记录时的时间 flag 是否满足条件
        '''
        if reclock_secs:
            if pre_secs == 0 or self.secs - pre_secs > reclock_secs:  # 从上次记录到现在没有此动作时间超过设置时间 重新计时
                first_secs = pre_secs = 0
            else:
                pre_secs = self.secs
        if first_secs == 0:
            if reclock_secs:
                first_secs = pre_secs = self.secs
            else:
                first_secs = self.secs
            return first_secs, pre_secs, False
        elif self.secs - first_secs > duration_secs:  # 从第一次记录到现在是否满足持续时间
            return first_secs, pre_secs, True
        else:
            return first_secs, pre_secs, False

    def end(self):
        '''
         实验结束时会调用该方法
        :return:
        '''
        return
