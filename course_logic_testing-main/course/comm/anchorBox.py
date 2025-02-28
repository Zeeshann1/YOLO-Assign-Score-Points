#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2021/3/11 12:43
# @Author: qiguangnan
# @FileName: anchorBox.py
import torch
import numpy as np
import math
import cv2
from shapely.geometry import LineString
from shapely.geometry import Point
from copy import deepcopy

def width(box): # 框宽
    return box[2] - box[0]

def high(box): # 框高
    return box[3] - box[1]

def box_area(box):  # 框面积
    return (box[2] - box[0]) * (box[3] - box[1])


def w_h_ratio(box): # 宽高比
    return (box[2] - box[0]) / (box[3] - box[1])

def box1_in_box2(box1, box2):
    return box1[0] > box2[0] and box1[1] > box2[1] and box1[2] < box2[2] and box1[3] < box2[3]

def distance_point(point1, point2): # 点的距离
    return math.hypot((point1[0] - point2[0]), (point1[1] - point2[1]))

def distance_box(box1, box2): # 两个框中心点距离
    center1 = center_point(box1)
    center2 = center_point(box2)
    return math.hypot((center1[0] - center2[0]), (center1[1] - center2[1]))

def iou(box1, box2, ratio=False): # 两个框iou(面积)
    if isinstance(box1, torch.Tensor):
        inter = (torch.min(box1[2:], box2[2:]) - torch.max(box1[:2], box2[:2])).clamp(0).prod()
    elif isinstance(box1, np.ndarray):
        inter = (np.minimum(box1[2:], box2[2:]) - np.maximum(box1[:2], box2[:2])).clip(0).prod()
    else:
        inter = max(min(box1[2], box2[2]) - max(box1[0], box2[0]), 0) * max(
            min(box1[3], box2[3]) - max(box1[1], box2[1]), 0)
    if ratio:
        area1 = box_area(box1)
        area2 = box_area(box2)
        return inter / (area1 + area2 - inter)
    else:
        return inter

def iou_min(box1, box2): # 两个框iou(面积)
    if isinstance(box1, torch.Tensor):
        inter = (torch.min(box1[2:], box2[2:]) - torch.max(box1[:2], box2[:2])).clamp(0).prod()
    elif isinstance(box1, np.ndarray):
        inter = (np.minimum(box1[2:], box2[2:]) - np.maximum(box1[:2], box2[:2])).clip(0).prod()
    else:
        inter = max(min(box1[2], box2[2]) - max(box1[0], box2[0]), 0) * max(
            min(box1[3], box2[3]) - max(box1[1], box2[1]), 0)
    area1 = box_area(box1)
    area2 = box_area(box2)
    return inter / min(area1, area2)

def plot_one_box(x, img, color=None, label=None, line_thickness=None):  ## 绘制一个box
    tl = line_thickness  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, line_thickness, cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

def combineBox(*boxes): # 获取几个检测框合并后的检测框
    combin_box = None
    for box in boxes:
        if combin_box is None:
            combin_box = deepcopy(box)
        else:
            if box[0] < combin_box[0]:
                combin_box[0] = box[0]
            if box[1] < combin_box[1]:
                combin_box[1] = box[1]
            if box[2] > combin_box[2]:
                combin_box[2] = box[2]
            if box[3] > combin_box[3]:
                combin_box[3] = box[3]
    return combin_box

def box_container(box1, box2):
    pt_lu = (box1[0]+5, box1[1]+5)
    pt_rd = (box1[2]-5, box1[3]-5)
    return pt_in_box(pt_lu,box2) and pt_in_box(pt_rd,box2)

def separate_left_right(box1, box2):  # 从镜头方向看
    if center_distance_h(box1, box2) < 0:
        return (box1, box2)
    else:
        return (box2, box1)


def pt_in_box(pt, box):
    return not (bool(pt[0] < box[0]) or bool(pt[0] > box[2]) or bool(pt[1] < box[1]) or bool(pt[1] > box[3]))


def pt_in_polygon(point, polygonPoints):  ## 判断点是否在多边形中
    '''
    判断坐标点是否在多边形区域中
    原理：该坐标点向左水平的射线与多边型的边有 n 个交点，如果 n 为奇数则说明该点在多边形中，n 为偶数则不在多边形中
    :param point: 点坐标
    :param pointList: list [(lon, lat)...] 多边形点的顺序需根据顺时针或逆时针，不能乱
    '''
    iCount = len(polygonPoints)
    assert iCount > 2
    x, y = point

    ## 计算多边型的最大最小x y 坐标，如果坐标点超出了最大最小经坐标则一定不再多边型中
    if isinstance(polygonPoints, torch.Tensor):
        [maxX, maxY], _ = torch.max(polygonPoints, 0)
        [minX, minY], _ = torch.min(polygonPoints, 0)
    elif isinstance(polygonPoints, np.ndarray):
        maxX, maxY = np.max(polygonPoints, axis=0)
        minX, minY = np.min(polygonPoints, axis=0)
    else:
        maxX = max(polygonPoints)[0]
        minX = min(polygonPoints)[0]
        maxY = max(polygonPoints, key=lambda x: x[1])[1]
        minY = min(polygonPoints, key=lambda x: x[1])[1]
    if x > maxX or x < minX or y > maxY or y < minY:
        return False
    iSum = 0
    for i in range(iCount):
        x1, y1 = polygonPoints[i]
        x2, y2 = polygonPoints[0] if (i == iCount - 1) else polygonPoints[i + 1]
        if ((y > y1) and (y < y2)) or ((y > y2) and (y < y1)):  ## y在两点y之间 否则无交点
            if x <= min(x1, x2): ## x < 两点最小x，在线段左边，无交点,
                continue
            elif x > max(x1, x2): ## x >= 两点最大x，必有交点
                iSum += 1
                continue
            else:  ## x在两点 x 之间
                pX = x1 - (x1 - x2) * (y1 - y) / (y1 - y2)  ## 利用等比算出坐标点水平线与两坐标点线段的交点的 x
                if (pX <= x):  ## 如果交点x <= 坐标点x， 与坐标点向左射线有交点
                    iSum += 1

    return True if iSum % 2 != 0 else False


def center_distance_v(box1, box2, abs_v=False):  # 垂直方向中心点距离
    dis = float(box1[3] + box1[1] - box2[3] - box2[1]) / 2
    return abs(dis) if abs_v else dis

def center_distance_h(box1, box2, abs_v=False):  # 水平方向中心距离
    dis = float(box1[2] + box1[0] - box2[2] - box2[0]) / 2
    return abs(dis) if abs_v else dis


def center_point(box):
    return float(box[2] + box[0]) / 2, float(box[3] + box[1]) / 2


def min_dis_boxes(box1, box2): # 两个不相交矩形的最短距离 左上右下
    x11, y11, x12, y12 = box1
    x21, y21, x22, y22 = box2
    if x12 < x21:
        if y12 < y21:
            return math.hypot(x21 - x12, y21 - y12)
        elif y11 > y22:
            return math.hypot(x21 - x12, y11 - y22)
        else:
            return x21 - x12
    elif x11 > x22:
        if y12 < y21:
            return math.hypot(x11 - x22, y21 - y12)
        elif y11 > y22:
            return math.hypot(x11 - x22, y11 - y22)
        else:
            return x11 - x22
    elif y11 > y22:
        return y11 - y22
    else:
        return y21 - y12


def separate(pred):  ## 区分左右
    if pred.shape[0] == 0:
        left = right = None
    elif pred.shape[0] == 1:
        if pred[0][0] > 960:
            left = pred[0][:4]
            right = None
        else:
            right = pred[0][:4]
            left = None
    else:
        right, left = pred[pred[:, 0].argsort()][:, :4]

    return left, right

def iscrosses(line1, line2):  # line1=[[1,1],[0,0]]
    if LineString(line1).crosses(LineString(line2)):
        return True
    return False
def adjoin(box1, box2):  # x1y1x2y2,box1在下方，box2在上方
    flg = False
    if box1[1] > box2[1]:
        # center = [(box1[0]+(box1[2]/2)), (box1[1]+(box1[3]/2))]
        # line1 = [[(box1[0]+(box1[2]/2)), 0], center]
        # line2 = [[box2[0], box2[1]], [box2[0]+box2[2], box2[1]]]
        # flg = iscrosses(line1, line2)
        center = [((box1[2] - box1[0])/2 + box1[0]), ((box1[3] - box1[1])/2 + box1[1])]
        line1 = [[((box1[2] - box1[0])/2 + box1[0]), 0], center]
        line2 = [[box2[0], box2[1]], [box2[2], box2[3]]]
        flg = iscrosses(line1, line2)

    return flg

# def get_point_line_distance(self, point, line):
#     point_x = point[0]
#     point_y = point[1]
#     line_s_x = line[0][0]
#     line_s_y = line[0][1]
#     line_e_x = line[1][0]
#     line_e_y = line[1][1]
#     #若直线与y轴平行，则距离为点的x坐标与直线上任意一点的x坐标差值的绝对值
#     if line_e_x - line_s_x == 0:
#         return math.fabs(point_x - line_s_x)
#     #若直线与x轴平行，则距离为点的y坐标与直线上任意一点的y坐标差值的绝对值
#     if line_e_y - line_s_y == 0:
#         return math.fabs(point_y - line_s_y)
#     #斜率
#     k = (line_e_y - line_s_y) / (line_e_x - line_s_x)
#     #截距
#     b = line_s_y - k * line_s_x
#     #带入公式得到距离dis
#     dis = math.fabs(k * point_x - point_y + b) / math.pow(k * k + 1, 0.5)
#     return dis

# box2右下点到box1斜边的距离，前视摄像头
def beaker_glass_rod_tool(box1, box2):  # box1 glass_rod, box2 beaker
    beaker_point_x, beaker_point_y = box2[0], box2[3]
    line_x1, line_y1 = box1[0], box1[1]
    line_x2, line_y2 = box1[2], box1[3]
    if line_x1 - line_x2 == 0:
        return math.fabs(beaker_point_x - line_x1)
    if line_y1 - line_y2 == 0:
        return math.fabs(beaker_point_y - line_y1)
    # 斜率
    k = (line_y2 - line_y1) / (line_x2 - line_x1)
    # 结局
    b = line_y1 - k * line_x1
    dis = math.fabs(k * beaker_point_x - beaker_point_y + b) / math.pow(k * k + 1, 0.5)
    # A = line_y2 - line_y1
    # B = line_x1 - line_x2
    # C = line_x1 * (line_y1 - line_y2) + line_y1 * (line_x2 - line_x1)
    # dis = np.abs(A * beaker_point_x + B * beaker_point_y + C) / (np.sqrt(A ** 2 + B ** 2))
    return dis


if __name__ == '__main__':
    # box1 = np.array([100, 100, 200, 200])
    # box2 = np.array([300, 300, 400, 400])

    box3 = torch.tensor([0, 0, 100, 100])
    box4 = torch.tensor([0, 0, 50, 50])
    #
    # box5 = [100, 100, 200, 200]
    # box6 = [50, 0, 250, 150]

    # print(iou(box1, box2))
    # print(float(iou(box3, box4)))
    # print(iou(box5, box6))

    # print(center_distance_h(box3, box4))

    # print(center(box1))
    print(box_container(box4, box3))
