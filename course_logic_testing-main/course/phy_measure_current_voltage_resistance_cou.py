#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/02
# @Author  : Qinhe
# @File    : phy_measure_current_voltage_resistance_conf.py


from .comm import *
from .comm.course_base import ConfigModel
import copy


class PHY_measure_current_voltage_resistance(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(PHY_measure_current_voltage_resistance, self).__init__(*args, **kwargs)

        self.set_center_box = False  # 设置操作区域框

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
        self.scorePoint14 = False
        self.scorePoint15 = False

        self.all_frame_terminals = []

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
        self.flag5_min = 0
        self.flag5_max = 0
        self.flag5_range = ''
        self.flag5_inertance_min = 0
        self.flag5_inertance_max = 0
        self.flag6_v_polarity_route = []
        self.flag7_a_polarity_route = []
        self.flag8_parallel_route = []  # parallel 并联
        self.flag9_serie_route = []  # serie 串联
        self.flag10_inertance_top = 0
        self.flag10_inertance_side = 0
        self.flag11_inertance_top = 0
        self.flag11_inertance_side = 0
        self.flag12_on_top = 0
        self.flag12_top_dt = 0
        self.flag12_inertance_top = 0
        self.flag12_inertance_side = 0
        self.flag12_inertance_front = 0
        self.flag13_on_top = 0
        self.flag13_inertance_top = 0
        self.flag13_inertance_side = 0
        self.flag14_inertance_top = 0

        self.clearn_desk_info = []  # 整理桌面信息

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

                # 确定图片正反  #
                if not self.set_center_box and power_source_top.shape[0] != 0:
                    # h, w = self.top_img0.shape[:2]  todo
                    # 根据最开始器材在图片的位置确定操作区域
                    center_box_upright = torch.tensor([self.w_top * 0.33, self.h_top * 0.45, self.w_top * 0.72, self.h_top * 0.87], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
                    center_box_upend = torch.tensor([self.w_top * 0.28, self.h_top * 0.13, self.w_top * 0.67, self.h_top * 0.55], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面

                    binding_post = center_point(power_source_top[0][0:4])
                    self.center_box = center_box_upend if binding_post[1] > (self.h_top / 2) else center_box_upright
                    self.set_center_box = True

                switch_top = torch.cat([switch_off_top, switch_on_top], dim=0)
                if switch_top.shape[0] != 0:
                    switch_top = switch_top[torch.argsort(-switch_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                pointer_top = torch.cat([pointer_offset_top, pointer_zero_top], dim=0)
                if pointer_top.shape[0] != 0:
                    pointer_top = pointer_top[torch.argsort(-pointer_top[:, 4])]  # 置信度排序,指针  torch.sort(input, dim=0)按列排序

                range_top = torch.cat([min_1_top, max_1_top], dim=0)
                if range_top.shape[0] != 0:
                    range_top = range_top[torch.argsort(-range_top[:, 4])]  # 置信度排序,量程  torch.sort(input, dim=0)按列排序

                wire_post_top = torch.cat([wire_connection_red_top, wire_connection_black_top, min_1_top, max_1_top, connect_above_top, connect_following_top], dim=0)

                equipments_top = torch.cat([power_source_top, switch_top, ammeter_top, slide_rheostat_top, fixed_resistor_top, voltmeter_top], dim=0)  #

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
                    pointer_side = pointer_side[torch.argsort(-pointer_side[:, 4])]  # 置信度排序,指针  torch.sort(input, dim=0)按列排序

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
                this_frame_terminals = self.all_estimate_picture(wire_connection_top, equipments_top, wire_post_top)
                # 判断是否已经完成一次实验操作  演示版用导线辅助判断
                # self.all_estimate_experiment_ing(wire_connection_top)  # todo 重置self.的变量

            # 1.电路连接时开关处于断开状态
            if not self.scorePoint1 and top_true and "1" in self.exper_score_ids:
                point1view = self.point1_switch_off(switch_off_top, wire_connection_top, wire_post_top, switch_top,
                                                    switch_off_side, switch_off_front)
                if point1view[0]:
                    self.scorePoint1 = True
                    if point1view[1] == 'top':
                        self.assignScore(1, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point1view[1] == 'side':
                        self.assignScore(1, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point1view[1] == 'front':
                        self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)
            # END scorePoint1

            # 画布
            # self.all_canvas_creation()  # 创建画布

            # 2.滑动变阻器接入正确且电阻最大
            if not self.scorePoint2 and "2" in self.exper_score_ids and wire_post_top.shape[0] >= 2:  # 接线柱大于2
                point2view = self.point2_r_right(connect_above_top, connect_following_top,
                                                 connect_above_side, connect_following_side,
                                                 top_true, side_true)
                if point2view[0]:
                    self.scorePoint2 = True
                    if point2view[1] == 'top':
                        self.assignScore(2, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point2view[1] == 'side':
                        self.assignScore(2, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)

            # 3.滑动变阻器接入正确且电阻最大
            if not self.scorePoint3 and "3" in self.exper_score_ids and wire_post_top.shape[0] >= 2:  # 接线柱大于2
                point3view = self.point3_r_max(connect_following_top, following_top, gleithretter_top,
                                               connect_following_side, following_side, gleithretter_side,
                                               top_true, side_true)
                if point3view[0]:
                    self.scorePoint3 = True
                    if point3view[1] == 'top':
                        self.assignScore(3, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point3view[1] == 'side':
                        self.assignScore(3, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)

            # 4.电压表选择合适量程
            if not self.scorePoint4 and top_true and "4" in self.exper_score_ids and wire_post_top.shape[0] >= 3:  # 接线柱大于3
                point4view = self.point4_v_range(power_source_top, range_top, voltmeter_top)
                if point4view[0] and point4view[1] == 'top':
                    self.scorePoint4 = True
                    self.assignScore(4, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

            # 5.电流表选择合适量程
            if not self.scorePoint5 and top_true and "5" in self.exper_score_ids and wire_post_top.shape[0] >= 3:  # 接线柱大于3
                point5view = self.point5_a_range(power_source_top, range_top, ammeter_top)
                if point5view[0] and point5view[1] == 'top':
                    self.scorePoint5 = True
                    self.assignScore(5, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

            # 6.电压表，电源正负极连接正确
            if not self.scorePoint6 and top_true and "6" in self.exper_score_ids and len(self.all_frame_terminals) >= 2:  # 有器材被连接
                point6view = self.point6_v_polaritys(this_frame_terminals)
                if point6view[0] and point6view[1] == 'top':
                    self.scorePoint6 = True
                    self.assignScore(6, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

            # 7.电流表，电源正负极连接正确
            if not self.scorePoint7 and top_true and "7" in self.exper_score_ids and len(self.all_frame_terminals) >= 2:  # 有器材被连接
                point7view = self.point7_a_polaritys(this_frame_terminals)
                if point7view[0] and point7view[1] == 'top':
                    self.scorePoint7 = True
                    self.assignScore(7, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

            # 8.电压表并联在电阻两端  与电压表连接的器材一定有一根接线柱是连接了两个导线的
            if not self.scorePoint8 and top_true and "8" in self.exper_score_ids and len(self.all_frame_terminals) >= 2:  # 有器材被连接
                point8view = self.point8_parallels(this_frame_terminals)
                if point8view[0] and point8view[1] == 'top':
                    self.scorePoint8 = True
                    self.assignScore(8, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

                # self.all_canvas_drow(parallel_gather)  # 绘制画布
                # self.show_process(canvas)

            # 9.电源，开关，滑动变阻器，电阻，电流表串联
            if not self.scorePoint9 and top_true and "9" in self.exper_score_ids and len(self.all_frame_terminals) >= 5:  # 有器材被连接
                point9view = self.point9_series(this_frame_terminals)
                if point9view[0] and point9view[1] == 'top':
                    self.scorePoint9 = True
                    self.assignScore(9, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

            # 10.闭合开关，电压表指针发生偏转
            if not self.scorePoint10 and len(wire_connection_top) >= 4 and len(self.all_frame_terminals) >= 7:  # 导线个数大于4个，有器材被连接
                point10view = self.point10_v_criterion(pointer_top, switch_top, voltmeter_top,
                                                       pointer_side, switch_side, voltmeter_side,
                                                       top_true, side_true)
                if point10view[0]:
                    self.scorePoint10 = True
                    if point10view[1] == 'top':
                        self.assignScore(10, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point10view[1] == 'side':
                        self.assignScore(10, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)

            # 11.闭合开关，电流表指针发生偏转
            if not self.scorePoint11 and len(wire_connection_top) >= 4 and len(self.all_frame_terminals) >= 7:  # 导线个数大于4个，有器材被连接
                point11view = self.point11_a_criterion(pointer_top, switch_top, ammeter_top,
                                                       pointer_side, switch_side, ammeter_side,
                                                       top_true, side_true)
                if point11view[0]:
                    self.scorePoint11 = True
                    if point11view[1] == 'top':
                        self.assignScore(11, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point11view[1] == 'side':
                        self.assignScore(11, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)

            # 12.改变滑动变阻器电阻，观察电流表示数
            # 与滑动变阻器是否为Rmax无关，关键在于滑片位置的变化，使用相对平行的水平距离
            # 发生在闭合开关，但为断开开关中间
            if not self.scorePoint12 and len(self.all_frame_terminals) >= 7:  # 有器材被连接
                point12view = self.point12_gleithretter_site(following_top, connect_following_top, gleithretter_top, pointer_offset_top,
                                                             slide_rheostat_side, gleithretter_side,
                                                             slide_rheostat_front, gleithretter_front,
                                                             top_true, side_true, front_true,)
                if point12view[0]:
                    self.scorePoint12 = True
                    if point12view[1] == 'top':
                        self.assignScore(12, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point12view[1] == 'side':
                        self.assignScore(12, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point12view[1] == 'front':
                        self.assignScore(12, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 13.断开开关后再拆电路
            if not self.scorePoint13 and len(wire_connection_top) >= 4 and len(self.all_frame_terminals) >= 7:  # 导线个数大于4个，有器材被连接
                point13view = self.point13_switch_off(switch_top, pointer_top, ammeter_top, voltmeter_top,
                                                      pointer_side, switch_side, ammeter_side, voltmeter_side,
                                                      this_frame_terminals, top_true, side_true)
                if point13view[0]:
                    self.scorePoint13 = True
                    if point13view[1] == 'top':
                        self.assignScore(13, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point13view[1] == 'side':
                        self.assignScore(13, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)

            # 14.整理桌面
            if not self.scorePoint14 and len(self.all_frame_terminals) >= 7:  # 有器材被连接
                point14view = self.point14_clean(power_source_top, switch_top, ammeter_top,
                                                 slide_rheostat_top, fixed_resistor_top, voltmeter_top,
                                                 clean_desk_top, clean_desk_side, clean_desk_front,
                                                 top_true, side_true, front_true)
                if point14view[0]:
                    self.scorePoint14 = True
                    if point14view[1] == 'top':
                        self.assignScore(14, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point14view[1] == 'side':
                        self.assignScore(14, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point14view[1] == 'front':
                        self.assignScore(14, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

    def all_estimate_experiment_ing(self, wire_connection_top):  # 判断是否已经完成一次实验操作  演示版用导线辅助判断
        if len(wire_connection_top) >= 2 and not self.experiment_ing and not self.first_end:  # 判断第一次实验开始连接器材
            self.experiment_ing = True  # 打开拆除器材的门

        elif len(wire_connection_top) >= 2 and not self.experiment_ing and self.first_end:  # 判断再次实验开始连接器材
            self.experiment_ing = True  # 打开再次做实验的门
            self.experiment_end = 0
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
            self.scorePoint11 = False
            self.retracementScore(index=11)
            self.scorePoint12 = False
            self.retracementScore(index=12)
            self.scorePoint13 = False
            self.retracementScore(index=13)
            self.scorePoint14 = False
            self.retracementScore(index=14)

        elif len(wire_connection_top) == 0 and self.experiment_ing:  # 判断拆除器材
            self.experiment_end += 1
            if self.experiment_end > 100:
                self.experiment_ing = False
                self.first_end = True  # 打开再次做实验的门


    def all_estimate_picture(self, wire_connection_top, equipments_top, wire_post_top):
        # 6,7，8,9,10,11,12,13
        this_frame_terminals = []  # 这张图片中连接的器材
        this_frame_terminals_key = []
        if wire_connection_top.shape[0] != 0 \
                and (not self.scorePoint6 or not self.scorePoint7
                     or not self.scorePoint8 or not self.scorePoint9
                     or not self.scorePoint10 or not self.scorePoint11
                     or not self.scorePoint12 or not self.scorePoint13):  # 串并联，正负极
            for connection_top in wire_connection_top:  # 已连接的导线
                connection_top_box = connection_top[:4]
                equipments = []  # 器材
                connection_posts = []  # 连接导线的接线柱
                two_terminals = []  # [{'terminals_1':{'two_box_1':[],'two_box_2':[]}},{'terminals_2':{'two_box_3':[],'two_box_4':[]}}]

                # 提取与导线有交集的器材   一根导线和N个器材
                if equipments_top.shape[0] == 0:  # items is power_source_top and
                    continue
                for equipment in equipments_top:
                    equipment_box = equipment[:4]
                    if iou(connection_top_box, equipment_box) > 0:
                        equipments.append(equipment)

                # 判断导线连接的是哪个接线柱   一根导线和N个接线柱
                if wire_post_top.shape[0] == 0:
                    continue
                for post in wire_post_top:
                    post_box = post[:4]
                    if iou_min(connection_top_box, post_box) > 0.4:
                        connection_posts.append(post)

                # 确定器材和接线柱  有限器材和有限接线柱
                if len(equipments) >= 2 and len(connection_posts) >= 2:
                    if len(connection_posts) > 2:
                        connection_posts = self.all_find_two_points(connection_posts, equipments, connection_top)

                    if len(connection_posts) == 2:
                        for equ in equipments:
                            for post in connection_posts:
                                two_box = {}
                                terminals = {}
                                if iou(equ[:4], post[:4]) > 0:
                                    two_box['equ'] = equ[:4]
                                    two_box['post'] = post[:4]
                                    two_box['frequency'] = 0
                                    two_box['both'] = False
                                    term = str(self.class_name[int(equ[5])].split('_')[0] + '_' +
                                               self.class_name[int(post[5])].split('_')[-2])
                                    terminals[term] = two_box  # todo 待做 此实验中器材唯一，暂时不考虑重复
                                    two_terminals.append(terminals)

                # 确定一根导线连接两个器材
                # 此时的two_terminals只是一根导线的两端
                if len(two_terminals) == 2 and list(two_terminals[0].keys())[0].split('_')[0] != list(two_terminals[-1].keys())[0].split('_')[0]:
                    this_frame_terminals.append(two_terminals)
                    this_frame_terminals_key.append(list(two_terminals[0].keys())[0] + '_' + list(two_terminals[1].keys())[0])

            #         self.all_canvas_drow(parallel_gather)  # 绘制画布
            # # self.canvas = cv2.resize(self.canvas, (int(self.w_top/3), int(self.h_top/3)))
            #
            # self.show_process(self.canvas)

            self.all_frame_terminals += list(set(this_frame_terminals_key).difference(set(self.all_frame_terminals)))  # 累计的器材连接情况
        return this_frame_terminals

    def all_find_two_points(self, connection_posts, equipments, connection_top):
        # 导线轮廓
        if len(connection_posts) > 2:
            points = []  # 终极目标self TODO
            # 填充器材区域为白色
            this_frame = copy.deepcopy(self.frame_top)
            for eq in equipments:
                this_frame[int(eq[1]):int(eq[3]), int(eq[0]):int(eq[2])] = np.full((abs(int(eq[1]) - int(eq[3])), abs(int(eq[0]) - int(eq[2])), 3), 255)
            # end---填充器材

            # 截取导线区域
            connection = this_frame[int(connection_top[1]) - 10:int(connection_top[3]) + 10, int(connection_top[0]) - 10:int(connection_top[2]) + 10]
            # connection1 = self.frame_top[int(connection_top[1]) - 10:int(connection_top[3]) + 10, int(connection_top[0]) - 10:int(connection_top[2]) + 10]
            # end----截取导线

            # 处理图片
            img = cv2.cvtColor(connection, cv2.COLOR_BGR2GRAY)  # 转灰度图
            ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # 二值化
            img = cv2.Canny(img, 100, 1200)  # 提取轮廓
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 得到结构元素
            img = cv2.dilate(img, kernel, iterations=2)  # 膨胀
            img = cv2.erode(img, kernel, iterations=2)  # 侵蚀
            img = cv2.dilate(img, kernel, iterations=2)  # 膨胀
            # end---处理图片

            # 找到最大的轮廓面积
            max_cont = []  # 可以放到self中  TODO
            ct = 0
            contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 得到轮廓的坐标
            for cont in contours:
                if cv2.contourArea(cont) > ct:
                    ct = cv2.contourArea(cont)
                    max_cont = (cont)
            # end---最大面积

            if len(max_cont) > 0:
                # 一阶求导

                r = 1
                k_x = []  # k是斜率
                k_y = []
                max_cont = np.vstack((max_cont, max_cont[0:r].reshape((r, 1, 2))))  # 将0位置的坐标复制粘贴到新的维
                for i in range(len(max_cont) - r):
                    k_x.append(max_cont[i + r][0][0] - max_cont[i][0][0])  # 记录x轴的相邻坐标的走向（变化规律）
                    k_y.append(max_cont[i + r][0][1] - max_cont[i][0][1])  # 记录y轴的相邻坐标的走向（变化规律）

                k_x[0] = k_x[-1]
                k_y[0] = k_y[-1]
                for i in range(1, len(k_x)):  # 降噪 变化为0的
                    if k_x[i] == 0:
                        k_x[i] = k_x[i - 1]
                    if k_y[i] == 0:
                        k_y[i] = k_y[i - 1]

                k_x1 = copy.deepcopy(k_x)
                k_x1.insert(0, k_x1.pop(-1))  # 错位
                k_x2 = list(map(lambda a: abs(a[0] - a[1]), zip(k_x1, k_x)))  # 找到x轴走向变化的转折点
                k_y1 = copy.deepcopy(k_y)
                k_y1.insert(0, k_y1.pop(-1))  # 错位
                k_y2 = list(map(lambda a: abs(a[0] - a[1]), zip(k_y1, k_y)))  # 找到y轴走向变化的转折点

                k_x2_id = []
                k_y2_id = []
                # 找到转折点的id
                for i in range(len(k_x2)):
                    if k_x2[i] > 0:
                        k_x2_id.append(i)
                    if k_y2[i] > 0:
                        k_y2_id.append(i)
                # 放大转折点的区域
                for i in k_x2_id:
                    k_x2[max(0, i - 10):min(i + 10, len(k_x2) - 1)] = [k_x2[i]] * abs(max(0, i - 10) - min(i + 10, len(k_x2) - 1))
                for i in k_y2_id:
                    k_y2[max(0, i - 10):min(i + 10, len(k_x2) - 1)] = [k_y2[i]] * abs(max(0, i - 10) - min(i + 10, len(k_x2) - 1))

                turn_points = list(map(lambda a: a[0] + a[1], zip(k_x2, k_y2)))  # x轴和y轴同时发生转折的点
                turn_points_id = [i for i in range(len(turn_points)) if turn_points[i] > 2]  # 提取id
                point_id = []
                if len(turn_points_id) > 1:
                    # 过滤相邻的点
                    turn_points_id.insert(0, turn_points_id.pop(-1))
                    for i in range(1, len(turn_points_id)):
                        if 1 < abs(turn_points_id[i] - turn_points_id[i - 1]) < len(turn_points) - 11:
                            point_id.append(turn_points_id[i])
                    # end---过滤v

                    for j in point_id:
                        # cv2.circle(connection1, tuple(max_cont[j][0]), 1, (255, 255, 0), 3)
                        # cv2.putText(connection1, f'{j}', tuple(max_cont[j][0]), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 1)
                        points.append(max_cont[j][0])

            '''显示单个导线窗口'''
            # img = np.concatenate((img.reshape((img.shape[0], img.shape[1], 1)), img.reshape((img.shape[0], img.shape[1], 1)), img.reshape((img.shape[0], img.shape[1], 1))), axis=2)
            # # img = np.concatenate((img1.reshape((img1.shape[0], img1.shape[1], 1)), img1.reshape((img1.shape[0], img1.shape[1], 1)), img1.reshape((img1.shape[0], img1.shape[1], 1))), axis=2)
            # imgall = np.hstack([img, connection1])
            # cv2.imshow('f', imgall)
            # cv2.waitKey(1000)
            # cv2.destroyWindow('f')

            posts1 = []
            if len(points) > 1:
                posts = []
                d1 = []
                for post in connection_posts:
                    d_self = 3000
                    group = {}
                    # 找到与接线柱最近的转折点
                    for point in points:
                        d = distance_point((point[0] + int(connection_top[0]) - 10, point[1] + int(connection_top[1]) - 10), center_point(post[:4]))  # 计算转折点与接线柱坐标的距离)
                        if d < d_self:
                            d_self = d
                            group['point'] = point
                            group['post'] = post
                    d1.append(d_self)
                    posts.append(group)
                    # end ----最近的转折点
                d2 = copy.deepcopy(d1)
                posts1.append(posts[d2.index(d1.pop(d1.index(min(d1))))]['post'])
                posts1.append(posts[d2.index(d1.pop(d1.index(min(d1))))]['post'])

                return posts1  # connection_posts = posts1
            else:
                return posts1  # connection_posts = posts1

    def all_replace_gather_free(self, gather, free):
        list(gather[0].values())[0]['equ'] = list(free[0].values())[0]['equ']
        list(gather[0].values())[0]['post'] = list(free[0].values())[0]['post']
        list(gather[0].values())[0]['frequency'] = list(free[0].values())[0]['frequency']
        list(gather[-1].values())[0]['equ'] = list(free[-1].values())[0]['equ']
        list(gather[-1].values())[0]['post'] = list(free[-1].values())[0]['post']
        list(gather[-1].values())[0]['frequency'] = list(free[-1].values())[0]['frequency']

    def all_canvas_creation(self):  # 创建画布
        self.equ_name = ['power', 'switch', 'ammeter', 'slide', 'fixed', 'voltmeter']
        self.equ_end = []
        self.equ_close = [(0, 0, 255), (0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]
        self.canvas = np.zeros((self.h_top, self.w_top, 3), dtype="uint8")

    def all_canvas_drow(self, parallel_gather):  # 绘制画布
        line = []
        font = cv2.FONT_HERSHEY_SIMPLEX
        # for parallel_gather1 in parallel_route:
        for terminals in parallel_gather:
            index = self.equ_name.index(list(terminals.keys())[0].split('_')[0])
            name_equ = list(terminals.keys())[0].split('_')[0]
            name_post = list(terminals.keys())[0]

            if name_equ not in self.equ_end or name_equ == 'power':
                equ_box = list(terminals.values())[0]['equ']
                cv2.rectangle(self.canvas, (int(equ_box[0]), int(equ_box[1])), (int(equ_box[2]), int(equ_box[3])), self.equ_close[index], 3)
                cv2.putText(self.canvas, name_equ, (int(equ_box[0]), int(equ_box[1]) + 50), font, 1, (255, 255, 255), 1)
                self.equ_end.append(name_equ)
            if name_post not in self.equ_end or name_post == 'fixed_red':
                equ_post = list(terminals.values())[0]['post']
                cv2.rectangle(self.canvas, (int(equ_post[0]), int(equ_post[1])), (int(equ_post[2]), int(equ_post[3])), self.equ_close[index], 3)
                self.equ_end.append(name_post)
                line.append(center_point(equ_post))
            if len(line) == 2:
                cv2.line(self.canvas, (int(line[0][0]), int(line[0][1])), (int(line[1][0]), int(line[1][1])), (255, 255, 255), 3)  # 9

    def point1_switch_off(self, switch_off_top, wire_connection_top, wire_post_top, switch_top,
                          switch_off_side, switch_off_front):
        if switch_off_top.shape[0] != 0 and (wire_connection_top.shape[0] != 0 or
                                             wire_post_top.shape[0] != 0):  #
            if self.class_name[int(switch_top[0][5])] == 'switch_off_top' and switch_off_top[0][4] >= 0.9:
                self.flag1_inertance_top += 1
                if self.flag1_inertance_top > 15:
                    return [True, 'top']
            if switch_off_side.shape[0] != 0:
                self.flag1_inertance_side += 1
                if self.flag1_inertance_side > 5:
                    return [True, 'side']
            elif switch_off_front.shape[0] != 0:
                self.flag1_inertance_front += 1
                if self.flag1_inertance_front > 5:
                    return [True, 'front']
        return [False, '']

    def point2_r_right(self, connect_above_top, connect_following_top,
                       connect_above_side, connect_following_side,
                       top_true, side_true):
        # 接入正确
        if top_true and connect_above_top.shape[0] == 1 and connect_following_top.shape[0] == 1:
            self.flag3_inertance_top += 1
            if self.flag3_inertance_top > 7:
                return [True, 'top']

        elif side_true and connect_above_side.shape[0] == 1 and connect_following_side.shape[0] == 1:  # 添加第一个连接的组合
            self.flag3_inertance_side += 1
            if self.flag3_inertance_side > 3:
                return [True, 'side']
        return [False, '']

    def point3_r_max(self, connect_following_top, following_top, gleithretter_top,
                     connect_following_side, following_side, gleithretter_side,
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

    def point4_v_range(self, power_source_top, range_top, voltmeter_top):
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

            # 找到与电压表相交的量程
            v_range = []
            if len(range_top) != 0 and len(voltmeter_top) != 0:
                for range_t in range_top:
                    if iou(range_t[:4], voltmeter_top[0][:4]) > 0:
                        if len(v_range) != 0 and v_range[4] < range_t[4]:
                            v_range.clear()
                        v_range += range_t
            if self.flag4_range == 'min' and len(v_range) != 0 and self.class_name[int(v_range[5])] == 'min_red_top' and 3 > power_num > 0:  #
                self.flag4_inertance_min += 1
                if self.flag4_inertance_min > 3:
                    return [True, 'top']

            elif self.flag4_range == 'max' and len(v_range) != 0 and self.class_name[int(v_range[5])] == 'max_red_top' and power_num > 2:
                self.flag4_inertance_max += 1
                if self.flag4_inertance_max > 3:
                    return [True, 'top']
        return [False, '']

    def point5_a_range(self, power_source_top, range_top, ammeter_top):
        if power_source_top.shape[0] != 0 and range_top.shape[0] != 0:
            power_num = 0
            for power_source in power_source_top:
                power_source_box = power_source[:4]
                if iou(self.center_box, power_source_box) > 0:
                    power_num += 1
            # 判断一个电源还是两个电源，统计帧数，差的绝对值，比较出现次数
            if 3 > power_num > 0:
                self.flag5_min += 1
            elif power_num > 2:
                self.flag5_max += 1
            if abs(self.flag5_min - self.flag5_max) > 10:
                self.flag5_range = 'min' if self.flag5_min > self.flag5_max else 'max'
            if abs(self.flag5_min - self.flag5_max) > 65:
                if self.flag5_min > self.flag5_max:
                    self.flag5_min -= 40
                elif self.flag5_min < self.flag5_max:
                    self.flag5_max -= 40

            # 找到与电流表相交的量程
            a_range = []
            if len(range_top) != 0 and len(ammeter_top) != 0:
                for range_t in range_top:
                    if iou(range_t[:4], ammeter_top[0][:4]) > 0:
                        if len(a_range) != 0 and a_range[4] < range_t[4]:
                            a_range.clear()
                        a_range += range_t
            if self.flag5_range == 'min' and len(a_range) != 0 and self.class_name[int(a_range[5])] == 'min_red_top' and 3 > power_num > 0:
                self.flag5_inertance_min += 1
                if self.flag5_inertance_min > 3:
                    return [True, 'top']
            elif self.flag5_range == 'max' and len(a_range) != 0 and self.class_name[int(a_range[5])] == 'max_red_top' and power_num > 2:
                self.flag5_inertance_max += 1
                if self.flag5_inertance_max > 3:
                    return [True, 'top']
        return [False, '']

    def point6_v_polaritys(self, this_frame_terminals):  # TODO 出现了连接错误的情况（未完成）
        # 判断电源正负极连接
        v_polaritys = copy.deepcopy(this_frame_terminals)

        if len(self.flag6_v_polarity_route) == 0:  # 添加第一个连接的组合  从电压表出发
            for v_polarity in v_polaritys:
                if list(v_polarity[0].keys())[0] in ['power_red', 'power_black'] or list(v_polarity[-1].keys())[0] in ['power_red', 'power_black']:
                    if list(v_polarity[-1].keys())[0] in ['power_red', 'power_black']:
                        v_polarity.insert(0, v_polarity.pop(v_polarity.index(v_polarity[-1])))  # 重新排序
                    self.flag6_v_polarity_route.append([copy.deepcopy(v_polarity)])
                    break

        if len(self.flag6_v_polarity_route) != 0:  # 列表 [[],[],[]]
            for v_polarity_route in self.flag6_v_polarity_route:  # 单个路径在路径集合中
                # 如果第一个不是电源要清空clean
                if list(v_polarity_route[0][0].values())[0]['frequency'] > 70:
                    self.flag6_v_polarity_route.remove(v_polarity_route)

                for v_polarity_gather in v_polarity_route:  # 这里的v_polarity_gather只代表一根导线  for v_polarity_gather in v_polarity_route:
                    for v_polarity_free in v_polaritys:
                        if list(v_polarity_gather[0].keys())[0].split('_')[0] in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]] or \
                                list(v_polarity_gather[-1].keys())[0].split('_')[0] in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]]:
                            # 替换box  post的iou，equ的iou   同一导线连接的两个器材的位置比较
                            if list(v_polarity_gather[0].keys())[0].split('_')[0] in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    list(v_polarity_gather[-1].keys())[0].split('_')[0] in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]]:
                                # 调整顺序
                                if list(v_polarity_gather[0].keys())[0].split('_')[0] == list(v_polarity_free[-1].keys())[0].split('_')[0]:
                                    v_polarity_free.insert(0, v_polarity_free.pop(-1))  # 重新排序
                                equ_box_gather_0 = list(v_polarity_gather[0].values())[0]['equ']  # 已连接的器材，id为0
                                post_box_gather_0 = list(v_polarity_gather[0].values())[0]['post']  # 已连接的接线柱，id为0
                                equ_box_gather_1 = list(v_polarity_gather[-1].values())[0]['equ']  # 已连接的器材，id为1
                                post_box_gather_1 = list(v_polarity_gather[-1].values())[0]['post']  # 已连接的接线柱，id为1
                                equ_box_free_0 = list(v_polarity_free[0].values())[0]['equ']  # 待连接的器材，id为0
                                post_box_free_0 = list(v_polarity_free[0].values())[0]['post']  # 待连接的接线柱，id为0
                                equ_box_free_1 = list(v_polarity_free[-1].values())[0]['equ']  # 待连接的器材，id为1
                                post_box_free_1 = list(v_polarity_free[-1].values())[0]['post']  # 待连接的接线柱，id为1

                                # 同一个目标直接替换
                                if iou_min(equ_box_gather_0, equ_box_free_0) > 0.4 and iou_min(equ_box_gather_1, equ_box_free_1) > 0.4 and \
                                        iou_min(post_box_gather_0, post_box_free_0) > 0.4 and iou_min(post_box_gather_1, post_box_free_1) > 0.4:
                                    self.all_replace_gather_free(v_polarity_gather, v_polarity_free)
                                    break

                                # 遮挡情况，大于某个值再替换
                                elif list(v_polarity_gather[0].values())[0]['frequency'] > 50:
                                    self.all_replace_gather_free(v_polarity_gather, v_polarity_free)
                                    break
                            # end--- 同一导线连接的两个器材的位置比较

                            # 匹配gather[0]的位置，找到接有两跟导线
                            elif list(v_polarity_gather[0].keys())[0].split('_')[0] in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    list(v_polarity_gather[-1].keys())[0].split('_')[0] not in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    (list(v_polarity_free[0].keys())[0] in ['power_red', 'power_black'] or
                                     list(v_polarity_free[-1].keys())[0] in ['power_red', 'power_black']) and \
                                    not list(v_polarity_free[0].values())[0]['both']:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(v_polarity_gather[0].keys())[0].split('_')[0] == list(v_polarity_free[-1].keys())[0].split('_')[0]:
                                    v_polarity_free.insert(0, v_polarity_free.pop(-1))  # 重新排序
                                post_box_gather = list(v_polarity_gather[0].values())[0]['post']
                                post_box_free = list(v_polarity_free[0].values())[0]['post']

                                # 将另一条路径加入
                                if iou_min(post_box_gather, post_box_free) < 0:
                                    list(v_polarity_gather[0].values())[0]['both'] = True
                                    list(v_polarity_free[0].values())[0]['both'] = True
                                    self.flag6_v_polarity_route.append([copy.deepcopy(v_polarity_free)])

                            # 匹配gather[-1]的位置，找到接有两跟导线
                            elif list(v_polarity_gather[0].keys())[0].split('_')[0] not in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    list(v_polarity_gather[-1].keys())[0].split('_')[0] in [list(v_polarity_free[0].keys())[0].split('_')[0], list(v_polarity_free[-1].keys())[0].split('_')[0]]:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(v_polarity_gather[-1].keys())[0].split('_')[0] == list(v_polarity_free[-1].keys())[0].split('_')[0]:
                                    v_polarity_free.insert(0, v_polarity_free.pop(-1))
                                post_box_gather = list(v_polarity_gather[-1].values())[0]['post']
                                post_box_free = list(v_polarity_free[0].values())[0]['post']
                                equ_box_gather = list(v_polarity_gather[-1].values())[0]['equ']

                                # 不分路线  接线柱依次顺序连接
                                if iou_min(post_box_gather, post_box_free) < 0.2 and iou(equ_box_gather, post_box_free) > 0 and v_polarity_route[-1] is v_polarity_gather:
                                    v_polarity_route.append(v_polarity_free)

                                # 匹配gather[-1]的位置，gather[-1]不是v_polarity_gather的最后一个，找到接有两跟导线
                                elif iou_min(post_box_gather, post_box_free) > 0.4 and iou(equ_box_gather, post_box_free) > 0 and not list(v_polarity_gather[-1].values())[0]['both']:  # 0.7 >=  > 0.4
                                    list(v_polarity_gather[-1].values())[0]['both'] = True
                                    list(v_polarity_free[0].values())[0]['both'] = True
                                    while v_polarity_route[-1] is not v_polarity_gather:
                                        v_polarity_route.pop(-1)
                                    v_polarity_route.append(v_polarity_free)

                    # 记数出现频率
                    list(v_polarity_gather[0].values())[0]['frequency'] += 1

                    # 尾部是电压表
                    if list(v_polarity_route[0][0].keys())[0].split('_')[-1] == list(v_polarity_route[-1][-1].keys())[0].split('_')[-1] and \
                            list(v_polarity_route[-1][-1].keys())[0] in ['voltmeter_red', 'voltmeter_black']:
                        return [True, 'top']
        return [False, '']

    def point7_a_polaritys(self, this_frame_terminals):
        # 判断电源正负极连接
        a_polaritys = copy.deepcopy(this_frame_terminals)

        if len(self.flag7_a_polarity_route) == 0:  # 添加第一个连接的组合  从电压表出发
            for a_polarity in a_polaritys:
                if list(a_polarity[0].keys())[0] in ['power_red', 'power_black'] or list(a_polarity[-1].keys())[0] in ['power_red', 'power_black']:
                    if list(a_polarity[-1].keys())[0] in ['power_red', 'power_black']:
                        a_polarity.insert(0, a_polarity.pop(a_polarity.index(a_polarity[-1])))  # 重新排序
                    self.flag7_a_polarity_route.append([copy.deepcopy(a_polarity)])
                    break

        if len(self.flag7_a_polarity_route) != 0:  # 列表 [[],[],[]]
            for a_polarity_route in self.flag7_a_polarity_route:  # 单个路径在路径集合中

                # 如果第一个不是电源要清空clean
                if list(a_polarity_route[0][0].keys())[0] not in ['power_red', 'power_black']:
                    self.flag7_a_polarity_route.remove(a_polarity_route)

                for a_polarity_gather in a_polarity_route:  # 这里的a_polarity_gather只代表一根导线  for a_polarity_gather in a_polarity_route:
                    for a_polarity_free in a_polaritys:
                        if list(a_polarity_gather[0].keys())[0].split('_')[0] in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]] or \
                                list(a_polarity_gather[-1].keys())[0].split('_')[0] in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]]:
                            # 替换box  post的iou，equ的iou   同一导线连接的两个器材的位置比较
                            if list(a_polarity_gather[0].keys())[0].split('_')[0] in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    list(a_polarity_gather[-1].keys())[0].split('_')[0] in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]]:
                                # 调整顺序
                                if list(a_polarity_gather[0].keys())[0].split('_')[0] == list(a_polarity_free[-1].keys())[0].split('_')[0]:
                                    a_polarity_free.insert(0, a_polarity_free.pop(-1))  # 重新排序
                                equ_box_gather_0 = list(a_polarity_gather[0].values())[0]['equ']  # 已连接的器材，id为0
                                post_box_gather_0 = list(a_polarity_gather[0].values())[0]['post']  # 已连接的接线柱，id为0
                                equ_box_gather_1 = list(a_polarity_gather[-1].values())[0]['equ']  # 已连接的器材，id为1
                                post_box_gather_1 = list(a_polarity_gather[-1].values())[0]['post']  # 已连接的接线柱，id为1
                                equ_box_free_0 = list(a_polarity_free[0].values())[0]['equ']  # 待连接的器材，id为0
                                post_box_free_0 = list(a_polarity_free[0].values())[0]['post']  # 待连接的接线柱，id为0
                                equ_box_free_1 = list(a_polarity_free[-1].values())[0]['equ']  # 待连接的器材，id为1
                                post_box_free_1 = list(a_polarity_free[-1].values())[0]['post']  # 待连接的接线柱，id为1

                                # 同一个目标直接替换
                                if iou_min(equ_box_gather_0, equ_box_free_0) > 0.4 and iou_min(equ_box_gather_1, equ_box_free_1) > 0.4 and \
                                        iou_min(post_box_gather_0, post_box_free_0) > 0.4 and iou_min(post_box_gather_1, post_box_free_1) > 0.4:
                                    self.all_replace_gather_free(a_polarity_gather, a_polarity_free)
                                    break

                                # 遮挡情况，大于某个值再替换
                                elif list(a_polarity_gather[0].values())[0]['frequency'] > 50:
                                    self.all_replace_gather_free(a_polarity_gather, a_polarity_free)
                                    break
                            # end--- 同一导线连接的两个器材的位置比较

                            # 匹配gather[0]的位置，找到接有两跟导线
                            elif list(a_polarity_gather[0].keys())[0].split('_')[0] in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    list(a_polarity_gather[-1].keys())[0].split('_')[0] not in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    (list(a_polarity_free[0].keys())[0] in ['power_red', 'power_black'] or
                                     list(a_polarity_free[-1].keys())[0] in ['power_red', 'power_black']) and \
                                    not list(a_polarity_free[0].values())[0]['both']:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(a_polarity_gather[0].keys())[0].split('_')[0] == list(a_polarity_free[-1].keys())[0].split('_')[0]:
                                    a_polarity_free.insert(0, a_polarity_free.pop(-1))  # 重新排序
                                post_box_gather = list(a_polarity_gather[0].values())[0]['post']
                                post_box_free = list(a_polarity_free[0].values())[0]['post']

                                # 将另一条路径加入
                                if iou_min(post_box_gather, post_box_free) < 0:  # 0.7 >=  > 0.4
                                    list(a_polarity_gather[0].values())[0]['both'] = True
                                    list(a_polarity_free[0].values())[0]['both'] = True
                                    self.flag7_a_polarity_route.append([copy.deepcopy(a_polarity_free)])

                            # 匹配gather[-1]的位置，找到接有两跟导线
                            elif list(a_polarity_gather[0].keys())[0].split('_')[0] not in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]] and \
                                    list(a_polarity_gather[-1].keys())[0].split('_')[0] in [list(a_polarity_free[0].keys())[0].split('_')[0], list(a_polarity_free[-1].keys())[0].split('_')[0]]:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(a_polarity_gather[-1].keys())[0].split('_')[0] == list(a_polarity_free[-1].keys())[0].split('_')[0]:
                                    a_polarity_free.insert(0, a_polarity_free.pop(-1))
                                post_box_gather = list(a_polarity_gather[-1].values())[0]['post']
                                post_box_free = list(a_polarity_free[0].values())[0]['post']
                                equ_box_gather = list(a_polarity_gather[-1].values())[0]['equ']

                                # 不分路线  接线柱依次顺序连接
                                if iou_min(post_box_gather, post_box_free) < 0.2 and iou(equ_box_gather, post_box_free) > 0 and a_polarity_route[-1] is a_polarity_gather:
                                    a_polarity_route.append(a_polarity_free)

                    # 记数出现频率
                    list(a_polarity_gather[0].values())[0]['frequency'] += 1
                    # 尾部是电流表
                    if list(a_polarity_route[0][0].keys())[0].split('_')[-1] == list(a_polarity_route[-1][-1].keys())[0].split('_')[-1] and \
                            list(a_polarity_route[-1][-1].keys())[0] in ['ammeter_red', 'ammeter_black']:
                        return [True, 'top']
        return [False, '']

    def point8_parallels(self, this_frame_terminals):
        # 从V+到V-，寻找连接了两根导线的接线柱
        # 判断并联
        # 添加并联的器材
        parallels = copy.deepcopy(this_frame_terminals)

        if len(self.flag8_parallel_route) == 0:  # 添加第一个连接的组合  从电压表出发
            for parallel in parallels:
                if list(parallel[0].keys())[0] in ['voltmeter_red', 'voltmeter_black'] or list(parallel[-1].keys())[0] in ['voltmeter_red', 'voltmeter_black']:
                    if list(parallel[-1].keys())[0] in ['voltmeter_red', 'voltmeter_black']:
                        parallel.insert(0, parallel.pop(parallel.index(parallel[-1])))  # 重新排序
                    self.flag8_parallel_route.append([copy.deepcopy(parallel)])
                    break

        if len(self.flag8_parallel_route) != 0:  # 并联列表 [[],[],[]]
            for parallel_route in self.flag8_parallel_route:  # 单个路径在路径集合中
                # 如果第一个不是电压表要清空clean
                if list(parallel_route[0][0].keys())[0] not in ['voltmeter_red', 'voltmeter_black']:
                    self.flag8_parallel_route.remove(parallel_route)

                for parallel_gather in parallel_route:  # 这里的parallel_gather只代表一根导线  for parallel_gather in parallel_route:
                    for parallel_free in parallels:
                        if list(parallel_gather[0].keys())[0].split('_')[0] in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]] or \
                                list(parallel_gather[-1].keys())[0].split('_')[0] in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]]:
                            # 替换box  post的iou，equ的iou   同一导线连接的两个器材的位置比较
                            if list(parallel_gather[0].keys())[0].split('_')[0] in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]] and \
                                    list(parallel_gather[-1].keys())[0].split('_')[0] in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]]:
                                # 调整顺序
                                if list(parallel_gather[0].keys())[0].split('_')[0] == list(parallel_free[-1].keys())[0].split('_')[0]:
                                    parallel_free.insert(0, parallel_free.pop(-1))  # 重新排序
                                equ_box_gather_0 = list(parallel_gather[0].values())[0]['equ']  # 已连接的器材，id为0
                                post_box_gather_0 = list(parallel_gather[0].values())[0]['post']  # 已连接的接线柱，id为0
                                equ_box_gather_1 = list(parallel_gather[-1].values())[0]['equ']  # 已连接的器材，id为1
                                post_box_gather_1 = list(parallel_gather[-1].values())[0]['post']  # 已连接的接线柱，id为1
                                equ_box_free_0 = list(parallel_free[0].values())[0]['equ']  # 待连接的器材，id为0
                                post_box_free_0 = list(parallel_free[0].values())[0]['post']  # 待连接的接线柱，id为0
                                equ_box_free_1 = list(parallel_free[-1].values())[0]['equ']  # 待连接的器材，id为1
                                post_box_free_1 = list(parallel_free[-1].values())[0]['post']  # 待连接的接线柱，id为1

                                # 同一个目标直接替换
                                if iou_min(equ_box_gather_0, equ_box_free_0) > 0.4 and iou_min(equ_box_gather_1, equ_box_free_1) > 0.4 and \
                                        iou_min(post_box_gather_0, post_box_free_0) > 0.4 and iou_min(post_box_gather_1, post_box_free_1) > 0.4:
                                    self.all_replace_gather_free(parallel_gather, parallel_free)

                                # 遮挡情况，大于某个值再替换
                                elif list(parallel_gather[0].values())[0]['frequency'] > 50:
                                    self.all_replace_gather_free(parallel_gather, parallel_free)
                                    break
                            # end--- 同一导线连接的两个器材的位置比较

                            # 匹配gather[0]的位置，找到接有两跟导线
                            elif list(parallel_gather[0].keys())[0].split('_')[0] in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]] and \
                                    list(parallel_gather[-1].keys())[0].split('_')[0] not in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]]:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(parallel_gather[0].keys())[0].split('_')[0] == list(parallel_free[-1].keys())[0].split('_')[0]:
                                    parallel_free.insert(0, parallel_free.pop(-1))  # 重新排序
                                post_box_gather = list(parallel_gather[0].values())[0]['post']
                                equ_box_gather = list(parallel_gather[0].values())[0]['equ']
                                post_box_free = list(parallel_free[0].values())[0]['post']

                                # 两个连接了导线的接线柱在器材两端, 新的接线柱与器材有交集
                                if iou_min(post_box_gather, post_box_free) > 0.4 and iou(equ_box_gather, post_box_free) > 0 and not list(parallel_gather[0].values())[0]['both']:  # 0.7 >=  > 0.4
                                    list(parallel_gather[0].values())[0]['both'] = True
                                    list(parallel_free[0].values())[0]['both'] = True
                                    route_fen = copy.deepcopy(parallel_route[0:parallel_route.index(parallel_gather)])
                                    route_fen.append(copy.deepcopy(parallel_free))
                                    self.flag8_parallel_route.append(route_fen)

                            # 匹配gather[-1]的位置，找到接有两跟导线
                            elif list(parallel_gather[0].keys())[0].split('_')[0] not in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]] and \
                                    list(parallel_gather[-1].keys())[0].split('_')[0] in [list(parallel_free[0].keys())[0].split('_')[0], list(parallel_free[-1].keys())[0].split('_')[0]]:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(parallel_gather[-1].keys())[0].split('_')[0] == list(parallel_free[-1].keys())[0].split('_')[0]:
                                    parallel_free.insert(0, parallel_free.pop(-1))
                                post_box_gather = list(parallel_gather[-1].values())[0]['post']
                                post_box_free = list(parallel_free[0].values())[0]['post']
                                equ_box_gather = list(parallel_gather[-1].values())[0]['equ']

                                # 不分路线  接线柱依次顺序连接
                                if iou_min(post_box_gather, post_box_free) < 0.2 and iou(equ_box_gather, post_box_free) > 0 and parallel_route[-1] is parallel_gather:
                                    parallel_route.append(parallel_free)

                                # 匹配gather[-1]的位置，gather[-1]不是parallel_gather的最后一个，找到接有两跟导线
                                elif iou_min(post_box_gather, post_box_free) > 0.4 and iou(equ_box_gather, post_box_free) > 0 and not list(parallel_gather[-1].values())[0]['both']:  # 0.7 >=  > 0.4
                                    list(parallel_gather[-1].values())[0]['both'] = True
                                    list(parallel_free[0].values())[0]['both'] = True
                                    route_he = copy.deepcopy(parallel_route[0:parallel_route.index(parallel_gather) + 1])
                                    route_he.append(copy.deepcopy(parallel_free))
                                    self.flag8_parallel_route.append(route_he)

                    # 记数出现频率
                    list(parallel_gather[0].values())[0]['frequency'] += 1

                # 首尾都是电压表，iou_min小于0.2，并联  len(dict)>=2, 电压表上两个接线柱iou_min<0.3
                if list(parallel_route[0][0].keys())[0].split('_')[0] == list(parallel_route[-1][-1].keys())[0].split('_')[0] and \
                        iou_min(list(parallel_route[0][0].values())[0]['post'], list(parallel_route[-1][-1].values())[0]['post']) < 0.5:
                    return [True, 'top']
        return [False, '']

    def point9_series(self, this_frame_terminals):
        # 从U+到U-，跳过V
        # 判断串联
        # 添加串联的器材
        series = copy.deepcopy(this_frame_terminals)

        if len(self.flag9_serie_route) == 0:  # 添加第一个连接的组合  从电压表出发
            for serie in series:
                if list(serie[0].keys())[0] in ['power_red', 'power_black'] or list(serie[-1].keys())[0] in ['power_red', 'power_black']:
                    if list(serie[-1].keys())[0] in ['power_red', 'power_black']:
                        serie.insert(0, serie.pop(serie.index(serie[-1])))  # 重新排序
                    self.flag9_serie_route.append([copy.deepcopy(serie)])
                    break

        if len(self.flag9_serie_route) != 0:  # 串联列表 [[],[],[]]
            # print(f'len(self.flag3_serie_route: {len(self.flag3_serie_route)}')
            for serie_route in self.flag9_serie_route:  # 单个路径在路径集合中
                # 如果第一个不是电源要清空clean
                if list(serie_route[0][0].keys())[0] not in ['power_red', 'power_black']:
                    self.flag9_serie_route.remove(serie_route)
                for serie_gather in serie_route:  # 这里的serie_gather只代表一根导线  for serie_gather in serie_route:
                    for serie_free in series:
                        if 'voltmeter' in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]]:
                            continue
                        if list(serie_gather[0].keys())[0].split('_')[0] in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]] or \
                                list(serie_gather[-1].keys())[0].split('_')[0] in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]]:
                            # 替换box  post的iou，equ的iou   同一导线连接的两个器材的位置比较
                            if list(serie_gather[0].keys())[0].split('_')[0] in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]] and \
                                    list(serie_gather[-1].keys())[0].split('_')[0] in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]]:
                                # 调整顺序
                                if list(serie_gather[0].keys())[0].split('_')[0] == list(serie_free[-1].keys())[0].split('_')[0]:
                                    serie_free.insert(0, serie_free.pop(-1))  # 重新排序
                                equ_box_gather_0 = list(serie_gather[0].values())[0]['equ']  # 已连接的器材，id为0
                                post_box_gather_0 = list(serie_gather[0].values())[0]['post']  # 已连接的接线柱，id为0
                                equ_box_gather_1 = list(serie_gather[-1].values())[0]['equ']  # 已连接的器材，id为1
                                post_box_gather_1 = list(serie_gather[-1].values())[0]['post']  # 已连接的接线柱，id为1
                                equ_box_free_0 = list(serie_free[0].values())[0]['equ']  # 待连接的器材，id为0
                                post_box_free_0 = list(serie_free[0].values())[0]['post']  # 待连接的接线柱，id为0
                                equ_box_free_1 = list(serie_free[-1].values())[0]['equ']  # 待连接的器材，id为1
                                post_box_free_1 = list(serie_free[-1].values())[0]['post']  # 待连接的接线柱，id为1

                                # 同一个目标直接替换
                                if iou_min(equ_box_gather_0, equ_box_free_0) > 0.4 and iou_min(equ_box_gather_1, equ_box_free_1) > 0.4 and \
                                        iou_min(post_box_gather_0, post_box_free_0) > 0.4 and iou_min(post_box_gather_1, post_box_free_1) > 0.4:
                                    self.all_replace_gather_free(serie_gather, serie_free)
                                    break

                                # 遮挡情况，大于某个值再替换
                                elif list(serie_gather[0].values())[0]['frequency'] > 50:
                                    self.all_replace_gather_free(serie_gather, serie_free)
                                    break
                            # end--- 同一导线连接的两个器材的位置比较

                            # 匹配gather[-1]的位置，找到接有两跟导线
                            elif list(serie_gather[0].keys())[0].split('_')[0] not in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]] and \
                                    list(serie_gather[-1].keys())[0].split('_')[0] in [list(serie_free[0].keys())[0].split('_')[0], list(serie_free[-1].keys())[0].split('_')[0]]:  # == list(parallel_free[0].keys())[0].split('_')[0]
                                # 调整顺序
                                if list(serie_gather[-1].keys())[0].split('_')[0] == list(serie_free[-1].keys())[0].split('_')[0]:
                                    serie_free.insert(0, serie_free.pop(-1))
                                post_box_gather = list(serie_gather[-1].values())[0]['post']
                                post_box_free = list(serie_free[0].values())[0]['post']
                                equ_box_gather = list(serie_gather[-1].values())[0]['equ']

                                # 不分路线  接线柱依次顺序连接
                                if iou_min(post_box_gather, post_box_free) < 0.2 and iou(equ_box_gather, post_box_free) > 0 and serie_route[-1] is serie_gather:
                                    serie_route.append(serie_free)

                    # 记数出现频率
                    list(serie_gather[0].values())[0]['frequency'] += 1

                # 首尾都是电源，接线柱不在同一位置
                if list(serie_route[0][0].keys())[0].split('_')[0] == list(serie_route[-1][-1].keys())[0].split('_')[0] and \
                        iou_min(list(serie_route[0][0].values())[0]['post'], list(serie_route[-1][-1].values())[0]['post']) < 0.5:
                    return [True, 'top']
        return [False, '']

    def point10_v_criterion(self, pointer_top, switch_top, voltmeter_top,
                            pointer_side, switch_side, voltmeter_side,
                            top_true, side_true):
        if top_true:
            criterion_num_top = 0
            # 找到与电压表相交的指针
            v_pointer_top = []
            if len(pointer_top) != 0 and len(voltmeter_top) != 0:
                for pointer_t in pointer_top:
                    if iou(pointer_t[:4], voltmeter_top[0][:4]) > 0:
                        if len(v_pointer_top) != 0 and v_pointer_top[4] < pointer_t[4]:
                            v_pointer_top.clear()
                        v_pointer_top += pointer_t
            if len(v_pointer_top) != 0 and self.class_name[int(v_pointer_top[5])] == 'pointer_offset_top':
                criterion_num_top += 1
            if switch_top.shape[0] != 0 and self.class_name[int(switch_top[0][5])] == 'switch_on_top':
                criterion_num_top += 1
            if criterion_num_top == 2:
                #     self.flag9_inertance_top += 1
                # if self.flag9_inertance_top > 1:
                return [True, 'top']

        if side_true and not self.scorePoint10:
            criterion_num_side = 0
            # 找到与电压表相交的指针
            v_pointer_side = []
            if len(pointer_side) != 0 and len(voltmeter_side) != 0:
                for pointer_s in pointer_side:
                    if iou(pointer_s[:4], voltmeter_side[0][:4]) > 0:
                        if len(v_pointer_side) != 0 and v_pointer_side[4] < pointer_s[4]:
                            v_pointer_side.clear()
                        v_pointer_side += pointer_s
            if len(v_pointer_side) != 0 and self.class_name[int(pointer_side[0][5])] == 'pointer_offset_top':
                criterion_num_side += 1
            if switch_side.shape[0] != 0 and self.class_name[int(switch_side[0][5])] == 'switch_on_top':
                criterion_num_side += 1
            if criterion_num_side == 2:
                #     self.flag9_inertance_side += 1
                # if self.flag9_inertance_side > 1:
                return [True, 'side']
        return [False, '']

    def point11_a_criterion(self, pointer_top, switch_top, ammeter_top,
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
                #     self.flag10_inertance_top += 1
                # if self.flag10_inertance_top > 1:
                return [True, 'top']

        if side_true and not self.scorePoint11:
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
                #     self.flag10_inertance_side += 1
                # if self.flag10_inertance_side > 1:
                return [True, 'side']
        return [False, '']

    def point12_gleithretter_site(self, following_top, connect_following_top, gleithretter_top, pointer_offset_top,
                                  slide_rheostat_side, gleithretter_side,
                                  slide_rheostat_front, gleithretter_front,
                                  top_true, side_true, front_true,):
        # 改变滑片位置 先求滑片、following连接线与following、connect_following连接线的夹角，
        # 再求相对水平时滑片到following的水平距离（垂直距离恒等），用位移来确定滑片位置发生改变
        if  top_true and following_top.shape[0] != 0 and connect_following_top.shape[0] != 0 and \
                gleithretter_top.shape[0] != 0 and pointer_offset_top.shape[0] != 0:
            following_top_box = following_top[0][:4]
            connect_following_top_box = connect_following_top[0][:4]
            gleithretter_top_box = gleithretter_top[0][:4]
            oa_rt = distance_box(following_top_box, gleithretter_top_box)
            ob_rt = distance_box(following_top_box, connect_following_top_box)
            ab_rt = distance_box(gleithretter_top_box, connect_following_top_box)
            coso_rt = (oa_rt * oa_rt + ob_rt * ob_rt - ab_rt * ab_rt) / (2 * oa_rt * ob_rt + 0.0001)
            dt = oa_rt * coso_rt
            # print(dt)
            if self.flag12_top_dt == 0:
                self.flag12_top_dt = dt
            else:
                delta_dt = abs(dt - self.flag12_top_dt)
                # print(self.flag11_top_dt, delta_dt)
                if delta_dt > 65:
                    self.flag12_inertance_top += 1
                    # print(self.flag11_inertance_top)
                if self.flag12_inertance_top > 5:
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
                self.flag12_inertance_side += 1
            if self.flag12_inertance_side > 3:
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
                self.flag12_inertance_front += 1
            if self.flag12_inertance_front > 3:
                return [True, 'front']
        return [False, '']

    def point13_switch_off(self, switch_top, pointer_top, ammeter_top, voltmeter_top,
                           pointer_side, switch_side, ammeter_side, voltmeter_side,
                           this_frame_terminals, top_true, side_true):
        if top_true and switch_top.shape[0] != 0 and \
                self.class_name[int(switch_top[0][5])] == 'switch_off_top' and \
                len(this_frame_terminals) >= 3:
            self.flag13_on_top += 1
        if self.flag13_on_top > 20:
            criterion_num_top = 0
            # 找到与电压表相交的指针
            a_pointer_top = []
            v_pointer_top = []
            if len(pointer_top) != 0 and (len(ammeter_top) != 0 or len(voltmeter_top) != 0):
                for pointer_t in pointer_top:
                    for item in [ammeter_top, voltmeter_top]:
                        if iou(pointer_t[:4], item[0][:4]) > 0:
                            if self.class_name[int(item[0][5])] == 'ammeter_top':
                                if len(a_pointer_top) != 0 and a_pointer_top[4] < pointer_t[4]:
                                    a_pointer_top.clear()
                                a_pointer_top += pointer_t
                            if self.class_name[int(item[0][5])] == 'voltmeter_top':
                                if len(v_pointer_top) != 0 and v_pointer_top[4] < pointer_t[4]:
                                    v_pointer_top.clear()
                                v_pointer_top += pointer_t

            if (len(a_pointer_top) != 0 or len(v_pointer_top) != 0) and \
                    (self.class_name[int(a_pointer_top[5])] == 'pointer_zero_top' or self.class_name[int(v_pointer_top[5])] == 'pointer_zero_top'):
                criterion_num_top += 1
            if switch_top.shape[0] != 0 and switch_side.shape[0] != 0 and self.class_name[int(switch_top[0][5])] == 'switch_off_top':
                criterion_num_top += 1
            if criterion_num_top == 2:
                self.flag13_inertance_top += 1
            if self.flag13_inertance_top > 15:
                return [True, 'top']

            if side_true and not self.scorePoint13:
                criterion_num_side = 0
                # 找到与电压表相交的指针
                a_pointer_side = []
                v_pointer_side = []
                if len(pointer_side) != 0 and (len(ammeter_side) != 0 or len(voltmeter_side) != 0):
                    for pointer_s in pointer_side:
                        for item in [ammeter_side, voltmeter_side]:
                            if iou(pointer_s[:4], item[0][:4]) > 0:
                                if self.class_name[int(item[0][5])] == 'ammeter_top':
                                    if len(a_pointer_side) != 0 and a_pointer_side[4] < pointer_s[4]:
                                        a_pointer_side.clear()
                                    a_pointer_side += pointer_s
                                if self.class_name[int(item[0][5])] == 'voltmeter_top':
                                    if len(v_pointer_side) != 0 and v_pointer_side[4] < pointer_s[4]:
                                        v_pointer_side.clear()
                                    v_pointer_side += pointer_s
                if (len(a_pointer_side) != 0 or len(v_pointer_side) != 0) and \
                    (self.class_name[int(a_pointer_side[5])] == 'pointer_zero_top' or self.class_name[int(v_pointer_side[5])] == 'pointer_zero_top'):
                    criterion_num_side += 1
                if switch_side.shape[0] != 0 and self.class_name[int(switch_side[0][5])] == 'switch_off_top':
                    criterion_num_side += 1
                if criterion_num_side == 2:
                    self.flag13_inertance_side += 1
                if self.flag13_inertance_side > 3:
                    return [True, 'side']
        return [False, '']

    def point14_clean(self, power_source_top, switch_top, ammeter_top,
                      slide_rheostat_top, fixed_resistor_top, voltmeter_top,
                      clean_desk_top, clean_desk_side, clean_desk_front,
                      top_true, side_true, front_true):
        in_center_box = False
        if top_true:
            for items in [power_source_top, switch_top, ammeter_top, slide_rheostat_top, fixed_resistor_top, voltmeter_top]:
                for item in items:
                    item_box = item[:4]
                    if iou(item_box, self.center_box) > 0:
                        in_center_box = True
                        break
                if in_center_box:
                    break

            if not in_center_box or clean_desk_top.shape[0] != 0:
                self.flag14_inertance_top += 1
                # if self.flag14_inertance_top > 5:
                return [True, 'top']
        elif side_true and clean_desk_side.shape[0] != 0:
            return [True, 'side']
        elif front_true and clean_desk_front.shape[0] != 0:
            return [True, 'front']
        return [False, '']