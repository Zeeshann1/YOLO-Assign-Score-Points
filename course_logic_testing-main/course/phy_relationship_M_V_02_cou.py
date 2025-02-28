#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/02/19 14:34
# @Author  : Qiguangnan
# @File    : phy_relationship_M_V_02_cou.py

'''
探究物质质量和体积的关系(电子天平&盐水)
'''

from .comm import *
from .about_weigh_score_point_cou import AboutWeigh
from numpy import mean


class PHY_relationship_M_V_02(AboutWeigh):

    def __init__(self):
        super(PHY_relationship_M_V_02, self).__init__()
        self.scale_zero_info = []  # 记录清零信息
        self.cylinder_on_salver = False  # 量筒在天平上
        self.cylinder_not_on_salver_secs = 0
        self.cylinder_not_on_salver_secs_pre = 0
        self.cylinder_on_scalver = False
        self.water_cylinder_r_list = []
        self.water_cylinder_secs_list = []

        self.current_exp_num = 0
        self.exp_num = 2

    def score_process(self, *args):  # 赋分逻辑部分
        # return
        # ['手', '眼睛', '头', '抹布', '电子天平', '电子天平托盘', '天平开',
        # '天平置零', '天平关', '天平非零', '广口瓶',
        # '细口瓶', '细口瓶口', '瓶塞未倒放', '瓶塞倒放', '量筒', '量筒底', '水柱', '液体',
        # '食盐颗粒', '药匙', '药匙勺', '烧杯', '玻璃棒', '胶头滴管',
        # '标签']
        (hands_top, eyes_top, heads_top, dusters_top, scales_top, salvers_top, scale_ons_top,
         scale_zeros_top, scale_offs_top, scale_not_zeros_top, measuring_cylinders_top,
         measuring_cylinder_bottoms_top, water_columns_top, liquids_top, beakers_top) = self.preds_top

        (hands_front, eyes_front, heads_front, dusters_front, scales_front, salvers_front, scale_ons_front,
         scale_zeros_front, scale_offs_front, scale_not_zeros_front, measuring_cylinders_front,
         measuring_cylinder_bottoms_front, water_columns_front, liquids_front, beakers_front) = self.preds_front

        self.cylinder_on_salver = self.cylinderOnSalver(scales_top, salvers_top, measuring_cylinders_top,
                                                        measuring_cylinder_bottoms_top, scales_front, salvers_front,
                                                        measuring_cylinders_front, measuring_cylinder_bottoms_front)

        water_cylinder_r = self.w_m_r(water_columns_front, measuring_cylinders_front, measuring_cylinder_bottoms_front)
        if water_cylinder_r:  # 量筒中水柱占量筒比
            if len(self.water_cylinder_r_list) > 60:
                self.water_cylinder_r_list.pop(0)
            self.water_cylinder_r_list.append(float(water_cylinder_r))
            self.water_cylinder_secs_list.append(self.secs)
            if (self.current_exp_num == 0
                and len(self.water_cylinder_r_list) > 2
                and self.water_cylinder_secs_list[-1] - self.water_cylinder_secs_list[0]) > 2:
                self.current_exp_num = 1

        if self.current_exp_num == 1 and (self.scorePoint3 or self.scorePoint4):
            l = len(self.water_cylinder_r_list)
            if l > 50:
                cur_mean = mean(self.water_cylinder_r_list[-20:])
                pre_mean = mean(self.water_cylinder_r_list[:20])
                if cur_mean - pre_mean > pre_mean * 0.5:
                    self.current_exp_num = 2
        # 1.将量筒置于电子天平中央，完成电子天平"清零"操作
        if not self.scorePoint1:
            info = self.openScale(1, scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_not_zeros_top)
            if info:
                self.assignScore(*info[:6])
        # 2.将量筒置于电子天平中央，完成电子天平"清零"操作
        if not self.scorePoint2 and water_columns_front.shape[0] == 0:
            if self.cylinder_on_salver:
                self.scale_zero_info = self.updateInfoList(2, self.scale_zero_info, 'top', 1)
                info = self.scaleSetZero(2, hands_top, salvers_top, scales_top, hands_front, salvers_front,
                                         scales_front, scale_zeros_top)
                if info:
                    self.assignScore(*info[:6])
            elif self.scale_zero_info:
                self.cylinder_not_on_salver_secs, self.cylinder_not_on_salver_secs_pre, flag = self.duration(
                    self.cylinder_not_on_salver_secs, 1, self.cylinder_not_on_salver_secs_pre, 0.8)
                if flag:
                    if len(self.scale_zero_info) == 1:
                        self.assignScore(*self.scale_zero_info[-1])
                    else:
                        self.assignScore(*self.scale_zero_info[1])

        # 3.取下量筒，倒入适当的盐水，观察并记录量筒中液面对应的示数
        if self.current_exp_num == 1 and not self.scorePoint3 and water_columns_front.shape[
            0] == 1 and not self.cylinder_on_salver:
            info = self.readDisplayData(water_columns_front, heads_front, eyes_front)
            if info:
                self.assignScore(3, *info[:5])
                self.initReadCylinderDiaplayData()  # 初始化

        # 4.再将量筒置于电子天平中央，记录电子天平的示数
        if self.current_exp_num == 1 and not self.scorePoint4 and water_columns_front.shape[
            0] == 1 and self.cylinder_on_salver:
            salver_top_box = self.salverBox(salvers_top, scales_top)
            salver_front_box = self.salverBox(salvers_front, scales_front, view='front')
            if salver_front_box is not None and salver_top_box is None:
                return
            if self.handNotOnScale(hands_top, salver_top_box, hands_front, salver_front_box):
                self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 5.取下量筒，改变盐水的体积，观察并记录量筒中液面对应的示数
        if self.current_exp_num == 2 and not self.scorePoint5 and water_columns_front.shape[
            0] == 1 and not self.cylinder_on_salver:
            info = self.readDisplayData(water_columns_front, heads_front, eyes_front)
            if info:
                self.assignScore(5, *info[:5])
                self.initReadCylinderDiaplayData()  # 初始化

        # 6.再将量筒置于电子天平中央，记录电子天平的示数
        if self.current_exp_num == 2 and not self.scorePoint6 and water_columns_front.shape[
            0] == 1 and self.cylinder_on_salver:
            salver_top_box = self.salverBox(salvers_top, scales_top)
            salver_front_box = self.salverBox(salvers_front, scales_front, view='front')
            if salver_front_box is not None and salver_top_box is None:
                return
            if self.handNotOnScale(hands_top, salver_top_box, hands_front, salver_front_box):
                self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 7. 整理实验器材
        top_items = [scales_top, measuring_cylinders_top, measuring_cylinder_bottoms_top, beakers_top]
        front_items = [scales_front, measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front]
        if not self.scorePoint7 and len(self.score_list) > 3:
            info = self.clearnDesk([top_items, front_items],
                                   [self.center_area_top, self.center_area_front],
                                   ['top', 'front'])
            if info is not None:
                self.assignScore(7, *info[:5])

        if self.scorePoint7 and len(self.score_list) != 7:
            if not self.desk_is_clearn([top_items, front_items],
                                       [self.center_area_top, self.center_area_front],
                                       ['top', 'front']):
                self.initClearnDesk()
                self.retracementScore(7)

    def w_m_r(self, water_columns_front, measuring_cylinders_front, measuring_cylinder_bottoms_front):
        if (water_columns_front.shape[0] == 1
                and measuring_cylinders_front.shape[0] == 1
                and measuring_cylinder_bottoms_front.shape[0] == 1):  # 量筒， 量筒底， 水柱
            water_column_front_box = water_columns_front[0][:4]
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            measuring_cylinder_bottom_front_box = measuring_cylinder_bottoms_front[0][:4]
            bottom_w = width(measuring_cylinder_bottom_front_box)
            bottom_h = high(measuring_cylinder_bottom_front_box)
            if (center_distance_h(measuring_cylinder_bottom_front_box,
                                  measuring_cylinder_front_box, True) < bottom_w / 2
                    and center_distance_v(measuring_cylinder_bottom_front_box,
                                          measuring_cylinder_front_box) > bottom_h):
                water_cylinder_r = high(water_column_front_box) / high(measuring_cylinder_front_box)  # 水高 / 量筒高
                return water_cylinder_r
