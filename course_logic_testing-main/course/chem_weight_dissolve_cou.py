#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 15:04
# @Author  : Qiguangnan
# @File    : chem_weight_dissolve_cou.py


import random
from .comm import *
from .comm.course_base import ConfigModel
import traceback

from configg.global_config import experimental_site_top as est
from configg.global_config import experimental_site_front as esf
from copy import deepcopy
from logger import logger
import cv2


# from config.chem_weigh_dissolve_conf import CWZDCLYRJ01
# from utilsg.litF import uploaded_images, encode_image_jpg, upload_redis_or_save_json_local, ts2ft
# from configg.global_config import SCORE_ROOT_PATH
# from .comm import Plot
# from logger import logger


class CHEM_weight_dissolve(ConfigModel):

    def __init__(self):
        super(CHEM_weight_dissolve, self).__init__()

        self.open_scale_time = 0.  # 天平打开时间
        self.open_scale_time_pre = 0.  # 天平打开时间
        self.beaker_on_salver_time = 0.  # 烧杯放托盘上时间
        self.zero_time = 0.  # 天平置零
        self.zero_time_pre = 0.
        self.weight_info = []  # 记录称量信息
        self.water_column_time = 0.  # 添加水
        self.water_column_time_pre = 0.
        self.add_water = False
        self.dropper_water_info = []
        self.water_to_beaker_info = []  # 记录水导入烧杯
        self.stir_dissolve_time = 0.  # 搅拌溶解 计时
        self.stir_dissolve_time_p = 0.
        self.transfer_liquid_info = []
        self.clearn_time = 0.
        self.clearn_desk_info = []  # 记录整理桌面的信息

        self.dropper_water_secs = 0
        self.dropper_water_secs_pre = 0
        self.dropper_water_flag = False
        self.see_display_info = []  # 读示数
        self.see_display_head_info = []  # 读示数（只有头）
        self.see_display_score = []
        self.see_display_time = 0
        self.see_display_time_pre = 0

    # def setCenterBox(self, device, top_img0, front_img0, est=None, esf=None):  # 设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
    #     if est:
    #         self.h_top, self.w_top = top_img0.shape[:2]
    #         self.center_box_ = torch.tensor(
    #             [self.w_top * est[0], self.h_top * est[1], self.w_top * est[2], self.h_top * est[3]],
    #             device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
    #     if esf:
    #         self.h_front, self.w_front = front_img0.shape[:2]
    #         self.center_box_front = torch.tensor(
    #             [self.w_front * esf[0], self.h_front * esf[1], self.w_front * esf[2], self.h_front * esf[3]],
    #             device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
    #     self.set_center_box = True

    # def run_one_result_process(self, frame_top, frame_front, frame_side,
    #                            pred_top, pred_front, pred_side,
    #                            time_top, time_front, time_side,
    #                            num_frame_top,
    #                            num_frame_front,
    #                            num_frame_side,
    #                            path_save,
    #                            names_label):
    #     self.time_top = time_top
    #     self.time_front = time_front
    #     self.num_frame_top = num_frame_top
    #     self.num_frame_front = num_frame_front
    #     self.frame_top = frame_top
    #     self.frame_front = frame_front
    #     self.secs = time_front / 1000
    #
    #     if frame_top is None or frame_front is None:
    #         return
    #
    #     front_true = False
    #     top_true = False
    #     self.preds_top = None
    #     self.preds_front = None
    #     device_use = "cuda :0"
    #     if pred_front != None and pred_front.shape[0]:
    #         front_true = True
    #         device_use = pred_front.device
    #     self.preds_front, self.objects_front = self.assign_labels(frame_front, pred_front, names_label)
    #
    #     if pred_top != None and pred_top.shape[0]:
    #         top_true = True
    #         device_use = pred_top.device
    #     self.preds_top, self.objects_top = self.assign_labels(frame_top, pred_top, names_label)
    #
    #     self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
    #                        top_preds=self.preds_top, front_preds=self.preds_front, side_preds=None)
    def score_process(self, top_true, front_true, side_true):
        if top_true and front_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分
            hands_top, eyes_top, heads_top, scales_top, scale_ons_top, scale_zeros_top, salvers_top, \
            weight_papers_top, bottle_NaCLs_top, NaCL_powders_top, scale_offs_top, scale_notzeros_top, \
            spoons_top, spoon_us_top, stopper_not_ups_top, stopper_ups_top, measuring_cylinders_top, \
            beakers_top, blocks_top, reserved_1_top, water_columns_top, reserved_2_top, \
            reserved_3_top, glass_rods_top, bottle_n_ms_top, reserved_4_top, reserved_5_top, \
            dusters_top, droppers_top, liquids_top, liquid_on_desks_top, clean_desks_top = self.preds_top

            hands_front, eyes_front, heads_front, scales_front, scale_ons_front, scale_zeros_front, salvers_front, \
            weight_papers_front, bottle_NaCLs_front, NaCL_powders_front, scale_offs_front, scale_notzeros_front, \
            spoons_front, spoon_us_front, stopper_not_ups_front, stopper_ups_front, measuring_cylinders_front, \
            beakers_front, blocks_front, reserved_1_front, water_columns_front, reserved_2_front, \
            reserved_3_front, glass_rods_front, bottle_n_ms_front, reserved_4_front, reserved_5_front, \
            dusters_front, droppers_front, liquids_front, liquid_on_desks_front, clean_desks_front = self.preds_front
            # 1.水平放置电子天平，打开电源
            # 双手不在天平上，天平示数不为关
            # self.plot.plot(self.preds_top, self.frame_top)
            # self.plot.plot(self.preds_front, self.frame_front)
            # img = cv2.resize(np.vstack([self.frame_top, self.frame_front]), (0, 0), fx=0.5, fy=0.5)
            # cv2.imshow('1', img)
            # cv2.waitKey(1)
            if not self.scorePoint1:
                if self.open_scale(hands_top, scales_top, hands_front, scales_front, scale_offs_top, scale_ons_top,
                                   scale_zeros_top, scale_notzeros_top):
                    conf_c = 0.1
                    self.assignScore(index=1,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="1.jpg",
                                     preds=self.preds_top
                                     )
                    self.scorePoint1 = True
                    # print('-----1-----')

            # 2.烧杯放置在称量盘上，天平示数清零
            # 烧杯在天平托盘上，天平示数显示0，手不在天平上
            if not self.scorePoint2:
                res = self.scale_set_zero(hands_top, salvers_top, beakers_top, scales_top, hands_front,
                                          salvers_front, beakers_front, scale_zeros_top)
                conf_c = 0.1
                if res == 1:
                    if not self.scorePoint1:
                        self.assignScore(index=1,
                                         img=self.frame_top,
                                         object=self.objects_top,
                                         conf=conf_c,
                                         time_frame=self.time_top,
                                         num_frame=self.num_frame_top,
                                         name_save="1.jpg",
                                         preds=self.preds_top
                                         )
                    self.assignScore(index=2,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="2.jpg",
                                     preds=self.preds_top
                                     )
                    self.scorePoint2 = True
                    # print('-----2-----')
                elif res == 2:
                    self.assignScore(index=2,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="2.jpg",
                                     preds=self.preds_top
                                     )
                    self.scorePoint2 = True
                    # print('-----2-----')

            # 3.用药匙取粉末状固体于烧杯，添加至规定量
            if not self.scorePoint3 and self.scorePoint1:
                info = self.measure_NaCl(3, stopper_not_ups_top, stopper_not_ups_front, NaCL_powders_front,
                                         spoons_front,
                                         beakers_front, spoons_top, salvers_top, hands_front, hands_top)
                if info is not None:
                    index, frame, preds, secs = info
                    conf_c = 0.1
                    self.assignScore(index=index,
                                     img=frame,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=secs * 1000,
                                     num_frame=self.num_frame_top,
                                     name_save="3.jpg",
                                     preds=preds
                                     )
                    self.scorePoint3 = True
                    # print('-----3-----')

            # 量筒中加水
            if not self.scorePoint5:
                self.water_in_cylinder(water_columns_front)

            if not self.dropper_water_flag:  # 胶头滴管滴加
                self.dropper_water(droppers_front, measuring_cylinders_front)

            # 4.向量筒中倾倒蒸馏水，用胶头滴管滴加蒸馏水至规定体积
            if not self.scorePoint4:
                info = self.check_water_V(4, water_columns_front, heads_front, eyes_front)
                if info is not None:
                    index, frame, preds, secs = info
                    conf_c = 0.1
                    self.assignScore(index=index,
                                     img=frame,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=secs * 1000,
                                     num_frame=self.num_frame_top,
                                     name_save="4.jpg",
                                     preds=preds
                                     )
                    self.scorePoint4 = True
                    # print('-----4-----')
            # 5 把量取的蒸馏水全部倒入烧杯中(前视)
            if not self.scorePoint5 and self.add_water:
                info = self.water_to_beaker(5, measuring_cylinders_front, beakers_front, liquids_front)
                if info is not None:
                    index, frame, preds, secs = info
                    conf_c = 0.1
                    self.assignScore(index=index,
                                     img=frame,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=secs * 1000,
                                     num_frame=self.num_frame_top,
                                     name_save="5.jpg",
                                     preds=preds
                                     )
                    self.scorePoint5 = True
                    # print('-----5-----')

            # 6 用玻璃棒搅拌，至固体药品全部溶解(前视)
            if not self.scorePoint6:
                if self.stir_dissolve(glass_rods_front, beakers_front, hands_front):
                    conf_c = 0.1
                    self.assignScore(index=6,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="6.jpg",
                                     preds=self.preds_top
                                     )
                    self.scorePoint6 = True
                    # print('-----6-----')

            # 7 将所得的溶液转移到指定容器中
            if not self.scorePoint7:
                info = self.transfer_liquid(7, stopper_not_ups_top, stopper_not_ups_front, beakers_front,
                                            bottle_n_ms_front, hands_front)
                if info is not None:
                    index, frame, preds, secs = info
                    conf_c = 0.1
                    self.assignScore(index=index,
                                     img=frame,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=secs * 1000,
                                     num_frame=self.num_frame_top,
                                     name_save="7.jpg",
                                     preds=preds
                                     )
                    self.scorePoint7 = True
                    # print('-----7-----')

            top_items = [scales_top, weight_papers_top, bottle_NaCLs_top, spoons_top, stopper_not_ups_top,
                         stopper_ups_top, measuring_cylinders_top, beakers_top, water_columns_top,
                         glass_rods_top, bottle_n_ms_top, dusters_top, droppers_top, liquids_top,
                         liquid_on_desks_top]
            front_items = [scales_front, bottle_NaCLs_front, spoons_front, stopper_not_ups_front,
                           stopper_ups_front, measuring_cylinders_front, beakers_front, water_columns_front,
                           glass_rods_front, bottle_n_ms_front, dusters_front, droppers_front, liquids_front,
                           liquid_on_desks_front]
            # 8 整理桌面
            if not self.scorePoint8 and \
                    scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[0] == 0 \
                    and (self.scorePoint3 or self.scorePoint5 or self.scorePoint6):
                if self.clearn_desk(8, top_items, front_items):
                    conf_c = 0.1
                    self.assignScore(index=8,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="8.jpg",
                                     preds=self.preds_top
                                     )
                    self.scorePoint8 = True
                    # print('-----8-----')
            if self.scorePoint8 and len(self.score_list) != 8:
                if not self.desk_is_clearn(top_items, front_items):
                    self.retracementScore(8)

    # 打开电子天平
    def open_scale(self, hands_top, scales_top, hands_front, scales_front, scale_offs_top, scale_ons_top,
                   scale_zeros_top, scale_notzeros_top):
        if hands_top.shape[0] > 0 and scales_top.shape[0] > 0:
            scale_top_box = scales_top[0][:4]
            if pt_in_polygon(center_point(scale_top_box), self.center_area_top):
                hand_scale_top_flag = True  # 手和天平没有交集？
                hand_scale_front_flag = True  # 手和天平没有交集？
                for hand_top in hands_top:  # 顶视 手与天平是否相交
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, scale_top_box) > 0:
                        hand_scale_top_flag = False
                        break
                if hand_scale_top_flag:
                    if hands_front.shape[0] > 0 and scales_front.shape[0] > 0:
                        scale_front_box = scales_front[0][:4]
                        for hand_front in hands_front:  # 前视 手与天平是否相交
                            hand_front_box = hand_front[:4]
                            if iou(scale_front_box, hand_front_box) > 0:
                                hand_scale_front_flag = False
                                break
                if hand_scale_top_flag or hand_scale_front_flag:
                    if scale_offs_top.shape[0] == 0 and (
                            scale_ons_top.shape[0] + scale_zeros_top.shape[0] +
                            scale_notzeros_top.shape[
                                0] != 0):  # 天平打开
                        self.open_scale_time, self.open_scale_time_pre, flag = self.duration(self.open_scale_time, 1,
                                                                                             self.open_scale_time_pre,
                                                                                             0.5)
                        if flag:
                            return True

    # 天平置零
    def scale_set_zero(self, hands_top, salvers_top, beakers_top, scales_top, hands_front, salvers_front, beakers_front,
                       scale_zeros_top):
        beaker_on_salver = False  # 烧杯在托盘上
        if hands_top.shape[0] > 0 and salvers_top.shape[0] > 0 and beakers_top.shape[0] > 0 and \
                scales_top.shape[0] > 0:  # 显示0.0
            scale_top_box = scales_top[0][:4]
            if pt_in_polygon(center_point(scale_top_box), self.center_area_top):  # 天平在实验区域
                salver_top_box = salvers_top[0][:4]
                for beaker_top in beakers_top:
                    beaker_top_box = beaker_top[:4]
                    if iou(beaker_top_box, salver_top_box) == box_area(beaker_top_box):
                        hand_salver_top_flag = True  # 手和托盘没有交集？
                        hand_salver_front_flag = True  # 手和托盘没有交集？
                        for hand_top in hands_top:
                            hand_top_box = hand_top[:4]
                            if iou(hand_top_box, salver_top_box) > 0:
                                hand_salver_top_flag = False
                                break
                        if hand_salver_top_flag:
                            if hands_front.shape[0] > 0 and salvers_front.shape[0] > 0:
                                salver_front_box = salvers_front[0][:4]
                                for hand_front in hands_front:  # 前视 手与天平是否相交
                                    hand_front_box = hand_front[:4]
                                    if iou(salver_front_box, hand_front_box) > 0:
                                        hand_salver_front_flag = False
                                        break
                        if hand_salver_top_flag or hand_salver_front_flag:  # 手不在托盘上 # 烧杯完全在托盘中
                            beaker_on_salver = True
        if not beaker_on_salver and beakers_front.shape[0] > 0 and salvers_front.shape[0] > 0 and \
                hands_front.shape[0] > 0:  # 前视 托盘 烧杯
            salver_front_box = salvers_front[0][:4]
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                if iou(beaker_front_box, salver_front_box) > 0 and \
                        abs(center_distance_h(beaker_front_box, salver_front_box)) < self.h_front * 0.052:
                    hand_salver_front_flag = True  # 前视手和托盘没有交集？
                    hand_salver_top_flag = True  # 顶视手和托盘没有交集？
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, salver_front_box) > 0:
                            hand_salver_front_flag = False
                            break
                    if not hand_salver_front_flag:  # 前视 手和托盘有交集
                        if hands_top.shape[0] > 0 and salvers_top.shape[0] > 0:
                            salver_top_box = salvers_top[0][:4]
                            for hand_top in hands_top:  # 顶视 手与托盘是否相交
                                hand_top_box = hand_top[:4]
                                if iou(salver_top_box, hand_top_box) > 0:
                                    hand_salver_top_flag = False
                                    break
                    if hand_salver_top_flag or hand_salver_front_flag:  # 手不在托盘上 # 烧杯完全在托盘中
                        beaker_on_salver = True

        if beaker_on_salver:  # 烧杯在托盘中
            if self.beaker_on_salver_time == 0:
                self.beaker_on_salver_time = self.secs
            elif self.secs - self.beaker_on_salver_time > 1:  # 烧杯放上去大于 1  秒
                if scale_zeros_top.shape[0] > 0:
                    self.zero_time, self.zero_time_pre, flag = self.duration(self.zero_time, 1.5, self.zero_time_pre,
                                                                             0.6)
                    if flag:
                        return 1
                if self.scorePoint1 and not self.scorePoint2 and self.secs - self.beaker_on_salver_time > 6:  # 超过 n 秒自动赋分
                    return 2

    # 读示数
    def check_water_V(self, score_index, water_columns_front, heads_front, eyes_front):
        if water_columns_front.shape[0] == 0:
            return
        column_t_front_box = water_columns_front[0][:4]
        flag = self.see_display(score_index, eyes_front, heads_front, column_t_front_box)
        if flag:
            if self.see_display_info:
                self.see_display_score = deepcopy(self.see_display_info)
            elif self.see_display_head_info:
                self.see_display_score = deepcopy(self.see_display_head_info)
        if self.see_display_score and self.secs - self.see_display_score[-1] > 1.5:  # 1.5 秒后赋分
            if self.dropper_water_flag:
                img1 = cv2.imread((self.save_path / 'dropper_water.jpg').as_posix())
                if img1 is not None:
                    x = int(self.see_display_score[4])
                    if x < self.w_front / 4:
                        x1, x2 = 0, int(self.w_front / 2)
                    elif x < (self.w_front / 4) * 3:
                        x1, x2 = int(x - self.w_front / 4), int(x + self.w_front / 4)
                    else:
                        x1, x2 = int(self.w_front / 2), int(self.w_front)
                    self.plot(self.see_display_score[2], self.see_display_score[1])
                    img2 = self.see_display_score[1][:, x1:x2, :]
                    img = np.hstack([img1, img2])
                    self.see_display_score[1] = img
                    self.see_display_score[2] = None
            return self.see_display_score[:4]

    def see_display(self, score_index, eyes_front, heads_front, column_t_front_box):  # 看量筒液面示数
        water_column_center_point_up = (
            (column_t_front_box[0] + column_t_front_box[2]) / 2, column_t_front_box[1])  # 水柱液面中心点
        v_d_thre_b = self.h_front * 0.3  # 判错用
        v_d_thre = self.h_front * 0.14  # 眼睛和液面垂直距离阈值 1080 * 1920 约 150 pixel
        # v_d_thre = self.h_front * 0.2  # 眼睛和液面垂直距离阈值 1080 * 1920 约 150 pixel
        head_front_box = None  # 头box
        dis_head_water = 0
        if heads_front.shape[0] > 0:  # 选距离水柱最近的头
            for head_front in heads_front:
                head_front_box_ = head_front[:4]
                dis_head_water_ = distance_point(center_point(head_front_box_), water_column_center_point_up)
                if dis_head_water == 0 or dis_head_water_ < dis_head_water:
                    head_front_box = head_front_box_
                    dis_head_water = dis_head_water_
        if (head_front_box is not None and
                abs(center_point(head_front_box)[1] - column_t_front_box[1]) < v_d_thre_b):
            if eyes_front.shape[0] > 0:  # 眼睛
                eye_front_boxes = []
                for eye_front in eyes_front:
                    eye_front_box_ = eye_front[:4]
                    if box1_in_box2(eye_front_box_, head_front_box):
                        eye_front_boxes.append(eye_front_box_)
                eye_center_h = 0
                if len(eye_front_boxes) == 1:
                    eye_center_h = center_point(eye_front_boxes[0])[1]  # 眼睛中心高度
                elif len(eye_front_boxes) == 2:
                    eye_center_h = (center_point(eye_front_boxes[0])[1] + center_point(eye_front_boxes[1])[1]) / 2
                if eye_center_h != 0:  # 以眼睛计算
                    dis_eye_water = abs(eye_center_h - column_t_front_box[1])  # 眼睛与液面垂直距离
                    if not self.see_display_info or dis_eye_water < self.see_display_info[-2]:
                        self.see_display_info = [score_index, self.frame_front, self.preds_front,
                                                 self.secs, water_column_center_point_up[0], dis_eye_water, self.secs]
                    else:
                        self.see_display_info[-1] = self.secs

                    if dis_eye_water < v_d_thre:
                        self.see_display_time, self.see_display_time_pre, flag = self.duration(self.see_display_time,
                                                                                               0.5,
                                                                                               self.see_display_time_pre,
                                                                                               0.3)
                        if flag:
                            return True
                else:  # 以头中心算
                    if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                        self.see_display_head_info = [score_index, self.frame_front,
                                                      self.preds_front, self.secs,
                                                      water_column_center_point_up[0], dis_head_water, self.secs]
                    else:
                        self.see_display_head_info[-1] = self.secs
                    if abs(center_point(head_front_box)[1] - column_t_front_box[1]) < v_d_thre:
                        self.see_display_time, self.see_display_time_pre, flag = self.duration(self.see_display_time,
                                                                                               0.5,
                                                                                               self.see_display_time_pre,
                                                                                               0.3)
                        if flag:
                            return True

    # 胶头滴管滴加
    def dropper_water(self, droppers_front, cylinders_front):
        if (droppers_front.shape[0] > 0 and cylinders_front.shape[0] > 0):
            dropper_front_box = droppers_front[0][:4]
            cylinder_front_box = cylinders_front[0][:4]
            dropper_cylinder_d_h = abs(center_distance_h(dropper_front_box, cylinder_front_box))  # 滴管 量筒中心水平距离
            dropper_cylinder_d_h_thre = self.h_front * 0.05  # 1080 * 0.05 54 pixel 滴管 量筒 水平方向阈值
            dropper_cylinder_d_v_thre = -self.h_front * 0.045  # 1080 * 0.045 48 pixel 滴管 量筒 垂直方向阈值
            # dropper_cylinder_d_h_thre = self.h_front * 0.1  # 1080 * 0.05 54 pixel 滴管 量筒 水平方向阈值
            # dropper_cylinder_d_v_thre = -self.h_front * 0.1  # 1080 * 0.045 48 pixel 滴管 量筒 垂直方向阈值
            if (
                    dropper_cylinder_d_h < dropper_cylinder_d_h_thre
                    and cylinder_front_box[1] - dropper_front_box[3] > dropper_cylinder_d_v_thre
            ):
                self.dropper_water_secs, self.dropper_water_secs_pre, flag = self.duration(self.dropper_water_secs,
                                                                                           1,
                                                                                           self.dropper_water_secs_pre,
                                                                                           0.3)
                if flag:
                    x = int(center_point(cylinder_front_box)[0])
                    if x < self.w_front / 4:
                        x1, x2 = 0, int(self.w_front / 2)
                    elif x < (self.w_front / 4) * 3:
                        x1, x2 = int(x - self.w_front / 4), int(x + self.w_front / 4)
                    else:
                        x1, x2 = int(self.w_front / 2), int(self.w_front)
                    img = self.frame_front
                    self.plot(self.preds_front, img)
                    cv2.imwrite((self.save_path / 'dropper_water.jpg').as_posix(), img[:, x1:x2, :])  # save img
                    self.dropper_water_flag = True

    # 量取 NaCl
    def measure_NaCl(self, index, stopper_not_ups_top, stopper_not_ups_front, NaCL_powders_front, spoons_front,
                     beakers_front,
                     spoons_top, salvers_top, hands_front, hands_top):
        if stopper_not_ups_top.shape[0] == 0:  # 前视无瓶塞朝下
            if stopper_not_ups_front.shape[0] == 0:  # 顶视无瓶塞朝下
                if NaCL_powders_front.shape[0] > 0 and \
                        spoons_front.shape[0] > 0 and \
                        beakers_front.shape[0] > 0:
                    NaCL_powder_front_box = NaCL_powders_front[0][:4]
                    spoon_front_box = spoons_front[0][:4]
                    beaker_front_box = beakers_front[0][:4]
                    if iou(NaCL_powder_front_box, beaker_front_box) > 0 and \
                            center_distance_v(NaCL_powder_front_box, beaker_front_box) > 0:  # 烧杯底有 食盐颗粒
                        if iou(beaker_front_box, spoon_front_box) > 0:  # 前视药匙和烧杯有交集
                            if spoons_top.shape[0] > 0 and salvers_top.shape[0] > 0:
                                spoon_top_box = spoons_top[0][:4]
                                salver_top_box = salvers_top[0][:4]
                                if iou(salver_top_box, spoon_top_box) > 0:  # 顶视托盘和药匙有交集
                                    self.weight_info = [index, self.frame_front, self.preds_front, self.secs]
                if self.weight_info and self.secs - self.weight_info[-1] > 1:  # 前视
                    if spoons_front.shape[0] == 0:
                        return self.weight_info[:4]
                    elif spoons_front.shape[0] > 0 and hands_front.shape[0] > 0:
                        spoon_front_box = spoons_front[0][:4]
                        hands_spoon_front = False  # 手和药匙有交集
                        for hand_front in hands_front:
                            hand_front_box = hand_front[:4]
                            if iou(hand_front_box, spoon_front_box) > 0:
                                hands_spoon_front = True
                                break
                        if not hands_spoon_front:
                            return self.weight_info[:4]
                    if not self.scorePoint3 and spoons_top.shape[0] == 0:  # 顶视
                        return self.weight_info[:4]
                    elif not self.scorePoint3 and hands_top.shape != 0 and spoons_top.shape[0] > 0:
                        spoon_top_box = spoons_top[0][:4]
                        hands_spoon_top = False  # 手和药匙有交集?
                        for hand_top in hands_top:
                            hand_top_box = hand_top[:4]
                            if iou(hand_top_box, spoon_top_box) > 0:
                                hands_spoon_top = False
                                break
                        if hands_spoon_top:
                            return self.weight_info[:4]

    # 向量筒中倒水
    def water_in_cylinder(self, water_columns_front):
        if water_columns_front.shape[0] > 0:
            water_column_front_box = water_columns_front[0][:4]
            if pt_in_polygon(center_point(water_column_front_box), self.center_area_front):
                self.water_column_time, self.water_column_time_pre, flag = self.duration(self.water_column_time, 3,
                                                                                         self.water_column_time_pre,
                                                                                         1)
                if flag:
                    self.add_water = True

    # 把量取的蒸馏水全部倒入烧杯中
    def water_to_beaker(self, index, measuring_cylinders_front, beakers_front, liquids_front):
        if measuring_cylinders_front.shape[0] > 0 and beakers_front.shape[0] > 0:
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            # beaker_front_box = beakers_front[0][:4]
            w_h_r = w_h_ratio(measuring_cylinder_front_box)
            if liquids_front.shape[0] > 0:
                liquid_front_box = liquids_front[0][:4]
                for beaker_front in beakers_front:
                    beaker_front_box = beaker_front[:4]
                    if iou(liquid_front_box, beaker_front_box) > 0 and \
                            center_distance_v(liquid_front_box, beaker_front_box) > 0:  # 烧杯中有液体
                        if w_h_ratio(measuring_cylinder_front_box) > 1.0 and \
                                min_dis_boxes(measuring_cylinder_front_box,
                                              beaker_front_box) < self.h_front * 0.028:  # 量筒横放与烧杯有交点
                            if not self.water_to_beaker_info or w_h_r > self.water_to_beaker_info[-2]:
                                self.water_to_beaker_info = [index, self.frame_front, self.preds_front, self.secs, w_h_r,
                                                             self.secs]
                            else:
                                self.water_to_beaker_info[-1] = self.secs
                            return
            elif self.scorePoint4 or self.add_water:
                if measuring_cylinders_front.shape[0] > 0 and beakers_front.shape[0] > 0:
                    measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                    w_h_r = w_h_ratio(measuring_cylinder_front_box)
                    for beaker_front in beakers_front:
                        beaker_front_box = beaker_front[:4]
                        if w_h_r > 1.5 and min_dis_boxes(measuring_cylinder_front_box,
                                                         beaker_front_box) < self.h_front * 0.028:  # 量筒横放与烧杯有交点
                            if not self.water_to_beaker_info:
                                self.water_to_beaker_info = [index, self.frame_front, self.preds_front, self.secs, w_h_r,
                                                             self.secs]
                            else:
                                self.water_to_beaker_info[-1] = self.secs
                            return
        if self.water_to_beaker_info and self.secs - self.water_to_beaker_info[-1] > 0.5:
            return self.water_to_beaker_info[:4]

    # 玻璃棒搅拌至固体全部溶解
    def stir_dissolve(self, glass_rods_front, beakers_front, hands_front):
        if glass_rods_front.shape[0] > 0 and beakers_front.shape[0] > 0 and hands_front.shape[0] > 0:
            glass_rod_front_box = glass_rods_front[0][:4]
            hand_glass_rod = False
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if iou(hand_front_box, glass_rod_front_box) > 0:
                    hand_glass_rod = True
                    break
            if hand_glass_rod:
                for beaker_front in beakers_front:
                    beaker_front_box = beaker_front[:4]
                    if iou(glass_rod_front_box, beaker_front_box) > 0 and \
                            center_distance_v(beaker_front_box, glass_rod_front_box) > 0:
                        self.stir_dissolve_time, self.stir_dissolve_time_p, flag = self.duration(self.stir_dissolve_time,
                                                                                                 20,
                                                                                                 self.stir_dissolve_time_p,
                                                                                                 5)
                        if flag:
                            return True

    # 将所得的溶液转移到指定容器中
    def transfer_liquid(self, index, stopper_not_ups_top, stopper_not_ups_front, beakers_front, bottle_n_ms_front, hands_front):
        if (stopper_not_ups_top.shape[0] == 0  # 前视无瓶塞朝下
                and stopper_not_ups_front.shape[0] == 0  # 顶视无瓶塞朝下
                and beakers_front.shape[0] > 0  # 前视有烧杯
                and bottle_n_ms_front.shape[0] > 0  # 前视有细口瓶
                and hands_front.shape[0] > 0):
            hand_beaker = False  # 手拿烧杯
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                for bottle_n_m_front in bottle_n_ms_front:
                    bottle_n_m_front_box = bottle_n_m_front[:4]
                    d_v = center_distance_v(bottle_n_m_front_box, beaker_front_box) > 0  # 烧杯高于细口瓶
                    if (iou(bottle_n_m_front_box, beaker_front_box) > 0
                            and d_v > 0
                            and w_h_ratio(beaker_front_box) > 1.1):  # 烧杯细口瓶相交
                        for hand_front in hands_front:
                            hand_front_box = hand_front[:4]
                            if iou(hand_front_box, beaker_front_box) > 0:
                                hand_beaker = True
                                break
                        if hand_beaker and (not self.transfer_liquid_info or d_v > self.transfer_liquid_info[-2]):
                            self.transfer_liquid_info = [index, self.frame_front, self.preds_front, self.secs, d_v,
                                                         self.secs]
                        else:
                            self.transfer_liquid_info[-1] = self.secs
                        return
                if hand_beaker:
                    break
        if self.transfer_liquid_info and self.secs - self.transfer_liquid_info[-1] > 0.5:
            return self.transfer_liquid_info[:4]

    # 清理桌面
    def clearn_desk(self, index, top_items, front_items):
        if self.desk_is_clearn(top_items, front_items):
            self.clearn_desk_info = [index, self.frame_top, self.preds_top, self.secs]
            self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
            if flag:
                self.clearn_time = 0
                return True
                # self.assignScore(8, self.frame_top, self.preds_top)
        else:
            self.clearn_time = 0

    def duration(self, first_time, duration_time, pre_time=None, reclock=None):
        if reclock:
            if self.secs - pre_time > reclock:  # n 秒内没有此动作 重新计时
                first_time = pre_time = 0.
            else:
                pre_time = self.secs
        if first_time == 0:
            if reclock:
                first_time = pre_time = self.secs
            else:
                first_time = self.secs
            return first_time, pre_time, False
        elif self.secs - first_time > duration_time:
            return first_time, pre_time, True
        else:
            return first_time, pre_time, False

    def desk_is_clearn(self, top_items, front_items):
        for items in top_items:
            if items.shape[0] == 0:
                continue
            else:
                for item in items:
                    item_box = item[:4]
                    if pt_in_polygon(center_point(item_box), self.center_area_top) > 0:
                        return False
        for items in front_items:
            if items.shape[0] == 0:
                continue
            else:
                for item in items:
                    item_box = item[:4]
                    if pt_in_polygon(center_point(item_box), self.center_area_front) > 0:
                        return False
        return True

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:
            # self.assignScore(*self.clearn_desk_info)
            return True
