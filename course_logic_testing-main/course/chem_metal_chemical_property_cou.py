#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/03/09 15:18
# @Author  : lld
# @File    : chem_metal_chemical_property.py


from .comm import *


class CHEM_metal_chemical_property(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(CHEM_metal_chemical_property, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.add_Mg_flag = False
        self.Mg_heat_flag = False
        self.add_Fe_flag = False
        self.Fe_heat_flag = False
        self.add_Zn_flag = False
        self.Zn_heat_flag = False
        self.add_Al_flag = False
        self.Al_heat_flag = False
        self.add_Cu_flag = False
        self.Cu_heat_flag = False
        self.tube_Mg_flag = False
        self.Mg_bottle_hand_flag = False
        self.Mg_tube_holder_flag = False
        self.tube_Fe_flag = False
        self.Fe_bottle_hand_flag = False
        self.Fe_tube_holder_flag = False
        self.tube_Zn_flag = False
        self.Zn_bottle_hand_flag = False
        self.Zn_tube_holder_flag = False
        self.tube_Al_flag = False
        self.Al_bottle_hand_flag = False
        self.Al_tube_holder_flag = False
        self.tube_Cu_flag = False
        self.Cu_bottle_hand_flag = False
        self.Cu_tube_holder_flag = False
        self.add_HCL_flag = False

        self.clean_time = 0
        self.clean_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        hands_front, dusters_front, wild_mouth_bottles_front, narrow_mouth_bottles_front, narrow_mouths_front, \
        plugs_wrong_front, plugs_right_front, eyes_front, rubber_droppers_front, tubes_front, tube_mouths_front, \
        tube_bottoms_front, tweezers_front, crucibles_clamp_front, alcohol_lamps_front, flames_front, \
        ignitions_front, tube_holders_front = self.preds_front

        hands_top, dusters_top, wild_mouth_bottles_top, narrow_mouth_bottles_top, narrow_mouths_top, \
        plugs_wrong_top, plugs_right_top, eyes_top, rubber_droppers_top, tubes_top, tube_mouths_top, \
        tube_bottoms_top, tweezers_top, crucibles_clamp_top, alcohol_lamps_top, flames_top, ignitions_top, \
        tube_holders_top = self.preds_top

        front_items = [wild_mouth_bottles_front, narrow_mouth_bottles_front, narrow_mouths_front, plugs_wrong_front,
                       plugs_right_front, eyes_front, rubber_droppers_front, tubes_front, tube_mouths_front,
                       tube_bottoms_front, tweezers_front, crucibles_clamp_front, alcohol_lamps_front, flames_front,
                       ignitions_front, tube_holders_front]

        top_items = [wild_mouth_bottles_top, narrow_mouth_bottles_top, narrow_mouths_top, plugs_wrong_top,
                     plugs_right_top, eyes_top, rubber_droppers_top, tubes_top, crucibles_clamp_top, alcohol_lamps_top,
                     flames_top, ignitions_top, tube_holders_top]

        # 1.用坩埚钳分别夹持一小段镁条、铁钉、锌片、铝片和铜片，用酒精灯外焰加热，观察并记录现象。
        if not self.scorePoint1:
            if self.add_matal_heat(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                                   crucibles_clamp_front,  alcohol_lamps_front, flames_front, wild_mouth_bottles_top,
                                   crucibles_clamp_top):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.另取五支试管，分别加入一小段镁条、铁钉、锌片、铝片和铜片。
        if not self.scorePoint2:
            if self.add_metal(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front, tubes_front,
                              tweezers_front, tube_holders_top, hands_top):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.将五支试管中依次滴加稀盐酸（或稀硫酸）至金属样品完全浸没，观察并记录现象。
        if self.scorePoint2 and not self.scorePoint3:
            if self.add_HCl(hands_front, plugs_wrong_front, plugs_right_front, tubes_front, narrow_mouth_bottles_front,
                            eyes_front, rubber_droppers_front, tube_bottoms_front):
                self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 4.清洗仪器，整理桌面。
        if not self.scorePoint4:
            self.clean_desk(4, top_items, front_items)
        if self.scorePoint4 and len(self.score_list) != 4:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(4)

    # 1.用坩埚钳分别夹持一小段镁条、铁钉、锌片、铝片和铜片，用酒精灯外焰加热，观察并记录现象。

    def add_matal_heat(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                       crucibles_clamp_front, alcohol_lamps_front, flames_front, wild_mouth_bottles_top,
                       crucibles_clamp_top):
        #  夹Mg
        if not self.add_Mg_flag:  # 如果没夹Mg
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 如果不存在瓶塞非倒放或者存在瓶塞倒放
                if flames_front.shape[0] == 0:  # 酒精灯火焰不存在
                    if wild_mouth_bottles_front.shape[0] != 0 and crucibles_clamp_front.shape[0] != 0 and \
                            hands_front.shape[0] != 0:  # 如果广口瓶、坩锅钳、手存在
                        crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                        for hand_front in hands_front:  # 遍历手
                            hand_front_box = hand_front[:4]  # 取手坐标
                            for wild_mouth_bottle_front in wild_mouth_bottles_front:  # 遍历广口瓶
                                wild_mouth_bottle_front_box = wild_mouth_bottle_front[:4]  # 取广口瓶坐标
                                if iou(hand_front_box, wild_mouth_bottle_front_box) > 0:  # 如果手和广口瓶相交
                                    if iou(crucibles_clamp_front_box, wild_mouth_bottle_front_box) > 0 and \
                                            center_distance_v(wild_mouth_bottle_front_box,
                                                              crucibles_clamp_front_box) > 0:
                                        # 如果坩锅钳和广口瓶相交且坩锅钳高于广口瓶
                                        self.add_Mg_flag = True  # 已夹Mg
                                        # print("前视已夹Mg")
                                    else:
                                        self.add_Mg_flag = False

            if wild_mouth_bottles_top.shape[0] != 0 and crucibles_clamp_top.shape[0] != 0:  # 顶视广口瓶、坩锅钳存在
                crucibles_clamp_top_box = crucibles_clamp_top[0][:4]
                for wild_mouth_bottle_top in wild_mouth_bottles_top:  # 遍历广口瓶
                    wild_mouth_bottle_top_box = wild_mouth_bottle_top[:4]
                    if iou(crucibles_clamp_top_box, wild_mouth_bottle_top_box) > 0:  # 广口瓶和坩锅钳相交
                        self.add_Mg_flag = True
                        # print("顶视已夹Mg")
                        break

        if self.add_Mg_flag and not self.Mg_heat_flag:  # 已夹Mg且未加热
            if crucibles_clamp_front.shape[0] != 0 and alcohol_lamps_front.shape[0] != 0 and \
                    flames_front.shape[0] != 0:  # 坩锅钳存在、酒精灯存在、酒精灯火焰存在
                crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                alcohol_lamps_front_box = alcohol_lamps_front[0][:4]  # 取酒精灯坐标
                flames_front_box = flames_front[0][:4]  # 取火焰坐标
                if iou(crucibles_clamp_front_box, flames_front_box) and \
                        center_distance_v(alcohol_lamps_front_box, crucibles_clamp_front_box):  # 火焰与坩锅钳相交且坩锅钳在酒精灯上方
                    self.Mg_heat_flag = True  # Mg 已经加热
                    # print("前视Mg已加热")
        # 夹Fe
        if self.Mg_heat_flag and not self.add_Fe_flag:  #
            if flames_front.shape[0] == 0:  # 酒精灯火焰不存在
                if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 如果不存在瓶塞非倒放或者存在瓶塞倒放
                    if wild_mouth_bottles_front.shape[0] != 0 and crucibles_clamp_front.shape[0] != 0 and \
                            hands_front.shape[0] != 0:  # 如果广口瓶、坩锅钳、手存在
                        crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                        for hand_front in hands_front:  # 遍历手
                            hand_front_box = hand_front[:4]  # 取手坐标
                            for wild_mouth_bottle_front in wild_mouth_bottles_front:  # 遍历广口瓶
                                wild_mouth_bottle_front_box = wild_mouth_bottle_front[:4]  # 取广口瓶坐标
                                if iou(hand_front_box, wild_mouth_bottle_front_box) > 0:  # 如果手和广口瓶相交
                                    if iou(crucibles_clamp_front_box, wild_mouth_bottle_front_box) > 0 and \
                                            center_distance_v(wild_mouth_bottle_front_box,
                                                              crucibles_clamp_front_box) > 0:
                                        # 如果坩锅钳和广口瓶相交且坩锅钳高于广口瓶
                                        self.add_Fe_flag = True  # 已夹Fe
                                        # print("前视已夹Fe")
                                    else:
                                        self.add_Fe_flag = False

            if wild_mouth_bottles_top.shape[0] != 0 and crucibles_clamp_top.shape[0] != 0:  # 顶视广口瓶、坩锅钳存在
                crucibles_clamp_top_box = crucibles_clamp_top[0][:4]
                for wild_mouth_bottle_top in wild_mouth_bottles_top:
                    wild_mouth_bottle_top_box = wild_mouth_bottle_top[:4]
                    if iou(crucibles_clamp_top_box, wild_mouth_bottle_top_box) > 0:
                        self.add_Fe_flag = True
                        # print("顶视已夹Fe")
                        break

        if self.add_Fe_flag and not self.Fe_heat_flag:  # 已夹Fe且未加热
            if crucibles_clamp_front.shape[0] != 0 and alcohol_lamps_front.shape[0] != 0 and \
                    flames_front.shape[0] != 0:  # 坩锅钳存在、酒精灯存在、酒精灯火焰存在
                crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                alcohol_lamps_front_box = alcohol_lamps_front[0][:4]  # 取酒精灯坐标
                flames_front_box = flames_front[0][:4]  # 取火焰坐标
                if iou(crucibles_clamp_front_box, flames_front_box) and \
                        center_distance_v(alcohol_lamps_front_box, crucibles_clamp_front_box):  # 火焰与坩锅钳相交且坩锅钳在酒精灯上方
                    self.Fe_heat_flag = True  # Fe 已经加热
                    # print("前视Fe已加热")

        # Zn夹取
        if self.Fe_heat_flag and not self.add_Zn_flag:  # 如果没夹Zn
            if flames_front.shape[0] == 0:  # 酒精灯火焰不存在
                if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 如果不存在瓶塞非倒放或者存在瓶塞倒放
                    if wild_mouth_bottles_front.shape[0] != 0 and crucibles_clamp_front.shape[0] != 0 and \
                            hands_front.shape[0] != 0:  # 如果广口瓶、坩锅钳、手存在
                        crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                        for hand_front in hands_front:  # 遍历手
                            hand_front_box = hand_front[:4]  # 取手坐标
                            for wild_mouth_bottle_front in wild_mouth_bottles_front:  # 遍历广口瓶
                                wild_mouth_bottle_front_box = wild_mouth_bottle_front[:4]  # 取广口瓶坐标
                                if iou(hand_front_box, wild_mouth_bottle_front_box) > 0:  # 如果手和广口瓶相交
                                    if iou(crucibles_clamp_front_box, wild_mouth_bottle_front_box) > 0 and \
                                            center_distance_v(wild_mouth_bottle_front_box,
                                                              crucibles_clamp_front_box) > 0:
                                        # 如果坩锅钳和广口瓶相交且坩锅钳高于广口瓶
                                        self.add_Zn_flag = True  # 已夹Zn
                                        # print("前视已夹Zn")
                                    else:
                                        self.add_Zn_flag = False

            if wild_mouth_bottles_top.shape[0] != 0 and crucibles_clamp_top.shape[0] != 0:  # 顶视广口瓶、坩锅钳存在
                crucibles_clamp_top_box = crucibles_clamp_top[0][:4]
                for wild_mouth_bottle_top in wild_mouth_bottles_top:
                    wild_mouth_bottle_top_box = wild_mouth_bottle_top[:4]
                    if iou(crucibles_clamp_top_box, wild_mouth_bottle_top_box) > 0:
                        self.add_Zn_flag = True
                        # print("顶视已夹Zn")
                        break

        if self.add_Zn_flag and not self.Zn_heat_flag:  # 已夹Zn且未加热
            if crucibles_clamp_front.shape[0] != 0 and alcohol_lamps_front.shape[0] != 0 and \
                    flames_front.shape[0] != 0:  # 坩锅钳存在、酒精灯存在、酒精灯火焰存在
                crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                alcohol_lamps_front_box = alcohol_lamps_front[0][:4]  # 取酒精灯坐标
                flames_front_box = flames_front[0][:4]  # 取火焰坐标
                if iou(crucibles_clamp_front_box, flames_front_box) and \
                        center_distance_v(alcohol_lamps_front_box, crucibles_clamp_front_box):  # 火焰与坩锅钳相交且坩锅钳在酒精灯上方
                    self.Zn_heat_flag = True  # Zn 已经加热
                    # print("前视Zn已加热")

        # 夹Al
        if self.Zn_heat_flag and not self.add_Al_flag:  # 如果没夹Al
            if flames_front.shape[0] == 0:  # 酒精灯火焰不存在
                if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 如果不存在瓶塞非倒放或者存在瓶塞倒放
                    if wild_mouth_bottles_front.shape[0] != 0 and crucibles_clamp_front.shape[0] != 0 and \
                            hands_front.shape[0] != 0:  # 如果广口瓶、坩锅钳、手存在
                        crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                        for hand_front in hands_front:  # 遍历手
                            hand_front_box = hand_front[:4]  # 取手坐标
                            for wild_mouth_bottle_front in wild_mouth_bottles_front:  # 遍历广口瓶
                                wild_mouth_bottle_front_box = wild_mouth_bottle_front[:4]  # 取广口瓶坐标
                                if iou(hand_front_box, wild_mouth_bottle_front_box) > 0:  # 如果手和广口瓶相交
                                    if iou(crucibles_clamp_front_box, wild_mouth_bottle_front_box) > 0 and \
                                            center_distance_v(wild_mouth_bottle_front_box,
                                                              crucibles_clamp_front_box) > 0:
                                        # 如果坩锅钳和广口瓶相交且坩锅钳高于广口瓶
                                        self.add_Al_flag = True  # 已夹Al
                                        # print("前视已夹Al")
                                    else:
                                        self.add_Al_flag = False

            if wild_mouth_bottles_top.shape[0] != 0 and crucibles_clamp_top.shape[0] != 0:  # 顶视广口瓶、坩锅钳存在
                crucibles_clamp_top_box = crucibles_clamp_top[0][:4]
                for wild_mouth_bottle_top in wild_mouth_bottles_top:
                    wild_mouth_bottle_top_box = wild_mouth_bottle_top[:4]
                    if iou(crucibles_clamp_top_box, wild_mouth_bottle_top_box) > 0:
                        self.add_Al_flag = True
                        # print("顶视已夹Al")
                        break

        if self.add_Al_flag and not self.Al_heat_flag:  # 已夹Al且未加热
            if crucibles_clamp_front.shape[0] != 0 and alcohol_lamps_front.shape[0] != 0 and \
                    flames_front.shape[0] != 0:  # 坩锅钳存在、酒精灯存在、酒精灯火焰存在
                crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                alcohol_lamps_front_box = alcohol_lamps_front[0][:4]  # 取酒精灯坐标
                flames_front_box = flames_front[0][:4]  # 取火焰坐标
                if iou(crucibles_clamp_front_box, flames_front_box) and \
                        center_distance_v(alcohol_lamps_front_box, crucibles_clamp_front_box):  # 火焰与坩锅钳相交且坩锅钳在酒精灯上方
                    self.Al_heat_flag = True  # Al 已经加热
                    # print("前视Al已加热")

        # 夹Cu
        if self.Al_heat_flag and not self.add_Cu_flag:  # 如果没夹Cu
            if flames_front.shape[0] == 0:  # 酒精灯火焰不存在
                if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 如果不存在瓶塞非倒放或者存在瓶塞倒放
                    if wild_mouth_bottles_front.shape[0] != 0 and crucibles_clamp_front.shape[0] != 0 and \
                            hands_front.shape[0] != 0:  # 如果广口瓶、坩锅钳、手存在
                        crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                        for hand_front in hands_front:  # 遍历手
                            hand_front_box = hand_front[:4]  # 取手坐标
                            for wild_mouth_bottle_front in wild_mouth_bottles_front:  # 遍历广口瓶
                                wild_mouth_bottle_front_box = wild_mouth_bottle_front[:4]  # 取广口瓶坐标
                                if iou(hand_front_box, wild_mouth_bottle_front_box) > 0:  # 如果手和广口瓶相交
                                    if iou(crucibles_clamp_front_box, wild_mouth_bottle_front_box) > 0 and \
                                            center_distance_v(wild_mouth_bottle_front_box,
                                                              crucibles_clamp_front_box) > 0:
                                        # 如果坩锅钳和广口瓶相交且坩锅钳高于广口瓶
                                        self.add_Cu_flag = True  # 已夹Cu
                                        # print("前视已夹Cu")
                                    else:
                                        self.add_Cu_flag = False

            if wild_mouth_bottles_top.shape[0] != 0 and crucibles_clamp_top.shape[0] != 0:  # 顶视广口瓶、坩锅钳存在
                crucibles_clamp_top_box = crucibles_clamp_top[0][:4]
                for wild_mouth_bottle_top in wild_mouth_bottles_top:
                    wild_mouth_bottle_top_box = wild_mouth_bottle_top[:4]
                    if iou(crucibles_clamp_top_box, wild_mouth_bottle_top_box) > 0:
                        self.add_Cu_flag = True
                        # print("顶视已夹Cu")

        if self.add_Cu_flag and not self.Cu_heat_flag:  # 已夹Cu且未加热
            if crucibles_clamp_front.shape[0] != 0 and alcohol_lamps_front.shape[0] != 0 and \
                    flames_front.shape[0] != 0:  # 坩锅钳存在、酒精灯存在、酒精灯火焰存在
                crucibles_clamp_front_box = crucibles_clamp_front[0][:4]  # 取坩锅钳坐标
                alcohol_lamps_front_box = alcohol_lamps_front[0][:4]  # 取酒精灯坐标
                flames_front_box = flames_front[0][:4]  # 取火焰坐标

                if iou(crucibles_clamp_front_box, flames_front_box) and \
                        center_distance_v(alcohol_lamps_front_box, crucibles_clamp_front_box):  # 火焰与坩锅钳相交且坩锅钳在酒精灯上方
                    self.Cu_heat_flag = True  # Cu 已经加热
                    # print("前视Cu已加热")

        if self.Cu_heat_flag:
            # print("赋分1完成")
            return True

    # 2.另取五支试管，分别加入一小段镁条、铁钉、锌片、铝片和铜片。
    def add_metal(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front, tubes_front, \
                  tweezers_front, tube_holders_top, hands_top):
        # 前视
        # 试管加入Mg
        if not self.tube_Mg_flag:
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
                if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and \
                        tubes_front.shape[0] != 0 and hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                    # print(2.11)
                    tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                    wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                    hands_front_boxs = []  # 建立手的空列表
                    hand_tweezer_flag = False  # 设置手抓镊子标志
                    for hand_front in hands_front:  # 遍历出现的所有手
                        hand_front_box = hand_front[:4]  # 取手的xyxy
                        if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                            # print(2.12)
                            if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                    iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                                # print(2.13)
                                hand_tweezer_flag = True  # 手抓镊子为True
                            else:
                                # print(2.14)
                                hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                    if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                        # print(2.15)
                        if center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0:
                            # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                            # print(2.16)
                            if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                                # print(2.17)
                                tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                            else:  # 否则镊子在放入试管中
                                # print(2.18)
                                tweezer_tube_flag = False  # 镊子和试管相交标志为False
                                for tube_front in tubes_front:  # 遍历试管
                                    tube_front_box = tube_front[:4]  # 取试管xyxy
                                    hand_tube_flag = False  # 手拿试管
                                    for hand_front_box in hands_front_boxs:  # 遍历手
                                        if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                            # print(2.19)
                                            hand_tube_flag = True  # 手和试管相交标志为True
                                            tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                            break  # 跳出当前遍历
                                if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                    self.tube_Mg_flag = True
                                    # print("前视已夹Mg到试管中")

        if self.tube_Mg_flag and not self.Mg_tube_holder_flag:  # Mg已装入试管中，未将Mg试管放到试管架上
            if tube_holders_top.shape[0] != 0 and hands_top.shape[0] != 0:  # 试管架、手存在
                tube_holders_top_box = tube_holders_top[0][:4]
                hands_top_box = hands_top[0][:4]
                if iou(tube_holders_top_box, hands_top_box) > 0:  # 手和试管架相交
                    self.Mg_tube_holder_flag = True
                    # print("顶视已将Mg试管放到试管架上")

        # if self.tube_Mg_flag and not self.Mg_bottle_hand_flag:  # Mg已装入试管中，手未放好Mg瓶
        #     if wild_mouth_bottles_front.shape[0] != 0 and hands_front.shape[0] != 0:
        #         wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
        #         for hand_front in hands_front:  # 遍历出现的所有手
        #             hand_front_box = hand_front[:4]  # 取手的xyxy
        #             if iou(wild_mouth_bottle_front_box, hand_front_box):   # 手和广口瓶相交
        #                 self.Mg_bottle_hand_flag = True
#         #                 print("已放好Mg瓶")

        # 试管加入Fe
        if self.Mg_tube_holder_flag and not self.tube_Fe_flag:
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
                if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and \
                        tubes_front.shape[0] != 0 and hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                    # print(2.21)
                    tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                    wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                    hands_front_boxs = []  # 建立手的空列表
                    hand_tweezer_flag = False  # 设置手抓镊子标志
                    for hand_front in hands_front:  # 遍历出现的所有手
                        hand_front_box = hand_front[:4]  # 取手的xyxy
                        if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                            # print(2.22)
                            if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                    iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                                # print(2.23)
                                hand_tweezer_flag = True  # 手抓镊子为True
                            else:
                                # print(2.24)
                                hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                    if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                        # print(2.25)
                        if center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0:
                            # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                            # print(2.26)
                            if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                                # print(2.27)
                                tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                            else:  # 否则镊子在放入试管中
                                # print(2.28)
                                tweezer_tube_flag = False  # 镊子和试管相交标志为False
                                for tube_front in tubes_front:  # 遍历试管
                                    tube_front_box = tube_front[:4]  # 取试管xyxy
                                    hand_tube_flag = False  # 手拿试管
                                    for hand_front_box in hands_front_boxs:  # 遍历手
                                        if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                            # print(2.29)
                                            hand_tube_flag = True  # 手和试管相交标志为True
                                            tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                            break  # 跳出当前遍历
                                if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                    self.tube_Fe_flag = True
                                    # print("前视已夹Fe到试管中")

        if self.tube_Fe_flag and not self.Fe_tube_holder_flag:  # Fe已装入试管中，未将Fe试管放到试管架上
            if tube_holders_top.shape[0] != 0 and hands_top.shape[0] != 0:  # 试管架、手存在
                tube_holders_top_box = tube_holders_top[0][:4]
                hands_top_box = hands_top[0][:4]
                if iou(tube_holders_top_box, hands_top_box) > 0:  # 手和试管架相交
                    self.Fe_tube_holder_flag = True
                    # print("顶视已将Fe试管放到试管架上")

        # if self.tube_Fe_flag and not self.Fe_bottle_hand_flag:  # Fe已装入镊子中，手未放好Fe瓶
        #     if wild_mouth_bottles_front.shape[0] != 0 and hands_front.shape[0] != 0:
        #         wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
        #         for hand_front in hands_front:  # 遍历出现的所有手
        #             hand_front_box = hand_front[:4]  # 取手的xyxy
        #             if iou(wild_mouth_bottle_front_box, hand_front_box):   # 手和广口瓶相交
        #                 self.Fe_bottle_hand_flag = True
#         #                 print("已放好Fe瓶")

        # 试管加入Zn
        if self.Fe_tube_holder_flag and not self.tube_Zn_flag:
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置

                if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and \
                        tubes_front.shape[0] != 0 and hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                    # print(2.31)
                    tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                    wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                    hands_front_boxs = []  # 建立手的空列表
                    hand_tweezer_flag = False  # 设置手抓镊子标志
                    for hand_front in hands_front:  # 遍历出现的所有手
                        hand_front_box = hand_front[:4]  # 取手的xyxy
                        if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                            # print(2.32)
                            if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                    iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                                # print(2.33)
                                hand_tweezer_flag = True  # 手抓镊子为True
                            else:
                                # print(2.34)
                                hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                    if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                        # print(2.35)
                        if center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0:
                            # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                            # print(2.36)
                            if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                                # print(2.37)
                                tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                            else:  # 否则镊子在放入试管中
                                # print(2.38)
                                tweezer_tube_flag = False  # 镊子和试管相交标志为False
                                for tube_front in tubes_front:  # 遍历试管
                                    tube_front_box = tube_front[:4]  # 取试管xyxy
                                    hand_tube_flag = False  # 手拿试管
                                    for hand_front_box in hands_front_boxs:  # 遍历手
                                        if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                            # print(2.39)
                                            hand_tube_flag = True  # 手和试管相交标志为True
                                            tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                            break  # 跳出当前遍历
                                if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                    self.tube_Zn_flag = True
                                    # print("前视已夹Zn到试管中")

        if self.tube_Zn_flag and not self.Zn_tube_holder_flag:  # Zn已装入试管中，未将Zn试管放到试管架上
            if tube_holders_top.shape[0] != 0 and hands_top.shape[0] != 0:  # 试管架、手存在
                tube_holders_top_box = tube_holders_top[0][:4]
                hands_top_box = hands_top[0][:4]
                if iou(tube_holders_top_box, hands_top_box) > 0:  # 手和试管架相交
                    self.Zn_tube_holder_flag = True
                    # print("顶视已将Zn试管放到试管架上")

        # if self.tube_Zn_flag and not self.Zn_bottle_hand_flag:  # Zn已装入镊子中，手未放好Zn瓶
        #     if wild_mouth_bottles_front.shape[0] != 0 and hands_front.shape[0] != 0:
        #         wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
        #         for hand_front in hands_front:  # 遍历出现的所有手
        #             hand_front_box = hand_front[:4]  # 取手的xyxy
        #             if iou(wild_mouth_bottle_front_box, hand_front_box):   # 手和广口瓶相交
        #                 self.Zn_bottle_hand_flag = True
#         #                 print("已放好Zn瓶")

        # 试管加入Al
        if self.Zn_tube_holder_flag and not self.tube_Al_flag:
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置

                if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and \
                        tubes_front.shape[0] != 0 and hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                    # print(2.41)
                    tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                    wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                    hands_front_boxs = []  # 建立手的空列表
                    hand_tweezer_flag = False  # 设置手抓镊子标志
                    for hand_front in hands_front:  # 遍历出现的所有手
                        hand_front_box = hand_front[:4]  # 取手的xyxy
                        if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                            # print(2.42)
                            if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                    iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                                # print(2.43)
                                hand_tweezer_flag = True  # 手抓镊子为True
                            else:
                                # print(2.44)
                                hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                    if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                        # print(2.45)
                        if center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0:
                            # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                            # print(2.46)
                            if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                                # print(2.47)
                                tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                            else:  # 否则镊子在放入试管中
                                # print(2.48)
                                tweezer_tube_flag = False  # 镊子和试管相交标志为False
                                for tube_front in tubes_front:  # 遍历试管
                                    tube_front_box = tube_front[:4]  # 取试管xyxy
                                    hand_tube_flag = False  # 手拿试管
                                    for hand_front_box in hands_front_boxs:  # 遍历手
                                        if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                            # print(2.49)
                                            hand_tube_flag = True  # 手和试管相交标志为True
                                            tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                            break  # 跳出当前遍历
                                if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                    self.tube_Al_flag = True
                                    # print("前视已夹Al到试管中")

        if self.tube_Al_flag and not self.Al_tube_holder_flag:  # Al已装入试管中，未将Al试管放到试管架上
            if tube_holders_top.shape[0] != 0 and hands_top.shape[0] != 0:  # 试管架、手存在
                tube_holders_top_box = tube_holders_top[0][:4]
                hands_top_box = hands_top[0][:4]
                if iou(tube_holders_top_box, hands_top_box) > 0:  # 手和试管架相交
                    self.Al_tube_holder_flag = True
                    # print("顶视已将Al试管放到试管架上")

        # if self.tube_Al_flag and not self.Al_bottle_hand_flag:  # Al已装入镊子中，手未放好Al瓶
        #     if wild_mouth_bottles_front.shape[0] != 0 and hands_front.shape[0] != 0:
        #         wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
        #         for hand_front in hands_front:  # 遍历出现的所有手
        #             hand_front_box = hand_front[:4]  # 取手的xyxy
        #             if iou(wild_mouth_bottle_front_box, hand_front_box):   # 手和广口瓶相交
        #                 self.Al_bottle_hand_flag = True
#         #                 print("已放好Al瓶")

        # 试管加入Cu
        if self.Al_tube_holder_flag and not self.tube_Cu_flag:
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置

                if tweezers_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and \
                        tubes_front.shape[0] != 0 and hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
                    # print(2.51)
                    tweezer_front_box = tweezers_front[0][:4]  # 取镊子xyxy
                    wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶金属
                    hands_front_boxs = []  # 建立手的空列表
                    hand_tweezer_flag = False  # 设置手抓镊子标志
                    for hand_front in hands_front:  # 遍历出现的所有手
                        hand_front_box = hand_front[:4]  # 取手的xyxy
                        if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                            # print(2.52)
                            if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                                    iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                                # print(2.53)
                                hand_tweezer_flag = True  # 手抓镊子为True
                            else:
                                # print(2.54)
                                hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
                    if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                        # print(2.55)
                        if center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0:
                            # 镊子高于广口瓶：可能在夹金属也可能镊子在放入试管中
                            # print(2.56)
                            if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶中夹金属,相交
                                # print(2.57)
                                tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                            else:  # 否则镊子在放入试管中
                                # print(2.58)
                                tweezer_tube_flag = False  # 镊子和试管相交标志为False
                                for tube_front in tubes_front:  # 遍历试管
                                    tube_front_box = tube_front[:4]  # 取试管xyxy
                                    hand_tube_flag = False  # 手拿试管
                                    for hand_front_box in hands_front_boxs:  # 遍历手
                                        if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交，手拿试管
                                            # print(2.59)
                                            hand_tube_flag = True  # 手和试管相交标志为True
                                            tweezer_tube_flag = True  # 镊子和试管相交标志为True
                                            break  # 跳出当前遍历
                                if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                                    self.tube_Cu_flag = True
                                    # print("前视已夹Cu到试管中")

        if self.tube_Cu_flag and not self.Cu_tube_holder_flag:  # Cu已装入试管中，未将Cu试管放到试管架上
            if tube_holders_top.shape[0] != 0 and hands_top.shape[0] != 0:  # 试管架、手存在
                tube_holders_top_box = tube_holders_top[0][:4]
                hands_top_box = hands_top[0][:4]
                if iou(tube_holders_top_box, hands_top_box) > 0:  # 手和试管架相交
                    self.Cu_tube_holder_flag = True
                    # print("顶视已将Cu试管放到试管架上")

                    # if self.tube_Cu_flag and not self.Cu_bottle_hand_flag:  # Cu已装入镊子中，手未放好Cu瓶
                    #     if wild_mouth_bottles_front.shape[0] != 0 and hands_front.shape[0] != 0:
                    #         wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
                    #         for hand_front in hands_front:  # 遍历出现的所有手
                    #             hand_front_box = hand_front[:4]  # 取手的xyxy
                    #             if iou(wild_mouth_bottle_front_box, hand_front_box):   # 手和广口瓶相交
                    #                 self.Cu_bottle_hand_flag = True
                    # # print("已放好Cu瓶")
                    # print("赋分2完成")
                    return True

    # 3.将五支试管中依次滴加稀盐酸（或稀硫酸）至金属样品完全浸没，观察并记录现象。

    def add_HCl(self, hands_front, plugs_wrong_front, plugs_right_front, tubes_front, narrow_mouth_bottles_front,
                eyes_front, rubber_droppers_front, tube_bottoms_front):
        # 前视

        if not self.add_HCL_flag:
            # print(3.1)
            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
                # print(3.2)
                if narrow_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                        rubber_droppers_front.shape[0] != 0:
                    # 细口瓶、试管、胶头滴管存在
                    narrow_mouth_bottles_front_box = narrow_mouth_bottles_front[0][:4]
                    # print(3.3)
                    for rubber_dropper_front in rubber_droppers_front:  # 遍历胶头滴管
                        rubber_dropper_front_box = rubber_dropper_front[:4]
                        if not iou(narrow_mouth_bottles_front_box, rubber_dropper_front_box) and \
                                center_distance_v(rubber_dropper_front_box, narrow_mouth_bottles_front_box) :

                            # 如果胶头滴管不和细口瓶相交且在细口瓶上方
                            # print(3.4)
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]
                                if center_distance_v(rubber_dropper_front_box, tube_front_box) and \
                                        abs(center_distance_h(rubber_dropper_front_box, tube_front_box)) < 0.02 * self.w_front:
                                    # 如果胶头滴管中心点在试管中心点上方且两者的横向距离小于0.02*1920
                                    # print(3.5)
                                    self.add_HCL_flag = True
                                    break
                            break
        if self.add_HCL_flag:
            hands_no_droppers_flag = False
            # print(3.6)
            if rubber_droppers_front.shape[0] != 0 and hands_front.shape[0] != 0:
                rubber_droppers_front_box = rubber_droppers_front[0][:4]
                hands_front_box = hands_front[0][:4]
                # print(3.7)
                if iou(rubber_droppers_front_box, hands_front_box) == 0:
                    hands_no_droppers_flag = True
                    # print(3.8)
            elif rubber_droppers_front.shape[0] == 0:
                hands_no_droppers_flag = True
                # print(3.9)
            else :
                hands_no_droppers_flag = False
                # print(3.10)
            if hands_no_droppers_flag:
                # print(3.11)
                if tubes_front.shape[0] != 0 and eyes_front.shape[0] != 0 and hands_front.shape[0] != 0 and \
                        tube_bottoms_front.shape[0] != 0:   # 试管底部、试管、眼睛、手存在
                    eyes_front_box = eyes_front[0][:4]
                    tube_bottoms_front_box = tube_bottoms_front[0][:4]
                    # print(3.12)
                    for hand_front in hands_front:  # 遍历手
                        hand_front_box = hand_front[:4]
                        for tube_front in tubes_front:  # 遍历试管
                            tube_front_box = tube_front[:4]
                            # print(3.13)
                            if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交
                                # print(3.14)
                                if center_distance_v(eyes_front_box, tube_bottoms_front_box) > 0 or \
                                        center_distance_v(eyes_front_box, tube_front_box) > 0:  # 试管底部在眼睛上方或者试管中心点在眼睛上方
                                    # print(3.15)
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
