#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04/23 11:18
# @Author  : lld
# @File    : bio_breathe_CO2_change_cou.py
"""

"""

from .comm import *
from .comm.course_base import ConfigModel

class BIO_breathe_CO2_change(ConfigModel):  # 继承course_base.py中类ConfigModel
    def __init__(self, *args, **kwargs):
        super(BIO_breathe_CO2_change, self).__init__(*args, **kwargs)
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

        self.select_beakers_first1 = 0
        self.select_beakers_last1 = 0
        self.select_beakers_first2 = 0
        self.select_beakers_last2 = 0

        self.label_on_beaker_first = 0
        self.label_on_beaker_last = 0
        self.label_on_beaker_flag = False

        self.add_limewater_in_beaker_flag = False

        self.equivalent_limewater_flag = False
        self.equivalent_limewater_first = 0
        self.equivalent_limewater_last = 0

        self.unclear_straw_flag = False
        self.clear_straw_flag = False
        self.straw_to_limewater_first0 = 0
        self.straw_to_limewater_last0 = 0
        self.straw_to_limewater_first1 = 0
        self.straw_to_limewater_last1 = 0
        self.straw_to_limewater_first2 = 0
        self.straw_to_limewater_last2 = 0
        self.straw_to_limewater_first3 = 0
        self.straw_to_limewater_last3 = 0
        self.straw_to_limewater_first4 = 0
        self.straw_to_limewater_last4 = 0

        self.aurilave_to_limewater_flag = False
        self.aurilave_to_limewater_first1 = 0
        self.aurilave_to_limewater_last1 = 0
        self.aurilave_to_limewater_first2 = 0
        self.aurilave_to_limewater_last2 = 0

        self.limewater_phenomenon_flag = False
        self.limewater_phenomenon_first = 0
        self.limewater_phenomenon_last = 0

        self.clean_time = 0
        self.clean_desk_info = []  # 整理桌面信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        hands_front, beakers_front, narrow_mouth_bottles_front, narrow_mouths_front, labels_front, straws_front, \
        aurilaves_front, syringes_front, clear_liquids_front, clear_straw_front, unclear_liquids_front, \
        unclear_straw_front, plugs_right_front, plugs_wrong_front, dusters_front, waste_bottles_front = self.preds_front

        hands_top, beakers_top, narrow_mouth_bottles_top, narrow_mouths_top, labels_top, straws_top, \
        aurilaves_top, syringes_top, clear_straw_top, clear_liquids_top, unclear_liquids_top, unclear_straw_top, \
        plugs_right_top, plugs_wrong_top, dusters_top, waste_bottles_top = self.preds_top

        hands_side, beakers_side, narrow_mouth_bottles_side, narrow_mouths_side, labels_side, straws_side, \
        aurilavs_side, syringes_side, cclear_straw_side, clear_liquids_side, unclear_liquids_side, unclear_straw_side, \
        plugs_right_side, plugs_wrong_side, dusters_side, waste_bottles_side = self.preds_side

        front_items = [clear_liquids_front, unclear_liquids_front]
        top_items = [beakers_top]

        # 如果未得到得分点，则执行函数。
        # 1.选取大小相等的两个烧杯得分，选取大小不同的两个烧杯不得分。
        if not self.scorePoint1 :
            if self.select_beakers(hands_front, hands_top, beakers_front, beakers_top):
                self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 2.在实验过程中，能正确使用实验用品。
        if not self.scorePoint2 :
            if self.use_right():
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 3.在两个烧杯上分别贴上标签。
        if not self.scorePoint3:
            if self.label_on_beaker(beakers_front, labels_front):
                self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
        # 4.在两个烧杯中倒入石灰水得分，倒入清水不得分。
        if not self.scorePoint4:
            if self.limewater_in_beaker(beakers_front, clear_liquids_front, hands_front, plugs_wrong_front,
                                        plugs_right_front, narrow_mouth_bottles_front, narrow_mouths_front):
                self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
        # 5.在两个烧杯中倒入等量的石灰水得分，倒入的石灰水不等量不得分。
        if self.scorePoint1 and self.scorePoint4 and not self.scorePoint5:
            if self.equivalent_limewater(beakers_front, clear_liquids_front):
                self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 6.用塑料管向澄清石灰水中连续吹气，液体无贱出现象。
        if not self.scorePoint6:
            if self.straw_to_limewater(clear_liquids_front, clear_straw_front, unclear_straw_front, unclear_liquids_front,
                                       beakers_front, straws_front, aurilaves_front, syringes_front):
                self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
        # 7.用洗耳球（或注射器）向澄清石灰水中连续通气，液体无贱出现象。
        if not self.scorePoint7:
            if self.aurilave_to_limewater(clear_liquids_front, clear_straw_front, beakers_front, straws_front,
                                          aurilaves_front, syringes_front):
                self.assignScore(7, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 8.吹气的石灰水变浑浊，打气的石灰水无变化得分，实验现象不明显不得分。
        if self.scorePoint7 and not self.scorePoint8:
            if self.limewater_phenomenon(clear_liquids_front, unclear_liquids_front, beakers_front, clear_straw_front):
                self.assignScore(8, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)
                self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                 self.num_frame_front)

        # 9.将烧杯中石灰水倒入废料槽中，其他实验用品归位，清洁桌面，举手示意实验完毕。
        if not self.scorePoint9 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3 or self.scorePoint8 or
                                      self.scorePoint4 or self.scorePoint5 or self.scorePoint6 or self.scorePoint7):
            self.clean_desk(9, top_items, front_items)
            # self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front,
            #                  self.num_frame_front)

        if self.scorePoint9 and len(self.score_list) != 9:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                # self.retracementScore(2)
                self.retracementScore(9)

    # 1.选取大小相等的两个烧杯得分，选取大小不同的两个烧杯不得分。
    def select_beakers(self, hands_front, hands_top, beakers_front, beakers_top):
        if beakers_front.shape[0] == 2:
            beakers_front_box1 = beakers_front[0][:4]
            beakers_front_box2 = beakers_front[1][:4]
            if abs((box_area(beakers_front_box1) - box_area(beakers_front_box2))) < 1500 :
                self.select_beakers_first1, self.select_beakers_last1, flag1 = \
                    self.duration(self.select_beakers_first1, 2, self.select_beakers_last1, 0.5)
                if flag1:
                    # print("得分1前符合")
                    return True
        if beakers_top.shape[0] == 2:
            beakers_top_box1 = beakers_top[0][:4]
            beakers_top_box2 = beakers_top[1][:4]
            if abs((box_area(beakers_top_box1) - box_area(beakers_top_box2))) < 700:
                self.select_beakers_first2, self.select_beakers_last2, flag1 = \
                    self.duration(self.select_beakers_first2, 2, self.select_beakers_last2, 0.5)
                if flag1:
                    # print("得分1前符合")
                    return True

    # 2.在实验过程中，能正确使用实验用品。
    def use_right(self,):
        pass

    # 3.在两个烧杯上分别贴上标签。
    def label_on_beaker(self, beakers_front, labels_front):
        self.label_on_beaker_flag = False
        if beakers_front.shape[0] == 2 and labels_front.shape[0] == 2:
            beakers_front_box1 = beakers_front[0][:4]
            beakers_front_box2 = beakers_front[1][:4]
            labels_front_box1 = labels_front[0][:4]
            labels_front_box2 = labels_front[1][:4]
            if (pt_in_box(center_point(labels_front_box1), beakers_front_box1) and
                pt_in_box(center_point(labels_front_box2), beakers_front_box2)) or \
                    (pt_in_box(center_point(labels_front_box1), beakers_front_box2) and
                     pt_in_box(center_point(labels_front_box2), beakers_front_box1)):
                self.label_on_beaker_first, self.label_on_beaker_last, flag3 = \
                    self.duration(self.label_on_beaker_first, 2, self.label_on_beaker_last, 0.5)
                if flag3:
                    self.label_on_beaker_flag = True
                return True

    # 4.在两个烧杯中倒入石灰水得分，倒入清水不得分。
    def limewater_in_beaker(self, beakers_front, clear_liquids_front, hands_front, plugs_wrong_front, plugs_right_front,
                            narrow_mouth_bottles_front, narrow_mouths_front):
        # self.add_limewater_in_beaker_flag = False
        if plugs_wrong_front.shape[0] == 0:  # 瓶塞正确放，没有错误放置
            if narrow_mouth_bottles_front.shape[0] != 0 and narrow_mouths_front.shape[0] != 0 and \
                    beakers_front.shape[0] != 0 and hands_front.shape[0] != 0:
                for narrow_mouth_bottle_front in narrow_mouth_bottles_front:  # 遍历出现的细口瓶
                    narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]  # 取细口瓶的xyxy
                    narrow_mouth_front_box = None  # 初始设置无细口瓶口
                    for narrow_mouth_front in narrow_mouths_front:  # 遍历细口瓶口
                        narrow_mouth_front_box = narrow_mouth_front[:4]  # 取细口瓶口xyxy
                        if iou(narrow_mouth_front_box, narrow_mouth_bottle_front_box):  # 细口瓶和细口瓶口相交（证明是同一个细口瓶）
                            # print("细口瓶和细口瓶口相交")
                            break
                        else:
                            narrow_mouth_front_box = None
                    if narrow_mouth_front_box is not None:  # 有细口瓶口
                        # print("有细口瓶口")
                        for beaker_front in beakers_front:  # 遍历出现的烧杯
                            beaker_front_box = beaker_front[:4]
                            if center_distance_v(beaker_front_box, narrow_mouth_bottle_front_box) > 0:
                            # if pt_in_polygon(center_point(beaker_front_box), self.center_area_front) and \
                            #         center_distance_v(beaker_front_box, narrow_mouth_bottle_front_box) > 0:
                            #     print("正在倒液体")  # 烧杯在操作区域,细口瓶高于烧杯
                                self.add_limewater_in_beaker_flag = True
                                # if clear_liquids_front.shape[0] != 0:
                                #     for clear_liquid_front in clear_liquids_front: # 遍历出现的澄清液体
                                #         clear_liquid_front_box = clear_liquid_front[:4]
                                #         if pt_in_box(center_point(clear_liquid_front_box),beaker_front_box):
                                #             self.add_limewater_in_beaker_flag = True
        if self.add_limewater_in_beaker_flag :
            # print("倒了一部分液体")
            if clear_liquids_front.shape[0] == 2 and beakers_front.shape[0] == 2:
                beakers_front_box1 = beakers_front[0][:4]
                beakers_front_box2 = beakers_front[1][:4]
                clear_liquids_front_box1 = clear_liquids_front[0][:4]
                clear_liquids_front_box2 = clear_liquids_front[1][:4]
                if (pt_in_box(center_point(clear_liquids_front_box1), beakers_front_box1) and
                    pt_in_box(center_point(clear_liquids_front_box2), beakers_front_box2)) or \
                        (pt_in_box(center_point(clear_liquids_front_box1), beakers_front_box2) and
                         pt_in_box(center_point(clear_liquids_front_box2), beakers_front_box1)):
                    # print("得分4符合")
                    return True

    # 5.在两个烧杯中倒入等量的石灰水得分，倒入的石灰水不等量不得分。
    def equivalent_limewater(self, beakers_front, clear_liquids_front):
        self.equivalent_limewater_flag = False
        if clear_liquids_front.shape[0] == 2 and beakers_front.shape[0] == 2:
            beakers_front_box1 = beakers_front[0][:4]
            beakers_front_box2 = beakers_front[1][:4]
            clear_liquids_front_box1 = clear_liquids_front[0][:4]
            clear_liquids_front_box2 = clear_liquids_front[1][:4]
            if (pt_in_box(center_point(clear_liquids_front_box1), beakers_front_box1) and
                pt_in_box(center_point(clear_liquids_front_box2), beakers_front_box2)) or \
                    (pt_in_box(center_point(clear_liquids_front_box1), beakers_front_box2) and
                     pt_in_box(center_point(clear_liquids_front_box2), beakers_front_box1)):
                if abs(box_area(clear_liquids_front_box1) - box_area(clear_liquids_front_box1)) < 200 :
                    self.equivalent_limewater_first, self.equivalent_limewater_last, flag5 = \
                        self.duration(self.equivalent_limewater_first, 2, self.equivalent_limewater_last, 0.5)
                    if flag5:
                        self.equivalent_limewater_flag = True
                    return True

    # 6.用塑料管向澄清石灰水中连续吹气，液体无贱出现象。
    def straw_to_limewater(self, clear_liquids_front, clear_straw_front, unclear_straw_front, unclear_liquids_front,
                           beakers_front, straws_front, aurilaves_front, syringes_front):
        # self.unclear_straw_flag = False
        # self.clear_straw_flag = False
        # if clear_straw_front.shape[0] != 0:
        #     self.clear_straw_flag = True
#         #     print("澄清吸管存在")
        if beakers_front.shape[0] != 0 and straws_front.shape[0] != 0 :  # 烧杯存在、吸管存在、浑浊吸管存在
            for beaker_front in beakers_front:  # 遍历出现的烧杯
                beaker_front_box = beaker_front[:4]
                for straw_front in straws_front:  # 遍历出现的吸管
                    straw_front_box = straw_front[:4]
                    if aurilaves_front.shape[0] == 0 and syringes_front.shape[0] == 0:
                        # print("洗耳球不存在，注射器不存在")
                        if iou(beaker_front_box, straw_front_box) and \
                                center_distance_v(beaker_front_box, straw_front_box) > 0:
                            self.straw_to_limewater_first1, self.straw_to_limewater_last1, flag6 = \
                                self.duration(self.straw_to_limewater_first1, 1, self.straw_to_limewater_last1, 0.5)
                            # print("情况1符合")
                            if flag6:
                                self.unclear_straw_flag = True
                                # print("情况1符合并赋分")
                    elif aurilaves_front.shape[0] != 0 and syringes_front.shape[0] == 0:
                        # print("洗耳球存在，注射器不存在")
                        aurilaves_front_box = aurilaves_front[0][:4]
                        if iou(beaker_front_box, straw_front_box) and \
                                center_distance_v(beaker_front_box, straw_front_box) > 0 and \
                                center_distance_v(aurilaves_front_box, straw_front_box) > 0:
                            self.straw_to_limewater_first2, self.straw_to_limewater_last2, flag6 = \
                                self.duration(self.straw_to_limewater_first2, 1, self.straw_to_limewater_last2, 0.5)
                            # print("情况2符合")
                            if flag6:
                                self.unclear_straw_flag = True
                                # print("情况2符合,并赋分")

                    elif aurilaves_front.shape[0] == 0 and syringes_front.shape[0] != 0:
                        # print("洗耳球不存在，注射器存在")
                        syringes_front_box =  syringes_front[0][:4]
                        if iou(beaker_front_box, straw_front_box) and \
                                center_distance_v(beaker_front_box, straw_front_box) > 0 and \
                                center_distance_v(syringes_front_box, straw_front_box) > 0:
                            self.straw_to_limewater_first3, self.straw_to_limewater_last3, flag6 = \
                                self.duration(self.straw_to_limewater_first3, 1, self.straw_to_limewater_last3, 0.5)
                            # print("情况3符合")
                            if flag6:
                                self.unclear_straw_flag = True
                                # print("情况3符合，并赋分")

                    elif aurilaves_front.shape[0] != 0 and syringes_front.shape[0] != 0:
                        # print("洗耳球存在，注射器存在")
                        aurilaves_front_box = aurilaves_front[0][:4]
                        syringes_front_box = syringes_front[0][:4]
                        if iou(beaker_front_box, straw_front_box) and \
                                center_distance_v(beaker_front_box, straw_front_box) > 0 and \
                                center_distance_v(syringes_front_box, straw_front_box) > 0 and \
                                center_distance_v(aurilaves_front_box, straw_front_box) > 0:
                            self.straw_to_limewater_first4, self.straw_to_limewater_last4, flag6 = \
                                self.duration(self.straw_to_limewater_first4, 1, self.straw_to_limewater_last4, 0.5)
                            # print("情况4符合")
                            if flag6:
                                self.unclear_straw_flag = True
                                # print("情况4符合,并赋分")
        if self.unclear_straw_flag and (unclear_liquids_front.shape[0] != 0 or unclear_straw_front.shape[0] != 0 ):
            self.straw_to_limewater_first0, self.straw_to_limewater_last0, flag6 = \
                self.duration(self.straw_to_limewater_first0, 1, self.straw_to_limewater_last0, 0.5)
            if flag6:
                # print("得分6赋分")
                return True

    # 7.用洗耳球（或注射器）向澄清石灰水中连续通气，液体无贱出现象。
    def aurilave_to_limewater(self, clear_liquids_front, clear_straw_front, beakers_front, straws_front,
                              aurilaves_front, syringes_front):
        self.aurilave_to_limewater_flag = False
        if beakers_front.shape[0] != 0 and straws_front.shape[0] != 0 and clear_straw_front.shape[0] != 0:
            clear_straw_front_box = clear_straw_front[0][:4]
            for beaker_front in beakers_front:  # 遍历出现的烧杯
                beaker_front_box = beaker_front[:4]
                for straw_front in straws_front:  # 遍历出现的吸管
                    straw_front_box = straw_front[:4]
                    if aurilaves_front.shape[0] != 0: # 洗耳球存在
                        aurilaves_front_box = aurilaves_front[0][:4]
                        if iou(beaker_front_box, straw_front_box) and \
                                pt_in_box(center_point(clear_straw_front_box), beaker_front_box) and \
                                center_distance_v(beaker_front_box, straw_front_box) > 0 and \
                                center_distance_v(straw_front_box, aurilaves_front_box) > 0:
                            self.aurilave_to_limewater_first1, self.aurilave_to_limewater_last1, flag7 = \
                                self.duration(self.aurilave_to_limewater_first1, 1, self.aurilave_to_limewater_last1, 0.5)
                            if flag7:
                                self.aurilave_to_limewater_flag = True
                                return True
                    if syringes_front.shape[0] != 0: # 注射器存在
                        syringes_front_box = syringes_front[0][:4]
                        if iou(beaker_front_box, straw_front_box) and \
                                pt_in_box(center_point(clear_straw_front_box), beaker_front_box) and \
                                center_distance_v(beaker_front_box, straw_front_box) > 0 and \
                                center_distance_v(straw_front_box, syringes_front_box) > 0:
                            self.aurilave_to_limewater_first2, self.aurilave_to_limewater_last2, flag7 = \
                                self.duration(self.aurilave_to_limewater_first2, 1, self.aurilave_to_limewater_last2, 0.5)
                            if flag7:
                                self.aurilave_to_limewater_flag = True
                                return True

    # 8.吹气的石灰水变浑浊，打气的石灰水无变化得分，实验现象不明显不得分。
    def limewater_phenomenon(self, clear_liquids_front, unclear_liquids_front, beakers_front, clear_straw_front):
        self.limewater_phenomenon_flag = False
        if beakers_front.shape[0] == 2 and clear_liquids_front.shape[0] == 1 and unclear_liquids_front.shape[0] == 1 and \
                clear_straw_front.shape[0] == 0:
            beakers_front_box1 = beakers_front[0][:4]
            beakers_front_box2 = beakers_front[1][:4]
            clear_liquids_front_box1 = clear_liquids_front[0][:4]
            unclear_liquids_front = unclear_liquids_front[0][:4]
            if (pt_in_box(center_point(clear_liquids_front_box1), beakers_front_box1) and
                pt_in_box(center_point(unclear_liquids_front), beakers_front_box2)) or \
                    (pt_in_box(center_point(clear_liquids_front_box1), beakers_front_box2) and
                     pt_in_box(center_point(unclear_liquids_front), beakers_front_box1)):
                self.limewater_phenomenon_first, self.limewater_phenomenon_last, flag8 = \
                    self.duration(self.limewater_phenomenon_first, 2, self.limewater_phenomenon_last, 0.5)
                if flag8:
                    self.limewater_phenomenon_flag = True
                return True

    # 9.实验结束后能及时整理器材;能和监考老师文明礼貌交流

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
# # #         '''print实际相当于sys.stdout.write'''
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         pass
#
#
# # # sys.stdout = Logger('/home/xiding/new_aiexhibition_windows-master/test_log/log.txt')  # 调用print时相当于Logger().write()
