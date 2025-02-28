#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/02/26 17:18
# @Author  : lld
# @File    : phy_salver_balance_measure_mass_cou.py

"""

V2.0更新
1.解决天平摆放位置太偏只能检测到一个螺母问题
2.优化得分点1和3平衡条件
3.可能会出现得分点1和3提前出的问题

"""
from .comm import *
from .comm.course_base import ConfigModel



class PHY_salver_balance_measure_mass(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(PHY_salver_balance_measure_mass, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False

        self.set_cursor_zero_flag = False  # 游码置0

        self.set_nut_balance_flag = False  # 螺母调平
        self.set_cursor_zero_first = 0
        self.set_cursor_zero_last = 0
        self.set_zero_balance_first = 0  # 调0平衡
        self.set_zero_balance_last = 0
        self.set_zero_balance_first1 = 0  # 调0平衡
        self.set_zero_balance_last1 = 0
        self.set_zero_balance_first2 = 0  # 调0平衡
        self.set_zero_balance_last2 = 0
        self.set_zero_balance_first0 = 0  # 调0平衡
        self.set_zero_balance_last0 = 0
        self.set_zero_balance_first3 = 0  # 调0平衡
        self.set_zero_balance_last3 = 0

        self.add_metal_flag = False  # 加金属
        self.add_weight_flag = False  # 加砝码
        self.left_object_right_weight_first = 0  # 左物右码
        self.left_object_right_weight_last = 0

        self.set_salver_balance_flag = False  # 天平平衡
        self.set_salver_balance_first = 0  # 天平平衡
        self.set_salver_balance_last = 0
        self.set_tweezers_cursors_info = []
        self.set_tweezers_cursors_flag = False

        self.clean_time = 0
        self.clean_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        hands_front, heads_front, eyes_front, dusters_front, clean_desks_front, salvers_front, weight_tweezers_front, \
        nuts_front, metal_blocks_front, weights_front, weight_boxs_front, salver_balances_front, cursors_front = self.preds_front

        hands_top, heads_top, eyes_top, dusters_top, clean_desks_top, salvers_top, weight_tweezers_top, nuts_top, \
        metal_blocks_top, weights_top, weight_boxs_top, salver_balances_top, cursors_top, = self.preds_top

        front_items = [salver_balances_front]
        top_items = [salver_balances_top]

        # 如果未得到得分点，则执行函数。
        # 1.能正确把游码移到标尺的零刻度处。
        if not self.scorePoint1 and not self.scorePoint3 and not self.scorePoint4:
            # if self.cursor_set_zero(nuts_front, salver_balances_front, weight_tweezers_front, cursors_front,
            #                         metal_blocks_top, salver_balances_top, weight_tweezers_top, salvers_top):
            if self.cursor_set_zero(weight_tweezers_front, salver_balances_front, cursors_top, cursors_front,
                                    metal_blocks_top, salver_balances_top, weight_tweezers_top, salvers_top,
                                    weights_front, weights_top):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.并根据指针偏向情况，调节平衡螺母使天平平衡。
        if not self.scorePoint2 and not self.scorePoint3 and not self.scorePoint4 and \
                not self.scorePoint5 :
            if self.nut_balance(salvers_front, metal_blocks_front, salver_balances_top, salver_balances_front, cursors_front,
                                weights_front, hands_front):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.能正确在左盘放被测物，右盘放砝码。
        if not self.scorePoint3:
            if self.left_object_right_weight(salver_balances_front, salvers_front, weight_tweezers_front,
                                             metal_blocks_front, weights_front, salver_balances_top, salvers_top,
                                             weight_tweezers_top,  metal_blocks_top, weights_top):
                self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
                self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 4.能用镊子由大到小放置砝码，轻拿轻放。
        if not self.scorePoint4:
            if self.set_weight(salvers_front, metal_blocks_front, weight_tweezers_front, weights_front, hands_front,
                               salver_balances_front, salvers_top, metal_blocks_top, weight_tweezers_top, weights_top,
                               hands_top, salver_balances_top):
                self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 5.称量时会根据指针偏向情况，通过加减砝码或移动游码使天平平衡，并正确读出物体质量的数据。
        if not self.scorePoint5:
            if self.set_salver_balance(salvers_front, salver_balances_front, metal_blocks_front, weights_front,
                                       nuts_front, cursors_top, salver_balances_top, weight_tweezers_top, salvers_top,
                                       weight_tweezers_front):
                self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 6.实验结束后能及时整理器材。
        if not self.scorePoint6 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3 or self.scorePoint4 or
                                     self.scorePoint5):
            self.clean_desk(6, top_items, front_items)
        if self.scorePoint6 and len(self.score_list) != 6:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(6)

    # 1.能正确把游码移到标尺的零刻度处。

    def cursor_set_zero(self, weight_tweezers_front, salver_balances_front, cursors_top, cursors_front,
                        metal_blocks_top, salver_balances_top, weight_tweezers_top, salvers_top, weights_front, weights_top):
#         # print("步骤1开始赋分")
        # 前视
        if not self.set_cursor_zero_flag:  # 游码未置0
            if salver_balances_front.shape[0] != 0 and salver_balances_top.shape[0] != 0 \
                    and weights_front.shape[0] == 0 and weights_top.shape[0] == 0:
                # 托盘天平、平衡螺母存在
                salver_balance_front_box = salver_balances_front[0][:4]  # 取托盘天平的xyxy
                salver_balance_top_box = salver_balances_top[0][:4]
                if salver_balance_top_box[1] > 0.01 * self.h_front:
#                     # print("天平位置摆放正确")
                    if cursors_top.shape[0] != 0:  # 顶视游码存在
#                         # print("顶视游码存在")
                        if salver_balances_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and \
                                salvers_top.shape[0] == 2:
                            # ，顶视托盘天平、砝码镊子、托盘存在
                            salver_balances_top_box = salver_balances_top[0][:4]
                            weight_tweezers_top_box = weight_tweezers_top[0][:4]
                            salvers_top_box1 = salvers_top[0][:4]
                            salvers_top_box2 = salvers_top[1][:4]
                            if metal_blocks_top.shape[0] != 0:  # 顶视存在烧杯
#                                 # print("顶视存在烧杯")
                                metal_blocks_top_box = metal_blocks_top[0][:4]
                                if not pt_in_box(center_point(metal_blocks_top_box), salver_balances_top_box) and \
                                        abs(center_distance_h(salver_balances_top_box,
                                                              weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(
                                    weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                    self.set_cursor_zero_flag = True
#                                     # print("顶视已移动游码==================================================================")
                            else:  # 顶视不存在烧杯
#                                 # print("顶视不存在烧杯")
                                if abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(
                                    weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1)
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2)
                                    self.set_cursor_zero_flag = True
#                                     # print("顶视已移动游码===============================================")

                    # elif cursors_top.shape[0] == 0 and cursors_front.shape[0] == 0:  # 前视游码不存在
                    elif cursors_top.shape[0] == 0:
#                         # print("顶视游码不存在")
                        if salver_balances_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and \
                                salvers_top.shape[0] == 2:
                            # ，顶视托盘天平、砝码镊子、托盘存在
                            salver_balances_top_box = salver_balances_top[0][:4]
                            weight_tweezers_top_box = weight_tweezers_top[0][:4]
                            salvers_top_box1 = salvers_top[0][:4]
                            salvers_top_box2 = salvers_top[1][:4]
                            if metal_blocks_top.shape[0] != 0:  # 顶视存在烧杯
#                                 # print("顶视存在烧杯")
                                metal_blocks_top_box = metal_blocks_top[0][:4]
                                if not pt_in_box(center_point(metal_blocks_top_box), salver_balances_top_box) and \
                                        abs(center_distance_h(salver_balances_top_box,
                                                              weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(
                                    weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) and \

                                    self.set_cursor_zero_flag = True
#                                     # print("顶视已移动游码==================================================================")
                            else:  # 顶视不存在烧杯
#                                 # print("顶视不存在烧杯")
                                if abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(
                                    weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1)
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2)
                                    self.set_cursor_zero_flag = True
#                                     # print("顶视已移动游码===============================================")
                # if weight_tweezers_front.shape[0] != 0:  # 前视镊子存在
                #     weight_tweezers_front_box = weight_tweezers_front[0][:4]
                #     if pt_in_box(center_point(weight_tweezers_front_box), salver_balance_front_box):
                #         self.set_cursor_zero_flag = True
#                         # print("前视镊子调整游码")

        if self.set_cursor_zero_flag:
#             # print("赋分1结束===========================================================")
            return True
#         # print("步骤1开始赋分")
        # # 前视
        # if salver_balances_front.shape[0] != 0 :
        #     # 托盘天平存在
        #     salver_balance_front_box = salver_balances_front[0][:4]  # 取托盘天平的xyxy
        #     if cursors_front.shape[0] != 0:  # 前视游码存在
        #         cursor_front_box = cursors_front[0][:4]  # 取游标的xyxy
        #         if center_distance_h(cursor_front_box, salver_balance_front_box) > 0.04 * self.w_front:
        #             # 水平方向上游标与托盘天平中心点x距离>1920*0.04
        #             self.set_cursor_zero_first, self.set_cursor_zero_last, flag = \
        #                 self.duration(self.set_cursor_zero_first, 0.5, self.set_cursor_zero_last, 0.3)
        #             if flag:
        #                 return True
        #
        #     elif salver_balances_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and salvers_top.shape[0] == 2:
        #         # 前视游码不存在，顶视托盘天平、砝码镊子、托盘存在
        #         salver_balances_top_box = salver_balances_top[0][:4]
        #         weight_tweezers_top_box = weight_tweezers_top[0][:4]
        #         salvers_top_box1 = salvers_top[0][:4]
        #         salvers_top_box2 = salvers_top[1][:4]
        #         if metal_blocks_top.shape[0] != 0: # 顶视存在金属块
        #             metal_blocks_top_box = metal_blocks_top[0][:4]
        #             if not pt_in_box(center_point(metal_blocks_top_box), salver_balances_top_box) and \
        #                     not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
        #                     not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) and \
        #                     abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 120 and \
        #                     0 < abs(salver_balances_top_box[3] - float(weight_tweezers_top_box[3] +
        #                                                                weight_tweezers_top_box[1]) / 2) < 35:
        #                 self.set_cursor_zero_flag = True
#         #                 print("顶视已移动游码==================================================================")
        #         else:  # 顶视不存在金属块
        #             if not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
        #                     not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) and \
        #                     abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 120 and \
        #                     0 < abs(salver_balances_top_box[3] - float(weight_tweezers_top_box[3] +
        #                                                                weight_tweezers_top_box[1]) / 2) < 35:
        #                 self.set_cursor_zero_flag = True
#         #                 print("顶视已移动游码===============================================")
        # if self.set_cursor_zero_flag:
        #     return True

    # 2.根据指针偏向情况，调节平衡螺母使天平平衡
    def nut_balance(self, salvers_front,  metal_blocks_front, salver_balances_top, salver_balances_front, cursors_front,
                    weights_front, hands_front):
#         # print("螺母未平衡")
        if salver_balances_top.shape[0] != 0 and weights_front.shape[0] == 0 and hands_front.shape[0] != 0:
            # 托盘天平、平衡螺母存在
            salver_balance_top_box = salver_balances_top[0][:4]
            if salver_balance_top_box[1] > 0.01 * self.h_front:
                if salver_balances_front.shape[0] != 0 and salvers_front.shape[0] == 2:
                    # 螺母两个、两只手、托盘天平、两托盘同时存在，前视游码不存在
                    salver_balance_front_box = salver_balances_front[0][:4]
                    salvers_front_box1 = salvers_front[0][:4]
                    salvers_front_box2 = salvers_front[1][:4]
                    # hand_front_box1 = hands_front[0][:4]
                    # hand_front_box2 = hands_front[1][:4]
                    if metal_blocks_front.shape[0] != 0:
                        metal_blocks_front_box = metal_blocks_front[0][:4]
#                         # print("烧杯存在")
                        if center_distance_v(metal_blocks_front_box, salver_balance_front_box) > 0:
                            if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.015 * self.h_front:
#                                 # print("托盘和螺母平位置平衡")
                                if cursors_front.shape[0] != 0:  # 如果游码存在
                                    cursor_front_box = cursors_front[0][:4]  # 取游码的xyxy
#                                     # print("游码存在")
                                    if center_distance_h(cursor_front_box, salver_balance_front_box) > 0.03 * self.w_front:
                                        # 水平方向上游标与托盘天平中心点x距离>1920*0.04
#                                         # print("游码位置符合")
                                        self.set_zero_balance_first0, self.set_zero_balance_last0, flag0 = \
                                            self.duration(self.set_zero_balance_first0, 1, self.set_zero_balance_last0, 0.5)

                                        if flag0:
                                            self.set_nut_balance_flag = True
#                                         # print("天平已平衡——————————————————————————————————————————————")
                                    else:
                                        self.set_nut_balance_flag = False
#                                         # print("天平未平衡")

                                else :
#                                     # print("游码不存在")
                                    self.set_zero_balance_first1, self.set_zero_balance_last1, flag1 = \
                                        self.duration(self.set_zero_balance_first1, 1, self.set_zero_balance_last1, 0.5)
#                                     # print("游码不存在，符合一定时间")
                                    if flag1:
                                        self.set_nut_balance_flag = True
#                                         # print("游码没检测到、砝码检测到，天平已平衡++++++++++++++++++++++++++++++++++++++++")

                    else:
#                         # print("烧杯不存在")
#                         # print(abs(center_distance_v(salvers_front_box1, salvers_front_box2)))
                        if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.015 * self.h_front:
#                             # print("托盘和螺母平位置平衡")

                            # if not pt_in_box(center_point(hand_front_box1), salver_balance_front_box) and not \
                            #         pt_in_box(center_point(hand_front_box2), salver_balance_front_box):
                                # 中心点距离游码天平减去游码的h距离大于0.04×1920,且双手的中心点都不在托盘天平中
                            if cursors_front.shape[0] != 0:  # 如果游码存在
                                cursor_front_box = cursors_front[0][:4]  # 取游码的xyxy
#                                 # print("游码存在")
                                if center_distance_h(cursor_front_box, salver_balance_front_box) > 0.02 * self.w_front:
                                    # 水平方向上游标与托盘天平中心点x距离>1920*0.04
                                    # self.set_nut_balance_flag = True
#                                     # print("游码位置符合")
                                    self.set_zero_balance_first2, self.set_zero_balance_last2, flag2 = \
                                        self.duration(self.set_zero_balance_first2, 1, self.set_zero_balance_last2, 0.5)
                                    if flag2:
                                        self.set_nut_balance_flag = True
#                                         # print("天平已平衡+++++++++++++++++++++++++++++++++++++++++")
                                else:
                                    self.set_nut_balance_flag = False
#                                     # print("天平未平衡")
                            # elif self.scorePoint1:
                            else:
#                                 # print("游码不存在")
                                self.set_zero_balance_first3, self.set_zero_balance_last3, flag3 = \
                                    self.duration(self.set_zero_balance_first3,1, self.set_zero_balance_last3, 0.5)
#                                 # print("游码不存在符合一定时间")
                                if flag3:
                                    self.set_nut_balance_flag = True
#                                     # print("游码和金属块没检测到，天平已平衡++++++++++++++++++++++++++++++++++++++++")

                if self.set_nut_balance_flag:
                    self.set_zero_balance_first, self.set_zero_balance_last, flag = \
                        self.duration(self.set_zero_balance_first, 1, self.set_zero_balance_last, 0.3)
                    if flag:
#                         # print("赋分2完成")
                        return True

    # 3.能正确在左盘放被测物，右盘用镊子放砝码。
    def left_object_right_weight(self, salver_balances_front, salvers_front, weight_tweezers_front, metal_blocks_front,
                                 weights_front, salver_balances_top, salvers_top, weight_tweezers_top,
                                 metal_blocks_top, weights_top):
        if not self.add_metal_flag:
#             # print("开始放金属块")
            if salvers_front.shape[0] == 2 and metal_blocks_front.shape[0] != 0 and \
                    salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0:
                # 两个托盘与金属块同时存在
                metal_blocks_front_box = metal_blocks_front[0][:4]
                salver_balances_front_box = salver_balances_front[0][:4]
                weights_front_box = weights_front[0][:4]
                if center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
                        center_distance_h(weights_front_box, salver_balances_front_box) < 0:
#                     # print("前视金属块在右托盘上")
                    self.add_metal_flag = True
            elif salvers_top.shape[0] == 2 and metal_blocks_top.shape[0] != 0 and \
                    salver_balances_top.shape[0] != 0:
                metal_blocks_top_box = metal_blocks_top[0][:4]
                salver_balances_top_box = salver_balances_top[0][:4]
                if center_distance_h(metal_blocks_top_box, salver_balances_top_box) < 0 and \
                        pt_in_box(center_point(metal_blocks_top_box), salver_balances_top_box):
#                     # print("顶视金属块在右托盘上")
                    self.add_metal_flag = True

        if self.add_metal_flag:  # 如果已放金属块，未放砝码
            if salver_balances_front.shape[0] != 0 and metal_blocks_front.shape[0] != 0 and \
                    weights_front.shape[0] != 0 and weight_tweezers_front.shape[0] != 0:  # 托盘天平与金属块、镊子、砝码同时存在
                salver_balances_front_box = salver_balances_front[0][:4]
                weight_tweezers_front_box = weight_tweezers_front[0][:4]
#                 # print("前视已放金属块，未放砝码")
                for weight_front in weights_front:  # 遍历同时出现的砝码
                    weight_front_box = weight_front[:4]
                    if iou(salver_balances_front_box, weight_front_box) and iou(salver_balances_front_box,
                                                                                weight_tweezers_front_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
#                         # print("前视已放砝码")
                        self.add_weight_flag = True
#                         # print("赋分3结束")
                        return True
            elif salver_balances_top.shape[0] != 0 and \
                    weights_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0:  # 托盘天平与烧杯、镊子、砝码同时存在
                salver_balances_top_box = salver_balances_top[0][:4]
                weight_tweezers_top_box = weight_tweezers_top[0][:4]
#                 # print("顶视已放烧杯，未放砝码")
                for weight_top in weights_top:  # 遍历同时出现的砝码
                    weight_top_box = weight_top[:4]
                    if iou(salver_balances_top_box, weight_top_box) and \
                            iou(salver_balances_top_box, weight_tweezers_top_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
#                         # print("顶视已放砝码")
#                         # print("赋分5结束")
                        self.add_weight_flag = True
                        return True

    # 4.用镊子按照从大到小顺序摆放砝码
    def set_weight(self, salvers_front, metal_blocks_front, weight_tweezers_front, weights_front, hands_front,
                   salver_balances_front, salvers_top, metal_blocks_top, weight_tweezers_top, weights_top, hands_top,
                   salver_balances_top):
        # 前
        if salvers_front.shape[0] == 2 and metal_blocks_front.shape[0] != 0 and weight_tweezers_front.shape[0] != 0 and \
                weights_front.shape[0] != 0 and hands_front.shape[0] != 0:  # 托盘数量为2，存在金属块、砝码、手、镊子
            weights_front_box = weights_front[0][:4]
            weight_tweezers_front_box = weight_tweezers_front[0][:4]
            metal_blocks_front_box = metal_blocks_front[0][:4]
            salver_balances_front_box = salver_balances_front[0][:4]
            # print("前视存在砝码、金属块、镊子、手")
            if center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
                    center_distance_h(weights_front_box, salver_balances_front_box) < 0 :
                for hand_front in hands_front:  # 遍历出现的手
                    hand_front_box = hand_front[:4]
                    if iou(hand_front_box, weight_tweezers_front_box) and \
                            center_distance_v(weights_front_box, weight_tweezers_front_box) and \
                            weights_front.shape[0] >= 2:
                        # 手和镊子相交、 且砝码大于等于2
                        set_tweezer_weight_flag = True
                        if set_tweezer_weight_flag:
                            # print("前视赋分4完成")
                            return True
        # 顶
        if salvers_top.shape[0] == 2 and metal_blocks_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and \
                weights_top.shape[0] != 0 and hands_top.shape[0] != 0:  # 托盘数量为2，存在金属块、砝码、手、镊子
            weights_top_box = weights_top[0][:4]
            weight_tweezers_top_box = weight_tweezers_top[0][:4]
            metal_blocks_top_box = metal_blocks_top[0][:4]
            salver_balances_top_box = salver_balances_top[0][:4]
            # print("顶存在砝码、金属块、镊子、手")
            if center_distance_h(metal_blocks_top_box, salver_balances_top_box) < 0 and \
                    center_distance_h(weights_top_box, salver_balances_top_box) > 0 :
                for hand_top in hands_top:  # 遍历出现的手
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, weight_tweezers_top_box) and \
                            center_distance_v(weights_top_box, weight_tweezers_top_box) and \
                            weights_top.shape[0] >= 2:
                        # 手和镊子相交、 且砝码大于等于2
                        set_tweezer_weight_flag = True
                        if set_tweezer_weight_flag:
                            # print("顶视赋分4完成")
                            return True

    # 5.称量时会根据指针偏向情况，通过加减砝码或移动游码使天平平衡，并正确读出物体质量的数据。
    def set_salver_balance(self, salvers_front, salver_balances_front, metal_blocks_front, weights_front,
                           nuts_front, cursors_top, salver_balances_top, weight_tweezers_top, salvers_top,
                           weight_tweezers_front):


        if not self.set_tweezers_cursors_flag:
            # print("开始移动游码")
            if weights_front.shape[0] != 0 or metal_blocks_front.shape[0] != 0:
                # 金属块、砝码同时存在
                # print("前视金属块和砝码存在")
                if salver_balances_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and salvers_top.shape[0] == 2:
                    # print("顶视托盘天平、托盘存在、镊子存在")
                    salver_balances_top_box = salver_balances_top[0][:4]
                    weight_tweezers_top_box = weight_tweezers_top[0][:4]
                    salvers_top_box1 = salvers_top[0][:4]
                    salvers_top_box2 = salvers_top[1][:4]
                    if not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
                            not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) and \
                            abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 100 and \
                            0 < abs(salver_balances_top_box[3]-float(weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 120:
                        # 镊子不在两个托盘中，托盘天平和镊子中心x小于120, 托盘天平的下y2与镊子的中心点y小于120
                        self.set_tweezers_cursors_flag = True
                        # print("顶视已移动游码=======================================================================")
                    elif cursors_top.shape[0] != 0:  # 顶视游码存在
                        self.set_tweezers_cursors_flag = True
                        # print("顶视游码存在")
                    elif weight_tweezers_top.shape[0] == 0:
                        # print("顶视镊子不存在")
                        if not self.set_tweezers_cursors_info:
                            self.set_tweezers_cursors_info= [time.time()]
                        else :
                            self.set_tweezers_cursors_info[-1] = time.time()
                        if self.set_tweezers_cursors_info and time.time() - self.set_tweezers_cursors_info[-1] > 5:
                            self.set_tweezers_cursors_flag = True

                elif salvers_front.shape[0] == 2 and metal_blocks_front.shape[0] != 0 and \
                        salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0 and \
                        weight_tweezers_front.shape[0] !=0:
                    # 两个托盘与金属块砝码同时存在
                    metal_blocks_front_box = metal_blocks_front[0][:4]
                    salver_balances_front_box = salver_balances_front[0][:4]
                    weights_front_box = weights_front[0][:4]
                    weight_tweezers_front_box = weight_tweezers_front[0][:4]
                    if center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
                            center_distance_h(weights_front_box, salver_balances_front_box) < 0 and \
                            distance_box(weight_tweezers_front_box, salver_balances_front_box) < 100:
                        # print("得分点5前视金属块在右托盘上，砝码在左")
                        self.set_tweezers_cursors_flag = True

        if self.set_tweezers_cursors_flag:
            # print("前视调平中")
            if salvers_front.shape[0] == 2 :
                # 螺母、托盘存在
                salvers_front_box1 = salvers_front[0][:4]
                salvers_front_box2 = salvers_front[1][:4]
                if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.02 * self.h_front :
                    # print("正在平衡------------------------------------------")
                    if salver_balances_front.shape[0] != 0 and \
                            weights_front.shape[0] != 0 :
                        # 金属块砝码同时存在
                        # metal_blocks_front_box = metal_blocks_front[0][:4]
                        salver_balances_front_box = salver_balances_front[0][:4]
                        weights_front_box = weights_front[0][:4]
                        if center_distance_h(weights_front_box, salver_balances_front_box) < 0 :
                            self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                                self.duration(self.set_salver_balance_first, 2)
                            # print("已调游码,托盘天平平衡")
                            if flag:
                                # print("赋分5完成")
                                return True

    # 清理桌面

    def clean_desk(self, score_index, top_items, front_items):
        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
            self.clean_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                    self.num_frame_top, self.secs]
            self.clean_time, _, flag = self.duration(self.clean_time, 2)
            if flag:
                self.clean_time = 0
                self.assignScore(score_index, self.frame_top, self.time_front, self.objects_top, self.preds_top,
                                 self.num_frame_top)
        else:
            self.clean_time = 0

    def end(self):  # 实验结束时判断是否整理桌面，如果有则进行赋分
        if self.clean_desk_info and self.secs - self.clean_desk_info[-1] < 2:
            self.assignScore(*self.clean_desk_info[:6])
            return True

    def desk_is_clean(self, views_items=None, center_boxes=None):
        for view_items, center_box in zip(views_items, center_boxes):
            for items in view_items:
                if items.shape[0] != 0:
                    for item in items:
                        item_box = item[:4]
                        if pt_in_box(center_point(item_box), center_box) > 0:
                            return False
        return True

    def duration(self, first_time, duration_time, pre_time=None, reclock_time=None):
        if reclock_time:
            if self.secs - pre_time > reclock_time:  # n 秒内没有此动作 重新计时
                first_time = pre_time = 0.
            else:
                pre_time = self.secs
        if first_time == 0:
            if reclock_time:
                first_time = pre_time = self.secs
            else:
                first_time = self.secs
            return first_time, pre_time, False
        elif self.secs - first_time > duration_time:
            return first_time, pre_time, True
        else:
            return first_time, pre_time, False

# 打印log
# class Logger(object):
#     def __init__(self, fileN='Default.log'):
#         self.terminal = sys.stdout
#         self.log = open(fileN, 'a')
#
#     def write(self, message):
# #         '''print实际相当于sys.stdout.write'''
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         pass
#
#
# # sys.stdout = Logger('/home/xiding/new_aiexhibition_windows-master/test_log/log.txt')  # 调用print时相当于Logger().write()
