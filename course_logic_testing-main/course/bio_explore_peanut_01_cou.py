#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04
# @Author  : Qinhe
# @File    : bio_explore_peanut_01_cou.py


from .comm import *
from .comm.course_base import ConfigModel
import copy
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()


class BIO_explore_peanut(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(BIO_explore_peanut, self).__init__(*args, **kwargs)

        self.set_center_box = False  # 设置操作区域框
        self.center_box = None

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

        self.point_swich1 = True
        self.point_swich2 = False
        self.point_swich3 = False
        self.point_swich4 = False
        self.point_swich5 = False
        self.point_swich6 = False
        self.point_swich7 = False
        self.point_swich8 = False
        self.point_swich9 = False
        self.point_swich10 = False

        self.experiment_ing = False  # 正在做实验  判断拆除器材
        self.experiment_end = 0  # 器材完成拆除事件计数
        self.first_end = False  # 一次完整的实验

        self.point2_d = []

        self.flag1_inertance_top = 0
        self.flag1_inertance_side = 0
        self.flag1_inertance_front = 0
        self.flag2_inertance_top = 0
        self.flag2_inertance_side = 0
        self.flag2_inertance_front = 0
        self.flag3_inertance_top = 0
        self.flag3_inertance_side = 0
        self.flag3_inertance_front = 0
        self.flag4_inertance_top = 0
        self.flag4_inertance_side = 0
        self.flag4_inertance_front = 0
        self.flag5_inertance_top = 0
        self.flag5_inertance_side = 0
        self.flag5_inertance_front = 0
        self.flag6_inertance_top = 0
        self.flag6_inertance_side = 0
        self.flag6_inertance_front = 0
        self.flag7_inertance_top = 0
        self.flag7_inertance_side = 0
        self.flag7_inertance_front = 0
        self.flag8_inertance_top = 0
        self.flag8_inertance_side = 0
        self.flag8_inertance_front = 0
        self.flag9_inertance_top = 0
        self.flag9_inertance_side = 0
        self.flag9_inertance_front = 0
        self.flag10_inertance_top = 0
        self.flag10_inertance_side = 0
        self.flag10_inertance_front = 0

        self.clearn_desk_info = []  # 整理桌面信息

        self.class_name = ['big_peanut', 'little_peanut', 'beaker', 'take_peanut',
                           'ruler',
                           'triangle', 'use_triangle', 'wrong_use_triangle',
                           'one_measuring', 'two_measuring', \
                           'nonius', 'nonius_peanut', 'nonius_peanut_wrong',
                           'write', 'pen_hand', 'table',
                           'calculator', 'key_down', 'hand_calculator', 'clean']

    def score_process(self, top_true, front_true, side_true):
        if top_true or front_true or side_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分
            # [top_preds, side_preds, front1_preds], [top_img0, side_img0, front_img0] = preds, img0s # 检测框和ing

            if top_true:
                big_peanut_top, little_peanut_top, beaker_top, take_peanut_top, \
                ruler_top, triangle_top, use_triangle_top, wrong_use_triangle_top, \
                one_measuring_top, two_measuring_top, \
                nonius_top, nonius_peanut_top, nonius_peanut_wrong_top, \
                write_top, pen_hand_top, \
                table_top, calculator_top, \
                key_down_top, hand_calculator_top, clean_top = self.preds_top

                # 确定图片正反  #
                if not self.set_center_box and beaker_top.shape[0] != 0:
                    # h, w = self.top_img0.shape[:2]  todo
                    # 根据最开始器材在图片的位置确定操作区域
                    center_box_upright = torch.tensor([self.w_top * 0.33, self.h_top * 0.45, self.w_top * 0.72, self.h_top * 0.87], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
                    center_box_upend = torch.tensor([self.w_top * 0.28, self.h_top * 0.13, self.w_top * 0.67, self.h_top * 0.55], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面

                    binding_post = center_point(beaker_top[0][0:4])
                    self.center_box = center_box_upend if binding_post[1] > (self.h_top / 2) else center_box_upright
                    self.set_center_box = True


                peanuts_top = torch.cat([big_peanut_top, little_peanut_top], dim=0)
                # if switch_top.shape[0] != 0:
                #     switch_top = switch_top[torch.argsort(-switch_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                measure_top = torch.cat([use_triangle_top, wrong_use_triangle_top, one_measuring_top, two_measuring_top, nonius_peanut_top], dim=0)
                if measure_top.shape[0] != 0:
                    measure_top = measure_top[torch.argsort(-measure_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                key_top = torch.cat([key_down_top, hand_calculator_top], dim=0)
                if key_top.shape[0] != 0:
                    key_top = key_top[torch.argsort(-key_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                equipments_top = torch.cat([peanuts_top, beaker_top, take_peanut_top, ruler_top, triangle_top, nonius_top, key_top], dim=0)  #

            if side_true:
                big_peanut_side, little_peanut_side, beaker_side, take_peanut_side, \
                ruler_side, triangle_side, use_triangle_side, wrong_use_triangle_side, \
                one_measuring_side, two_measuring_side, \
                nonius_side, nonius_peanut_side, nonius_peanut_wrong_side, \
                write_side, pen_hand_side, \
                table_side, calculator_side, key_down_side, \
                hand_calculator_side, clean_side = self.preds_side

                peanuts_side = torch.cat([big_peanut_side, little_peanut_side], dim=0)
                # if hua_sheng_side.shape[0] != 0:
                #     hua_sheng_side = hua_sheng_side[torch.argsort(-hua_sheng_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                measure_side = torch.cat([use_triangle_side, wrong_use_triangle_side], dim=0)
                if measure_side.shape[0] != 0:
                    measure_side = measure_side[torch.argsort(-measure_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                key_side = torch.cat([key_down_side, hand_calculator_side], dim=0)
                if key_side.shape[0] != 0:
                    key_side = key_side[torch.argsort(-key_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

            if front_true:
                big_peanut_front, little_peanut_front, beaker_front, take_peanut_front, \
                ruler_front, triangle_front, use_triangle_front, wrong_use_triangle_front, \
                one_measuring_front, two_measuring_front, \
                nonius_front, nonius_peanut_front, nonius_peanut_wrong_front, \
                write_front, pen_hand_front, \
                table_front, calculator_front, key_down_front, \
                hand_calculator_front, clean_front = self.preds_front

                peanuts_front = torch.cat([big_peanut_front, little_peanut_front], dim=0)

                measure_front = torch.cat([use_triangle_front, wrong_use_triangle_front], dim=0)
                if measure_front.shape[0] != 0:
                    measure_front = measure_front[torch.argsort(-measure_front[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                key_front = torch.cat([key_down_front, hand_calculator_front], dim=0)
                if key_front.shape[0] != 0:
                    key_front = key_front[torch.argsort(-key_front[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

            if top_true:
                self.all_point_swich(peanuts_top, measure_top, key_down_top, hand_calculator_top)            # 判断是否已经完成一次实验操作  演示版用导线辅助判断
            # self.all_estimate_experiment_ing(wire_connection_top)  # todo 重置self.的变量

            # 1.随机选取花生果实得分，未随机选取的不得分
            if not self.scorePoint1 and "1" in self.exper_score_ids and self.point_swich1:
                point1view = self.point1(top_true, big_peanut_top, little_peanut_top, take_peanut_top, peanuts_top,
                                         side_true, big_peanut_side, little_peanut_side, take_peanut_side, peanuts_side,
                                         front_true, big_peanut_front, little_peanut_front, take_peanut_front, peanuts_front)
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

            # 2.在实验过程中，能正确使用实验用品
            if not self.scorePoint2 and "2" in self.exper_score_ids and self.point_swich2:
                point2view = self.point2(top_true, triangle_top, measure_top, peanuts_top, nonius_peanut_top,one_measuring_top, two_measuring_top,
                                         side_true, triangle_side, measure_side, peanuts_side, nonius_peanut_side,one_measuring_side, two_measuring_side,
                                         front_true, triangle_front, measure_front, peanuts_front, nonius_peanut_front,one_measuring_front, two_measuring_front)
                if point2view[0]:
                    self.scorePoint2 = True
                    if point2view[1] == 'top':
                        self.assignScore(2, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point2view[1] == 'side':
                        self.assignScore(2, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point2view[1] == 'front':
                        self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 3.用测量工具依次测量 3 枚大品种花生果实长轴的长度
            if not self.scorePoint3 and "3" in self.exper_score_ids and self.point_swich3:
                point3view = self.point3(top_true, triangle_top, measure_top, big_peanut_top, nonius_peanut_top,one_measuring_top, two_measuring_top,
                                         side_true, triangle_side, measure_side, big_peanut_side, nonius_peanut_side,one_measuring_side, two_measuring_side,
                                         front_true, triangle_front, measure_front, big_peanut_front, nonius_peanut_front,one_measuring_front, two_measuring_front)
                if point3view[0]:
                    self.scorePoint3 = True
                    if point3view[1] == 'top':
                        self.assignScore(3, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point3view[1] == 'side':
                        self.assignScore(3, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point3view[1] == 'front':
                        self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)
                    # plt.hist(self.point2_d,100)
                    # sns.kdeplot(self.point2_d, shade=True)
                    # plt.show()
                    # print(self.point2_d)


            # 4.用测量工具依次测量 3 枚小品种花生果实长轴的长度
            if not self.scorePoint4 and "4" in self.exper_score_ids and self.point_swich4:
                point4view = self.point4(top_true, triangle_top, measure_top, little_peanut_top, nonius_peanut_top,one_measuring_top, two_measuring_top,
                                         side_true, triangle_side, measure_side, little_peanut_side, nonius_peanut_side,one_measuring_side, two_measuring_side,
                                         front_true, triangle_front, measure_front, little_peanut_front, nonius_peanut_front,one_measuring_front, two_measuring_front)
                if point4view[0]:
                    self.scorePoint4 = True
                    if point4view[1] == 'top':
                        self.assignScore(4, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point4view[1] == 'side':
                        self.assignScore(4, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point4view[1] == 'front':
                        self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 5.将测量得到的数据如实记录在电子实验记录卡中
            # 默认得分  需要加一个限制条件
            if not self.scorePoint5 and "5" in self.exper_score_ids and self.point_swich5:
                point5view = self.point5(top_true, write_top,
                                         side_true, write_side,
                                         front_true, write_front)
                if point5view[0]:
                    self.scorePoint5 = True
                    if point5view[1] == 'top':
                        self.assignScore(5, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point5view[1] == 'side':
                        self.assignScore(5, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point5view[1] == 'front':
                        self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 6.利用计算器算出平均值，记录在电子实验记录卡中
            if not self.scorePoint6 and "6" in self.exper_score_ids and self.point_swich6:
                point6view = self.point6(top_true, key_top,
                                         side_true, key_side,
                                         front_true, key_front)
                if point6view[0]:
                    self.scorePoint6 = True
                    if point6view[1] == 'top':
                        self.assignScore(6, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point6view[1] == 'side':
                        self.assignScore(6, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point6view[1] == 'front':
                        self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 7.分析实验数据，推测花生果实大小变异的原因，选 B 得分
            # 默认得分  需要加一个限制条件
            if not self.scorePoint7 and "7" in self.exper_score_ids and self.point_swich7:
                point7view = self.point7(top_true, write_top,
                                         side_true, write_side,
                                         front_true, write_front)
                if point7view[0]:
                    self.scorePoint7 = True
                    if point7view[1] == 'top':
                        self.assignScore(7, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point7view[1] == 'side':
                        self.assignScore(7, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point7view[1] == 'front':
                        self.assignScore(7, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 8.分析实验数据，推测花生果实大小变异的原因，选 A 得分
            # 默认得分  需要加一个限制条件
            if not self.scorePoint8 and "8" in self.exper_score_ids and self.point_swich8:
                point8view = self.point8(top_true, write_top,
                                         side_true, write_side,
                                         front_true, write_front)
                if point8view[0]:
                    self.scorePoint8 = True
                    if point8view[1] == 'top':
                        self.assignScore(8, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point8view[1] == 'side':
                        self.assignScore(8, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point8view[1] == 'front':
                        self.assignScore(8, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

                # self.all_canvas_drow(parallel_gather)  # 绘制画布
                # self.show_process(canvas)

            # 9.将测量过的大、小品种果实分别放入原来的烧杯中， 其它实验用品归位，清洁桌面
            if not self.scorePoint9 and "9" in self.exper_score_ids and self.point_swich9:
                point9view = self.point9(top_true, clean_top, equipments_top,
                                         side_true, clean_side,
                                         front_true, clean_front)
                if point9view[0]:
                    self.scorePoint9 = True
                    if point9view[1] == 'top':
                        self.assignScore(9, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point9view[1] == 'side':
                        self.assignScore(9, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point9view[1] == 'front':
                        self.assignScore(9, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)
                    # sns.set()
                    # plt.plot(self.point2_d)
                    # a=sns.kdeplot(self.point2_d, shade=True)
                    # plt.show(a)
                    # print(self.point2_d)

            # 10.有序正确完成各步骤，确认提交电子实验记录卡
            # 默认得分  需要加一个限制条件
            if not self.scorePoint10 and "10" in self.exper_score_ids and self.point_swich10:
                point10view = self.point10(top_true, clean_top,
                                           side_true, clean_side,
                                           front_true, clean_front)
                if point10view[0]:
                    self.scorePoint10 = True
                    if point10view[1] == 'top':
                        self.assignScore(10, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point10view[1] == 'side':
                        self.assignScore(10, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point10view[1] == 'front':
                        self.assignScore(10, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

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

    def all_reorganization_frame(self, frame_num, frame1, frame2, frame3, frame4):
        """
        frames:需要合成图片的集合，frame的个数是需要合成的图片个数，frame的序列是摆放的位置
        """
        if frame_num == 2:
            pass

        elif frame_num == 3:
            pass

    def all_point_swich(self, peanuts_top, measure_top, key_down_top, hand_calculator_top):
        if not self.scorePoint1:
            self.point_swich1 = True

        if (not self.point_swich2 or not self.point_swich3 or not self.point_swich4) and peanuts_top.shape[0] != 0:
            self.point_swich2 = True
            self.point_swich3 = True
            self.point_swich4 = True

        self.point_swich5 = False

        if (not self.point_swich6 or not self.point_swich9) and peanuts_top.shape[0] != 0 and self.center_box is not None:
            for items in peanuts_top:
                item_box = items[:4]
                if iou(item_box, self.center_box) > 0:
                    self.point_swich6 = True
                    self.point_swich9 = True


        self.point_swich7 = False
        self.point_swich8 = False

        # if not self.point_swich9 and self.point_swich6 and (key_down_top.shape[0] != 0 or hand_calculator_top.shape[0] != 0):
        #     # print('key_down_top', key_down_top)
        #     # print('hand_calculator_top', hand_calculator_top)
        #     self.point_swich9 = True
        #     # print('self.point_swich9', self.point_swich9)

        self.point_swich10 = False


    def point1(self, top_true, big_peanut_top, little_peanut_top, take_peanut_top, peanuts_top,
               side_true, big_peanut_side, little_peanut_side, take_peanut_side, peanuts_side,
               front_true, big_peanut_front, little_peanut_front, take_peanut_front, peanuts_front):
        # 将取花生的图片、桌面有花生的图片二合一
        if top_true:
            if take_peanut_top.shape[0] != 0 and peanuts_top.shape[0] != 0:  #
                # print('take_peanut_top',  take_peanut_top)
                # print('big_peanut_top',  big_peanut_top)
                # print('little_peanut_top',  little_peanut_top)
                # print('peanuts_top',  peanuts_top)
                self.flag1_inertance_top += 1
                if self.flag1_inertance_top > 1:
                    return [True, 'top']
            elif big_peanut_top.shape[0] != 0 and little_peanut_top.shape[0] != 0:  #
                # print('take_peanut_top',  take_peanut_top)
                # print('big_peanut_top',  big_peanut_top)
                # print('little_peanut_top',  little_peanut_top)
                # print('peanuts_top',  peanuts_top)
                self.flag1_inertance_top += 1
                if self.flag1_inertance_top > 5:
                    return [True, 'top']
        if side_true:
            if take_peanut_side.shape[0] != 0 and peanuts_side.shape[0] != 0:
                # print('take_peanut_side,', take_peanut_side)
                # print('big_peanut_side,', big_peanut_side)
                # print('little_peanut_side,', little_peanut_side)
                # print('peanuts_side,', peanuts_side)
                self.flag1_inertance_side += 1
                if self.flag1_inertance_side > 1:
                    return [True, 'side']
            elif big_peanut_side.shape[0] != 0 and little_peanut_side.shape[0] != 0:
                # print('take_peanut_side,', take_peanut_side)
                # print('big_peanut_side,', big_peanut_side)
                # print('little_peanut_side,', little_peanut_side)
                # print('peanuts_side,', peanuts_side)
                self.flag1_inertance_side += 1
                if self.flag1_inertance_side > 1:
                    return [True, 'side']
        if front_true:
            if take_peanut_front.shape[0] != 0 and peanuts_front.shape[0] != 0:
                # print('take_peanut_front', take_peanut_front)
                # print('big_peanut_front', big_peanut_front)
                # print('little_peanut_front', little_peanut_front)
                # print('peanuts_front', peanuts_front)
                self.flag1_inertance_front += 1
                if self.flag1_inertance_front > 1:
                    return [True, 'front']
            elif big_peanut_front.shape[0] != 0 and little_peanut_front.shape[0] != 0:
                # print('take_peanut_front', take_peanut_front)
                # print('big_peanut_front', big_peanut_front)
                # print('little_peanut_front', little_peanut_front)
                # print('peanuts_front', peanuts_front)
                self.flag1_inertance_front += 1
                if self.flag1_inertance_front > 1:
                    return [True, 'front']
        return [False, '']

    def point2(self, top_true, triangle_top, measure_top, peanuts_top, nonius_peanut_top,one_measuring_top, two_measuring_top,
               side_true, triangle_side, measure_side, peanuts_side, nonius_peanut_side,one_measuring_side, two_measuring_side,
               front_true, triangle_front, measure_front, peanuts_front, nonius_peanut_front, one_measuring_front, two_measuring_front):
        # 需要判断两只三角板平行  单个三角板的宽度做统计  要求在正确使用的情况下
        # 花生与使用三角板有交集，确定在测量中
        if top_true and peanuts_top.shape[0] != 0:
            if measure_top.shape[0] != 0 and self.class_name[int(measure_top[0][5])] == 'use_triangle':
                # 花生与使用三角板有交集
                measure_top_box = measure_top[0][:4]
                # for tri_top in triangle_top:
                #     triangle_top_box = tri_top[:4]
                #     if iou(measure_top_box, triangle_top_box) > 0:
                #         self.point2_d.append(int(abs(triangle_top_box[0]-triangle_top_box[3])))

                for peanut_top in peanuts_top:
                    peanut_top_box = peanut_top[:4]
                    if iou(measure_top_box, peanut_top_box) > 0:
                        # print('triangle_top',  triangle_top)
                        # print('measure_top',  measure_top)
                        # print('peanuts_top',  peanuts_top)
                        self.flag2_inertance_top += 1
                        if self.flag2_inertance_top > 1:
                            return [True, 'top']

            # elif nonius_peanut_top.shape[0] != 0 and self.class_name[int(nonius_peanut_top[5])] == 'nonius_peanut':
            #     self.flag2_inertance_top += 1
            #     if self.flag2_inertance_top > 1:
            #         return [True, 'top']
                # # 花生与使用三角板有交集
                # nonius_peanut_top_box = nonius_peanut_top[0][:4]
                # # for tri_top in triangle_top:
                # #     triangle_top_box = tri_top[:4]
                # #     if iou(measure_top_box, triangle_top_box) > 0:
                # #         self.point2_d.append(int(abs(triangle_top_box[0]-triangle_top_box[3])))
                #
                # for peanut_top in peanuts_top:
                #     peanut_top_box = peanut_top[:4]
                #     if iou(nonius_peanut_top_box, peanut_top_box) > 0:
                #         # print('triangle_top',  triangle_top)
                #         # print('measure_top',  measure_top)
                #         # print('peanuts_top',  peanuts_top)
                #         self.flag2_inertance_top += 1
                #         if self.flag2_inertance_top > 1:
                #             return [True, 'top']
            elif nonius_peanut_top.shape[0] != 0 or one_measuring_top.shape[0] != 0 or two_measuring_top.shape[0] != 0:
                self.flag2_inertance_top += 1
                if self.flag2_inertance_top > 1:
                    return [True, 'top']

        # elif side_true and peanuts_side.shape[0] != 0 and measure_side.shape[0] != 0 and self.class_name[int(measure_side[0][5])] == 'use_triangle':
        #     measure_side_box = measure_side[0][:4]
        #     for peanut_side in peanuts_side:
        #         peanut_side_box = peanut_side[:4]
        #         if iou(measure_side_box, peanut_side_box) > 0:
        #             print('triangle_side,', triangle_side)
        #             print('measure_side,', measure_side)
        #             print('peanuts_side,', peanuts_side)
        #             self.flag2_inertance_side += 1
        #             if self.flag2_inertance_side > 1:
        #                 return [True, 'side']

        elif front_true and peanuts_front.shape[0] != 0:
            if measure_front.shape[0] != 0 and self.class_name[int(measure_front[0][5])] == 'use_triangle':

                measure_front_box = measure_front[0][:4]
                for peanut_front in peanuts_front:
                    peanut_front_box = peanut_front[:4]
                    if iou(measure_front_box, peanut_front_box) > 0:
                        # print('triangle_front', triangle_front)
                        # print('measure_front', measure_front)
                        # print('peanuts_front', peanuts_front)
                        self.flag2_inertance_front += 1
                        if self.flag2_inertance_front > 1:
                            return [True, 'front']
            # if nonius_peanut_front.shape[0] != 0 and self.class_name[int(nonius_peanut_front[5])] == 'nonius_peanut':
            #     self.flag2_inertance_front += 1
            #     if self.flag2_inertance_front > 1:
            #         return [True, 'side']
                # nonius_peanut_front_box = nonius_peanut_front[0][:4]
                # for peanut_front in peanuts_front:
                #     peanut_front_box = peanut_front[:4]
                #     if iou(nonius_peanut_front_box, peanut_front_box) > 0:
                #         # print('triangle_front', triangle_front)
                #         # print('measure_front', measure_front)
                #         # print('peanuts_front', peanuts_front)
                #         self.flag2_inertance_front += 1
                #         if self.flag2_inertance_front > 1:
                #             return [True, 'side']
            elif nonius_peanut_front.shape[0] != 0 or one_measuring_front.shape[0] != 0 or two_measuring_front.shape[0] != 0:
                self.flag2_inertance_front += 1
                if self.flag2_inertance_front > 1:
                    return [True, 'front']
        return [False, '']

    def point3(self, top_true, triangle_top, measure_top, big_peanut_top, nonius_peanut_top,one_measuring_top, two_measuring_top,
               side_true, triangle_side, measure_side, big_peanut_side, nonius_peanut_side,one_measuring_side, two_measuring_side,
               front_true, triangle_front, measure_front, big_peanut_front, nonius_peanut_front,one_measuring_front, two_measuring_front):
        # 三次测量组成一张图
        # 确定花生位置有变化
        # 测量的是大花生
        if top_true and big_peanut_top.shape[0] != 0:
            if measure_top.shape[0] != 0 and self.class_name[int(measure_top[0][5])] == 'use_triangle':
                # 大花生与使用三角板有交集
                measure_top_box = measure_top[0][:4]
                for big_top in big_peanut_top:
                    big_top_box = big_top[:4]
                    if iou(measure_top_box, big_top_box) > 0:
                        self.flag3_inertance_top += 1
                        # if self.flag3_inertance_top > 1:
                        return [True, 'top']

            elif nonius_peanut_top.shape[0] != 0 or one_measuring_top.shape[0] != 0 or two_measuring_top.shape[0] != 0:
                self.flag3_inertance_top += 1
                # if self.flag3_inertance_top > 1:
                return [True, 'top']


        # elif side_true and big_peanut_side.shape[0] != 0 and measure_side.shape[0] != 0 and self.class_name[int(measure_side[0][5])] == 'use_triangle':
        #     measure_side_box = measure_side[0][:4]
        #     for big_side in big_peanut_side:
        #         big_side_box = big_side[:4]
        #         if iou(measure_side_box, big_side_box) > 0:
        #             self.flag3_inertance_side += 1
        #             if self.flag3_inertance_side > 17:
        #                 return [True, 'side']

        elif front_true and big_peanut_front.shape[0] != 0:
            if measure_front.shape[0] != 0 and self.class_name[int(measure_front[0][5])] == 'use_triangle':
                measure_front_box = measure_front[0][:4]
                for big_front in big_peanut_front:
                    big_front_box = big_front[:4]
                    if iou(measure_front_box, big_front_box) > 0:
                        self.flag3_inertance_front += 1
                        # if self.flag3_inertance_front > 1:
                        return [True, 'front']
            elif nonius_peanut_front.shape[0] != 0 or one_measuring_front.shape[0] != 0 or two_measuring_front.shape[0] != 0:
                self.flag3_inertance_front += 1
                # if self.flag3_inertance_front > 1:
                return [True, 'front']

        return [False, '']

    def point4(self, top_true, triangle_top, measure_top, little_peanut_top, nonius_peanut_top,one_measuring_top, two_measuring_top,
               side_true, triangle_side, measure_side, little_peanut_side, nonius_peanut_side,one_measuring_side, two_measuring_side,
               front_true, triangle_front, measure_front, little_peanut_front, nonius_peanut_front,one_measuring_front, two_measuring_front):
        # 三次测量组成一张图
        # 确定花生位置有变化  追踪
        # 测量的是小花生
        if top_true and little_peanut_top.shape[0] != 0:
            if measure_top.shape[0] != 0 and self.class_name[int(measure_top[0][5])] == 'use_triangle':
                # 小花生与使用三角板有交集
                measure_top_box = measure_top[0][:4]
                for little_top in little_peanut_top:
                    little_top_box = little_top[:4]
                    if iou(measure_top_box, little_top_box) > 0:
                        self.flag4_inertance_top += 1
                        # if self.flag4_inertance_top > 1:
                        return [True, 'top']
            elif nonius_peanut_top.shape[0] != 0 or one_measuring_top.shape[0] != 0 or two_measuring_top.shape[0] != 0:
                self.flag4_inertance_top += 1
                if self.flag4_inertance_top > 3:
                    return [True, 'top']

        # elif side_true and little_peanut_side.shape[0] != 0 and measure_side.shape[0] != 0 and self.class_name[int(measure_side[0][5])] == 'use_triangle':
        #     measure_side_box = measure_side[0][:4]
        #     for little_side in little_peanut_side:
        #         little_side_box = little_side[:4]
        #         if iou(measure_side_box, little_side_box) > 0:
        #             self.flag4_inertance_side += 1
        #             if self.flag4_inertance_side > 9:
        #                 return [True, 'side']

        elif front_true and little_peanut_front.shape[0] != 0:
            if measure_front.shape[0] != 0 and self.class_name[int(measure_front[0][5])] == 'use_triangle':
                measure_front_box = measure_front[0][:4]
                for little_front in little_peanut_front:
                    little_front_box = little_front[:4]
                    if iou(measure_front_box, little_front_box) > 0:
                        self.flag4_inertance_front += 1
                        # if self.flag4_inertance_front > 1:
                        return [True, 'front']
            elif nonius_peanut_front.shape[0] != 0 or one_measuring_front.shape[0] != 0 or two_measuring_front.shape[0] != 0:
                self.flag4_inertance_front += 1
                if self.flag4_inertance_front > 3:
                    return [True, 'front']
        return [False, '']

    def point5(self, top_true, write_top,
               side_true, write_side,
               front_true, write_front):
        return [True, '']

    def point6(self, top_true, key_top,
               side_true, key_side,
               front_true, key_front):
        if top_true and key_top.shape[0] != 0 and self.class_name[int(key_top[0][5])] == 'key_down':
            self.flag6_inertance_top += 1
            # if self.flag6_inertance_top > 1:
            return [True, 'top']

        elif side_true and key_side.shape[0] != 0 and self.class_name[int(key_side[0][5])] == 'key_down':
            self.flag6_inertance_side += 1
            # if self.flag6_inertance_side > 1:
            return [True, 'side']

        elif front_true and key_front.shape[0] != 0 and self.class_name[int(key_front[0][5])] == 'key_down':
            self.flag6_inertance_front += 1
            # if self.flag6_inertance_front > 1:
            return [True, 'front']
        return [False, '']

    def point7(self, top_true, write_top,
               side_true, write_side,
               front_true, write_front):
        return [True, '']

    def point8(self, top_true, write_top,
               side_true, write_side,
               front_true, write_front):
        return [True, '']

    def point9(self, top_true, clean_top, equipments_top,
               side_true, clean_side,
               front_true, clean_front):
        in_center_box = False
        if top_true:
            if self.center_box is not None:
                for items in equipments_top:
                    item_box = items[:4]
                    if iou(item_box, self.center_box) > 0:
                        in_center_box = True
                        break

            if not in_center_box or clean_top.shape[0] != 0:
                # print('clean_top', clean_top)
                self.flag9_inertance_top += 1
                # print('equipments_top', equipments_top)
                if self.flag9_inertance_top > 5:
                    return [True, 'top']
        elif side_true and clean_side.shape[0] != 0:
            return [True, 'side']
        elif front_true and clean_front.shape[0] != 0:
            return [True, 'front']
        return [False, '']

    def point10(self, top_true, clean_top,
                side_true, clean_side,
                front_true, clean_front):
        return [True, '']
