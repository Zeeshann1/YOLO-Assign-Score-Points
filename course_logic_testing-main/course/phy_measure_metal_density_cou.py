#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/01/07 17:18
# @Author  : lld
# @File    : phy_measure_metal_density_cou.py
"""
V2.2更新
1.得分4中倒水增加顶视检测烧杯
2.得分点5和7的观察时间阈值减小
3.金属块和量筒的iou可以为0.9-1
4.得分1的平衡条件放松，高度差阈值为螺母1080×0.02,和托盘天平1080×0.14

V2.3更新
1.解决天平摆放位置太偏只能检测到一个螺母问题
2.优化得分点1和3平衡条件
3.可能会出现得分点1和3提前出的问题
待优化：可能会出现下蹲时放金属块不出分的问题

"""

from .comm import *
from .comm.course_base import ConfigModel


class PHY_measure_metal_density(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(PHY_measure_metal_density, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False
        self.scorePoint8 = False

        self.set_cursor_zero_flag = False  # 游码置0
        self.set_nut_balance_flag = False  # 螺母调平
        self.set_zero_balance_first0 = 0  # 调0平衡
        self.set_zero_balance_last0 = 0
        self.set_zero_balance_first1 = 0  # 调0平衡
        self.set_zero_balance_last1 = 0
        self.set_zero_balance_first2 = 0  # 调0平衡
        self.set_zero_balance_last2 = 0
        self.set_zero_balance_first3 = 0  # 调0平衡
        self.set_zero_balance_last3 = 0
        self.set_zero_balance_first = 0  # 调0平衡
        self.set_zero_balance_last = 0

        self.add_metal_flag = False  # 加金属
        self.add_weight_flag = False  # 加砝码
        self.left_object_right_weight_first = 0  # 左物右码
        self.left_object_right_weight_last = 0

        self.set_tweezers_cursors_first = 0
        self.set_tweezers_cursors_last = 0

        self.set_salver_balance_flag = False  # 天平平衡
        self.set_salver_balance_first = 0  # 天平平衡
        self.set_salver_balance_last = 0

        self.set_tweezers_cursors_flag = False
        self.set_tweezers_cursors_info = []

        self.beaker_measuring_cylinder_flag = False  # 烧杯向量筒倒水
        self.add_water_first = 0  # 量筒中倒水
        self.add_water_last = 0
        self.add_water_beaker_info = []  # 用烧杯向量筒加水信息
        self.add_water_info = []

        self.block_in_water_flag = False  # 金属块在水中
        self.see_display_first = 0  # 读示数
        self.see_display_last = 0
        self.see_display_info = []  # 读示数
        self.see_display_head_info = []  # 读示数（只有头）

        self.see_display_block_first = 0  # 读示数（有物块）
        self.see_display_block_last = 0
        self.see_display_block_info = []  # 读示数（有物块）
        self.see_display_block_head_info = []  # 读示数（有物块）（只有头）

        self.block_in_water_first = 0
        self.block_in_water_last = 0

        self.clean_time = 0
        self.clean_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        hands_front, heads_front, eyes_front, dusters_front, clean_desks_front, salvers_front, weight_tweezers_front, \
        nuts_front, metal_blocks_front, weights_front, weight_boxs_front, salver_balances_front, \
        cursors_front, measuring_cylinders_front, cylinders_bottom_front, water_columns_front, \
        beakers_front, liquids_front = self.preds_front

        hands_top, heads_top, eyes_top, dusters_top, clean_desks_top, salvers_top, weight_tweezers_top, \
        nuts_top, metal_blocks_top, weights_top, weight_boxs_top, salver_balances_top, cursors_top, \
        measuring_cylinders_top, cylinders_bottom_top, water_columns_top, beakers_top, liquids_top = self.preds_top

        front_items = [salvers_front, weight_tweezers_front, nuts_front, metal_blocks_front, weights_front,
                       weight_boxs_front, salver_balances_front, cursors_front, measuring_cylinders_front,
                       cylinders_bottom_front,
                       water_columns_front, beakers_front, liquids_front]
        top_items = [salvers_top, weight_tweezers_top, nuts_top, metal_blocks_top, weights_top, weight_boxs_top,
                     salver_balances_top, cursors_top, measuring_cylinders_top, cylinders_bottom_top, water_columns_top,
                     beakers_top, liquids_top]

        # 如果未得到得分点，则执行函数。
        # 1.将托盘天平放在水平台面，调节天平平衡。
        if not self.scorePoint1:
            if self.set_zero_balance(salvers_front, metal_blocks_front, salver_balances_top, salver_balances_front,
                                     cursors_front, weights_front, hands_front):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.能正确在左盘放被测物，右盘用镊子放砝码。
        if not self.scorePoint2:
            if self.left_object_right_weight(salver_balances_front, salvers_front, weight_tweezers_front, metal_blocks_front,
                                             weights_front, salver_balances_top, salvers_top, weight_tweezers_top,
                                             metal_blocks_top, weights_top):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.称量时会根据指针偏向情况，通过加减砝码或移动游码使天平平衡，并正确读出物体质量的数据。
        if not self.scorePoint3:
            if self.set_salver_balance_01(salvers_front, salver_balances_front, metal_blocks_front, weights_front,
                                          nuts_front, cursors_top, salver_balances_top, weight_tweezers_top,
                                          salvers_top, weight_tweezers_front):

                if self.set_salver_balance_02(salvers_front, salver_balances_front, metal_blocks_front, weights_front,
                                              nuts_front, cursors_top, salver_balances_top, weight_tweezers_top,
                                              salvers_top, weight_tweezers_front):
                    self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                     self.num_frame_front)


        # 4.在量筒中倒入适量的水。
        if not self.scorePoint4:
            # if self.add_water(4, water_columns_front, beakers_front, measuring_cylinders_front, metal_blocks_front):
            # self.assignScore(4, self.frame_front, self.secs*1000, self.objects_front, self.preds_front,
            #                  self.num_frame_front)
            info = self.add_water(4, water_columns_front, beakers_front, measuring_cylinders_front, metal_blocks_front,
                                  beakers_top, hands_top)
            if info is not None:
                self.assignScore(*info)

        # 5.观察量筒中水面对应的示数，记录水的体积。
        if self.scorePoint4 and not self.scorePoint5:
            # if self.record_V_display(5, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
            #                          metal_blocks_front):
            #     self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front,
            #                      self.num_frame_front)
            info = self.record_V_display(5, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                         metal_blocks_front)
            if info is not None:
                self.assignScore(*info)

        # 6.用细绳拴住金属块，慢慢浸没在水中。
        if not self.scorePoint6:
            if self.block_in_water(measuring_cylinders_front, measuring_cylinders_top, water_columns_front,
                                   metal_blocks_front, metal_blocks_top):
                self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 7.观察量筒中水面对应的示数，记录水和金属块的总体积。
        if self.scorePoint6 and not self.scorePoint7:  # and self.scorePoint6:
            # if self.record_V_display(7, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
            #                          metal_blocks_front):
            #     self.assignScore(7, self.frame_front, self.secs*1000, self.objects_front, self.preds_front,
            #                      self.num_frame_front)
            info = self.record_V_display(7, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                         metal_blocks_front)
            if info is not None:
                self.assignScore(*info)

        # 8.实验结束后能及时整理器材。
        if not self.scorePoint8 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3 or self.scorePoint8 or
                                     self.scorePoint4 or self.scorePoint5 or self.scorePoint6 or self.scorePoint7):
            self.clean_desk(8, top_items, front_items)
        if self.scorePoint8 and len(self.score_list) != 8:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(8)

    # 1.将托盘天平放在水平台面，调节天平平衡。
    # 将托盘天平放在水平台面。用镊子将游码移到0刻度处。调节平衡螺母，使指针指到分度盘的中央刻度线（或指针指在0刻度线）。

    def set_zero_balance(self, salvers_front, metal_blocks_front, salver_balances_top, salver_balances_front,
                         cursors_front, weights_front, hands_front):
        # print("螺母未平衡")
        if salver_balances_top.shape[0] != 0 and weights_front.shape[0] == 0 and hands_front.shape[0] != 0:
            # 托盘天平、平衡螺母存在
            salver_balance_top_box = salver_balances_top[0][:4]
            if salver_balance_top_box[1] > 0.01 * self.h_front:
                if salver_balances_front.shape[0] != 0 and salvers_front.shape[0] == 2:
                    # 螺母两个、两只手、托盘天平、两托盘同时存在，前视游码不存在
                    salver_balance_front_box = salver_balances_front[0][:4]
                    salvers_front_box1 = salvers_front[0][:4]
                    salvers_front_box2 = salvers_front[1][:4]
                    if metal_blocks_front.shape[0] != 0:
                        metal_blocks_front_box = metal_blocks_front[0][:4]
                        # print("金属块存在")
                        if center_distance_v(metal_blocks_front_box, salver_balance_front_box) > 0:
                            if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.015 * self.h_front:
                                # print("托盘和螺母平位置平衡")
                                if cursors_front.shape[0] != 0:  # 如果游码存在
                                    cursor_front_box = cursors_front[0][:4]  # 取游码的xyxy
                                    # print("游码存在")
                                    if center_distance_h(cursor_front_box,
                                                         salver_balance_front_box) > 0.03 * self.w_front:
                                        # 水平方向上游标与托盘天平中心点x距离>1920*0.04
                                        # print("游码位置符合")
                                        self.set_zero_balance_first0, self.set_zero_balance_last0, flag0 = \
                                            self.duration(self.set_zero_balance_first0, 2, self.set_zero_balance_last0,
                                                          0.5)

                                        if flag0:
                                            self.set_nut_balance_flag = True
                                            # print("天平已平衡——————————————————————————————————————————————")
                                    else:
                                        self.set_nut_balance_flag = False
                                        # print("天平未平衡")
                                else:
                                    # print("游码不存在")
                                    self.set_zero_balance_first1, self.set_zero_balance_last1, flag1 = \
                                        self.duration(self.set_zero_balance_first1, 2, self.set_zero_balance_last1, 0.5)
                                    # print("游码不存在，符合一定时间")
                                    if flag1:
                                        self.set_nut_balance_flag = True
                                        # print("游码没检测到、砝码检测到，天平已平衡++++++++++++++++++++++++++++++++++++++++")

                    else:
                        # print("金属块不存在")
                        # # print(abs(center_distance_v(salvers_front_box1, salvers_front_box2)))
                        if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.015 * self.h_front:
                            # print("托盘和螺母平位置平衡")

                            # if not pt_in_box(center_point(hand_front_box1), salver_balance_front_box) and not \
                            #         pt_in_box(center_point(hand_front_box2), salver_balance_front_box):
                            # 中心点距离游码天平减去游码的h距离大于0.04×1920,且双手的中心点都不在托盘天平中
                            if cursors_front.shape[0] != 0:  # 如果游码存在
                                cursor_front_box = cursors_front[0][:4]  # 取游码的xyxy
                                # print("游码存在")
                                if center_distance_h(cursor_front_box, salver_balance_front_box) > 0.02 * self.w_front:
                                    # 水平方向上游标与托盘天平中心点x距离>1920*0.04
                                    # self.set_nut_balance_flag = True
                                    # print("游码位置符合")
                                    self.set_zero_balance_first2, self.set_zero_balance_last2, flag2 = \
                                        self.duration(self.set_zero_balance_first2, 2, self.set_zero_balance_last2, 0.5)
                                    if flag2:
                                        self.set_nut_balance_flag = True
                                        # print("天平已平衡+++++++++++++++++++++++++++++++++++++++++")
                                else:
                                    self.set_nut_balance_flag = False
                                    # print("天平未平衡")
                            # elif self.scorePoint1:
                            else:
                                # print("游码不存在")
                                self.set_zero_balance_first3, self.set_zero_balance_last3, flag3 = \
                                    self.duration(self.set_zero_balance_first3, 2, self.set_zero_balance_last3, 0.5)
                                # print("游码不存在符合一定时间")
                                if flag3:
                                    self.set_nut_balance_flag = True
                                    # print("游码和金属块没检测到，天平已平衡++++++++++++++++++++++++++++++++++++++++")

                if self.set_nut_balance_flag:
                    self.set_zero_balance_first, self.set_zero_balance_last, flag = \
                        self.duration(self.set_zero_balance_first, 2, self.set_zero_balance_last, 0.3)
                    if flag:
                        # print("赋分1完成")
                        return True

    # 2.能正确在左盘放被测物，右盘用镊子放砝码。
    def left_object_right_weight(self, salver_balances_front, salvers_front, weight_tweezers_front, metal_blocks_front,
                                 weights_front, salver_balances_top, salvers_top, weight_tweezers_top, metal_blocks_top,
                                 weights_top):
        self.add_metal_flag = False
        if not self.add_metal_flag:
#             # print("开始放金属块")
            if salvers_front.shape[0] == 2 and metal_blocks_front.shape[0] != 0 and \
                    salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0:
                # 两个托盘与烧杯同时存在
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
#                     # print("顶视金属块在左托盘上")
                    self.add_metal_flag = True

        if self.add_metal_flag:  # 如果已放金属块，未放砝码
            if salver_balances_front.shape[0] != 0 and metal_blocks_front.shape[0] != 0 and \
                    weights_front.shape[0] != 0 and weight_tweezers_front.shape[0] != 0:  # 托盘天平与烧杯、镊子、砝码同时存在
                salver_balances_front_box = salver_balances_front[0][:4]
                weight_tweezers_front_box = weight_tweezers_front[0][:4]
#                 # print("前视已放烧杯，未放砝码")
                for weight_front in weights_front:  # 遍历同时出现的砝码
                    weight_front_box = weight_front[:4]
                    if iou(salver_balances_front_box, weight_front_box) and iou(salver_balances_front_box,
                                                                                weight_tweezers_front_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
#                         # print("前视已放砝码")
                        self.add_weight_flag = True
#                         # print("赋分2结束")
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
#                         # print("赋分2结束")
                        self.add_weight_flag = True
                        return True

    # 3.称量时会根据指针偏向情况，通过加减砝码或移动游码使天平平衡，并正确读出物体质量的数据。
    def set_salver_balance_01(self, salvers_front, salver_balances_front, metal_blocks_front, weights_front, nuts_front,
                           cursors_top, salver_balances_top, weight_tweezers_top, salvers_top, weight_tweezers_front):
        self.set_tweezers_cursors_flag = False
        if not self.set_tweezers_cursors_flag:
#         #         print("开始移动游码")
            if weights_front.shape[0] != 0 or metal_blocks_front.shape[0] != 0:
                # 烧杯、砝码存在
#         #             print("前视烧杯和砝码存在")
                if salver_balances_top.shape[0] != 0 and salvers_top.shape[0] == 2:
#         #                 print("顶视托盘天平、托盘存在")
                    salver_balances_top_box = salver_balances_top[0][:4]
                    salvers_top_box1 = salvers_top[0][:4]
                    salvers_top_box2 = salvers_top[1][:4]
                    if salvers_front.shape[0] == 2 and metal_blocks_front.shape[0] != 0 and \
                            salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0 and \
                            weight_tweezers_front.shape[0] != 0:
#         #                     print("平衡判定情况1")
                        # 两个托盘与烧杯、托盘天平、砝码、镊子同时存在
                        weight_tweezers_front_box = weight_tweezers_front[0][:4]
#         #                     print("判断前视镊子位置")
                        if pt_in_box(center_point(weight_tweezers_front_box), salver_balances_top_box):
#         #                         print("情况1符合")
                            self.set_tweezers_cursors_flag = True
                            return True
                    elif weight_tweezers_top.shape[0] != 0:  # 顶视镊子存在
                        weight_tweezers_top_box = weight_tweezers_top[0][:4]
#         #                     print("平衡判定情况2")
                        if salvers_front.shape[0] == 2 and metal_blocks_front.shape[0] != 0 and \
                                salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0:
                            # 两个托盘与烧杯同时存在
                            metal_blocks_front_box = metal_blocks_front[0][:4]
                            salver_balances_front_box = salver_balances_front[0][:4]
                            weights_front_box = weights_front[0][:4]
                            if center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
                                    center_distance_h(weights_front_box, salver_balances_front_box) < 0:
#         #                             print("判断顶视镊子位置")
                                if not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
                                        not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) :
                                    if abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 200 or \
                                            0 < abs(salver_balances_top_box[3]-float(weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 200 or \
                                            distance_box(weight_tweezers_top_box, salver_balances_top_box) < 400 :
                                        # 镊子不在两个托盘中，托盘天平和镊子中心高度差小于120,托盘天平的下y2与镊子的中心点y小于120
#         #                                     print("情况2符合")
                                        self.set_tweezers_cursors_flag = True
                                        return True

                    elif cursors_top.shape[0] != 0:  # 顶视游码存在
                        self.set_tweezers_cursors_flag = True
#         #                     print("平衡判定情况3,顶视游码存在")
                        return True
    def set_salver_balance_02(self, salvers_front, salver_balances_front, metal_blocks_front, weights_front, nuts_front,
                              cursors_top, salver_balances_top, weight_tweezers_top, salvers_top,
                              weight_tweezers_front):
        # if self.set_tweezers_cursors_flag:
#         # print("前视调平中")
        if salvers_front.shape[0] == 2:
            salvers_front_box1 = salvers_front[0][:4]
            salvers_front_box2 = salvers_front[1][:4]
#             # print(abs(center_distance_v(salvers_front_box1, salvers_front_box2)))
            if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.021 * self.h_front:
#                 # print("正在平衡------------------------------------------")
                if metal_blocks_front.shape[0] != 0 and salver_balances_front.shape[0] != 0 and \
                        weights_front.shape[0] != 0 :
                    # 烧杯砝码同时存在
#                     # print("烧杯砝码同时存在")
                    metal_blocks_box = metal_blocks_front[0][:4]
                    salver_balances_front_box = salver_balances_front[0][:4]
                    weights_front_box = weights_front[0][:4]
                    if (center_distance_h(metal_blocks_box, salver_balances_front_box) > 0 and \
                            center_distance_h(weights_front_box, salver_balances_front_box) < 0 and \
                            iou(metal_blocks_box,salver_balances_front_box) > 0) or \
                            (center_distance_h(metal_blocks_box, salver_balances_front_box) < 0 and
                            center_distance_h(weights_front_box, salver_balances_front_box) > 0 and
                            iou(metal_blocks_box,salver_balances_front_box) > 0):
                        # 支持左物右码和左码右物
                        self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                            self.duration(self.set_salver_balance_first, 2.5, self.set_salver_balance_last,0.5)
#                         # print("已调游码,托盘天平平衡")
                        if flag:
#                             # print("赋分3完成")
                            return True
                elif metal_blocks_front.shape[0] == 0 and salver_balances_front.shape[0] != 0 and \
                        weights_front.shape[0] != 0 :
#                     # print("砝码存在")
                    salver_balances_front_box = salver_balances_front[0][:4]
                    weights_front_box = weights_front[0][:4]
                    if center_distance_h(weights_front_box, salver_balances_front_box) < 0 or \
                            center_distance_h(weights_front_box, salver_balances_front_box) > 0:
                        self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                            self.duration(self.set_salver_balance_first, 2.5, self.set_salver_balance_last,0.5)
#                         # print("已调游码,托盘天平平衡")
                        if flag:
#                             # print("赋分7完成")
                            return True
                elif metal_blocks_front.shape[0] != 0 and salver_balances_front.shape[0] != 0 and \
                        weights_front.shape[0] == 0 :
#                     # print("烧杯存在")
                    beakers_front_box = metal_blocks_front[0][:4]
                    salver_balances_front_box = salver_balances_front[0][:4]
                    if (center_distance_h(beakers_front_box, salver_balances_front_box) > 0 or
                        center_distance_h(beakers_front_box, salver_balances_front_box) < 0) and \
                            iou(beakers_front_box,salver_balances_front_box) > 0:
                        self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                            self.duration(self.set_salver_balance_first, 2.5, self.set_salver_balance_last,0.5)
#                         # print("已调游码,托盘天平平衡")
                        if flag:
#                             # print("赋分7完成")
                            return True

    # 4. 在量筒中倒入适量的水。
    def add_water(self, score_index, water_columns_front, beakers_front, measuring_cylinders_front, metal_blocks_front,
                  beakers_top, hands_top):
        if water_columns_front.shape[0] > 0 and water_columns_front[0][3] - water_columns_front[0][1] > \
                self.h_front * 0.06:  # 水柱存在，y2-y1d大于1080×0.06像素
            water_columns_front_box = water_columns_front[0][:4]  # 取水柱xyxy
            # print("水柱存在")
            if metal_blocks_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0 and \
                    beakers_front.shape[0] > 0:  # 金属块、量筒、烧杯存在
                metal_blocks_front_box = metal_blocks_front[0][:4]
                measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                beaker_front_box = beakers_front[0][:4]
                # print("金属块存在")
                if iou(water_columns_front_box, measuring_cylinder_front_box):
                    self.beaker_measuring_cylinder_flag = True  # 烧杯量筒倒水为True
                    if not pt_in_box(center_point(metal_blocks_front_box), measuring_cylinder_front_box):
                        # print("金属块不在量筒中")
                        if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
                                iou(beaker_front_box, measuring_cylinder_front_box) > 0:  # 烧杯y在量筒y上方 烧杯与量筒有交集
                            self.beaker_measuring_cylinder_flag = False  # 烧杯向量筒倒水未结束
                            self.record_add_water_info(score_index, self.frame_front, self.time_front, self.objects_front,
                                                       self.preds_front, self.num_frame_front,
                                                       water_columns_front_box, True)
                            # print("正在倒水，实时记录量筒中水位高度变化")

                    if self.beaker_measuring_cylinder_flag:  # 烧杯量筒倒水为True
                        self.add_water_first, self.add_water_last, flag = \
                            self.duration(self.add_water_first, 3, self.add_water_last, 0.5)
                        # print("量筒中已经有水")
                        if flag:
                            self.record_add_water_info(score_index, self.frame_front, self.time_front,
                                                       self.objects_front, self.preds_front, self.num_frame_front,
                                                       water_columns_front_box, True)
                            # print("在烧杯向量筒中倒水的列表进行更新")

            elif metal_blocks_front.shape[0] == 0 and measuring_cylinders_front.shape[0] > 0 and \
                    beakers_front.shape[0] > 0:  # 金属块、量筒、烧杯存在:
                # print("金属块不存在")
                measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                beaker_front_box = beakers_front[0][:4]
                if iou(water_columns_front_box, measuring_cylinder_front_box):
                    self.beaker_measuring_cylinder_flag = True  # 烧杯量筒倒水为True
                    if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
                            iou(beaker_front_box, measuring_cylinder_front_box) > 0:  # 烧杯y在量筒y上方 烧杯与量筒有交集
                        self.beaker_measuring_cylinder_flag = False  # 烧杯向量筒倒水未结束
                        self.record_add_water_info(score_index, self.frame_front, self.time_front, self.objects_front,
                                                   self.preds_front, self.num_frame_front,
                                                   water_columns_front_box, True)
                        # print("正在倒水，实时记录量筒中水位高度变化")

                    if self.beaker_measuring_cylinder_flag:  # 烧杯量筒倒水为True
                        self.add_water_first, self.add_water_last, flag = \
                            self.duration(self.add_water_first, 3, self.add_water_last, 0.2)
                        # print("量筒中已经有水")
                        if flag:
                            self.record_add_water_info(score_index, self.frame_front, self.time_front,
                                                       self.objects_front, self.preds_front, self.num_frame_front,
                                                       water_columns_front_box, True)
                            # print("在烧杯向量筒中倒水的列表进行更新")

            elif metal_blocks_front.shape[0] == 0 and measuring_cylinders_front.shape[0] > 0 and \
                    beakers_top.shape[0] > 0 and hands_top.shape[0] != 0:  # 金属块、量筒、烧杯、手存在:
                # print("顶视量筒和手存在")
                measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                beaker_top_box = beakers_top[0][:4]
                if iou(water_columns_front_box, measuring_cylinder_front_box):
                    self.beaker_measuring_cylinder_flag = True  # 烧杯量筒倒水为True
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if iou(beaker_top_box, hand_top_box) > 0:
                            self.beaker_measuring_cylinder_flag = False  # 烧杯向量筒倒水未结束
                            self.record_add_water_info(score_index, self.frame_front, self.time_front, self.objects_front,
                                                       self.preds_front, self.num_frame_front,
                                                       water_columns_front_box, True)
                            # print("正在倒水，实时记录量筒中水位高度变化")

                    if self.beaker_measuring_cylinder_flag:  # 烧杯量筒倒水为True
                        self.add_water_first, self.add_water_last, flag = \
                            self.duration(self.add_water_first, 3, self.add_water_last, 0.2)
                        # print("量筒中已经有水")
                        if flag:
                            self.record_add_water_info(score_index, self.frame_front, self.time_front,
                                                       self.objects_front, self.preds_front, self.num_frame_front,
                                                       water_columns_front_box, True)
                            # print("在烧杯向量筒中倒水的列表进行更新")

        if self.add_water_beaker_info:
            if self.secs - self.add_water_beaker_info[-1] > 0.5:
                # print("烧杯向量筒中倒水列表更新已完成，赋分4已完成")
                return self.add_water_beaker_info[:6]
        elif self.add_water_info:
            if self.secs - self.add_water_info[-1] > 0.5:
                # print("量筒中水列表更新已完成，赋分4已完成")
                return self.add_water_info[:6]

    # 5. 观察量筒中水面对应的示数，记录水的体积。
    def record_V_display(self, score_index, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                         metal_blocks_front):
        self.block_in_water_flag = False  # 金属块不在水中
        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0:  # 量筒水柱存在
            # print("5.量筒和水柱存在")
            water_columns_front_box = water_columns_front[0][:4]
            if metal_blocks_front.shape[0] > 0:  # 金属块存在
                # print("5.金属块存在")
                block_front_box = metal_blocks_front[0][:4]
                if iou(water_columns_front_box, block_front_box) >= box_area(block_front_box) * 0.9 and \
                        block_front_box[1] - water_columns_front_box[1] > self.h_front * 0.028:  # 金属块在水里
                    self.block_in_water_flag = True
                    # print("5.金属块与水柱高度差符合")
            if not self.block_in_water_flag:  # 金属块不在水中
                self.see_display(score_index, eyes_front, heads_front, water_columns_front_box, False)
                # print("5.金属块不在水中")
                if self.see_display_info and self.secs - self.see_display_info[-1] > 0.5:
                    return self.see_display_info[:6]
                elif self.see_display_head_info and self.secs - self.see_display_head_info[-1] > 0.5:
                    return self.see_display_head_info[:6]
            else:
                # print("5.金属块在水中")
                self.see_display(score_index, eyes_front, heads_front, water_columns_front_box, True)
                if self.see_display_block_info and self.secs - self.see_display_block_info[-1] > 0.3:
                    return self.see_display_block_info[:6]
                elif self.see_display_block_head_info and self.secs - self.see_display_block_head_info[-1] > 0.3:
                    return self.see_display_block_head_info[:6]

    # 看示数
    def see_display(self, score_index, eyes_front, heads_front, water_columns_front_box, block=False):  # 看示数
        water_column_center_point_up = (
            (water_columns_front_box[0] + water_columns_front_box[2]) / 2, water_columns_front_box[1])  # 水柱液面中心
        if eyes_front.shape[0] > 0:  # 眼睛
            eyes_front_box_list = []
            for eye_front in eyes_front:
                eye_front_box = eye_front[:4]
                if distance_point(center_point(eye_front_box),
                                  water_column_center_point_up) < self.h_front * 0.185:
                    eyes_front_box_list.append(eye_front_box)
            if len(eyes_front_box_list) == 0:  # 如果眼睛框=0
                return
            elif len(eyes_front_box_list) == 1:  # 眼睛框=1
                eye_center_h = center_point(eyes_front_box_list[0])[1]  # 取上中心点y
            elif len(eyes_front_box_list) == 2:  # 眼睛框=2
                eye_center_h = (center_point(eyes_front_box_list[0])[1] + center_point(eyes_front_box_list[1])[1]) / 2
            else:
                return
            dis_eye_water = abs(eye_center_h - water_columns_front_box[1])  # 取眼睛上中心点与水柱液面y
            if dis_eye_water < self.h_front * 0.135:
                # print("57.眼睛与液面距离符合高度差")
                if not block:
                    # print("57.金属块不在水中")
                    # self.see_display_first, self.see_display_last, flag = \
                    #     self.duration(self.see_display_first, 0.4, self.see_display_last, 0.3)
                    self.see_display_first, self.see_display_last, flag = \
                        self.duration(self.see_display_first, 0.2)
                    if flag:
                        if not self.see_display_info or dis_eye_water < self.see_display_info[-2]:
                            self.see_display_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                     self.preds_front, self.num_frame_front, dis_eye_water, self.secs]
                        else:
                            self.see_display_info[-1] = self.secs
                else:
                    # print("57.金属块在水中")
                    # self.see_display_block_first, self.see_display_block_last, flag = \
                    #     self.duration(self.see_display_block_first, 0.4, self.see_display_block_last, 0.3)
                    self.see_display_block_first, self.see_display_block_last, flag = \
                        self.duration(self.see_display_block_first, 0.2)
                    if flag:
                        # print("flag存在")
                        if not self.see_display_block_info or dis_eye_water < self.see_display_block_info[-2]:
                            self.see_display_block_info = [score_index, self.frame_front, self.time_front,
                                                           self.objects_front, self.preds_front, self.num_frame_front,
                                                           dis_eye_water, self.secs]
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
                # print("57.头与液面距离符合高度差")
                if not block:
                    # print("57.金属块不在水中")
                    # self.see_display_first, self.see_display_last, flag = \
                    #     self.duration(self.see_display_first, 0.4, self.see_display_last, 0.3)
                    self.see_display_first, self.see_display_last, flag = self.duration(self.see_display_first, 0.2)
                    if flag:
                        if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                            self.see_display_head_info = [score_index, self.frame_front, self.time_front,
                                                          self.objects_front,
                                                          self.preds_front, self.num_frame_front, dis_head_water,
                                                          self.secs]
                        else:
                            self.see_display_head_info[-1] = self.secs
                else:
                    # print("57.金属块在水中")
                    # self.see_display_block_first, self.see_display_block_last, flag = \
                    #     self.duration(self.see_display_block_first, 0.4, self.see_display_block_last, 0.3)
                    self.see_display_block_first, self.see_display_block_last, flag = \
                        self.duration(self.see_display_block_first, 0.2)
                    if flag:
                        # print("flag存在")
                        if not self.see_display_block_head_info or dis_head_water < \
                                self.see_display_block_head_info[-2]:
                            self.see_display_block_head_info = \
                                [score_index, self.frame_front, self.time_front, self.objects_front,
                                 self.preds_front, self.num_frame_front, dis_head_water, self.secs]
                        else:
                            self.see_display_block_head_info[-1] = self.secs

    # 6. 用细绳拴住金属块，慢慢浸没在水中。
    # 物块放在水中
    def block_in_water(self, measuring_cylinders_front, measuring_cylinders_top, water_columns_front,
                       metal_blocks_front, metal_blocks_top):
        # 顶视 ，用于判断
        if metal_blocks_top.shape[0] > 0:  # 金属块存在
            block_cylinder = False  # 金属块不在水里
            if measuring_cylinders_top.shape[0] > 0:  # 量筒存在
                measuring_cylinder_top = measuring_cylinders_top[0][:4]
                for metal_block_top in metal_blocks_top:
                    metal_block_top_box = metal_block_top[:4]
                    if iou(metal_block_top_box, measuring_cylinder_top) > 0:  # 量筒和金属块相交
                        block_cylinder = True  # 金属块在水里
            if not block_cylinder:  # 金属块不在水里
                return  # 不再执行
        # 前视
        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0 and \
                metal_blocks_front.shape[0] > 0:  # 量筒 水柱 金属块
            # print("量筒水柱金属块存在")
            water_columns_front_box = water_columns_front[0][:4]  # 水柱
            metal_block_front_box = metal_blocks_front[0][:4]  # 金属块
            if iou(water_columns_front_box, metal_block_front_box) > 0.9*box_area(metal_block_front_box) and \
                    metal_block_front_box[1] - water_columns_front_box[1] > self.h_front * 0.028:  # 金属块在水里
                # print("金属块在水中")
                # self.block_in_water_first, self.block_in_water_last, flag = \
                #     self.duration(self.block_in_water_first, 0.6, self.block_in_water_last, 0.3)
                self.block_in_water_first, self.block_in_water_last, flag = \
                    self.duration(self.block_in_water_first, 0.5)
                if flag:
                    # print("赋分6完成")
                    return True

        # 记录向量筒中添加水的信息

    def record_add_water_info(self, score_index, img0, mses, objects, preds, num_frame, box, beaker=False):
        y = box[3] - box[1]  # 用来更新水柱高度
        if beaker:  # 如果检测到烧杯
            if not self.add_water_beaker_info or y > self.add_water_beaker_info[-2]:  # 无烧杯倒水信息或者y大于列表中第五个
                self.add_water_beaker_info = [score_index, img0, mses, objects, preds, num_frame, y, self.secs]
            else:  # 有烧杯倒水信息或y小于等于列表第五个参数
                self.add_water_beaker_info[-1] = self.secs  # 更新时间参数
        else:
            if not self.add_water_info or self.add_water_info[-2] < y:  # 无水信息或者列表中参数小于y
                self.add_water_info = [score_index, img0, mses, objects, preds, num_frame, y, self.secs]

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
