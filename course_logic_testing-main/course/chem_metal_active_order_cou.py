#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/03/07 15:18
# @Author  : lld
# @File    : chem_metal_active_order_cou.py


from .comm import *
from .comm.course_base import ConfigModel

class CHEM_metal_active_order(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(CHEM_metal_active_order, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False

        self.add_Fe_Cu_Ag_flag = False
        self.add_HCL_flag = False
        self.add_Fe_Ag_flag = False
        self.add_CuSO4_flag = False
        self.add_Fe_Cu_flag = False
        self.add_AgNO3_flag = False

        self.clean_time = 0
        self.clean_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        hands_front, dusters_front, wild_mouth_bottles_front, narrow_mouth_bottles_front, narrow_mouths_front, \
        plugs_wrong_front, plugs_right_front, eyes_front, rubber_droppers_front, tubes_front, tube_mouths_front, \
        tube_bottoms_front, tweezers_front = self.preds_front

        hands_top, dusters_top, wild_mouth_bottles_top, narrow_mouth_bottles_top, narrow_mouths_top, plugs_wrong_top, \
        plugs_right_top, eyes_top, rubber_droppers_top, tubes_top, tube_mouths_top, tube_bottoms_top, \
        tweezers_top = self.preds_top

        front_items = [wild_mouth_bottles_front, narrow_mouth_bottles_front,
                       narrow_mouths_front, plugs_wrong_front, plugs_right_front, eyes_front, rubber_droppers_front,
                       tubes_front, tube_mouths_front, tube_bottoms_front, tweezers_front]

        top_items = [wild_mouth_bottles_top, narrow_mouth_bottles_top, narrow_mouths_top,
                     plugs_wrong_top, plugs_right_top, eyes_top, rubber_droppers_top, tubes_top, tube_mouths_top,
                     tube_bottoms_top, tweezers_top]

        # 1.将铁丝、铜丝、银粒分别放入3支试管中，各加入约2ml稀盐酸或稀硫酸，观察并记录现象。
        if not self.scorePoint1:
            if self.add_Fe_Cu_Ag_HCl(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                                     tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                                     rubber_droppers_front, tube_bottoms_front):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.将铁丝、银粒分别放入2支试管中，各加入约2ml硫酸铜溶液，观察并记录现象。
        if self.scorePoint1 and not self.scorePoint2:
            if self.add_Fe_Ag_CuSO4(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                                    tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                                    rubber_droppers_front, tube_bottoms_front):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.将铁丝、铜丝分别放入2支试管中，各加入约2ml硝酸银溶液，观察并记录现象。
        if self.scorePoint2 and not self.scorePoint3:
            if self.add_Fe_Cu_AgNO3(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                                    tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                                    rubber_droppers_front, tube_bottoms_front):
                self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 4.清洗仪器，整理桌面。
        if not self.scorePoint4:
            self.clean_desk(4, top_items, front_items)
        if self.scorePoint4 and len(self.score_list) != 4:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(4)

    # 1.将铁丝、铜丝、银粒分别放入3支试管中，各加入约2ml稀盐酸或稀硫酸，观察并记录现象。

    def add_Fe_Cu_Ag_HCl(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                         tubes_front,
                         tweezers_front, narrow_mouth_bottles_front, eyes_front, rubber_droppers_front,
                         tube_bottoms_front):
        # 前视
        if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
 # print(1.1)
            if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and \
                    tubes_front.shape[0] != 0 and hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
# print(1.2)
                tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                hands_front_boxs = []  # 建立手的空列表
                hand_tweezer_flag = False  # 设置手抓镊子标志
                for hand_front in hands_front:  # 遍历出现的所有手
                    hand_front_box = hand_front[:4]  # 取手的xyxy
                    if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
# print(1.3)
                        if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
# print(1.4)
                            hand_tweezer_flag = True  # 手抓镊子为True
                        else:
# print(1.5)
                            hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
# print(1.6)
                    if center_distance_v(wild_mouth_bottle_front_box,
                                         tweezer_front_box) > 0:  # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
# print(1.7)
                        if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
# print(1.8)
                            tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                        else:  # 否则镊子在放入试管中
 # print(1.9)
                            tweezer_tube_flag = False  # 镊子和试管相交标志为False
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]  # 取试管xyxy
                                hand_tube_flag = False  # 手拿试管
                                for hand_front_box in hands_front_boxs:  # 遍历手
                                    if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
 # print(1.10)
                                        hand_tube_flag = True  # 手和试管相交标志为True
                                        tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                        break  # 跳出当前遍历
                            if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                self.add_Fe_Cu_Ag_flag = True
#                                 # print(1.11)

        if self.add_Fe_Cu_Ag_flag and not self.add_HCL_flag:
# print(1.12)
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
 # print(1.13)
                if narrow_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                        rubber_droppers_front.shape[0] != 0:
                    # 细口瓶、试管、胶头滴管存在
                    narrow_mouth_bottles_front_box = narrow_mouth_bottles_front[0][:4]
                    # print(1.14)
                    for rubber_dropper_front in rubber_droppers_front:  # 遍历胶头滴管
                        rubber_dropper_front_box = rubber_dropper_front[:4]
                        if not iou(narrow_mouth_bottles_front_box, rubber_dropper_front_box) and \
                                center_distance_v(rubber_dropper_front_box, narrow_mouth_bottles_front_box):

                            # 如果胶头滴管不和细口瓶相交且在细口瓶上方
                            # print(1.15)
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]
                                if center_distance_v(rubber_dropper_front_box, tube_front_box) and \
                                        abs(center_distance_h(rubber_dropper_front_box,
                                                              tube_front_box)) < 0.02 * self.w_front:
                                    # 如果胶头滴管中心点在试管中心点上方且两者的横向距离小于0.02*1920
                                    # print(1.16)
                                    self.add_HCL_flag = True
                                    break
                            break
        if self.add_HCL_flag:
            hands_no_droppers_flag = False
            # print(1.17)
            if rubber_droppers_front.shape[0] != 0 and hands_front.shape[0] != 0:
                rubber_droppers_front_box = rubber_droppers_front[0][:4]
                hands_front_box = hands_front[0][:4]
                # print(1.18)
                if iou(rubber_droppers_front_box, hands_front_box) == 0:
                    hands_no_droppers_flag = True
                    # print(1.181)
            elif rubber_droppers_front.shape[0] == 0:
                hands_no_droppers_flag = True
                # print(1.19)
            else:
                hands_no_droppers_flag = False
                # print(1.20)
            if hands_no_droppers_flag:
                # print(1.21)
                if tubes_front.shape[0] != 0 and eyes_front.shape[0] != 0 and hands_front.shape[0] != 0 and \
                        tube_bottoms_front.shape[0] != 0:  # 试管底部、试管、眼睛、手存在
                    eyes_front_box = eyes_front[0][:4]
                    tube_bottoms_front_box = tube_bottoms_front[0][:4]
                    # print(1.23)
                    for hand_front in hands_front:  # 遍历手
                        hand_front_box = hand_front[:4]
                        for tube_front in tubes_front:  # 遍历试管
                            tube_front_box = tube_front[:4]
                            # print(1.24)
                            if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交
                                # print(1.25)
                                if center_distance_v(eyes_front_box, tube_bottoms_front_box) > 0 or \
                                        center_distance_v(eyes_front_box,
                                                          tube_front_box) > 0:  # 试管底部在眼睛上方或者试管中心点在眼睛上方
                                    # print(1.26)
                                    return True

    # 2.将铁丝、银粒分别放入2支试管中，各加入约2ml硫酸铜溶液，观察并记录现象。

    def add_Fe_Ag_CuSO4(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                        tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                        rubber_droppers_front, tube_bottoms_front):
        # 前视

        if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
            # print(2.1)
            if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[
                0] != 0 and \
                    hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                # print(2.2)
                tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                hands_front_boxs = []  # 建立手的空列表
                hand_tweezer_flag = False  # 设置手抓镊子标志
                for hand_front in hands_front:  # 遍历出现的所有手
                    hand_front_box = hand_front[:4]  # 取手的xyxy
                    if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                        # print(2.3)
                        if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                            # print(2.4)
                            hand_tweezer_flag = True  # 手抓镊子为True
                        else:
                            # print(2.5)
                            hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                    # print(2.6)
                    if center_distance_v(wild_mouth_bottle_front_box,
                                         tweezer_front_box) > 0:  # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                        # print(2.7)
                        if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                            # print(2.8)
                            tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                        else:  # 否则镊子在放入试管中
                            # print(2.9)
                            tweezer_tube_flag = False  # 镊子和试管相交标志为False
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]  # 取试管xyxy
                                hand_tube_flag = False  # 手拿试管
                                for hand_front_box in hands_front_boxs:  # 遍历手
                                    if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                        # print(2.10)
                                        hand_tube_flag = True  # 手和试管相交标志为True
                                        tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                        break  # 跳出当前遍历
                            if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                self.add_Fe_Ag_flag = True
                                # print(2.11)

        if self.add_Fe_Ag_flag and not self.add_CuSO4_flag:
            # print(2.12)
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
                # print(2.13)
                if narrow_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                        rubber_droppers_front.shape[0] != 0:
                    # 细口瓶、试管、胶头滴管存在
                    narrow_mouth_bottles_front_box = narrow_mouth_bottles_front[0][:4]
                    # print(2.14)
                    for rubber_dropper_front in rubber_droppers_front:  # 遍历胶头滴管
                        rubber_dropper_front_box = rubber_dropper_front[:4]
                        if not iou(narrow_mouth_bottles_front_box, rubber_dropper_front_box) and \
                                center_distance_v(rubber_dropper_front_box, narrow_mouth_bottles_front_box):

                            # 如果胶头滴管不和细口瓶相交且在细口瓶上方
                            # print(2.15)
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]
                                if center_distance_v(rubber_dropper_front_box, tube_front_box) and \
                                        abs(center_distance_h(rubber_dropper_front_box,
                                                              tube_front_box)) < 0.02 * self.w_front:
                                    # 如果胶头滴管中心点在试管中心点上方且两者的横向距离小于0.02*1920
                                    # print(2.16)
                                    self.add_CuSO4_flag = True
                                    break
                            break
        if self.add_CuSO4_flag:
            hands_no_droppers_flag = False
            # print(2.17)
            if rubber_droppers_front.shape[0] != 0 and hands_front.shape[0] != 0:
                rubber_droppers_front_box = rubber_droppers_front[0][:4]
                hands_front_box = hands_front[0][:4]
                # print(2.18)
                if iou(rubber_droppers_front_box, hands_front_box) == 0:
                    hands_no_droppers_flag = True
                    # print(2.181)
            elif rubber_droppers_front.shape[0] == 0:
                hands_no_droppers_flag = True
                # print(2.19)
            else:
                hands_no_droppers_flag = False
                # print(2.20)
            if hands_no_droppers_flag:
                # print(2.21)
                if tubes_front.shape[0] != 0 and eyes_front.shape[0] != 0 and hands_front.shape[0] != 0 and \
                        tube_bottoms_front.shape[0] != 0:  # 试管、眼睛、手存在
                    eyes_front_box = eyes_front[0][:4]
                    tube_bottoms_front_box = tube_bottoms_front[0][:4]
                    # print(2.23)
                    for hand_front in hands_front:  # 遍历手
                        hand_front_box = hand_front[:4]
                        for tube_front in tubes_front:  # 遍历试管
                            tube_front_box = tube_front[:4]
                            # print(2.24)
                            if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交
                                # print(2.25)
                                if center_distance_v(eyes_front_box, tube_bottoms_front_box) > 0 or \
                                        center_distance_v(eyes_front_box,
                                                          tube_front_box) > 0:  # 试管底部在眼睛上方或者试管中心点在眼睛上方
                                    # print(2.26)
                                    return True

    # 3.将铁丝、铜丝分别放入2支试管中，各加入约2ml硝酸银溶液，观察并记录现象。

    def add_Fe_Cu_AgNO3(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                        tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                        rubber_droppers_front, tube_bottoms_front):
        # 前视

        if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
            # print(3.1)
            if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[
                0] != 0 and \
                    hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                # print(3.2)
                tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                hands_front_boxs = []  # 建立手的空列表
                hand_tweezer_flag = False  # 设置手抓镊子标志
                for hand_front in hands_front:  # 遍历出现的所有手
                    hand_front_box = hand_front[:4]  # 取手的xyxy
                    if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                        # print(3.3)
                        if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                            # print(3.4)
                            hand_tweezer_flag = True  # 手抓镊子为True
                        else:
                            # print(3.5)
                            hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                    # print(3.6)
                    if center_distance_v(wild_mouth_bottle_front_box,
                                         tweezer_front_box) > 0:  # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                        # print(3.7)
                        if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                            # print(3.8)
                            tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                        else:  # 否则镊子在放入试管中
                            # print(3.9)
                            tweezer_tube_flag = False  # 镊子和试管相交标志为False
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]  # 取试管xyxy
                                hand_tube_flag = False  # 手拿试管
                                for hand_front_box in hands_front_boxs:  # 遍历手
                                    if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                        # print(3.10)
                                        hand_tube_flag = True  # 手和试管相交标志为True
                                        tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                        break  # 跳出当前遍历
                            if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                self.add_Fe_Cu_flag = True
                                # print(3.11)

        if self.add_Fe_Cu_flag and not self.add_AgNO3_flag:
            # print(3.12)
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
                # print(3.13)
                if narrow_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                        rubber_droppers_front.shape[0] != 0:
                    # 细口瓶、试管、胶头滴管存在
                    narrow_mouth_bottles_front_box = narrow_mouth_bottles_front[0][:4]
                    # print(3.14)
                    for rubber_dropper_front in rubber_droppers_front:  # 遍历胶头滴管
                        rubber_dropper_front_box = rubber_dropper_front[:4]
                        if not iou(narrow_mouth_bottles_front_box, rubber_dropper_front_box) and \
                                center_distance_v(rubber_dropper_front_box, narrow_mouth_bottles_front_box):

                            # 如果胶头滴管不和细口瓶相交且在细口瓶上方
                            # print(3.15)
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]
                                if center_distance_v(rubber_dropper_front_box, tube_front_box) and \
                                        abs(center_distance_h(rubber_dropper_front_box,
                                                              tube_front_box)) < 0.02 * self.w_front:
                                    # 如果胶头滴管中心点在试管中心点上方且两者的横向距离小于0.02*1920
                                    # print(3.16)
                                    self.add_AgNO3_flag = True
                                    break
                            break
        if self.add_AgNO3_flag:
            hands_no_droppers_flag = False
            # print(3.17)
            if rubber_droppers_front.shape[0] != 0 and hands_front.shape[0] != 0:
                rubber_droppers_front_box = rubber_droppers_front[0][:4]
                hands_front_box = hands_front[0][:4]
                # print(3.18)
                if iou(rubber_droppers_front_box, hands_front_box) == 0:
                    hands_no_droppers_flag = True
                    # print(3.181)
            elif rubber_droppers_front.shape[0] == 0:
                hands_no_droppers_flag = True
                # print(3.19)
            else:
                hands_no_droppers_flag = False
                # print(3.20)
            if hands_no_droppers_flag:
                # print(3.21)
                if tubes_front.shape[0] != 0 and eyes_front.shape[0] != 0 and hands_front.shape[0] != 0 and \
                        tube_bottoms_front.shape[0] != 0:  # 试管、眼睛、手存在
                    eyes_front_box = eyes_front[0][:4]
                    tube_bottoms_front_box = tube_bottoms_front[0][:4]
                    # print(3.23)
                    for hand_front in hands_front:  # 遍历手
                        hand_front_box = hand_front[:4]
                        for tube_front in tubes_front:  # 遍历试管
                            tube_front_box = tube_front[:4]
                            # print(3.24)
                            if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交
                                # print(3.25)
                                if center_distance_v(eyes_front_box, tube_bottoms_front_box) > 0 or \
                                        center_distance_v(eyes_front_box,
                                                          tube_front_box) > 0:  # 试管底部在眼睛上方或者试管中心点在眼睛上方
                                    # print(3.26)
                                    return True

    # 4. 清洗仪器，整理桌面。
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
