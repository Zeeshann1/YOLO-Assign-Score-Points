#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 15:04
# @Author  : Qiguangnan
# @File    : bio_seed_starch_cou.py


'''
验证种子中含有淀粉
'''

import random
from .comm import *


class BIO_seed_starch(ConfigModel):

    def __init__(self):
        super(BIO_seed_starch, self).__init__()

        self.drop_secs = 0.  # 滴碘液时间
        # 得分点标记
        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False
        self.scorePoint8 = False
        self.scorePoint9 = False

        self.culture_dishs_top_area = 0
        self.hand_corn_beaker = False  # 手和玉米烧杯有交
        self.reject_box_tweezer = False  # 镊子和废物槽有交
        self.preCutting = False  # 切玉米前条件
        self.cuttingInfo = []  # 记录切玉米信息
        self.culture_dish_top_box = None
        self.corn_beaker_top_box = None
        self.culture_dish_tweezer_front_info = []  # 记录镊子夹取玉米放培养皿信息 前视
        self.culture_dish_tweezer_corn_info = []  # 记录镊子夹取玉米放培养皿信息 玉米
        self.culture_dish_dropper_info = []  # 记录滴管滴加信息
        self.clearn_f_num = 0
        self.clearn_desk_info = []

    def post_assign(self, index, img, time_frame, object, preds, num_frame, conf, name_save, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, *args):  # 赋分逻辑部分
        peanut_beakers_front, corns_front, corn_beakers_front, blades_front, tweezers_front, \
        iodine_solution_bottles_front, droppers_front, red_ink_bottles_front, boards_front, \
        culture_dishs_front, dusters_front, reject_boxs_front, hands_front, \
        peanuts_front, cutting_corns_front = self.preds_front

        peanut_beakers_top, corns_top, corn_beakers_top, blades_top, tweezers_top, \
        iodine_solution_bottles_top, droppers_top, red_ink_bottles_top, boards_top, \
        culture_dishs_top, dusters_top, reject_boxs_top, hands_top, peanuts_top, \
        cutting_corns_top = self.preds_top

        if corn_beakers_top.shape[0] != 0:
            self.corn_beaker_top_box = corn_beakers_top[0][:4]
        if self.culture_dishs_top_area == 0 and culture_dishs_top.shape[0] != 0 and hands_top.shape[0] == 2:
            culture_dish_top_box = culture_dishs_top[0][:4]
            culture_dish_hand = False  # 手和培养皿是否有交集
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(hand_top_box, culture_dish_top_box) > 0:
                    culture_dish_hand = True
                    break
            if not culture_dish_hand:
                self.culture_dishs_top_area = float(box_area(culture_dish_top_box))

        # 1 选取玉米种子
        if not self.scorePoint1:
            info = self.select_corn(1, hands_top, hands_front, corns_front, corns_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 2 用镊子夹取种子
        if not self.scorePoint2:
            info = self.tweezer_corn(2, corns_front, tweezers_front, hands_front, corns_top, tweezers_top, hands_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 3 将种子放在木板上
        if not self.scorePoint3:
            info = self.corn_on_board(3, boards_front, corns_front, tweezers_front, hands_front, boards_top,
                                      corns_top, tweezers_top, hands_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 4 用刀将玉米种子切开
        if not self.scorePoint4:
            info = self.cut_corn(4, boards_top, boards_front, hands_top, hands_front, blades_top, blades_front,
                                 cutting_corns_front, corns_front, corns_top, cutting_corns_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 5 用镊子夹取切好的种子放在培养皿中
        if not self.scorePoint5 and self.scorePoint4:
            info = self.tweezer_corn_culture(5, culture_dishs_front, culture_dishs_top, corns_front, corns_top,
                                             tweezers_front, tweezers_top, hands_front, hands_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 6 将适量的碘液滴在种子的纵切面中
        if not self.scorePoint6:
            info = self.drop_corn(6, droppers_top, culture_dishs_top, red_ink_bottles_top, droppers_front,
                                  culture_dishs_front,
                                  hands_front, hands_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 7 正确使用实验用品
        if not self.scorePoint7 and self.scorePoint2 and self.scorePoint3 and self.scorePoint5 and self.scorePoint6:
            if self.secs - self.drop_secs > random.random():
                img1 = cv2.imread((self.save_path / '2.jpg').as_posix())
                img2 = cv2.imread((self.save_path / '3.jpg').as_posix())
                img3 = cv2.imread((self.save_path / '5.jpg').as_posix())
                img4 = cv2.imread((self.save_path / '6.jpg').as_posix())
                res = np.hstack([np.vstack([img1, img2]), np.vstack([img3, img4])])
                res = cv2.resize(res, dsize=None, fx=0.5, fy=0.5)
                self.assignScore(7, res, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)

        # 8 滴加碘液的玉米切面变蓝
        if not self.scorePoint8 and self.scorePoint1 and self.scorePoint6:
            info = self.blued(8, iodine_solution_bottles_top, red_ink_bottles_top, droppers_top, culture_dishs_top)
            if info is not None:
                self.assignScore(*info[:6])

        # 9 整理桌面
        top_items = [peanut_beakers_top, corns_top, corn_beakers_top, blades_top, tweezers_top,
                     iodine_solution_bottles_top, droppers_top, red_ink_bottles_top,
                     boards_top, culture_dishs_top, dusters_top, reject_boxs_top]
        front_items = [peanut_beakers_front, corns_front, corn_beakers_front, blades_front, tweezers_front,
                       iodine_solution_bottles_front, droppers_front, red_ink_bottles_front,
                       boards_front, culture_dishs_front, dusters_front, reject_boxs_front]
        if not self.scorePoint9 and (len(self.score_list) > 4):
            # if not self.reject_box_tweezer:  # 将种子放到废液缸中
            #     if reject_boxs_top.shape[0] != 0 and tweezers_top.shape[0] != 0:
            #         reject_box_top_box = reject_boxs_top[0][:4]
            #         tweezer_top_box = tweezers_top[0][:4]
            #         r_t_iou = iou(reject_box_top_box, tweezer_top_box)
            #         if r_t_iou > 0:
            #             cv2.imwrite((self.save_path / 'corn_reject_box.jpg').as_posix(), self.top_img0)
            #             self.reject_box_tweezer = True
            #
            # if not self.reject_box_tweezer:  # 将种子放到废液缸中
            #     if reject_boxs_top.shape[0] != 0 and hands_top.shape[0] != 0:
            #         reject_box_top_box = reject_boxs_top[0][:4]
            #         for hand_top in hands_top:
            #             hand_top_box = hand_top[:4]
            #             r_t_iou = iou(reject_box_top_box, hand_top_box)
            #             if r_t_iou > 0:
            #                 cv2.imwrite((self.save_path / 'corn_reject_box.jpg').as_posix(),
            #                             self.top_img0)
            #                 self.reject_box_tweezer = True
            #                 break
            # if self.reject_box_tweezer:
            info = self.clearn_desk(9, top_items, front_items)
            if info is not None:
                self.assignScore(*info[:6])

        if self.scorePoint9 and len(self.score_list) != 9:
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(9)

    # 选取玉米种子
    def select_corn(self, score_index, hands_top, hands_front, corns_front, corns_top):
        if (not self.hand_corn_beaker
                and self.corn_beaker_top_box is not None
                and hands_top.shape[0] != 0):  # 手与玉米烧杯是否有交集 有代表去取玉米种子
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(self.corn_beaker_top_box, hand_top_box) > 0:
                    self.hand_corn_beaker = True
        if self.hand_corn_beaker and corns_front.shape[0] != 0 and hands_front.shape[0] != 0:  # 前视
            hand_corn = False  # 手和种子是否有交集
            corn_front_box = corns_front[0][:4]
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if min_dis_boxes(hand_front_box, corn_front_box) < 0.001 * self.h_front:
                    hand_corn = True
                    break
            if not hand_corn:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front
        if not self.scorePoint1 and self.hand_corn_beaker and corns_top.shape[0] != 0:  # 顶视
            hand_corn = False
            corn_top_box = corns_top[0][:4]
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if min_dis_boxes(hand_top_box, corn_top_box):
                    hand_corn = True
                    break
            if not hand_corn:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    # 用镊子夹取玉米
    def tweezer_corn(self, score_index, corns_front, tweezers_front, hands_front, corns_top, tweezers_top, hands_top):
        if corns_front.shape[0] != 0 and tweezers_front.shape[0] != 0 and hands_front.shape[0] > 0:
            for corn_front in corns_front:
                corn_front_box = corn_front[:4]
                tweezer_front_box = tweezers_front[0][:4]
                c_t_iou = iou(corn_front_box, tweezer_front_box)
                if c_t_iou > 0:
                    hand_corn = False  # 手和种子是否有交集
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if min_dis_boxes(hand_front_box, corn_front_box) < 0.001 * self.h_front:
                            hand_corn = True
                            break
                    if not hand_corn:  # 手和种子没有交集
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

        if not self.scorePoint2 and corns_top.shape[0] != 0 and tweezers_top.shape[0] != 0 and \
                hands_top.shape[0] > 0:
            for corn_top in corns_top:
                corn_top_box = corn_top[:4]
                tweezer_top_box = tweezers_top[0][:4]
                c_t_iou = iou(corn_top_box, tweezer_top_box)
                if c_t_iou > 0:
                    hand_corn = False  # 手和种子是否有交集
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if min_dis_boxes(hand_top_box, corn_top_box) < 0.001 * self.h_front:
                            hand_corn = True
                            break
                    if not hand_corn:  # 手和种子没有交集 种子和镊子有交集
                        return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top

    # 玉米在模板上
    def corn_on_board(self, score_index, boards_front, corns_front, tweezers_front, hands_front, boards_top, corns_top,
                      tweezers_top, hands_top):
        if boards_front.shape[0] != 0 and corns_front.shape[0] != 0 and tweezers_front.shape[0] != 0 and \
                hands_front.shape[0] != 0:  # 前视 种子 玉米 镊子 手
            board_front_box = boards_front[0][:4]
            tweezer_front_box = tweezers_front[0][:4]
            for corn_front in corns_front:
                corn_front_box = corn_front[:4]
                c_t_iou = min_dis_boxes(corn_front_box, tweezer_front_box)  # 种子和镊子距离
                b_c_iou = iou(corn_front_box, board_front_box)  # 种子木板的交集
                corn_area = box_area(corn_front_box)
                if corn_area == b_c_iou and c_t_iou > 0.04 * self.h_front:  # 种子完全在模板框里面 且种子和镊子没有交集
                    hand_corn = False  # 手和种子是否有交集
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if min_dis_boxes(hand_front_box, corn_front_box) < 0.001 * self.h_front:
                            hand_corn = True
                            break
                    if not hand_corn:  # 手和种子没有交集
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

        if not self.scorePoint3 and boards_top.shape[0] != 0 and corns_top.shape[0] != 0 and \
                tweezers_top.shape[0] != 0 and hands_top.shape != 0:  # 顶视 种子 玉米 镊子 手
            board_top_box = boards_top[0][:4]
            tweezer_top_box = tweezers_top[0][:4]
            for corn_top in corns_top:
                corn_top_box = corn_top[:4]
                c_t_iou = min_dis_boxes(corn_top_box, tweezer_top_box)
                b_c_iou = iou(corn_top_box, board_top_box)
                corn_area = box_area(corn_top_box)
                if corn_area == b_c_iou and c_t_iou > 0.04 * self.h_top:  # 种子完全在模板框里面 且种子和镊子没有交集
                    hand_corn = False  # 手和种子是否有交集
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if min_dis_boxes(hand_top_box, corn_top_box) < 0.001 * self.h_top:
                            hand_corn = True
                            break
                    if not hand_corn:  # 手和种子没有交集 种子和镊子有交集
                        return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top

    # 用刀切玉米
    def cut_corn(self, score_index, boards_top, boards_front, hands_top, hands_front, blades_top, blades_front,
                 cutting_corns_front, corns_front, corns_top, cutting_corns_top):
        self.preCutting = False
        if boards_top.shape[0] != 0 and boards_front.shape[0] != 0:  # 前视和顶视手和木板有交集
            board_top_box = boards_top[0][:4]
            board_front_box = boards_front[0][:4]
            if hands_top.shape[0] != 0 and hands_front.shape[0] != 0:
                hand_board_f = False
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, board_top_box) > 0:
                        hand_board_f = True
                        break
                if hand_board_f:
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, board_front_box) > 0:
                            self.preCutting = True
                            break
            if self.preCutting and blades_top.shape[0] != 0:  # 顶部视角 刀片和木板没有交集
                blade_top_box = blades_top[0][:4]
                if iou(blade_top_box, board_top_box) == 0:
                    self.preCutting = False
            if self.preCutting and blades_front.shape[0] != 0:  # 前视 刀片和木板没有交集
                blade_front_box = blades_front[0][:4]
                if iou(blade_front_box, board_front_box) == 0:
                    self.preCutting = False

            if self.preCutting:  # 符合切玉米前提条件
                if cutting_corns_front.shape[0] != 0:  # 前视
                    cutting_corn_front_box = cutting_corns_front[0][:4]
                    if iou(cutting_corn_front_box, board_front_box) > 0:
                        self.cuttingInfo = [score_index, self.frame_front, self.time_front, self.objects_front,
                                            self.preds_front, self.num_frame_front, self.secs]
                if not self.scorePoint4 and blades_front.shape[0] != 0 and corns_front.shape[
                    0] != 0:  # 前视
                    blade_front_box = blades_front[0][:4]
                    for corn_front in corns_front:
                        corn_front_box = corn_front[:4]
                        if iou(blade_front_box, corn_front_box) > 0 and \
                                center_distance_v(corn_front_box,
                                                  blade_front_box) > 0:  # 刀片 种子交 刀片在种子上方
                            self.cuttingInfo = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                self.preds_front, self.num_frame_front, self.secs]
                            break
                if not self.scorePoint4 and cutting_corns_top.shape[0] != 0:
                    cutting_corn_top_box = cutting_corns_top[0][:4]
                    if iou(cutting_corn_top_box, board_top_box) == box_area(cutting_corn_top_box):
                        self.cuttingInfo = [score_index, self.frame_front, self.time_front, self.objects_front,
                                            self.preds_front, self.num_frame_front, self.secs]
                if not self.scorePoint4 and blades_top.shape[0] != 0 and corns_top.shape[0] != 0:
                    blade_top_box = blades_top[0][:4]
                    for corn_top in corns_top:
                        corn_top_box = corn_top[:4]
                        if iou(blade_top_box, corn_top_box) > 0 and \
                                iou(blade_top_box, board_top_box) == box_area(blade_top_box):
                            self.cuttingInfo = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                self.preds_front, self.num_frame_front, self.secs]
                            break
        if self.cuttingInfo and self.secs - self.cuttingInfo[-1] > 2:
            return self.cuttingInfo[:6]

    # 用镊子夹取玉米到培养皿中
    def tweezer_corn_culture(self, score_index, culture_dishs_front, culture_dishs_top, corns_front, corns_top,
                             tweezers_front, tweezers_top, hands_front, hands_top):
        corn_in_culture_dish = False
        if culture_dishs_front.shape[0] != 0 and culture_dishs_top.shape[0] != 0:  # 前视 顶视都有培养皿
            culture_dish_front_box = culture_dishs_front[0][:4]
            culture_dish_top_box = culture_dishs_top[0][:4]
            if corns_front.shape[0] != 0:
                for corn_front in corns_front:
                    corn_front_box = corn_front[:4]
                    if box1_in_box2(corn_front_box, culture_dish_front_box):
                        corn_in_culture_dish = True
                        break
                if not corn_in_culture_dish and corns_top.shape[0] != 0:
                    for corn_top in corns_top:
                        corn_top_box = corn_top[:4]
                        if box1_in_box2(corn_top_box, culture_dish_top_box):
                            corn_in_culture_dish = True
                            break
            if tweezers_front.shape[0] != 0 and hands_front.shape[0] != 0 and hands_top.shape[0] != 0:
                # 前视镊子和培养皿有交集(顶视手和培养皿也要有交集)
                tweezer_front_box = tweezers_front[0][:4]
                if not pt_in_polygon(center_point(tweezer_front_box), self.center_area_front):
                    return
                hand_tweezer = 0  # 0 表示与手没有交集 1 表示与 1 只手有交集 2 表示与左手有交叉 3 表示与右手有交集 4 表示与两只手有交集
                if hands_front.shape[0] == 1:  # 前视一只手
                    hand_front_box = hands_front[0][:4]
                    if iou(hand_front_box, tweezer_front_box) > 0:
                        hand_tweezer = 1
                else:  # 前视两只手
                    hands_front_left, hands_front_right = separate_left_right(hands_front[0][:4],
                                                                              hands_front[1][:4])
                    if iou(hands_front_left, tweezer_front_box) > 0:
                        hand_tweezer = 2
                    if iou(hands_front_right, tweezer_front_box) > 0:
                        if hand_tweezer == 2:
                            hand_tweezer = 4
                        else:
                            hand_tweezer = 3
                c_t_iou = iou(culture_dish_front_box, tweezer_front_box)  # 培养皿 镊子交集
                d = center_distance_v(culture_dish_front_box, tweezer_front_box)  # 培养皿在镊子下
                if c_t_iou > 0 and d > 0 and hand_tweezer > 0:
                    if tweezers_top.shape[0] != 0:
                        tweezer_top = tweezers_top[0][:4]
                        if iou(culture_dish_top_box, tweezer_top) > 0:  # 顶视镊子和培养皿有交集
                            self.tweezer_culture(score_index, c_t_iou, corn_in_culture_dish)
                    else:
                        if hands_top.shape[0] == 1:
                            hand_top = hands_top[0][:4]
                            if min_dis_boxes(hand_top, culture_dish_top_box) < self.h_top * 0.046:
                                self.tweezer_culture(score_index, c_t_iou, corn_in_culture_dish)
                        else:
                            hands_top_left, hands_top_right = separate_left_right(hands_front[0][:4],
                                                                                  hands_front[1][:4])
                            if hand_tweezer == 1 or hand_tweezer == 4:  # 前视只有一只手
                                for hand_top in hands_top:
                                    hand_top_box = hand_top[:4]
                                    if min_dis_boxes(hand_top_box, culture_dish_top_box) < self.h_top * 0.046:
                                        self.tweezer_culture(score_index, c_t_iou, corn_in_culture_dish)
                                        break
                            elif hand_tweezer == 2:  # 前视与左手有交集 顶视 右手与培养皿较近
                                if min_dis_boxes(hands_top_right, culture_dish_top_box) < self.h_top * 0.046:
                                    self.tweezer_culture(score_index, c_t_iou, corn_in_culture_dish)
                            else:  # 前视与右手有交集
                                if min_dis_boxes(hands_top_left, culture_dish_top_box) < self.h_top * 0.046:
                                    self.tweezer_culture(score_index, c_t_iou, corn_in_culture_dish)
        if self.culture_dish_tweezer_corn_info and self.secs - self.culture_dish_tweezer_corn_info[-1] > 1:
            return self.culture_dish_tweezer_corn_info[:6]
        elif self.culture_dish_tweezer_front_info and self.secs - self.culture_dish_tweezer_front_info[-1] > 1:
            return self.culture_dish_tweezer_front_info[:6]

    # 用碘液滴玉米
    def drop_corn(self, score_index, droppers_top, culture_dishs_top, red_ink_bottles_top, droppers_front,
                  culture_dishs_front,
                  hands_front, hands_top):
        pre_dropper = True
        if droppers_top.shape[0] == 2:  # 顶视 两个滴管都在操作区外
            dropper_top_box1 = droppers_top[0][:4]
            dropper_top_box2 = droppers_top[1][:4]
            # if not pt_in_polygon(center_point(dropper_top_box1), self.center_area_top) and \
            #         not pt_in_polygon(center_point(dropper_top_box2), self.center_area_top):
            #     pre_dropper = False
        if pre_dropper and red_ink_bottles_top.shape[0] == 1 and droppers_top.shape[0] > 0:
            red_ink_bottle_top_box = red_ink_bottles_top[0][:4]
            r_a_iou = 0
            for dropper_top in droppers_top:
                dropper_top_box = dropper_top[:4]
                r_d_iou = iou(dropper_top_box, red_ink_bottle_top_box)
                if r_d_iou > 0:
                    if center_point(red_ink_bottle_top_box)[0] > (self.w_top / 2):  # 红墨水在桌面右边
                        if center_point(dropper_top_box)[0] >= center_point(red_ink_bottle_top_box)[
                            0]:  # 滴管在瓶子右侧
                            r_a_iou += r_d_iou
                    else:  # 红墨水在桌面左边
                        if center_point(dropper_top_box)[0] <= center_point(red_ink_bottle_top_box)[
                            0]:  # 滴管在瓶子左侧
                            r_a_iou += r_d_iou
            if r_a_iou > 0:  # 红墨水上面有滴管
                if droppers_front.shape[0] != 0 and culture_dishs_front.shape[0] != 0 and hands_front.shape[
                    0] != 0 and hands_top.shape[0] != 0:
                    culture_dish_front_box = culture_dishs_front[0][:4]
                    if pt_in_polygon(center_point(culture_dish_front_box), self.center_area_front):
                        for dropper_front in droppers_front:
                            dropper_front_box = dropper_front[:4]
                            d_c_iou = iou(dropper_front_box, culture_dish_front_box)
                            d = center_distance_v(culture_dish_front_box, dropper_front_box)
                            if d_c_iou > 0 and d > 0:
                                if not self.culture_dish_dropper_info or d_c_iou > self.culture_dish_dropper_info[-2]:
                                    self.culture_dish_dropper_info = [score_index, self.frame_front, self.time_front,
                                                                      self.objects_front, self.preds_front,
                                                                      self.num_frame_front, d_c_iou, self.secs]
                                else:
                                    self.culture_dish_dropper_info[-1] = self.secs

                # if droppers_top.shape[0] != 0 and culture_dishs_top.shape[0] != 0 and hands_front.shape[
                #     0] != 0 and hands_top.shape[0] != 0:
                #     culture_dish_top_box = culture_dishs_top[0][:4]
                #     for dropper_top in droppers_top:
                #         dropper_top_box = dropper_top[:4]
                #         d_c_iou = iou(dropper_top_box, culture_dish_top_box)
                #         if d_c_iou > 0:
                #             if not self.culture_dish_dropper_info or d_c_iou > self.culture_dish_dropper_info[-2]:
                #                 self.culture_dish_dropper_info = [score_index, self.frame_top, self.time_front,
                #                                                   self.objects_front, self.preds_top,
                #                                                   self.num_frame_front, d_c_iou, self.secs]
                #             else:
                #                 self.culture_dish_dropper_info[-1] = self.secs

        if self.culture_dish_dropper_info and self.secs - self.culture_dish_dropper_info[-1] > 0.5:
            self.drop_secs = self.secs
            return self.culture_dish_dropper_info[:6]

    # 切面变蓝
    def blued(self, score_index, iodine_solution_bottles_top, red_ink_bottles_top, droppers_top, culture_dishs_top):
        if (self.secs - self.drop_secs > 1
                and iodine_solution_bottles_top.shape[0] == 1
                and red_ink_bottles_top.shape[0] == 1
                and droppers_top.shape[0] == 2
                and culture_dishs_top.shape[0] != 0):
            iodine_solution_bottle_top_box = iodine_solution_bottles_top[0][:4]
            red_ink_bottle_top_box = red_ink_bottles_top[0][:4]
            i_a_iou = 0
            r_a_iou = 0
            for dropper_top in droppers_top:
                dropper_top_box = dropper_top[:4]
                i_d_iou = iou(dropper_top_box, iodine_solution_bottle_top_box)  # 判断碘液上是否有滴管
                if i_d_iou > 0:
                    if center_point(iodine_solution_bottle_top_box)[0] > (self.w_top / 2):  # 碘液在桌面右边
                        if center_point(dropper_top_box)[0] >= center_point(iodine_solution_bottle_top_box)[
                            0]:  # 滴管在碘液瓶子右侧
                            i_a_iou += i_d_iou
                    else:  # 碘液在桌面左边
                        if center_point(dropper_top_box)[0] <= center_point(iodine_solution_bottle_top_box)[
                            0]:  # 滴管在碘液瓶子左侧
                            i_a_iou += i_d_iou
                r_d_iou = iou(dropper_top_box, red_ink_bottle_top_box)  # 判断 红墨水上是否有滴管
                if r_d_iou > 0:
                    if center_point(red_ink_bottle_top_box)[0] > (self.w_top / 2):  # 红墨水在桌面右边
                        if center_point(dropper_top_box)[0] >= center_point(red_ink_bottle_top_box)[
                            0]:  # 滴管在红墨水瓶子右侧
                            r_a_iou += r_d_iou
                    else:  # 红墨水在桌面左边
                        if center_point(dropper_top_box)[0] <= center_point(red_ink_bottle_top_box)[
                            0]:  # 滴管在红墨水瓶子左侧
                            r_a_iou += r_d_iou

            if i_a_iou > 0 and r_a_iou > 0:  # 判断红墨水瓶子上有滴管 碘液瓶子上有滴管
                culture_dish_top_box = culture_dishs_top[0][:4]
                if box_area(culture_dish_top_box) > self.culture_dishs_top_area * 0.85:
                    return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    # 清理桌面
    def clearn_desk(self, score_index, top_items, front_items):
        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 2)
            if flag:
                self.clearn_f_num = 0
                return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]
        else:
            self.clearn_f_num = 0

    def tweezer_culture(self, score_index, c_t_iou, corn=False):
        if corn:
            if not self.culture_dish_tweezer_corn_info or c_t_iou > self.culture_dish_tweezer_corn_info[-2]:
                self.culture_dish_tweezer_corn_info = [score_index, self.frame_front, self.time_front,
                                                       self.objects_front, self.preds_front, self.num_frame_front,
                                                       c_t_iou, self.secs]
            else:
                self.culture_dish_tweezer_corn_info[-1] = self.secs
        else:
            if not self.culture_dish_tweezer_front_info or c_t_iou > self.culture_dish_tweezer_front_info[-2]:
                self.culture_dish_tweezer_front_info = [score_index, self.frame_front, self.time_front,
                                                        self.objects_front, self.preds_front, self.num_frame_front,
                                                        c_t_iou, self.secs]
            else:
                self.culture_dish_tweezer_front_info[-1] = self.secs
            if self.culture_dish_tweezer_corn_info:
                self.culture_dish_tweezer_corn_info[-1] = self.secs

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2:
            self.assignScore(*self.clearn_desk_info[:6])
            return True
