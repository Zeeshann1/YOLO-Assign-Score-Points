#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04/22 11:18
# @Author  : lld
# @File    : phy_measure_liquid_density_cou.py
"""
V2.0
1.解决两得分点一起出分
2.解决平衡得分点提前出
3.修改量筒中水柱高度阈值
4.解决平衡时不需要检测到双手时的操作情况
5.修改托盘高度差的阈值，放宽到15像素
V2.1
1.加入得分点2,加入空托盘判断条件
2.加入得分点先后赋分顺序判断
3.前视有量筒遮挡，得分点3和4的砝码和烧杯无法检测
4.前视有托盘天平遮挡，得分点5和6无法检测，需要测视和顶视来优化倒水
V2.2 新评分点
1.解决1和2的托盘天平在操作区才能评分的问题
2.扩大平衡时镊子的范围
3.增加选择小烧杯得分点
V2.3
1.优化改成得分点1必须要有调零
2.优化得分6,放松阈值
3.优化得分7的倒水，只要有相关动作就给分
4.优化收拾桌面，放松给分
V3.0
1. 优化了得分2中有砝码不进行判断
2. 优化了得分3中必须有1或者2得分后才进行判断
3. 优化了得分8倒水的误检测
4. 优化了得分9观察，设置水柱高度，拿起观察不得分，支持量筒远离人脸进行观察
V3.1
1. 优化得分2的天平位置阈值修改
2. 加入侧视观察量筒判断
3. 放宽整理桌面赋分
V3.2
1.继续放宽得分2的时间阈值
2.继续放宽得分2、6的时间阈值
3.解除得分3、8、9的关联性
V3.3
1.优化得分1,增加前视镊子判断
V3.4
1.优化得分6的出分顺序以及平衡判断
2.优化得分9的侧视观察
V3.5
1.优化平衡时前视无法检测到烧杯或者砝码
2.优化得分1和2操作区外也可以得分
V3.6
1.优化了得分2必须要用手
2.优化了得分1可以不用检测前视游码
3.优化了得分6平衡的放宽
4.优化了清理桌面
5.优化了得分5，可以不区分左右
"""




from .comm import *
from .comm.course_base import ConfigModel

class PHY_measure_liquid_density(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(PHY_measure_liquid_density, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False
        self.scorePoint8 = False
        self.scorePoint9 = False
        self.scorePoint9 = False
        self.scorePoint10 = False

        self.set_cursor_zero_flag = False  # 游码置0
        self.set_nut_balance_flag = False  # 螺母调平
        self.set_cursor_zero_first = 0 # 游码归0
        self.set_cursor_zero_last = 0
        self.set_zero_balance_first0 = 0
        self.set_zero_balance_last0 = 0
        self.set_zero_balance_first1 = 0  # 调0平衡
        self.set_zero_balance_last1 = 0
        self.set_zero_balance_first2 = 0  # 调0平衡
        self.set_zero_balance_last2 = 0
        self.set_zero_balance_first = 0  # 调0平衡
        self.set_zero_balance_last = 0
        self.set_zero_balance_first3 = 0  # 调0平衡
        self.set_zero_balance_last3 = 0

        self.select_beaker_first = 0 # 选择烧杯
        self.select_beaker_last = 0  # 选择烧杯

        self.add_metal_flag = False  # 加金属
        self.add_beaker_flag = False  # 放烧杯
        self.add_weight_flag = False  # 加砝码
        self.from_big_to_small_flag = False  # 从大到小
        self.left_object_right_weight_first = 0  # 左物右码
        self.left_object_right_weight_last = 0

        self.set_tweezers_cursors_first = 0
        self.set_tweezers_cursors_last = 0

        self.set_salver_balance_flag = False  # 天平平衡
        self.set_salver_balance_first = 0  # 天平平衡
        self.set_salver_balance_last = 0

        self.set_tweezers_cursors_flag = False
        self.set_tweezers_cursors_info = []
        self.score6 = False

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
        nuts_front, waste_bottles_front, weights_front, weight_boxs_front, salver_balances_front, \
        cursors_front, measuring_cylinders_front, cylinders_bottom_front, water_columns_front, \
        beakers_front, liquids_front = self.preds_front

        hands_top, heads_top, eyes_top, dusters_top, clean_desks_top, salvers_top, weight_tweezers_top, \
        nuts_top, waste_bottles_top, weights_top, weight_boxs_top, salver_balances_top, cursors_top, \
        measuring_cylinders_top, cylinders_bottom_top, water_columns_top, beakers_top, liquids_top = self.preds_top

        hands_side, heads_side, eyes_side, dusters_side, clean_desks_side, salvers_side, weight_tweezers_side, \
        nuts_side, waste_bottles_side, weights_side, weight_boxs_side, salver_balances_side, cursors_side, \
        measuring_cylinders_side, cylinders_bottom_side, water_columns_side, beakers_side, liquids_side = self.preds_side

        front_items = [waste_bottles_front]
        top_items = [salver_balances_top]

        # 如果未得到得分点，则执行函数。
        # 1.将天平放在水平桌面上，用镊子将游码归零
        if not self.scorePoint1 and not self.scorePoint4 \
                and not self.scorePoint5 and not self.scorePoint6 and not self.scorePoint7 and not self.scorePoint8 \
                and not self.scorePoint9:
            if self.cursor_set_zero(weight_tweezers_front, salver_balances_front, cursors_top, cursors_front,
                                    beakers_top, salver_balances_top, weight_tweezers_top, salvers_top, weights_front, weights_top):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.调节平衡螺母使天平平衡
        if not self.scorePoint2 and not self.scorePoint4 and not self.scorePoint5 and \
                not self.scorePoint6 and not self.scorePoint7 and not self.scorePoint8 and not self.scorePoint9:
            if self.nut_balance(salvers_front, beakers_front, salver_balances_top, salver_balances_front, cursors_front,
                                weights_front, hands_front):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.选择小烧杯进行测量
        if not self.scorePoint3 and not self.scorePoint6 and not self.scorePoint7 and \
                not self.scorePoint8 and not self.scorePoint9 :
            if self.select_beaker(salver_balances_front, salvers_front, beakers_front, salver_balances_top, beakers_top, hands_front):
                self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
        # 4.按照左物右码操作
        if self.scorePoint3 and not self.scorePoint4 and not self.scorePoint5 and not self.scorePoint6 and \
                not self.scorePoint7 and not self.scorePoint8 and not self.scorePoint9:
            if self.left_object_right_weight(salver_balances_front, salvers_front, weight_tweezers_front,
                                             beakers_front, weights_front, salver_balances_top, salvers_top,
                                             weight_tweezers_top, beakers_top, weights_top):
                self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
        # 5.从大到小添加游码

        if self.scorePoint3 and not self.scorePoint5 and not self.scorePoint6 and not self.scorePoint7 and \
                not self.scorePoint8 and not self.scorePoint9:
            if self.from_big_to_small(salver_balances_front, salvers_front, weight_tweezers_front,
                                             beakers_front, weights_front, salver_balances_top, salvers_top,
                                             weight_tweezers_top, beakers_top, weights_top):
                self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 6.用镊子移动游码，直至天平平衡
        # 7.读出烧杯和盐水的总质量m
        if self.scorePoint5 and not self.scorePoint6 :
            # if self.set_salver_balance_01(salvers_front, salver_balances_front, beakers_front, weights_front,
            #                               nuts_front, cursors_top, salver_balances_top, weight_tweezers_top,
            #                               salvers_top, weight_tweezers_front):

            if self.set_salver_balance_02(salvers_front, salver_balances_front, beakers_front, weights_front,
                                          nuts_front, cursors_top, salver_balances_top, weight_tweezers_top,
                                          salvers_top, weight_tweezers_front):
                self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                             self.num_frame_front)

        # 8.往量筒中倒入适量的盐水，把量筒放在水平桌面上
        if self.scorePoint5 and not self.scorePoint8 and not self.scorePoint9:
            if self.add_water(8,water_columns_front, beakers_front, measuring_cylinders_front, beakers_top, hands_top,
                              beakers_side, measuring_cylinders_side, liquids_side, liquids_front):
                self.assignScore(8, self.frame_front, self.secs*1000, self.objects_front, self.preds_front,
                             self.num_frame_front)
            # info = self.add_water(8, water_columns_front, beakers_front, measuring_cylinders_front,
            #                       beakers_top, hands_top, beakers_side, measuring_cylinders_side)
            # if info is not None:
            #     self.assignScore(*info)

        # 9.读出量筒中盐水的体积V。
        if (self.scorePoint5 or self.scorePoint8) and not self.scorePoint9:
            info = self.record_V_display(9, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                         beakers_front,eyes_side, heads_side, water_columns_side,measuring_cylinders_side)

            if info is not None:
                self.assignScore(*info)
                if not self.scorePoint8 :
                    info[0] = 8
                    self.assignScore(*info)

        # 10.实验结束后能及时整理器材;能和监考老师文明礼貌交流
        if not self.scorePoint10 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3 or self.scorePoint8 or
                                      self.scorePoint4 or self.scorePoint5 or self.scorePoint6 or self.scorePoint7):
            self.clean_desk(10, top_items, front_items)
        if self.scorePoint10 and len(self.score_list) != 10:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(10)

    # 1.将天平放在水平桌面上，用镊子将游码归零
    def cursor_set_zero(self, weight_tweezers_front, salver_balances_front, cursors_top, cursors_front, beakers_top,
                        salver_balances_top, weight_tweezers_top, salvers_top, weights_front, weights_top):
        # print("步骤1开始赋分")
        # 前视
        if not self.set_cursor_zero_flag:  # 游码未置0
            if salver_balances_front.shape[0] != 0 and salver_balances_top.shape[0] != 0 \
                    and weights_front.shape[0] == 0 and weights_top.shape[0] == 0:
                # 托盘天平、平衡螺母存在
                salver_balance_front_box = salver_balances_front[0][:4]  # 取托盘天平的xyxy
                salver_balance_top_box = salver_balances_top[0][:4]
                if salver_balance_top_box[1] > 0.01 * self.h_front:
                    # print("天平位置摆放正确")
                    if cursors_top.shape[0] != 0: # 顶视游码存在
                        # print("顶视游码存在")
                        if salver_balances_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and salvers_top.shape[0] == 2:
                        # ，顶视托盘天平、砝码镊子、托盘存在
                            salver_balances_top_box = salver_balances_top[0][:4]
                            weight_tweezers_top_box = weight_tweezers_top[0][:4]
                            salvers_top_box1 = salvers_top[0][:4]
                            salvers_top_box2 = salvers_top[1][:4]
                            if beakers_top.shape[0] != 0:  # 顶视存在烧杯
                                # print("顶视存在烧杯")
                                beakers_top_box = beakers_top[0][:4]
                                if not pt_in_box(center_point(beakers_top_box), salver_balances_top_box) and \
                                        abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                        # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
                                        # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) and \

                                    self.set_cursor_zero_flag = True
                                    # print("顶视已移动游码==================================================================")
                            else:  # 顶视不存在烧杯
                                # print("顶视不存在烧杯")
                                if abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                        # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1)
                                        # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2)
                                    self.set_cursor_zero_flag = True
                                    # print("顶视已移动游码===============================================")

                    # elif cursors_top.shape[0] == 0 and cursors_front.shape[0] == 0:  # 前视游码不存在
                    elif cursors_top.shape[0] == 0:
                        # print("顶视游码不存在")
                        if salver_balances_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0 and \
                                salvers_top.shape[0] == 2:
                            # ，顶视托盘天平、砝码镊子、托盘存在
                            salver_balances_top_box = salver_balances_top[0][:4]
                            weight_tweezers_top_box = weight_tweezers_top[0][:4]
                            salvers_top_box1 = salvers_top[0][:4]
                            salvers_top_box2 = salvers_top[1][:4]
                            if beakers_top.shape[0] != 0:  # 顶视存在烧杯
                                # print("顶视存在烧杯")
                                beakers_top_box = beakers_top[0][:4]
                                if not pt_in_box(center_point(beakers_top_box), salver_balances_top_box) and \
                                        abs(center_distance_h(salver_balances_top_box,
                                                              weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(
                                    weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) and \

                                    self.set_cursor_zero_flag = True
                                    # print("顶视已移动游码==================================================================")
                            else:  # 顶视不存在烧杯
                                # print("顶视不存在烧杯")
                                if abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 100 and \
                                        0 < abs(salver_balances_top_box[3] - float(
                                    weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 60:
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1)
                                    # not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2)
                                    self.set_cursor_zero_flag = True
                                    # print("顶视已移动游码===============================================")
                if weight_tweezers_front.shape[0] != 0 :# 前视镊子存在
                    weight_tweezers_front_box = weight_tweezers_front[0][:4]
                    if pt_in_box(center_point(weight_tweezers_front_box),salver_balance_front_box):
                        self.set_cursor_zero_flag = True
                        # print("前视镊子调整游码")


                    # elif cursors_top.shape[0] == 0 and cursors_front.shape[0] != 0:  # 前视游码存在
#                     #     print("顶视游码不存在，前视游码存在")
                    #     cursor_front_box = cursors_front[0][:4]  # 取游标的xyxy
                    #     if center_distance_h(cursor_front_box, salver_balance_front_box) > 0.04 * self.w_front:
                    #         # 水平方向上游标与托盘天平中心点x距离>1920*0.04
                    #         self.set_cursor_zero_first, self.set_cursor_zero_last, flag = \
                    #             self.duration(self.set_cursor_zero_first, 0.8, self.set_cursor_zero_last, 0.1)
                    #         if flag:
                    #             return True
        if self.set_cursor_zero_flag:
            # print("赋分1结束===========================================================")
            return True

    # 2.调节平衡螺母使天平平衡。
    def nut_balance(self, salvers_front, beakers_front, salver_balances_top, salver_balances_front, cursors_front,
                    weights_front, hands_front):
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
                    # hand_front_box1 = hands_front[0][:4]
                    # hand_front_box2 = hands_front[1][:4]
                    if beakers_front.shape[0] != 0:
                        beakers_front_box = beakers_front[0][:4]
                        # print("烧杯存在")
                        if center_distance_v(beakers_front_box, salver_balance_front_box) > 0:
                            if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.015 * self.h_front:
                                # print("托盘和螺母平位置平衡")
                                # print(abs(center_distance_v(salvers_front_box1, salvers_front_box2)))
                                # if not pt_in_box(center_point(hand_front_box1), salver_balance_front_box) and not \
                                #         pt_in_box(center_point(hand_front_box2), salver_balance_front_box):
                                #    # 且双手的中心点都不在托盘天平中
                                if cursors_front.shape[0] != 0:  # 如果游码存在
                                    cursor_front_box = cursors_front[0][:4]  # 取游码的xyxy
                                    # print("游码存在")
                                    if center_distance_h(cursor_front_box, salver_balance_front_box) > 0.03 * self.w_front:
                                        # 水平方向上游标与托盘天平中心点x距离>1920*0.04
                                        # print("游码位置符合")
                                        self.set_zero_balance_first0, self.set_zero_balance_last0, flag0 = \
                                            self.duration(self.set_zero_balance_first0, 1, self.set_zero_balance_last0, 0.5)

                                        if flag0:
                                            self.set_nut_balance_flag = True
                                        # print("天平已平衡——————————————————————————————————————————————")
                                    else:
                                        self.set_nut_balance_flag = False
                                        # print("天平未平衡")
                                # elif self.scorePoint1:
                                else :
                                    # print("游码不存在")
                                    self.set_zero_balance_first1, self.set_zero_balance_last1, flag1 = \
                                        self.duration(self.set_zero_balance_first1, 1, self.set_zero_balance_last1, 0.5)
                                    # print("游码不存在，符合一定时间")
                                    if flag1:
                                        self.set_nut_balance_flag = True
                                        # print("游码没检测到、砝码检测到，天平已平衡++++++++++++++++++++++++++++++++++++++++")

                    else:
                        # print("烧杯不存在")
                        # print(abs(center_distance_v(salvers_front_box1, salvers_front_box2)))
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
                                        self.duration(self.set_zero_balance_first2, 1, self.set_zero_balance_last2, 0.5)
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
                                    self.duration(self.set_zero_balance_first3,1, self.set_zero_balance_last3, 0.5)
                                # print("游码不存在符合一定时间")
                                if flag3:
                                    self.set_nut_balance_flag = True
                                    # print("游码和金属块没检测到，天平已平衡++++++++++++++++++++++++++++++++++++++++")

                if self.set_nut_balance_flag:
                    self.set_zero_balance_first, self.set_zero_balance_last, flag = \
                        self.duration(self.set_zero_balance_first, 1, self.set_zero_balance_last, 0.3)
                    if flag:
                        # print("赋分2完成")
                        return True

    # 3. 选择小烧杯进行测量
    def select_beaker(self, salver_balances_front, salvers_front, beakers_front, salver_balances_top, beakers_top, hands_front):
        self.add_beaker_flag = False
        if not self.add_beaker_flag:
            # print("开始放烧杯")
            if salvers_front.shape[0] == 2 and beakers_front.shape[0] != 0 and salver_balances_front.shape[0] != 0 \
                    and hands_front.shape[0] != 0:
                # 两个托盘与烧杯同时存在
                beakers_front_box = beakers_front[0][:4]
                salver_balances_front_box = salver_balances_front[0][:4]
                if pt_in_box(center_point(beakers_front_box), salver_balances_front_box):
                # if center_distance_h(beakers_front_box, salver_balances_front_box) > 0 and \
                #         center_distance_v(beakers_front_box, salver_balances_front_box) < 0 :
                #     print("前视烧杯在天平中")
                    self.select_beaker_first, self.select_beaker_last, flag_beaker = \
                        self.duration(self.select_beaker_first, 1.5, self.select_beaker_last, 0.5)
                    if flag_beaker:
                        self.add_beaker_flag = True
                        # print("赋分3完成")
                        return True

            elif salver_balances_top.shape[0] != 0 and beakers_top.shape[0] != 0 and hands_front.shape[0] != 0:
                # 两个托盘与烧杯同时存在
                beakers_top_box = beakers_top[0][:4]
                salver_balances_top_box = salver_balances_top[0][:4]
                if pt_in_box(center_point(beakers_top_box), salver_balances_top_box):
                # if center_distance_h(beakers_top_box, salver_balances_top_box) < 0 and \
                #         pt_in_box(center_point(beakers_top_box), salver_balances_top_box):
                #     print("顶视烧杯在左托盘上")
                    self.select_beaker_first, self.select_beaker_last, flag_beaker = \
                        self.duration(self.select_beaker_first, 1.5, self.select_beaker_last, 0.5)
                    if flag_beaker:
                        self.add_beaker_flag = True
                        # print("赋分3完成")
                        return True

    # 4. 按照左物右码操作
    def left_object_right_weight(self, salver_balances_front, salvers_front, weight_tweezers_front, beakers_front,
                                    weights_front, salver_balances_top, salvers_top, weight_tweezers_top, beakers_top,
                                    weights_top):
        self.add_metal_flag = False
        if not self.add_metal_flag:
            # print("开始放烧杯")
            if salvers_front.shape[0] == 2 and beakers_front.shape[0] != 0 and \
                    salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0:
                # 两个托盘与烧杯同时存在
                metal_blocks_front_box = beakers_front[0][:4]
                salver_balances_front_box = salver_balances_front[0][:4]
                weights_front_box = weights_front[0][:4]
                if center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
                        center_distance_h(weights_front_box, salver_balances_front_box) < 0:
                    # print("前视烧杯在右托盘上")
                    self.add_metal_flag = True
            elif salvers_top.shape[0] == 2 and beakers_top.shape[0] != 0 and \
                    salver_balances_top.shape[0] != 0:
                metal_blocks_top_box = beakers_top[0][:4]
                salver_balances_top_box = salver_balances_top[0][:4]
                if center_distance_h(metal_blocks_top_box, salver_balances_top_box) < 0 and \
                        pt_in_box(center_point(metal_blocks_top_box), salver_balances_top_box):
                    # print("顶视烧杯在右托盘上")
                    self.add_metal_flag = True

        if self.add_metal_flag:  # 如果已放烧杯，未放砝码
            if salver_balances_front.shape[0] != 0 and beakers_front.shape[0] != 0 and \
                    weights_front.shape[0] != 0 and weight_tweezers_front.shape[0] != 0:  # 托盘天平与烧杯、镊子、砝码同时存在
                salver_balances_front_box = salver_balances_front[0][:4]
                weight_tweezers_front_box = weight_tweezers_front[0][:4]
                # print("前视已放烧杯，未放砝码")
                for weight_front in weights_front:  # 遍历同时出现的砝码
                    weight_front_box = weight_front[:4]
                    if iou(salver_balances_front_box, weight_front_box) and iou(salver_balances_front_box,
                                                                                weight_tweezers_front_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
                        # print("前视已放砝码")
                        self.add_weight_flag = True
                        # print("赋分5结束")
                        return True
            elif salver_balances_top.shape[0] != 0 and \
                    weights_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0:  # 托盘天平与烧杯、镊子、砝码同时存在
                salver_balances_top_box = salver_balances_top[0][:4]
                weight_tweezers_top_box = weight_tweezers_top[0][:4]
                # print("顶视已放烧杯，未放砝码")
                for weight_top in weights_top:  # 遍历同时出现的砝码
                    weight_top_box = weight_top[:4]
                    if iou(salver_balances_top_box, weight_top_box) and \
                            iou(salver_balances_top_box, weight_tweezers_top_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
                        # print("顶视已放砝码")
                        # print("赋分5结束")
                        self.add_weight_flag = True
                        return True

    # 5. 从大到小添加游码
    def from_big_to_small(self, salver_balances_front, salvers_front, weight_tweezers_front, beakers_front,
                                    weights_front, salver_balances_top, salvers_top, weight_tweezers_top, beakers_top,
                                    weights_top):
        self.from_big_to_small_flag = False
        if not self.from_big_to_small_flag:
            # print("开始放烧杯")
            if salvers_front.shape[0] == 2 and beakers_front.shape[0] != 0 and \
                    salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0:
                # 两个托盘与烧杯同时存在
                metal_blocks_front_box = beakers_front[0][:4]
                salver_balances_front_box = salver_balances_front[0][:4]
                weights_front_box = weights_front[0][:4]
                if (center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
                        center_distance_h(weights_front_box, salver_balances_front_box) < 0) or \
                        (center_distance_h(metal_blocks_front_box, salver_balances_front_box) < 0 and \
                        center_distance_h(weights_front_box, salver_balances_front_box) > 0):
                    # print("前视烧杯在右托盘上")
                    self.from_big_to_small_flag = True
            elif salvers_top.shape[0] == 2 and beakers_top.shape[0] != 0 and \
                    salver_balances_top.shape[0] != 0:
                metal_blocks_top_box = beakers_top[0][:4]
                salver_balances_top_box = salver_balances_top[0][:4]
                if center_distance_h(metal_blocks_top_box, salver_balances_top_box) < 0 and \
                        pt_in_box(center_point(metal_blocks_top_box), salver_balances_top_box):
                    # print("顶视烧杯在右托盘上")
                    self.from_big_to_small_flag = True

        if self.from_big_to_small_flag:  # 如果已放烧杯，未放砝码
            if salver_balances_front.shape[0] != 0 and beakers_front.shape[0] != 0 and \
                    weights_front.shape[0] != 0 and weight_tweezers_front.shape[0] != 0:  # 托盘天平与烧杯、镊子、砝码同时存在
                salver_balances_front_box = salver_balances_front[0][:4]
                weight_tweezers_front_box = weight_tweezers_front[0][:4]
                # print("前视已放烧杯，未放砝码")
                for weight_front in weights_front:  # 遍历同时出现的砝码
                    weight_front_box = weight_front[:4]
                    if iou(salver_balances_front_box, weight_front_box) and iou(salver_balances_front_box,
                                                                                weight_tweezers_front_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
                        # print("前视已放砝码")
                        self.from_big_to_small_flag = True
                        # print("赋分5结束")
                        return True
            elif salver_balances_top.shape[0] != 0 and \
                    weights_top.shape[0] != 0 and weight_tweezers_top.shape[0] != 0:  # 托盘天平与烧杯、镊子、砝码同时存在
                salver_balances_top_box = salver_balances_top[0][:4]
                weight_tweezers_top_box = weight_tweezers_top[0][:4]
                # print("顶视已放烧杯，未放砝码")
                for weight_top in weights_top:  # 遍历同时出现的砝码
                    weight_top_box = weight_top[:4]
                    if iou(salver_balances_top_box, weight_top_box) and \
                            iou(salver_balances_top_box, weight_tweezers_top_box):
                        # 砝码和托盘相交，镊子和托盘天平相交
                        # print("顶视已放砝码")
                        # print("赋分5结束")
                        self.from_big_to_small_flag = True
                        return True

    # 6. 用镊子移动游码，直至天平平衡
    # 7. 读出烧杯和盐水的总质量m
    # def set_salver_balance_01(self, salvers_front, salver_balances_front, beakers_front, weights_front, nuts_front,
    #                        cursors_top, salver_balances_top, weight_tweezers_top, salvers_top, weight_tweezers_front):
    #     self.set_tweezers_cursors_flag = False
    #     if not self.set_tweezers_cursors_flag:
#     #         print("开始移动游码")
    #         if weights_front.shape[0] != 0 or beakers_front.shape[0] != 0:
    #             # 烧杯、砝码存在
#     #             print("前视烧杯和砝码存在")
    #             if salver_balances_top.shape[0] != 0 and salvers_top.shape[0] == 2:
#     #                 print("顶视托盘天平、托盘存在")
    #                 salver_balances_top_box = salver_balances_top[0][:4]
    #                 salvers_top_box1 = salvers_top[0][:4]
    #                 salvers_top_box2 = salvers_top[1][:4]
    #                 if salvers_front.shape[0] == 2 and beakers_front.shape[0] != 0 and \
    #                         salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0 and \
    #                         weight_tweezers_front.shape[0] != 0:
#     #                     print("平衡判定情况1")
    #                     # 两个托盘与烧杯、托盘天平、砝码、镊子同时存在
    #                     weight_tweezers_front_box = weight_tweezers_front[0][:4]
#     #                     print("判断前视镊子位置")
    #                     if pt_in_box(center_point(weight_tweezers_front_box), salver_balances_top_box):
#     #                         print("情况1符合")
    #                         self.set_tweezers_cursors_flag = True
    #                         return True
    #                 elif weight_tweezers_top.shape[0] != 0:  # 顶视镊子存在
    #                     weight_tweezers_top_box = weight_tweezers_top[0][:4]
#     #                     print("平衡判定情况2")
    #                     if salvers_front.shape[0] == 2 and beakers_front.shape[0] != 0 and \
    #                             salver_balances_front.shape[0] != 0 and weights_front.shape[0] != 0:
    #                         # 两个托盘与烧杯同时存在
    #                         metal_blocks_front_box = beakers_front[0][:4]
    #                         salver_balances_front_box = salver_balances_front[0][:4]
    #                         weights_front_box = weights_front[0][:4]
    #                         if center_distance_h(metal_blocks_front_box, salver_balances_front_box) > 0 and \
    #                                 center_distance_h(weights_front_box, salver_balances_front_box) < 0:
#     #                             print("判断顶视镊子位置")
    #                             if not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box1) and \
    #                                     not pt_in_box(center_point(weight_tweezers_top_box), salvers_top_box2) :
    #                                 if abs(center_distance_h(salver_balances_top_box, weight_tweezers_top_box)) < 200 or \
    #                                         0 < abs(salver_balances_top_box[3]-float(weight_tweezers_top_box[3] + weight_tweezers_top_box[1]) / 2) < 200 or \
    #                                         distance_box(weight_tweezers_top_box, salver_balances_top_box) < 400 :
    #                                     # 镊子不在两个托盘中，托盘天平和镊子中心高度差小于120,托盘天平的下y2与镊子的中心点y小于120
#     #                                     print("情况2符合")
    #                                     self.set_tweezers_cursors_flag = True
    #                                     return True
    #
    #                 elif cursors_top.shape[0] != 0:  # 顶视游码存在
    #                     self.set_tweezers_cursors_flag = True
#     #                     print("平衡判定情况3,顶视游码存在")
    #                     return True

    def set_salver_balance_02(self, salvers_front, salver_balances_front, beakers_front, weights_front, nuts_front,
                              cursors_top, salver_balances_top, weight_tweezers_top, salvers_top,
                              weight_tweezers_front):
        # if self.set_tweezers_cursors_flag:
        # print("前视调平中")
        if salvers_front.shape[0] == 2:
            salvers_front_box1 = salvers_front[0][:4]
            salvers_front_box2 = salvers_front[1][:4]
            # print(abs(center_distance_v(salvers_front_box1, salvers_front_box2)))
            if abs(center_distance_v(salvers_front_box1, salvers_front_box2)) < 0.02 * self.h_front:
                # print("正在平衡------------------------------------------")
                if beakers_front.shape[0] != 0 and salver_balances_front.shape[0] != 0 and \
                        weights_front.shape[0] != 0 :
                    # 烧杯砝码同时存在
                    # print("烧杯砝码同时存在")
                    beakers_front_box = beakers_front[0][:4]
                    salver_balances_front_box = salver_balances_front[0][:4]
                    weights_front_box = weights_front[0][:4]
                    if (center_distance_h(beakers_front_box, salver_balances_front_box) > 0 and \
                            center_distance_h(weights_front_box, salver_balances_front_box) < 0 and \
                            iou(beakers_front_box,salver_balances_front_box) > 0) or \
                            (center_distance_h(beakers_front_box, salver_balances_front_box) < 0 and
                            center_distance_h(weights_front_box, salver_balances_front_box) > 0 and
                            iou(beakers_front_box,salver_balances_front_box) > 0):
                        # 支持左物右码和左码右物
                        self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                            self.duration(self.set_salver_balance_first, 2.5, self.set_salver_balance_last,0.5)
                        # print("已调游码,托盘天平平衡")
                        if flag:
                            # print("赋分7完成")
                            return True
                elif beakers_front.shape[0] == 0 and salver_balances_front.shape[0] != 0 and \
                        weights_front.shape[0] != 0 :
                    # print("砝码存在")
                    salver_balances_front_box = salver_balances_front[0][:4]
                    weights_front_box = weights_front[0][:4]
                    if center_distance_h(weights_front_box, salver_balances_front_box) < 0 or \
                            center_distance_h(weights_front_box, salver_balances_front_box) > 0:
                        self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                            self.duration(self.set_salver_balance_first, 2.5, self.set_salver_balance_last,0.5)
                        # print("已调游码,托盘天平平衡")
                        if flag:
                            # print("赋分7完成")
                            return True
                elif beakers_front.shape[0] != 0 and salver_balances_front.shape[0] != 0 and \
                        weights_front.shape[0] == 0 :
                    # print("烧杯存在")
                    beakers_front_box = beakers_front[0][:4]
                    salver_balances_front_box = salver_balances_front[0][:4]
                    if (center_distance_h(beakers_front_box, salver_balances_front_box) > 0 or
                        center_distance_h(beakers_front_box, salver_balances_front_box) < 0) and \
                            iou(beakers_front_box,salver_balances_front_box) > 0:
                        self.set_salver_balance_first, self.set_salver_balance_last, flag = \
                            self.duration(self.set_salver_balance_first, 2.5, self.set_salver_balance_last,0.5)
                        # print("已调游码,托盘天平平衡")
                        if flag:
                            # print("赋分7完成")
                            return True


    # 8. 往量筒中倒入适量的盐水，把量筒放在水平桌面上。
    def add_water(self, score_index, water_columns_front, beakers_front, measuring_cylinders_front,
                  beakers_top, hands_top, beakers_side, measuring_cylinders_side, liquids_side, liquids_front):
        self.beaker_measuring_cylinder_flag = False
        # print("判断倒水动作")
        if beakers_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0:
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            beaker_front_box = beakers_front[0][:4]
            if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
                            iou(beaker_front_box, measuring_cylinder_front_box) > 0:
                # 烧杯y在量筒y上方 烧杯与量筒有交集
                self.beaker_measuring_cylinder_flag = True
                # print("前视赋分8完成")
                return True
        if liquids_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0:
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            liquids_front_box = liquids_front[0][:4]
            if min(liquids_front_box[1], liquids_front_box[3]) < measuring_cylinder_front_box[1] and \
                            iou(liquids_front_box, measuring_cylinder_front_box) > 0:
                # 烧杯y在量筒y上方 烧杯与量筒有交集
                self.beaker_measuring_cylinder_flag = True
                # print("前视赋分8完成")
                return True

        if beakers_side.shape[0] > 0 and measuring_cylinders_side.shape[0] > 0:
            measuring_cylinder_side_box = measuring_cylinders_side[0][:4]
            beaker_side_box = beakers_side[0][:4]
            if min(beaker_side_box[1], beaker_side_box[3]) < measuring_cylinder_side_box[1] and \
                            iou(beaker_side_box, measuring_cylinder_side_box) > 0:
                # 烧杯y在量筒y上方 烧杯与量筒有交集
                self.beaker_measuring_cylinder_flag = True
                # print("侧视烧杯赋分8完成")
                return True
        if liquids_side.shape[0] > 0 and measuring_cylinders_side.shape[0] > 0:
            measuring_cylinder_side_box = measuring_cylinders_side[0][:4]
            liquids_side_box = liquids_side[0][:4]
            if min(liquids_side_box[1], liquids_side_box[3]) < measuring_cylinder_side_box[1] and \
                            iou(liquids_side_box, measuring_cylinder_side_box) > 0:
                # 烧杯y在量筒y上方 烧杯与量筒有交集
                self.beaker_measuring_cylinder_flag = True
                # print("侧视液体赋分8完成")
                return True





        # if water_columns_front.shape[0] > 0 and water_columns_front[0][3] - water_columns_front[0][1] > \
        #         self.h_front * 0.06:  # 水柱存在，y2-y1d大于1080×0.06像素
        #     water_columns_front_box = water_columns_front[0][:4]  # 取水柱xyxy
#         #     print("水柱存在")
        #     if measuring_cylinders_front.shape[0] > 0 and beakers_front.shape[0] > 0:  # 量筒、烧杯存在
        #         measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
        #         beaker_front_box = beakers_front[0][:4]
        #         if iou(water_columns_front_box, measuring_cylinder_front_box):
        #             #self.beaker_measuring_cylinder_flag = True  # 烧杯量筒倒水为True
        #             if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
        #                     iou(beaker_front_box, measuring_cylinder_front_box) > 0:  # 烧杯y在量筒y上方 烧杯与量筒有交集
        #                 self.beaker_measuring_cylinder_flag = False  # 烧杯向量筒倒水未结束
        #                 self.record_add_water_info(score_index, self.frame_front, self.time_front, self.objects_front,
        #                                            self.preds_front, self.num_frame_front,
        #                                            water_columns_front_box, True)
#         #                 print("正在倒水，实时记录量筒中水位高度变化")
        #
        #             if self.beaker_measuring_cylinder_flag:  # 烧杯量筒倒水为True
        #                 self.add_water_first, self.add_water_last, flag = \
        #                     self.duration(self.add_water_first, 3, self.add_water_last, 0.5)
#         #                 print("量筒中已经有水")
        #                 if flag:
        #                     self.record_add_water_info(score_index, self.frame_front, self.time_front,
        #                                                self.objects_front, self.preds_front, self.num_frame_front,
        #                                                water_columns_front_box, True)
#         #                     print("在烧杯向量筒中倒水的列表进行更新")
        #
        #     elif measuring_cylinders_front.shape[0] > 0 and beakers_top.shape[0] > 0 and hands_top.shape[0] != 0:
        #         # 量筒、烧杯、手存在:
#         #         print("顶视量筒和手存在")
        #         measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
        #         beaker_top_box = beakers_top[0][:4]
        #         if iou(water_columns_front_box, measuring_cylinder_front_box):
        #             self.beaker_measuring_cylinder_flag = True  # 烧杯量筒倒水为True
        #             for hand_top in hands_top:
        #                 hand_top_box = hand_top[:4]
        #                 if iou(beaker_top_box, hand_top_box) > 0:
        #                     self.beaker_measuring_cylinder_flag = False  # 烧杯向量筒倒水未结束
        #                     self.record_add_water_info(score_index, self.frame_front, self.time_front, self.objects_front,
        #                                                self.preds_front, self.num_frame_front,
        #                                                water_columns_front_box, True)
#         #                     print("正在倒水，实时记录量筒中水位高度变化")
        #
        #             if self.beaker_measuring_cylinder_flag:  # 烧杯量筒倒水为True
        #                 self.add_water_first, self.add_water_last, flag = \
        #                     self.duration(self.add_water_first, 3, self.add_water_last, 0.2)
#         #                 print("量筒中已经有水")
        #                 if flag:
        #                     self.record_add_water_info(score_index, self.frame_front, self.time_front,
        #                                                self.objects_front, self.preds_front, self.num_frame_front,
        #                                                water_columns_front_box, True)
#         #                     print("在烧杯向量筒中倒水的列表进行更新")
        #
        # if self.add_water_beaker_info:
        #     if self.secs - self.add_water_beaker_info[-1] > 0.5:
#         #         print("烧杯向量筒中倒水列表更新已完成，赋分8已完成")
        #         return self.add_water_beaker_info[:6]
        # elif self.add_water_info:
        #     if self.secs - self.add_water_info[-1] > 0.5:
#         #         print("量筒中水列表更新已完成，赋分8已完成")
        #         return self.add_water_info[:6]

    # 9. 读出量筒中盐水的体积V。
    def record_V_display(self, score_index, measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                         beakers_front,eyes_side, heads_side, water_columns_side,measuring_cylinders_side):
        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0:  # 量筒水柱存在
            # print("9.量筒和水柱存在")
            water_columns_front_box = water_columns_front[0][:4]
            if water_columns_front_box[1] > 0.45 * self.h_front:
                self.see_display(score_index, eyes_front, heads_front, water_columns_front_box, False)
                if self.see_display_info and self.secs - self.see_display_info[-1] > 0.5:
                    return self.see_display_info[:6]
                elif self.see_display_head_info and self.secs - self.see_display_head_info[-1] > 0.5:
                    return self.see_display_head_info[:6]

        if measuring_cylinders_side.shape[0] > 0 and water_columns_side.shape[0] > 0:  # 量筒水柱存在
            # print("9.量筒和水柱存在")
            water_columns_side_box = water_columns_side[0][:4]
            measuring_cylinders_side_box = measuring_cylinders_side[0][:4]
            if 0.45 * self.w_front < water_columns_side_box[2] < 0.9 * self.w_front and\
                    iou(water_columns_side_box,measuring_cylinders_side_box) > 0:
                # self.see_display(score_index, eyes_front, heads_front, water_columns_front_box, False)
            # if measuring_cylinders_front_box[1] > 0.25 * self.h_front and \
            #         abs(center_distance_v(measuring_cylinders_front_box, heads_front_box)) < 0.1 * self.h_front:
            #     print("9.头和量筒位置符合")
                self.see_display2(score_index, eyes_side, heads_side, water_columns_side_box, False)
                # print("执行函数")
                if self.see_display_head_info and self.secs - self.see_display_head_info[-1] > 0.5:
                    return self.see_display_head_info[:6]



    # 看示数
    def see_display(self, score_index, eyes_front, heads_front, water_columns_front_box, block=False):  # 看示数
        water_column_center_point_up = (
            (water_columns_front_box[0] + water_columns_front_box[2]) / 2, water_columns_front_box[1])  # 水柱液面中心
        if eyes_front.shape[0] > 0:  # 眼睛
            eyes_front_box_list = []
            for eye_front in eyes_front:
                eye_front_box = eye_front[:4]
                # print("判断眼睛距离")
                # if abs(center_distance_v(eye_front_box, water_column_center_point_up))< self.h_front * 0.145:
                if distance_point(center_point(eye_front_box), water_column_center_point_up) < self.h_front * 0.385:
                    # print("眼睛和液面距离符合")
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
            if dis_eye_water < self.h_front * 0.14:
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


    def see_display2(self, score_index, eyes_side, heads_side, water_columns_side_box, block=False):  # 看示数
        water_column_center_point_up = (
            (water_columns_side_box[0] + water_columns_side_box[2]) / 2, water_columns_side_box[1])  # 水柱液面中心
        if heads_side.shape[0] > 0:  # 只检测出头
            heads_side_box = []
            dis_head_water = 0
            dis_head_water_h = 0
            for head_side in heads_side:
                head_side_box = head_side[:4]
                # dis_head_water = distance_point(center_point(head_side_box), water_column_center_point_up)
                dis_head_water = abs(center_distance_v(head_side_box, water_columns_side_box))
                dis_head_water_h = abs(center_distance_h(head_side_box, water_columns_side_box))
                # print("判断头与液面距离")
                # print(dis_head_water)
                # print(dis_head_water_h)
                if dis_head_water < self.h_front * 0.18 and dis_head_water_h < self.w_front * 0.4:
                    heads_side_box.append(head_side_box)
                    # print("判断头与液面距离符合，加入队列")
            if len(heads_side_box) == 1:
                # print("57.头与液面距离符合高度差")
                if not block:
                    # print("57.金属块不在水中")
                    self.see_display_first, self.see_display_last, flag = self.duration(self.see_display_first, 0.2)
                    # print("1")
                    if flag:
                        # print("1.5")
                        if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                            # print("2")
                            self.see_display_head_info = [score_index, self.frame_side, self.time_side,
                                                          self.objects_side,
                                                          self.preds_side, self.num_frame_side, dis_head_water,
                                                          self.secs]
                        else:
                            self.see_display_head_info[-1] = self.secs
                            # print("3")

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

    # 10.实验结束后能及时整理器材;能和监考老师文明礼貌交流

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
        if self.clean_desk_info and self.secs - self.clean_desk_info[-1] < 1:
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

    # def duration(self, first_time, duration_time, pre_time=None, reclock_time=None):
    #     if reclock_time:
    #         if self.secs - pre_time > reclock_time:  # n 秒内没有此动作 重新计时
    #             first_time = pre_time = 0.
    #         else:
    #             pre_time = self.secs
    #     if first_time == 0:
    #         if reclock_time:
    #             first_time = pre_time = self.secs
    #         else:
    #             first_time = self.secs
    #         return first_time, pre_time, False
    #     elif self.secs - first_time > duration_time:
    #         return first_time, pre_time, True
    #     else:
    #         return first_time, pre_time, False

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
