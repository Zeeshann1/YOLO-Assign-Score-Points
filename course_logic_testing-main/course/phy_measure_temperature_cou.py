#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/11/11 14:28
# @File    : phy_measure_temperature_cou.py

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


"""
需要注意的点 有时候3,4 的得分点出不来,因为 需要把 头和 温度计的 距离系数设大一点 搜索 由于头的位置
"""


class PHY_measure_temperature(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(PHY_measure_temperature, self).__init__(*args, **kwargs)
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
        self.flagtime2_pre = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
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
        # [self.top_preds, self.front_preds], [self.top_img0, self.front_img0] = self.assign_score_queue.get()
        # if not self.set_center_box:
        #     self.setCenterBox(self.front_preds[0].device, est, esf)  # 设置操作中心区域

        # *-------------------------------------------------* 以下为赋分逻辑部分
        """
            主要用前视角
        """
        beakers_front, thermometers_front, water_columns_front, glass_bubbles_front, hands_front, \
        heads_front, eyes_front = self.preds_front

        beakers_top, thermometers_top, water_columns_top, glass_bubbles_top, hands_top, \
        heads_top, eyes_top = self.preds_top

        try:
            # 1 会估测温度,能正确选择合适的温度计
            if not self.scorePoint1:
                info = self.select_thermometer(1, thermometers_front, hands_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 2 测量时玻璃泡完全浸没于被测液体中,且没有碰到容器底部或容器壁
            if not self.scorePoint2 and self.scorePoint1:
                info = self.correctly_bubble_pos(2,water_columns_front, thermometers_front, beakers_front,
                                          glass_bubbles_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 3 读数时玻璃泡没有离开被测液体
            if not self.scorePoint3 and self.scorePoint2:
                info = self.glass_bubble_in_liquid(3,heads_front, hands_front, eyes_front, thermometers_front,
                                            glass_bubbles_front, beakers_front, water_columns_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 4 待温度计的液注稳定后读数,读数时视线要与温度计中液柱的液面相平
            if not self.scorePoint4 and self.scorePoint3:
                info = self.correctly_read(4,heads_front, hands_front, eyes_front, thermometers_front,
                                           glass_bubbles_front, beakers_front, water_columns_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 5 实验结束后能及时整理仪器
            top_items = [beakers_top, thermometers_top, water_columns_top, glass_bubbles_top, ]
            front_items = [beakers_front, thermometers_front, water_columns_front, glass_bubbles_front]

            if not self.scorePoint5 and (self.scorePoint1 or self.scorePoint2 or
                                         self.scorePoint3 or self.scorePoint4):
                info = self.clearn_desk(5, top_items, front_items)
                if info is not None:
                    self.assignScore(*info)
            if self.scorePoint5 and len(self.score_list) != 5:
                if not self.desk_is_clearn([top_items], [self.center_area_top]):
                    self.retracementScore(5)
        except:
            logger.error(traceback.format_exc())

    # 1
    def select_thermometer(self, score_index, thermometers_front, hands_front):
        """
        1 会估测温度,能正确选择合适的温度计: 手与温度计有交集,且温度计中心点在操作区域内
        :param thermometers_front:
        :param hands_front:
        :return:
        """
        if thermometers_front.shape[0] != 0 and hands_front.shape[0] != 0:
            status = False
            for hand_front in hands_front:
                for thermometer_front in thermometers_front:
                    hand_ther_iou = iou(hand_front[:4], thermometer_front[:4])
                    thermometer_pos = pt_in_polygon(center_point(thermometer_front[:4]), self.center_area_front)
                    if hand_ther_iou > 0 and thermometer_pos:
                        status = True
                        break
            if status:
                self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 4.0, self.flagtime1_2, 3)
                if flag:
                    # self.scorePoint1 = True
                    # self.assignScore(1, self.front_img0, self.front_preds)

                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


    def f_box1_in_box2_have_pos(self, box1, box2, box_base=None, rate=0.1):
        """
        box1 在 box2 里 且 box1 不接触box2 四周有一定的距离;
        :param box1:
        :param box2:
        :param box_base:
        :param rate:
        :return:
        """

        x11, y11, x12, y12 = box1
        x21, y21, x22, y22 = box2
        return x11-x21 > rate * abs(x22 - x21) and y11 - y21 > rate * abs(y22 - y21) \
               and x22-x12 > rate*abs(x22 - x21) and y22-y12 > rate*abs(y22-y21)

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

    # 2.1  --优化
    def correctly_bubble_pos(self,score_index, water_columns_front, thermometers_front, beakers_front, glass_bubbles_front):
        """
        测量时玻璃泡完全浸没于被测液体中,且没有碰到容器底部或容器壁:
        :param water_columns_front:
        :param thermometers_front:
        :param beakers_front:
        :param glass_bubbles_front:
        :return:
        """
        if water_columns_front.shape[0] != 0 and beakers_front.shape[0] != 0:
            if glass_bubbles_front.shape[0] != 0:
                status = False
                for glass_bubble_front in glass_bubbles_front:
                    pos_res = self.f_box1_in_box2_have_pos(box1=glass_bubble_front[:4], box2=water_columns_front[0][:4]
                                                           , box_base=water_columns_front[0][:4], rate=0.1)
                    if pos_res:
                        status = True
                        break
                if status:
                    self.flagtime2, self.flagtime2_pre, flag = self.duration(self.flagtime2, 2.0, self.flagtime2_pre, 2.0)
                    if flag:
                        # self.scorePoint2 = True
                        # self.assignScore(2, self.front_img0, self.front_preds)
                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


            else:
                status = False
                if thermometers_front.shape[0] != 0:
                    for thermometer_front in thermometers_front:
                        de_glass_bubb = self.f_glass_bubb(box1=thermometer_front[:4], box_base=water_columns_front[0][:4],
                                          add_lenth_x_rate=0.1, add_lenth_y_rate=0.1)
                        pos_res = self.f_box1_in_box2_have_pos(box1=de_glass_bubb, box2=water_columns_front[0][:4]
                                                               , box_base=water_columns_front[0][:4], rate=0.1)
                        if pos_res:
                            status = True
                            break
                    if status:
                        self.flagtime2, self.flagtime2_pre, flag = self.duration(self.flagtime2, 2.0, self.flagtime2_pre, 2.0)
                        if flag:
                            # self.scorePoint2 = True
                            # self.assignScore(2, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        pass


    # 3.1
    def glass_bubble_in_liquid(self, score_index, heads_front, hands_front, eyes_front, thermometers_front,
                               glass_bubbles_front, beakers_front, water_columns_front):
        """
        读数时玻璃泡没有离开被测液体: 1 玻璃泡在液体内部: 玻璃泡的中心点与液面柱 上下左右有一定的距离范围 或者 温度计的右下点与液面柱上下左右有一定距离
                                2玻璃泡在液体内部的前提下,头的中心点与温度计的中心点在一个范围内
        :param heads_front:
        :param hands_front:
        :param eyes_front:
        :param thermometers_front:
        :param glass_bubbles_front:
        :param beakers_front:
        :param water_columns_front:
        :return:
        """
        if water_columns_front.shape[0] != 0 and beakers_front.shape[0] != 0 and thermometers_front.shape[0] != 0:
            if glass_bubbles_front.shape[0] != 0 and not self.scorePoint3:
                status = False
                for glass_bubble_front in glass_bubbles_front:
                    pos_res = self.f_box1_in_box2_have_pos(box1=glass_bubble_front[:4], box2=water_columns_front[0][:4]
                                                           , box_base=water_columns_front[0][:4], rate=0.1)
                    if pos_res:
                        status = True
                        break
                if status:
                    # 玻璃泡在液体内部的前提下,
                    sight_status = False
                    for head_front in heads_front:
                        head_cent_pos = center_point(head_front[:4])
                        for thermometer_front in thermometers_front:
                            therm_cent_pos = center_point(thermometer_front[:4])
                            if abs(head_cent_pos[1] - therm_cent_pos[1]) < 0.15 * self.frame_front.shape[0]:
                                # if abs(head_cent_pos[1] - therm_cent_pos[1]) < 1 * self.front_img0.shape[0]:  # 由于头的位置离温度计位置高度相差太大 所以系数要变大
                                sight_status = True
                                break
                    if sight_status:
                        self.flagtime3, _, flag = self.duration(self.flagtime3, 2.0)
                        if flag:
                            # self.scorePoint3 = True
                            # self.assignScore(3, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

            if glass_bubbles_front.shape[0] == 0 and not self.scorePoint3:
                status = False
                for thermometer_front in thermometers_front:
                    de_glass_bubb = self.f_glass_bubb(box1=thermometer_front[:4], box_base=water_columns_front[0][:4],
                                      add_lenth_x_rate=0.1, add_lenth_y_rate=0.1)
                    pos_res = self.f_box1_in_box2_have_pos(box1=de_glass_bubb, box2=water_columns_front[0][:4]
                                                           , box_base=water_columns_front[0][:4], rate=0.1)
                    if pos_res:
                        status = True
                        break
                if status:
                    # 玻璃泡在液体内部的前提下,
                    sight_status = False
                    for head_front in heads_front:
                        head_cent_pos = center_point(head_front[:4])
                        for thermometer_front in thermometers_front:
                            therm_cent_pos = center_point(thermometer_front[:4])
                            if abs(head_cent_pos[1] - therm_cent_pos[1]) < 0.15 * self.frame_front.shape[0]:
                                sight_status = True
                                break
                    if sight_status:
                        self.flagtime3, _, flag = self.duration(self.flagtime3, 2.0)
                        if flag:
                            # self.scorePoint3 = True
                            # self.assignScore(3, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        pass

    # 4.1
    def correctly_read(self, score_index, heads_front, hands_front, eyes_front, thermometers_front,
                       glass_bubbles_front, beakers_front, water_columns_front):
        """
        待温度计的液注稳定后读数,读数时视线要与温度计中液柱的液面相平
        :param heads_front:
        :param hands_front:
        :param eyes_front:
        :param thermometers_front:
        :param glass_bubbles_front:
        :param beakers_front:
        :param water_columns_front:
        :return:
        """
        if water_columns_front.shape[0] != 0 and beakers_front.shape[0] != 0 and thermometers_front.shape[0] != 0:
            if glass_bubbles_front.shape[0] != 0:
                status = False
                for glass_bubble_front in glass_bubbles_front:
                    pos_res = self.f_box1_in_box2_have_pos(box1=glass_bubble_front[:4], box2=water_columns_front[0][:4]
                                                           , box_base=water_columns_front[0][:4], rate=0.1)
                    if pos_res:
                        status = True
                        break
                if status:
                    # print('玻璃泡在液面内---------444')
                    # 玻璃泡在液体内部的前提下,
                    head_info = [[0.]]
                    thermometer_info = [[0.]]
                    sight_status = False
                    for head_front in heads_front:
                        head_cent_pos = center_point(head_front[:4])
                        for thermometer_front in thermometers_front:
                            therm_cent_pos = center_point(thermometer_front[:4])
                            if abs(head_cent_pos[1] - therm_cent_pos[1]) < 0.15 * self.frame_front.shape[0]:
                                # if abs(head_cent_pos[1] - therm_cent_pos[1]) < 1 * self.front_img0.shape[0]:  # 由于头的位置离温度计位置高度相差太大 所以系数要变大
                                sight_status = True
                                head_info[-1] = head_front[:4]
                                thermometer_info[-1] = thermometer_front[:4]
                                break
                    if sight_status:
                        self.flagtime4, _, flag = self.duration(self.flagtime4, 1.0)
                        if flag:
                            # 画出 读数时,视线与温度计持平的框
                            if len(head_info[0]) == 4:
                                self.make_frame(self.frame_front, head_info[0], thermometer_info[0])
                            # self.scorePoint4 = True
                            # self.assignScore(4, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front


            if glass_bubbles_front.shape[0] == 0 and not self.scorePoint4:
                status = False
                for thermometer_front in thermometers_front:
                    de_glass_bubb = self.f_glass_bubb(box1=thermometer_front[:4], box_base=water_columns_front[0][:4],
                                                      add_lenth_x_rate=0.1, add_lenth_y_rate=0.1)
                    pos_res = self.f_box1_in_box2_have_pos(box1=de_glass_bubb, box2=water_columns_front[0][:4]
                                                           , box_base=water_columns_front[0][:4], rate=0.1)
                    if pos_res:
                        status = True
                        break
                if status:
                    sight_status = False
                    head_info = [[0.0]]
                    thermometer_info = [[0.]]
                    for head_front in heads_front:
                        head_cent_pos = center_point(head_front[:4])
                        for thermometer_front in thermometers_front:
                            therm_cent_pos = center_point(thermometer_front[:4])
                            if abs(head_cent_pos[1] - therm_cent_pos[1]) < 0.15 * self.frame_front.shape[0]:
                                sight_status = True
                                head_info[-1] = head_front[:4]
                                thermometer_info[-1] = thermometer_front[:4]
                                break
                    if sight_status:
                        # 画出 读数时,视线与温度计持平的框
                        self.flagtime4, _, flag = self.duration(self.flagtime4, 2.0)
                        if flag:
                            if len(head_info[0]) == 4:
                                self.make_frame(self.frame_front, head_info[0], thermometer_info[0])
                            # self.scorePoint4 = True
                            # self.assignScore(4, self.front_img0, self.front_preds)
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                pass

    # 清理桌面
    def clearn_desk(self, score_index, top_items, front_items):
        # if self.desk_is_clearn(top_items, front_items):
        #     self.clearn_desk_info = [5, self.front_img0, self.front_preds, time.time()]
        #     self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
        #     if flag:
        #         self.scorePoint5 = True
        #         self.assignScore(5, self.front_img0, self.front_preds)
        # else:
        #     self.clearn_time = 0
        if self.desk_is_clearn([front_items], [self.center_area_front]):  # 只看前视角
            self.clearn_desk_info = [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                     self.num_frame_front, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 2)
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
