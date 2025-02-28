#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/05/04 14:34
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_sz_cou.py

'''
一定溶质质量分数的氯化钠溶液配置(托盘天平)
'''

from .comm import *
from .about_weigh_score_point_sz_cou import AboutWeigh

experimental_site_front = [[0.223, 0.],
                           [0.303, 0.61],
                           [0.315, 0.665],
                           [0.343, 0.71],
                           [0.385, 0.74],
                           [0.424, 0.75],
                           [0.576, 0.75],
                           [0.615, 0.74],
                           [0.657, 0.71],
                           [0.685, 0.665],
                           [0.697, 0.61],
                           [0.777, 0.]]

experimental_site_top = [[0.3, 1.0],
                         [0.3, 0.62],
                         [0.31, 0.55],
                         [0.33, 0.51],
                         [0.36, 0.48],
                         [0.4, 0.46],
                         [0.6, 0.46],
                         [0.64, 0.48],
                         [0.67, 0.51],
                         [0.69, 0.55],
                         [0.7, 0.62],
                         [0.7, 1.0]]


class CHEM_allocate_solution_sz(AboutWeigh):

    def __init__(self, *args, **kwargs):
        super(CHEM_allocate_solution_sz, self).__init__(*args, **kwargs)
        self.last_frame_info = []
        self.r_list = []
        self.check_c = False
        self.judget_g = False
        self.V_R_THRE_BREAK = 0.42  # 烧杯中水的比例
        self.V_R_THRE_NMB = 0.55  # 细口瓶中水的比例
        self.set_front_area = False

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    @try_decorator
    def score_process(self, *args):  # 赋分逻辑部分
        (hands_front, eyes_front, heads_front, dusters_front, measuring_cylinders_front,
         measuring_cylinder_bottoms_front, water_columns_front, liquid_levels_front, narrow_mouth_bottles_front,
         narrow_mouth_bottlenecks_front, narrow_stopper_no_upends_front, narrow_stopper_upends_front, labels_front,
         liquids_front, salt_granules_front, beakers_front, glass_rods_front, droppers_front, label_papers_front,
         labellings_front, pens_front, writings_front, write_labels_front) = self.preds_front
        '''
        手, 眼睛, 头, 抹布, 量筒, 
        量筒底, 水柱, 液面, 细口瓶, 
        细口瓶口, 细口瓶瓶塞未倒放, 细口瓶瓶塞倒放, 标签, 
        液体, 食盐颗粒, 烧杯, 玻璃棒, 胶头滴管, 标签纸
        贴标签, 笔, 写字, 写标签
        '''
        (hands_top, eyes_top, heads_top, dusters_top, measuring_cylinders_top,
         measuring_cylinder_bottoms_top, water_columns_top, liquid_levels_top, narrow_mouth_bottles_top,
         narrow_mouth_bottlenecks_top, narrow_stopper_no_upends_top, narrow_stopper_upends_top, labels_top,
         liquids_top, salt_granules_top, beakers_top, glass_rods_top, droppers_top, label_papers_top,
         labellings_top, pens_top, writings_top, write_labels_top) = self.preds_top

        if not self.judget_g:
            min_y = self.h_top
            for items in self.preds_top:
                for item in items:
                    if item[1] < min_y:
                        min_y = item[1]
            if min_y > self.h_top *  0.14 and min_y != self.h_top: # 一代
                self.center_area_top = (np.array(experimental_site_top) * [self.w_top, self.h_top]).astype(np.int32)
            self.judget_g = True

        self.last_frame_info = [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]

        if not self.set_front_area:
            self.center_operation_area_front = (
                    np.array(experimental_site_front) * [self.w_front, self.h_front]).astype(np.int32)
            self.set_front_area = True

        # 2. 能选用100 mL量筒量取液体
        if not self.scorePoint2 and self.water_in_cylinder:
            self.assignScore(2, *self.last_frame_info[:5])  # 默认先赋分

        if not self.water_in_cylinder:
            self.waterInCylinder(None, water_columns_front, liquid_levels_front, measuring_cylinders_front)

        # 3. 取用水时能瓶塞倒放
        if not self.scorePoint3:
            self.stopperUpend(narrow_stopper_upends_front, narrow_stopper_no_upends_front, narrow_stopper_upends_top,
                              narrow_stopper_no_upends_top)
            if self.stoper_unend_info and self.water_in_cylinder and abs(
                    self.water_in_cylinder_secs - self.stoper_unend_info[-1]) < 30:
                self.assignScore(3, *self.stoper_unend_info[:5])
            elif self.stoper_unend_info and self.pour_water_to_cylinder(narrow_mouth_bottles_front,
                                                                        measuring_cylinders_front):
                self.assignScore(3, *self.stoper_unend_info[:5])
            elif self.stoper_unend_info and self.pour_water_to_cylinder(narrow_mouth_bottlenecks_front,
                                                                        measuring_cylinders_front):
                self.assignScore(3, *self.stoper_unend_info[:5])

        # 4. 能正确使用胶头滴管定容
        # if self.water_in_cylinder and not self.scorePoint4:
        if not self.scorePoint4:
            info = self.dropWater2cylinder(droppers_front, measuring_cylinders_front, water_columns_front,
                                           liquid_levels_front)
            self.dropWater2cylinderTop(droppers_top, measuring_cylinders_top, hands_top)
            if self.scorePoint5 and self.preReadDisplayData(narrow_mouth_bottles_front, measuring_cylinders_front):
                self.readDisplayData(hands_front, measuring_cylinders_front, water_columns_front,
                                     liquid_levels_front,
                                     heads_front, eyes_front)
            if info:
                if not self.scorePoint3 and self.stoper_unend_info:
                    self.assignScore(3, *self.stoper_unend_info[:5])
                self.assignScore(4, *info[:5])
                if self.scorePoint5 and self.secs - self.read_display_score_secs > 5:
                    self.retracementScore(5)
                    self.initReadCylinderDiaplayData()

        if not self.no_water_column_flag and self.water_in_cylinder and self.secs - self.water_in_cylinder_secs > 5:
            self.no_water_column(water_columns_front, liquid_levels_front)

        # 5. 能平视凹液面最低处
        if not self.scorePoint5:
            if self.preReadDisplayData(narrow_mouth_bottles_front, measuring_cylinders_front):
                self.readDisplayData(hands_front, measuring_cylinders_front, water_columns_front,
                                     liquid_levels_front,
                                     heads_front, eyes_front)
                if self.no_water_column_flag or self.water_in_beaker_flag:
                    if self.read_display_info:
                        self.assignScore(5, *self.read_display_info[:5])
                    elif self.read_display_head_info:
                        self.assignScore(5, *self.read_display_head_info[:5])
                    if not self.scorePoint3 and self.stoper_unend_info:
                        self.assignScore(3, *self.stoper_unend_info[:5])

        if not self.water_in_beaker_flag:
            self.water2beaker(hands_front, measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                              liquids_front)

        # #  判断水量  烧杯不准确，取消判断
        # if not self.check_c and not self.water_in_beaker_flag:
        #     self.water2beaker(measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front, liquids_front)
        # # elif not self.check_c and self.water_in_beaker_flag:
        # elif self.water_in_beaker_flag:
        #     if beakers_front.shape[0] > 0 and liquids_front.shape[0] > 0 and hands_front.shape[0] > 0:
        #         for beaker_front in beakers_front:
        #             beaker_front_box = beaker_front[:4]
        #             is_break = False
        #             for liquid_front in liquids_front:
        #                 liquid_front_box = liquid_front[:4]
        #                 if iou(liquid_front_box, beaker_front_box) > box_area(liquid_front_box) * 0.8:
        #                     r = int(beaker_front_box[3] - liquid_front_box[1]) / high(beaker_front_box)
        #                     point = (int(liquid_front_box[0]), int(liquid_front_box[3] + 50))
        #                     cv2.putText(self.frame_front, f"r{r:.2f}", point, cv2.FONT_HERSHEY_SIMPLEX, 1,
        #                                 (0, 0, 255), 2)
        #                     if len(self.r_list) > 40:
        #                         self.r_list.pop(-1)
        #                     self.r_list.append(r)
        #                     if len(self.r_list) == 40:
        #                         if sum(self.r_list[-10:]) / 10 < self.V_R_THRE_BREAK:
        #                             self.retracementScore(2)  # 撤回 得分点 2
        #                             self.scorePoint2 = True
        #                         self.check_c = True
        #                     is_break = True
        #                     break
        #             if is_break:
        #                 break

        # 6. 能选用玻璃棒搅拌
        if not self.scorePoint6:
            info = self.select_glass_rod_stir(glass_rods_front, beakers_front, hands_front, liquids_front,
                                              glass_rods_top, beakers_top, hands_top, self.water_in_beaker_flag)
            if info is not None:
                self.assignScore(6, *info[:5])
                if not self.scorePoint3 and self.stoper_unend_info:
                    self.assignScore(3, *self.stoper_unend_info[:5])

        # 7. 正确使用玻璃棒
        if not self.scorePoint7:
            info = self.correct_use_glass_rod_stir(glass_rods_front, beakers_front, hands_front, liquids_front,
                                                   glass_rods_top, beakers_top, hands_top, self.water_in_beaker_flag)
            if info is not None:
                self.assignScore(7, *info[:5])
                if not self.scorePoint6:
                    self.assignScore(6, *info[:5])

            if self.auxiliary_glass_rod_stir(glass_rods_front, beakers_front, hands_front, liquids_front,
                                             self.water_in_beaker_flag):
                if (self.use_glass_rod_secs >= self.hand_over_beaker_secs
                        and self.use_glass_rod_secs <= self.hand_over_beaker_secs_pre):
                    if not self.scorePoint6 and self.use_glass_rod_secs - self.hand_over_beaker_secs > 4:
                        self.assignScore(6, *self.last_frame_info[:5])
                    if not self.scorePoint7 and self.hand_over_beaker_secs_pre - self.hand_over_beaker_secs > 15:
                        self.assignScore(7, *self.last_frame_info[:5])

        if not self.check_c and (self.scorePoint6 or self.scorePoint7) and not self.transfer_liquid_flag:  # 转移液体
            if self.transferLiquid(beakers_front, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front,
                                   hands_front):
                self.r_list = []
        # if not self.check_c and self.transfer_liquid_flag:
        #     if narrow_mouth_bottles_front.shape[0] > 0 and liquids_front.shape[0] > 0 and hands_front.shape[0] > 0:
        #         for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
        #             narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
        #             is_break = False
        #             for liquid_front in liquids_front:
        #                 liquid_front_box = liquid_front[:4]
        #                 if iou(liquid_front_box, narrow_mouth_bottle_front_box) > box_area(liquid_front_box) * 0.8:
        #                     r = int(narrow_mouth_bottle_front_box[3] - liquid_front_box[1]) / high(
        #                         narrow_mouth_bottle_front_box)
        #                     # point = (int(liquid_front_box[0]), int(liquid_front_box[3] + 50))
        #                     # cv2.putText(self.frame_front, f"r{r:.2f}", point, cv2.FONT_HERSHEY_SIMPLEX, 1,
        #                     #             (0, 0, 255), 2)
        #                     if len(self.r_list) > 50:
        #                         self.r_list.pop(-1)
        #                     self.r_list.append(r)
        #                     if len(self.r_list) == 50:
        #                         if sum(self.r_list[-20:]) / 20 < self.V_R_THRE_NMB:
        #                             self.retracementScore(2)  # 撤回 得分点 2
        #                             self.scorePoint2 = True
        #                         self.check_c = True
        #                     is_break = True
        #                     break
        #             if is_break:
        #                 break

        # 8. 正确书写标签内容
        if not self.scorePoint8 and len(self.score_list) > 0:
            info = self.correct_write_label(write_labels_front, writings_front, hands_front, pens_front,
                                            label_papers_front,
                                            write_labels_top, writings_top, hands_top, pens_top, label_papers_top)
            if info is not None:
                if self.scorePoint11:
                    self.retracementScore(8)
                self.assignScore(8, *info[:5])
                if self.scorePoint9:
                    self.retracementScore(9)

        if not self.scorePoint11 and self.transfer_liquid_flag:
            info = self.stick_label(labellings_front, narrow_mouth_bottles_front, labellings_top,
                                    narrow_mouth_bottles_top)
            if info is not None:
                self.assignScore(8, *info[:5])
                self.scorePoint8 = False
                self.scorePoint11 = True

        # 9. 清洗仪器，整理桌面
        top_items = [measuring_cylinders_top, measuring_cylinder_bottoms_top,  # narrow_mouth_bottles_top,
                     narrow_stopper_no_upends_top, narrow_stopper_upends_top,
                     beakers_top, glass_rods_top, droppers_top]
        """
        量筒 量筒底 细口瓶
        细口瓶塞倒放 细口瓶塞正放
        烧杯 玻璃棒 胶头滴管
        """

        front_items = [measuring_cylinder_bottoms_front, narrow_mouth_bottles_front,
                       narrow_stopper_no_upends_front, narrow_stopper_upends_front,
                       beakers_front, glass_rods_front, droppers_front]

        if not self.scorePoint9 and len(self.score_list) > 1:
            info = self.clearnDesk(["top", "front"], [top_items, front_items],
                                   [self.center_area_top, self.center_operation_area_front])
            if info:
                self.assignScore(9, *info[:5])
                self.assignScore(10, *info[:5])
        if self.scorePoint9 and len(self.score_list) != 10:
            if not self.desk_is_clearn(["top", "front"], [top_items], [self.center_area_top]):
                self.retracementScore(9)
                self.retracementScore(10)

    @try_decorator
    def end(self):
        if not self.scorePoint4 and self.drop_water_info_top:
            self.assignScore(4, *self.drop_water_info_top[:5])
        if not self.scorePoint5:
            if self.read_display_info:
                self.assignScore(5, *self.read_display_info[:5])
            elif self.read_display_head_info:
                self.assignScore(5, *self.read_display_head_info[:5])
        if not self.scorePoint6:
            if self.select_glass_rod_stir_info:
                self.assignScore(6, *self.select_glass_rod_stir_info[:5])
            elif self.select_glass_rod_stir_info_top:
                self.assignScore(6, *self.select_glass_rod_stir_info_top)
        if not self.scorePoint7:
            if self.select_glass_rod_stir_info:
                self.assignScore(7, *self.select_glass_rod_stir_info[:5])
            elif self.select_glass_rod_stir_info_top:
                self.assignScore(7, *self.select_glass_rod_stir_info_top)
        if not self.scorePoint9 and self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:  # 结束前 2s 内有记录
            self.assignScore(9, *self.clearn_desk_info[:5])
        if not self.scorePoint10:
            self.assignScore(10, *self.last_frame_info[:5])
