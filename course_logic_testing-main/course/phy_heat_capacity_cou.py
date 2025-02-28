#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/12/7 13:12
# @File    : phy_heat_capacity_cou.py


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


class PHY_heat_capacity(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(PHY_heat_capacity, self).__init__(*args, **kwargs)
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

        #
        self.flagtime1 = 0.
        self.flagtime1_2 = 0.
        self.flagtime2 = 0.
        self.flagtime2_2 = 0.
        self.flagtime2_2_1 = 0.
        self.flagtime2_2_2 = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
        # 火焰熄灭时间
        self.flag_flame = 0.0
        self.flag_flame_pre = 0.0

        self.flagtime4 = 0.
        self.flagtime4_2 = 0.
        self.flagtime5 = 0.

        self.clearn_time = 0.
        self.clearn_desk_info = []

        self.scoreframe2 = 0
        self.scoreframe3 = 0
        self.scoreframe3_2 = 0
        self.scoreframe4 = 0

        self.set_center_box = False  # 设置中心操作区域

        # 实验标志
        self.flag1 = False

        self.scorePoint3_info = [[], []]
        self.flag3 = False
        self.flag3_gla_bubb = False

        self.beaker_scale_status = False
        self.glass_bubb_in_water_status = False
        self.glass_bubb_in_oil_status = False

    # def setCenterBox(self, device, est=None, esf=None):  # 设置实验操作区域 (可用于判断整理桌面以及排除一些错误位置影响)
    #     if hasattr(self, 'top_img0') and est:
    #         self.h_top, self.w_top = self.top_img0.shape[:2]
    #         self.center_box_top = torch.tensor(
    #             [self.w_top * est[0], self.h_top * est[1], self.w_top * est[2], self.h_top * est[3]],
    #             device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
    #     if hasattr(self, 'front_img0') and esf:
    #         self.h_front, self.w_front = self.front_img0.shape[:2]
    #         self.center_box_front = torch.tensor(
    #             [self.w_front * esf[0], self.h_front * esf[1], self.w_front * esf[2], self.h_front * esf[3]],
    #             device=device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
    #     self.set_center_box = True

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self,top_true,front_true,side_true):  # 赋分逻辑部分
        # [self.side_preds, self.front_preds], [self.side_img0, self.front_img0] = self.assign_score_queue.get()
        # if not self.set_center_box:
        #     self.setCenterBox(self.front_preds[0].device, est, esf)  # 设置操作中心区域

        # *-------------------------------------------------* 以下为赋分逻辑部分
        """
            主要用前视角
        """
        hands_front, flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        matchs_front, thermometers_front, glass_bubbles_front, holders_front, beakers_front, measure_cups_front, \
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front, \
        oil_columns_front, scales_front = self.preds_front

        hands_side, flames_side, alcohol_burners_side, lamp_caps_side, asbestos_nets_side, \
        matchs_side, thermometers_side, glass_bubbles_side, holders_side, beakers_side, measure_cups_side, \
        water_columns_side, match_flames_side, stop_watchs_side, hand_stop_watchs_side, bases_side, oil_columns_side, \
        scales_side = self.preds_side
        try:
            # 1.称取相同质量的水和油分别倒入两只烧杯中
            if not self.scorePoint1:
                info = self.same_quality_water_oil(1,beakers_front, scales_front, water_columns_front, oil_columns_front)
                if info is not None:
                    self.assignScore(*info)

            # 2 加热用温度计测量两液体的初温度t1 预先设定好液体加热的末温度t2
            if self.scorePoint1 and not self.scorePoint2:
                info = self.measure_first_temperature(2,bases_front, beakers_front, thermometers_front, glass_bubbles_front,
                                               water_columns_front,oil_columns_front,
                                               asbestos_nets_front, alcohol_burners_front, flames_front,hands_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 3 分别用酒精灯给两液体加热,记录下加热时刻
            if not self.scorePoint3:
                info = self.two_alcohol_heat_two_liquid(3,bases_front, beakers_front, thermometers_front, glass_bubbles_front,
                                                 water_columns_front, oil_columns_front, asbestos_nets_front,
                                                 alcohol_burners_front, flames_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 4 实验结束后能及时整理仪器
            side_items = [flames_side, alcohol_burners_side, lamp_caps_side, asbestos_nets_side, \
        matchs_side, thermometers_side, glass_bubbles_side, beakers_side, measure_cups_side, \
        water_columns_side, match_flames_side, stop_watchs_side, hand_stop_watchs_side, bases_side]
            front_items = [flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        matchs_front, thermometers_front, glass_bubbles_front, beakers_front, measure_cups_front, \
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front]

            if not self.scorePoint4 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):
                info = self.clearn_desk(4,side_items, front_items)
                if info is not None:
                    self.assignScore(*info)

            if self.scorePoint4 and len(self.score_list) != 4:
                if not self.desk_is_clearn([front_items], [self.center_area_front]):
                    self.retracementScore(4)
        except:
            logger.error(traceback.format_exc())

    #1
    def same_quality_water_oil(self,score_index, beakers_front, scales_front, water_columns_front, oil_columns_front):
        """
        1.称取相同质量的水和油分别倒入两只烧杯中
            烧杯在 电子天平上;
            烧杯中有水柱存在;烧杯中有油柱存在
            烧杯不在电子天平上;
        :param beakers_front:
        :param scales_front:
        :param water_columns_front:
        :param oil_columns_front:
        :return:
        """
        if beakers_front.shape[0] != 0 and scales_front.shape[0] != 0:
            # self.beaker_scale_status = False
            for beaker_front in beakers_front:
                beaker_scale_iou = iou(beaker_front[:4], scales_front[0][:4])
                beaker_in_scale_top = center_distance_v(beaker_front[:4], scales_front[0][:4]) < 0
                if beaker_scale_iou and beaker_in_scale_top:
                    self.beaker_scale_status = True
            if self.beaker_scale_status:
                water_in_beaker, oil_in_beaker = False, False
                if water_columns_front.shape[0] != 0:
                    for beaker_front in beakers_front:
                        for water_column_front in water_columns_front:
                            if iou(beaker_front[:4], water_column_front[:4]) == box_area(water_column_front[:4]):
                                water_in_beaker = True
                                break
                if oil_columns_front.shape[0] != 0:
                    for beaker_front in beakers_front:
                        for oil_column_front in oil_columns_front:
                            if iou(beaker_front[:4], oil_column_front[:4]) == box_area(oil_column_front[:4]):
                                oil_in_beaker = True
                                break
                if water_in_beaker and oil_in_beaker:
                    beaker_scale_status = False
                    for beaker_front in beakers_front:
                        # 烧杯不在电子天平上
                        if iou(beaker_front[:4], scales_front[0][:4]) > 0:
                            beaker_scale_status = True
                    if not beaker_scale_status:
                        self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 2)
                        flag = True
                        if flag:
                            # self.scorePoint1 = True
                            # self.assignScore(1, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    #2
    def measure_first_temperature(self,score_index, bases_front, beakers_front, thermometers_front, glass_bubbles_front, water_columns_front,
                                  oil_columns_front, asbestos_nets_front, alcohol_burners_front, flames_front,hands_front):
        """
        2 加热用温度计测量两液体的初温度t1 预先设定好液体加热的末温度t2
        :param bases_front:
        :param beakers_front:
        :param thermometers_front:
        :param water_columns_front:
        :param asbestos_nets_front:
        :param alcohol_burners_front:
        :param flames_front:
        :return:
        """
        if bases_front.shape[0] != 0 and beakers_front.shape[0] != 0 and water_columns_front.shape[0] != 0 and \
                oil_columns_front.shape[0] != 0:
            glass_bubb_in_water_status, glass_bubb_in_oil_status = False, False
            if glass_bubbles_front.shape[0] != 0:
                for glass_bubble_front in glass_bubbles_front:
                    for water_column_front in water_columns_front:
                        if box1_in_box2(glass_bubble_front[:4], water_column_front[:4]):
                            # 更改水柱的框高度
                            water_column_front = self.f_box_add_y(water_column_front[:4], frame=self.frame_front,
                                                                  add_lenth_y_rate=0.0092)
                            # 烧杯内部 玻璃泡中心点和烧杯的box左右,底部距离在一个范围内 或者 玻璃泡中心点和液面柱的box左右且底部在一个距离范围
                            glass_bubb_in_water_column = self.f_box1_in_box2_have_pos(glass_bubble_front[:4],
                                                                                      water_column_front[:4],
                                                                                      frame=self.frame_front,
                                                                                      rate=0.001)
                            glass_bubbles_ypos = (max(water_column_front[:4][1], water_column_front[:4][3]) -
                                                  max(glass_bubbles_front[0][:4][1],
                                                      glass_bubbles_front[0][:4][3])) > 3.
                            if glass_bubb_in_water_column and glass_bubbles_ypos:
                                glass_bubb_in_water_status = True
                                break
                            pass
                    for oil_column_front in oil_columns_front:
                        if box1_in_box2(glass_bubble_front[:4], oil_column_front[:4]):
                            # 更改水柱的框高度
                            oil_column_front = self.f_box_add_y(oil_column_front[:4], frame=self.frame_front,
                                                                  add_lenth_y_rate=0.0092)
                            # 烧杯内部 玻璃泡中心点和烧杯的box左右,底部距离在一个范围内 或者 玻璃泡中心点和液面柱的box左右且底部在一个距离范围
                            glass_bubb_in_oil_column = self.f_box1_in_box2_have_pos(glass_bubble_front[:4],
                                                                                      oil_column_front[:4],
                                                                                      frame=self.frame_front,
                                                                                      rate=0.001)
                            glass_bubbles_ypos = (max(oil_column_front[:4][1], oil_column_front[:4][3]) -
                                                  max(glass_bubbles_front[0][:4][1],
                                                      glass_bubbles_front[0][:4][3])) > 3.
                            if glass_bubb_in_oil_column and glass_bubbles_ypos:
                                glass_bubb_in_oil_status = True
                                break
                            pass
            if thermometers_front.shape[0] != 0:
                for thermometer_front in thermometers_front:
                    for water_column_front in water_columns_front:
                        if iou(water_column_front[:4], thermometer_front[:4]) > 0:
                            # 自己定义一个 玻璃泡框
                            de_glass_bubb = self.f_glass_bubb(thermometer_front[:4], box_base=water_column_front[:4],
                                                              add_lenth_x_rate=0.05,
                                                              add_lenth_y_rate=0.05)  # 自己定义一个 玻璃泡框
                            # print(f'自己定义玻璃泡的 tensor: {de_glass_bubb}---类型:{type(de_glass_bubb)}')
                            # 烧杯y向下加长;
                            # 更改水柱的框高度
                            water_column_front = self.f_box_add_y(water_column_front[:4], frame=self.frame_front,
                                                                  add_lenth_y_rate=0.0092)
                            # 烧杯内部 玻璃泡中心点和烧杯的box左右,底部距离在一个范围内 或者 玻璃泡中心点和液面柱的box左右且底部在一个距离范围
                            glass_bubb_in_water_column = self.f_box1_in_box2_have_pos(de_glass_bubb,
                                                                                      water_column_front[:4],
                                                                                      frame=self.frame_front,
                                                                                      rate=0.001)
                            glass_bubbles_ypos = (max(water_column_front[:4][1], water_column_front[:4][3]) -
                                                  max(de_glass_bubb[1], de_glass_bubb[3])) > 3.
                            if glass_bubb_in_water_column and glass_bubbles_ypos:
                                glass_bubb_in_water_status = True
                    for oil_column_front in oil_columns_front:
                        if iou(oil_column_front[:4], thermometer_front[:4]) > 0:
                            # 自己定义一个 玻璃泡框
                            de_glass_bubb = self.f_glass_bubb(thermometer_front[:4], box_base=oil_column_front[:4],
                                                              add_lenth_x_rate=0.05,
                                                              add_lenth_y_rate=0.05)  # 自己定义一个 玻璃泡框
                            # print(f'自己定义玻璃泡的 tensor: {de_glass_bubb}---类型:{type(de_glass_bubb)}')
                            # 烧杯y向下加长;
                            # 更改油柱的框高度
                            oil_column_front = self.f_box_add_y(oil_column_front[:4], frame=self.frame_front,
                                                                  add_lenth_y_rate=0.0092)
                            # 烧杯内部 玻璃泡中心点和烧杯的box左右,底部距离在一个范围内 或者 玻璃泡中心点和液面柱的box左右且底部在一个距离范围
                            glass_bubb_in_oil_column = self.f_box1_in_box2_have_pos(de_glass_bubb,
                                                                                      oil_column_front[:4],
                                                                                      frame=self.frame_front,
                                                                                      rate=0.001)
                            glass_bubbles_ypos = (max(oil_column_front[:4][1], oil_column_front[:4][3]) -
                                                  max(de_glass_bubb[1], de_glass_bubb[3])) > 3.
                            if glass_bubb_in_oil_column and glass_bubbles_ypos:
                                glass_bubb_in_oil_status = True

            if glass_bubb_in_water_status and glass_bubb_in_oil_status:
                hand_thermometer_status = False
                # 手与温度计没有交集
                for hand_front in hands_front:

                    for thermometer_front in thermometers_front:
                        if iou(hand_front[:4], thermometer_front[:4]) > 0:
                            hand_thermometer_status = True
                            break
                if not hand_thermometer_status:
                    self.flagtime2, self.flagtime2_2, flag = self.duration(self.flagtime2,2)
                    flag = True

                    if flag:
                        # self.scorePoint2 = True
                        # self.assignScore(2, self.front_img0, self.front_preds)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    #3
    def two_alcohol_heat_two_liquid(self,score_index, bases_front, beakers_front, thermometers_front, glass_bubbles_front,
                                                 water_columns_front, oil_columns_front, asbestos_nets_front,
                                                 alcohol_burners_front, flames_front):
        """
        3 分别用酒精灯给两液体加热,记录下加热时刻
        :param bases_front:
        :param beakers_front:
        :param thermometers_front:
        :param glass_bubbles_front:
        :param water_columns_front:
        :param oil_columns_front:
        :param asbestos_nets_front:
        :param alcohol_burners_front:
        :param flames_front:
        :return:
        """
        if bases_front.shape[0] != 0 and alcohol_burners_front.shape[0] !=0 and asbestos_nets_front.shape[0] != 0 and \
            beakers_front.shape[0] != 0 and flames_front.shape[0] != 0:
            heat_water, heat_oil = False, False
            if water_columns_front.shape[0] != 0:
                for flame_front in flames_front:
                    for water_column_front in water_columns_front:
                        water_flame_pos_y = center_distance_v(flame_front[:4], water_column_front[:4]) > 0  # 火焰在下方
                        water_flame_pos_x = abs(center_distance_h(flame_front[:4], water_column_front[:4])) < 0.01 * self.frame_front.shape[1]
                        if water_flame_pos_y and water_flame_pos_x:
                            heat_water = True
                            break
            if oil_columns_front.shape[0] != 0:
                for flame_front in flames_front:
                    for oil_column_front in oil_columns_front:
                        oil_flame_pos_y = center_distance_v(flame_front[:4], oil_column_front[:4]) > 0
                        oil_flame_pos_x = abs(center_distance_h(flame_front[:4], oil_column_front[:4])) < 0.01 * self.frame_front.shape[1]
                        if oil_flame_pos_y and oil_flame_pos_x:
                            heat_oil = True
                            break
            if heat_water and heat_oil:
                self.flagtime3, self.flagtime3_2, flag = self.duration(self.flagtime3, 2)
                flag = True

                if flag:
                    # self.scorePoint3 = True
                    # self.assignScore(3, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                pass

    # 清理桌面
    def clearn_desk(self,score_index, top_items, front_items):
        # if self.desk_is_clearn(top_items, front_items):
        #     self.clearn_desk_info = [4, self.front_img0, self.front_preds, time.time()]
        #     self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
        #     if flag:
        #         self.scorePoint4 = True
        #         self.assignScore(4, self.front_img0, self.front_preds)
        # else:
        #     self.clearn_time = 0

        if self.desk_is_clearn([front_items], [self.center_area_front]):  # 只看前视角
            self.clearn_desk_info = [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                     self.num_frame_front, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 0.5)
            if flag:
                # self.assignScore(5, self.top_img0, self.top_preds)
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
    #                 # if iou(item_box, self.center_box_front) >0:
    #                 #     return False
    #     return True

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info)
            return True

    def make_frame(self, img, box1, box2, label_CHS="视线与温度计持平", conf=0.888):
        """
        用于将两个框 框在一起 给一个标签
        :param img: 待画的图
        :param box1: 待画的框1
        :param box2: 待画的框2
        :param label_CHS: 标签-中文
        :param conf: 置信度
        :return:
        """
        x_min = min(box1[0], box1[2], box2[0], box2[2])
        y_min = min(box1[1], box1[3], box2[1], box2[3])
        x_max = max(box1[0], box1[2], box2[0], box2[2])
        y_max = max(box1[1], box1[3], box2[1], box2[3])

        x1, y1, x2, y2 = int(x_min), int(y_min), int(x_max), int(y_max)
        color = [0, 0, 255]  # 255,0,0  # [B,G,R]  红色
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)  # 青色框框出所需范围,
        text = f'{"  " * len(label_CHS)} {conf:.2f}'
        ###
        from PIL import Image, ImageDraw, ImageFont
        char_l = (len(label_CHS) * 2 + 7) * 9  ## length of character
        bg_ch = np.array([0, 0, 255], dtype=np.uint8)  # [B,G,R] 蓝色
        bg_ch = np.broadcast_to(bg_ch, (18, char_l, 3))  # 广播机制
        pil_bg = Image.fromarray(bg_ch)
        draw = ImageDraw.Draw(pil_bg)  # 设置背景区域大小(18, char_l, 3),背景颜色为[0,0,255]
        fontStyle = ImageFont.truetype("../font/simhei.ttf", 18)  # 设置字体
        draw.text((5, 1), label_CHS, (255, 255, 255), font=fontStyle)  # 设置字,字体颜色 为白色 (5,0)-字体在背景的显示位置
        np_bg = np.asarray(pil_bg)
        h, w, _ = img.shape
        y, x, _ = np_bg.shape  # y,x 为写中文字的背景 高宽
        px, py = x1, y1  # px,py为需要画框的左上角的点
        # px, py 重新赋值 解决框的背景解释超出图片的范围 问题
        if w - px < x:
            px = w - x
        if py < y:
            py = y
        img[py - y:py, px:px + x] = np_bg  ## Chinese characters background
        cv2.putText(img, text, (px, py - 3), 0, 0.6, [225, 255, 255], thickness=1,
                    lineType=cv2.LINE_AA)

    def f_glass_bubb(self, box1, box_base, add_lenth_x_rate=0.1, add_lenth_y_rate=0.1):
        """
        自定义一个 盒子
        应用于 看不见 玻璃泡的情况,依据温度计的box 定义一个玻璃泡
        根据已知的box1 按照box_base的比例 生成新的 box
        :param box1: 按照此box 的位置 生成新的box
        :param box_base: 按此box比例 得到新的 box
        :return:
        """
        # print(f" 比例box大小   ===={box_base}")
        x11,y11,x12,y12 = box1
        x21,y21,x22,y22 = box_base
        c_x = float((x11 + x12) / 2)
        pre_x1 = c_x - add_lenth_x_rate * abs(x22-x21)
        pre_y1 = max(y11, y12)
        pre_x2 = c_x + add_lenth_x_rate * abs(x22-x21)
        pre_y2 = max(y11, y12) + add_lenth_y_rate * abs(y22-y21)
        return torch.tensor([pre_x1, pre_y1, pre_x2, pre_y2])

    def f_box_add_y(self, box, frame, add_lenth_y_rate):
        """
        烧杯的box 底部向下延长
        :param box:
        :return:
        """

        x1, y1, x2, y2 = box
        # box的中心点的y 在frame的上半部 此时摄像头斜向上照,box底部需要加长
        if center_point(box)[1] < frame.shape[0] / 2:
            # box 底部加长
            pass
        elif center_point(box)[1] > frame.shape[0] / 2:
            # box的中心点的y 在frame的下半部 此时摄像头斜向下照,box底部需要减小
            # box 底部减小
            add_lenth_y_rate = -add_lenth_y_rate
            pass

        return torch.tensor([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2) + add_lenth_y_rate * frame.shape[0]])

    def f_box1_in_box2_have_pos(self,box1, box2, frame=None, rate=0.0026):
        """
        box1 在 box2 里 且 box1 不接触box2 四周有一定的距离;
        :param box1:
        :param box2:
        :param frame:
        :return:
        """

        x11, y11, x12, y12 = box1
        x21, y21, x22, y22 = box2
        return x11-x21 > rate*frame.shape[1] and y11-y21 > rate*frame.shape[0] \
               and x22-x12 > rate*frame.shape[1] and y22-y12 > rate*frame.shape[0]