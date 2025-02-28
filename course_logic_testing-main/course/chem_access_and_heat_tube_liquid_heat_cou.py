#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/12/29 12:53
# @File    : chem_access_and_heat_tube_liquid_heat_cou.py


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


class CHEM_access_and_heat_tube_liquid_heat(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(CHEM_access_and_heat_tube_liquid_heat, self).__init__()
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
        self.flagtime1_2 = 0.
        self.flagtime1_3 = 0.
        self.flagtime1_4 = 0.
        self.flagtime1_5 = 0.
        self.flagtime1_6 = 0.
        self.flagtime2 = 0.
        self.flagtime2_2 = 0.
        self.flagtime2_2_1 = 0.
        self.flagtime2_2_2 = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
        self.flagtime3_2_1 = 0.
        self.flagtime3_2_2 = 0.
        # 火焰熄灭时间
        self.flag_flame = 0.0
        self.flag_flame_pre = 0.0
        self.flagtime4 = 0.
        self.flagtime4_2 = 0.
        self.flagtime5 = 0.
        self.flagtime5_2 = 0.
        self.flagtime6 = 0.
        self.flagtime6_2 = 0.
        self.flagtime7 = 0.
        self.flagtime7_2 = 0.
        self.flagtime8 = 0.
        self.flagtime8_2 = 0.
        self.flagtime9 = 0.
        self.flagtime9_2 = 0.

        self.clearn_time = 0.
        self.clearn_desk_info = []

        self.scoreframe2 = 0
        self.scoreframe3 = 0
        self.scoreframe3_2 = 0
        self.scoreframe4 = 0

        self.set_center_box = False  # 设置中心操作区域

        # 实验标志
        # self.flag1 = False
        #
        # self.scorePoint3_info = [[], []]
        # self.flag3 = False
        # self.flag3_gla_bubb = False
        self.wood_clamp_head_tube_pos_list1 = []
        self.wood_clamp_head_tube_pos1 = 0.0
        self.wood_clamp_head_tube_pos_list2 = []
        self.wood_clamp_head_tube_pos2 = 0.0

        self.flag1 = False
        self.flag1_2 = False
        self.flag7 = False

        self.box2_left = []
        self.box2_right = []

        self.box2_left2 = []
        self.box2_right2 = []

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
        # [self.top_preds, self.front_preds], [self.top_img0, self.front_img0] = self.assign_score_queue.get()
        # if not self.set_center_box:
        #     self.setCenterBox(self.front_preds[0].device, est, esf)  # 设置操作中心区域

        # *-------------------------------------------------* 以下为赋分逻辑部分


        """
            主要用前视角
        """
        hands_front, flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        matchs_front, thermometers_front, glass_bubbles_front, holders_front, beakers_front, measure_cups_front, \
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front,\
        oil_columns_front, scales_front, narrow_bottles_front, iron_rings_front, iron_poles_front, tubes_front, \
        tube_mouths_front, tube_foots_front, iron_clamp_heads_front, iron_clamps_front, wood_clamps_front, \
        wood_clamp_heads_front, clean_waters_front, solid_reagents_front, matchboxs_front, woods_front,\
        not_bottom_inserts_front, bottom_inserts_front = self.preds_front

        hands_top, flames_top, alcohol_burners_top, lamp_caps_top, asbestos_nets_top, \
        matchs_top, thermometers_top, glass_bubbles_top, holders_top, beakers_top, measure_cups_top, \
        water_columns_top, match_flames_top, stop_watchs_top, hand_stop_watchs_top, bases_top, \
        oil_columns_top, scales_top, narrow_bottles_top, iron_rings_top, iron_poles_top, tubes_top, \
        tube_mouths_top, tube_foots_top, iron_clamp_heads_top, iron_clamps_top, wood_clamps_top, \
        wood_clamp_heads_top, clean_waters_top, solid_reagents_top, matchboxs_top, woods_top, \
        not_bottom_inserts_top, bottom_inserts_top = self.preds_top

        try:
            # 9 液体不超过试管容积的三分之一
            if not self.scorePoint9:
                info = self.liquid_correct(9, clean_waters_front, tubes_front)
                if info is not None:
                    self.assignScore(*info)

            # 1 试管夹从试管底部往上套,夹在距离试管口近三分之一处
            if not self.scorePoint7 and not self.scorePoint1:
                info = self.correct_clamp_tube(1,wood_clamps_front, wood_clamp_heads_front, tubes_front, tube_mouths_front,
                                        tube_foots_front, clean_waters_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 2 试管口向上倾斜约45度,不能对着自己或者他人
            if not self.scorePoint2:
                info = self.correct_tube_pos(2,tubes_front, wood_clamps_front, wood_clamp_heads_front,)
                if info is not None:
                    self.assignScore(*info)

            # 3 点燃酒精灯
            if not self.scorePoint3:
                info = self.light_alcohol_burner(3,alcohol_burners_front, matchs_front, match_flames_front, flames_front)
                if info is not None:
                    self.assignScore(*info)

            # 4 用酒精灯外焰加热
            if not self.scorePoint4 and self.scorePoint3:
                info = self.external_flame(4,alcohol_burners_front, flames_front, tubes_front, clean_waters_front, tube_foots_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 5 来回移动试管预热
            if not self.scorePoint5 and self.scorePoint3:
                info = self.back_forth_move_tube(5,tubes_front, clean_waters_front, tube_foots_front, alcohol_burners_front, flames_front, wood_clamps_front,
                                          wood_clamp_heads_front)
                if info is not None:
                    self.assignScore(*info)

            # 6 液体下方集中加热
            if not self.scorePoint6 and self.scorePoint5:
                info = self.focus_flame(6,alcohol_burners_front, flames_front, tubes_front, clean_waters_front,tube_foots_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 7 加热结束后,用灯帽盖灭酒精灯
            if not self.scorePoint7 and self.scorePoint3:
                info = self.put_out_alcohol_lamp(7,alcohol_burners_front, lamp_caps_front, flames_front)
                if info is not None:
                    self.assignScore(*info)

                pass
            # 8 实验结束后能及时整理仪器
            top_items = [flames_top, alcohol_burners_top, lamp_caps_top,matchs_top, beakers_top,
                           measure_cups_top, bases_top,narrow_bottles_top, tubes_top,
                           tube_mouths_top, tube_foots_top, wood_clamps_top, wood_clamp_heads_top,
                           clean_waters_top, matchboxs_top, woods_top]
            front_items = [flames_front, alcohol_burners_front, lamp_caps_front,matchs_front, beakers_front,
                           measure_cups_front, bases_front,narrow_bottles_front, tubes_front,
                           tube_mouths_front, tube_foots_front, wood_clamps_front, wood_clamp_heads_front,
                           clean_waters_front, matchboxs_front, woods_front]

            if not self.scorePoint8 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):
                info = self.clearn_desk(8,top_items, front_items)
                if info is not None:
                    self.assignScore(*info)

            if self.scorePoint8 and len(self.score_list) != 8:
                if not self.desk_is_clearn([top_items,front_items], [self.center_area_top,self.center_area_front]):
                    self.retracementScore(8)
        except:
            logger.error(traceback.format_exc())

    # 1 试管夹从试管底部往上套,夹在距离试管口近三分之一处
    def correct_clamp_tube(self,score_index, wood_clamps_front, wood_clamp_heads_front, tubes_front, tube_mouths_front,
                                        tube_foots_front, clean_waters_front):
        """
        前视角:
            默认从底部插入,
            1 计算木试管夹与试管内液体中心点垂直放向距离 与 试管框的高度比在 大于0.5 说明试管夹距离底部大于2/3处,保持该状态2秒
            2 计算木试管夹与试管底部中心点垂直放向距离 与 试管框的高度比在 大于0.5 说明试管夹距离底部大于2/3处,保持该状态2秒
            3 计算 试管夹与试管底部垂直方向距离 与 木试管夹与试管口部的中心点垂直方向距离的比值 在 1.5~3之间

        :param wood_clamps_front:
        :param wood_clamp_heads_front:
        :param tubes_front:
        :param tube_mouths_front:
        :param tube_foots_front:
        :param clean_waters_front:
        :return:
        """
        if wood_clamp_heads_front.shape[0] != 0:
            self.flag1 = True  # 默认是从底部插入的
            if clean_waters_front.shape[0] != 0 and tubes_front.shape[0] != 0:
                status = False
                for wood_clamp_head_front in wood_clamp_heads_front:
                    for clean_water_front in clean_waters_front:
                        wood_clamp_head_clean_water_iou = iou(wood_clamp_head_front[:4], clean_water_front[:4]) > 0
                        if wood_clamp_head_clean_water_iou:
                            self.flag1 = True

                if self.flag1:
                    for wood_clamp_head_front in wood_clamp_heads_front:
                        for clean_water_front in clean_waters_front:
                            wood_clamp_head_tube_foot_pos_y = abs(center_distance_v(wood_clamp_head_front[:4],
                                                                                      clean_water_front[:4]))
                            for tube_front in tubes_front:
                                wood_head_tube_iou = iou(tube_front[:4], wood_clamp_head_front[:4]) > 0
                                if wood_head_tube_iou:
                                    wood_clamp_head_tube_foot_rate = wood_clamp_head_tube_foot_pos_y / abs(tube_front[:4][1] -
                                                                                                           tube_front[:4][3])
                                    if 0.8 > wood_clamp_head_tube_foot_rate > 0.5:
                                        status = True
                                        # 说明夹到三分之一处
                if status:
                    # 说明夹到三分之一处
                    self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 1.0,
                                                                           self.flagtime1_2, 1)
                    if flag:
                        # self.scorePoint1 = True
                        # self.assignScore(1, self.front_img0, self.front_preds)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


            if tube_foots_front.shape[0] != 0 and tubes_front.shape[0] != 0:
                status = False
                for wood_clamp_head_front in wood_clamp_heads_front:
                    for tube_foot_front in tube_foots_front:
                        wood_clamp_head_foot_iou = iou(wood_clamp_head_front[:4], tube_foot_front[:4])
                        if wood_clamp_head_foot_iou:
                            self.flag1 = True
                if self.flag1:
                    for wood_clamp_head_front in wood_clamp_heads_front:
                        for tube_foot_front in tube_foots_front:
                            wood_clamp_head_tube_foot_pos_y = abs(center_distance_v(wood_clamp_head_front[:4],
                                                                                      tube_foot_front[:4]))
                            for tube_front in tubes_front:
                                wood_head_tube_iou = iou(tube_front[:4], wood_clamp_head_front[:4]) > 0
                                if wood_head_tube_iou:
                                    wood_clamp_head_tube_foot_rate = wood_clamp_head_tube_foot_pos_y / abs(tube_front[:4][1] -
                                                                                                           tube_front[:4][3])
                                    if 0.8 > wood_clamp_head_tube_foot_rate > 0.5:
                                        status = True
                                        # 说明夹到三分之一处
                if status:
                    # 说明夹到三分之一处
                    self.flagtime1_3, self.flagtime1_4, flag = self.duration(self.flagtime1_3, 1.0,
                                                                           self.flagtime1_4, 1)
                    if flag:
                        # self.scorePoint1 = True
                        # self.assignScore(1, self.front_img0, self.front_preds)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


            if tube_foots_front.shape[0] != 0 or clean_waters_front.shape[0] != 0 and tube_mouths_front.shape[0] != 0:
                status = False
                if tube_foots_front.shape[0] != 0:
                    for wood_clamp_head_front in wood_clamp_heads_front:
                        for tube_foot_front in tube_foots_front:
                            wood_clamp_head_foot_iou = iou(wood_clamp_head_front[:4], tube_foot_front[:4])
                            if wood_clamp_head_foot_iou:
                                self.flag1 = True
                    if self.flag1:
                        for wood_clamp_head_front in wood_clamp_heads_front:
                            for tube_foot_front in tube_foots_front:
                                for tube_mouth_front in tube_mouths_front:
                                    head_mouth_y = abs(center_distance_v(wood_clamp_head_front[:4], tube_mouth_front[:4])) \
                                        if abs(center_distance_v(wood_clamp_head_front[:4], tube_mouth_front[:4])) else 1
                                    head_foot_y = abs(center_distance_v(wood_clamp_head_front[:4], tube_foot_front[:4]))
                                    if 1.5< head_foot_y/head_mouth_y < 3:  # 铁试管夹到底部距离 比 铁试管夹到试管开口的距离   范围 0.5~1
                                        status = True
                    if status:
                        # 说明夹到三分之一处
                        self.flagtime1_5, self.flagtime1_6, flag = self.duration(self.flagtime1_5, 1.0,
                                                                                 self.flagtime1_6, 1)
                        if flag:
                            # self.scorePoint1 = True
                            # self.assignScore(1, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                pass
            if tube_mouths_front.shape[0] == 0 and tube_foots_front.shape[0] == 0 and tubes_front.shape[0] != 0:
                # 通过木试管夹头和试管来判断
                status = False
                for tube_front in tubes_front:
                    for wood_clamp_head_front in wood_clamp_heads_front:
                        wood_head_tube_iou = iou(tube_front[:4], wood_clamp_head_front[:4]) > 0
                        if wood_head_tube_iou:
                            tube_x1,tube_y1,tube_x2,tube_y2, = tube_front[:4]
                            v_pos = abs(center_point(wood_clamp_head_front[:4])[1] - max(tube_y1, tube_y2))  # 木试管夹头中心点与试管右下角点的y距离
                            if v_pos - self.wood_clamp_head_tube_pos2 > 5 and not self.flag1_2:
                                self.wood_clamp_head_tube_pos_list2.append(v_pos)
                                self.wood_clamp_head_tube_pos2 = v_pos
                            if len(self.wood_clamp_head_tube_pos_list2) > 3:
                                self.flag1_2 = True
                                break
                if self.flag1_2:
                    for wood_clamp_head_front in wood_clamp_heads_front:
                        for tube_front in tubes_front:
                            wood_head_tube_iou = iou(tube_front[:4], wood_clamp_head_front[:4]) > 0
                            if wood_head_tube_iou:
                                tube_x1, tube_y1, tube_x2, tube_y2, = tube_front[:4]
                                wood_clamp_head_tube_foot_pos_y = abs(center_point(wood_clamp_head_front[:4])[1] - max(tube_y1,
                                                                                         tube_y2))  # 木试管夹头中心点与试管右下角点的y距离
                                wood_clamp_head_tube_foot_rate = wood_clamp_head_tube_foot_pos_y / abs(tube_front[:4][1] -
                                                                                                       tube_front[:4][3])
                                if 0.8 > wood_clamp_head_tube_foot_rate > 0.5:
                                    # 说明夹到三分之一处
                                    status = True
                                    self.wood_clamp_head_tube_pos_list2.clear()
                                    self.wood_clamp_head_tube_pos2 = 0.0
                if status:
                    self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 1.0,
                                                                           self.flagtime1_2, 1)
                    if flag:
                        # self.scorePoint1 = True
                        # self.assignScore(1, self.front_img0, self.front_preds)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 2 试管口向上倾斜约45度,不能对着自己或者他人
    def correct_tube_pos(self,score_index, tubes_front, wood_clamps_front, wood_clamp_heads_front,):
        """
        前视角
        试管和试管夹头有交集, 0.6<试管的高/试管的宽 <1.8  # 角度 40<du<50 保持状态 2 秒
        :param tubes_front:
        :param wood_clamps_front:
        :param wood_clamp_heads_front:
        :return:
        """
        if tubes_front.shape[0] != 0:
            status = False
            for tube_front in tubes_front:
                clamp_head_tube_status = False
                for wood_clamp_head_front in wood_clamp_heads_front:
                    if iou(tube_front[:4], wood_clamp_head_front[:4]):
                        clamp_head_tube_status = True
                        break
                if clamp_head_tube_status:
                    h_v_rate = abs(tube_front[:4][1] - tube_front[:4][3]) / abs(tube_front[:4][0] - tube_front[:4][2])
                    if 0.6 < h_v_rate < 1.8:
                        status = True
            if status:
                self.flagtime2, self.flagtime2_2, flag = self.duration(self.flagtime2, 2.0,
                                                                       self.flagtime2_2, 2)
                if flag:
                    # self.scorePoint2 = True
                    # self.assignScore(2, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 3 点燃酒精灯
    def light_alcohol_burner(self,score_index, alcohol_burners_front, matchs_front, match_flames_front, flames_front):
        """
        前视角:
            打火机点燃酒精灯的标签出现或者该标签没出现火焰标签出现超过1秒,给分
        """
        if match_flames_front.shape[0] != 0:
            self.flagtime3_2_1, self.flagtime3_2_2, flag = self.duration(self.flagtime3_2_1, 0.1,
                                                                         self.flagtime3_2_2, 0.1)
            if flag:
                # self.scorePoint3 = True
                # self.assignScore(3, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        else:
            if flames_front.shape[0] != 0:
                self.flagtime3, self.flagtime3_2, flag = self.duration(self.flagtime3, 1,
                                                                       self.flagtime3_2, 1)
                if flag:
                    # self.scorePoint3 = True
                    # self.assignScore(3, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


    # 4 用酒精灯外焰加热
    def external_flame(self,score_index, alcohol_burners_front, flames_front, tubes_front, clean_waters_front, tube_foots_front):
        """
        前视角:
        1,试管内液体中心点垂直方向位置在火焰中心点垂直方向位置上方
        2 试管内液体中心点与火焰中心点水平方向距离 不大于 酒精灯的宽度;
        同时满足 1,2 持续时间3秒给分
        或者
            3 试管底部中心点垂直方向位置在火焰中心点垂直方向位置上方
            4 试管底部中心点与火焰中心点水平方向距离 不大于 酒精灯的宽度;
            同时满足 3,4 持续时间3秒给分
        """
        if flames_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0:
            status = False
            if clean_waters_front.shape[0] != 0:
                for clean_water_front in clean_waters_front:
                    for flame_front in flames_front:
                        water_flame_pos_y = center_distance_v(clean_water_front[:4], flame_front[:4]) < 0
                        for alcohol_burner_front in alcohol_burners_front:
                            water_flame_pos_h = abs(center_distance_h(clean_water_front[:4], flame_front[:4])) < \
                                                abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                            if water_flame_pos_h and water_flame_pos_y:
                                status = True
                                break
            if tube_foots_front.shape[0] != 0:
                for tube_foot_front in tube_foots_front:
                    for flame_front in flames_front:
                        foot_flame_pos_y = center_distance_v(tube_foot_front[:4], flame_front[:4]) < 0
                        for alcohol_burner_front in alcohol_burners_front:
                            foot_flame_pos_h = abs(center_distance_h(tube_foot_front[:4], flame_front[:4])) < \
                                                abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                            if foot_flame_pos_h and foot_flame_pos_y:
                                status = True
                                break
            if status:
                self.flagtime4, self.flagtime4_2, flag = self.duration(self.flagtime4, 3,
                                                                       self.flagtime4_2, 3)
                if flag:
                    # self.scorePoint4 = True
                    # self.assignScore(4, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # # 5 来回移动试管预热
    def back_forth_move_tube(self,score_index, tubes_front, clean_waters_front, tube_foots_front, alcohol_burners_front,
                             flames_front, wood_clamps_front, wood_clamp_heads_front):
        """
        1 试管内液体中心点的垂直方向在酒精灯中心点垂直方向上方
        2 试管内液体中心点与酒精灯中心点水平方向不大于酒精灯的宽;
        3 满足1,2条件通过判断试管内液体(试管底部)与酒精灯的水平方向位置关系来判断在晃动试管
        """
        if clean_waters_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0 and flames_front.shape[0] != 0:
            for clean_water_front in clean_waters_front:
                for alcohol_burner_front in alcohol_burners_front:
                    if center_distance_v(clean_water_front[:4], alcohol_burner_front[:4]) < 0 and abs(center_distance_h(clean_water_front[:4], alcohol_burner_front[:4])) < abs(
                            alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2]):  # box1 在 box2上面
                        if center_distance_h(clean_water_front[:4], alcohol_burner_front[:4]) < 0:  # box1 在box2 左边
                            self.box2_left.append(center_point(clean_water_front[:4])[0])
                        else:
                            self.box2_right.append(center_point(clean_water_front[:4])[0])
                        break
            if len(self.box2_left) > 20 and len(self.box2_right) > 20:
                # self.scorePoint5 = True
                # self.assignScore(5, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        if tube_foots_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0 and flames_front.shape[0] != 0:
            for tube_foot_front in tube_foots_front:
                for alcohol_burner_front in alcohol_burners_front:
                    if center_distance_v(tube_foot_front[:4], alcohol_burner_front[:4]) < 0 and abs(center_distance_h(tube_foot_front[:4], alcohol_burner_front[:4])) < abs(
                            alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2]):  # box1 在 box2上面
                        if center_distance_h(tube_foot_front[:4], alcohol_burner_front[:4]) < 0:  # box1 在box2 左边
                            self.box2_left2.append(center_point(tube_foot_front[:4])[0])
                        else:
                            self.box2_right2.append(center_point(tube_foot_front[:4])[0])
                        break
            if len(self.box2_left2) > 20 and len(self.box2_right2) > 20:
                # self.scorePoint5 = True
                # self.assignScore(5, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 6 液体下方集中加热
    def focus_flame(self,score_index, alcohol_burners_front, flames_front, tubes_front, clean_waters_front, tube_foots_front):
        """
        前视角:
        1试管内液体(试管底部)中心点 在酒精灯中心点垂直方向上方;
        2 试管内液体(试管底部)中心点 与酒精灯中心点 水平方向距离小于3个像素
        满足 1,2 同时火焰存在 保持状态3秒
        """
        if tubes_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0:
            status = False
            pos_status = False
            if clean_waters_front.shape[0] != 0:
                for clean_water_front in clean_waters_front:
                    for alcohol_burner_front in alcohol_burners_front:
                        water_flame_pos_y = center_distance_v(clean_water_front[:4], alcohol_burner_front[:4]) < 0
                        water_flame_pos_h = abs(center_distance_h(clean_water_front[:4], alcohol_burner_front[:4])) < 3
                        if water_flame_pos_h and water_flame_pos_y:
                            pos_status = True
                            break
            if tube_foots_front.shape[0] != 0:
                for tube_foot_front in tube_foots_front:
                    for alcohol_burner_front in alcohol_burners_front:
                        foot_flame_pos_y = center_distance_v(tube_foot_front[:4], alcohol_burner_front[:4]) < 0
                        foot_flame_pos_h = abs(center_distance_h(tube_foot_front[:4], alcohol_burner_front[:4])) < 3
                        if foot_flame_pos_h and foot_flame_pos_y:
                            pos_status = True
                            break

            if flames_front.shape[0] != 0 and pos_status:
                status = True
            if status:
                self.flagtime6, self.flagtime6_2, flag = self.duration(self.flagtime6, 3,
                                                                       self.flagtime6_2, 3)
                if flag:
                    # self.scorePoint6 = True
                    # self.assignScore(6, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 7 该灭酒精灯
    def put_out_alcohol_lamp(self,score_index, alcohol_burners_front, lamp_caps_front, flames_front):
        """
        加热结束后,用灯帽盖灭酒精灯:
        1 判断灯帽中心点与酒精灯中心点的垂直方向位置 灯帽在酒精灯上方;
        2 灯帽的中心点水平方向与酒精灯中心点水平方向距离小于酒精灯的宽
        满足 1,2 且火焰不存在,且灯帽与酒精灯有交集;
        :param alcohol_burners_front:
        :param lamp_caps_front:
        :param flames_front:
        :return:
        """
        if alcohol_burners_front.shape[0] != 0 and lamp_caps_front.shape[0] != 0:
            alcohol_status = False
            for alcohol_burner_front in alcohol_burners_front:
                for lamp_cap_front in lamp_caps_front:
                    lamp_cap_pos_v = center_distance_v(alcohol_burner_front[:4], lamp_cap_front[:4]) > 0
                    lamp_cap_pos_h = abs(center_distance_h(alcohol_burner_front[:4], lamp_cap_front[:4])) < abs(alcohol_burner_front[:4][0]-alcohol_burner_front[:4][2])
                    if lamp_cap_pos_v and lamp_cap_pos_h and flames_front.shape[0] == 0:
                        self.flag7 = True
                        break
            if self.flag7:
                for alcohol_burner_front in alcohol_burners_front:
                    for lamp_cap_front in lamp_caps_front:
                        if iou(alcohol_burner_front[:4], lamp_cap_front[:4]) > 0:
                            alcohol_status = True
                            break
            if alcohol_status:
                if flames_front.shape[0] == 0:  # 当没有火焰说明该灭成功
                    # self.scorePoint7 = True
                    # self.assignScore(7, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


    # 9液体不超过试管容积的三分之一
    def liquid_correct(self,score_index, clean_waters_front, tubes_front):
        """
        前视角
            试管内液体框的高与 试管的高 比值 小于0.4,满足条件保持 2秒
        """
        if clean_waters_front.shape[0] != 0 and tubes_front.shape[0] != 0:
            status = False
            for tube_front in tubes_front:
                for clean_water_front in clean_waters_front:
                    tube_y = abs(tube_front[:4][1] - tube_front[:4][3]) if abs(tube_front[:4][1] - tube_front[:4][3]) else 1
                    clean_water_y = abs(clean_water_front[:4][1] - clean_water_front[:4][3])
                    if clean_water_y / tube_y < 0.4:
                        status = True
                        pass
            if status:
                self.flagtime9, self.flagtime9_2, flag = self.duration(self.flagtime9, 2.0,
                                                                       self.flagtime9_2, 2)
                if flag:
                    # self.scorePoint9 = True
                    # self.assignScore(9, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


    # 清理桌面
    def clearn_desk(self,score_index, top_items, front_items):
        # if self.desk_is_clearn(top_items, front_items):
        #     self.clearn_desk_info = [8, self.front_img0, self.front_preds, time.time()]
        #     self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
        #     if flag:
        #         self.scorePoint4 = True
        #         self.assignScore(8, self.front_img0, self.front_preds)
        # else:
        #     self.clearn_time = 0

        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):  # 只看前视角
            self.clearn_desk_info = [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                     self.num_frame_front, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 0.5)
            if flag:
                # self.assignScore(5, self.top_img0, self.top_preds)
                self.clearn_f_num = 0
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

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
    #     for items in front_items:
    #         if items.shape[0] == 0:
    #             continue
    #         else:
    #             for item in items:
    #                 item_box = item[:4]
    #                 if pt_in_box(center_point(item_box), self.center_box_front) > 0:
    #                     return False
    #                 # if iou(item_box, self.center_box_front) >0:
    #                 #     return False
    #     return True


    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info)
            return True

    def make_frame(self, img, box1, box2, label_CHS="视线与温度计持平", conf=0.888):
        """
        用于将两个框 框在一起 给一个标签
        :param img: 待画的图
        :param box1: 待画的框1
        :param box2: 待画的框2
        :param label_CHS: 标签-中文
        :param conf: 置信度
        :return:
        """
        x_min = min(box1[0], box1[2], box2[0], box2[2])
        y_min = min(box1[1], box1[3], box2[1], box2[3])
        x_max = max(box1[0], box1[2], box2[0], box2[2])
        y_max = max(box1[1], box1[3], box2[1], box2[3])

        x1, y1, x2, y2 = int(x_min), int(y_min), int(x_max), int(y_max)
        color = [0, 0, 255]  # 255,0,0  # [B,G,R]  红色
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)  # 青色框框出所需范围,
        text = f'{"  " * len(label_CHS)} {conf:.2f}'
        ###
        from PIL import Image, ImageDraw, ImageFont
        char_l = (len(label_CHS) * 2 + 7) * 9  ## length of character
        bg_ch = np.array([0, 0, 255], dtype=np.uint8)  # [B,G,R] 蓝色
        bg_ch = np.broadcast_to(bg_ch, (18, char_l, 3))  # 广播机制
        pil_bg = Image.fromarray(bg_ch)
        draw = ImageDraw.Draw(pil_bg)  # 设置背景区域大小(18, char_l, 3),背景颜色为[0,0,255]
        fontStyle = ImageFont.truetype("../font/simhei.ttf", 18)  # 设置字体
        draw.text((5, 1), label_CHS, (255, 255, 255), font=fontStyle)  # 设置字,字体颜色 为白色 (5,0)-字体在背景的显示位置
        np_bg = np.asarray(pil_bg)
        h, w, _ = img.shape
        y, x, _ = np_bg.shape  # y,x 为写中文字的背景 高宽
        px, py = x1, y1  # px,py为需要画框的左上角的点
        # px, py 重新赋值 解决框的背景解释超出图片的范围 问题
        if w - px < x:
            px = w - x
        if py < y:
            py = y
        img[py - y:py, px:px + x] = np_bg  ## Chinese characters background
        cv2.putText(img, text, (px, py - 3), 0, 0.6, [225, 255, 255], thickness=1,
                    lineType=cv2.LINE_AA)
