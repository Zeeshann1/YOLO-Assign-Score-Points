#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/2/19 09:42
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_03_cou.py

'''
一定溶质质量分数的NaCl溶液的配制(电子天平)
'''

from .comm import *
import numpy as np
from .about_weigh_score_point_cou import AboutWeigh
from copy import deepcopy


class CHEM_allocate_solution_03(AboutWeigh):

    def __init__(self, *args, **kwargs):
        super(CHEM_allocate_solution_03, self).__init__(*args, **kwargs)

        self.beaker_on_salver_time = 0.  # 烧杯放托盘上时间
        self.weight_info = []  # 记录称量信息
        self.weight_hand_info = []  # 记录称量信息（轻拍手腕或药匙）
        self.spoon_non_f_num = 0  # 没有药匙

        self.drop_water_flag = False  # 滴加水标志

        self.stopper_wrong_f_num = 0  # 瓶塞放置错误
        self.stopper_wrong_f_num_pre = 0

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分
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

        # 1.水平放置电子天平，打开电源
        if not self.scorePoint1:
            info = self.openScale(1, scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_not_zeros_top)
            if info:
                self.assignScore(*info)

        # 2.烧杯放置在称量盘上，按“去皮（清零）”键，示数归为零'
        if not self.scorePoint2:
            info = self.scaleZero(2, hands_top, salvers_top, scales_top, beakers_top, hands_front, salvers_front,
                                  scales_front, beakers_front, scale_zeros_top)
            if info:
                self.assignScore(*info)

        # 3.用药匙取固体氯化钠，轻拍手腕（或药匙柄）添加至规定质量
        if not self.scorePoint3:
            info = self.weighNaCl(3, stopper_downs_top, stopper_downs_front, salt_granules_front, spoons_front,
                                  spoon_us_front, beakers_front, spoons_top, spoon_us_top, hands_front, hands_top,
                                  salvers_front, scales_front, salvers_top, scales_top)
            if info:
                self.assignScore(*info)

        # 量筒中加水
        if not self.water_in_cylinder:
            self.waterInCylinder(water_columns_front, measuring_cylinders_front)

        if not self.drop_water_flag:  # 胶头滴管滴加
            info = self.dropWaterIncylinder(droppers_front, measuring_cylinders_front, water_columns_front)
            if info:
                self.drop_water_flag = True

        # 4. 向量筒中倾倒蒸馏水至规定体积或接近规定体积；若接近规定体积，将量筒水平放置，用胶头滴管逐滴滴加蒸馏水至规定体积
        if not self.scorePoint4:
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
                self.assignScore(4, *info[:5])

        # 5. 把量取的蒸馏水全部倒入烧杯中
        if not self.scorePoint5:
            info = self.water2beaker(measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                                     liquids_front)
            if info is not None:
                self.assignScore(5, *info[:5])

        # 6. 用玻璃棒搅拌，至固体药品全部溶解(前视)
        if not self.scorePoint6:
            info = self.stirDissolve(glass_rods_front, beakers_front, hands_front)
            if info is not None:
                self.assignScore(6, *info[:5])

        # 7. 将所得的溶液转移到指定容器中
        if not self.scorePoint7:
            info = self.transferLiquid(beakers_front, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front,
                                       hands_front)
            if info is not None:
                self.assignScore(7, *info[:5])

        top_items = [scales_top, wild_mouth_bottles_top, narrow_mouth_bottles_top, stopper_ups_top, stopper_downs_top,
                     measuring_cylinders_top, salt_granules_top, spoons_top, beakers_top, glass_rods_top, droppers_top]
        front_items = [scales_front, wild_mouth_bottles_front, narrow_mouth_bottles_front, stopper_ups_front,
                       stopper_downs_front, measuring_cylinders_front, liquids_front, salt_granules_front, spoons_front,
                       beakers_front, glass_rods_front, droppers_front]
        # 8. 清洗仪器，整理桌面
        if (not self.scorePoint8
                and scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_not_zeros_top.shape[0] == 0  # 天平关
                and (len(self.score_list) > 4)):
            info = self.clearnDesk([top_items, front_items],
                                   [self.center_area_top, self.center_area_front],
                                   ['top', 'front'])
            if info:
                self.assignScore(8, *info[:5])
        if self.scorePoint8 and len(self.score_list) != 8:
            if not self.desk_is_clearn([top_items, front_items],
                                       [self.center_area_top, self.center_area_front],
                                       ['top', 'front']):
                self.retracementScore(8)

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

    # 烧杯放置在称量盘上，按“去皮（清零）”键，示数归为零
    def scaleZero(self, score_index, hands_top, salvers_top, scales_top, beakers_top, hands_front, salvers_front,
                  scales_front, beakers_front, scale_zeros_top):
        beaker_on_salver = False  # 烧杯在托盘上
        salver_top_box = self.salverBox(salvers_top, scales_top)
        salver_front_box = self.salverBox(salvers_front, scales_front, 'front')
        if hands_top.shape[0] > 0 and salver_top_box is not None and beakers_top.shape[0] > 0:  # 显示0.0
            if pt_in_polygon(center_point(salver_top_box), self.center_area_top):  # 天平托盘在实验区域
                for beaker_top in beakers_top:
                    beaker_top_box = beaker_top[:4]
                    if iou(beaker_top_box, salver_top_box) >= box_area(beaker_top_box) * 0.8:
                        beaker_on_salver = True
        if (not beaker_on_salver
                and beakers_front.shape[0] > 0
                and salver_front_box is not None
                and hands_front.shape[0] > 0):  # 前视 托盘 烧杯
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                if iou(beaker_front_box, salver_front_box) > 0 and \
                        abs(center_distance_h(beaker_front_box, salver_front_box)) < self.h_front * 0.052:
                    beaker_on_salver = True
        if beaker_on_salver:  # 烧杯在托盘中
            if self.beaker_on_salver_time == 0:
                self.beaker_on_salver_time = self.secs
            elif self.secs - self.beaker_on_salver_time > 0.3:  # 烧杯放上去大于 0.3  秒
                info = self.scaleSetZero(score_index, hands_top, salvers_top, scales_top, hands_front, salvers_front,
                                         scales_front, scale_zeros_top)
                if info:
                    if not self.scorePoint1:
                        info[0] = 1
                        self.assignScore(*info)
                    info[0] = 2
                    return info[:6]
                if not self.scorePoint2 and self.secs - self.beaker_on_salver_time > 3 and self.scale_zero_info:  # 超过 n 秒自动赋分
                    if not self.scorePoint1:
                        self.scale_zero_info[0] = 1
                        self.assignScore(*self.scale_zero_info)
                    self.scale_zero_info[0] = score_index
                    return self.scale_zero_info
                if self.scorePoint1 and not self.scorePoint2 and self.secs - self.beaker_on_salver_time > 4:  # 超过 n 秒自动赋分
                    return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top

    # 3. 用药匙取固体氯化钠，轻拍手腕（或药匙柄）添加至规定质量 # todo 拍手腕
    def weighNaCl(self, score_index, stopper_downs_top, stopper_downs_front, salt_granules_front, spoons_front,
                  spoon_us_front, beakers_front, spoons_top, spoon_us_top, hands_front, hands_top, salvers_front,
                  scales_front, salvers_top, scales_top):
        # if (salt_granules_front.shape[0] > 0 and
        #         spoons_front.shape[0] > 0 and
        #         beakers_front.shape[0] > 0):
        #     NaCL_powder_front_box = salt_granules_front[0][:4]
        #     spoon_front_box = spoons_front[0][:4]
        #     beaker_front_box = beakers_front[0][:4]
        #     salver_front_box = self.salverBox(salvers_front, scales_front, 'front')
        #     if (salver_front_box is not None and
        #             iou(NaCL_powder_front_box, beaker_front_box) > 0 and
        #             center_distance_v(NaCL_powder_front_box, beaker_front_box) > 0 and
        #             iou(NaCL_powder_front_box, salver_front_box) > box_area(NaCL_powder_front_box) * 0.5 and
        #             center_distance_h(NaCL_powder_front_box, salver_front_box, True) <
        #             (salver_front_box[2] - salver_front_box[0]) * 0.35 and  # 烧杯底有 食盐颗粒 在托盘上
        #             iou(beaker_front_box, spoon_front_box) > 0):  # 前视药匙和烧杯有交集
        #         self.weight_info = [score_index, self.frame_front, self.time_front, self.objects_front,
        #                             self.preds_front, self.num_frame_front, self.secs]
        salver_top_box = self.salverBox(salvers_top, scales_top)
        if (salt_granules_front.shape[0] > 0
                and hands_top.shape[0] >= 2
                and spoons_top.shape[0] > 0
                and salver_top_box is not None):
            salt_granule_front_box = salt_granules_front[0][:4]
            spoon_top_box = spoons_top[0][:4]
            if iou(salver_top_box, spoon_top_box) > box_area(spoon_top_box) * 0.35:
                hand_spoon = 0
                spoon_hand_box = None
                hand_box_list = []
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    if (pt_in_polygon(center_point(hand_top_box), self.center_area_top)
                            and iou(spoon_top_box, hand_top_box) > 0):
                        hand_spoon += 1
                        spoon_hand_box = deepcopy(hand_top_box)
                    else:
                        hand_box_list.append(hand_top_box)
                if hand_spoon == 2:  # 两只手与药匙相交
                    self.weight_hand_info = [score_index, self.frame_top, self.time_top, self.objects_top,
                                             self.preds_top, self.num_frame_top, self.secs]
                elif hand_spoon == 1:
                    w = (spoon_hand_box[2] - spoon_hand_box[0]) * 0.2
                    h = (spoon_hand_box[3] - spoon_hand_box[1]) * 0.85
                    orientation = 'right'  # 用右手拿药匙
                    if spoon_us_top.shape[0] > 0:
                        spoon_u_top_box = spoon_us_top[0][:4]
                        if center_distance_h(spoon_top_box, spoon_u_top_box) < 0:
                            orientation = 'left'
                    elif spoon_us_front.shape[0] > 0 and spoons_front.shape[0] > 0:
                        spoon_u_front_box = spoon_us_front[0][:4]
                        spoon_front_box = spoons_front[0][:4]
                        if center_distance_h(spoon_front_box, spoon_u_front_box) > 0:
                            orientation = 'left'
                    else:
                        if center_distance_h(spoon_top_box, salver_top_box) < 0:  # 药匙在左
                            orientation = 'left'
                    if orientation == 'right':
                        spoon_hand_box[0] += w
                        spoon_hand_box[2] += w
                    else:  # 药匙在左
                        spoon_hand_box[0] -= w
                        spoon_hand_box[2] -= w
                    spoon_hand_box[1] += h
                    spoon_hand_box[3] += h
                    for hand_top_box in hand_box_list:
                        if iou(spoon_hand_box, hand_top_box) > 0:
                            self.weight_hand_info = [score_index, self.frame_top, self.time_top, self.objects_top,
                                                     self.preds_top, self.num_frame_top, self.secs]
        if self.weight_hand_info:
            return self.weight_hand_info[:6]

        # if self.weight_info and self.secs - self.weight_info[-1] > 1:
        #     if spoons_front.shape[0] == 0 and spoons_top.shape[0] == 0:
        #         if self.spoon_non_f_num == 0:
        #             self.spoon_non_f_num = self.secs
        #         elif self.secs - self.spoon_non_f_num > 1:
        #             return self.weight_info[:6]
        #     else:
        #         self.spoon_non_f_num = 0
        #     if spoons_front.shape[0] > 0 and hands_front.shape[0] > 0:
        #         spoon_front_box = spoons_front[0][:4]
        #         hands_spoon_front = False  # 手和药匙有交集
        #         for hand_front in hands_front:
        #             hand_front_box = hand_front[:4]
        #             if iou(hand_front_box, spoon_front_box) > 0:
        #                 hands_spoon_front = True
        #                 break
        #         if not hands_spoon_front:
        #             return self.weight_info[:6]
        #     elif not self.scorePoint3 and hands_top.shape != 0 and spoons_top.shape[0] > 0:
        #         spoon_top_box = spoons_top[0][:4]
        #         hands_spoon_top = False  # 手和药匙有交集?
        #         for hand_top in hands_top:
        #             hand_top_box = hand_top[:4]
        #             if iou(hand_top_box, spoon_top_box) > 0:
        #                 hands_spoon_top = False
        #                 break
        #         if hands_spoon_top:
        #             return self.weight_info[:6]

        if (stopper_downs_top.shape[0] + stopper_downs_front.shape[0] > 0 and self.is_teach):
            self.stopper_wrong_f_num, self.stopper_wrong_f_num_pre, flag = self.duration(self.stopper_wrong_f_num,
                                                                                         2,
                                                                                         self.stopper_wrong_f_num_pre,
                                                                                         0.5)
            pass
            # if stopper_downs_front.shape[0] != 0 and flag:
            #     self.faultyOperation(1, '瓶塞放置错误，应该倒放在桌面上', self.front_img0, self.front_preds)
            # elif stopper_downs_top.shape[0] != 0 and flag:
            #     self.faultyOperation(1, '瓶塞放置错误，应该倒放在桌面上', self.top_img0, self.top_preds)
