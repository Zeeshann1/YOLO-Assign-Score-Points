#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 14:34
# @Author  : Qiguangnan
# @File    : phy_relationship_M_V_01_cou.py.py

'''
探究物质质量和体积的关系(电子天平&橡皮块)
'''

from .comm import *


class PHY_relationship_M_V_01(ConfigModel):

    def __init__(self):
        super(PHY_relationship_M_V_01, self).__init__()
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
        self.scorePoint10 = False

        self.num = 4  # 总称量次数
        self.eraser_num = 0  # 橡皮数量
        self.weight_num = 0  # 称重次数
        self.measure_v_num = 0  # 量体积次数

        self.block_notin_water = True
        self.block_in_water = False  # 物块是否在水中
        self.block_in_water_n = 0  # 物块在水中 次数

        self.scale_on_time = 0.
        self.scale_on_time_pre = 0.
        self.open_scale_time = 0.  # 打开天平的时间
        self.scale_zero_time = 0.
        self.scale_zero_info = []
        self.start_weight = False
        self.reset()

    def post_assign(self, index, img, time_frame, object, preds, num_frame, conf, name_save, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def reset(self):
        self.weight_time = 0.
        self.weight_time_pre = 0.
        self.weight_info = []  # 记录称量信息
        self.water_column_time = 0.  # 添加水
        self.water_column_time_pre = 0.
        self.add_water_beaker_info = []  # 用烧杯向量筒加水信息
        self.add_water_info = []
        self.see_display_time = 0.
        self.see_display_time_pre = 0.
        self.see_display_info = []  # 读示数
        self.see_display_head_info = []  # 读示数（只有头）
        self.block_notin_water_time = 0.
        self.block_notin_water_time_pre = 0.
        self.block_in_water_time = 0.
        self.block_in_water_time_pre = 0.
        self.clearn_time = 0.
        self.clearn_desk_info = []  # 整理桌面信息

    def score_process(self, *args):  # 赋分逻辑部分
        hands_top, eyes_top, heads_top, dusters_top, scales_top, salvers_top, scale_ons_top, scale_zeros_top, \
        scale_offs_top, scale_notzeros_top, erasers_top, cylinders_top, cylinder_bs_top, column_ws_top, liquids_top, \
        beakers_top = self.preds_top

        hands_front, eyes_front, heads_front, dusters_front, scales_front, salvers_front, salver_ons_front, \
        salver_zeros_front, salver_offs_front, salver_notzeros_front, erasers_front, cylinders_front, \
        cylinder_bs_front, column_ws_front, liquids_front, beakers_front = self.preds_front

        if max(erasers_top.shape[0], erasers_front.shape[0]) > self.eraser_num:
            self.eraser_num = int(max(erasers_top.shape[0], erasers_front.shape[0]))

        block_in_water = self.blockInWater(cylinders_front, column_ws_front, erasers_front)  # 物块是否在水中
        if self.block_in_water != block_in_water:
            if block_in_water:
                self.block_in_water_n += 1
            self.block_in_water = block_in_water

        # 1.打开电子天平, 清零
        if not self.scorePoint1:
            if not self.open_scale_time:
                self.open_scale(scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_notzeros_top)
            else:
                info = self.set_zeron(1, scale_zeros_top, scales_top)
                if info is not None:
                    self.assignScore(*info)

        # 2.将橡皮置于电子天平中央，记录电子天平示数
        if not self.scorePoint2:
            info = self.weight_block(2, erasers_top, erasers_front, salvers_top, salvers_front, hands_top, hands_front)
            if info is not None:
                self.assignScore(*info)
                self.weight_num += 1  # 称量次数 +1
                self.reset()

        # 3.在量筒中倒入适量的水
        # 量筒中有水， 前视
        if not self.scorePoint3:
            info = self.add_water(3, column_ws_front, beakers_front, cylinders_front)
            if info is not None:
                self.assignScore(*info[:6])

        # 4 观察并记录量筒中水面对应的示数
        if not self.scorePoint4 and not self.block_in_water:
            info = self.record_V_display(4, column_ws_front, heads_front, eyes_front)
            if info is not None:
                self.assignScore(*info)
                self.reset()

        # 5 将系有细线的橡皮慢慢放入量筒并浸没在水中
        # 前视
        if not self.scorePoint5 and self.block_in_water:
            self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

        # 6 观察并记录量筒中水面对应的示数（有橡皮）
        if not self.scorePoint6 and self.scorePoint5 and self.block_in_water:
            info = self.record_V_display(6, column_ws_front, heads_front, eyes_front)
            if info is not None:
                self.assignScore(*info)
                self.measure_v_num += 1
                self.reset()

        # 7 8 9 再测量3 组
        if self.scorePoint2 and self.weight_num < self.num:
            info = self.weight_block(erasers_top, erasers_front, salvers_top, salvers_front, hands_top, hands_front)
            if info is not None:
                if self.weight_num < self.measure_v_num:
                    self.assignScore(*info)
                if self.weight_num < self.eraser_num:
                    self.weight_num += 1  # 称量次数 +1
                self.reset()

        # 7 8 9 再测量3 组
        if self.scorePoint6 and self.block_in_water and self.measure_v_num < self.num and self.measure_v_num < self.block_in_water_n:
            info = self.record_V_display(6 + self.measure_v_num, column_ws_front, heads_front, eyes_front)
            if info is not None:
                if self.measure_v_num < self.weight_num:
                    self.assignScore(*info)
                if self.measure_v_num < self.eraser_num:
                    self.measure_v_num += 1  # 测量体积次数 +1
                self.reset()

        # 10 整理实验器材
        top_items = [scales_top, cylinders_top, beakers_top, erasers_top, dusters_top]
        front_items = [scales_front, cylinders_front, beakers_front, erasers_front, dusters_front]
        if not self.scorePoint10 and \
                scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[0] == 0 \
                and (self.scorePoint3 or self.scorePoint5 or self.scorePoint6):
            self.clearn_desk(10, top_items, front_items)
        if self.scorePoint10 and len(self.score_list) != 10:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(10)

    # 物块放在水中
    def blockInWater(self, cylinders_front, column_ts_front, blocks_front):
        if cylinders_front.shape[0] > 0 and column_ts_front.shape[0] > 0 and blocks_front.shape[0] > 0:  # 量筒水柱物块
            column_t_front_box = column_ts_front[0][:4]  # 水柱
            if pt_in_polygon(center_point(column_t_front_box), self.center_area_front):  # 限制范围
                block_boxes = []
                for block_front in blocks_front:
                    block_front_box = block_front[:4]
                    if iou(column_t_front_box, block_front_box) >= box_area(block_front_box) * 0.8 and \
                            block_front_box[1] - column_t_front_box[1] > self.h_front * 0.015:  # 物块在水里
                        block_boxes.append(block_front_box)
                if len(block_boxes) == 1:
                    self.block_in_water_time, self.block_in_water_time_pre, flag = self.duration(
                        self.block_in_water_time, 1.5, self.block_in_water_time_pre, 0.5)
                    if flag:
                        return True
                    elif self.block_in_water:
                        return not self.secs - self.block_in_water_time_pre > 2
                    else:
                        return False
                elif self.block_in_water:
                    return not self.secs - self.block_in_water_time_pre > 2
                else:
                    return False
            elif self.block_in_water:
                return not self.secs - self.block_in_water_time_pre > 2
            else:
                return False
        elif self.block_in_water:
            return not self.secs - self.block_in_water_time_pre > 2
        else:
            return False

    # 打开天平
    def open_scale(self, scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_notzeros_top):
        if scales_top.shape[0] > 0:
            scale_top_box = scales_top[0][:4]
            if (pt_in_polygon(center_point(scale_top_box), self.center_area_top)
                    and scale_offs_top.shape[0] == 0
                    and (scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[0] != 0)):  # 天平打开
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
                    self.scale_on_time, self.scale_on_time_pre, flag = self.duration(self.scale_on_time, 3,
                                                                                     self.scale_on_time_pre, 1)
                    if flag:
                        self.open_scale_time = self.secs

    # 天平置零
    def set_zeron(self, score_index, scale_zeros_top, scales_top):
        if scale_zeros_top.shape[0] > 0 and scales_top.shape[0] > 0:  # 显示0.0
            scale_top_box = scales_top[0][:4]
            scale_zero_top_box = scale_zeros_top[0][:4]
            if box1_in_box2(scale_zero_top_box, scale_top_box):
                if self.secs - self.open_scale_time > 0.5:
                    self.scale_zero_time, _, flag = self.duration(self.scale_zero_time, 0.3)
                    if flag:
                        return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top

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
                return self.scale_zero_info[0][:6]
            else:
                return self.scale_zero_info[1][:6]

    # 称量物块
    def weight_block(self, score_index, blocks_top, blocks_front, salvers_top, salvers_front, hands_top, hands_front):
        if blocks_front.shape[0] > 0 and salvers_front.shape[0] > 0:  # 前视 物块 托盘 手
            salver_front_box = salvers_front[0][:4]
            for block_front in blocks_front:
                block_front_box = block_front[:4]
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
                        self.weight_time, self.weight_time_pre, flag = self.duration(self.weight_time, 1,
                                                                                     self.weight_time_pre, 0.5)
                        if flag:
                            self.start_weight = True
                            self.update_weight(score_index)
                        return
        elif blocks_top.shape[0] > 0 and salvers_top.shape[0] > 0:  # 顶视
            salver_top_box = salvers_top[0][:4]
            for block_top in blocks_top:
                block_top_box = block_top[:4]
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
                        self.weight_time, self.weight_time_pre, flag = self.duration(self.weight_time, 1,
                                                                                     self.weight_time_pre, 0.5)
                        if flag:
                            self.update_weight(score_index)
                        return
        if self.weight_info and self.secs - self.weight_info[-1][-1] > 1:  # 停止称量1秒
            if len(self.weight_info) == 1:
                return self.weight_info[0][:6]
            else:
                return self.weight_info[1][:6]

    def update_weight(self, score_index):  # 更新称重数据信息
        if not self.weight_info:
            self.weight_info.append(
                [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                 self.secs, self.secs])
        elif len(self.weight_info) == 1 and self.secs - self.weight_info[-1][-2] > 2:
            self.weight_info.append(
                [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                 self.secs, self.secs])
        elif len(self.weight_info) == 2 and self.secs - self.weight_info[-1][-2] > 4:
            self.weight_info.append(
                [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                 self.secs, self.secs])
        elif len(self.weight_info) == 3 and self.secs - self.weight_info[-1][-2] > 6:
            self.weight_info.pop(0)
            self.weight_info.append(
                [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top,
                 self.secs, self.secs])
        else:
            self.weight_info[-1][-1] = self.secs  # 更新最后的时间

    # 加入水
    def add_water(self, score_index, water_columns_front, beakers_front, cylinders_front):
        if water_columns_front.shape[0] > 0 and \
                water_columns_front[0][3] - water_columns_front[0][1] > self.h_front * 0.06:
            water_column_front_box = water_columns_front[0][:4]
            if pt_in_polygon(center_point(water_column_front_box), self.center_area_front):
                beaker_measuring_cylinder = True  # 烧杯量筒倒水
                if beakers_front.shape[0] > 0 and cylinders_front.shape[0] > 0:
                    beaker_front_box = beakers_front[0][:4]
                    measuring_cylinder_front_box = cylinders_front[0][:4]
                    if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
                            iou(beaker_front_box, measuring_cylinder_front_box) > 0:  # 烧杯中心在量筒上方 烧杯与量筒有交集
                        beaker_measuring_cylinder = False
                        self.record_add_water_info(score_index, water_column_front_box, True)
                if beaker_measuring_cylinder:
                    self.water_column_time, self.water_column_time_pre, flag = self.duration(self.water_column_time, 3,
                                                                                             self.water_column_time_pre,
                                                                                             0.2)
                    if flag:
                        self.record_add_water_info(score_index, water_column_front_box)
            if self.add_water_beaker_info:
                if self.secs - self.add_water_beaker_info[-1] > 0.5:
                    return self.add_water_beaker_info
            elif self.add_water_info:
                if self.secs - self.add_water_info[-1] > 0.5:
                    return self.add_water_info[:6]

    # 记录示数
    def record_V_display(self, score_index, column_ts_front, heads_front, eyes_front):
        if column_ts_front.shape[0] == 0:
            return
        column_t_front_box = column_ts_front[0][:4]
        self.see_display(score_index, eyes_front, heads_front, column_t_front_box)
        if self.see_display_info and self.secs - self.see_display_info[-1] > 1:
            return self.see_display_info[:6]
        elif self.see_display_head_info and self.secs - self.see_display_head_info[-1] > 1:
            return self.see_display_head_info[:6]

    # 读示数
    def see_display(self, score_index, eyes_front, heads_front, column_t_front_box):  # 看示数
        water_column_center_point_up = (
            (column_t_front_box[0] + column_t_front_box[2]) / 2, column_t_front_box[1])  # 水柱液面中心
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
            dis_eye_water = abs(eye_center_h - column_t_front_box[1])
            if dis_eye_water < self.h_front * 0.135:
                self.see_display_time, self.see_display_time_pre, flag = self.duration(self.see_display_time,
                                                                                       0.4,
                                                                                       self.see_display_time_pre,
                                                                                       0.3)
                if flag:
                    if not self.see_display_info or dis_eye_water < self.see_display_info[-2]:
                        self.see_display_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                 self.preds_front, self.num_frame_front, dis_eye_water, self.secs]
                    else:
                        self.see_display_info[-1] = self.secs
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
                self.see_display_time, self.see_display_time_pre, flag = self.duration(self.see_display_time,
                                                                                       0.4,
                                                                                       self.see_display_time_pre,
                                                                                       0.3)
                if flag:
                    if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                        self.see_display_head_info = [score_index, self.frame_front, self.time_front,
                                                      self.objects_front, self.preds_front, self.num_frame_front,
                                                      dis_head_water, self.secs]
                    else:
                        self.see_display_head_info[-1] = self.secs

    # 清理桌面
    def clearn_desk(self, score_index, top_items, front_items):
        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
            if flag:
                self.clearn_time = 0
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top
        else:
            self.clearn_time = 0

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
            if not self.add_water_info or self.add_water_info[4] < y:
                self.add_water_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                       self.preds_front, self.num_frame_front, y, self.secs]

    def end(self):  # 实验结束时判断是否整理桌面，如果有则进行赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info[:6])
            return True
