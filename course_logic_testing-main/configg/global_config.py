# -*- coding:utf-8 -*-
import os.path
import platform
import shutil
from enum import Enum

SYSTEM_NOW = platform.system()

GLOBAL_NUM_ONEMODELDETECT = 1  # 每个模型处理的学生终端个数（仅对视频流有用）
GLOBAL_NUM_ONEDEVICELOAD = 2  # 每块显卡加载的模型个数
GLOBAL_STEP_MP4 = 2  # 视频文件处理时的抽帧间隔
GLOBAL_RTSP_SEC_THR = 120  # 认为实时视频接受到任务到开始处理时间超过该值，就需以视频文件请求

#gpu decode set
GLOBAL_GPU_DECODE = True  # 是否开启GPU做硬解码, default False;  服务器发行版本设为True

GLOBAL_USE_RTMP = True  # 是否需要将模型检测的结果，画图后通过视频流返回；True 返回，False 不返回
GLOBAL_USE_MULTI_THREAD = True  # 视频流是否使用多线程，多线程情况下imshow无法工作，调试状态可以设置为False

#delete download mp4 file
GLOBAL_DELETE_DOWNLOAD_MP4 = True  #是否在赋分后删除下载文件；默认为True。注意：如果临时需要修改为False,后续需及时清理并关注磁盘大小，避免磁盘空间用尽

# model Type set
GLOBAL_is_user_all_model_type = True  # 是否所有模型都用同一种类型   ;default False ； 发布版本（如服务器版本），必须设置为True
GLOBAL_all_model_type_name = 'Tensorrt6'  # "yolo" or "openvino" or  "Tensorrt6" or  'YoloPoint': default 'YoloPoint'

OPENVINO_VERSION = 2022  #openvino版本选择
OPENVINO_DEVICE = 'GPU'  #['AUTO','CPU','GPU'],如果是AUTO类型加载模型比较快，但是刚开始检测比较慢，大概10s之后就恢复正常性能，GPU加载模型比较慢

# 一代小白试验区参数 区域为多边形
# experimental_site_top = [[0.32362939, 0.95833333], [0.32637061, 0.53679337],
#                          [0.3839364, 0.44785575], [0.66217105, 0.44785575],
#                          [0.72590461, 0.53557505], [0.72590461, 0.96807992]]
# experimental_site_side = [[0.48878838, 0.15789474], [0.45315241, 0.22002924],
#                           [0.3935307, 0.69152047], [0.4517818, 0.79020468],
#                           [0.83623904, 0.75609162], [0.71219846, 0.16398635]]
# experimental_site_front = [[0.26949013, 0.01291423], [0.72453399, 0.01169591],
#                            [0.82390351, 0.73659844], [0.74714912, 0.85721248],
#                            [0.22288925, 0.85477583], [0.13654057, 0.75121832]]

# 二代小白试验区参数 区域为多边形
experimental_site_top = [[0.2, 1.0], [0.2, 0.62], [0.21, 0.55], [0.23, 0.51],
                         [0.26, 0.48], [0.3, 0.46], [0.7, 0.46], [0.74, 0.48],
                         [0.77, 0.51], [0.79, 0.55], [0.8, 0.62], [0.8, 1.0]]
experimental_site_side = [[0.75, 0.25], [0.53, 0.25], [0.505, 0.259],
                          [0.485, 0.292], [0.476, 0.674], [0.493, 0.753],
                          [0.536, 0.802], [0.885, 0.802]]
experimental_site_front = [[0.223, 0.], [0.223, 0.66], [0.235, 0.715],
                           [0.263, 0.76], [0.305, 0.79], [0.344, 0.80],
                           [0.656, 0.80], [0.695, 0.79], [0.737, 0.76],
                           [0.765, 0.715], [0.777, 0.66], [0.777, 0.]]


class status_return(Enum):
    OK = 0
    SERVER_is_busy = 1
    ERROR_data_received = 2
    ERROR_rtsp_failed = 3
    ERROR_model_not_exist = 4
    ERROR_Mp4_download_failed = 5
    ERROR_Callback_failed = 6


SAVE_RESULT_LOCAL = True  #将图片保存在本地true,否则上传minio
GLOBAL_USE_NGINXURL = True  #True --本地图片结果返回时用静态文件url,否则用base64data； 魔盒集群需设置为true

QUALITY_JPG = 60
PORT = 5000  ## API 端口
if SYSTEM_NOW == "Linux":
    APACHE_DIR = "/var/"  # apache httpd 根路径
    SCORE_ROOT_PATH = "/var/"  ## 分数存储目录
else:
    APACHE_DIR = "D:\\"  # "'/var/www/html'  # apache httpd 根路径
    SCORE_ROOT_PATH = "D:\\"  # "/var/www/html"  ## 分数存储目录


class global_var:
    # minio_url = "192.168.12.159:9000/"
    # access_key = "xdai"
    # secret_key = "xdaiasdfghjkl"

    # minio_url = "minio.shxidsy.net/"
    minio_url = "192.168.1.143:8091/"

    access_key = "xidinguser"
    secret_key = "U2FsdGVkX1/7uyvj0trCzSNFsfDZ66dMSAEZjNlvW1c="
    # redis_queue_response = redis.Redis(host='localhost', port=55000, password="", db=0)
    if SYSTEM_NOW == "Linux":
    #if 0:
        #redis_url_host = "172.17.0.1"  # 算法本机docker用
        redis_url_host = "127.0.0.1"  # 算法本机redis用
        # redis_url_host = "192.168.1.172"  # 公司测试服务器用
        #redis_url_host = "192.168.12.186"  # 186本机专用
        redis_port = 6379
    else:
        redis_url_host = "192.168.12.159"
        redis_port = 55000
        # redis_url_host = "192.168.12.186"
        # redis_port = 6379
    #
    redis_password = ""  # local machine for test
    # redis_password = "1qaz@WSX"   # 教学系统端提供
    redis_db_model_info = 11
    redis_db_ai_result = 12
    redis_db_ai_task = 13
    redis_db_ai_stop = 14
    redis_db_realtime_info = 15
    redis_db_part_info = 11

    #rtmp_video_info
    rtmp_video_url = "rtmp://192.168.1.194/"


def get_rtmp_video_url():
    return global_var.rtmp_video_url


def get_minio_url():
    return global_var.minio_url


def get_minio_access_key():
    return global_var.access_key


def get_minio_secret_key():
    return global_var.secret_key


def get_redis_url_host():
    return global_var.redis_url_host


def get_redis_port():
    return global_var.redis_port


def get_redis_password():
    return global_var.redis_password


def get_redis_db_model_info():
    return global_var.redis_db_model_info


def get_redis_db_ai_result():
    return global_var.redis_db_ai_result


def get_redis_db_ai_task():
    return global_var.redis_db_ai_task


def get_redis_db_ai_stop():
    return global_var.redis_db_ai_stop


def get_redis_db_realtime_info():
    return global_var.redis_db_realtime_info

def get_redis_db_partInfo_info():
    return global_var.redis_db_part_info

def create_root_save_path():
    paths = SCORE_ROOT_PATH.split("/")
    temp_path = ""
    for index, p in enumerate(paths):
        if index == 0:
            temp_path = os.path.join("/", p)
        else:
            temp_path = os.path.join(temp_path, p)
            if not os.path.exists(temp_path):
                os.mkdir(temp_path)


def create_new_student_flag_dir(pathflag):
    path_student = os.path.join(SCORE_ROOT_PATH, pathflag)
    try:
        if os.path.exists(path_student):
            if os.path.isdir(path_student):
                shutil.rmtree(path_student)
            else:
                os.remove(path_student)
        os.mkdir(path_student)
    except Exception as e:
        print("created init save dir failed{}{}".format(path_student, e))
