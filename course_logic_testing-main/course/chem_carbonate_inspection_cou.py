#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/03/07 15:18
# @Author  : lld
# @File    : chem_carbonate_inspection_cou.py


from .comm import *
from .comm.course_base import ConfigModel

class CHEM_carbonate_inspection(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(CHEM_carbonate_inspection, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False

        self.add_CaOH2_info = []  # 加入CaOH2
        self.marble_tube_on_base_info = []  # 大理石试管放在铁架台上
        self.CO2_clear_limewater_info = []
        self.clear_limewater_turbid_info = []

        self.clear_limewater_turbid_first = 0
        self.clear_limewater_turbid_last = 0
        self.clean_time = 0
        self.clean_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        hands_front, duster_front, wild_mouth_bottles_front, narrow_mouth_bottles_front, narrow_mouths_front, \
        plug_wrong_front, plug_right_front, label_front, marbles_front, tubes_front, tubes_mouth_front, \
        tube_stand_front, tweezer_front, base_front, iron_bar_front, iron_clamp_front, iron_clamp_head_front, \
        conduit_90_short_front, conduit_90_length_front, rubber_hose_front, clear_liquid_front, \
        bubble_reaction_front, caco3_h2o_front = self.preds_front

        hands_top, duster_top, wild_mouth_bottle_top, narrow_mouth_bottle_top, narrow_mouth_top, plug_wrong_top, \
        plug_right_top, label_top, marble_top, tube_top, tube_mouth_top, tube_stand_top, tweezer_top, base_top, \
        iron_bar_top, iron_clamp_top, iron_clamp_head_top, conduit_90_short_top, conduit_90_length_top, \
        rubber_hose_top, clear_liquid_top, bubble_reaction_top, caco3_h2o_top = self.preds_top

        front_items = [wild_mouth_bottles_front, narrow_mouth_bottles_front,
                       narrow_mouths_front, plug_wrong_front, plug_right_front, label_front, marbles_front,
                       tubes_front, tubes_mouth_front, tube_stand_front, tweezer_front, base_front, iron_bar_front,
                       iron_clamp_front, iron_clamp_head_front, conduit_90_short_front, conduit_90_length_front,
                       rubber_hose_front, clear_liquid_front, bubble_reaction_front, caco3_h2o_front]

        top_items = [wild_mouth_bottle_top, narrow_mouth_bottle_top, narrow_mouth_top,
                     plug_wrong_top, plug_right_top, label_top, marble_top, tube_top, tube_mouth_top,
                     tube_stand_top, tweezer_top, base_top, iron_bar_top, iron_clamp_top, iron_clamp_head_top,
                     conduit_90_short_top, conduit_90_length_top, rubber_hose_top, clear_liquid_top,
                     bubble_reaction_top, caco3_h2o_top]

        # 1.在小试管中加入石灰水，置于试管架上待用。
        if not self.scorePoint1:
            if self.add_CaOH2(hands_front, plug_wrong_front, plug_right_front, narrow_mouth_bottles_front,
                              narrow_mouths_front, tubes_front, tubes_mouth_front, clear_liquid_front, marbles_front):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.取一小块大理石于大试管中。
        if not self.scorePoint2:
            if self.add_marble(tweezer_front, wild_mouth_bottles_front, tubes_front,  hands_front, marbles_front):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.将其固定于铁架台上。
        if not self.scorePoint3:
            if self.marble_tube_on_base(marbles_front, tubes_front, iron_clamp_head_front):
                self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
        # 4.向大试管中加入稀盐酸。
        if not self.scorePoint4:
            if self.add_HCl(plug_wrong_front, narrow_mouth_bottles_front, narrow_mouths_front, tubes_mouth_front,
                            marbles_front, iron_clamp_head_front, iron_clamp_front):
                self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 5.将带导管的橡皮塞迅速塞禁大试管，将导管深入小试管的石灰水中。
        if not self.scorePoint5:
            if self.add_CO2_clear_limewater(conduit_90_length_front, tubes_front, clear_liquid_front,
                                            bubble_reaction_front):
                self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 6.澄清石灰水变浑浊。
        if not self.scorePoint6:
            if self.clear_limewater_turbid(caco3_h2o_front, tubes_front, conduit_90_length_front, clear_liquid_front,
                                           rubber_hose_front):
                self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 7.拆卸装置，清洗仪器，整理桌面。
        if not self.scorePoint7:
            self.clean_desk(7, top_items, front_items)
        if self.scorePoint7 and len(self.score_list) != 7:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(7)

    # 1.在小试管中加入石灰水，置于试管架上待用。

    def add_CaOH2(self, hands_front, plug_wrong_front, plug_right_front, narrow_mouth_bottles_front,
                  narrow_mouths_front, tubes_front, tubes_mouth_front, clear_liquid_front, marbles_front):
        # print("得分点1赋分开始")
        # 前视
        if plug_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
            if narrow_mouth_bottles_front.shape[0] != 0 and narrow_mouths_front.shape[0] != 0 and \
                    tubes_front.shape[0] != 0 and tubes_mouth_front.shape[0] != 0 and hands_front.shape[0] != 0 and \
                    marbles_front.shape[0] == 0:
                # print("细口瓶、细口瓶口、试管、试管口存在,大理石不存在")
                # 细口瓶、细口瓶口、试管、试管口存在,大理石不存在
                for narrow_mouth_bottle_front in narrow_mouth_bottles_front:  # 遍历出现的细口瓶
                    narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]  # 取细口瓶的xyxy
                    if pt_in_polygon(center_point(narrow_mouth_bottle_front_box), self.center_area_front):  # 细口瓶在操作区域内
                        narrow_mouth_front_box = None  # 初始设置无细口瓶口
                        # print("细口瓶在操作区域内")
                        for narrow_mouth_front in narrow_mouths_front:  # 遍历细口瓶口
                            narrow_mouth_front_box = narrow_mouth_front[:4]  # 取细口瓶口xyxy
                            if iou(narrow_mouth_front_box, narrow_mouth_bottle_front_box):  # 细口瓶和细口瓶口相交（证明是同一个细口瓶）
                                # print("细口瓶和细口瓶口相交")
                                break
                            else:
                                narrow_mouth_front_box = None
                        if narrow_mouth_front_box is not None:  # 有细口瓶口
                            # print("有细口瓶口")
                            for tube_front in tubes_front:  # 遍历出现的试管
                                tube_front_box = tube_front[:4]
                                if pt_in_polygon(center_point(tube_front_box), self.center_area_front) and \
                                        center_distance_v(tube_front_box, narrow_mouth_bottle_front_box) > 0:
                                    # 试管在操作区域,细口瓶高于试管
                                    for tube_mouth_front in tubes_mouth_front:  # 遍历出现的试管口
                                        tube_mouth_front_box = tube_mouth_front[:4]
                                        if iou(tube_front_box, tube_mouth_front_box) > 0:  # 试管口和试管相交且一一对应
                                            if iou(tube_mouth_front_box, narrow_mouth_front_box) > 0:  # 试管口和细口瓶口相交
                                                # if clear_liquid_front.shape[0] !=0 :# 澄清液体存在
                                                # clear_liquid_front_box = clear_liquid_front[0][:4]
                                                # print(1.5)
                                                # if iou(clear_liquid_front_box, tube_front_box) >0 :#澄清液体和试管相交
                                                # print(1.6)
                                                # print("试管口和细口瓶口相交")
                                                # return Ture
                                                if not self.add_CaOH2_info:  # 如果该列表不空
                                                    self.add_CaOH2_info = [1, self.frame_front, self.time_front,
                                                                           self.objects_front, self.preds_front,
                                                                           self.num_frame_front, time.time()]  # 添加列表中信息
                                                    # print("加入CaOH2列表存在")
                                                else:
                                                    self.add_CaOH2_info[-1] = time.time()
                                                    # print("新创建加入CaOH2列表")
        if self.add_CaOH2_info and time.time() - self.add_CaOH2_info[-1] > 0.3:  # 延迟赋分
            # print("得分点1赋分结束")
            return True

    # 2.取一小块大理石于大试管中。
    def add_marble(self, tweezer_front, wild_mouth_bottles_front, tubes_front, hands_front, marbles_front):
        # print("得分点2赋分开始")
        # 前视
        if tweezer_front.shape[0] != 0 and wild_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                hands_front.shape[0] > 1:  # 镊子、广口瓶、试管、手存在
            tweezer_front_box = tweezer_front[0][:4]  # 取镊子xyxy
            wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]  # 取广口瓶（大理石）
            hands_front_boxs = []  # 建立手的空列表
            hand_tweezer_flag = False  # 设置手抓镊子标志
            # print("镊子、广口瓶、试管、手存在")
            for hand_front in hands_front:  # 遍历出现的所有手
                hand_front_box = hand_front[:4]  # 取手的xyxy
                if pt_in_polygon(center_point(hand_front_box), self.center_area_front):  # 当此手的中心点在前视操作区域中
                    if min_dis_boxes(hand_front_box, tweezer_front_box) < self.h_front * 0.02 or \
                            iou(hand_front_box, tweezer_front_box):  # 手和镊子不相交框的最短距离小于1080×0.02或者两框相交
                        hand_tweezer_flag = True  # 手抓镊子为True
                        # print("手抓镊子")
                    else:
                        hands_front_boxs.append(hand_front_box)  # 否则将不符合的hand box存放到列表末尾
            # if hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
            if len(hands_front_boxs) > 0 and hand_tweezer_flag:  # 手拿镊子列表不为空且手抓镊子为True
                # print("手拿镊子列存在")
                if center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0:  # 镊子高于广口瓶，可能在夹大理石可能在放入试管中
                    if iou(tweezer_front_box, wild_mouth_bottle_front_box) > 0:  # 镊子在广口瓶(大理石)中,相交
                        tweezer_bottle_flag = True  # 设置镊子和瓶子相交标志
                        # print("镊子与广口瓶相交")
                    else:  # 否则镊子在放入试管中
                        tweezer_tube_flag = False  # 镊子和试管相交标志为False
                        # print("镊子与广口瓶不相交")
                        for tube_front in tubes_front:  # 遍历试管
                            tube_front_box = tube_front[:4]  # 取试管xyxy
                            hand_tube_flag = False  # 手拿试管
                            for hand_front_box in hands_front_boxs:  # 遍历手
                                if iou(hand_front_box, tube_front_box) > 0:  # 试管和手相交
                                    hand_tube_flag = True  # 手和试管相交标志为True
                                    # print("手拿试管")
                                    return True
                        #             if marbles_front.shape[0] != 0:  # 大理石存在
                        #                 for marble_front in marbles_front:
                        #                     marble_front_box = marble_front[:4]
                        #                     if iou(marble_front_box, tube_front_box) > 0:
                        #                         tweezer_tube_flag = True
                        #                         print("大理石存在")
                        #                         break  # 跳出当前遍历
                        # if tweezer_tube_flag and hand_tube_flag:  # 手拿试管、镊子和试管
                        #     return

    # 3.将其固定于铁架台上。
    # 前视
    def marble_tube_on_base(self, marbles_front, tubes_front, iron_clamp_head_front):
        if marbles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and iron_clamp_head_front.shape[0] != 0:
            # 大理石、试管、铁夹头存在
            iron_clamp_head_front_box = iron_clamp_head_front[0][:4]  # 取铁夹头xyxy
            marble_front_box = marbles_front[0][:4]  # 取大理石xyxy
            # print("大理石存在")
            for tube_front in tubes_front:  # 遍历试管
                tube_front_box = tube_front[:4]  # 取试管xyxy
                if iou(iron_clamp_head_front_box, tube_front_box) > 0 and \
                        pt_in_box(center_point(marble_front_box), tube_front_box) and \
                        center_distance_v(tube_front_box, iron_clamp_head_front_box) > self.h_front * 0.06:
                    # 铁夹头和试管相交、大理石在试管中、铁夹头在试管上方>0.02×1080
                    return True
        #             if not self.marble_tube_on_base_info:
        #                 self.marble_tube_on_base_info = [1, time.time()]  # 添加列表中信息
        #                 print("试管放在铁架台上列表存在")
        #             else:
        #                 self.marble_tube_on_base_info[-1] = time.time()
        #                 print("更新试管放在铁架台上列表存在")
        # if self.marble_tube_on_base_info and time.time() - self.marble_tube_on_base_info[-1] > 1:
        #     print("得分点3赋分结束")
        #     return True

    # 4. 向大试管中加入稀盐酸。
    # 前视
    def add_HCl(self, plug_wrong_front, narrow_mouth_bottles_front, narrow_mouths_front, tubes_mouth_front,
                marbles_front, iron_clamp_head_front, iron_clamp_front):
        if narrow_mouth_bottles_front.shape[0] != 0 and narrow_mouths_front.shape[0] != 0 and \
                iron_clamp_head_front.shape[0] != 0 and iron_clamp_front.shape[0] != 0 and \
                tubes_mouth_front.shape[0] != 0 and plug_wrong_front.shape[0] == 0:  # 细口瓶、细口瓶口、铁夹头、铁夹存在，瓶塞没有倒放
            iron_clamp_head_front_box = iron_clamp_head_front[0][:4]  # 铁夹头xyxy
            iron_clamp_front_box = iron_clamp_front[:4]  # 铁夹xyxy
            bottle_tube_flag = False  # 瓶子和试管标志
            for narrow_mouth_front in narrow_mouths_front:  # 遍历细口瓶口
                narrow_mouth_front_box = narrow_mouth_front[:4]  # 取细口瓶口xyxy
                if center_distance_v(iron_clamp_head_front_box, narrow_mouth_front_box) or \
                        center_distance_v(iron_clamp_front_box, narrow_mouth_front_box):
                    # 如果细口瓶口高于铁夹或者高于铁夹头
                    for tube_mouth_front in tubes_mouth_front:  # 遍历试管口
                        tube_front_mouth_box = tube_mouth_front[:4]  # 取试管口xyxy
                        if iou(tube_front_mouth_box, narrow_mouth_front_box) > 0:  # 试管口和细口瓶口相交
                            bottle_tube_flag = True
            if bottle_tube_flag and marbles_front.shape[0] != 0:
                return True  # 赋分

    # 5. 将带导管的橡皮塞迅速塞进大试管，将导管深入小试管的石灰水中。
    def add_CO2_clear_limewater(self, conduit_90_length_front, tubes_front, clear_liquid_front, bubble_reaction_front):
        # 前视
        if conduit_90_length_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                clear_liquid_front.shape[0] != 0 and bubble_reaction_front.shape[0] != 0:  # 长导管、试管、澄清试剂、气泡反应存在
            conduit_90_length_front_box = conduit_90_length_front[0][:4]  # 取长导管xyxy
            clear_liquid_front_box = clear_liquid_front[0][:4]
            # print("长导管、试管、澄清试剂、气泡反应存在")
            for tube_front in tubes_front:  # 遍历试管
                tube_front_box = tube_front[:4]  # 取试管xyxy
                if pt_in_polygon(center_point(tube_front_box), self.center_area_front):  # 长导管中心点在操作区域
                    if iou(conduit_90_length_front_box, tube_front_box) > 0 and \
                            pt_in_box(center_point(clear_liquid_front_box), tube_front_box):  # 长导管与试管相交且澄清试剂中心点在试管中
                        # print("长导管与试管相交且澄清试剂中心点在试管中")
                        return True
                    #     if not self.CO2_clear_limewater_info:
                    #         self.CO2_clear_limewater_info = [1, time.time()]  # 添加列表中信息
                    #         print("CO2通入清水列表存在")
                    #     else:
                    #         self.CO2_clear_limewater_info[-1] = time.time()
                    #         print("更新CO2通入清水列表存在")
                    # if self.CO2_clear_limewater_info and time.time() - self.CO2_clear_limewater_info[-1] > 0.5:
                    #     print("得分点5赋分结束")
                    #     return True

    # 6.观察并记录现象，得出结论。（澄清石灰水变浑浊）
    def clear_limewater_turbid(self, caco3_h2o_front, tubes_front, conduit_90_length_front, clear_liquid_front,
                               rubber_hose_front):
        # 前视
        # if self.CO2_clear_limewater_info and time.time() - self.CO2_clear_limewater_info[-1] > 5:  # 通入CO2后经过10秒
        #     print("通入CO2后经过10秒")
        if caco3_h2o_front.shape[0] != 0 and tubes_front.shape[0] != 0 and rubber_hose_front.shape[0] != 0 and \
                conduit_90_length_front.shape[0] != 0 and clear_liquid_front.shape[0] == 0:
            # 石灰水浑浊 试管 长直角导管、试管夹存在， 澄清试剂不存在
            # print("石灰水浑浊、试管、长直角导管、试管夹存在，澄清试剂不存在")
            conduit_90_length_front_box = conduit_90_length_front[0][:4]
            for tube_front in tubes_front:  # 遍历试管
                tube_front_box = tube_front[:4]
                if pt_in_polygon(center_point(tube_front_box), self.center_area_front):  # 试管中心点在操作区域中
                    if iou(conduit_90_length_front_box, tube_front_box) > 0:  # 长导管与试管相交
                        # return True
                        self.clear_limewater_turbid_first, self.clear_limewater_turbid_last, flag = \
                            self.duration(self.clear_limewater_turbid_first, 0.5, self.clear_limewater_turbid_last, 0.3)

                        # print("已调游码,托盘天平平衡")
                        if flag:
                            # print("赋分3完成")
                            return True

    # 7. 拆卸装置，清洗仪器，整理桌面。
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
#         '''print实际相当于sys.stdout.write'''
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         pass
#
#
# sys.stdout = Logger('/home/xiding/new_aiexhibition_windows-master/test_log/log.txt')  # 调用print时相当于Logger().write()
