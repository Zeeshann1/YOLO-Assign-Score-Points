#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 14:34
# @Author  : cbj
# @File    : phy_measure_density_scale_cou.py

import traceback
from .comm import *
from .comm.course_base import ConfigModel

# from queue import Queue
# import cv2
# import numpy as np
# from threading import Thread
# from pathlib import Path
# from util import ts2ft
from logger import logger
# from concurrent.futures import ThreadPoolExecutor
from config import experimental_site_top as est
from config import experimental_site_front as esf
# from config import EXP_MAP
import random


class PHY_lever_balance(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(PHY_lever_balance, self).__init__(*args, **kwargs)
        self.initScore()

    def initScore(self):
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

        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.flag4 = False
        self.flag5 = False
        self.flag6 = False
        self.flag7 = False

        # 记录标志时间
        self.flag1time = 0.0
        self.flag2time = 0.0
        self.flag3time = 0.0
        self.flag4time = 0.0
        self.flag5time = 0.0
        self.flag6time = 0.0
        self.flag7time = 0.0

        # 单侧挂钩码
        self.single_slider_pos = [0.0]

        # self.clearn_time = 0.
        self.clearn_f_num = 0.
        self.clearn_desk_info = []  # 整理桌面信息
        self.set_center_box = False  # 是否设置中心区域

    def setCenterBox(self, device, est=None, esf=None):  # 设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
        if hasattr(self, 'top_img0') and est:
            self.h_top, self.w_top = self.top_img0.shape[:2]
            self.center_box_top = torch.tensor(
                [self.w_top * est[0], self.h_top * est[1], self.w_top * est[2], self.h_top * est[3]],
                device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
        if hasattr(self, 'front_img0') and esf:
            self.h_front, self.w_front = self.front_img0.shape[:2]
            self.center_box_front = torch.tensor(
                [self.w_front * esf[0], self.h_front * esf[1], self.w_front * esf[2], self.h_front * esf[3]],
                device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
        self.set_center_box = True

    def post_assign(self, index, img, time_frame, object, preds, num_frame, conf, name_save, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def get_hookweight_num(self, hook_weights_front, boutns_front, levers_front, front_img0):
        """
        获取钩码数
        遍历钩码与黑旋钮的位置判断左边钩码和右边钩码,
        对于左侧,
            判断左边第一个钩码与杠杆的交集判断挂了第一个钩码,后面的钩码与前一个钩码的距离在一个范围内表示挂在了前一个钩码上
        右边同理.
        :param hook_weights_front:
        :param boutns_front:
        :param levers_front:
        :param front_img0:
        :return:
        """
        left_hook = []
        right_hook = []
        for hook_weight_front in hook_weights_front:
            # 左侧
            if center_distance_h(hook_weight_front[:4], boutns_front[0][:4]) < 0:
                h_l_iou = iou(hook_weight_front[:4], levers_front[0][:4])
                if h_l_iou > 0:
                    left_hook.append(hook_weight_front[:4])
                else:
                    if left_hook:
                        if 0 < abs(center_point(hook_weight_front[:4])[1] - center_point(left_hook[-1])[1]) < 0.092*front_img0.shape[0]:
                            left_hook.append(hook_weight_front[:4])
            else:
                h_l_iou = iou(hook_weight_front[:4], levers_front[0][:4])
                if h_l_iou > 0:
                    right_hook.append(hook_weight_front[:4])
                else:
                    if right_hook:
                        if 0 < abs(center_point(hook_weight_front[:4])[1] - center_point(right_hook[-1])[1]) < 0.092*front_img0.shape[0]:
                            right_hook.append(hook_weight_front[:4])
        return left_hook, right_hook

    def score_process(self,top_true,front_true,side_true):  # 赋分逻辑部分
        # [self.top_preds, self.front_preds], [self.top_img0, self.front_img0] = detect_info
        #
        # if not self.set_center_box:
        #     self.setCenterBox(self.top_preds[0].device, est, esf)  # 设置中心区域

        hands_front, gel_pens_front, papers_front, levers_front, nuts_front, iron_poles_front, sliders_front, \
        spring_ergometers_front, hook_weights_front, boutns_front, clean_desks_front, heads_front, \
        eyes_front = self.preds_front

        hands_top, gel_pens_top, papers_top, levers_top, nuts_top, iron_poles_top, sliders_top, \
        spring_ergometers_top, hook_weights_top, boutns_top, clean_desks_top, heads_top, \
        eyes_top = self.preds_top

        """
                        1.安装杠杆,将杠杆中点支在铁架台上: lever_front 与 iron_pole_front iou大于0 并且lever_front 垂直中心点在 iron_pole_front 的上方
                        2.'调节杠杆两端的螺母,使杠杆在水平位置平衡': 首先 步骤1 得分,情况下 有 hand 与 nut iou大于0 这个步骤,-> 手 与 螺母 iou=0 (或者
                        手 与 杠杆 iou=0 )且 lever与iron_pole iou>0 且 杠杆的垂直中心点在铁杆的垂直中心点的上方且左右两个螺母的垂直方向上的大小差值在某个范围,即杠杆平衡;
                        3.'弹簧测力计调零': 判断弹簧测力计的宽高比在一定范围, 竖直时可视为调零; 手与测力计有交集,且测力计的宽高比在一定范围
                        4. '杠杆两侧测力':步骤2,3存在,以铁杆作为判断依据, 滑块中心点x坐标小于铁杆中心点x轴坐标 说明滑块在铁杆的左侧,反之在右侧;当两侧均有滑块时,左边 钩码中心点的y轴大于设定的某个值说明钩码已经挂载左边了,此时可以计算钩码个数.判断左边挂了几个钩码
                        同理右边;再判断 手与杠杆iou=0 两个螺母的垂直方向中心点的差值在某个范围--可判断两侧平衡;
                        5.'杠杆同一侧测力': 步骤2,3 存在,判断通过判断滑块的中心点x轴与铁杆的中心点的x轴大小判断在哪一侧且只在同一侧,判断钩码的中心点y轴在在某个范围内,且弹簧测力计也在铁杆的同侧,且
                        弹簧测力计与滑块iou>0且 两个螺母的垂直方向位置y差值在某个范围--可判断同侧平衡;
                        6. '观察记录数据': 步骤4存在或者步骤5存在,判断 手与笔有交集且笔与纸有交集;
                        7 '改变钩码个数,位置,弹簧测力计拉杠杆的位置,再完成几组实验';
                        8 整理实验器材: scoreFlag1,scoreFlag2... 存在,且桌面在限定趋区域没有物品
                        9 当 scoreFlag1 scoreFlag2...存在或者 scoreFlag8 存在 则得分
                        """
        # 1 安装杠杆 在支架上
        if not self.scorePoint1:
            # self.lever_on_bracket(levers_front, boutns_front, hands_front, self.front_img0, self.front_preds)
            info = self.lever_on_bracket(1, levers_front, boutns_front, hands_front)
            if info is not None:
                self.assignScore(*info)


        # 2 调节平衡螺母 杠杆水平调零使平衡
        if not self.scorePoint2 and self.scorePoint1:
            # self.mea_lever_zero(hands_front, nuts_front, levers_front, boutns_front, hook_weights_front,
            #                     self.front_img0, self.front_preds)

            info = self.mea_lever_zero(2, hands_front, nuts_front, levers_front, boutns_front, hook_weights_front)
            if info is not None:
                self.assignScore(*info)

        # 3弹簧测力计调零
        if not self.scorePoint3:
            # self.mea_dynamometer_zero(heads_front, spring_ergometers_front, hook_weights_front, levers_front,
            #                           self.front_img0, self.front_preds)
            info = self.mea_dynamometer_zero(3, heads_front, spring_ergometers_front, hook_weights_front, levers_front)
            if info is not None:
                self.assignScore(*info)

        # 4 杠杆两侧测力
        if not self.scorePoint4 and self.scorePoint1:
            # self.both_side_mea(levers_front, boutns_front, nuts_front, hook_weights_front, hands_front,
            #                    self.front_img0, self.front_preds)

            info = self.both_side_mea(4, levers_front, boutns_front, nuts_front, hook_weights_front, hands_front,)
            if info is not None:
                self.assignScore(*info)

        # 5 杠杆同一侧测力
        if not self.scorePoint5:
            # self.same_side_mea(levers_front, boutns_front, nuts_front, hook_weights_front, spring_ergometers_front,
            #                    hands_front, self.front_img0, self.front_preds)

            info = self.same_side_mea(5, levers_front, boutns_front, nuts_front, hook_weights_front,
                                      spring_ergometers_front, hands_front)
            if info is not None:
                self.assignScore(*info)

        # 6 改变钩码个数,位置以及弹簧测力计拉杠杆的位置,再完成几组实验
        if not self.scorePoint6:
            # self.change_pos_mea(levers_front, boutns_front, nuts_front, hook_weights_front, spring_ergometers_front,
            #                     hands_front, self.front_img0, self.front_preds)
            info = self.change_pos_mea(6, levers_front, boutns_front, nuts_front, hook_weights_front,
                                       spring_ergometers_front, hands_front)
            if info is not None:
                self.assignScore(*info)

        # 7 清洗仪器，整理桌面
        top_items = [levers_top, nuts_top, iron_poles_top, boutns_top, sliders_top,
                     spring_ergometers_top, hook_weights_top, ]

        front_items = [levers_front, nuts_front, iron_poles_front, boutns_front, sliders_front,
                       spring_ergometers_front, hook_weights_front, ]
        if not self.scorePoint7 and (self.scorePoint1 or self.scorePoint2):
            # self.clearn_desk(top_items, front_items)
            info = self.clearn_desk(7,top_items,front_items)
            if info is not None:
                self.assignScore(*info)

        if self.scorePoint7 and len(self.score_list) != 7:
            # if not self.desk_is_clearn(top_items, front_items):
            if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                self.retracementScore(7)

    # 1
    def lever_on_bracket(self, score_index, levers_front, boutns_front, hands_front):
        """
        杠杆在支架上的判断: 1杠杆和黑旋钮之间的垂直距离在一个范围内表示杠杆挂在了铁杆上,手和杠杆没有交集
        :param levers_front:
        :param boutns_front:
        :param hands_front:
        :param front_img0:
        :return:
        """
        if levers_front.shape[0] != 0 and boutns_front.shape[0] != 0 and \
                0 < abs(center_distance_v(boutns_front[0][:4], levers_front[0][:4])) < 0.185 * self.frame_front.shape[0]:
            hand_lever_iou = False
            if hands_front.shape[0] != 0:
                for hand_front in hands_front:
                    h_l_iou = iou(hand_front[:4], levers_front[0][:4])
                    if h_l_iou:
                        hand_lever_iou = True
            if not hand_lever_iou:
                self.flag1time, _, flag = self.duration(self.flag1time, 1.0)
                if flag:
                    # self.scorePoint1 = True
                    # self.assignScore(1, front_img0, front_pres)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        pass

    # 2
    def mea_lever_zero(self, score_index, hands_front, nuts_front, levers_front, boutns_front, hook_weights_front):
        """
        调节平衡螺母 杠杆水平调零使平衡 : 手和螺母有交集并且记录一下表示已经调过螺母,手和螺母没有交集且手和杠杆没有交集 在一定时间范围内给分
        :param hands_front:
        :param nuts_front:
        :param levers_front:
        :param boutns_front:
        :param hook_weights_front:
        :param front_img0:
        :param front_pres:
        :return:
        """
        if hands_front.shape[0] != 0 and nuts_front.shape[0] != 0 and levers_front.shape[0] != 0 and \
                boutns_front.shape[0] != 0:
            if hook_weights_front.shape[0] == 0:
                for hand_front in hands_front:
                    if self.flag2:
                        break
                    for nut_front in nuts_front:
                        if iou(hand_front[:4], nut_front[:4]) > 0:
                            self.flag2 = True
                            break
                # 若手已经接触过螺母 则已经调零;接下来判断天平平衡
                if self.flag2:
                    is_balance = True
                    for hand_front in hands_front:

                        for nut_front in nuts_front:
                            if iou(hand_front[:4], nut_front[:4]) == 0 and \
                                    iou(hand_front[:4], levers_front[0][:4]) == 0:
                                continue
                            else:
                                is_balance = False
                    if is_balance:
                        self.flag2time, _, flag = self.duration(self.flag2time, 1.0)
                        if flag:
                            # self.scorePoint2 = True
                            # self.assignScore(2, front_img0, front_pres)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        pass

    # 3
    def mea_dynamometer_zero(self, score_index, heads_front, spring_ergometers_front, hook_weights_front, levers_front):
        """
        弹簧测力计调零 : 首先钩码不在杠杆上,头的垂直中心点和弹簧测力计 在一个范围内,最后保持状态在一个时间范围内给分
        :param heads_front:
        :param spring_ergometers_front:
        :param hook_weights_front:
        :param levers_front:
        :param front_img0:
        :param front_pres:
        :return:
        """
        if heads_front.shape[0] != 0 and spring_ergometers_front.shape[0] != 0:
            spr_status = True
            if hook_weights_front.shape[0] != 0 and levers_front.shape[0] != 0:
                for hook_weight_front in hook_weights_front:
                    h_l_iou = iou(hook_weight_front[:4], levers_front[0][:4])
                    if h_l_iou != 0:
                        spr_status = False
                        break
            if spr_status:
                is_balance3 = False
                for head_front in heads_front:
                    if abs(center_distance_v(head_front[:4],
                                             spring_ergometers_front[0][:4])) < 0.1111 * self.frame_front.shape[0]:
                        is_balance3 = True
                        break
                if is_balance3:
                    self.flag3time, _, flag = self.duration(self.flag3time, 1.0)
                    if flag:
                        # self.scorePoint3 = True
                        # self.assignScore(3, front_img0, front_pres)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4
    def both_side_mea(self, score_index, levers_front, boutns_front, nuts_front, hook_weights_front, hands_front):
        """
        杠杆两侧测力 : 手和螺母.手和杠杆没有交集的前提下 获取杠杆左右钩码数,通过判断左右钩码数不相等,杠杆宽高比在一个范围内 平衡
        :param levers_front:
        :param boutns_front:
        :param nuts_front:
        :param hook_weights_front:
        :param hands_front:
        :param front_img0:
        :param front_pres:
        :return:
        """
        if levers_front.shape[0] != 0 and \
                boutns_front.shape[0] != 0 and nuts_front.shape[0] != 0 \
                and hook_weights_front.shape[0] != 0:
            hand_status = True
            if hands_front.shape[0] != 0:
                for hand_front in hands_front:
                    hand_lever_iou = iou(hand_front[:4], levers_front[0][:4])
                    for nut_front in nuts_front:
                        hand_nut_iou = iou(nut_front[:4], hand_front[:4])
                        if hand_nut_iou == 0 and hand_lever_iou == 0:
                            continue
                        else:
                            hand_status = False
            if hand_status:
                # 获取左右钩码
                left_hook, right_hook = self.get_hookweight_num(hook_weights_front, boutns_front,
                                                                levers_front, self.frame_front)
                if len(left_hook) and len(right_hook) and len(left_hook) != len(right_hook):
                    if w_h_ratio(levers_front[0][:4]) > 6:
                        self.flag4time, _, flag = self.duration(self.flag4time, 0.1)
                        if flag:
                            # self.scorePoint4 = True
                            # self.assignScore(4, front_img0, front_pres)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
            else:
                self.flag4time = 0

    # 5
    def same_side_mea(self, score_index, levers_front, boutns_front, nuts_front, hook_weights_front,
                      spring_ergometers_front, hands_front):
        """
        杠杆同一侧测力: 弹簧测力计在frame的上方,,且杠杆宽高比在一个范围内情况下,获取杠杆左右钩码数,哪侧没有钩码,则表明在对面侧测量,判断弹簧测力计
        与黑旋钮的位置判断与钩码在同一侧, 弹簧测力计宽高比在一个范围且杠杆宽高比在一个范围,手与螺母没有交集且手与杠杆没有交集,
        且手与弹簧测力计的交并比率在一个范围内
        同理 右侧 ...

        :param levers_front:
        :param boutns_front:
        :param nuts_front:
        :param hook_weights_front:
        :param spring_ergometers_front:
        :param hands_front:
        :param front_img0:
        :param front_pres:
        :return:
        """
        if levers_front.shape[0] != 0 and \
                boutns_front.shape[0] != 0 and nuts_front.shape[0] == 2 and \
                hook_weights_front.shape[0] != 0 and \
                spring_ergometers_front.shape[0] != 0:
            # 弹簧测力计在上方
            if center_point(spring_ergometers_front[0][:4])[1] < self.frame_front.shape[0] * 0.5 and \
                    w_h_ratio(levers_front[0][:4]) > 6:
                # # 获取左右钩码
                left_hook, right_hook = self.get_hookweight_num(hook_weights_front, boutns_front,
                                                                levers_front, self.frame_front)
                # 左侧
                if center_distance_h(spring_ergometers_front[0][:4], boutns_front[0][:4]) < 0:
                    if left_hook and not right_hook:
                        spr_w_h_ratio = w_h_ratio(spring_ergometers_front[0][:4]) < 0.6
                        # print(f"spr_w_h_ratio xxxxx1029----{spr_w_h_ratio}")
                        lever_w_h_ratio = w_h_ratio(levers_front[0][:4]) > 6
                        if spr_w_h_ratio and lever_w_h_ratio:
                            is_balance_5 = True
                            if hands_front.shape[0] != 0:
                                for nut_front in nuts_front:
                                    for hand_front in hands_front:
                                        hand_nut_iou = iou(hand_front[:4], nut_front[:4])
                                        hand_lever_iou = iou(hand_front[:4], levers_front[0][:4])
                                        hand_pri_iou = iou(hand_front[:4], spring_ergometers_front[0][:4], True)
                                        if hand_lever_iou == 0 and hand_nut_iou == 0 and hand_pri_iou < 0.1:
                                            pass
                                        else:
                                            is_balance_5 = False
                                            break

                            if is_balance_5:
                                self.flag5time, _, flag = self.duration(self.flag5time, 1.0)
                                if flag:
                                    # self.scorePoint5 = True
                                    # self.assignScore(5, front_img0, front_pres)
                                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
                else:
                    if not left_hook and right_hook:
                        spr_w_h_ratio = w_h_ratio(spring_ergometers_front[0][:4]) < 0.6
                        # print(f"spr_w_h_ratioyyyyy1029----{spr_w_h_ratio}")
                        lever_w_h_ratio = w_h_ratio(levers_front[0][:4]) > 6
                        if spr_w_h_ratio and lever_w_h_ratio:
                            is_balance_5 = True
                            if hands_front.shape[0] != 0:
                                for nut_front in nuts_front:
                                    for hand_front in hands_front:
                                        hand_nut_iou = iou(hand_front[:4], nut_front[:4])
                                        hand_lever_iou = iou(hand_front[:4], levers_front[0][:4])
                                        hand_spr_iou = iou(hand_front[:4], spring_ergometers_front[0][:4], True)
                                        # print(f"hand_spr_iou============={hand_spr_iou}")
                                        if hand_lever_iou == 0 and hand_nut_iou == 0 and hand_spr_iou < 0.1:
                                            pass
                                        else:
                                            is_balance_5 = False
                                            break
                            if is_balance_5:
                                self.flag5time, _, flag = self.duration(self.flag5time, 1.0)
                                if flag:
                                    # self.scorePoint5 = True
                                    # self.assignScore(5, front_img0, front_pres)
                                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 6
    def change_pos_mea(self, score_index, levers_front, boutns_front, nuts_front, hook_weights_front,
                       spring_ergometers_front, hands_front, ):
        """
        改变钩码个数,位置以及弹簧测力计拉杠杆的位置,再完成几组实验:
        1 获取杠杆上钩码的左右个数, 判断弹簧测力计与黑旋钮的位置判断弹簧测力计与钩码在同一侧测量
        2 同在左侧 弹簧测力计在一个范围 ,杠杆的宽高比在一个范围 手与杠杆没有交集 手与螺母没有交集的情况下
        3 保持2状态在3秒 判断钩码与黑旋钮水平方向的位置,与上一次位置比不在一个范围内,则表明移动了钩码位置,移动位置次数达到3 给分

        右侧同理...

        :param levers_front:
        :param boutns_front:
        :param nuts_front:
        :param hook_weights_front:
        :param spring_ergometers_front:
        :param hands_front:
        :param front_img0:
        :param front_pres:
        :return:
        """
        if levers_front.shape[0] != 0 and boutns_front.shape[0] != 0 and nuts_front.shape[0] != 0 \
                and hook_weights_front.shape[0] != 0:

            # 钩码数量
            # 获取左右钩码
            left_hook, right_hook = self.get_hookweight_num(hook_weights_front, boutns_front,
                                                            levers_front, self.frame_front)
            # 两侧测量
            # if len(left_hook) and len(right_hook) and len(left_hook) != len(right_hook):
            #     # 左右两边有滑块(左右两边挂钩码使杠杆平衡) --> 遍历钩码数
            #     # 两边悬挂不同的钩码 且 手与杠杆没有交集 且 两个nut 垂直距离 在范围内则判断平衡
            #     self.flag6 = True
            #     if hands_front.shape[0] != 0:
            #         for hand_front in hands_front:
            #             hand_lever_iou = iou(hand_front[:4], levers_front[0][:4])
            #             for nut_front in nuts_front:
            #                 hand_nut_iou = iou(nut_front[:4], hand_front[:4])
            #                 if hand_nut_iou == 0 and hand_lever_iou == 0:
            #                     continue
            #                 else:
            #                     self.flag6 = False
            #     # 手与螺母没交集; 手与杠杆没有交集
            #     if self.flag6:
            #         # 判断杠杆平衡
            #         if w_h_ratio(levers_front[0][:4]) > 6:
            #             if self.flag6time == 0:
            #                 self.flag6time = time.time()
            #             else:
            #                 if time.time() - self.flag6time > 3:
            #                     # 添加钩码个数
            #                     # if len(self.left_hook_num_list) > 10:
            #                     #     self.left_hook_num_list.clear()
            #                     # if len(self.right_hook_num_list) > 10:
            #                     #     self.right_hook_num_list.clear()
            #                     # if len(left_hook) not in self.left_hook_num_list:
            #                     #     self.left_hook_num_list.append(len(left_hook))
            #                     # if len(right_hook) not in self.right_hook_num_list:
            #                     #     self.right_hook_num_list.append(len(right_hook))
            #                     for hook_weight_front in hook_weights_front:
            #                         # 滑块在铁杆左侧
            #                         hook_boutn_dist = center_distance_h(hook_weight_front[:4],
            #                                                             boutns_front[0][:4])
            #                         if iou(hook_weight_front[:4], levers_front[0][:4]) > 0 and hook_boutn_dist<0:
            #                             if not self.left_slider_pos[-1]-0.0104*front_img0.shape[1] < hook_boutn_dist < self.left_slider_pos[-1] + 0.0104*front_img0.shape[1]:
            #                                 self.left_slider_pos.append(hook_boutn_dist)
            #                         if iou(hook_weight_front[:4], levers_front[0][:4]) > 0 and hook_boutn_dist > 0:
            #                             if not self.right_slider_pos[-1]-0.0104*front_img0.shape[1] <hook_boutn_dist < self.right_slider_pos[-1] +0.0104*front_img0.shape[1]:
            #                                 self.right_slider_pos.append(hook_boutn_dist)
            #                     print(self.left_slider_pos, self.right_slider_pos)
            #             if len(self.left_slider_pos) == 3:
            #                 self.scorePoint6 = True
            #                 self.assignScore(6, front_img0)
            #                 self.left_slider_pos = [0.0]
            #                 self.right_slider_pos = [0.0]
            #         else:
            #             self.flag4time = 0

            # # 同在左侧
            if len(left_hook) and not len(right_hook) and spring_ergometers_front.shape[0] != 0 and \
                    center_distance_h(spring_ergometers_front[0][:4], boutns_front[0][:4]) < 0:
                left_hookweight_num = 0
                spr_w_h_ratio = w_h_ratio(spring_ergometers_front[0][:4]) < 0.6
                # print(f"spr_w_h_ratio----{spr_w_h_ratio}")
                lever_w_h_ratio = w_h_ratio(levers_front[0][:4]) > 6
                is_balance_6 = True
                if hands_front.shape[0] != 0:
                    for nut_front in nuts_front:
                        for hand_front in hands_front:
                            hand_nut_iou = iou(hand_front[:4], nut_front[:4])
                            hand_lever_iou = iou(hand_front[:4], levers_front[0][:4])
                            if hand_nut_iou == 0 and hand_lever_iou == 0 and spr_w_h_ratio and lever_w_h_ratio:
                                continue
                            else:
                                is_balance_6 = False
                else:
                    if not spr_w_h_ratio or not lever_w_h_ratio:
                        is_balance_6 = False

                if is_balance_6:
                    if self.flag6time == 0:
                        self.flag6time = time.time()
                    else:
                        if time.time() - self.flag6time > 3:
                            # todo: 接下来判断弹簧测力挂住滑块的位置这个位置代表是否移动是最合适的; 目前用的是滑块和钩码挂住的位置 作为判断依据
                            # 添加钩码个数
                            for hook_weight_front in hook_weights_front:
                                hook_boutn_dist = center_distance_h(hook_weight_front[:4],
                                                                    boutns_front[0][:4])
                                if iou(hook_weight_front[:4], levers_front[0][:4]) > 0 \
                                        and hook_boutn_dist < 0:
                                    if not self.single_slider_pos[-1] - 0.01 * self.frame_front.shape[
                                        1] < hook_boutn_dist < \
                                           self.single_slider_pos[-1] + 0.01 * self.frame_front.shape[1]:  # 10
                                        self.single_slider_pos.append(hook_boutn_dist)
                            if len(self.single_slider_pos) == 3:
                                # self.scorePoint6 = True
                                # self.assignScore(6, front_img0, front_pres)
                                self.single_slider_pos = [0.0]
                                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
                else:
                    self.flag6time = 0

            # # 同在右侧
            if not len(left_hook) and len(right_hook) and spring_ergometers_front.shape[0] != 0 and \
                    center_distance_h(spring_ergometers_front[0][:4], boutns_front[0][:4]) > 0:
                spr_w_h_ratio = w_h_ratio(spring_ergometers_front[0][:4]) < 0.6
                # print(f"spr_w_h_ratio----right----{spr_w_h_ratio}")
                lever_w_h_ratio = w_h_ratio(levers_front[0][:4]) > 6
                is_balance_6 = True
                if hands_front.shape[0] != 0:
                    for nut_front in nuts_front:
                        for hand_front in hands_front:
                            hand_nut_iou = iou(hand_front[:4], nut_front[:4])
                            hand_lever_iou = iou(hand_front[:4], levers_front[0][:4])
                            if hand_nut_iou == 0 and hand_lever_iou == 0 and spr_w_h_ratio and lever_w_h_ratio:
                                # todo: 需要并上  spring_ergometers_front 宽高比 需要实际测出宽高比在哪个范围内而判断
                                # print(f"弹簧测力计宽高比44444 you--------")
                                # print(w_h_ratio(spring_ergometers_front[0][:4]))
                                # print(f"弹簧测力计宽高比44444 you--------")
                                # is_balance_6 = True
                                continue
                            else:
                                is_balance_6 = False
                else:
                    if not spr_w_h_ratio or not lever_w_h_ratio:
                        is_balance_6 = False
                if is_balance_6:
                    if self.flag6time == 0:
                        self.flag6time = time.time()
                    else:
                        if time.time() - self.flag6time > 3:
                            for hook_weight_front in hook_weights_front:
                                hook_boutn_dist = center_distance_h(hook_weight_front[:4],
                                                                    boutns_front[0][:4])
                                if iou(hook_weight_front[:4], levers_front[0][:4]) > 0 \
                                        and hook_boutn_dist > 0:
                                    if not self.single_slider_pos[-1] - 0.01 * self.frame_front.shape[
                                        1] < hook_boutn_dist < \
                                           self.single_slider_pos[
                                               -1] + 0.01 * self.frame_front.shape[1]:  # 10
                                        self.single_slider_pos.append(hook_boutn_dist)

                            if len(self.single_slider_pos) == 3:
                                # self.scorePoint6 = True
                                # self.assignScore(6, front_img0, front_pres)
                                self.single_slider_pos = [0.0]
                                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                else:
                    self.flag6time = 0
        pass

    # 清理桌面
    def clearn_desk(self,score_index, top_items, front_items):
        # if self.desk_is_clearn(top_items, front_items):
        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
            # self.clearn_desk_info = [7, self.front_img0, self.front_preds, time.time()]
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]

            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 2)
            if flag:
                # self.assignScore(7, self.top_img0, self.top_preds)
                self.clearn_f_num = 0
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        else:
            self.clearn_f_num = 0

    # def desk_is_clearn(self, top_items, front_items):
    #     # for items in top_items:
    #     #     if items.shape[0] == 0:
    #     #         continue
    #     #     else:
    #     #         for item in items:
    #     #             item_box = item[:4]
    #     #             if pt_in_box(center_point(item_box), self.center_box_top) > 0:
    #     #                 return False
    #     for items in front_items:
    #         if items.shape[0] == 0:
    #             continue
    #         else:
    #             for item in items:
    #                 item_box = item[:4]
    #                 if pt_in_box(center_point(item_box), self.center_box_front) > 0:
    #                     return False
    #     return True

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info)
            return True