#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 14:34
# @Author  : Qiguangnan
# @File    : phy_measureDensity.py


from .comm import *
from .comm.course_base import ConfigModel

# from config.phy_measure_density_scale_conf import PCLWKMD01
import traceback
from logger import logger
from configg.global_config import experimental_site_top as est
from configg.global_config import experimental_site_front as esf


class PHY_measure_density_scale(ConfigModel):

    def __init__(self):
        super(PHY_measure_density_scale, self).__init__()

        self.scale_on_time = 0.
        self.open_scale_time = 0.  # 打开天平的时间
        self.scale_zero_time = 0.
        self.weight_time = 0.
        self.weight_time_pre = 0.
        self.weight_info = []
        self.water_column_time = 0.  # 添加水
        self.water_column_time_pre = 0.
        self.add_water_beaker_info = []  # 用烧杯向量筒加水信息
        self.add_water_info = []
        self.see_display_time = 0.
        self.see_display_time_pre = 0.
        self.see_display_info = []  # 读示数
        self.see_display_block_time = 0.
        self.see_display_block_time_pre = 0.
        self.see_display_block_info = []  # 读示数（有物块）
        self.block_in_water_time = 0.
        self.block_in_water_time_pre = 0.
        self.clearn_time = 0.
        self.clearn_desk_info = []  # 整理桌面信息

        self.h_top = 0  # 顶视 高
        self.w_top = 0  # 顶视 宽
        self.h_front = 0  # 前视 高
        self.w_front = 0  # 前视 宽
        self.score_list = []  # 已经得到的得分点

    def setCenterBox(self, device, top_img0, front_img0, est=None, esf=None):
        '''
        设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
        :param device:
        :param top_img0:
        :param front_img0:
        :param est:
        :param esf:
        :return:
        '''

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
        # print("top result:: {}".format(pred_top))
        # print("front result:: {}".format(pred_front))
        # time_process_start = time.time()

        front_true = False
        top_true = False
        top1_preds = None
        front1_preds = None
        if pred_front != None and pred_front.shape[0]:
            front1_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            front_true = True
        if pred_top != None and pred_top.shape[0]:
            top1_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
            top_true = True

        self.rtmp_push_fun(top_img=frame_top,front_img=frame_front,side_img=frame_side,
                           top_preds=top1_preds,front_preds=front1_preds,side_preds=None)

        if top_true:
            hands_top, eyes_top, heads_top, scales_top, scale_ons_top, scale_zeros_top, salvers_top, \
            weight_papers_top, bottle_NaCLs_top, NaCL_powders_top, scale_offs_top, scale_notzeros_top, \
            spoons_top, spoon_us_top, stopper_not_ups_top, stopper_ups_top, measuring_cylinders_top, beakers_top, \
            blocks_top, add_water_cylinders_top, water_columns_top, measuring_waters_top, \
            measuring_water_falses_top, glass_rods_top, bottle_n_ms_top, stir_dissolves_top, dump_liquids_top, \
            dusters_top, droppers_top, liquids_top, liquid_on_desks_top, clean_desks_top = top1_preds

            if not self.set_center_box:
                self.setCenterBox(pred_top.device, frame_top, frame_front, est, esf)  # 设置中心区域

        if front_true:
            hands_front, eyes_front, heads_front, scales_front, scale_ons_front, scale_zeros_front, salvers_front, \
            weight_papers_front, bottle_NaCLs_front, NaCL_powders_front, scale_offs_front, scale_notzeros_front, \
            spoons_front, spoon_us_front, stopper_not_ups_front, stopper_ups_front, measuring_cylinders_front, \
            beakers_front, blocks_front, add_water_cylinders_front, water_columns_front, \
            measuring_waters_front, measuring_water_falses_front, glass_rods_front, bottle_n_ms_front, \
            stir_dissolves_front, dump_liquids_front, dusters_front, droppers_front, liquids_front, \
            liquid_on_desks_front, clean_desks_front = front1_preds

            if not self.set_center_box:
                self.setCenterBox(pred_front.device, frame_top, frame_front, est, esf)  # 设置中心区域

        if top_true or front_true:
            try:
                # 1.打开电子天平
                if not self.scorePoint1:
                    self.open_scale(scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_notzeros_top,
                                    frame_top, objects_top, time_top, num_frame_top, top1_preds)

                # 2.检查电子天平初始示数，若不为0进行清零操作
                if self.scorePoint1 and not self.scorePoint2:
                    self.set_zeron(scale_zeros_top, scales_top,
                                   frame_top, objects_top, time_top, num_frame_top, top1_preds)

                # 3.将系有细线的金属块置于电子天平中央，记录电子天平的示数
                if not self.scorePoint3:
                    self.weight_block(blocks_top, blocks_front, salvers_top, salvers_front, hands_top, hands_front,
                                      frame_top, objects_top, time_top, num_frame_top, top1_preds,
                                      frame_front, objects_front, time_front, num_frame_front, front1_preds
                                      )

                # 4.在量筒中倒入适量的水
                # 量筒中有水， 前视
                if not self.scorePoint4:
                    self.add_water(water_columns_front, beakers_front, measuring_cylinders_front,
                                   frame_top, objects_top, time_top, num_frame_top, top1_preds,
                                   frame_front, objects_front, time_front, num_frame_front, front1_preds
                                   )

                # 5 观察并记录量筒中水面对应的示数
                if not self.scorePoint5:
                    self.record_V_display(measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                          blocks_front, frame_top, objects_top, time_top, num_frame_top, top1_preds,
                                          frame_front, objects_front, time_front, num_frame_front, front1_preds)

                # 6 将系有细线的金属块放入量筒并㓎没在水中
                # 前视
                if not self.scorePoint6:
                    self.block_in_water(measuring_cylinders_front, measuring_cylinders_top, water_columns_front,
                                        blocks_front, blocks_top, frame_top, objects_top, time_top,
                                        num_frame_top, top1_preds,
                                        frame_front, objects_front, time_front, num_frame_front, front1_preds)

                # 7 观察并记录量筒中水面对应的示数
                if not self.scorePoint7 and self.scorePoint6:
                    self.record_V_display(measuring_cylinders_front, water_columns_front, heads_front, eyes_front,
                                          blocks_front, frame_top, objects_top, time_top, num_frame_top, top1_preds,
                                          frame_front, objects_front, time_front, num_frame_front, front1_preds)

                # # 9 把量取的水倒入烧杯中
                # # 前视
                # if not self.scorePoint9:
                #     if hands_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0 and beakers_front.shape[
                #         0] > 0:
                #         beaker_front_box = beakers_front[0][:4]
                #         measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                #         if w_h_ratio(measuring_cylinder_front_box) > 1.0 and iou(measuring_cylinder_front_box,
                #                                                                  beaker_front_box) > 0:  # 量筒横放与烧杯有交点
                #             self.scorePoint9 = True

                # 8 清洗仪器，整理桌面
                top_items = [scales_top, measuring_cylinders_top, beakers_top, blocks_top, dusters_top]
                front_items = [scales_front, measuring_cylinders_front, beakers_front, blocks_front, dusters_front]
                if not self.scorePoint8 and \
                        scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[0] == 0 \
                        and (self.scorePoint3 or self.scorePoint5 or self.scorePoint6):
                    self.clearn_desk(top_items, front_items, frame_top, objects_top, time_top, num_frame_top,
                                     top1_preds,
                                     frame_front, objects_front, time_front, num_frame_front, front1_preds)
                if self.scorePoint8 and len(self.score_list) != 8:
                    if not self.desk_is_clearn(top_items, front_items):
                        self.retracementScore(8)
            except:
                logger.error(traceback.format_exc())

    # 打开天平
    def open_scale(self, scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_notzeros_top,
                   frame_top, objects_top, time_top, num_frame_top, pred_top):
        if scales_top.shape[0] > 0:
            scale_top_box = scales_top[0][:4]
            if pt_in_box(center_point(scale_top_box), self.center_box_top):
                if scale_offs_top.shape[0] == 0 and (
                        scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_notzeros_top.shape[
                    0] != 0):  # 天平打开
                    display_in_scale = False
                    if scale_ons_top.shape[0] > 0:
                        scale_on_box = scale_ons_top[0][:4]
                        if box1_in_box2(scale_on_box, scale_top_box):
                            display_in_scale = True
                    if not display_in_scale and scale_zeros_top.shape[0] > 0:
                        scale_zero_box = scale_zeros_top[0][:4]
                        if box1_in_box2(scale_zero_box, scale_top_box):
                            display_in_scale = True
                    if not display_in_scale and scale_notzeros_top.shape[0] > 0:
                        scale_notzero_box = scale_notzeros_top[0][:4]
                        if box1_in_box2(scale_notzero_box, scale_top_box):
                            display_in_scale = True
                    if display_in_scale:
                        self.scale_on_time, _, flag = self.duration(self.scale_on_time, 0.3)
                        if flag:
                            self.open_scale_time = time.time()
                            # self.assignScore(1, self.top_img0, self.top_preds)
                            self.scorePoint1 = True
                            conf_c = 0.1
                            self.assignScore(index=1,
                                             img=frame_top,
                                             object=objects_top,
                                             conf=conf_c,
                                             time_frame=time_top,
                                             num_frame=num_frame_top,
                                             name_save="1.jpg",
                                             preds=pred_top
                                             )
                            # frame_top,objects_top,time_top,num_frame_top,pred_top

    # 天平置零
    def set_zeron(self, scale_zeros_top, scales_top,
                  frame_top, objects_top, time_top, num_frame_top, pred_top):
        if scale_zeros_top.shape[0] > 0 and scales_top.shape[0] > 0:  # 显示0.0
            scale_top_box = scales_top[0][:4]
            scale_zero_top_box = scale_zeros_top[0][:4]
            if box1_in_box2(scale_zero_top_box, scale_top_box):
                if time.time() - self.open_scale_time > 0.5:
                    self.scale_zero_time, _, flag = self.duration(self.scale_zero_time, 0.3)
                    if flag:
                        # self.assignScore(2, self.top_img0, self.top_preds)
                        self.scorePoint2 = True
                        conf_c = 0.1
                        self.assignScore(index=2,
                                         img=frame_top,
                                         object=objects_top,
                                         conf=conf_c,
                                         time_frame=time_top,
                                         num_frame=num_frame_top,
                                         name_save="2.jpg",
                                         preds=pred_top
                                         )

        if not self.scorePoint2 and time.time() - self.open_scale_time > 4:  # 8 秒后自动赋分
            # self.assignScore(2, self.top_img0, self.top_preds)
            self.scorePoint2 = True
            conf_c = 0.1
            self.assignScore(index=2,
                             img=frame_top,
                             object=objects_top,
                             conf=conf_c,
                             time_frame=time_top,
                             num_frame=num_frame_top,
                             name_save="2.jpg",
                             preds=pred_top
                             )

    # 称量物块
    def weight_block(self, blocks_top, blocks_front, salvers_top, salvers_front, hands_top, hands_front,
                     frame_top, objects_top, time_top, num_frame_top, pred_top,
                     frame_front, objects_front, time_front, num_frame_front, pred_front):
        if blocks_front.shape[0] > 0 and salvers_front.shape[0] > 0:  # 前视 物块 托盘 手
            block_front_box = blocks_front[0][:4]
            salver_front_box = salvers_front[0][:4]
            if iou(block_front_box, salver_front_box) > 0 and \
                    abs(center_distance_h(block_front_box, salver_front_box)) < self.h_front * 0.052:  # 水平方向中心距离
                hand_salver = False  # 手和托盘是否有交集
                if hands_top.shape[0] > 0 and salvers_top.shape[0] > 0:
                    salver_top_box = salvers_top[0][:4]
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if iou(hand_top_box, salver_top_box) > 0:
                            hand_salver = True
                            break
                if hand_salver and hands_front.shape[0] > 0:  # 顶视手和托盘有交集 判断前视
                    hand_front_salver = False  # 前视手和托盘是否交集
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, salver_front_box) > 0:
                            hand_front_salver = True
                            break
                    if not hand_front_salver:  # 前视没有交集
                        hand_salver = False
                if not hand_salver:  # 手和托盘没有交集
                    self.weight_time, self.weight_time_pre, flag = self.duration(self.weight_time, 1,
                                                                                 self.weight_time_pre, 0.5)
                    if flag:
                        # self.weight_info = [3, self.top_img0, self.top_preds, time.time()]
                        self.weight_info = [3, frame_top, objects_top, time_top, num_frame_top, pred_top, time.time()]

        elif blocks_top.shape[0] > 0 and salvers_top.shape[0] > 0:  # 顶视
            block_top_box = blocks_top[0][:4]
            salver_top_box = salvers_top[0][:4]
            if iou(block_top_box, salver_top_box) == box_area(block_top_box):  # 物块在托盘中
                hand_salver = False  # 手和托盘是否有交集
                if hands_top.shape[0] > 0:
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if iou(hand_top_box, salver_top_box) > 0:
                            hand_salver = True
                            break
                if hand_salver and hands_front.shape[0] > 0 and salvers_front.shape[0] > 0:  # 顶视有交集 判断前视
                    hand_front_salver = False  # 前视手和托盘是否交集
                    salver_front_box = salvers_front[0][:4]
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, salver_front_box) > 0:
                            hand_front_salver = True
                            break
                    if not hand_front_salver:  # 前视没有交集
                        hand_salver = False
                if not hand_salver:  # 手和托盘没有交集
                    self.weight_time, self.weight_time_pre, flag = self.duration(self.weight_time, 1,
                                                                                 self.weight_time_pre, 0.5)
                    if flag:
                        self.weight_info = [3, frame_top, objects_top, time_top, num_frame_top, pred_top, time.time()]

        if self.weight_info and not self.scorePoint3 and time.time() - self.weight_info[-1] > 1:  # 停止称量1秒
            # self.assignScore(*self.weight_info[:4])
            self.scorePoint3 = True
            conf_c = 0.1
            self.assignScore(index=3,
                             img=self.weight_info[1],
                             object=self.weight_info[2],
                             conf=conf_c,
                             time_frame=self.weight_info[3],
                             num_frame=self.weight_info[4],
                             name_save="3.jpg",
                             preds=self.weight_info[5]
                             )

    # 加入水
    def add_water(self, water_columns_front, beakers_front, measuring_cylinders_front,
                  frame_top, objects_top, time_top, num_frame_top, pred_top,
                  frame_front, objects_front, time_front, num_frame_front, pred_front
                  ):
        if water_columns_front.shape[0] > 0 and water_columns_front[0][3] - water_columns_front[0][
            1] > self.h_front * 0.06:
            water_column_front_box = water_columns_front[0][:4]
            if pt_in_box(center_point(water_column_front_box), self.center_box_front):
                if beakers_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0:
                    beaker_front_box = beakers_front[0][:4]
                    measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
                    if min(beaker_front_box[1], beaker_front_box[3]) < measuring_cylinder_front_box[1] and \
                            iou(beaker_front_box, measuring_cylinder_front_box) > 0:  # 烧杯中心在量筒上方 烧杯与量筒有交集
                        # self.water_column_time, self.water_column_time_pre, flag = self.duration(self.water_column_time,
                        #                                                                          1,
                        #                                                                          self.water_column_time_pre,
                        #                                                                          0.5)
                        # if flag:
                        self.record_add_water_info(water_column_front_box,
                                                   frame_front, objects_front, time_front, num_frame_front,
                                                   pred_front, True)
                else:
                    self.water_column_time, self.water_column_time_pre, flag = self.duration(self.water_column_time, 1,
                                                                                             self.water_column_time_pre,
                                                                                             0.2)
                    if flag:
                        self.record_add_water_info(water_column_front_box,
                                                   frame_front, objects_front, time_front, num_frame_front, pred_front)

            if self.add_water_beaker_info:
                # if time.time() - self.add_water_beaker_info[-1] > 0.5:
                if num_frame_front - self.add_water_beaker_info[4] > 10:
                    # self.assignScore(*self.add_water_beaker_info[:4])
                    self.scorePoint4 = True
                    conf_c = 0.1
                    self.assignScore(index=4,
                                     img=self.add_water_beaker_info[1],
                                     object=self.add_water_beaker_info[2],
                                     conf=conf_c,
                                     time_frame=self.add_water_beaker_info[3],
                                     num_frame=self.add_water_beaker_info[4],
                                     name_save="4.jpg",
                                     preds=self.add_water_beaker_info[5]
                                     )

            elif self.add_water_info:
                # if time.time() - self.add_water_info[-1] > 0.5:
                if num_frame_front - self.add_water_info[4] > 10:
                    # self.assignScore(*self.add_water_info[:4])
                    self.scorePoint4 = True
                    conf_c = 0.1
                    self.assignScore(index=4,
                                     img=self.add_water_info[1],
                                     object=self.add_water_info[2],
                                     conf=conf_c,
                                     time_frame=self.add_water_info[3],
                                     num_frame=self.add_water_info[4],
                                     name_save="4.jpg",
                                     preds=self.add_water_info[5]
                                     )

    # 记录示数
    def record_V_display(self, measuring_cylinders_front, water_columns_front, heads_front, eyes_front, blocks_front,
                         frame_top, objects_top, time_top, num_frame_top, pred_top,
                         frame_front, objects_front, time_front, num_frame_front, pred_front
                         ):
        block_in_water = False
        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0 and \
                heads_front.shape[0] > 0 and eyes_front.shape[0] > 0:
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            water_column_front_box = water_columns_front[0][:4]
            if blocks_front.shape[0] > 0:
                block_front_box = blocks_front[0][:4]  # 物块
                if iou(water_column_front_box, block_front_box) == box_area(block_front_box) and \
                        block_front_box[1] - water_column_front_box[1] > self.h_front * 0.028:  # 物块在水里
                    block_in_water = True
            if not block_in_water:  # 物块不在水中
                self.see_display(heads_front, eyes_front, water_column_front_box, measuring_cylinder_front_box,
                                 frame_top, objects_top, time_top, num_frame_top, pred_top,
                                 frame_front, objects_front, time_front, num_frame_front, pred_front
                                 )
            else:
                self.see_display(heads_front, eyes_front, water_column_front_box, measuring_cylinder_front_box,
                                 frame_top, objects_top, time_top, num_frame_top, pred_top,
                                 frame_front, objects_front, time_front, num_frame_front, pred_front, True)

            if self.see_display_info and num_frame_front - self.see_display_info[4] > 6:
                # self.assignScore(*self.see_display_info[:4])
                self.scorePoint5 = True
                conf_c = 0.1
                self.assignScore(index=5,
                                 img=self.see_display_info[1],
                                 object=self.see_display_info[2],
                                 conf=conf_c,
                                 time_frame=self.see_display_info[3],
                                 num_frame=self.see_display_info[4],
                                 name_save="5.jpg",
                                 preds=self.see_display_info[5]
                                 )
            if self.see_display_block_info and num_frame_front - self.see_display_block_info[4] > 6:
                # self.assignScore(*self.see_display_block_info[:4])
                self.scorePoint7 = True
                conf_c = 0.1
                self.assignScore(index=7,
                                 img=self.see_display_block_info[1],
                                 object=self.see_display_block_info[2],
                                 conf=conf_c,
                                 time_frame=self.see_display_block_info[3],
                                 num_frame=self.see_display_block_info[4],
                                 name_save="7.jpg",
                                 preds=self.see_display_block_info[5]
                                 )

    def see_display(self, heads_front, eyes_front, water_column_front_box, measuring_cylinder_front_box,
                    frame_top, objects_top, time_top, num_frame_top, pred_top,
                    frame_front, objects_front, time_front, num_frame_front, pred_front,
                    block=False
                    ):  # 看示数
        head_front_box = None
        head_measuring_cylinder_distance = 0
        for head_front in heads_front:
            head_front_box_ = head_front[:4]
            h_m_d = distance_box(head_front_box_, water_column_front_box)
            if head_measuring_cylinder_distance == 0:
                head_measuring_cylinder_distance = h_m_d
                head_front_box = head_front_box_
            if h_m_d < head_measuring_cylinder_distance:
                head_front_box = head_front_box_
        if head_front_box is not None and center_point(head_front_box)[1] > measuring_cylinder_front_box[1]:  # 头中心比量筒底
            eyes_front_box = []
            for eye_front in eyes_front:
                if box1_in_box2(eye_front[:4], head_front_box):
                    eyes_front_box.append(eye_front[:4])
            eye_center_h = None
            if len(eyes_front_box) == 0:
                pass
            elif len(eyes_front_box) == 1:
                eye_center_h = center_point(eyes_front_box[0])[1]
            else:
                eye_center_h = (center_point(eyes_front_box[0])[1] + center_point(eyes_front_box[1])[1]) / 2
            if eye_center_h is not None:
                dis_eye_water = abs(eye_center_h - water_column_front_box[1])
                if dis_eye_water < self.h_front * 0.135:
                    if not block:
                        self.see_display_time, self.see_display_time_pre, flag = self.duration(self.see_display_time,
                                                                                               0.5,
                                                                                               self.see_display_time_pre,
                                                                                               0.4)
                        if flag:
                            if not self.see_display_info or dis_eye_water < self.see_display_info[-1]:
                                self.see_display_info = [5, frame_front, objects_front, time_front, num_frame_front,
                                                         pred_front, dis_eye_water]
                            else:
                                self.see_display_info[4] = num_frame_front  # time.time()
                    else:
                        self.see_display_block_time, self.see_display_block_time_pre, flag = self.duration(
                            self.see_display_block_time, 0.2, self.see_display_block_time_pre, 0.4)
                        if flag:
                            if not self.see_display_block_info or dis_eye_water < self.see_display_block_info[-2]:
                                # self.see_display_block_info = [7, self.front_img0, self.front_preds, time.time(),
                                #                                dis_eye_water, time.time()]
                                self.see_display_block_info = [7, frame_front, objects_front, time_front,
                                                               num_frame_front,
                                                               pred_front, dis_eye_water, time.time()]
                            else:
                                self.see_display_block_info[4] = num_frame_front  # time.time()

    # 物块放在水中
    def block_in_water(self, measuring_cylinders_front, measuring_cylinders_top, water_columns_front, blocks_front,
                       blocks_top, frame_top, objects_top, time_top, num_frame_top, pred_top,
                       frame_front, objects_front, time_front, num_frame_front, pred_front):
        if blocks_top.shape[0] > 0:  # 顶部 物块不在水里直接返回
            block_cylinder = False
            block_top_box = blocks_top[0][:4]
            if measuring_cylinders_top.shape[0] > 0:
                measuring_cylinder_top = measuring_cylinders_top[0][:4]
                if iou(block_top_box, measuring_cylinder_top) > 0:
                    block_cylinder = True
            if not block_cylinder:
                return

        if measuring_cylinders_front.shape[0] > 0 and water_columns_front.shape[0] > 0 and blocks_front.shape[
            0] > 0:  # 量筒 水柱 物块
            water_column_front_box = water_columns_front[0][:4]  # 水柱
            block_front_box = blocks_front[0][:4]  # 物块
            if pt_in_box(center_point(water_column_front_box), self.center_box_front):  # 限制范围
                if iou(water_column_front_box, block_front_box) == box_area(block_front_box) and \
                        block_front_box[1] - water_column_front_box[1] > self.h_front * 0.028:  # 物块在水里
                    self.block_in_water_time, self.block_in_water_time_pre, flag = self.duration(
                        self.block_in_water_time, 1, self.block_in_water_time_pre, 0.5)
                    if flag:
                        # self.assignScore(6, self.front_img0, self.front_preds)
                        self.scorePoint6 = True
                        conf_c = 0.1
                        self.assignScore(index=6,
                                         img=frame_front,
                                         object=objects_front,
                                         conf=conf_c,
                                         time_frame=time_front,
                                         num_frame=num_frame_front,
                                         name_save="6.jpg",
                                         preds=pred_front
                                         )

    # 清理桌面
    def clearn_desk(self, top_items, front_items,
                    frame_top, objects_top, time_top, num_frame_top, pred_top,
                    frame_front, objects_front, time_front, num_frame_front, pred_front
                    ):
        if self.desk_is_clearn(top_items, front_items):
            # self.clearn_desk_info = [8, self.top_img0, self.top_preds, time.time()]
            self.clearn_desk_info = [8, frame_top, objects_top, time_top, num_frame_top, pred_top]
            self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
            if flag:
                # self.assignScore(8, self.top_img0, self.top_preds)
                self.scorePoint8 = True
                conf_c = 0.1
                self.assignScore(index=8,
                                 img=frame_top,
                                 object=objects_top,
                                 conf=conf_c,
                                 time_frame=time_top,
                                 num_frame=num_frame_top,
                                 name_save="8.jpg",
                                 preds=pred_top
                                 )
                self.clearn_time = 0
        else:
            self.clearn_time = 0

    def duration(self, first_time, duration_time, pre_time=None, reclock=None):
        if reclock:
            if time.time() - pre_time > reclock:  # n 秒内没有此动作 重新计时
                first_time = pre_time = 0.
            else:
                pre_time = time.time()
        if first_time == 0:
            if reclock:
                first_time = pre_time = time.time()
            else:
                first_time = time.time()
            return first_time, pre_time, False
        elif time.time() - first_time > duration_time:
            return first_time, pre_time, True
        else:
            return first_time, pre_time, False

    # 记录向量筒中添加水的信息
    def record_add_water_info(self, box, frame_front, objects_front, time_front, num_frame_front,
                              pred_front, beaker=False):
        y = box[3] - box[1]
        if beaker:
            if not self.add_water_beaker_info or y > self.add_water_beaker_info[4]:
                # self.add_water_beaker_info = [4, img0, preds, time.time(), y, time.time()]
                self.add_water_beaker_info = [4, frame_front, objects_front, time_front, num_frame_front, pred_front]
            else:
                self.add_water_beaker_info[4] = num_frame_front
        else:
            if not self.add_water_info or self.add_water_info[4] < y:
                # self.add_water_info = [4, img0, preds, time.time(), y, time.time()]
                self.add_water_info = [4, frame_front, objects_front, time_front, num_frame_front, pred_front]
            else:
                self.add_water_info[4] = num_frame_front

    def desk_is_clearn(self, top_items, front_items):
        for items in top_items:
            if items.shape[0] == 0:
                continue
            else:
                for item in items:
                    item_box = item[:4]
                    if pt_in_box(center_point(item_box), self.center_box_top) > 0:
                        return False
        for items in front_items:
            if items.shape[0] == 0:
                continue
            else:
                for item in items:
                    item_box = item[:4]
                    if pt_in_box(center_point(item_box), self.center_box_front) > 0:
                        return False
        return True

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            # self.assignScore(*self.clearn_desk_info)
            self.scorePoint8 = True
            conf_c = 0.1
            self.assignScore(index=8,
                             img=self.clearn_desk_info[1],
                             object=self.clearn_desk_info[2],
                             conf=conf_c,
                             time_frame=self.clearn_desk_info[3],
                             num_frame=self.clearn_desk_info[4],
                             name_save="8.jpg",
                             preds=self.clearn_desk_info[5]
                             )
            return True
