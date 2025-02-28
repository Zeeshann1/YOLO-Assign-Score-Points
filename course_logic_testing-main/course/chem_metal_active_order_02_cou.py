#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04/07 15:18
# @Author  : lld
# @File    : chem_metal_active_order_02_cou.py


from .comm import *
from .comm.course_base import ConfigModel

class CHEM_metal_active_order_02(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(CHEM_metal_active_order_02, self).__init__(*args, **kwargs)
        # 各得分点初始化
        self.scorePoint1 = False
        self.scorePoint2 = False

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

        # 1.小试管中盛金属M，加入2滴稀盐酸。
        if not self.scorePoint1:
            if self.add_Metal_HCl(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                                     tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                                     rubber_droppers_front, tube_bottoms_front):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.观察现象：金属M表面______；结论：M的金属活动性比氢______。
        if self.scorePoint1 and not self.scorePoint2:
            if self.observe_Metal(hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                                    tubes_front, tweezers_front, narrow_mouth_bottles_front, eyes_front,
                                    rubber_droppers_front, tube_bottoms_front):
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

    # 1.小试管中盛金属M，加入2滴稀盐酸。

    def add_Metal_HCl(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front,
                         tubes_front,
                         tweezers_front, narrow_mouth_bottles_front, eyes_front, rubber_droppers_front,
                         tube_bottoms_front):
        # 前视

        if not self.add_HCL_flag:

            if plugs_right_front.shape[0] != 0 or plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
                if narrow_mouth_bottles_front.shape[0] != 0 and tubes_front.shape[0] != 0 and \
                        rubber_droppers_front.shape[0] != 0:
                    # 细口瓶、试管、胶头滴管存在
                    narrow_mouth_bottles_front_box = narrow_mouth_bottles_front[0][:4]
                    for rubber_dropper_front in rubber_droppers_front:  # 遍历胶头滴管
                        rubber_dropper_front_box = rubber_dropper_front[:4]
                        if not iou(narrow_mouth_bottles_front_box, rubber_dropper_front_box) and \
                                center_distance_v(rubber_dropper_front_box, narrow_mouth_bottles_front_box):

                            # 如果胶头滴管不和细口瓶相交且在细口瓶上方
                            for tube_front in tubes_front:  # 遍历试管
                                tube_front_box = tube_front[:4]
                                if center_distance_v(rubber_dropper_front_box, tube_front_box) and \
                                        abs(center_distance_h(rubber_dropper_front_box,
                                                              tube_front_box)) < 0.02 * self.w_front:
                                    # 如果胶头滴管中心点在试管中心点上方且两者的横向距离小于0.02*1920
                                    self.add_HCL_flag = True
                                    return True

    # 2.观察现象：金属M表面______；结论：M的金属活动性比氢______。

    def observe_Metal(self, hands_front, wild_mouth_bottles_front, plugs_wrong_front, plugs_right_front, tubes_front,
                          tweezers_front, narrow_mouth_bottles_front, eyes_front, rubber_droppers_front,
                          tube_bottoms_front):
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
