#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/12/22 12:55
# @File    : chem_access_and_heat_beaker_liquid_heat_cou.py

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


class CHEM_access_and_heat_beaker_liquid_heat(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(CHEM_access_and_heat_beaker_liquid_heat, self).__init__(*args, **kwargs)
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
        self.flagtime2 = 0.
        self.flagtime2_2 = 0.
        self.flagtime2_2_1 = 0.
        self.flagtime2_2_2 = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
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

        self.clearn_time = 0.
        self.clearn_desk_info = []

        self.scoreframe2 = 0
        self.scoreframe3 = 0
        self.scoreframe3_2 = 0
        self.scoreframe4 = 0

        self.set_center_box = False  # 设置中心操作区域

        # 实验标志
        self.flag1 = False

        self.ring_pos = 0.0
        self.ring_pos_num = 0
        self.ring_pos_list = []

        self.flag7 = False
        # self.scorePoint3_info = [[], []]
        # self.flag3 = False
        # self.flag3_gla_bubb = False

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
        # hands_front, flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        # matchs_front, thermometers_front, glass_bubbles_front, holders_front, beakers_front, measure_cups_front, \
        # water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front = self.front_preds
        #
        # hands_top, flames_top, alcohol_burners_top, lamp_caps_top, asbestos_nets_top, \
        # matchs_top, thermometers_top, glass_bubbles_top, holders_top, beakers_top, measure_cups_top, \
        # water_columns_top, match_flames_top, stop_watchs_top, hand_stop_watchs_top, bases_top = self.top_preds


        hands_front, flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        matchs_front, thermometers_front, glass_bubbles_front, holders_front, beakers_front, measure_cups_front, \
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front,\
        oil_columns_front, scales_front, narrow_bottles_front, iron_rings_front, iron_poles_front, tubes_front, \
        tube_mouths_front, tube_foots_front, iron_clamp_heads_front, iron_clamps_front, wood_clamps_front, \
        wood_clamp_heads_front, clean_waters_front, solid_reagents_front, matchboxs_front, woods_front = self.preds_front

        hands_top, flames_top, alcohol_burners_top, lamp_caps_top, asbestos_nets_top, \
        matchs_top, thermometers_top, glass_bubbles_top, holders_top, beakers_top, measure_cups_top, \
        water_columns_top, match_flames_top, stop_watchs_top, hand_stop_watchs_top, bases_top, \
        oil_columns_top, scales_top, narrow_bottles_top, iron_rings_top, iron_poles_top, tubes_top, \
        tube_mouths_top, tube_foots_top, iron_clamp_heads_top, iron_clamps_top, wood_clamps_top, \
        wood_clamp_heads_top, clean_waters_top, solid_reagents_top, matchboxs_top, woods_top = self.preds_top

        try:
            # 1 放置铁架台
            if not self.scorePoint1:
                info = self.place_iron_platform(1, bases_front, bases_top)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 2 放置酒精灯
            if self.scorePoint1 and not self.scorePoint2:
                info = self.place_alcohol_lamp(2, bases_front, alcohol_burners_front, hands_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 3 调节铁圈高度
            if self.scorePoint1 and not self.scorePoint3:
                info = self.adjust_ironring_height(3, iron_rings_front, bases_front, hands_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 4 放置石棉网
            if self.scorePoint1 and not self.scorePoint4:
                info = self.place_asbestos_net(4, bases_front, asbestos_nets_front, hands_front, iron_rings_front)
                if info is not None:
                    self.assignScore(*info)
                pass
            # 5 放置烧杯
            if self.scorePoint4 and not self.scorePoint5:
                info = self.place_beaker(5, asbestos_nets_front, beakers_front, bases_front, hands_front)
                if info is not None:
                    self.assignScore(*info)
                pass


            # 6 点燃酒精灯,外焰加热
            if self.scorePoint5 and not self.scorePoint6:
                info = self.light_the_alcohol_lamp(6,alcohol_burners_front, matchs_front, flames_front, beakers_front,
                                           water_columns_front, asbestos_nets_front, holders_front, match_flames_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 7 加热结束后,用灯帽盖灭酒精灯
            if self.scorePoint6 and not self.scorePoint7:
                info =  self.put_out_alcohol_lamp(7,alcohol_burners_front, lamp_caps_front, flames_front)
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
                info = self.clearn_desk(8,top_items, front_items)
                if info is not None:
                    self.assignScore(*info)

            if self.scorePoint8 and len(self.score_list) != 8:
                if not self.desk_is_clearn([top_items,front_items], [self.center_area_top,self.center_area_front]):
                    self.retracementScore(8)
        except:
            logger.error(traceback.format_exc())

    # 1 放置铁架台
    def place_iron_platform(self,score_index, bases_front, bases_top):
        """
        放置铁架台 :
        铁架台在设置中操作区域内
        :param bases_front:
        :param bases_top:
        :return:
        """
        if bases_front.shape[0] != 0:
            base_in_test_area = False

            for base_front in bases_front:
                if pt_in_polygon(center_point(base_front[:4]),self.center_area_top):
                # if iou(base_front[:4], self.center_box_top):
                    base_in_test_area = True
                    pass
            if base_in_test_area:
                self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 3.0, self.flagtime1_2, 3)
                if flag:
                    # self.scorePoint1 = True
                    # self.assignScore(1, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


    # 2 放置酒精灯
    def place_alcohol_lamp(self,score_index, bases_front, alcohol_burners_front, hands_front):
        """
            1手和酒精灯有交集
            2 满足1 条件下 酒精灯垂直方向中心点小于底座垂直方向中心点,酒精灯水平方向中心点与底座水平方向中心点在一个阈值内,表明酒精灯在底座上
            满足 1,2 持续时间1s;
        """
        if bases_front.shape[0] != 0 and alcohol_burners_front.shape[0] != 0:
            hand_alco_status = False
            alcohol_burner_status = False
            for hand_front in hands_front:
                for alcohol_burner_front in alcohol_burners_front:
                    hand_alco_iou = iou(hand_front[:4], alcohol_burner_front[:4])
                    if hand_alco_iou > 0:
                        hand_alco_status = True
                        break
            if hand_alco_status:
                for base_front in bases_front:
                    for alcohol_burner_front in alcohol_burners_front:
                        alc_base_v_pos = center_distance_v(alcohol_burner_front[:4], base_front[:4]) < 0  # 酒精灯在 底座上面
                        alc_base_h_pos = abs(center_distance_h(alcohol_burner_front[:4], base_front[:4])) < 0.25*abs(base_front[:4][0]-base_front[:4][2])
                        if alc_base_v_pos and alc_base_h_pos:
                            alcohol_burner_status = True
                            break
            if alcohol_burner_status:
                self.flagtime2, self.flagtime2_2, flag = self.duration(self.flagtime2, 0.1, self.flagtime2_2, 0.1)
                if flag:
                    # self.scorePoint2 = True
                    # self.assignScore(2, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        pass

    # 3调节铁圈高度
    def adjust_ironring_height(self,score_index, iron_rings_front, bases_front, hands_front):
        """
        前视角:
            1 手和铁圈有交集;
            2 满足条件1 铁圈中心点与底座中心点水平方向在一个阈值内,铁圈中心点垂直方向距离小于底座垂直方向距离--铁圈在底座上
            3 满足条件2 当铁圈位置改变且手与铁圈位置有交集;则证明调节铁圈高度
        """
        if iron_rings_front.shape[0] != 0 and bases_front.shape[0] != 0:
            # print(self.ring_pos_list)
            hand_ring_status = False
            regulate_ring_status = False
            for hand_front in hands_front:
                for iron_ring_front in iron_rings_front:
                    hand_ring_iou = iou(hand_front[:4], iron_ring_front[:4])
                    if hand_ring_iou > 0:
                        hand_ring_status = True
            if hand_ring_status:
                for iron_ring_front in iron_rings_front:
                    for base_front in bases_front:
                        iron_rings_base_h = abs(center_distance_h(iron_ring_front[:4], base_front[:4])) < \
                                            abs(base_front[:4][0] - base_front[:4][2])  # 铁圈水平位置相对底座在一个范围内
                        iron_rings_base_y = center_distance_v(base_front[:4], iron_ring_front[:4])  # 铁圈在底座上面
                        if iron_rings_base_h and iron_rings_base_y > 0:
                            center_ring_y = center_point(iron_ring_front[:4])[1]
                            if center_ring_y != self.ring_pos and center_ring_y not in self.ring_pos_list and \
                                    len(self.ring_pos_list) < 12:
                                self.ring_pos_list.append(center_ring_y)
                            if len(self.ring_pos_list) == 10:
                                self.ring_pos_num += 1
                                self.ring_pos_list.clear()
                                for hand_front in hands_front:
                                    hand_ring_iou2 = iou(hand_front[:4], iron_ring_front[:4])
                                    if hand_ring_iou2 > 0:
                                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                            # if self.ring_pos_num == 4:
                            #     # self.scorePoint3 = True
                            #     # self.assignScore(3, self.front_img0, self.front_preds)
                            #     return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

            # if regulate_ring_status:
            #     self.flagtime3, self.flagtime3_2, flag = self.duration(self.flagtime3, 0.1, self.flagtime3_2, 0.1)
            #     if flag:
            #         self.scorePoint3 = True
            #         self.assignScore(3, self.front_img0, self.front_preds)

    # 4放置石棉网
    def place_asbestos_net(self,score_index, bases_front, asbestos_nets_front, hands_front, iron_rings_front):
        """
        放置石棉网:
        1 手与石棉网有交集 给一个状态
        2 满足状态1 石棉网与铁圈有交集 且石棉网中心点垂直方向距离在铁圈中心点垂直方向距离上方
        满足 1,2 条件 成立
        :param bases_front:
        :param asbestos_nets_front:
        :return:
        """
        if bases_front.shape[0] != 0 and asbestos_nets_front.shape[0] != 0 and iron_rings_front.shape[0] != 0:
            hand_asb_net_status = False
            asb_net_status = False
            for hand_front in hands_front:
                for asbestos_net_front in asbestos_nets_front:
                    hand_net_iou = iou(asbestos_net_front[:4], hand_front[:4])
                    if hand_net_iou > 0:
                        hand_asb_net_status = True
                        break
            # if hand_asb_net_status:
            #     for base_front in bases_front:
            #         for asbestos_net_front in asbestos_nets_front:
            #             asb_net_base_pos_v = center_distance_v(base_front[:4], asbestos_net_front[:4]) > 0
            #             asb_net_base_pos_h = abs(center_distance_h(base_front[:4], asbestos_net_front[:4])) < 0.5*abs(base_front[:4][0]-base_front[:4][2])
            #             if asb_net_base_pos_v and asb_net_base_pos_h:
            #                 asb_net_status = True
            #                 break
            if hand_asb_net_status:
                for asbestos_net_front in asbestos_nets_front:
                    for iron_ring_front in iron_rings_front:
                        asb_net_base_pos_v = center_distance_v(iron_ring_front[:4], asbestos_net_front[:4]) > 0
                        if iou(asbestos_net_front[:4], iron_ring_front[:4])>0 and asb_net_base_pos_v:
                            asb_net_status = True
                            break
                        # asb_net_base_pos_h = abs(center_distance_h(iron_ring_front[:4], asbestos_net_front[:4])) < abs(base_front[:4][0]-base_front[:4][2])
                        # if asb_net_base_pos_v and asb_net_base_pos_h:
                        #     asb_net_status = True
                        #     break

            if asb_net_status:
                self.flagtime4, self.flagtime4_2, flag = self.duration(self.flagtime4, 0.1, self.flagtime4_2, 0.1)
                if flag:
                    # self.scorePoint4 = True
                    # self.assignScore(4, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                # self.scorePoint4 = True
                # self.assignScore(4, self.front_img0, self.front_preds)

    # 5放置烧杯
    def place_beaker(self,score_index, asbestos_nets_front, beakers_front, bases_front, hands_front):
        """
        放置烧杯:
        1 手与烧杯有交集 状态1
        2满足条件1,烧杯中心点垂直方向距离在石棉网中心点垂直方向距离上方, 烧杯中心点的水平位置与石棉网中心点水平位置在一个范围内
        3 满足2 条件 完毕
        :param asbestos_nets_front:
        :param beakers_front:
        :param bases_front:
        :return:
        """
        if asbestos_nets_front.shape[0] != 0 and beakers_front.shape[0] != 0 and bases_front.shape[0] != 0:
            hand_beaker_status = False
            beaker_status = False
            for hand_front in hands_front:
                for beaker_front in beakers_front:
                    hand_beaker_iou = iou(hand_front[:4], beaker_front[:4])
                    if hand_beaker_iou > 0:
                        hand_beaker_status = True
                        break
            if hand_beaker_status:
                for asbestos_net_front in asbestos_nets_front:
                    for beaker_front in beakers_front:
                        beaker_asb_pos_v = center_distance_v(asbestos_net_front[:4], beaker_front[:4]) > 0
                        beaker_asb_pos_h = abs(center_distance_h(asbestos_net_front[:4], beaker_front[:4])) < 0.25*abs(beaker_front[:4][0] - beaker_front[:4][2])
                        if beaker_asb_pos_h and beaker_asb_pos_v:
                            beaker_status = True
                            break
            if beaker_status:
                # self.flagtime5, self.flagtime5_2, flag = self.duration(self.flagtime5, 0.5, self.flagtime5_2, 0.5)
                # if flag:
                #     self.scorePoint5 = True
                #     self.assignScore(5, self.front_img0, self.front_preds)
                # self.scorePoint5 = True
                # self.assignScore(5, self.front_img0, self.front_preds)
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 6点燃酒精灯,外焰加热
    def light_the_alcohol_lamp(self,score_index,alcohol_burners_front, matchs_front, flames_front, beakers_front,
                                           water_columns_front, asbestos_nets_front, holders_front, match_flames_front):
        """
        点燃酒精灯,外焰加热
        :
        1 打火机点燃酒精灯状态;
        2 在条件1下 烧杯中心点水平方向与酒精灯中心点水平方向在一个阈值,烧杯中心点垂直方向高出酒精灯垂直方向一个阈值;
        保持状态 完毕
        :param alcohol_burners_front:
        :param matchs_front:
        :param flames_front:
        :param beakers_front:
        :param water_columns_front:
        :param asbestos_nets_front:
        :param holders_front:
        :param match_flames_front:
        :return:
        """
        # 打火机点燃酒精灯

        # if alcohol_burners_front.shape[0] != 0 and beakers_front.shape[0] != 0 and water_columns_front.shape[0] != 0:
        if alcohol_burners_front.shape[0] != 0 and beakers_front.shape[0] != 0:
            if match_flames_front.shape[0] != 0 and not self.flag1:
                self.flag1 = True
            if flames_front.shape[0] != 0 and not self.flag1:
                # 火焰持续3秒存在 标志为true
                self.flagtime2_2_1, self.flagtime2_2_2, flag = self.duration(self.flagtime2_2_1, 0.1, self.flagtime2_2_2,
                                                                             0.1)
                if flag:
                    # self.scorePoint2 = True
                    # self.assignScore(2, self.front_img0, self.front_preds)
                    self.flag1 = True
            # 酒精灯外焰加热
            if self.flag1:
                status = False
                for beaker_front in beakers_front:
                    for alcohol_burner_front in alcohol_burners_front:
                        beaker_alco_burner_pos_x = abs(
                            center_distance_h(beaker_front[:4], alcohol_burner_front[:4])) < \
                                                   abs(alcohol_burner_front[:4][0] - alcohol_burner_front[:4][2])
                        # 烧杯在酒精灯上方: 烧杯box中心点大于 ((0.5*烧杯box的y)+(0.5*酒精灯box的y))
                        beaker_alco_burner_pos_y = center_distance_v(alcohol_burner_front[:4], beaker_front[:4])\
                                                   > 0.5 * abs(alcohol_burner_front[1] -
                                                               alcohol_burner_front[3]) + 0.5 * abs(beaker_front[1]
                                                                                                    - beaker_front[3])
                        if beaker_alco_burner_pos_x and beaker_alco_burner_pos_y:
                            status = True
                            break
                if status:
                    self.flagtime6, self.flagtime6_2, flag = self.duration(self.flagtime6, 0.1, self.flagtime6_2, 0.1)
                    if flag:
                        # self.scorePoint6 = True
                        # self.assignScore(6, self.front_img0, self.front_preds)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 7加热结束后,用灯帽盖灭酒精灯
    def put_out_alcohol_lamp(self,score_index, alcohol_burners_front, lamp_caps_front, flames_front):
        """
        加热结束后,用灯帽盖灭酒精灯:
        1 垂直方向上 酒精灯在灯帽下方; 水平方向上,酒精灯与灯帽在一个阈值范围内;
        2 在条件1下,酒精灯与灯帽有交集
        3 满足 2 状态,当乜有火焰时 完毕
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
                        # alcohol_status = True
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
