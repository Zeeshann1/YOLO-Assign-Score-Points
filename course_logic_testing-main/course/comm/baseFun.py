import time
import math
import traceback
import cv2
import numpy as np
import json
from scipy import stats
from pathlib import Path
from tqdm import tqdm


def try_decorator(func):
    def try_fun(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            traceback.print_exc()
    return try_fun

def best_angle(img, direction, keral, n_div, scale=1.0, angle_center=None, angle_sum=0., sum_list=None, img_best=None,
               convolve=False, con_k=20):
    """
    :param img: 灰度图片，经过边缘过滤的
    :param direction: 位置，水平方向为0， 垂直方向为1
    :param keral: 在direction方向上腐蚀核的大小 int
    :param n_div: 多少个值
    :param scale: 比例因子  开始位置 * 比例因子 = 开始角度
    :param angle_center: 中心角度
    :param angle_sum: 中心角度的累加和
    :param sum_list: 累加列表
    :param convolve: 是否用卷积计算区间累加
    :param con_k: 用卷积计算区间累加时，卷积的大小
    :return:
    """
    if angle_center is None:
        skip = False
        angle_center = 0.
    else:
        skip = True
    angle = angle_center
    img_h, img_w = img.shape  ## 图片高 宽
    rotate_center = (img_w * 0.5, img_h * 0.5)  ## 旋转中心
    if direction == 0:
        kernel = np.ones((keral, 1), np.uint8).T
    else:
        kernel = np.ones((keral, 1), np.uint8)

    for r_angle in range(math.ceil(-n_div / 2), math.ceil(n_div / 2)):
        if r_angle == 0 and skip:
            continue
        r_angle = angle_center + r_angle * scale
        rotate = cv2.getRotationMatrix2D(rotate_center, r_angle, 1)
        rotate_img = cv2.warpAffine(img, rotate, (img_w, img_h))  ## 旋转
        rotate_erode_img = cv2.erode(rotate_img, kernel, iterations=1)  ## 腐蚀
        sum_list_ = np.sum(rotate_erode_img, axis=1 - direction)
        if convolve:
            sum_list_ = np.convolve(sum_list_, np.ones(con_k, dtype=int), 'valid')
        max_v = np.max(sum_list_)  ## 计算 纵向梯度累加最大值

        if max_v > angle_sum:  ## 记录最大值的信息
            angle = r_angle
            angle_sum = max_v
            sum_list = sum_list_
            img_best = rotate_erode_img

    return angle, angle_sum, sum_list, img_best

def se_angle(img): ## 计算竖直方向的角度
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ## 计算水平方向梯度
    kernel_1 = np.array([[-1, -1, 0, 1, 1], ], np.float32)
    filter_1 = cv2.filter2D(img, -1, kernel_1)
    kernel_2 = np.array([[1, 1, 0, -1, -1], ], np.float32)
    filter_2 = cv2.filter2D(img, -1, kernel_2)
    filter_img = (filter_1 + filter_2)
    filter_img = cv2.copyMakeBorder(filter_img, 20, 20, 0, 0, cv2.BORDER_CONSTANT, value=0)  ## 图片上下加黑框

    angle, angle_sum, sum_list, img_best = best_angle(filter_img, 1, 10, 7, 5)
    angle, angle_sum, sum_list, img_best = best_angle(filter_img, 1, 10, 5, 2, angle, angle_sum, sum_list, img_best)
    angle, angle_sum, sum_list, img_best = best_angle(filter_img, 1, 10, 3, 1, angle, angle_sum, sum_list, img_best)

    return angle, img_best


def tan(angle):  ## 三角函数 tan
    return math.tan(math.pi * angle / 180)


## 坐标旋转
def p_rotate(centralp, point, angle):  ## 点旋转
    if angle == 0:
        return point
    angle = math.pi * angle / 180
    p_x, p_y = point[0], point[1]
    centralp_x, centralp_y = centralp[0], centralp[1]
    rotatex = (p_y - centralp_y) * math.sin(angle) + (p_x - centralp_x) * math.cos(angle) + centralp_x
    rotatey = (p_y - centralp_y) * math.cos(angle) - (p_x - centralp_x) * math.sin(angle) + centralp_y

    return rotatex, rotatey


## 展示图片
def cv_show(img, name='img', wait=0):
    cv2.imshow(name, img)
    cv2.waitKey(wait)
    cv2.destroyAllWindows()


def match(template, target):  ## 图片匹配
    height, width = template.shape[:2]
    result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    strmin_val = str(min_val)
    cv2.rectangle(target, min_loc, (min_loc[0] + width, min_loc[1] + height), (0, 0, 225), 2)

    print((min_loc[1] + height) / 2)

    cv2.imshow("MatchResult----MatchingValue=" + strmin_val, target)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cross_point(line1, line2):  # 两直线交点
    x1, y1, x2, y2 = line1  # 取四点坐标
    x3, y3, x4, y4 = line2

    if (y2 - y1) * (x4 - x3) == (y4 - y3) * (x2 - x1):  ## 平行 无交点
        return None

    if x2 != x1:  ## line1存在斜率
        k1 = (y2 - y1) / (x2 - x1)  # 计算斜率
        b1 = y1 - x1 * k1
        if x4 == x3:  # L2直线斜率不存在
            k2 = None
            b2 = 0
        else:
            k2 = (y4 - y3) / (x4 - x3)  # 斜率存在操作
            b2 = y3 - x3 * k2
        if k2 == None:
            x = x3
        else:
            x = (b2 - b1) / (k1 - k2)
        y = k1 * x + b1
        return x, y

    else:  ## line1不存在斜率
        k2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - x3 * k2
        return x1, k2 * x1 + b2


def distance2line(point, line_point1, line_point2):  # 计算点到直线距离
    point = np.array(point)
    line_point1 = np.array(line_point1)
    line_point2 = np.array(line_point2)
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(line_point1 - line_point2)
    return distance


def timekeeping(start, countdown:int=None):
    now = time.time()
    if countdown:
        t = countdown - int(now - start)
        if t < 0:
            return "00:00"
    else:
        t = int(now - start)
    minute = str(t // 60).rjust(2, '0')
    second = str(t % 60).rjust(2, '0')
    return minute + ":" + second

def CV(path, start=0, end=None, wait=1):
    """
    opencv读取视频
    :param path: 视频路径
    :param start: 视频开始时间
    :param end: 视频结束时间
    :param wait: 每帧等待时间
    :return: None
    """
    vc = cv2.VideoCapture(str(path))

    opened = vc.isOpened()
    if not opened:
        # cprint("视频打开错误", "red")
        return
    fps = vc.get(cv2.CAP_PROP_FPS)  ## 获取视频帧率
    count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))  ## 获取视频总帧数
    width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))  ## 获取视频宽度
    height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))  ## 获取视频高度
    # cprint(f"视频宽度: {width}, 视频高度: {height}, 视频总帧数: {count}, 视频帧率: {fps}", "cyan")

    if start:
        start_frame = min(int(start * fps), count)  # 开始帧
        vc.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  ## 设置视频的开始帧位置
    if end:
        count = min(int(end * fps), count) - start

    pbar = tqdm(total=count, desc="播放进度")  ## 进度条
    f_num = 0 ## 读取视频的帧数
    while opened:
        f_num += 1
        opened, frame = vc.read()
        if opened:
            frame = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
            cv2.imshow('result', frame)
            pbar.update(1)
            if cv2.waitKey(wait) == 27 or f_num == count:
                break
        else:
            break

    pbar.close()
    vc.release()
    cv2.destroyAllWindows()


def saveDetectResult(img, pred, path, img_n):
    pred = [item.cpu().numpy().tolist() for item in pred]
    hand_p, gel_pen_p, hook_weight_p, nut_p, spring_ergometer_p, paper_p, iron_pole_p, lever_p, slider_p, knob_p = pred
    res = {
        "hand": hand_p,
        "gel_pen": gel_pen_p,
        "hook_weight": hook_weight_p,
        "nut": nut_p,
        "spring_ergometer": spring_ergometer_p,
        "paper": paper_p,
        "iron_pole": iron_pole_p,
        "lever": lever_p,
        "slider": slider_p,
        "knob":knob_p
    }
    labels = {
        "version": "4.5.6",
        "flags": {},
        "shapes": [],
        "imagePath": None,
        "imageData": None,
        "imageHeight": 1080,
        "imageWidth": 1920
    }
    shape_tem = {
        "label": "",
        "points": [],
        "group_id": None,
        "parent_id": None,
        "shape_id": None,
        "shape_type": "rectangle",
        "flags": {}
    }
    for label, dets in res.items():
        for ps in dets:
            shape = shape_tem.copy()
            shape["label"] = label
            shape["points"] = [[ps[0], ps[1]], [ps[2], ps[3]]]
            labels["shapes"].append(shape)

    seq = str(img_n).rjust(6, "0")
    labels["imagePath"] = seq + ".jpg"
    img_path = str(Path(path) / f"{seq}.jpg")
    json_path = str(Path(path) / f"{seq}.json")
    detect_path = str(Path(path) / f"{seq}.detect")
    # cv2.imwrite(img_path, img)
    with open(json_path, 'w') as f:
        json.dump(labels, f, indent=2)
    with open(detect_path, 'w') as f:
        json.dump(res, f, indent=2)
