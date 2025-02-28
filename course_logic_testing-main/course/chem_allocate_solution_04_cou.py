#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/2/19 09:42
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_03_cou.py

'''
一定溶质质量分数的NaCl溶液的配制(稀释)
'''

from .comm import *
import numpy as np
from .about_weigh_score_point_cou import AboutWeigh


class CHEM_allocate_solution_04(AboutWeigh):

    def __init__(self, *args, **kwargs):
        super(CHEM_allocate_solution_04, self).__init__(*args, **kwargs)

        self.drop_water_flag = True  # 滴加水标志

    def score_process(self ,top_true, front_true, side_true):  # 赋分逻辑部分
        # ['手', '眼睛', '头', '抹布', '电子天平', '电子天平托盘', '天平开',
        # '天平置零', '天平关', '天平非零', '广口瓶',
        # '细口瓶', '细口瓶口', '瓶塞未倒放', '瓶塞倒放', '量筒', '量筒底', '水柱', '液体',
        # '食盐颗粒', '药匙', '药匙勺', '烧杯', '玻璃棒', '胶头滴管',
        # '标签']
        (hands_top, eyes_top, heads_top, dusters_top, scales_top, salvers_top, scale_ons_top,
         scale_zeros_top, scale_offs_top, scale_not_zeros_top, wild_mouth_bottles_top,
         narrow_mouth_bottles_top, narrow_mouth_bottlenecks_top, stopper_ups_top, stopper_downs_top,
         measuring_cylinders_top, measuring_cylinder_bottoms_top, water_columns_top, liquids_top,
         salt_granules_top, spoons_top, spoon_us_top, beakers_top, glass_rods_top, droppers_top,
         labels_top) = self.preds_top

        (hands_front, eyes_front, heads_front, dusters_front, scales_front, salvers_front, scale_ons_front,
         scale_zeros_front, scale_offs_front, scale_not_zeros_front, wild_mouth_bottles_front,
         narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, stopper_ups_front, stopper_downs_front,
         measuring_cylinders_front, measuring_cylinder_bottoms_front, water_columns_front, liquids_front,
         salt_granules_front, spoons_front, spoon_us_front, beakers_front, glass_rods_front, droppers_front,
         labels_front) = self.preds_front

        # 量筒中加水
        if not self.water_in_cylinder:
            self.waterInCylinder(water_columns_front, measuring_cylinders_front)

        if not self.drop_water_flag:  # 胶头滴管滴加
            info = self.dropWaterIncylinder(droppers_front, measuring_cylinders_front, water_columns_front)
            if info:
                self.drop_water_flag = True

        # 1.向量筒中倾倒所需的氯化钠溶液至规定体积或接近规定体积；若接近规定体积，将量筒水平放置，用胶头滴管逐滴滴加至规定体积
        if not self.scorePoint1 and not self.scorePoint2:
            info = self.readDisplayData(water_columns_front, heads_front, eyes_front)
            if info is not None:
                self.drop_water_flag = True
                if self.drop_water_info:
                    box = self.drop_water_info[-3]
                    img = self.drop_water_info[0]
                    preds = self.drop_water_info[3]
                    dropper_water_frame = self.cropFrame(box, img, preds)
                    box = info[5]
                    img = info[0]
                    preds = info[3]
                    read_diaplay_frame = self.cropFrame(box, img, preds)
                    img = np.hstack([dropper_water_frame, read_diaplay_frame])
                    info[0] = img
                    info[3] = None
                self.assignScore(1, *info[:5])
                self.drop_water_flag = True
                self.initDropWater2Cylinder()

        # 2.把量取的氯化钠溶液全部倒入烧杯中
        if not self.scorePoint2:
            info = self.water2beaker(measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                                     liquids_front)
            if info is not None:
                self.assignScore(2, *info[:5])
                self.water_in_cylinder = False
                self.water_to_beaker_info = []
                self.drop_water_flag = False
                self.initDropWater2Cylinder()

        # 3. 向量筒中倾倒蒸馏水至规定体积或接近规定体积；若接近规定体积，将量筒水平放置，用胶头滴管逐滴滴加蒸馏水至规定体积
        if self.scorePoint2 and not self.scorePoint3:
            info = self.readDisplayData(water_columns_front, heads_front, eyes_front)
            if info is not None:
                self.drop_water_flag = True
                if self.drop_water_info:
                    box = self.drop_water_info[-3]
                    img = self.drop_water_info[1]
                    preds = self.drop_water_info[4]
                    dropper_water_frame = self.cropFrame(box, img, preds)
                    box = info[5]
                    img = info[0]
                    preds = info[3]
                    read_diaplay_frame = self.cropFrame(box, img, preds)
                    img = np.hstack([dropper_water_frame, read_diaplay_frame])
                    info[0] = img
                    info[3] = None
                self.assignScore(3, *info[:5])
                self.water_to_beaker_info = []
                self.drop_water_flag = True
                # self.initDropWaterInfo()

        # 4. 把量取的蒸馏水也全部倒入烧杯中
        if self.scorePoint2 and not self.scorePoint4:
            info = self.water2beaker(measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                                     liquids_front)
            if info is not None:
                self.assignScore(4, *info[:5])
                self.water_in_cylinder = False
                self.drop_water_flag = False
                # self.initDropWaterInfo()

        # 5. 用玻璃棒搅拌，混匀
        if not self.scorePoint5:
            info = self.stirDissolve(glass_rods_front, beakers_front, hands_front, 6, 3)
            if info is not None:
                self.assignScore(5, *info[:5])

        # 6. 将所得的溶液转移到指定容器中
        if not self.scorePoint6:
            info = self.transferLiquid(beakers_front, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front,
                                       hands_front)
            if info is not None:
                self.assignScore(6, *info[:5])

        top_items = [scales_top, wild_mouth_bottles_top, narrow_mouth_bottles_top, stopper_ups_top, stopper_downs_top,
                     measuring_cylinders_top, salt_granules_top, spoons_top, beakers_top, glass_rods_top, droppers_top]

        front_items = [scales_front, wild_mouth_bottles_front, narrow_mouth_bottles_front, stopper_ups_front,
                       stopper_downs_front, measuring_cylinders_front, liquids_front, salt_granules_front, spoons_front,
                       beakers_front, glass_rods_front, droppers_front]

        # 7. 清洗仪器，整理桌面
        if (not self.scorePoint7 and len(self.score_list) > 3):
            info = self.clearnDesk([top_items, front_items],
                                   [self.center_area_top, self.center_area_front],
                                   ['top', 'front'])
            if info:
                self.assignScore(7, *info[:5])
        if self.scorePoint7 and len(self.score_list) != 7:
            if not self.desk_is_clearn([top_items, front_items],
                                       [self.center_area_top, self.center_area_front],
                                       ['top', 'front']):
                self.retracementScore(7)

    def cropFrame(self, box, frame, preds):
        x = int(center_point(box)[0])
        if x < self.w_front / 4:
            x1, x2 = 0, int(self.w_front / 2)
        elif x < (self.w_front / 4) * 3:
            x1, x2 = int(x - self.w_front / 4), int(x + self.w_front / 4)
        else:
            x1, x2 = int(self.w_front / 2), int(self.w_front)
        self.plot(preds, frame)
        return frame[:, x1:x2, :]
