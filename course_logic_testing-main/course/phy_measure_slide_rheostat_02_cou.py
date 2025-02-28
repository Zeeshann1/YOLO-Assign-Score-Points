#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : Qinhe
# @File    : phy_measure_slide_rheostat_02_cou.py
# 中考赋分


import random
from .comm import *
from .comm.course_base import ConfigModel


# from config.phy_measure_ammeter_conf import PYDLBCDL01
# from utilsg.litF import uploaded_images, encode_image_jpg, upload_redis_or_save_json_local, ts2ft
# from configg.global_config import SCORE_ROOT_PATH
# from .comm import Plot
# from logger import logger

import copy

class PHY_measure_slide_rheostat_02(ConfigModel):

    def __init__(self):
        super(PHY_measure_slide_rheostat_02, self).__init__()

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
        self.scorePoint11 = False
        self.scorePoint12 = False
        self.scorePoint13 = False

        self.experiment_ing = False  # 正在做实验  判断拆除器材
        self.experiment_end = 0  # 器材完成拆除事件计数
        self.first_end = False  # 一次完整的实验

        self.flag1_inertance_top = 0
        self.flag1_inertance_side = 0
        self.flag1_inertance_front = 0
        self.flag2_inertance_top = 0
        self.flag2_inertance_side = 0
        self.flag3_inertance_top = 0
        self.flag3_inertance_side = 0
        self.flag4_min = 0
        self.flag4_max = 0
        self.flag4_range = ''
        self.flag4_inertance_min = 0
        self.flag4_inertance_max = 0
        self.flag56789_equipment_increase = []  # 已连接的器材逐渐增加  针对连接了的器材
        self.flag5_inertance = 0
        self.flag6_inertance = 0
        self.flag7_inertance_top = 0
        self.flag7_inertance_side = 0
        self.flag7_inertance_front = 0
        self.flag8_on_top = 0
        self.flag8_top_dt = 0
        self.flag8_inertance_top = 0
        self.flag8_inertance_side = 0
        self.flag8_inertance_front = 0
        self.flag9_on_top = 0
        self.flag9_inertance_top = 0
        self.flag9_inertance_side = 0
        self.flag10_inertance_top = 0

        self.class_name = ['power_source_top', 'binding_post_red_top', 'binding_post_black_top',
                           'wire_connection_red_top', 'wire_connection_black_top', 'wire_connection_binding_post_top',
                           'switch_off_top', 'switch_on_top',
                           'slide_rheostat_top', 'gleithretter_top',
                           'above_top', 'following_top', 'connect_above_top', 'connect_following_top',
                           'ammeter_top', 'min_red_top', 'max_red_top', 'pointer_offset_top', 'pointer_zero_top',
                           'voltmeter_top', 'light_top', 'non_top', 'dim_top', 'bright_top', 'fixed_resistor_top',
                           'clean_desk_top', 'wire_connection_top']

    def score_process(self, top_true, front_true, side_true):
        if top_true or front_true or side_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分
            # [top_preds, side_preds, front1_preds], [top_img0, side_img0, front_img0] = preds, img0s # 检测框和ing

            if top_true:
                power_source_top, binding_post_red_top, binding_post_black_top, \
                wire_connection_red_top, wire_connection_black_top, wire_connection_binding_post_top, \
                switch_off_top, switch_on_top, \
                slide_rheostat_top, gleithretter_top, \
                above_top, following_top, connect_above_top, connect_following_top, \
                ammeter_top, min_1_top, max_1_top, pointer_offset_top, pointer_zero_top, \
                voltmeter_top, light_top, non_top, dim_top, bright_top, fixed_resistor_top, \
                clean_desk_top, wire_connection_top = self.preds_top

                # 确定图片正反
                if not self.set_center_box and power_source_top.shape[0] != 0:
                    h, w = self.frame_top.shape[:2]
                    # 根据最开始器材在图片的位置确定操作区域
                    center_box_upright = torch.tensor([w * 0.33, h * 0.45, w * 0.72, h * 0.87], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
                    center_box_upend = torch.tensor([w * 0.28, h * 0.13, w * 0.67, h * 0.55], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面

                    binding_post = center_point(power_source_top[0][0:4])
                    self.center_box = center_box_upend if binding_post[1] > (h / 2) else center_box_upright
                    self.set_center_box = True

                switch_top = torch.cat([switch_off_top, switch_on_top], dim=0)
                if switch_top.shape[0] != 0:
                    switch_top = switch_top[torch.argsort(-switch_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                pointer_top = torch.cat([pointer_offset_top, pointer_zero_top], dim=0)
                if pointer_top.shape[0] != 0:
                    pointer_top = pointer_top[torch.argsort(-pointer_top[:, 4])]  # 置信度排序,指针取第一个  torch.sort(input, dim=0)按列排序

                range_top = torch.cat([min_1_top, max_1_top], dim=0)
                if range_top.shape[0] != 0:
                    range_top = range_top[torch.argsort(-range_top[:, 4])]  # 置信度排序,量程取第一个

                wire_post_top = torch.cat([wire_connection_red_top, wire_connection_black_top, wire_connection_binding_post_top, min_1_top, max_1_top, connect_above_top, connect_following_top], dim=0)

            if side_true:
                power_source_side, binding_post_red_side, binding_post_black_side, \
                wire_connection_red_side, wire_connection_black_side, wire_connection_binding_post_side, \
                switch_off_side, switch_on_side, \
                slide_rheostat_side, gleithretter_side, \
                above_side, following_side, connect_above_side, connect_following_side, \
                ammeter_side, min_1_side, max_1_side, pointer_offset_side, pointer_zero_side, \
                voltmeter_side, light_side, non_side, dim_side, bright_side, fixed_resistor_side, \
                clean_desk_side, wire_connection_side = self.preds_side

                switch_side = torch.cat([switch_off_side, switch_on_side], dim=0)
                if switch_side.shape[0] != 0:
                    switch_side = switch_side[torch.argsort(-switch_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                pointer_side = torch.cat([pointer_offset_side, pointer_zero_side], dim=0)
                if pointer_side.shape[0] != 0:
                    pointer_side = pointer_side[torch.argsort(-pointer_side[:, 4])]  # 置信度排序,指针取第一个  torch.sort(input, dim=0)按列排序

            if front_true:
                power_source_front, binding_post_red_front, binding_post_black_front, \
                wire_connection_red_front, wire_connection_black_front, wire_connection_binding_post_front, \
                switch_off_front, switch_on_front, \
                slide_rheostat_front, gleithretter_front, \
                above_front, following_front, connect_above_front, connect_following_front, \
                ammeter_front, min_1_front, max_1_front, pointer_offset_front, pointer_zero_front, \
                voltmeter_front, light_front, non_front, dim_front, bright_front, fixed_resistor_front, \
                clean_desk_front, wire_connection_front = self.preds_front

            if top_true:
                # 判断与导线连接的器材
                this_frame_terminals = self.all_estimate_picture(wire_post_top, power_source_top, switch_top, ammeter_top, slide_rheostat_top)
                # 判断是否已经完成一次实验操作
                # self.all_estimate_experiment_ing(wire_post_top)  # todo 重置self.的变量

            # 1.电路连接时开关处于断开状态
            if not self.scorePoint1 and top_true and "1" in self.exper_score_ids:
                point1view = self.point1_switch_off(switch_off_top, wire_connection_top, wire_post_top, switch_top,
                                                    switch_off_side, switch_off_front, side_true, front_true)
                if point1view[0]:
                    self.scorePoint1 = True
                    conf_c = 0.1
                    if point1view[1] == 'top':
                        self.assignScore(index=1,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="1.jpg",
                                         preds=self.preds_top
                                         )
                    elif point1view[1] == 'side':
                        self.assignScore(index=1,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="1.jpg",
                                         preds=self.preds_side
                                         )
                    elif point1view[1] == 'front':
                        self.assignScore(index=1,
                                         img=self.frame_front,
                                         object=self.objects_front,
                                         conf=conf_c,
                                         time_frame=self.time_front,
                                         num_frame=self.num_frame_front,
                                         name_save="1.jpg",
                                         preds=self.preds_front
                                         )

            # 2.滑动变阻器连接一上一下两个接线柱
            # 发生在开关闭合之前，
            # 接入正确
            if not self.scorePoint2 and "2" in self.exper_score_ids and wire_post_top.shape[0] >= 2:  # 接线柱大于2个
                point2view = self.point2_r_right(connect_above_top, connect_following_top,
                                                 connect_above_side, connect_following_side,
                                                 top_true, side_true)
                if point2view[0]:
                    self.scorePoint2 = True
                    conf_c = 0.1
                    if point2view[1] == 'top':
                        self.assignScore(index=2,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="2.jpg",
                                         preds=self.preds_top
                                         )
                    elif point2view[1] == 'side':
                        self.assignScore(index=2,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="2.jpg",
                                         preds=self.preds_side
                                         )

            # 3.滑动变阻器电阻最大
            # 发生在开关闭合之前，
            # 电阻最大由滑片到following和connect_following的距离判断（顶视或侧视或前视）
            # 接入正确
            if not self.scorePoint3 and "3" in self.exper_score_ids and wire_post_top.shape[0] >= 2:  # 接线柱大于2个
                point3view = self.point3_r_max(following_top, connect_following_top, gleithretter_top,
                                               following_side, connect_following_side, gleithretter_side,
                                               top_true, side_true)
                if point3view[0]:
                    self.scorePoint3 = True
                    conf_c = 0.1
                    if point3view[1] == 'top':
                        self.assignScore(index=3,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="3.jpg",
                                         preds=self.preds_top
                                         )
                    elif point3view[1] == 'side':
                        self.assignScore(index=3,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="3.jpg",
                                         preds=self.preds_side
                                         )

            # 4.电流表选择合适量程
            if not self.scorePoint4 and top_true and "4" in self.exper_score_ids and wire_post_top.shape[0] >= 2:  # 接线柱大于2个
                point4view = self.point4_range(power_source_top, range_top, ammeter_top)
                if point4view[0] and point4view[1] == 'top':
                    self.scorePoint4 = True
                    conf_c = 0.1
                    self.assignScore(index=4,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="4.jpg",
                                     preds=self.preds_top
                                     )

            # 5.电流表，电源正负极连接正确
            if not self.scorePoint5 and top_true and "5" in self.exper_score_ids and len(self.flag56789_equipment_increase) >= 1:  # 有1个器材被连接
                point5view = self.point5_polarity(this_frame_terminals)
                if point5view[0] and point5view[1] == 'top':
                    self.scorePoint5 = True
                    conf_c = 0.1
                    self.assignScore(index=5,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="5.jpg",
                                     preds=self.preds_top
                                     )

            # 6.电源，开关，滑动变阻器，电流表串联
            if not self.scorePoint6 and top_true and "6" in self.exper_score_ids and len(self.flag56789_equipment_increase) >= 3:  # 有3个器材被连接
                point6view = self.point6_serie(this_frame_terminals, slide_rheostat_top)
                if point6view[0] and point6view[1] == 'top':
                    self.scorePoint6 = True
                    conf_c = 0.1
                    self.assignScore(index=6,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="6.jpg",
                                     preds=self.preds_top
                                     )



            # 7.闭合开关，电压表指针发生偏转
            if not self.scorePoint7 and "7" in self.exper_score_ids and wire_post_top.shape[0] >= 5 and len(self.flag56789_equipment_increase) == 4:  # 有4个器材被连接，接线柱大于5个
                point7view = self.point7_point(pointer_top, switch_top, ammeter_top,
                                               pointer_side, switch_side, ammeter_side,
                                               top_true, side_true)
                if point7view[0]:
                    self.scorePoint7 = True
                    conf_c = 0.1
                    if point7view[1] == 'top':
                        self.assignScore(index=7,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="7.jpg",
                                         preds=self.preds_top
                                         )
                    elif point7view[1] == 'side':
                        self.assignScore(index=7,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="7.jpg",
                                         preds=self.preds_side
                                         )

            # 8.改变滑动变阻器电阻，观察电流表示数
            # 与滑动变阻器是否为Rmax无关，关键在于滑片位置的变化，使用相对平行的水平距离
            # 发生在闭合开关，但为断开开关中间
            if not self.scorePoint8 and "8" in self.exper_score_ids and len(self.flag56789_equipment_increase) == 4:  # 有4个器材被连接
                point8view = self.point8_gleithretter_site(top_true, side_true, front_true,
                                                           following_top, connect_following_top, gleithretter_top, pointer_offset_top,
                                                           slide_rheostat_side,  gleithretter_side,
                                                           slide_rheostat_front, gleithretter_front)
                if point8view[0]:
                    self.scorePoint8 = True
                    conf_c = 0.1
                    if point8view[1] == 'top':
                        self.assignScore(index=8,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="8.jpg",
                                         preds=self.preds_top
                                         )
                    elif point8view[1] == 'side':
                        self.assignScore(index=8,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="8.jpg",
                                         preds=self.preds_side
                                         )
                    elif point8view[1] == 'front':
                        self.assignScore(index=8,
                                         img=self.frame_front,
                                         object=self.objects_front,
                                         conf=conf_c,
                                         time_frame=self.time_front,
                                         num_frame=self.num_frame_front,
                                         name_save="8.jpg",
                                         preds=self.preds_front
                                         )

            # 9.断开开关后再拆电路
            # 优化：加入时序 如self.flag3
            if not self.scorePoint9 and "9" in self.exper_score_ids and wire_post_top.shape[0] >= 5 and len(self.flag56789_equipment_increase) >= 3:  # 有3个器材被连接，接线柱大于5个
                point9view = self.point9_switch_off(switch_top, pointer_top, ammeter_top,
                                                    pointer_side, switch_side, ammeter_side,
                                                    this_frame_terminals, top_true, side_true)
                if point9view[0]:
                    self.scorePoint9 = True
                    conf_c = 0.1
                    if point9view[1] == 'top':
                        self.assignScore(index=9,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="9.jpg",
                                         preds=self.preds_top
                                         )
                    elif point9view[1] == 'side':
                        self.assignScore(index=9,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="9.jpg",
                                         preds=self.preds_side
                                         )

            # 10.整理桌面
            if not self.scorePoint10 and "10" in self.exper_score_ids and len(self.flag56789_equipment_increase) >= 4:  # 有4个器材被连接
                point10view = self.point10_clean(power_source_top, switch_top, ammeter_top, slide_rheostat_top,gleithretter_top,
                                                 top_true, clean_desk_top, side_true, clean_desk_side, front_true, clean_desk_front)
                if point10view[0]:
                    self.scorePoint10 = True
                    conf_c = 0.1
                    if point10view[1] == 'top':
                        self.assignScore(index=10,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="10.jpg",
                                         preds=self.preds_top
                                         )
                    elif point10view[1] == 'side':
                        self.assignScore(index=10,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="10.jpg",
                                         preds=self.preds_side
                                         )
                    elif point10view[1] == 'front':
                        self.assignScore(index=10,
                                         img=self.frame_front,
                                         object=self.objects_front,
                                         conf=conf_c,
                                         time_frame=self.time_front,
                                         num_frame=self.num_frame_front,
                                         name_save="10.jpg",
                                         preds=self.preds_front
                                         )

    def all_estimate_picture(self, wire_post_top, power_source_top, switch_top, ammeter_top, slide_rheostat_top):  # 判断与导线连接的器材
        this_frame_terminals = []
        if wire_post_top.shape[0] >= 3 and (not self.scorePoint5 or not self.scorePoint6 or not self.scorePoint9):
            equipments = {power_source_top: ['power', 0], switch_top: ['switch', 0], ammeter_top: ['ammeter', 0], slide_rheostat_top: ['slide', 0]}
            if wire_post_top.shape[0] != 0:
                for post_top in wire_post_top:
                    post_top_box = post_top[0:4]
                    for equipment, equipment_mate in equipments.items():
                        if equipment.shape[0] != 0:
                            for equip in equipment:
                                equipment_box = equip[0:4]
                                if iou(post_top_box, equipment_box) > 0:
                                    equipment_mate[1] += 1
            for equipment, equipment_mate in equipments.items():
                if equipment_mate[1] >= 2:
                    this_frame_terminals.append(equipment_mate[0])
            self.flag56789_equipment_increase += list(set(this_frame_terminals).difference(set(self.flag56789_equipment_increase)))  # 添加基于flag13的差集  #  累计的器材连接情况
        return this_frame_terminals

    def all_estimate_experiment_ing(self, wire_post_top):  # 判断是否已经完成一次实验操作  考试版用接线柱辅助判断
        if len(wire_post_top) >= 4 and not self.experiment_ing and not self.first_end:  # 判断第一次实验开始连接器材
            self.experiment_ing = True  # 打开拆除器材的门

        elif len(wire_post_top) >= 4 and not self.experiment_ing and self.first_end:  # 判断再次实验开始连接器材
            self.experiment_ing = True  # 打开再次做实验的门
            self.first_end = False  # 将本次实验重置为第一次实验

            self.scorePoint1 = False  # TODO 待做  针对每一个得分点创建单独的函数  重置得分点状态，得分情况，得分点初始化
            self.retracementScore(index=1)
            self.scorePoint2 = False
            self.retracementScore(index=2)
            self.scorePoint3 = False
            self.retracementScore(index=3)
            self.scorePoint4 = False
            self.retracementScore(index=4)
            self.scorePoint5 = False
            self.retracementScore(index=5)
            self.scorePoint6 = False
            self.retracementScore(index=6)
            self.scorePoint7 = False
            self.retracementScore(index=7)
            self.scorePoint8 = False
            self.retracementScore(index=8)
            self.scorePoint9 = False
            self.retracementScore(index=9)
            self.scorePoint10 = False
            self.retracementScore(index=10)

        elif len(wire_post_top) == 0 and self.experiment_ing:  # 判断拆除器材   考虑
            self.experiment_end += 1
            if self.experiment_end > 100:
                self.experiment_ing = False
                self.first_end = True  # 打开再次做实验的门

    def point1_switch_off(self, switch_off_top, wire_connection_top, wire_post_top, switch_top,
                          switch_off_side, switch_off_front, side_true, front_true):
        if switch_off_top.shape[0] != 0 and (wire_connection_top.shape[0] != 0 or
                                             wire_post_top.shape[0] != 0):  #
            if self.class_name[int(switch_top[0][5])] == 'switch_off_top' and switch_off_top[0][4] >= 0.9:
                self.flag1_inertance_top += 1
                if self.flag1_inertance_top > 15:
                    return [True, 'top']
            elif side_true and switch_off_side.shape[0] != 0:
                self.flag1_inertance_side += 1
                if self.flag1_inertance_side > 5:
                    return [True, 'side']
            elif front_true and switch_off_front.shape[0] != 0:
                self.flag1_inertance_front += 1
                if self.flag1_inertance_front > 5:
                    return [True, 'front']
        return [False, '']

    def point2_r_right(self, connect_above_top, connect_following_top,
                       connect_above_side, connect_following_side,
                       top_true, side_true):
        if top_true and connect_above_top.shape[0] == 1 and connect_following_top.shape[0] == 1:
            self.flag2_inertance_top += 1
            if self.flag2_inertance_top > 7:
                return [True, 'top']

        elif side_true and connect_above_side.shape[0] == 1 and connect_following_side.shape[0] == 1:
            self.flag2_inertance_side += 1
            if self.flag2_inertance_side > 3:
                return [True, 'side']
        return [False, '']

    def point3_r_max(self, following_top, connect_following_top, gleithretter_top,
                     following_side, connect_following_side, gleithretter_side,
                     top_true, side_true):
        if top_true and connect_following_top.shape[0] == 1 and following_top.shape[0] == 1 and gleithretter_top.shape[0] != 0:
            following_top_box = following_top[0][:4]
            connect_following_top_box = connect_following_top[0][:4]
            gleithretter_top_box = gleithretter_top[0][:4]
            oa = int(distance_box(following_top_box, gleithretter_top_box))
            ob = int(distance_box(following_top_box, connect_following_top_box))
            ab = int(distance_box(gleithretter_top_box, connect_following_top_box))
            coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob + 0.0001)
            if 0.5 > coso > -1:
                # 接入正确，Rmax，提交图片
                self.flag3_inertance_top += 1
                if self.flag3_inertance_top > 7:
                    return [True, 'top']

        elif side_true and connect_following_side.shape[0] == 1 and following_side.shape[0] == 1 and gleithretter_side.shape[0] != 0:
            following_side_box = following_side[0][:4]
            connect_following_side_box = connect_following_side[0][:4]
            gleithretter_side_box = gleithretter_side[0][:4]
            oa = int(distance_box(following_side_box, gleithretter_side_box))
            ob = int(distance_box(following_side_box, connect_following_side_box))
            ab = int(distance_box(gleithretter_side_box, connect_following_side_box))
            coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob + 0.0001)
            if 0.5 > coso > -1:
                self.flag3_inertance_side += 1
                if self.flag3_inertance_side > 3:
                    return [True, 'side']
        return [False, '']

    def point4_range(self, power_source_top, range_top, ammeter_top):
        if power_source_top.shape[0] != 0 and range_top.shape[0] != 0:
            power_num = 0
            for power_source in power_source_top:
                power_source_box = power_source[:4]
                if iou(self.center_box, power_source_box) > 0:
                    power_num += 1
            # 判断一个电源还是两个电源，统计帧数，差的绝对值，比较出现次数
            if 3 > power_num > 0:
                self.flag4_min += 1
            elif power_num > 2:
                self.flag4_max += 1
            if abs(self.flag4_min - self.flag4_max) > 10:
                self.flag4_range = 'min' if self.flag4_min > self.flag4_max else 'max'
            if abs(self.flag4_min - self.flag4_max) > 65:
                if self.flag4_min > self.flag4_max:
                    self.flag4_min -= 40
                elif self.flag4_min < self.flag4_max:
                    self.flag4_max -= 40

            # 找到与电压表相交的置信度最大的量程
            a_range = []
            if len(range_top) != 0 and len(ammeter_top) != 0:
                for range_t in range_top:
                    if iou(range_t[:4], ammeter_top[0][:4]) > 0:
                        if len(a_range) != 0 and a_range[4] < range_t[4]:
                            a_range.clear()
                        a_range += range_t

            if self.flag4_range == 'min' and len(a_range) != 0 and self.class_name[int(a_range[5])] == 'min_red_top' and 3 > power_num > 0:
                self.flag4_inertance_min += 1
                if self.flag4_inertance_min > 3:
                    return [True, 'top']

            elif self.flag4_range == 'max' and len(a_range) != 0 and self.class_name[int(a_range[5])] == 'max_red_top' and power_num > 2:
                # self.flag4_inertance_max += 1
                # if self.flag4_inertance_max > 1:
                return [True, 'top']
        return [False, '']

    def point5_polarity(self, this_frame_terminals):
        # 判断电源正负极连接
        polaritys_num = 0
        for item in ['power', 'ammeter']:
            if item in this_frame_terminals:
                polaritys_num += 1
        if polaritys_num == 2:
            self.flag5_inertance += 1
        if self.flag5_inertance > 3:
            return [True, 'top']
        return [False, '']

    def point6_serie(self, this_frame_terminals, slide_rheostat_top):
        # 从U+到U-，跳过V
        # 判断串联
        '''
        ### 可以有两个above或量following   未写入
        '''
        serie_num = 0
        for item in ['power', 'switch', 'ammeter', 'slide']:
            if item in this_frame_terminals:
                serie_num += 1
        if serie_num >= 3 and slide_rheostat_top.shape[0] != 0:
            self.flag6_inertance += 1
        if self.flag6_inertance > 3:
            return [True, 'top']
        return [False, '']

    def point7_point(self, pointer_top, switch_top, ammeter_top,
                     pointer_side, switch_side, ammeter_side,
                     top_true, side_true):
        if top_true:
            criterion_num_top = 0
            # 找到与电压表相交的指针
            a_pointer_top = []
            if len(pointer_top) != 0 and len(ammeter_top) != 0:
                for pointer_t in pointer_top:
                    if iou(pointer_t[:4], ammeter_top[0][:4]) > 0:
                        if len(a_pointer_top) != 0 and a_pointer_top[4] < pointer_t[4]:
                            a_pointer_top.clear()
                        a_pointer_top += pointer_t
            if len(a_pointer_top) != 0 and self.class_name[int(a_pointer_top[5])] == 'pointer_offset_top':
                criterion_num_top += 1
            if switch_top.shape[0] != 0 and self.class_name[int(switch_top[0][5])] == 'switch_on_top':
                criterion_num_top += 1
            if criterion_num_top == 2:
                #     self.flag7_inertance_top += 1
                # if self.flag7_inertance_top > 1:
                return [True, 'top']

        if side_true and not self.scorePoint7:
            criterion_num_side = 0
            # 找到与电压表相交的指针
            a_pointer_side = []
            if len(pointer_side) != 0 and len(ammeter_side) != 0:
                for pointer_s in pointer_side:
                    if iou(pointer_s[:4], ammeter_side[0][:4]) > 0:
                        if len(a_pointer_side) != 0 and a_pointer_side[4] < pointer_s[4]:
                            a_pointer_side.clear()
                        a_pointer_side += pointer_s
            if len(a_pointer_side) != 0 and self.class_name[int(a_pointer_side[5])] == 'pointer_offset_top':
                criterion_num_side += 1
            if switch_side.shape[0] != 0 and self.class_name[int(switch_side[0][5])] == 'switch_on_top':
                criterion_num_side += 1
            if criterion_num_side == 2:
                #   self.flag7_inertance_side += 1
                # if self.flag7_inertance_side > 1:
                return [True, 'side']
        return [False, '']

    def point8_gleithretter_site(self, top_true, side_true, front_true,
                                 following_top, connect_following_top, gleithretter_top, pointer_offset_top,
                                 slide_rheostat_side,  gleithretter_side,
                                 slide_rheostat_front, gleithretter_front):
        # 改变滑片位置 先求滑片、following连接线与following、connect_following连接线的夹角，
        # 再求相对水平时滑片到following的水平距离（垂直距离恒等），用位移来确定滑片位置发生改变
        if top_true and following_top.shape[0] != 0 and connect_following_top.shape[0] != 0 and \
                gleithretter_top.shape[0] != 0 and pointer_offset_top.shape[0] != 0:
            following_top_box = following_top[0][:4]
            connect_following_top_box = connect_following_top[0][:4]
            gleithretter_top_box = gleithretter_top[0][:4]
            oa_rt = distance_box(following_top_box, gleithretter_top_box)
            ob_rt = distance_box(following_top_box, connect_following_top_box)
            ab_rt = distance_box(gleithretter_top_box, connect_following_top_box)
            coso_rt = (oa_rt * oa_rt + ob_rt * ob_rt - ab_rt * ab_rt) / (2 * oa_rt * ob_rt + 0.0001)
            dt = oa_rt * coso_rt
            if self.flag8_top_dt == 0:
                self.flag8_top_dt = dt
            else:
                delta_dt = abs(dt - self.flag8_top_dt)
                if delta_dt > 65:
                    self.flag8_inertance_top += 1
                if self.flag8_inertance_top > 5:
                    return [True, 'top']

        if side_true and slide_rheostat_side.shape[0] != 0 and gleithretter_side.shape[0] != 0:
            slide_rheostat_side_box = slide_rheostat_side[0][:4]
            gleithretter_side_box = gleithretter_side[0][:4]
            if abs(slide_rheostat_side_box[2] - slide_rheostat_side_box[0]) > abs(slide_rheostat_side_box[3] - slide_rheostat_side_box[1]):
                od = center_distance_h(slide_rheostat_side_box, gleithretter_side_box)
                ratio = abs(od) / abs(slide_rheostat_side_box[2] - slide_rheostat_side_box[0])
            else:
                od = center_distance_v(slide_rheostat_side_box, gleithretter_side_box)
                ratio = abs(od) / abs(slide_rheostat_side_box[3] - slide_rheostat_side_box[1])
            if ratio < 0.1:
                self.flag8_inertance_side += 1
            if self.flag8_inertance_side > 3:
                return [True, 'side']

        if front_true and slide_rheostat_front.shape[0] != 0 and gleithretter_front.shape[0] != 0:
            slide_rheostat_front_box = slide_rheostat_front[0][:4]
            gleithretter_front_box = gleithretter_front[0][:4]
            if abs(slide_rheostat_front_box[2] - slide_rheostat_front_box[0]) > abs(slide_rheostat_front_box[3] - slide_rheostat_front_box[1]):
                od = center_distance_h(slide_rheostat_front_box, gleithretter_front_box)
                ratio = abs(od) / abs(slide_rheostat_front_box[2] - slide_rheostat_front_box[0])
            else:
                od = center_distance_v(slide_rheostat_front_box, gleithretter_front_box)
                ratio = abs(od) / abs(slide_rheostat_front_box[3] - slide_rheostat_front_box[1])
            if ratio < 0.1:
                self.flag8_inertance_front += 1
            if self.flag8_inertance_front > 3:
                return [True, 'front']
        return [False, '']

    def point9_switch_off(self, switch_top, pointer_top, ammeter_top,
                          pointer_side, switch_side, ammeter_side,
                          this_frame_terminals, top_true, side_true):
        if top_true and switch_top.shape[0] != 0 and \
                self.class_name[int(switch_top[0][5])] == 'switch_off_top' and \
                len(this_frame_terminals) >= 3:
            self.flag9_on_top += 1
        if self.flag9_on_top > 20:
            criterion_num_top = 0
            # 找到与电压表相交的指针
            a_pointer_top = []
            if len(pointer_top) != 0 and len(ammeter_top) != 0:
                for pointer_t in pointer_top:
                    if iou(pointer_t[:4], ammeter_top[0][:4]) > 0:
                        if len(a_pointer_top) != 0 and a_pointer_top[4] < pointer_t[4]:
                            a_pointer_top.clear()
                        a_pointer_top += pointer_t
            if len(a_pointer_top) != 0 and self.class_name[int(a_pointer_top[5])] == 'pointer_zero_top':
                criterion_num_top += 1
            if switch_top.shape[0] != 0 and switch_side.shape[0] != 0 and self.class_name[int(switch_top[0][5])] == 'switch_off_top':
                criterion_num_top += 1
            if criterion_num_top == 2:
                self.flag9_inertance_top += 1
            if self.flag9_inertance_top > 25:
                return [True, 'top']

            if side_true and not self.scorePoint9:
                criterion_num_side = 0
                # 找到与电压表相交的指针
                a_pointer_side = []
                if len(pointer_side) != 0 and len(ammeter_side) != 0:
                    for pointer_s in pointer_side:
                        if iou(pointer_s[:4], ammeter_side[0][:4]) > 0:
                            if len(a_pointer_side) != 0 and a_pointer_side[4] < pointer_s[4]:
                                a_pointer_side.clear()
                            a_pointer_side += pointer_s
                if len(a_pointer_side) != 0 and self.class_name[int(a_pointer_side[5])] == 'pointer_zero_top':
                    criterion_num_side += 1
                if switch_side.shape[0] != 0 and self.class_name[int(switch_side[0][5])] == 'switch_off_top':
                    criterion_num_side += 1
                if criterion_num_side == 2:
                    self.flag9_inertance_side += 1
                if self.flag9_inertance_side > 3:
                    return [True, 'side']
        return [False, '']

    def point10_clean(self, power_source_top, switch_top, ammeter_top, slide_rheostat_top,gleithretter_top,
                      top_true, clean_desk_top, side_true, clean_desk_side, front_true, clean_desk_front):
        in_center_box = False
        if top_true:
            for items in [power_source_top, switch_top, ammeter_top, slide_rheostat_top, gleithretter_top]:
                for item in items:
                    item_box = item[:4]
                    if iou(item_box, self.center_box) > 100:
                        in_center_box = True
                        break
                if in_center_box:
                    break

            if not in_center_box or clean_desk_top.shape[0] != 0:  # or clean_desk_top.shape[0] != 0
                self.flag10_inertance_top += 1
                # if self.flag10_inertance_top > 5:
                return [True, 'top']

        elif side_true and clean_desk_side.shape[0] != 0:  # not in_center_box or
            return [True, 'side']
        elif front_true and clean_desk_front.shape[0] != 0:  # not in_center_box or
            return [True, 'front']
        return [False, '']