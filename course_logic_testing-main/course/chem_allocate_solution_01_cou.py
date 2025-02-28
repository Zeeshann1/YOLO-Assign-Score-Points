#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 14:34
# @Author  : Qiguangnan
# @File    : phy_density_liquid_01_cou.py
# import traceback
from copy import deepcopy
# from .comm import *
# from queue import Queue
# import cv2
# from threading import Thread
# from pathlib import Path
# from util import ts2ft
# from concurrent.futures import ThreadPoolExecutor
# from config import experimental_site_top as est
# from config import experimental_site_front as esf
# from config import EXP_MAP

from .comm import *
from .comm.course_base import ConfigModel

import traceback
from logger import logger
from configg.global_config import experimental_site_top as est
from configg.global_config import experimental_site_front as esf

import cv2
import numpy as np


class CHEM_allocate_solution_01(ConfigModel):

    def __init__(self):
        super(CHEM_allocate_solution_01, self).__init__()

        # self.labels = labels
        # self.conf_thres_list = conf_thres_list
        # self.max_cn_list = max_cn_list
        # self.plot = Plot(labels, EN_CH_map)
        # self.save_path = Path(save_path)
        # self.flag = self.save_path.name
        # self.exper_id = self.save_path.parent.name
        # self.scorePointInfo = EXP_MAP[self.exper_id]['scorePointInfo']  # type: dict
        # self.modelInfo = EXP_MAP[self.exper_id]['modelInfo']
        # self.postNMSQueue = postNMSQueue  # type: Queue # 摄像头经模型预测框
        # self.stopSignalQueue = stopSignalQueue
        # self.actual_time = actual_time
        # self.local_start_time = local_start_time

        self.plot = Plot(labels=self.labels, EN_CH_map=self.EN_CH_map)

        self.h_top = 0  # 顶视 高
        self.w_top = 0  # 顶视 宽
        self.h_front = 0  # 前视 高
        self.w_front = 0  # 前视 宽
        self.set_center_box = False
        self.initScore()

    def initScore(self):
        self.weight_f_num = 0  # 称量
        self.weight_f_num_pre = 0
        self.weight_operate = False
        self.balance_f_num = 0  # 天平平衡
        self.balance_f_num_pre = 0
        self.add_water_operate = False
        self.add_water_f_num = 0  # 加水
        self.add_water_f_num_pre = 0  # 加水

        self.check_f_num = 0  # 检查容量瓶是否漏水
        self.check_f_num_pre = 0  # 检查容量瓶是否漏水

        self.rod_drainage_f_num = 0  # 玻璃棒引流
        self.rod_drainage_f_num_pre = 0  # 玻璃棒引流

        self.washing_num = 0  # 洗 次数
        self.dumping_num = 0  # 倒 次数
        self.wash_f_num = 0
        self.wash_f_num_pre = 0
        self.dump_f_num = 0
        self.dump_f_num_pre = 0

        self.dropper_f_num = 0  # 胶头滴管
        self.dropper_f_num_pre = 0

        self.shock_info = []  # 记录震荡信息

        self.see_scale_line_f_num = 0  # 定容看刻度线
        self.see_scale_line_f_num_pre = 0

        self.stir_f_num = 0  # 搅拌
        self.stir_f_num_pre = 0

        self.clearn_f_num = 0
        self.clearn_desk_info = []

    def preProcess(self, preds_pre):
        preds = []
        for label, info in self.modelInfo.items():  ## 提出每类的框
            index = info['index']
            conf = info['conf']
            max_cn = info['max_cn']  # 该类别最大的数量
            ca = preds_pre[preds_pre[:, -1] == index]  ## 单类别结果
            ca = ca[ca[:, 4] > conf]
            if max_cn != 0 and ca.shape[0] > max_cn:
                ca = ca[ca[:, 4].argsort(descending=True)][:max_cn]
            preds.append(ca)
        return preds


    def setCenterBox(self, device,top_img0,front_img0, est=None, esf=None):  # 设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
        if est:
            self.h_top, self.w_top = top_img0.shape[:2]
            self.center_box_top = torch.tensor(
                [self.w_top * est[0], self.h_top * est[1], self.w_top * est[2], self.h_top * est[3]],
                device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
        if esf:
            self.h_front, self.w_front = front_img0.shape[:2]
            self.center_box_front = torch.tensor(
                [self.w_front * esf[0], self.h_front * esf[1], self.w_front * esf[2], self.h_front * esf[3]],
                device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
        self.set_center_box = True

    def run_one_result_process(self, frame_top, frame_front, frame_side,
                               pred_top, pred_front, pred_side,
                               time_top, time_front, time_side,
                               num_frame_top,
                               num_frame_front,
                               num_frame_side,
                               path_save,
                               names_label):
        time_process_start = time.time()

        self.time_top = time_top
        self.time_front = time_front
        self.num_frame_top = num_frame_top
        self.num_frame_front = num_frame_front

        front_true = False
        top_true = False
        side_true = False
        device_use = "cuda :0"
        self.front_preds = None
        self.top_preds = None
        if pred_front != None and pred_front.shape[0]:
            self.front_preds, self.objects_front = self.assign_labels(frame_front, pred_front, names_label)
            front_true = True
            device_use = pred_front.device
        if pred_top != None and pred_top.shape[0]:
            self.top_preds, self.objects_top = self.assign_labels(frame_top, pred_top, names_label)
            top_true = True
            device_use = pred_top.device
        # if pred_side != None and pred_side.shape[0]:
        #     side_preds, objects_side = self.assign_labels(frame_side, pred_side, names_label)
        #     side_true = True
        #     device_use = pred_side.device

        self.rtmp_push_fun(top_img=frame_top,front_img=frame_front,side_img=frame_side,
                           top_preds=self.top_preds,front_preds=self.front_preds,side_preds=None)

        if not self.set_center_box:
            self.setCenterBox(device_use,frame_top,frame_front, est, esf)  # 设置操作中心区域

        if top_true or front_true:
            # 赋分逻辑部分
            if front_true:
                hands_front, eyes_front, heads_front, dusters_front, scales_front, salvers_front, nuts_front, \
                yms_front, rlps_front, lines_front, plugs_front, rlpds_front, gkps_front, xkps_front, xkpks_front, \
                pswdfs_front, psdfs_front, clzs_front, column_ws_front, liquids_front, nacls_front, spoons_front, \
                beakers_front, rods_front, droppers_front = self.front_preds

            if top_true:
                hands_top, eyes_top, heads_top, dusters_top, scales_top, salvers_top, nuts_top, yms_top, rlps_top, \
                lines_top, plugs_top, rlpds_top, gkps_top, xkps_top, xkpks_top, pswdfs_top, psdfs_top, clzs_top, column_ws_top, \
                liquids_top, nacls_top, spoons_top, beakers_top, rods_top, droppers_top = self.top_preds

            if self.dumping_num < 4 and top_true and front_true:
                self.washing(beakers_front, xkpks_front, beakers_top, xkpks_top, rlps_front, rods_front)

            # 托盘天平称量药品操作正确
            if not self.scorePoint1 and top_true and front_true:
                if self.weight(scales_top, clzs_top, nacls_top, salvers_front, nuts_front):
                    # self.assignScore(1, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=1,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="1.jpg",
                                     preds=self.front_preds
                                     )

            # 加入蒸馏水适量
            if not self.scorePoint2  and front_true \
                    and pswdfs_front.shape[0] == 0 and (not top_true or pswdfs_top.shape[0] == 0):
                if self.add_water(beakers_front, liquids_front):
                    # self.assignScore(2, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=2,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="2.jpg",
                                     preds=self.front_preds
                                     )

            # 3 搅拌操作正确 4 食盐完全溶解
            if ((not self.scorePoint3) or (not self.scorePoint4)) and front_true and top_true:
                if self.stir_dissolve(hands_front, rods_front, beakers_front, hands_top, rods_top, beakers_top) == 1:
                    # self.assignScore(3, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=3,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="3.jpg",
                                     preds=self.front_preds
                                     )
                if self.stir_dissolve(hands_front, rods_front, beakers_front, hands_top, rods_top, beakers_top) == 2:
                    # self.assignScore(4, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=4,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="4.jpg",
                                     preds=self.front_preds
                                     )

            # 5 检查容量瓶是否漏水操作正确
            if (not self.scorePoint5 and front_true and
                    (self.scorePoint6 + self.scorePoint7 + self.scorePoint8 + self.scorePoint9 +
                     self.scorePoint10 + self.scorePoint11 + self.scorePoint12 == 0)):
                if self.check(rlps_front, rlpds_front):
                    # self.assignScore(5, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=5,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="5.jpg",
                                     preds=self.front_preds
                                     )

            # 6 用玻璃棒引流
            if not self.scorePoint6 and front_true:
                if self.drainage(rlps_front, rods_front, beakers_front):
                    # self.assignScore(6, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=6,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="6.jpg",
                                     preds=self.front_preds
                                     )

            # 7 洗涤烧杯内壁2-3次，并将洗涤液一并转移到容量瓶中操作正确
            if not self.scorePoint7 and self.dumping_num == 3 and front_true:
                # self.assignScore(7, self.front_img0, self.front_preds)
                conf_c = 0.1
                self.assignScore(index=7,
                                 img=frame_front,
                                 object=self.objects_front,
                                 conf=conf_c,
                                 time_frame=self.time_front,
                                 num_frame=self.num_frame_front,
                                 name_save="7.jpg",
                                 preds=self.front_preds
                                 )

            # 8 振荡容量瓶操作正确
            if (self.dumping_num > 1 and
                    front_true and
                    not self.scorePoint8 and
                    not self.scorePoint9 and
                    not self.scorePoint10 and
                    not self.scorePoint11 and
                    not self.scorePoint12):
                if self.shock(hands_front, rlps_front, rlpds_front):
                    # self.assignScore(8, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=8,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="8.jpg",
                                     preds=self.front_preds
                                     )

            # 9 使用胶头滴管操作
            if not self.scorePoint9 and front_true:
                if self.dropper_correct(droppers_front, rlpds_front):
                    # self.assignScore(9, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=9,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="9.jpg",
                                     preds=self.front_preds
                                     )

            # 10 定容时视线与刻度线相平
            if not self.scorePoint10 and front_true:
                if self.constant_volume(eyes_front, heads_front, column_ws_front):
                    # self.assignScore(10, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=10,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="10.jpg",
                                     preds=self.front_preds
                                     )

            # 11 盖好瓶塞，反复上下颠倒，摇匀
            if (not self.scorePoint11 and front_true and plugs_front.shape[0] == 0 and
                    (self.scorePoint9 + self.scorePoint10) > 0):
                if self.upside_down(rlps_front, rlpds_front):
                    # self.assignScore(11, self.front_img0, self.front_preds)
                    conf_c = 0.1
                    self.assignScore(index=11,
                                     img=frame_front,
                                     object=self.objects_front,
                                     conf=conf_c,
                                     time_frame=self.time_front,
                                     num_frame=self.num_frame_front,
                                     name_save="11.jpg",
                                     preds=self.front_preds
                                     )

            # 12 清洗、整理仪器、药品
            if top_true:
                top_items = [dusters_top, scales_top, rlps_top, rlpds_top, gkps_top, xkps_top, xkpks_top,
                             pswdfs_top, psdfs_top, clzs_top, nacls_top, spoons_top, beakers_top, rods_top, droppers_top]
            else:
                top_items = []
            if front_true:
                front_items = [dusters_front, scales_front, rlps_front, rlpds_front, gkps_front, xkps_front, xkpks_front,
                               pswdfs_front, psdfs_front, clzs_front, spoons_front, beakers_front, rods_front, droppers_front]
            else:
                front_items = []
            if not self.scorePoint12 and len(self.score_list) > 2:
                self.clearn_desk(12, top_items, front_items,frame_top,frame_front)
            if self.scorePoint12 and len(self.score_list) != 12:
                if not self.desk_is_clearn([top_items, front_items], [self.center_box_top, self.center_box_front]):
                    self.retracementScore(12)

    # 1 托盘天平称量药品操作正确
    # 顶视 天平、称量纸、食盐颗粒、药匙
    # 前视 托盘、调节螺母
    def weight(self, scales_top, clzs_top, nacls_top, salvers_front, nuts_front):
        if not self.weight_operate and nacls_top.shape[0] > 0 and scales_top.shape[0] > 0 and clzs_top.shape[0] > 0:
            nacl_top_box = nacls_top[0][:4]
            scale_top_box = scales_top[0][:4]
            if center_distance_h(scale_top_box, nacl_top_box) > 0:  # 食盐在左边，左右托盘上有称量纸
                clz_top_boxes = []
                for clzs_top in clzs_top:
                    clz_top_box = clzs_top[:4]
                    if iou(clz_top_box, scale_top_box) > box_area(clz_top_box) * 0.5:
                        clz_top_boxes.append(clz_top_box)
                if len(clz_top_boxes) == 2:
                    self.weight_f_num, self.weight_f_num_pre, flag = self.duration(self.weight_f_num,
                                                                                   3,
                                                                                   self.weight_f_num_pre,
                                                                                   1)
                    if flag:
                        self.weight_operate = True
        if self.weight_operate:
            balance = False
            if salvers_front.shape[0] == 2:
                if abs(salvers_front[0][3] - salvers_front[1][3]) < self.h_front * 0.015:
                    balance = True
            if not balance and nuts_front.shape[0] == 2:
                if center_distance_v(nuts_front[0][:4], nuts_front[1][:4]) < self.h_front * 0.015:
                    balance = True
            if balance:
                self.balance_f_num, self.balance_f_num_pre, flag = self.duration(self.balance_f_num,
                                                                                 2,
                                                                                 self.balance_f_num_pre,
                                                                                 0.5)
                if flag:
                    return True

    # 2 加入蒸馏水适量
    def add_water(self, beakers_front, liquids_front):
        if self.washing_num == 1:
            if liquids_front.shape[0] > 0 and beakers_front.shape[0] > 0:
                beaker_front_box = beakers_front[0][:4]
                for liquid_front in liquids_front:
                    liquid_front_box = liquid_front[:4]
                    if iou(beaker_front_box, liquid_front_box) > box_area(liquid_front) * 0.8:
                        self.add_water_f_num, self.add_water_f_num_pre, flag = self.duration(self.add_water_f_num,
                                                                                             2,
                                                                                             self.add_water_f_num_pre,
                                                                                             0.5)
                        return flag

    # 3 搅拌操作正确 4 食盐完全溶解
    def stir_dissolve(self, hands_front, rods_front, beakers_front, hands_top, rods_top, beakers_top, ):
        stir = False
        if rods_front.shape[0] > 0 and beakers_front.shape[0] > 0 and hands_front.shape[0] > 0:
            rod_front_box = rods_front[0][:4]
            beaker_front_box = beakers_front[0][:4]
            hand_rod = False
            hand_beaker = False
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if not hand_rod and iou(hand_front_box, rod_front_box) > 0:
                    hand_rod = True
                if not hand_beaker and iou(hand_front_box, beaker_front_box) > 0:
                    hand_beaker = True
            if hand_rod and hand_beaker and iou(rod_front_box, beaker_front_box) > 0 and \
                    center_distance_v(beaker_front_box, rod_front_box) > 0:
                stir = True
        if not stir and rods_top.shape[0] > 0 and beakers_top.shape[0] > 0 and hands_top.shape[0] > 0:
            rod_top_box = rods_top[0][:4]
            beaker_top_box = beakers_top[0][:4]
            hand_rod = False
            hand_beaker = False
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if not hand_rod and iou(hand_top_box, rod_top_box) > 0:
                    hand_rod = True
                if not hand_beaker and iou(hand_top_box, beaker_top_box) > 0:
                    hand_beaker = True
            if hand_rod and hand_beaker and iou(rod_top_box, beaker_top_box) > 0:
                stir = True
        if stir:
            self.stir_f_num, self.stir_f_num_pre, flag = self.duration(self.stir_f_num,
                                                                       15,
                                                                       self.stir_f_num_pre,
                                                                       3)
            if not self.scorePoint3 and self.stir_f_num != 0 and time.time() - self.stir_f_num > 5:
                return 1
            if flag:
                return 2

    # 5 检查容量瓶是否漏水操作正确
    def check(self, rlps_front, rlpds_front):
        if rlps_front.shape[0] > 0 and rlpds_front.shape[0] > 0:
            rlp_front_box = rlps_front[0][:4]
            rlpd_front_box = rlpds_front[0][:4]
            if (rlpd_front_box[0] < center_point(rlp_front_box)[0] < rlpd_front_box[2] and
                    center_distance_v(rlp_front_box, rlpd_front_box) > 0):
                self.check_f_num, self.check_f_num_pre, flag = self.duration(self.check_f_num,
                                                                             5,
                                                                             self.check_f_num_pre,
                                                                             2)
                if flag:
                    return True

    # 6 用玻璃棒引流
    def drainage(self, rlps_front, rods_front, beakers_front):
        if rlps_front.shape[0] > 0 and rods_front.shape[0] > 0 and beakers_front.shape[0] > 0:
            rlp_front_box = rlps_front[0][:4]
            rod_front_box = rods_front[0][:4]
            beaker_front_box = beakers_front[0][:4]
            if (iou(rod_front_box, rlp_front_box) > 0 and  # 玻璃棒 容量瓶
                    center_distance_v(rlp_front_box, rod_front_box) > 0 and  # 玻璃棒在容量瓶上
                    iou(beaker_front_box, rod_front_box) > 0 and
                    center_distance_v(rlp_front_box, beaker_front_box) > 0):
                self.rod_drainage_f_num, self.rod_drainage_f_num_pre, flag = self.duration(self.rod_drainage_f_num,
                                                                                           4,
                                                                                           self.rod_drainage_f_num_pre,
                                                                                           2)
                if flag:
                    return True

    # 7 洗涤烧杯内壁2-3次，并将洗涤液一并转移到容量瓶中操作正确
    def washing(self, beakers_front, xkpks_front, beakers_top, xkpks_top, rlps_front, rods_front):
        if self.washing_num == self.dumping_num:
            add_water = False
            if beakers_front.shape[0] > 0 and xkpks_front.shape[0] > 0:
                beaker_front_box = beakers_front[0][:4]
                xkpk_front_box = xkpks_front[0][:4]
                xkpk_beaker_cv_d = abs(center_distance_h(xkpk_front_box, beaker_front_box))  # 细口瓶口、烧杯水平中心距离
                xkpk_beaker_uv_d = beaker_front_box[1] - center_point(xkpk_front_box)[1]  # 细口瓶口中心、烧杯顶部垂直距离
                if ((xkpk_beaker_cv_d < (beaker_front_box[2] - beaker_front_box[0]) / 2) and
                        (xkpk_beaker_uv_d > 0)):
                    add_water = True
            if not add_water and beakers_top.shape[0] > 0 and xkpks_top.shape[0] > 0:
                beaker_top_box = beakers_top[0][:4]
                xkpk_top_box = xkpks_top[0][:4]
                if iou(beaker_top_box, xkpk_top_box) > 0:
                    add_water = True
            if add_water:
                self.wash_f_num, self.wash_f_num_pre, flag = self.duration(self.wash_f_num,
                                                                           1,
                                                                           self.wash_f_num_pre,
                                                                           1)
                if flag:
                    self.washing_num += 1  # 加水操作
                    self.wash_f_num = self.wash_f_num_pre = 0
                    return
        if self.washing_num > self.dumping_num:
            if rlps_front.shape[0] > 0 and beakers_front.shape[0] > 0 and rods_front.shape[0] > 0:
                rlp_front_box = rlps_front[0][:4]
                beaker_front_box = beakers_front[0][:4]
                rod_front_box = rods_front[0][:4]
                if (iou(rod_front_box, rlp_front_box) > 0 and  # 玻璃棒 容量瓶
                        center_distance_v(rlp_front_box, rod_front_box) > 0 and  # 玻璃棒在容量瓶上
                        iou(beaker_front_box, rod_front_box) > 0 and
                        center_point(beaker_front_box)[1] < rlp_front_box[1]):
                    self.dump_f_num, self.dump_f_num_pre, flag = self.duration(self.dump_f_num,
                                                                               2,
                                                                               self.dump_f_num_pre,
                                                                               1)
                    if flag:
                        self.dumping_num += 1
                        self.dump_f_num = 0
                        self.dump_f_num_pre = 0

    # 8 振荡容量瓶操作正确
    def shock(self, hands_front, rlps_front, rlpds_front):
        if hands_front.shape[0] > 0 and rlps_front.shape[0] > 0 and rlpds_front.shape[0] > 0:
            rlpd_front_box = rlpds_front[0][:4]
            rlp_front_box = rlps_front[0][:4]
            if center_distance_v(rlpd_front_box, rlp_front_box) > 0:
                if len(self.shock_info) >= 20:
                    period = self.period(self.shock_info)
                    if period > 1:
                        return True
                    self.shock_info.pop(0)
                self.shock_info.append(center_point(rlpd_front_box)[0])

    def period(self, array):  # 震荡频率
        a = np.array(array)
        avg_1 = np.average(a[:10])
        avg_2 = np.average(a[-10:])
        avg = (avg_1 + avg_2) / 2
        if abs(avg_1 - avg_2) < self.h_front * 0.04:
            n = 0
            big = True
            for i, v in enumerate(a):
                if i == 0:
                    big = v > avg
                else:
                    if (v > avg and big) or (v < avg and not big):
                        continue
                    else:
                        if (abs(v - avg) > 4):
                            n += 1
                            big = v > avg
            return n // 2
        return 0

    # 9 使用胶头滴管操作
    def dropper_correct(self, droppers_front, rlpds_front, ):
        if droppers_front.shape[0] > 0 and rlpds_front.shape[0] > 0:
            dropper_front_box = droppers_front[0][:4]
            rlpd_front_box = rlpds_front[0][:4]
            if center_point(dropper_front_box)[1] < rlpd_front_box[1]:
                self.dropper_f_num, self.dropper_f_num_pre, flag = self.duration(self.dropper_f_num,
                                                                                 2,
                                                                                 self.dropper_f_num_pre,
                                                                                 1)
                if flag:
                    return True

    # 10 定容时视线与刻度线相平
    def constant_volume(self, eyes_front, heads_front, column_ws_front):
        if column_ws_front.shape[0] == 0:
            return
        column_w_front_box = column_ws_front[0][:4]
        water_column_center_point_up = (
            (column_w_front_box[0] + column_w_front_box[2]) / 2, column_w_front_box[1])  # 水柱液面中心
        if eyes_front.shape[0] > 0:  # 眼睛
            eyes_front_box = []
            for eye_front in eyes_front:
                eye_front_box = eye_front[:4]
                if distance_point(center_point(eye_front_box), water_column_center_point_up) < self.h_front * 0.185:
                    eyes_front_box.append(eye_front_box)
            if len(eyes_front_box) == 0:
                return
            elif len(eyes_front_box) == 1:
                eye_center_h = center_point(eyes_front_box[0])[1]  # 眼睛中心高度
            elif len(eyes_front_box) == 2:
                eye_center_h = (center_point(eyes_front_box[0])[1] + center_point(eyes_front_box[1])[1]) / 2
            else:
                return
            dis_eye_water = abs(eye_center_h - column_w_front_box[1])
            if dis_eye_water < self.h_front * 0.135:
                self.see_scale_line_f_num, self.see_scale_line_f_num_pre, flag = self.duration(
                    self.see_scale_line_f_num,
                    1,
                    self.see_scale_line_f_num_pre,
                    0.3)
                return True
        if heads_front.shape[0] > 0:  # 只检测出头
            heads_front_box = []
            for head_front in heads_front:
                head_front_box = head_front[:4]
                dis_head_water = distance_point(center_point(head_front_box), water_column_center_point_up)
                if dis_head_water < self.h_front * 0.185:
                    heads_front_box.append(head_front_box)
            if len(heads_front_box) == 1:
                self.see_scale_line_f_num, self.see_scale_line_f_num_pre, flag = self.duration(
                    self.see_scale_line_f_num,
                    1,
                    self.see_scale_line_f_num_pre,
                    0.3)
                if flag:
                    return True

    # 11 盖好瓶塞，反复上下颠倒，摇匀
    def upside_down(self, rlps_front, rlpds_front):
        if rlps_front.shape[0] > 0 and rlpds_front.shape[0] > 0:
            rlp_front_box = rlps_front[0][:4]
            rlpd_front_box = rlpds_front[0][:4]
            if (rlpd_front_box[0] < center_point(rlp_front_box)[0] < rlpd_front_box[2] and
                    center_distance_v(rlp_front_box, rlpd_front_box) > 0):
                return True

    def clearn_desk(self, score_index, top_items, front_items,frame_top,frame_front):
        if self.desk_is_clearn([top_items, front_items], [self.center_box_top, self.center_box_front]):
            self.clearn_desk_info = [score_index, deepcopy(frame_top), self.top_preds,
                                     deepcopy(self.objects_top), self.time_top,self.num_frame_top]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 1)
            if flag:
                # self.assignScore(score_index, deepcopy(self.top_img0), self.top_preds)
                self.clearn_f_num = 0
                conf_c = 0.1
                self.assignScore(index=score_index,
                                 img=frame_top,
                                 object=self.objects_top,
                                 conf=conf_c,
                                 time_frame=self.time_top,
                                 num_frame=self.num_frame_top,
                                 name_save=str(score_index)+".jpg",
                                 preds=self.top_preds
                                 )
        else:
            self.clearn_f_num = 0

    def end(self):  # 实验结束时判断是否整理桌面，如果有则进行赋分
        if self.clearn_desk_info and self.num_frame_top - self.clearn_desk_info[-1] < 20:
            # self.assignScore(*self.clearn_desk_info)
            conf_c = 0.1
            self.assignScore(index=self.clearn_desk_info[0],
                             img=self.clearn_desk_info[1],
                             object=self.clearn_desk_info[3],
                             conf=conf_c,
                             time_frame=self.clearn_desk_info[4],
                             num_frame=self.clearn_desk_info[5],
                             name_save=str(self.clearn_desk_info[0]) + ".jpg",
                             preds=self.clearn_desk_info[2]
                             )
            return True

    def desk_is_clearn(self, views_items=None, center_boxes=None):
        for view_items, center_box in zip(views_items, center_boxes):
            for items in view_items:
                if items.shape[0] != 0:
                    for item in items:
                        item_box = item[:4]
                        if pt_in_box(center_point(item_box), center_box) > 0:
                            return False
        return True

    def duration(self, first_f_num, duration_time, pre_f_num=None, reclock_time=None):
        '''
        持续时间判断
        :param first_f_num: 第一次记录一个动作的起始帧数
        :param duration_time: 该动作需要持续的时间 单位： 秒
        :param pre_f_num: # 上一次记录该动作时的帧数
        :param reclock_time: # 两次记录超过该时间需要重新计算 单位 秒
        :return: first_f_num: 第一次记录时的帧数 pre_f_num 前一次记录时的帧数 flag 是否满足条件
        '''
        if reclock_time:
            if time.time() - pre_f_num > reclock_time:  # 从上次记录到现在没有此动作时间超过设置时间 重新计时
                first_f_num = pre_f_num = 0
            else:
                pre_f_num = time.time()
        if first_f_num == 0:
            if reclock_time:
                first_f_num = pre_f_num = time.time()
            else:
                first_f_num = time.time()
            return first_f_num, pre_f_num, False
        elif time.time() - first_f_num > duration_time:  # 从第一次记录到现在是否满足持续时间
            return first_f_num, pre_f_num, True
        else:
            return first_f_num, pre_f_num, False