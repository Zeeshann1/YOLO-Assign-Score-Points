#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : j
# @Time    : 2021/11/11 14:00
# @File    : phy_measure_length_time_cou.py

import traceback
from .comm import *
from .comm.course_base import ConfigModel

# from queue import Queue
# import cv2
# import numpy as np
# from threading import Thread
# from pathlib import Path
# from util import ts2ft
from logger import logger
# from concurrent.futures import ThreadPoolExecutor
from config import experimental_site_top as est
from config import experimental_site_front as esf
# from config import EXP_MAP
import random


class PHY_measure_length_time(ConfigModel):

    def __init__(self, *args, **kwargs ):
        super(PHY_measure_length_time, self).__init__(*args, **kwargs)
        self.initScore()

    def initScore(self):
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

        #
        self.flagtime1 = 0.
        self.flagtime2 = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
        self.flagtime4 = 0.
        self.flagtime4_2 = 0.
        self.flagtime5 = 0.

        self.clearn_time = 0.
        self.clearn_desk_info = []

        self.scoreframe2 = 0
        self.scoreframe3 = 0
        self.scoreframe3_2 = 0
        self.scoreframe4 = 0

        self.set_center_box = False  # 是否设置中心区域
        self.clearn_f_num = 0.

    # def setCenterBox(self, device, est=None, esf=None):  # 设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
    #     if hasattr(self, 'top_img0') and est:
    #         self.h_top, self.w_top = self.top_img0.shape[:2]
    #         self.center_box_top = torch.tensor(
    #             [self.w_top * est[0], self.h_top * est[1], self.w_top * est[2], self.h_top * est[3]],
    #             device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
    #     if hasattr(self, 'front_img0') and esf:
    #         self.h_front, self.w_front = self.front_img0.shape[:2]
    #         self.center_box_front = torch.tensor(
    #             [self.w_front * esf[0], self.h_front * esf[1], self.w_front * esf[2], self.h_front * esf[3]],
    #             device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
    #     self.set_center_box = True

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self,top_true,front_true,side_true):  # 赋分逻辑部分
        # [self.top_preds, self.front_preds], [self.top_img0, self.front_img0] = detect_info
        #
        # if not self.set_center_box:
        #     self.setCenterBox(self.top_preds[0].device, est, esf)  # 设置中心区域
        # *-------------------------------------------------* 以下为赋分逻辑部分
        """
            主要用顶视角
        """

        hands_front, heads_front, rulers_front, stopwatchs_front, hand_ruler_objects_front, \
        hand_stopwatchs_front = self.preds_front

        hands_top, heads_top, rulers_top, stopwatchs_top, hand_ruler_objects_top, \
        hand_stopwatchs_top = self.preds_top
        try:
            # 1 根据对测量的精确程度的要求能正确选择刻度尺
            if not self.scorePoint1:
                # if stopwatchs_top.shape[0] != 0 and rulers_top.shape[0] != 0:
                #     self.make_frame(self.top_img0, stopwatchs_top[0], rulers_top[0],"你在干嘛", 0.555)
                #     self.assignScore(1, self.top_img0, self.top_preds)
                info = self.select_cale(1, hands_top, rulers_top, hand_ruler_objects_top)
                if info is not None:
                    self.assignScore(*info)

            # 2 能正确放置刻度处;对准刻度线,有刻度的一遍紧贴被测物体且与被测长度保持平行
            if not self.scorePoint2 and self.scorePoint1:
                info = self.correctly_placed(2, hand_ruler_objects_top, hands_top)
                if info is not None:
                    self.assignScore(*info)

            # 3 能准确将视线正对刻度线
            if not self.scorePoint3 and self.scorePoint2:
                info = self.sight_scale_mark(3, hand_ruler_objects_top, heads_top)
                if info is not None:
                    self.assignScore(*info)

            # 4 能正确使用停表的 归零 开始 暂停 <>
            if not self.scorePoint4:
                info = self.correctly_stopwatch(4, hands_top, stopwatchs_front, hand_stopwatchs_top, hand_stopwatchs_front)
                if info is not None:
                    self.assignScore(*info)

            # 5 实验结束后能计时整理仪器
            top_items = [rulers_top, stopwatchs_top, hand_ruler_objects_top,
                         hand_stopwatchs_top]
            front_items = [rulers_front, stopwatchs_front, hand_ruler_objects_front,
                           hand_stopwatchs_front]

            if not self.scorePoint5 and (self.scorePoint1 or self.scorePoint2 or
                                         self.scorePoint3 or self.scorePoint4):
                info = self.clearn_desk(5, top_items, front_items)
                if info is not None:
                    self.assignScore(*info)

            if self.scorePoint5 and len(self.score_list) != 5:
                if not self.desk_is_clearn([top_items], [self.center_area_top]):
                    self.retracementScore(5)
        except:
            logger.error(traceback.format_exc())

    # 1
    def select_cale(self, score_index, hands_top, rulers_top, hand_ruler_objects_top):
        """
        1 选择合适的尺子, 首先尺子在设置的中心区域,之后 手与尺子有交集;
        :param hands_top:
        :param rulers_top:
        :return:
        """
        if hands_top.shape[0] != 0 and rulers_top.shape[0] != 0:
            status = False
            for ruler_top in rulers_top:
                if pt_in_polygon(center_point(ruler_top[:4]), self.center_area_top):
                    status = True
                    break
            if status:
                hand_ruler_iou = False
                for hand_top in hands_top:
                    for ruler_top in rulers_top:
                        if iou(hand_top[:4], ruler_top[:4]) > 0:
                            hand_ruler_iou = True
                            break
                if hand_ruler_iou:
                    # 直接给分的话 有可能会他中途换了尺子,但截取到的是第一次拿尺子的图片
                    # self.flagtime1, _, flag = self.duration(self.flagtime1, 3.0)
                    # if flag:
                    #     self.scorePoint1 = True
                    #     self.assignScore(1, self.top_img0, self.top_preds)
                    if hand_ruler_objects_top.shape[0] != 0:
                        self.flagtime1, _, flag = self.duration(self.flagtime1, 3.0)
                        if flag:
                            # self.scorePoint1 = True
                            # self.assignScore(1, self.top_img0, self.top_preds)
                            return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

    # 2
    def correctly_placed(self, score_index, hand_ruler_objects_top, hands_top):
        """
        2 正确选择刻度
        :param hand_ruler_objects_top:
        :param hands_top:
        :return:
        """
        if hand_ruler_objects_top.shape[0] != 0 and hands_top.shape[0] != 0:
            status = False
            for hand_top in hands_top:
                if iou(hand_top[:4], hand_ruler_objects_top[0][:4]) > 0:
                    status = True
                    break
            if status:
                self.flagtime2, _, flag = self.duration(self.flagtime2, 3.0)
                if flag:
                    # self.scorePoint2 = True
                    # self.assignScore(2, self.top_img0, self.top_preds)
                    return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

    # 3
    def sight_scale_mark(self, score_index, hand_ruler_objects_top, heads_top):
        """
        3视线正对刻度线
        :param hand_ruler_objects_top:
        :param heads_top:
        :return:
        """
        if hand_ruler_objects_top.shape[0] != 0 and heads_top.shape[0] != 0:
            status = False

            for head_top in heads_top:
                head_hro_iou = iou(hand_ruler_objects_top[0][:4], head_top[:4], True)
                if head_hro_iou > 0.1:
                    status = True
            if status:
                self.flagtime3, _, flag = self.duration(self.flagtime3, 1.0)
                if flag:
                    # self.scorePoint3 = True
                    # self.assignScore(3, self.top_img0, self.top_preds)
                    return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

        if not self.scorePoint3 and hand_ruler_objects_top.shape[0] == 0 and heads_top.shape[0] != 0:
            self.flagtime3_2, _, flag = self.duration(self.flagtime3_2, 1.0)
            if flag:
                # self.scorePoint3 = True
                # self.assignScore(3, self.top_img0, self.top_preds)
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

    # 4
    def correctly_stopwatch(self, score_index, hands_top, stopwatchs_top, hand_stopwatchs_top, hand_stopwatchs_front):
        """
        4 正确使用停表
        :param hands_top:
        :param stopwatchs_front:
        :param hand_stopwatchs_top:
        :return:
        """
        if hands_top.shape[0] != 0 and stopwatchs_top.shape[0] != 0:
            flag4 = False
            for hand_top in hands_top:
                hand_stopwatch_iou = iou(hand_top[:4], stopwatchs_top[0][:4])
                stopwatch_pos = pt_in_polygon(center_point(stopwatchs_top[0][:4]), self.center_area_top)
                if hand_stopwatch_iou > 0.9 * box_area(stopwatchs_top[0][:4]) and stopwatch_pos:
                    flag4 = True
                    break
            if flag4:
                # if self.scoreframe4 > 20:
                #     self.scorePoint4 = True
                #     self.assignScore(4, self.top_img0, self.top_preds)
                #     self.scoreframe4 = 0
                # else:
                #     self.scoreframe4 += 1

                self.flagtime4, _, flag = self.duration(self.flagtime4, 1.0)
                if flag:
                    # self.scorePoint4 = True
                    # self.assignScore(4, self.top_img0, self.top_preds)
                    return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

        if not self.scorePoint4 and hand_stopwatchs_top.shape[0] != 0:
            self.flagtime4_2, _, flag = self.duration(self.flagtime4_2, 1.0)
            if flag:
                # self.scorePoint4 = True
                # self.assignScore(4, self.top_img0, self.top_preds)
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

        if not self.scorePoint4 and hand_stopwatchs_front.shape[0] != 0:
            self.flagtime4_2, _, flag = self.duration(self.flagtime4_2, 1.0)
            if flag:

                # self.scorePoint4 = True
                # self.assignScore(4, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        pass

    # 清理桌面
    def clearn_desk(self,score_index, top_items, front_items):
        if self.desk_is_clearn([top_items], [self.center_area_top]):  # 只看顶视角
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 2)
            if flag:
                # self.assignScore(5, self.top_img0, self.top_preds)
                self.clearn_f_num = 0
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

        else:
            self.clearn_f_num = 0

    # def desk_is_clearn(self, top_items, front_items):
    #     for items in top_items:
    #         if items.shape[0] == 0:
    #             continue
    #         else:
    #             for item in items:
    #                 item_box = item[:4]
    #                 if pt_in_box(center_point(item_box), self.center_box_top) > 0:
    #                     return False
    #     # for items in front_items:
    #     #     if items.shape[0] == 0:
    #     #         continue
    #     #     else:
    #     #         for item in items:
    #     #             item_box = item[:4]
    #     #             if pt_in_box(center_point(item_box), self.center_box_front) > 0:
    #     #                 return False
    #     return True

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info)
            return True
