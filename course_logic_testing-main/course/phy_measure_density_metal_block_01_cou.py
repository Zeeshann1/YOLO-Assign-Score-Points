#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 14:34
# @Author  : Qiguangnan
# @File    : phy_measure_density_01_cou.py.py

'''
测量金属块的密度(电子天平)
'''

from .comm import *
from .comm.course_base import ConfigModel


class PHY_measure_density_metal_block_01(ConfigModel):

    def __init__(self):
        super(PHY_measure_density_metal_block_01, self).__init__()
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

        self.scale_on_secs = 0.
        self.scale_on_secs_pre = 0.
        self.open_scale_secs = 0.  # 打开天平的时间
        self.scale_zero_secs = 0.
        self.scale_zero_info = []
        self.start_weight = False
        self.weight_secs = 0.
        self.weight_secs_pre = 0.
        self.weight_info = []  # 记录称量信息
        self.water_column_secs = 0.  # 添加水
        self.water_column_secs_pre = 0.
        self.add_water_beaker_info = []  # 用烧杯向量筒加水信息
        self.add_water_info = []
        self.see_display_secs = 0.
        self.see_display_secs_pre = 0.
        self.see_display_info = []  # 读示数
        self.see_display_head_info = []  # 读示数（只有头）
        self.see_display_block_secs = 0.
        self.see_display_block_secs_pre = 0.
        self.see_display_block_info = []  # 读示数（有物块）
        self.see_display_block_head_info = []  # 读示数（有物块）（只有头）
        self.block_in_water_secs = 0.
        self.block_in_water_secs_pre = 0.
        self.clearn_secs = 0.
        self.clearn_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, time_frame, object, preds, num_frame, conf, name_save, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分
        (hands_top, eyes_top, heads_top, dusters_top, scales_top, salvers_top, scale_ons_top, scale_zeros_top,
         scale_offs_top, scale_notzeros_top, blocks_top, measuring_cylinders_top, measuring_cylinder_ds_top,
         water_columns_top, liquids_top, beakers_top) = self.preds_top

        (hands_front, eyes_front, heads_front, dusters_front, scales_front, salvers_front, scale_ons_front,
         scale_zeros_front, scale_offs_front, scale_notzeros_front, blocks_front, measuring_cylinders_front,
         measuring_cylinder_ds_front, water_columns_front, liquids_front, beakers_front) = self.preds_front

        # 1.打开电子天平
        if not self.scorePoint1:
            if self.open_scale(scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_notzeros_top):
                self.assignScore(1, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

        # 2.检查电子天平初始示数，若不为0进行清零操作
        if self.scorePoint1 and not self.scorePoint2:
            info = self.set_zeron(2, scale_zeros_top, scales_top)
            if info is not None:
                self.assignScore(*info)

        # 3.将系有细线的金属块置于电子天平中央，记录电子天平的示数
        if not self.scorePoint3:
            info = self.weight_block(3, blocks_top, blocks_front, salvers_top, scales_top, salvers_front, scales_front,
                                     hands_top, hands_front)
            if info is not None:
                self.assignScore(*info)

        # 4.在量筒中倒入适量的水
        # 量筒中有水， 前视
        if not self.scorePoint4:
            info = self.add_water(4, water_columns_front, beakers_front, measuring_cylinders_front)
            if info is not None:
                self.assignScore(*info)

        # 5 观察并记录量筒中水面对应的示数
        if not self.scorePoint5:
            self.record_V_display(measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                  blocks_front)

        # 6 将系有细线的金属块放入量筒并㓎没在水中 前视
        if not self.scorePoint6:
            info = self.block_in_water(6, measuring_cylinders_front, measuring_cylinders_top, water_columns_front,
                                       blocks_front, blocks_top)
            if info is not None:
                self.assignScore(*info)

        # 7 观察并记录量筒中水面对应的示数
        if not self.scorePoint7 and self.scorePoint6:
            self.record_V_display(measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                  blocks_front)

        # # 9 把量取的水倒入烧杯中
        # # 前视
        # if not self.scorePoint9:
        #     if hands_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0 and beakers_front.shape[
        #         0] > 0:
        #         beaker_front_box = beakers_front[0][:4]
        #         measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
        #         if w_h_ratio(measuring_cylinder_front_box) > 1.0 and iou(measuring_cylinder_front_box,
        #                                                                  beaker_front_box) > 0:  # 量筒横放与烧杯有交点
        #             self.scorePoint9 = True

        # 8 清洗仪器，整理桌面
        top_items = [scales_top, measuring_cylinders_top, beakers_top, blocks_top, dusters_top]
        front_items = [scales_front, measuring_cylinders_front, beakers_front, blocks_front, dusters_front]
        if (not self.scorePoint8
                and scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[0] == 0
                and (self.scorePoint3 or self.scorePoint5 or self.scorePoint6)):
            info = self.clearn_desk(8, top_items, front_items)
            if info is not None:
                self.assignScore(*info)
        if self.scorePoint8 and len(self.score_list) != 8:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(8)

    # 打开天平
    def open_scale(self, scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_notzeros_top):
        if scales_top.shape[0] > 0:
            scale_top_box = scales_top[0][:4]
            if pt_in_polygon(center_point(scale_top_box), self.center_area_top):
                if scale_offs_top.shape[0] == 0 and (
                        scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[
                    0] != 0):  # 天平打开
                    display_in_scale = False
                    if scale_ons_top.shape[0] > 0:
                        scale_on_box = scale_ons_top[0][:4]
                        if box1_in_box2(scale_on_box, scale_top_box):
                            display_in_scale = True
                    if not display_in_scale and scale_zeros_top.shape[0] > 0:
                        scale_zero_box = scale_zeros_top[0][:4]
                        if box1_in_box2(scale_zero_box, scale_top_box):
                            display_in_scale = True
                    if not display_in_scale and scale_notzeros_top.shape[0] > 0:
                        scale_notzero_box = scale_notzeros_top[0][:4]
                        if box1_in_box2(scale_notzero_box, scale_top_box):
                            display_in_scale = True
                    if display_in_scale:
                        self.scale_on_secs, self.scale_on_secs_pre, flag = self.duration(self.scale_on_secs, 1,
                                                                                         self.scale_on_secs_pre, 0.5)
                        if flag:
                            self.open_scale_secs = self.secs
                            return True

    # 天平置零
    def set_zeron(self, score_index, scale_zeros_top, scales_top):
        if scale_zeros_top.shape[0] > 0 and scales_top.shape[0] > 0:  # 显示0.0
            scale_top_box = scales_top[0][:4]
            scale_zero_top_box = scale_zeros_top[0][:4]
            if box1_in_box2(scale_zero_top_box, scale_top_box):
                if self.secs - self.open_scale_secs > 0.5:
                    self.scale_zero_secs, _, flag = self.duration(self.scale_zero_secs, 0.3)
                    return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top

        if not self.scorePoint2 and self.secs - self.open_scale_secs > 3:  # 6 秒后自动赋分
            self.assignScore(2, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

        if not self.start_weight:  # 称量物块前
            if not self.scale_zero_info:
                self.scale_zero_info.append(
                    [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                     self.secs])
            elif len(self.scale_zero_info) == 1 and self.secs - self.scale_zero_info[-1][-1] > 2:
                self.scale_zero_info.append(
                    [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                     self.secs])
            elif len(self.scale_zero_info) == 2 and self.secs - self.scale_zero_info[-1][-1] > 3:
                self.scale_zero_info.append(
                    [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                     self.secs])
            elif len(self.scale_zero_info) == 3 and self.secs - self.scale_zero_info[-1][-1] > 4:
                self.scale_zero_info.pop(0)
                self.scale_zero_info.append(
                    [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                     self.secs])
        else:
            if len(self.scale_zero_info) == 1:
                self.assignScore(*self.scale_zero_info[0][:6])
            else:
                self.assignScore(*self.scale_zero_info[1][:6])
            del self.scale_zero_info

    # 称量物块
    def weight_block(self, score_index, blocks_top, blocks_front, salvers_top, scales_top, salvers_front, scales_front,
                     hands_top, hands_front):
        salver_top_box = self.salver_box(salvers_top, scales_top)
        salver_front_box = self.salver_box(salvers_front, scales_front, 'front')
        if salver_front_box is not None and blocks_front.shape[0] > 0:  # 前视 物块 托盘 手
            block_front_box = blocks_front[0][:4]
            if iou(block_front_box, salver_front_box) > 0 and \
                    abs(center_distance_h(block_front_box, salver_front_box)) < self.h_front * 0.052:  # 水平方向中心距离
                hand_salver = False  # 手和托盘是否有交集
                if hands_top.shape[0] > 0 and salvers_top.shape[0] > 0:
                    salver_top_box = salvers_top[0][:4]
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if iou(hand_top_box, salver_top_box) > 0:
                            hand_salver = True
                            break
                if hand_salver and hands_front.shape[0] > 0:  # 顶视手和托盘有交集 判断前视
                    hand_front_salver = False  # 前视手和托盘是否交集
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, salver_front_box) > 0:
                            hand_front_salver = True
                            break
                    if not hand_front_salver:  # 前视没有交集
                        hand_salver = False
                if not hand_salver:  # 手和托盘没有交集
                    self.weight_secs, self.weight_secs_pre, flag = self.duration(self.weight_secs, 1,
                                                                                 self.weight_secs_pre, 0.5)
                    if flag:
                        self.start_weight = True
                        self.update_weight(score_index)
                    return
        elif salver_top_box is not None and blocks_top.shape[0] > 0:  # 顶视
            block_top_box = blocks_top[0][:4]
            if iou(block_top_box, salver_top_box) == box_area(block_top_box):  # 物块在托盘中
                hand_salver = False  # 手和托盘是否有交集
                if hands_top.shape[0] > 0:
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if iou(hand_top_box, salver_top_box) > 0:
                            hand_salver = True
                            break
                if hand_salver and hands_front.shape[0] > 0 and salvers_front.shape[0] > 0:  # 顶视有交集 判断前视
                    hand_front_salver = False  # 前视手和托盘是否交集
                    salver_front_box = salvers_front[0][:4]
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, salver_front_box) > 0:
                            hand_front_salver = True
                            break
                    if not hand_front_salver:  # 前视没有交集
                        hand_salver = False
                if not hand_salver:  # 手和托盘没有交集
                    self.weight_secs, self.weight_secs_pre, flag = self.duration(self.weight_secs, 1,
                                                                                 self.weight_secs_pre, 0.5)
                    if flag:
                        self.update_weight(score_index)
                    return
        # if self.weight_info:
        #     print(self.num_frame_front, self.secs - self.weight_info[-1][-1])
        if self.weight_info and self.secs - self.weight_info[-1][-1] > 1:  # 停止称量1秒
            if len(self.weight_info) == 1:
                return self.weight_info[0][:6]
            else:
                return self.weight_info[1][:6]

    def update_weight(self, score_index):  # 更新称重数据信息
        if not self.weight_info:
            self.weight_info.append([score_index, self.frame_front, self.time_front, self.objects_front,
                                     self.preds_front, self.num_frame_front, self.secs, self.secs])
        elif len(self.weight_info) == 1 and self.secs - self.weight_info[-1][-2] > 2:
            self.weight_info.append([score_index, self.frame_front, self.time_front, self.objects_front,
                                     self.preds_front, self.num_frame_front, self.secs, self.secs])
        elif len(self.weight_info) == 2 and self.secs - self.weight_info[-1][-2] > 4:
            self.weight_info.append([score_index, self.frame_front, self.time_front, self.objects_front,
                                     self.preds_front, self.num_frame_front, self.secs, self.secs])
        elif len(self.weight_info) == 3 and self.secs - self.weight_info[-1][-2] > 6:
            self.weight_info.pop(0)
            self.weight_info.append([score_index, self.frame_front, self.time_front, self.objects_front,
                                     self.preds_front, self.num_frame_front, self.secs, self.secs])
        else:
            self.weight_info[-1][-1] = self.secs  # 更新最后的时间

    # 加入水
    def add_water(self, score_index, water_columns_front, beakers_front, measuring_cylinders_front):
        if water_columns_front.shape[0] > 0 and \
                water_columns_front[0][3] - water_columns_front[0][1] > self.h_front * 0.06:
            water_column_front_box = water_columns_front[0][:4]
            if pt_in_polygon(center_point(water_column_front_box), self.center_area_front):
                beaker_measuring_cylinder = True  # 烧杯量筒倒水
                if beakers_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0:
                    beaker_front_box = beakers_front[0][:4]
                    measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                    if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
                            iou(beaker_front_box, measuring_cylinder_front_box) > 0:  # 烧杯中心在量筒上方 烧杯与量筒有交集
                        beaker_measuring_cylinder = False
                        self.record_add_water_info(score_index, water_column_front_box, True)
                if beaker_measuring_cylinder:
                    self.water_column_secs, self.water_column_secs_pre, flag = self.duration(self.water_column_secs, 3,
                                                                                             self.water_column_secs_pre,
                                                                                             1.5)
                    if flag:
                        self.record_add_water_info(score_index, water_column_front_box)

            if self.add_water_beaker_info:
                if self.secs - self.add_water_beaker_info[-1] > 0.5:
                    return self.add_water_beaker_info[:6]

            elif self.add_water_info:
                if self.secs - self.add_water_info[-1] > 0.5:
                    return self.add_water_info[:6]

    # 记录示数
    def record_V_display(self, measuring_cylinders_front, water_columns_front, heads_front, eyes_front, blocks_front):
        block_in_water = False
        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0:
            water_column_front_box = water_columns_front[0][:4]
            if blocks_front.shape[0] > 0:
                block_front_box = blocks_front[0][:4]  # 物块
                if (iou(water_column_front_box, block_front_box) >= box_area(block_front_box) * 0.8
                        and block_front_box[1] - water_column_front_box[1] > self.h_front * 0.028):  # 物块在水里
                    block_in_water = True
            if not block_in_water:  # 物块不在水中
                self.see_display(eyes_front, heads_front, water_column_front_box)
            else:
                self.see_display(eyes_front, heads_front, water_column_front_box, True)

            if not self.scorePoint5:
                if self.see_display_info and self.secs - self.see_display_info[-1] > 1:
                    self.assignScore(*self.see_display_info[:6])
                elif self.see_display_head_info and self.secs - self.see_display_head_info[-1] > 1:
                    self.assignScore(*self.see_display_head_info[:6])
            if not self.scorePoint7:
                if self.see_display_block_info and self.secs - self.see_display_block_info[-1] > 1:
                    self.assignScore(*self.see_display_block_info[:6])
                elif self.see_display_block_head_info and self.secs - self.see_display_block_head_info[-1] > 1:
                    self.assignScore(*self.see_display_block_head_info[:6])

    # 读示数
    def see_display(self, eyes_front, heads_front, water_column_front_box, block=False):  # 看示数
        water_column_center_point_up = (
            (water_column_front_box[0] + water_column_front_box[2]) / 2, water_column_front_box[1])  # 水柱页面中心
        if eyes_front.shape[0] > 0:  # 眼睛
            eyes_front_box = []
            for eye_front in eyes_front:
                eye_front_box = eye_front[:4]
                if distance_point(center_point(eye_front_box), water_column_center_point_up) < self.h_front * 0.185:
                    eyes_front_box.append(eye_front_box)

            if len(eyes_front_box) == 0:
                return
            elif len(eyes_front_box) == 1:
                eye_center_h = center_point(eyes_front_box[0])[1]  # 眼睛中心高度
            elif len(eyes_front_box) == 2:
                eye_center_h = (center_point(eyes_front_box[0])[1] + center_point(eyes_front_box[1])[1]) / 2
            else:
                return
            dis_eye_water = abs(eye_center_h - water_column_front_box[1])
            if dis_eye_water < self.h_front * 0.135:
                if not block:
                    self.see_display_secs, self.see_display_secs_pre, flag = self.duration(self.see_display_secs,
                                                                                           0.4,
                                                                                           self.see_display_secs_pre,
                                                                                           0.3)
                    if flag:
                        if not self.see_display_info or dis_eye_water < self.see_display_info[-2]:
                            self.see_display_info = [5, self.frame_front, self.time_front, self.objects_front,
                                                     self.preds_front, self.num_frame_front, dis_eye_water, self.secs]
                        else:
                            self.see_display_info[-1] = self.secs
                else:
                    self.see_display_block_secs, self.see_display_block_secs_pre, flag = self.duration(
                        self.see_display_block_secs, 0.4, self.see_display_block_secs_pre, 0.3)
                    if flag:
                        if not self.see_display_block_info or dis_eye_water < self.see_display_block_info[-2]:
                            self.see_display_block_info = [7, self.frame_front, self.time_front, self.objects_front,
                                                           self.preds_front, self.num_frame_front, dis_eye_water,
                                                           self.secs]
                        else:
                            self.see_display_block_info[-1] = self.secs
                return
        if heads_front.shape[0] > 0:  # 只检测出头
            heads_front_box = []
            dis_head_water = 0
            for head_front in heads_front:
                head_front_box = head_front[:4]
                dis_head_water = distance_point(center_point(head_front_box), water_column_center_point_up)
                if dis_head_water < self.h_front * 0.185:
                    heads_front_box.append(head_front_box)
            if len(heads_front_box) == 1:
                if not block:
                    self.see_display_secs, self.see_display_secs_pre, flag = self.duration(self.see_display_secs,
                                                                                           0.4,
                                                                                           self.see_display_secs_pre,
                                                                                           0.3)
                    if flag:
                        if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                            self.see_display_head_info = [5, self.frame_front, self.time_front, self.objects_front,
                                                          self.preds_front, self.num_frame_front, dis_head_water,
                                                          self.secs]
                        else:
                            self.see_display_head_info[-1] = self.secs
                else:
                    self.see_display_block_secs, self.see_display_block_secs_pre, flag = self.duration(
                        self.see_display_block_secs, 0.4, self.see_display_block_secs_pre, 0.3)
                    if flag:
                        if not self.see_display_block_head_info or \
                                dis_head_water < self.see_display_block_head_info[-2]:
                            self.see_display_block_head_info = [7, self.frame_front, self.time_front,
                                                                self.objects_front, self.preds_front,
                                                                self.num_frame_front, dis_head_water, self.secs]
                        else:
                            self.see_display_block_head_info[-1] = self.secs

    # 物块放在水中
    def block_in_water(self, score_index, measuring_cylinders_front, measuring_cylinders_top, water_columns_front,
                       blocks_front,
                       blocks_top):
        if blocks_top.shape[0] > 0:  # 顶部 物块不在水里直接返回
            block_cylinder = False
            block_top_box = blocks_top[0][:4]
            if measuring_cylinders_top.shape[0] > 0:
                measuring_cylinder_top = measuring_cylinders_top[0][:4]
                if iou(block_top_box, measuring_cylinder_top) > 0:
                    block_cylinder = True
            if not block_cylinder:
                return

        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0 and blocks_front.shape[
            0] > 0:  # 量筒 水柱 物块
            water_column_front_box = water_columns_front[0][:4]  # 水柱
            block_front_box = blocks_front[0][:4]  # 物块
            if pt_in_polygon(center_point(water_column_front_box), self.center_area_front):  # 限制范围
                if iou(water_column_front_box, block_front_box) >= box_area(block_front_box) * 0.8 and \
                        block_front_box[1] - water_column_front_box[1] > self.h_front * 0.028:  # 物块在水里
                    self.block_in_water_secs, self.block_in_water_secs_pre, flag = self.duration(
                        self.block_in_water_secs, 1, self.block_in_water_secs_pre, 0.5)
                    if flag:
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    # 清理桌面
    def clearn_desk(self, score_index, top_items, front_items):
        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_secs, _, flag = self.duration(self.clearn_secs, 2)
            if flag:
                self.clearn_secs = 0
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top
        else:
            self.clearn_secs = 0

    # 记录向量筒中添加水的信息
    def record_add_water_info(self, score_index, box, beaker=False):
        y = box[3] - box[1]
        if beaker:
            if not self.add_water_beaker_info or y > self.add_water_beaker_info[-2]:
                self.add_water_beaker_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                              self.preds_front, self.num_frame_front, y, self.secs]
            else:
                self.add_water_beaker_info[-1] = self.secs
        else:
            if not self.add_water_info or self.add_water_info[-2] < y:
                self.add_water_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                       self.preds_front, self.num_frame_front, y, self.secs]

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info[:6])
            return True

    def salver_box(self, salvers, scales, view='top'):  # 由托盘天平、托盘 得出 托盘天平托盘 box 防止只检测出天平的情况
        ratio = (0.08, 0.3) if view == 'top' else (0.09, 0.5)
        w = self.w_top if view == 'top' else self.w_front
        if salvers.shape[0] > 0:  # 称量盘
            return salvers[0][:4]
        elif scales.shape[0] > 0:  # 整个天平
            salver_box = scales[0][:4]
            x = (salver_box[2] - salver_box[0]) * ratio[0]
            y = (salver_box[3] - salver_box[1]) * ratio[1]
            dis_h_r = (center_point(salver_box)[0] / w - 0.5) / 0.5
            salver_box[0] += x * (1 + dis_h_r)
            if view == 'top':
                salver_box[1] += x * 0.5
            salver_box[2] -= x * (1 - dis_h_r)
            salver_box[3] -= y
            return salver_box
            # if view=='top':
            #     cv2.rectangle(self.frame_top, (int(salver_box[0]), int(salver_box[1])), (int(salver_box[2]), int(salver_box[3])), (255, 0, 0), -1, cv2.LINE_AA)
            # else:
            #     cv2.rectangle(self.frame_front, (int(salver_box[0]), int(salver_box[1])), (int(salver_box[2]), int(salver_box[3])), (255, 0, 0), -1, cv2.LINE_AA)
