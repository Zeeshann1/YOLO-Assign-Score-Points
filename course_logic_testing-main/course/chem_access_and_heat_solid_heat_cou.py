#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2022/1/4 15:50
# @File    : chem_access_and_heat_solid_heat_cou.py

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


class CHEM_access_and_heat_solid_heat(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(CHEM_access_and_heat_solid_heat, self).__init__()
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
        self.flagtime2 = 0.
        self.flagtime2_2 = 0.
        self.flagtime2_2_1 = 0.
        self.flagtime2_2_2 = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
        self.flagtime3_2_1 = 0.
        self.flagtime3_2_2 = 0.
        self.flagtime3_3_1 = 0.
        self.flagtime3_3_2 = 0.
        self.flagtime3_4_1 = 0.
        self.flagtime3_4_2 = 0.
        self.flagtime3_5_1 = 0.
        self.flagtime3_5_2 = 0.
        # 火焰熄灭时间
        self.flag_flame = 0.0
        self.flag_flame_pre = 0.0
        self.flagtime4 = 0.
        self.flagtime4_2 = 0.
        self.flagtime4_3_1 = 0.
        self.flagtime4_3_2 = 0.

        self.flagtime5 = 0.
        self.flagtime5_2 = 0.
        self.flagtime6 = 0.
        self.flagtime6_2 = 0.
        self.flagtime7 = 0.
        self.flagtime7_2 = 0.
        self.flagtime8 = 0.
        self.flagtime8_2 = 0.

        self.clearn_time = 0.
        self.clearn_desk_info = []

        self.scoreframe2 = 0
        self.scoreframe3 = 0
        self.scoreframe3_2 = 0
        self.scoreframe4 = 0

        self.set_center_box = False  # 设置中心操作区域

        # 实验标志
        self.wood_clamp_head_tube_pos_list1 = []
        self.wood_clamp_head_tube_pos1 = 0.0
        self.wood_clamp_head_tube_pos_list2 = []
        self.wood_clamp_head_tube_pos2 = 0.0

        self.flag1 = False
        self.flag1_2 = False
        self.flag7 = False

        self.box1_info = []
        self.box2_left = []
        self.box2_right = []

        self.tube_foot_clamp_head_status = False
        self.solid_re_head_pos1 = 0.0

        self.solid_re_head_pos_list1 = []

        self.foot_li1 = []
        self.move_pos = 0.
        self.move_num = 0
        self.foot_li2 = []
        self.move_pos2 = 0.
        self.move_num2 = 0
        # 第五个得分点 预热试管时,用于拼接图片到一张图
        # res = np.full((540, 960, 3), 114, dtype=np.uint8)
        # self.images = [res, res, res, res]

        # 第六的得分点
        self.alc_bu_pos = 0.
        self.alc_bu_list = []
        self.num6 = 0

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
        # [self.top_preds, self.front_preds, self.side_preds], [self.top_img0, self.front_img0, self.side_img0] = self.assign_score_queue.get()
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
        wood_clamp_heads_front, clean_waters_front, solid_reagents_front, matchboxs_front, woods_front, \
        not_bottom_inserts_front, bottom_inserts_front = self.preds_front

        hands_top, flames_top, alcohol_burners_top, lamp_caps_top, asbestos_nets_top, \
        matchs_top, thermometers_top, glass_bubbles_top, holders_top, beakers_top, measure_cups_top, \
        water_columns_top, match_flames_top, stop_watchs_top, hand_stop_watchs_top, bases_top, \
        oil_columns_top, scales_top, narrow_bottles_top, iron_rings_top, iron_poles_top, tubes_top, \
        tube_mouths_top, tube_foots_top, iron_clamp_heads_top, iron_clamps_top, wood_clamps_top, \
        wood_clamp_heads_top, clean_waters_top, solid_reagents_top, matchboxs_top, woods_top, not_bottom_inserts_top, \
        bottom_inserts_top = self.preds_top

        hands_side, flames_side, alcohol_burners_side, lamp_caps_side, asbestos_nets_side, \
        matchs_side, thermometers_side, glass_bubbles_side, holders_side, beakers_side, measure_cups_side, \
        water_columns_side, match_flames_side, stop_watchs_side, hand_stop_watchs_side, bases_side, \
        oil_columns_side, scales_side, narrow_bottles_side, iron_rings_side, iron_poles_side, tubes_side, \
        tube_mouths_side, tube_foots_side, iron_clamp_heads_side, iron_clamps_side, wood_clamps_side, \
        wood_clamp_heads_side, clean_waters_side, solid_reagents_side, matchboxs_side, woods_side, \
        not_bottom_inserts_side, bottom_inserts_side = self.preds_side
        try:
            # 1 试管夹从试管底部向上夹在试管中上部(试管三分之一处)
            if not self.scorePoint1:
                info = self.correct_clamp_tube(1,hands_top, iron_clamp_heads_top, tubes_top, solid_reagents_top,
                                        tube_foots_top, tube_mouths_top, iron_clamp_heads_front, solid_reagents_front,
                                        tube_foots_front, bottom_inserts_top)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 2 试管口略微向下倾斜
            if not self.scorePoint2:
                info = self.correct_tube_pos(2,tubes_front, iron_clamp_heads_front, tube_mouths_front, tube_foots_front,
                                      solid_reagents_front,hands_front)
                if info is not None:
                    self.assignScore(*info)

            # 3 点燃酒精灯
            if not self.scorePoint3:
                info = self.light_alcohol_burner(3,alcohol_burners_front, matchs_front, match_flames_front, flames_front,
                                          match_flames_top, match_flames_side,flames_side)
                if info is not None:
                    self.assignScore(*info)

            # 4 用酒精灯外焰加热
            if not self.scorePoint4 and self.scorePoint3:
                info = self.external_flame(4,alcohol_burners_front, flames_front, tubes_front, solid_reagents_front,
                                    tube_foots_front,
                                    alcohol_burners_side, flames_side, tubes_side, solid_reagents_side, tube_foots_side)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 5 预热试管(来回移动酒精灯)
            if not self.scorePoint5 and self.scorePoint3:
                info = self.back_forth_move_tube(5,tubes_front, tube_foots_front, solid_reagents_front, alcohol_burners_front,
                                          flames_front)
                if info is not None:
                    self.assignScore(*info)

            # 6 固体下方集中加热
            if not self.scorePoint6 and self.scorePoint3:
                info = self.focus_flame(6,alcohol_burners_front, flames_front, tubes_front, solid_reagents_front,tube_foots_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 7 加热结束后,用灯帽盖灭酒精灯
            if not self.scorePoint7 and self.scorePoint3:
                info = self.put_out_alcohol_lamp(7,alcohol_burners_front, lamp_caps_front, flames_front, alcohol_burners_top, lamp_caps_top, flames_top)
                if info is not None:
                    self.assignScore(*info)
                pass
            # 8 实验结束后能及时整理仪器
            top_items = [flames_top, alcohol_burners_top, lamp_caps_top, asbestos_nets_top, \
        matchs_top, thermometers_top, glass_bubbles_top, holders_top, beakers_top, measure_cups_top, \
        water_columns_top, match_flames_top, stop_watchs_top, hand_stop_watchs_top, bases_top]
            front_items = [flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        matchs_front, thermometers_front, glass_bubbles_front, holders_front, beakers_front, measure_cups_front, \
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front]

            if not self.scorePoint8 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):
                self.clearn_desk(8, top_items, front_items)
            if self.scorePoint8 and len(self.score_list) != 8:
                if not self.desk_is_clearn([front_items], [self.center_area_front]):
                    self.retracementScore(8)
        except:
            logger.error(traceback.format_exc())

    # 1 试管夹从试管底部往上套,夹在距离试管口近三分之一处
    def correct_clamp_tube(self,score_index, hands_top, iron_clamp_heads_top, tubes_top, solid_reagents_top,
                            tube_foots_top, tube_mouths_top, iron_clamp_heads_front, solid_reagents_front,
                           tube_foots_front, bottom_inserts_top):
        """
            1 试管夹从试管底部向上夹在试管中上部(试管三分之一处):
            1.1 铁试管夹头与试管底部有交集;
            1.2 铁试管夹头在试管的中上部;
        :param hands_top:
        :param iron_clamp_heads_top:
        :param tubes_top:
        :param solid_reagents_top:
        :param tube_foots_top:
        :param tube_mouths_top:
        :return:
        """
        # 是否从试管底部开始套
        if iron_clamp_heads_top.shape[0] != 0 and solid_reagents_top.shape[0] != 0:
            for iron_clamp_head_top in iron_clamp_heads_top:
                for solid_reagent_top in solid_reagents_top:
                    if iou(iron_clamp_head_top[:4], solid_reagent_top[:4]) > 0 or \
                            min_dis_boxes(iron_clamp_head_top[:4], solid_reagent_top[:4]) < 10:
                        self.tube_foot_clamp_head_status = True

        if iron_clamp_heads_top.shape[0] != 0 and tube_foots_top.shape[0] != 0:
            for iron_clamp_head_top in iron_clamp_heads_top:
                for tube_foot_top in tube_foots_top:
                    if iou(iron_clamp_head_top[:4], tube_foot_top[:4]) > 0 or \
                            min_dis_boxes(iron_clamp_head_top[:4], tube_foot_top[:4]) < 10:
                        self.tube_foot_clamp_head_status = True

        if iron_clamp_heads_front.shape[0] != 0 and solid_reagents_front.shape[0] != 0:
            for iron_clamp_head_front in iron_clamp_heads_front:
                for solid_reagent_front in solid_reagents_front:
                    if iou(iron_clamp_head_front[:4], solid_reagent_front[:4]) > 0 or \
                            min_dis_boxes(iron_clamp_head_front[:4], solid_reagent_front[:4]) < 10:
                        self.tube_foot_clamp_head_status = True

        if iron_clamp_heads_front.shape[0] != 0 and tube_foots_front.shape[0] != 0:
            for iron_clamp_head_front in iron_clamp_heads_front:
                for tube_foot_front in tube_foots_front:
                    if iou(iron_clamp_head_front[:4], tube_foot_front[:4]) > 0 or \
                            min_dis_boxes(iron_clamp_head_front[:4], tube_foot_front[:4]) < 10:
                        self.tube_foot_clamp_head_status = True

        # 从底部插入的标签存在
        if bottom_inserts_top.shape[0] != 0:
            self.flagtime1_3, self.flagtime1_4, flag = self.duration(self.flagtime1_3, 0.1,
                                                                   self.flagtime1_4, 0.1)
            if flag:
                self.tube_foot_clamp_head_status = True

        # 是否试管夹夹在1/3处
        clamp_correct_status = False  # 试管夹在试管的状态;
        self.tube_foot_clamp_head_status = True  # 默认试管是从底部套进去的
        if self.tube_foot_clamp_head_status:
            if iron_clamp_heads_top.shape[0] != 0 and solid_reagents_top.shape[0] != 0 and tubes_top.shape[0] != 0:
                for iron_clamp_head_top in iron_clamp_heads_top:
                    for solid_reagent_top in solid_reagents_top:
                        for tube_top in tubes_top:
                            clamp_tube_iou = iou(tube_top[:4], iron_clamp_head_top[:4])
                            if clamp_tube_iou:
                                solid_clamp_head_pos_x = abs(center_distance_h(solid_reagent_top[:4],
                                                                               iron_clamp_head_top[:4]))
                                if 0.5 * abs(tube_top[:4][0] - tube_top[:4][2]) < solid_clamp_head_pos_x < 0.9 * abs(
                                        tube_top[:4][0] - tube_top[:4][2]):
                                    clamp_correct_status = True
                                    break

            if not clamp_correct_status and iron_clamp_heads_top.shape[0] != 0 and tube_foots_top.shape[0] != 0 and \
                    tubes_top.shape[0] != 0:
                for iron_clamp_head_top in iron_clamp_heads_top:
                    for tube_foot_top in tube_foots_top:
                        for tube_top in tubes_top:
                            clamp_tube_iou = iou(tube_top[:4], iron_clamp_head_top[:4])
                            if clamp_tube_iou:
                                foot_clame_head_pos_x = abs(center_distance_h(tube_foot_top[:4],
                                                                              iron_clamp_head_top[:4]))
                                if 0.5 * abs(tube_top[:4][0] - tube_top[:4][2]) < foot_clame_head_pos_x < 0.9 * abs(
                                        tube_top[:4][0] - tube_top[:4][2]):
                                    clamp_correct_status = True
                                    break
            if not clamp_correct_status and iron_clamp_heads_top.shape[0] != 0 and tube_mouths_top.shape[0] != 0 and \
                    tubes_top.shape[0] != 0:
                for iron_clamp_head_top in iron_clamp_heads_top:
                    for tube_mouth_top in tube_mouths_top:
                        for tube_top in tubes_top:
                            clamp_tube_iou = iou(tube_top[:4], iron_clamp_head_top[:4])
                            if clamp_tube_iou:
                                mouth_clamp_head_pos_x = abs(center_distance_h(tube_mouth_top[:4], iron_clamp_head_top[:4]))
                                if mouth_clamp_head_pos_x < 0.5 * abs(tube_top[:4][0] - tube_top[:4][2]):
                                    clamp_correct_status = True
                                    break
        if clamp_correct_status:
            self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 2,
                                                                   self.flagtime1_2, 2)
            if flag:
                # self.scorePoint1 = True
                # self.assignScore(1, self.top_img0, self.top_preds)
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top

    # 2 试管口略微向下倾斜
    def correct_tube_pos(self,score_index, tubes_front, iron_clamp_heads_front, tube_mouths_front, tube_foots_front,
                         solid_reagents_front,hands_front):
        """
        :
        试管和铁试管夹头有交集的情况下,
        之后 试管口的位置低于试管底部(
        或者试管口的位置低于固体药品的位置;
        或者铁试管夹位置低于固体药瓶位置;
        或者铁试管夹位置低于试管底部位置;)
        :param tubes_front:
        :param wood_clamps_front:
        :param wood_clamp_heads_front:
        :return:
        """
        correct_tube_status1 = False

        if iron_clamp_heads_front.shape[0] != 0 and tube_mouths_front.shape[0] != 0:
            for iron_clamp_head_front in iron_clamp_heads_front:
                for tube_mouth_front in tube_mouths_front:
                    if center_distance_v(iron_clamp_head_front[:4], tube_mouth_front[:4]) < 0:
                        correct_tube_status1 = True
                        break
        if iron_clamp_heads_front.shape[0] != 0 and tube_foots_front.shape[0] != 0:
            for iron_clamp_head_front in iron_clamp_heads_front:
                for tube_foot_front in tube_foots_front:
                    if center_distance_v(iron_clamp_head_front[:4], tube_foot_front[:4]) > 0:
                        correct_tube_status1 = True
                        break
        if tube_mouths_front.shape[0] != 0 and tube_foots_front.shape[0] != 0:
            for tube_mouth_front in tube_mouths_front:
                for tube_foot_front in tube_foots_front:
                    if center_distance_v(tube_mouth_front[:4], tube_foot_front[:4]) > 0:
                        correct_tube_status1 = True
                        break
        if correct_tube_status1:
            self.flagtime2, self.flagtime2_2, flag = self.duration(self.flagtime2, 2.0,
                                                                   self.flagtime2_2, 2)
            if flag:
                # self.scorePoint2 = True
                # self.assignScore(2, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


    # 3 点燃酒精灯
    def light_alcohol_burner(self,score_index, alcohol_burners_front, matchs_front, match_flames_front, flames_front,
                             match_flames_top, match_flames_side, flames_side):
        if match_flames_front.shape[0] != 0:
            self.flagtime3_2_1, self.flagtime3_2_2, flag = self.duration(self.flagtime3_2_1, 0.1,
                                                                   self.flagtime3_2_2, 0.1)
            if flag:
                # self.scorePoint3 = True
                # self.assignScore(3, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        elif match_flames_top.shape[0] != 0:
            self.flagtime3_3_1, self.flagtime3_3_2, flag = self.duration(self.flagtime3_3_1, 0.1,
                                                                         self.flagtime3_3_2, 0.1)
            if flag:
                # self.scorePoint3 = True
                # self.assignScore(3, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

            pass
        elif match_flames_side.shape[0] != 0:
            self.flagtime3_4_1 ,self.flagtime3_4_2 ,flag = self.duration(self.flagtime3_4_1, 0.1,
                                                                         self.flagtime3_4_2, 0.1)
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

            if flames_side.shape[0] != 0:
                self.flagtime3_5_1, self.flagtime3_5_2, flag = self.duration(self.flagtime3_5_1, 1,
                                                                       self.flagtime3_5_2, 1)
                if flag:
                    # self.scorePoint3 = True
                    # self.assignScore(3, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4 用酒精灯外焰加热
    def external_flame(self,score_index, alcohol_burners_front, flames_front, tubes_front, solid_reagents_front, tube_foots_front,
                                alcohol_burners_side, flames_side, tubes_side, solid_reagents_side, tube_foots_side):
        status = False
        flag4 = False
        if alcohol_burners_front.shape[0] != 0 and solid_reagents_front.shape[0] != 0:
            for alcohol_burner_front in alcohol_burners_front:
                for solid_reagent_front in solid_reagents_front:
                    solid_alc_pos_y = center_distance_v(solid_reagent_front[:4], alcohol_burner_front[:4]) < 0
                    solid_alc_pos_h = abs(center_distance_h(solid_reagent_front[:4], alcohol_burner_front[:4])) < \
                                      abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                    if solid_alc_pos_y and solid_alc_pos_h:
                        flag4 = True

        if not flag4 and alcohol_burners_front.shape[0] != 0 and tube_foots_front.shape[0] != 0:
            for alcohol_burner_front in alcohol_burners_front:
                for tube_foot_front in tube_foots_front:
                    foot_alc_pos_y = center_distance_v(tube_foot_front[:4], alcohol_burner_front[:4]) < 0
                    foot_alc_pos_h = abs(center_distance_h(tube_foot_front[:4], alcohol_burner_front[:4])) < \
                                     abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                    if foot_alc_pos_y and foot_alc_pos_h:
                        flag4 = True
        # # 酒精灯和试管的关系
        # if not flag4 and alcohol_burners_front.shape[0] != 0 and tubes_front.shape[0] != 0:
        #     for alcohol_burner_front in alcohol_burners_front:
        #         for tube_front in tubes_front:
        #             tube_alc_pos_y = center_distance_v(tube_front[:4], alcohol_burner_front[:4]) < 0
        #             tube_alc_pos_h = abs(center_distance_h(tube_front[:4], alcohol_burner_front[:4])) < \
        #                              abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
        #             if tube_alc_pos_y and tube_alc_pos_h:
        #                 flag4 = True

        if flag4 and flames_front.shape[0] != 0:
            status = True
        if status:
            # self.scorePoint4 = True
            # self.assignScore(4, self.front_img0, self.front_preds)

            self.flagtime4_3_1, self.flagtime4_3_2, flag = self.duration(self.flagtime4_3_1, 1,
                                                                   self.flagtime4_3_2, 1)
            if flag:
                # self.scorePoint4 = True
                # self.assignScore(4, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    def shock(self, box):
        if len(self.shock_info) == 40:
            period = self.period(self.shock_info)
            if period > 2:
                return True
            self.shock_info.pop(0)
        self.shock_info.append(center_point(box)[0])

    def period(self, array):  # 震荡频率
        a = np.array(array)
        avg_1 = np.average(a[:10])
        avg_2 = np.average(a[-10:])
        avg = (avg_1 + avg_2) / 2
        if abs(avg_1 - avg_2) < self.h_front * 0.04:
            n = 0
            big = True
            for i, v in enumerate(a):
                if i == 0:
                    big = v > avg
                else:
                    if (v > avg and big) or (v < avg and not big):
                        continue
                    else:
                        if (abs(v - avg) > 4):
                            n += 1
                            big = v > avg
            return n // 2
        return 0

    # # 5 预热试管(来回移动酒精灯)
    def back_forth_move_tube(self,score_index, tubes_front, tube_foots_front, solid_reagents_front, alcohol_burners_front,
                                          flames_front):
        """
        预热试管(来回移动酒精灯):
        判断 酒精灯相对于底座的水平方向位置记录10~20个,求平均,判断每一个值相对于均值的摇摆情况判断是否进行左右晃动酒精灯;


        :param tubes_front:
        :param tube_foots_front:
        :param solid_reagents_front:
        :param alcohol_burners_front:
        :param flames_front:
        :return:
        """
        if alcohol_burners_front.shape[0] != 0:
            if tube_foots_front.shape[0] != 0:
                status = False
                for alcohol_burner_front in alcohol_burners_front:
                    for tube_foot_front in tube_foots_front:
                        if center_distance_v(tube_foot_front[:4], alcohol_burner_front[:4]) < 0 and \
                            abs(center_distance_h(tube_foot_front[:4], alcohol_burner_front[:4])) <  \
                                abs(alcohol_burner_front[:4][0]-alcohol_burner_front[:4][2]):
                            if len(self.foot_li1) < 20:
                                now_pos = center_point(alcohol_burner_front[:4])[0]
                                if self.move_pos != now_pos and now_pos not in self.foot_li1:
                                    self.foot_li1.append(now_pos)
                                    self.move_pos = now_pos
                            pass
                if len(self.foot_li1) == 8:
                    self.foot_li1.clear()
                    self.move_num += 1
                    # 将图片拼接到一张图
                    # if len(self.images) == 4:
                    #     self.images.append(cv2.resize(self.front_img0, (960,540)))
                    # if len(self.images) > 4:
                    #     self.images.pop(0)
                if self.move_num == 6:
                    status = True
                # print(f"self.move_num======={self.move_num}")
                if status:
                    # vtitch1 = np.vstack(self.images[:2])
                    # vtitch2 = np.vstack(self.images[2:])
                    # htitch = np.hstack((vtitch1, vtitch2))
                    # self.scorePoint5 = True
                    # self.assignScore(5, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

            if solid_reagents_front.shape[0] != 0:
                # print('566666')
                # print(self.foot_li1)
                # print(self.foot_li2)
                # print('56666')
                status = False
                for alcohol_burner_front in alcohol_burners_front:
                    for solid_reagent_front in solid_reagents_front:
                        if center_distance_v(solid_reagent_front[:4], alcohol_burner_front[:4]) < 0 and \
                                abs(center_distance_h(solid_reagent_front[:4], alcohol_burner_front[:4])) < \
                                abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2]):
                            if len(self.foot_li2) < 20:
                                now_pos = center_point(alcohol_burner_front[:4])[0]
                                if self.move_pos2 != now_pos and now_pos not in self.foot_li2:
                                    self.foot_li2.append(now_pos)
                                    self.move_pos2 = now_pos
                if len(self.foot_li1) == 8:
                    self.foot_li2.clear()
                    self.move_num2 += 1
                # print(f"move_num2======={self.move_num2}")
                if self.move_num2 == 6:
                    status = True
                if status:
                    # self.scorePoint5 = True
                    # self.assignScore(5, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 6 固体下方集中加热
    def focus_flame(self,score_index, alcohol_burners_front, flames_front, tubes_front, solid_reagents_front,tube_foots_front):
        """
        固体下方集中加热:
        1 在满足得分点五 试管预热的情况下,
        酒精灯在试管底部(药品)下部,左右方向在一个范围内,手与酒精灯没有交集 算固定加热

        :param alcohol_burners_front:
        :param flames_front:
        :param tubes_front:
        :param solid_reagents_front:
        :return:
        """
        status = False
        flag6 = False
        if solid_reagents_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0:
            for alcohol_burner_front in alcohol_burners_front:
                for solid_reagent_front in solid_reagents_front:
                    solid_flame_pos_y = center_distance_v(solid_reagent_front[:4], alcohol_burner_front[:4]) < 0
                    solid_flame_pos_h = abs(center_distance_h(solid_reagent_front[:4], alcohol_burner_front[:4])) < \
                                        abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                    if solid_flame_pos_h and solid_flame_pos_y:
                        flag6 = True
                        break
        if tube_foots_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0:
            for alcohol_burner_front in alcohol_burners_front:
                for tube_foot_front in tube_foots_front:
                    foot_flame_pos_y = center_distance_v(tube_foot_front[:4], alcohol_burner_front[:4]) < 0
                    foot_flame_pos_h = abs(center_distance_h(tube_foot_front[:4], alcohol_burner_front[:4])) < \
                                       abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                    if foot_flame_pos_y and foot_flame_pos_h:
                        flag6 = True
                        break
        # # 酒精灯和试管的关系
        # if not flag6 and alcohol_burners_front.shape[0] != 0 and tubes_front.shape[0] != 0:
        #     for alcohol_burner_front in alcohol_burners_front:
        #         for tube_front in tubes_front:
        #             tube_alc_pos_y = center_distance_v(tube_front[:4], alcohol_burner_front[:4]) < 0
        #             tube_alc_pos_h = abs(center_distance_h(tube_front[:4], alcohol_burner_front[:4])) < \
        #                              abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
        #             if tube_alc_pos_y and tube_alc_pos_h:
        #                 flag6 = True

        if flag6 and flames_front.shape[0] != 0:
            status = True
        if status:
            # self.scorePoint6 = True
            # self.assignScore(6, self.front_img0, self.front_preds)

            self.flagtime6, self.flagtime6_2, flag = self.duration(self.flagtime6, 1,
                                                                   self.flagtime6_2, 1)
            if flag:
                # self.scorePoint6 = True
                # self.assignScore(6, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 7用灯帽盖灭酒精灯
    def put_out_alcohol_lamp(self,score_index, alcohol_burners_front, lamp_caps_front, flames_front, alcohol_burners_top,
                             lamp_caps_top, flames_top):
        """
        加热结束后,用灯帽盖灭酒精灯:
        1 判断灯帽与酒精灯的垂直方向位置和水平方向位置 在一个范围内
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
                    lamp_cap_pos_h = abs(center_distance_h(alcohol_burner_front[:4], lamp_cap_front[:4])) < 0.5*abs(alcohol_burner_front[:4][0]-alcohol_burner_front[:4][2])
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
