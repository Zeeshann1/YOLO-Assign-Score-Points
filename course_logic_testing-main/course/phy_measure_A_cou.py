#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : Qinhe
# @File    : phy_measure_A_cou.py

'''
用电流表测电流
'''

from .comm import *

class PHY_measure_A(ConfigModel):

    def __init__(self):
        super(PHY_measure_A, self).__init__()

        # 得分点标记
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False
        self.scorePoint8 = False

        self.ampere_meter_box = None  # 电流表位置
        self.switch_box = None  # 开关位置信息
        self.bulb_box = None  # 灯泡位置信息
        self.powers = None  # 电源位置信息

        self.graph = {'电源+': [],
                      '电源-': [],
                      '开关+': [],
                      '开关-': [],
                      '电流表+': [],
                      '电流表-': [],
                      '灯泡+': [],
                      '灯泡-': [],
                      }

        self.kgdk_secs = 0  # 开关断开时间
        self.kgdk_secs_pre = 0  #
        self.kgbh_secs = 0  # 开关闭合时间
        self.kgbh_secs_pre = 0

        self.clearn_secs = 0
        self.clearn_desk_info = []

    @property
    def post_(self):
        posted = set()
        for value in self.graph.values():
            for v in value:
                posted.add(v)
        return posted

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, *args):  # 赋分逻辑部分
        (s_tops, dy_tops, kgbh_tops, kgdk_tops, hsjxz_tops, hsjxz__tops, heisjxz_tops, heisjxz__tops, dxlj_tops,
        dlb_tops, zz0_tops, zz0kd_tops, xlc_tops, dlc_tops, dp_tops, dpl_tops) = self.preds_top
        (s_fronts, dy_fronts, kgbh_fronts, kgdk_fronts, hsjxz_fronts, hsjxz__fronts, heisjxz_fronts, heisjxz__fronts,
        dxlj_fronts, dlb_fronts, zz0_fronts, zz0kd_fronts, xlc_fronts, dlc_fronts, dp_fronts, dpl_fronts) = self.preds_front
        (s_sides, dy_sides, kgbh_sides, kgdk_sides, hsjxz_sides, hsjxz__sides, heisjxz_sides, heisjxz__sides,
        dxlj_sides, dlb_sides, zz0_sides, zz0kd_sides, xlc_sides, dlc_sides, dp_sides, dpl_sides) = self.preds_side

        if dlb_tops.shape[0] > 0:  # 记录电流表位置信息
            self.ampere_meter_box = dlb_tops[0][:4]
        if dp_tops.shape[0] > 0:  # 记录灯泡位置信息
            self.bulb_box = dp_tops[0][:4]
        if kgbh_tops.shape[0] > 0:
            self.switch_box = kgbh_tops[0][:4]
        elif kgdk_tops.shape[0] > 0:
            self.switch_box = kgdk_tops[0][:4]
        if dy_tops.shape[0] > 0:
            self.powers = dy_tops

        if dxlj_tops.shape[0] > 0:  # 导线连接
            for dxlj_top in dxlj_tops:
                dxlj_top_box = dxlj_top[:4]
                connections = self.associate(dxlj_top_box)  # 与导线连接的器件
                if len(connections) == 2:
                    r_1, b_1 = self.post_equip(connections[0][1], hsjxz__tops, heisjxz__tops, dxlj_top_box)  # 红黑接线柱
                    r_2, b_2 = self.post_equip(connections[1][1], hsjxz__tops, heisjxz__tops, dxlj_top_box)  # 红黑接线柱
                    if len(r_1) + len(b_1) > 0 and len(r_2) + len(b_2) > 0:
                        if connections[0][0] == '电流表' and connections[1][0] == '灯泡':
                            self.updateGraph(r_1, b_1, r_2, b_2, '电流表', '灯泡', dxlj_top_box)
                        elif connections[0][0] == '电流表' and connections[1][0] == '开关':
                            self.updateGraph(r_1, b_1, r_2, b_2, '电流表', '开关', dxlj_top_box)
                        elif connections[0][0] == '电流表' and connections[1][0] == '电源':
                            self.updateGraph(r_1, b_1, r_2, b_2, '电流表', '电源', dxlj_top_box)
                        elif connections[0][0] == '灯泡' and connections[1][0] == '开关':
                            self.updateGraph(r_1, b_1, r_2, b_2, '灯泡', '开关', dxlj_top_box)
                        elif connections[0][0] == '灯泡' and connections[1][0] == '电源':
                            self.updateGraph(r_1, b_1, r_2, b_2, '灯泡', '电源', dxlj_top_box)
                        elif connections[0][0] == '开关' and connections[1][0] == '电源':
                            self.updateGraph(r_1, b_1, r_2, b_2, '开关', '电源', dxlj_top_box)


        if not self.scorePoint1 and dxlj_tops.shape[0] > 1:  # 至少了连接两个导线
            if kgdk_tops.shape[0] > 0 or kgdk_fronts.shape[0] or kgdk_sides.shape[0] > 0:
                self.kgdk_secs, self.kgdk_secs_pre, flag = self.duration(self.kgdk_secs, 1, self.kgdk_secs_pre, 0.5)
                if flag:
                    self.assignScore(1, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    # self.faultyOperation(1, '错误1', self.top_img0, self.top_preds, 1)

        if not self.scorePoint2: # 电源、开关、小灯泡、电流表串联
            if self.in_series():
                self.assignScore(2, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                # self.faultyOperation(2, '错误2', self.top_img0, self.top_preds, 1)

        if not self.scorePoint3: # '电流从电流表的”+“接线柱流入，”-“接线柱流出'
            if self.A_P_N():
                self.assignScore(3, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                # self.faultyOperation(3, '错误3', self.top_img0, self.top_preds, 2)

        # 开关闭合 偏转 (在所有电路连接后)
        if not self.scorePoint4 and self.scorePoint2:
            if kgbh_tops.shape[0] > 0:
                self.kgbh_secs, self.kgbh_secs_pre, flag = self.duration(self.kgbh_secs, 1, self.kgbh_secs_pre, 0.3)
                if flag:
                    self.assignScore(4, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

        if not self.scorePoint4 and dpl_tops.shape[0] > 0:  # 闭合开关，指针偏转
            self.assignScore(4, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

        if not self.scorePoint5:  # 选择合适量程
            info = self.lchs(5, hsjxz__tops, heisjxz__tops, hsjxz_tops)
            if info is not None:
                self.assignScore(*info)

        top_items = [dy_tops, kgbh_tops, kgdk_tops, dlb_tops, dp_tops, hsjxz_tops, heisjxz_tops]
        if not self.scorePoint6 and len(self.score_list) > 1:  # 断开开关，拆除电路，整理实验器材
            info = self.clearn_desk(6, [top_items])
            if info is not None:
                self.assignScore(*info)

        if self.scorePoint6 and len(self.score_list) != 6:
            if not self.desk_is_clearn([top_items], [self.center_area_top]):
                self.retracementScore(6)

    def in_series(self):  # 判断串联
        devicees = set()
        next_post = '电源+'
        devicees.add(next_post[:-1])
        r_n = 0
        while next_post and r_n < 5:
            if len(self.graph[next_post]) == 1:
                next_post = self.graph[next_post][0]  # type:str
                devicees.add(next_post[:-1])
                if next_post == '电源-' and len(devicees) == 4:
                    return True
                if next_post.endswith('+'):
                    next_post = next_post.replace('+', '-')
                else:
                    next_post = next_post.replace('-', '+')
            else:
                return
            r_n += 1

    def A_P_N(self):  # 电流表电流正极进负极出
        next_post = '电源+'
        r_n = 0
        while next_post and r_n < 5:
            if len(self.graph[next_post]) == 1:
                next_post = self.graph[next_post][0]  # type:str
                if next_post.endswith('+'):
                    next_post = next_post.replace('+', '-')
                else:
                    next_post = next_post.replace('-', '+')
                if next_post == '电流表-' and len(self.graph[next_post]) == 1:
                    return True
            else:
                return
            r_n += 1

    def updateGraph(self, r_1, b_1, r_2, b_2, label1, label2, dxlj_top_box):
        if label1 == '电流表':
            if ((len(r_1) == 1 and len(b_1) == 0) or
                (len(r_1) == 1 and len(b_1) == 1 and
                 '电流表-' in self.post_ and
                 '电流表+' not in self.post_)):  # 导线连接与红接线柱 +
                self.updateGraph_(r_2, b_2, f'{label1}+', label2, dxlj_top_box)
            elif ((len(r_1) == 0 and len(b_1) == 1) or
                  (len(r_1) == 1 and len(b_1) == 1 and
                 '电流表-' not in self.post_ and
                 '电流表+' in self.post_)):  # 导线连接与黑接线柱
                self.updateGraph_(r_2, b_2, f'{label1}-', label2, dxlj_top_box)
        else:
            if ((len(r_1) == 1 and len(b_1) == 0) or
                    (len(r_1) == 1 and len(b_1) == 1 and
                     iou(dxlj_top_box, r_1[0]) > 0 and
                     iou(dxlj_top_box, b_1[0]) == 0)):  # 导线连接与红接线柱 +
                self.updateGraph_(r_2, b_2, f'{label1}+', label2, dxlj_top_box)
            elif ((len(r_1) == 0 and len(b_1) == 1) or
                  (len(r_1) == 1 and len(b_1) == 1 and
                   iou(dxlj_top_box, r_1[0]) == 0 and
                   iou(dxlj_top_box, b_1[0]) > 0)):  # 导线连接与黑接线柱
                self.updateGraph_(r_2, b_2, f'{label1}-', label2, dxlj_top_box)

    def updateGraph_(self, r_2, b_2, label1, label2, dxlj_top_box):
        if (len(r_2) == 1 and len(b_2) == 0) or \
                (len(r_2) == 1 and len(b_2) == 1 and
                 iou(dxlj_top_box, r_2[0]) > 0 and
                 iou(dxlj_top_box, b_2[0]) == 0):  # 导线连接与红接线柱

            if (f'{label2}+' not in self.graph[label1] and
                    label1 not in self.graph[f'{label2}+'] and
                    len(self.graph[label1]) == 0 and
                    len(self.graph[f'{label2}+']) == 0):
                self.graph[label1].append(f'{label2}+')
                self.graph[f'{label2}+'].append(label1)
        elif (len(r_2) == 0 and len(b_2) == 1) or \
                (len(r_2) == 1 and len(b_2) == 1 and
                 iou(dxlj_top_box, r_2[0]) == 0 and
                 iou(dxlj_top_box, b_2[0]) > 0):  # 导线连接与黑接线柱
            if (f'{label2}-' not in self.graph[label1] and
                    label1 not in self.graph[f'{label2}-'] and
                    len(self.graph[label1]) == 0 and
                    len(self.graph[f'{label2}-']) == 0):
                self.graph[label1].append(f'{label2}-')
                self.graph[f'{label2}-'].append(label1)

    def associate(self, dxlj_top_box):  # 返回与导线连接的器件
        connections = []
        if self.ampere_meter_box is not None and iou(dxlj_top_box, self.ampere_meter_box) > 0:
            connections.append(('电流表', self.ampere_meter_box))
        if self.bulb_box is not None and iou(dxlj_top_box, self.bulb_box) > 0:
            connections.append(('灯泡', self.bulb_box))
        if self.switch_box is not None and iou(dxlj_top_box, self.switch_box) > 0:
            connections.append(('开关', self.switch_box))
        if self.powers is not None:
            for power in self.powers:
                power_box = power[:4]
                if iou(dxlj_top_box, power_box) > 0:
                    connections.append(('电源', power_box))
        return connections

    def post_equip(self, equip_box, hsjxz__tops, heisjxz__tops, dxlj_top_box):  # 返回与在器件内的接线柱
        binding_post_r = []
        binding_post_b = []
        for post in hsjxz__tops:
            post_box = post[:4]
            if iou(post_box, equip_box) > 0 and min_dis_boxes(dxlj_top_box, post_box) < self.h_top * 0.028:
                binding_post_r.append(post_box)
        for post in heisjxz__tops:
            post_box = post[:4]
            if iou(post_box, equip_box) > 0 and min_dis_boxes(dxlj_top_box, post_box) < self.h_top * 0.028:
                binding_post_b.append(post_box)
        return binding_post_r, binding_post_b

    # 5 量程合适
    def lchs(self, score_index, hsjxz__tops, heisjxz__tops, hsjxz_tops):
        ampere_meter_r_ = []  # 电流表红色接线柱连接
        ampere_meter_r = []  # 电流表红色接线柱
        ampere_meter_b_ = []  # 电流表黑色接线柱连接
        if self.ampere_meter_box is not None \
                and hsjxz__tops.shape[0] > 0 \
                and heisjxz__tops.shape[0] > 0 \
                and hsjxz_tops.shape[0] > 0:
            for hsjxz__top in hsjxz__tops:
                hsjxz__top_box = hsjxz__top[:4]
                if box1_in_box2(hsjxz__top_box, self.ampere_meter_box):
                    ampere_meter_r_.append(('r_', center_point(hsjxz__top_box)))
            if len(ampere_meter_r_) == 1:  # 电流表一个红色接线柱连接
                for hsjxz_top in hsjxz_tops:
                    hsjxz_top_box = hsjxz_top[:4]
                    if box1_in_box2(hsjxz_top_box, self.ampere_meter_box):
                        ampere_meter_r.append(('r', center_point(hsjxz_top_box)))
            if len(ampere_meter_r) == 1:  # 电流表一个共色接线柱未连接
                for heisjxz__top in heisjxz__tops:
                    heisjxz__top_box = heisjxz__top[:4]
                    if box1_in_box2(heisjxz__top_box, self.ampere_meter_box):
                        ampere_meter_b_.append(('b', center_point(heisjxz__top_box)))
            if len(ampere_meter_b_) == 1:  # 电流表黑色接线柱连接
                binding_post = ampere_meter_r_ + ampere_meter_r + ampere_meter_b_  # 电流表接线柱
                binding_post_h = sorted(binding_post, key=lambda x: x[1][0])  # 以接线柱框中心x排序
                binding_post_v = sorted(binding_post, key=lambda x: x[1][0])  # 以接线柱框中心y排序
                if binding_post_h[-1][1][0] - binding_post_h[0][1][0] > \
                        binding_post_v[-1][1][0] - binding_post_v[0][1][0]:  # 三个接线柱取向水平
                    if binding_post_h[1][0] == 'r_':  # 中间为红色接线柱 小量程
                        return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top
                    else:  # 大量程
                        pass
                else:
                    if binding_post_v[1][0] == 'r_':  # 中间为红色接线柱 小量程
                        return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top
                    else:  # 大量程
                        pass

    # 6 整理桌面
    def clearn_desk(self, score_index, top_items):
        if self.desk_is_clearn(top_items, [self.center_area_top]):
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_secs, _, flag = self.duration(self.clearn_secs, 2)
            if flag:
                self.clearn_secs = 0
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top
        else:
            self.clearn_secs = 0

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info[:6])
            return True
