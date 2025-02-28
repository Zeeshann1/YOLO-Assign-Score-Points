#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/11/22 15:38
# @File    : phy_water_boiling_temperature_cou.py


import random
import traceback
from .comm import *
from logger import logger

# from .a_score import SCORE
# from config import experimental_site_top as est
# from config import experimental_site_front as esf
# from config import experimental_site_front as ess


class PHY_water_boiling_temperature(ConfigModel):

    def __init__(self, *args, **kwargs ):
        super(PHY_water_boiling_temperature, self).__init__(*args, **kwargs)
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
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front = self.preds_front

        hands_side, flames_side, alcohol_burners_side, lamp_caps_side, asbestos_nets_side, \
        matchs_side, thermometers_side, glass_bubbles_side, holders_side, beakers_side, measure_cups_side, \
        water_columns_side, match_flames_side, stop_watchs_side, hand_stop_watchs_side, bases_side = self.preds_side

        try:
            # 1.在烧杯中倒入适量的水，盖住盖板
            if not self.scorePoint1:
                info = self.beaker_water_holder(1,beakers_front, water_columns_front, holders_front,
                                         beakers_side, water_columns_side, holders_side)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 2 能使用火柴点燃酒精灯,调整酒精灯的位置,用酒精灯外焰给水加热
            if self.scorePoint1 and not self.scorePoint2:
                info = self.flame_alcohol_burners(2,alcohol_burners_front, matchs_front, flames_front, beakers_front,
                                           water_columns_front, asbestos_nets_front, holders_front,match_flames_front)
                if info is not None:
                    self.assignScore(*info)

            # 3 能正确固定温度计,让液泡与被测液体充分接触,不碰壁,不碰底
            if self.scorePoint2 and not self.scorePoint3:
                info = self.correct_hold_thermome(3, beakers_front, water_columns_front, thermometers_front,
                                                  glass_bubbles_front,flames_front, beakers_side, water_columns_side,
                                                  thermometers_side, glass_bubbles_side)
                if info is not None:
                    self.assignScore(*info)
            # 4 能正确测量多组温度数据
            # 5 实验结束后能及时整理仪器
            # 6 处理实验数据，并进行比较，得出实验结论


            pass
            # 4 实验结束后能及时整理仪器
            side_items = [flames_side, alcohol_burners_side, lamp_caps_side, asbestos_nets_side, \
        matchs_side, thermometers_side, glass_bubbles_side, holders_side, beakers_side, measure_cups_side, \
        water_columns_side, match_flames_side, stop_watchs_side, hand_stop_watchs_side, bases_side]
            front_items = [flames_front, alcohol_burners_front, lamp_caps_front, asbestos_nets_front, \
        matchs_front, thermometers_front, glass_bubbles_front, holders_front, beakers_front, measure_cups_front, \
        water_columns_front, match_flames_front, stop_watchs_front, hand_stop_watchs_front, bases_front]

            if not self.scorePoint4 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):
                info = self.clearn_desk(4, side_items, front_items)
                if info is not None:
                    self.assignScore(*info)

            if self.scorePoint4 and len(self.score_list) != 4:
                # [top_items], [self.center_area_top]
                if not self.desk_is_clearn([front_items], [self.center_area_front]):
                    self.retracementScore(4)
        except:
            logger.error(traceback.format_exc())

    # 1
    def beaker_water_holder(self,score_index, beakers_front, water_columns_front, holders_front,
                                         beakers_side, water_columns_side, holders_side):
        """
        1.在烧杯中倒入适量的水，盖住盖板
        :param beakers_front:
        :param water_columns_front:
        :param holders_front:
        :param beakers_side:
        :param water_columns_side:
        :param holders_side:
        :return:
        """
        if beakers_front.shape[0] != 0 and water_columns_front.shape[0] != 0 and holders_front.shape[0] != 0:
            status = False
            for beaker_front in beakers_front:
                beaker_holder_iou = iou(beaker_front[:4], holders_front[0][:4])  # 烧杯盖板交集
                beaker_holder_pos_y = center_distance_v(beaker_front[:4], holders_front[0][:4]) > 0  # 盖板在 烧杯的上方
                beaker_holder_pos_x = abs(center_distance_h(beaker_front[:4], holders_front[0][:4]))  # 酒精灯和烧杯水平方向偏移不大
                if beaker_holder_iou and beaker_holder_pos_y and beaker_holder_pos_x < 0.01 * self.frame_front.shape[1]:
                    status = True
                    self.make_frame(self.frame_front, beaker_front[:4], holders_front[0][:4],label_CHS='烧杯盖上盖板')

                    break
            if status:
                self.flagtime1, self.flagtime1_2, flag = self.duration(self.flagtime1, 2.0,)
                flag = True
                if flag:
                    # self.scorePoint1 = True
                    # self.assignScore(1, self.front_img0, self.front_preds)
                    return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

                pass

    # 2
    def flame_alcohol_burners(self,score_index, alcohol_burners_front, matchs_front, flames_front, beakers_front,
                                           water_columns_front, asbestos_nets_front, holders_front, match_flames_front):
        """
        2 能使用火柴点燃酒精灯,调整酒精灯的位置,用酒精灯外焰给水加热
        :param alcohol_burners_front:
        :param matchs_front:
        :param flames_front:
        :param beakers_front:
        :param water_columns_front:
        :param asbestos_nets_front:
        :return:
        """
        # 打火机点燃酒精灯

        if alcohol_burners_front.shape[0] != 0 and beakers_front.shape[0] != 0 and water_columns_front.shape[0] != 0 and holders_front.shape[0] != 0:
            if match_flames_front.shape[0] != 0 and not self.flag1:
                self.flag1 = True
            if flames_front.shape[0] != 0 and not self.flag1:
                # 火焰持续3秒存在 标志为true
                self.flagtime2_2_1, self.flagtime2_2_2, flag = self.duration(self.flagtime2_2_1, 1,)
                flag = True
                if flag:
                    # self.scorePoint2 = True
                    # self.assignScore(2, self.front_img0, self.front_preds)
                    self.flag1 = True
            # 酒精灯外焰加热
            if self.flag1:
                status = False
                for beaker_front in beakers_front:
                    beaker_alco_burner_pos_x = abs(center_distance_h(beaker_front[:4], alcohol_burners_front[0][:4])) < 0.1 * self.frame_front.shape[1]
                    # 烧杯在酒精灯上方: 烧杯box中心点大于 ((0.5*烧杯box的y)+(0.5*酒精灯box的y))
                    beaker_alco_burner_pos_y = center_distance_v(alcohol_burners_front[0][:4], beaker_front[:4]) > 0.5 * abs(alcohol_burners_front[0][1] - alcohol_burners_front[0][3]) + 0.5 * abs(beaker_front[1] - beaker_front[3])
                    if beaker_alco_burner_pos_x and beaker_alco_burner_pos_y and flames_front.shape[0] != 0:
                        status = True
                        break
                if status:

                    self.flagtime2, self.flagtime2_2, flag = self.duration(self.flagtime2, 1,)
                    flag = True
                    if flag:
                        # self.scorePoint2 = True
                        # self.assignScore(2, self.front_img0, self.front_preds)

                        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

            pass

    # 3
    def correct_hold_thermome(self,score_index, beakers_front, water_columns_front, thermometers_front, glass_bubbles_front,
                              flames_front, beakers_side, water_columns_side, thermometers_side, glass_bubbles_side):
        """
        3 能正确固定温度计,让液泡与被测液体充分接触,不碰壁,不碰底
        :param beakers_front:
        :param water_columns_front:
        :param thermometers_front:
        :param glass_bubbles_front:
        :param beakers_side:
        :param water_columns_side:
        :param thermometers_side:
        :param glass_bubbles_side:
        :return:
        """
        if beakers_front.shape[0] != 0 and water_columns_front.shape[0] != 0:
            if glass_bubbles_front.shape[0] != 0:
                for water_column_front in water_columns_front:
                    if box1_in_box2(glass_bubbles_front[0][:4], water_column_front[:4]):
                        # 更改水柱的框高度
                        water_column_front = self.f_box_add_y(water_column_front[:4], frame=self.frame_front,
                                                              add_lenth_y_rate=0.0092)
                        # 烧杯内部 玻璃泡中心点和烧杯的box左右,底部距离在一个范围内 或者 玻璃泡中心点和液面柱的box左右且底部在一个距离范围
                        glass_bubb_in_water_column = self.f_box1_in_box2_have_pos(glass_bubbles_front[0][:4],
                                                                                  water_column_front[:4],
                                                                                  frame=self.frame_front, rate=0.0026)
                        glass_bubbles_ypos = (max(water_column_front[:4][1], water_column_front[:4][3]) -
                                              max(glass_bubbles_front[0][:4][1], glass_bubbles_front[0][:4][3])) > 3.
                        if glass_bubb_in_water_column and glass_bubbles_ypos:
                            self.flagtime3, self.flagtime3_2, flag = self.duration(self.flagtime3, 1,)
                            flag = True
                            if flag and not self.flag3:
                                # self.scorePoint3_info[0] = [3, self.side_img0, self.side_preds, time.time()]
                                self.scorePoint3_info[0] = [score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side]
                                self.flag3 = True
                                # self.scorePoint3 = True
                                # self.assignScore(3, self.side_img0, self.side_img0)

            else:
                if thermometers_front.shape[0] != 0:
                    for water_column_front in water_columns_front:
                        if iou(water_column_front[:4], thermometers_front[0][:4]) > 0:
                            # 自己定义一个 玻璃泡框
                            # de_glass_bubb = self.f_glass_bubb(thermometers_front[0][:4], frame=self.front_img0,
                            #                                   add_lenth_x_rate=0.0052,
                            #                                   add_lenth_y_rate=0.0092)  # 自己定义一个 玻璃泡框

                            de_glass_bubb = self.f_glass_bubb(thermometers_front[0][:4], box_base=water_column_front[:4],
                                                              add_lenth_x_rate=0.05,
                                                              add_lenth_y_rate=0.05)  # 自己定义一个 玻璃泡框
                            # print(f'自己定义玻璃泡的 tensor: {de_glass_bubb}---类型:{type(de_glass_bubb)}')
                            # 烧杯y向下加长;
                            # 更改烧杯的框高度
                            water_column_front = self.f_box_add_y(water_column_front[:4], frame=self.frame_front,
                                                            add_lenth_y_rate=0.0092)
                            # 烧杯内部 玻璃泡中心点和烧杯的box左右,底部距离在一个范围内 或者 玻璃泡中心点和液面柱的box左右且底部在一个距离范围
                            glass_bubb_in_water_column = self.f_box1_in_box2_have_pos(de_glass_bubb,
                                                            water_column_front[:4], frame=self.frame_front, rate=0.0026)
                            glass_bubbles_ypos = (max(water_column_front[:4][1], water_column_front[:4][3]) -
                                                  max(de_glass_bubb[1], de_glass_bubb[3])) > 3.
                            if glass_bubb_in_water_column and glass_bubbles_ypos:
                                self.flagtime3, _, flag = self.duration(self.flagtime3, 1)
                                flag = True
                                if flag and not self.flag3_gla_bubb:
                                    # print('没有玻璃泡的情况22222================')
                                    # self.scorePoint3 = True
                                    # self.assignScore(3, self.side_img0, self.side_img0)
                                    # self.scorePoint3_info[1] = [3, self.side_img0, self.side_preds, time.time()]
                                    self.scorePoint3_info[1] = [score_index, self.frame_side, self.time_side, self.objects_side,
                                                                self.preds_side]

                                    self.flag3_gla_bubb = True
            # 当 烧杯与温度计没有交集的时候,此时出得分点
            status = False
            for beaker_front in beakers_front:
                if thermometers_front.shape[0] != 0:
                    if iou(beaker_front[:4], thermometers_front[0][:4]) == 0:
                        # 烧杯和温度计没有交集
                        status = True
                if glass_bubbles_front.shape[0] != 0:
                    if iou(beaker_front[:4], glass_bubbles_front[0][:4]) == 0:
                        # 烧杯和玻璃泡没有交集
                        status = True

            # 火焰熄灭时
            if flames_front.shape[0] == 0:
                self.flag_flame, self.flag_flame_pre, flag = self.duration(self.flag_flame, 1,)
                flag = True
                if flag:
                    status = True
            if status:
                if self.scorePoint3_info[0]:
                    # self.scorePoint3 = True
                    # self.assignScore(*[self.scorePoint3_info[0][0], self.scorePoint3_info[0][1], self.scorePoint3_info[0][2], self.scorePoint3_info[0][3]])
                    return self.scorePoint3_info[0]
                else:
                    if self.scorePoint3_info[1]:
                        # self.scorePoint3 = True
                        # self.assignScore(*[self.scorePoint3_info[1][0], self.scorePoint3_info[1][1], self.scorePoint3_info[1][2], self.scorePoint3_info[1][3]])
                        return self.scorePoint3_info[1]

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
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 2)
            flag = True
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
            # box的中心点的y 在frame的上半部 此时摄像头斜向下照,box底部需要减小
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