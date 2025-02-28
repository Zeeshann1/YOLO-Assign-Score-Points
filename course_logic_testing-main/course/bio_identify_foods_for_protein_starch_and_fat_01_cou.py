#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04
# @Author  : Qinhe
# @File    : bio_identify_foods_for_protein_starch_and_fat_01_cou.py


from .comm import *
from .comm.course_base import ConfigModel
import copy
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()


class BIO_identify_foods(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(BIO_identify_foods, self).__init__(*args, **kwargs)

        self.set_center_box = False  # 设置操作区域框将用过的实验材料放入废料槽中，其它实验用品归位，清洁桌面，举手示意实验完毕
        self.center_box = None

        self.scorePoint1 = False
        self.scorePoint2 = False
        self.scorePoint3 = False
        self.scorePoint4 = False
        self.scorePoint5 = False
        self.scorePoint6 = False
        self.scorePoint7 = False
        self.scorePoint8 = False
        self.scorePoint9 = False
        self.scorePoint10 = False
        self.scorePoint11 = False
        self.scorePoint12 = False
        self.scorePoint13 = False
        self.scorePoint14 = False
        self.scorePoint15 = False
        self.scorePoint16 = False

        self.point_swich1 = True
        self.point_swich2 = False
        self.point_swich3 = False
        self.point_swich4 = False
        self.point_swich5 = False
        self.point_swich6 = False
        self.point_swich7 = False
        self.point_swich8 = False
        self.point_swich9 = False
        self.point_swich10 = False
        self.point_swich11 = False
        self.point_swich12 = False
        self.point_swich13 = False
        self.point_swich14 = False
        self.point_swich15 = False
        self.point_swich16 = False

        self.experiment_ing = False  # 正在做实验  判断拆除器材
        self.experiment_end = 0  # 器材完成拆除事件计数
        self.first_end = False  # 一次完整的实验

        self.point2_d = []

        self.flag1_inertance_top = 0
        self.flag1_inertance_side = 0
        self.flag1_inertance_front = 0
        self.flag2_inertance_top = 0
        self.flag2_inertance_side = 0
        self.flag2_inertance_front = 0
        self.flag3_inertance_top = 0
        self.flag3_inertance_side = 0
        self.flag3_inertance_front = 0
        self.flag4_inertance_top = 0
        self.flag4_inertance_side = 0
        self.flag4_inertance_front = 0
        self.flag5_inertance_top = 0
        self.flag5_inertance_side = 0
        self.flag5_inertance_front = 0
        self.flag6_inertance_top = 0
        self.flag6_inertance_side = 0
        self.flag6_inertance_front = 0
        self.flag7_inertance_top = 0
        self.flag7_inertance_side = 0
        self.flag7_inertance_front = 0
        self.flag8_inertance_top = 0
        self.flag8_inertance_side = 0
        self.flag8_inertance_front = 0
        self.flag9_inertance_top = 0
        self.flag9_inertance_side = 0
        self.flag9_inertance_front = 0
        self.flag10_inertance_top = 0
        self.flag10_inertance_side = 0
        self.flag10_inertance_front = 0
        self.flag11_inertance_top = 0
        self.flag11_inertance_side = 0
        self.flag11_inertance_front = 0
        self.flag12_inertance_top = 0
        self.flag12_inertance_side = 0
        self.flag12_inertance_front = 0
        self.flag13_inertance_top = 0
        self.flag13_inertance_side = 0
        self.flag13_inertance_front = 0
        self.flag14_inertance_top = 0
        self.flag14_inertance_side = 0
        self.flag14_inertance_front = 0
        self.flag15_inertance_top = 0
        self.flag15_inertance_side = 0
        self.flag15_inertance_front = 0
        self.flag16_inertance_top = 0
        self.flag16_inertance_side = 0
        self.flag16_inertance_front = 0

        self.clearn_desk_info = []  # 整理桌面信息

        self.class_name = ['flour', 'dough', 'gelatinoid',
                           'peanut', 'wheat', 'slitting_peanut',
                           'crosscutting_peanut', 'slitting_wheat', 'crosscutting_wheat',
                           'iodine_solution', 'red_ink', 'dropper', 'dropper_water',
                           'dropper_starch', 'dropper_iodine_solution', 'dropper_red_ink',
                           'tube', 'volatile_liquid', 'tube_starch', 'tube_blue_liquid',
                           'tube_red_liquid', 'tube_end', 'tube_top', 'liquid_level',
                           'white_paper', 'press', 'grease',
                           'gauze', 'gauze_dough', 'blade', 'hand_blade',
                           'tweezers', 'tweezers_top', 'medicine_spoon', 'medicine_spoon_top',
                           'beaker', 'knead_dough', 'beaker_water', 'beaker_starch',
                           'clean']

    def score_process(self, top_true, front_true, side_true):
        if top_true or front_true or side_true:
        # *-------------------------------------------------* 以下为赋分逻辑部分
        # [top_preds, side_preds, front1_preds], [top_img0, side_img0, front_img0] = preds, img0s # 检测框和ing

            if top_true:
                flour_top, dough_top, gelatinoid_top, \
                peanut_top, wheat_top, slitting_peanut_top, \
                crosscutting_peanut_top, slitting_wheat_top, crosscutting_wheat_top, \
                iodine_solution_top, red_ink_top, dropper_top, dropper_water_top, \
                dropper_starch_top, dropper_iodine_solution_top, dropper_red_ink_top, \
                tube_top, volatile_liquid_top, tube_starch_top, tube_blue_liquid_top, \
                tube_red_liquid_top, tube_end_top, tube_top_top, liquid_level_top, \
                white_paper_top, press_top, grease_top, \
                gauze_top, gauze_dough_top, blade_top, hand_blade_top, \
                tweezers_top, tweezers_top_top, medicine_spoon_top, medicine_spoon_top_top, \
                beaker_top, knead_doughpress_top, beaker_water_top, beaker_starch_top, \
                clean_top = self.preds_top

                # 确定图片正反  #
                if not self.set_center_box and beaker_top.shape[0] != 0:
                    # h, w = self.top_img0.shape[:2]  todo
                    # 根据最开始器材在图片的位置确定操作区域
                    center_box_upright = torch.tensor([self.w_top * 0.33, self.h_top * 0.45, self.w_top * 0.72, self.h_top * 0.87], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
                    center_box_upend = torch.tensor([self.w_top * 0.28, self.h_top * 0.13, self.w_top * 0.67, self.h_top * 0.55], device=self.device)  ## 桌面实验区域，该区域没有物品代表已经整理桌面

                    binding_post = center_point(beaker_top[0][0:4])
                    self.center_box = center_box_upend if binding_post[1] > (self.h_top / 2) else center_box_upright
                    self.set_center_box = True

                # 胶头滴管液体
                dropper_liquid_top = torch.cat([dropper_water_top, dropper_starch_top, dropper_iodine_solution_top, dropper_red_ink_top], dim=0)
                if dropper_liquid_top.shape[0] != 0:
                    dropper_liquid_top = dropper_liquid_top[torch.argsort(-dropper_liquid_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 试管液体
                tube_liquid_top = torch.cat([tube_starch_top, tube_blue_liquid_top, tube_red_liquid_top], dim=0)
                if tube_liquid_top.shape[0] != 0:
                    tube_liquid_top = tube_liquid_top[torch.argsort(-tube_liquid_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 烧杯液体
                beaker_liquid_top = torch.cat([beaker_water_top, beaker_starch_top], dim=0)
                if beaker_liquid_top.shape[0] != 0:
                    beaker_liquid_top = beaker_liquid_top[torch.argsort(-beaker_liquid_top[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 种子：花生、小麦、纵切花生、纵切小麦、横切花生、横切小麦
                seed_top = torch.cat([peanut_top, wheat_top, slitting_peanut_top, crosscutting_peanut_top, slitting_wheat_top, crosscutting_wheat_top], dim=0)

                # 烧杯、试管、刀片、镊子、药匙、白纸、胶头滴管、纱布、碘液、红墨水、种子（包括切开的）
                equipments_top = torch.cat([beaker_top, tube_top, blade_top, tweezers_top, medicine_spoon_top,
                                            gauze_top, dropper_top, white_paper_top, iodine_solution_top, red_ink_top, seed_top], dim=0)  #

            if side_true:
                flour_side, dough_side, gelatinoid_side, \
                peanut_side, wheat_side, slitting_peanut_side, \
                crosscutting_peanut_side, slitting_wheat_side, crosscutting_wheat_side, \
                iodine_solution_side, red_ink_side, dropper_side, dropper_water_side, \
                dropper_starch_side, dropper_iodine_solution_side, dropper_red_ink_side, \
                tube_side, volatile_liquid_side, tube_starch_side, tube_blue_liquid_side, \
                tube_red_liquid_side, tube_end_side, tube_top_side, liquid_level_side, \
                white_paper_side, press_side, grease_side, \
                gauze_side, gauze_dough_side, blade_side, hand_blade_side, \
                tweezers_side, tweezers_top_side, medicine_spoon_side, medicine_spoon_top_side, \
                beaker_side, knead_doughpress_side, beaker_water_side, beaker_starch_side, \
                clean_side = self.preds_side

                # 胶头滴管液体
                dropper_liquid_side = torch.cat([dropper_water_side, dropper_starch_side, dropper_iodine_solution_side, dropper_red_ink_side], dim=0)
                if dropper_liquid_side.shape[0] != 0:
                    dropper_liquid_side = dropper_liquid_side[torch.argsort(-dropper_liquid_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 试管液体
                tube_liquid_side = torch.cat([tube_starch_side, tube_blue_liquid_side, tube_red_liquid_side], dim=0)
                if tube_liquid_side.shape[0] != 0:
                    tube_liquid_side = tube_liquid_side[torch.argsort(-tube_liquid_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 烧杯液体
                beaker_liquid_side = torch.cat([beaker_water_side, beaker_starch_side], dim=0)
                if beaker_liquid_side.shape[0] != 0:
                    beaker_liquid_side = beaker_liquid_side[torch.argsort(-beaker_liquid_side[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 种子：花生、小麦、纵切花生、纵切小麦、横切花生、横切小麦
                seed_side = torch.cat([peanut_side, wheat_side, slitting_peanut_side, crosscutting_peanut_side, slitting_wheat_side, crosscutting_wheat_side], dim=0)

            if front_true:
                flour_front, dough_front, gelatinoid_front, \
                peanut_front, wheat_front, slitting_peanut_front, \
                crosscutting_peanut_front, slitting_wheat_front, crosscutting_wheat_front, \
                iodine_solution_front, red_ink_front, dropper_front, dropper_water_front, \
                dropper_starch_front, dropper_iodine_solution_front, dropper_red_ink_front, \
                tube_front, volatile_liquid_front, tube_starch_front, tube_blue_liquid_front, \
                tube_red_liquid_front, tube_end_front, tube_top_front, liquid_level_front, \
                white_paper_front, press_front, grease_front, \
                gauze_front, gauze_dough_front, blade_front, hand_blade_front, \
                tweezers_front, tweezers_top_front, medicine_spoon_front, medicine_spoon_top_front, \
                beaker_front, knead_doughpress_front, beaker_water_front, beaker_starch_front, \
                clean_front = self.preds_front

                # 胶头滴管液体
                dropper_liquid_front = torch.cat([dropper_water_front, dropper_starch_front, dropper_iodine_solution_front, dropper_red_ink_front], dim=0)
                if dropper_liquid_front.shape[0] != 0:
                    dropper_liquid_front = dropper_liquid_front[torch.argsort(-dropper_liquid_front[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 试管液体
                tube_liquid_front = torch.cat([tube_starch_front, tube_blue_liquid_front, tube_red_liquid_front], dim=0)
                if tube_liquid_front.shape[0] != 0:
                    tube_liquid_front = tube_liquid_front[torch.argsort(-tube_liquid_front[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 烧杯液体
                beaker_liquid_front = torch.cat([beaker_water_front, beaker_starch_front], dim=0)
                if beaker_liquid_front.shape[0] != 0:
                    beaker_liquid_front = beaker_liquid_front[torch.argsort(-beaker_liquid_front[:, 4])]  # 置信度排序,开关取第一个  torch.sort(input, dim=0)按列排序

                # 种子：花生、小麦、纵切花生、纵切小麦、横切花生、横切小麦
                seed_front = torch.cat([peanut_front, wheat_front, slitting_peanut_front, crosscutting_peanut_front, slitting_wheat_front, crosscutting_wheat_front], dim=0)

            """
                todo
            """
            if top_true and front_true:
                # 判断是否已经完成一次实验操作  演示版用导线辅助判断
                self.all_point_swich(flour_top, dough_top, gelatinoid_top, seed_front,
                                     dropper_front, dropper_iodine_solution_front, dropper_red_ink_front,
                                     press_front, gauze_dough_front, hand_blade_front, knead_doughpress_front,
                                     beaker_starch_front, clean_top)
            # self.all_estimate_experiment_ing(wire_connection_top)  # todo 重置self.的变量

            # 画布
            # self.all_canvas_creation()  # 创建画布

            # 1.用药匙取适量面粉，加清水和成面团
            if not self.scorePoint1 and self.point_swich1 and "1" in self.exper_score_ids:
                point1view = self.point1(top_true, flour_top, dough_top, dropper_top, dropper_water_top, medicine_spoon_top, medicine_spoon_top_top,
                                         side_true, flour_side, dough_side, dropper_side, dropper_water_side, medicine_spoon_side, medicine_spoon_top_side,
                                         front_true, flour_front, dough_front, dropper_front, dropper_water_front, medicine_spoon_front, medicine_spoon_top_front)
                if point1view[0]:
                    self.scorePoint1 = True
                    if point1view[1] == 'top':
                        self.assignScore(1, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point1view[1] == 'side':
                        self.assignScore(1, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point1view[1] == 'front':
                        self.assignScore(1, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)
            # END scorePoint1

            # 2.用纱布包着面团
            if not self.scorePoint2 and self.point_swich2 and "2" in self.exper_score_ids:
                point2view = self.point2(top_true, dough_top, gauze_top, gauze_dough_top,
                                         side_true, dough_side, gauze_side, gauze_dough_side,
                                         front_true, dough_front, gauze_front, gauze_dough_front)
                if point2view[0]:
                    self.scorePoint2 = True
                    if point2view[1] == 'top':
                        self.assignScore(2, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point2view[1] == 'side':
                        self.assignScore(2, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point2view[1] == 'front':
                        self.assignScore(2, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 3.用纱布包着面团放入盛有清水的烧杯中，轻轻揉挤
            if not self.scorePoint3 and self.point_swich3 and "3" in self.exper_score_ids:
                point3view = self.point3(top_true, gauze_dough_top, beaker_top, knead_doughpress_top, beaker_liquid_top,
                                         side_true, gauze_dough_side, beaker_side, knead_doughpress_side, beaker_liquid_side,
                                         front_true, gauze_dough_front, beaker_front, knead_doughpress_front, beaker_liquid_front)
                if point3view[0]:
                    self.scorePoint3 = True
                    if point3view[1] == 'top':
                        self.assignScore(3, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point3view[1] == 'side':
                        self.assignScore(3, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point3view[1] == 'front':
                        self.assignScore(3, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)
                    # plt.hist(self.point2_d,100)
                    # sns.kdeplot(self.point2_d, shade=True)
                    # plt.show()
                    # print(self.point2_d)

            # 4.充分揉挤至不再有白色物质从纱布中渗出来
            if not self.scorePoint4 and self.point_swich4 and "4" in self.exper_score_ids:
                point4view = self.point4(top_true, beaker_top, knead_doughpress_top, beaker_liquid_top,
                                         side_true, beaker_side, knead_doughpress_side, beaker_liquid_side,
                                         front_true, beaker_front, knead_doughpress_front, beaker_liquid_front)
                if point4view[0]:
                    self.scorePoint4 = True
                    if point4view[1] == 'top':
                        self.assignScore(4, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point4view[1] == 'side':
                        self.assignScore(4, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point4view[1] == 'front':
                        self.assignScore(4, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 5.打开纱布，展示黄白色的胶状物质
            if not self.scorePoint5 and self.point_swich5 and "5" in self.exper_score_ids:
                point5view = self.point5(top_true, gauze_top, gelatinoid_top,
                                         side_true, gauze_side, gelatinoid_side,
                                         front_true, gauze_front, gelatinoid_front)
                if point5view[0]:
                    self.scorePoint5 = True
                    if point5view[1] == 'top':
                        self.assignScore(5, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point5view[1] == 'side':
                        self.assignScore(5, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point5view[1] == 'front':
                        self.assignScore(5, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 6.用滴管吸取适量乳白色液体于试管中
            if not self.scorePoint6 and self.point_swich6 and "6" in self.exper_score_ids:
                point6view = self.point6(top_true,dropper_top, dropper_liquid_top, tube_top, tube_liquid_top,
                                         side_true, dropper_side, dropper_liquid_side, tube_side, tube_liquid_side,
                                         front_true, dropper_front, dropper_liquid_front, tube_front, tube_liquid_front)
                if point6view[0]:
                    self.scorePoint6 = True
                    if point6view[1] == 'top':
                        self.assignScore(6, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point6view[1] == 'side':
                        self.assignScore(6, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point6view[1] == 'front':
                        self.assignScore(6, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 7.如果取的量超过试管容积的1/3不得分
            if not self.scorePoint7 and self.point_swich7 and "7" in self.exper_score_ids:
                point7view = self.point7(top_true, dropper_top, tube_top, tube_end_top, tube_top_top, liquid_level_top, tube_liquid_top,
                                         side_true, dropper_side, tube_side, tube_end_side, tube_top_side, liquid_level_side, tube_liquid_side,
                                         front_true, dropper_front, tube_front, tube_end_front, tube_top_front, liquid_level_front, tube_liquid_front)
                if point7view[0]:
                    self.scorePoint7 = True
                    if point7view[1] == 'top':
                        self.assignScore(7, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point7view[1] == 'side':
                        self.assignScore(7, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point7view[1] == 'front':
                        self.assignScore(7, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 8.滴加碘液得分，滴加红墨水不得分
            if not self.scorePoint8 and self.point_swich8 and "8" in self.exper_score_ids:
                point8view = self.point8(top_true, dropper_top, dropper_liquid_top, tube_top, tube_liquid_top,
                                         side_true, dropper_side, dropper_liquid_side, tube_side, tube_liquid_side,
                                         front_true, dropper_front, dropper_liquid_front, tube_front, tube_liquid_front)
                if point8view[0]:
                    self.scorePoint8 = True
                    if point8view[1] == 'top':
                        self.assignScore(8, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point8view[1] == 'side':
                        self.assignScore(8, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point8view[1] == 'front':
                        self.assignScore(8, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

                # self.all_canvas_drow(parallel_gather)  # 绘制画布
                # self.show_process(canvas)

            # 9.充分震荡摇匀试管
            if not self.scorePoint9 and self.point_swich9 and "9" in self.exper_score_ids:
                point9view = self.point9(top_true, dropper_top, dropper_liquid_top, tube_top, volatile_liquid_top, tube_liquid_top,
                                         side_true, dropper_side, dropper_liquid_side, tube_side, volatile_liquid_side, tube_liquid_side,
                                         front_true, dropper_front, dropper_liquid_front, tube_front, volatile_liquid_front, tube_liquid_front)
                if point9view[0]:
                    self.scorePoint9 = True
                    if point9view[1] == 'top':
                        self.assignScore(9, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point9view[1] == 'side':
                        self.assignScore(9, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point9view[1] == 'front':
                        self.assignScore(9, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)
                    # sns.set()
                    # plt.plot(self.point2_d)
                    # a=sns.kdeplot(self.point2_d, shade=True)
                    # plt.show(a)
                    # print(self.point2_d)

            # 10.液体变蓝色
            if not self.scorePoint10 and self.point_swich10 and "10" in self.exper_score_ids:
                point10view = self.point10(top_true, dropper_top, dropper_liquid_top, tube_top, tube_liquid_top,
                                           side_true, dropper_side, dropper_liquid_side, tube_side, tube_liquid_side,
                                           front_true, dropper_front, dropper_liquid_front, tube_front, tube_liquid_front)
                if point10view[0]:
                    self.scorePoint10 = True
                    if point10view[1] == 'top':
                        self.assignScore(10, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point10view[1] == 'side':
                        self.assignScore(10, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point10view[1] == 'front':
                        self.assignScore(10, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 11.取花生、小麦种子各一粒
            if not self.scorePoint11 and self.point_swich11 and "11" in self.exper_score_ids:
                point11view = self.point11(top_true, tweezers_top, tweezers_top_top, peanut_top, wheat_top,
                                           side_true, tweezers_side, tweezers_top_side, peanut_top, wheat_top,
                                           front_true, tweezers_front, tweezers_top_front, peanut_top, wheat_top)
                if point11view[0]:
                    self.scorePoint11 = True
                    if point11view[1] == 'top':
                        self.assignScore(11, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point11view[1] == 'side':
                        self.assignScore(11, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point11view[1] == 'front':
                        self.assignScore(11, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 12.用单面刀片纵向切开
            if not self.scorePoint12 and self.point_swich12 and "12" in self.exper_score_ids:
                point12view = self.point12(top_true, hand_blade_top, seed_top,
                                           side_true, hand_blade_side, seed_side,
                                           front_true, hand_blade_front, seed_front)
                if point12view[0]:
                    self.scorePoint12 = True
                    if point12view[1] == 'top':
                        self.assignScore(12, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point12view[1] == 'side':
                        self.assignScore(12, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point12view[1] == 'front':
                        self.assignScore(12, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 13.在白纸上A区域挤压花生种子
            if not self.scorePoint13 and self.point_swich13 and "13" in self.exper_score_ids:
                point13view = self.point13(top_true, white_paper_top, press_top, seed_top,
                                           side_true, white_paper_side, press_side, seed_side,
                                           front_true, white_paper_front, press_front, seed_front)
                if point13view[0]:
                    self.scorePoint13 = True
                    if point13view[1] == 'top':
                        self.assignScore(13, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point13view[1] == 'side':
                        self.assignScore(13, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point13view[1] == 'front':
                        self.assignScore(13, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 14.在白纸上B区域挤压小麦种子
            if not self.scorePoint14 and self.point_swich14 and "14" in self.exper_score_ids:
                point14view = self.point14(top_true, white_paper_top, press_top, seed_top,
                                           side_true, white_paper_side, press_side, seed_side,
                                           front_true, white_paper_front, press_front, seed_front)
                if point14view[0]:
                    self.scorePoint14 = True
                    if point14view[1] == 'top':
                        self.assignScore(14, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point14view[1] == 'side':
                        self.assignScore(14, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point14view[1] == 'front':
                        self.assignScore(14, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 15.记录白纸上哪片区域有油脂的斑点
            if not self.scorePoint15 and self.point_swich15 and "15" in self.exper_score_ids:
                point15view = self.point15(top_true, white_paper_top, grease_top,
                                           side_true, white_paper_side, grease_side,
                                           front_true, white_paper_front, grease_front)
                if point15view[0]:
                    self.scorePoint15 = True
                    if point15view[1] == 'top':
                        self.assignScore(15, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point15view[1] == 'side':
                        self.assignScore(15, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point15view[1] == 'front':
                        self.assignScore(15, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

            # 16.将用过的实验材料放入废料槽中，其它实验用品归位，清洁桌面，举手示意实验完毕
            if not self.scorePoint16 and self.point_swich16 and "16" in self.exper_score_ids:
                point16view = self.point16(top_true, clean_top, equipments_top,
                                           side_true, clean_side,
                                           front_true, clean_front)
                if point16view[0]:
                    self.scorePoint16 = True
                    if point16view[1] == 'top':
                        self.assignScore(16, self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top)
                    elif point16view[1] == 'side':
                        self.assignScore(16, self.frame_side, self.time_side, self.objects_side, self.preds_side, self.num_frame_side)
                    elif point16view[1] == 'front':
                        self.assignScore(16, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front)

    def all_estimate_experiment_ing(self, wire_connection_top):  # 判断是否已经完成一次实验操作  演示版用导线辅助判断
        if len(wire_connection_top) >= 2 and not self.experiment_ing and not self.first_end:  # 判断第一次实验开始连接器材
            self.experiment_ing = True  # 打开拆除器材的门

        elif len(wire_connection_top) >= 2 and not self.experiment_ing and self.first_end:  # 判断再次实验开始连接器材
            self.experiment_ing = True  # 打开再次做实验的门
            self.experiment_end = 0
            self.first_end = False  # 将本次实验重置为第一次实验

            self.scorePoint1 = False  # TODO 待做  针对每一个得分点创建单独的函数  重置得分点状态，得分情况，得分点初始化
            self.retracementScore(index=1)
            self.scorePoint2 = False
            self.retracementScore(index=2)
            self.scorePoint3 = False
            self.retracementScore(index=3)
            self.scorePoint4 = False
            self.retracementScore(index=4)
            self.scorePoint5 = False
            self.retracementScore(index=5)
            self.scorePoint6 = False
            self.retracementScore(index=6)
            self.scorePoint7 = False
            self.retracementScore(index=7)
            self.scorePoint8 = False
            self.retracementScore(index=8)
            self.scorePoint9 = False
            self.retracementScore(index=9)
            self.scorePoint10 = False
            self.retracementScore(index=10)
            self.scorePoint11 = False
            self.retracementScore(index=11)
            self.scorePoint12 = False
            self.retracementScore(index=12)
            self.scorePoint13 = False
            self.retracementScore(index=13)
            self.scorePoint14 = False
            self.retracementScore(index=14)
            self.scorePoint15 = False
            self.retracementScore(index=15)
            self.scorePoint16 = False
            self.retracementScore(index=16)

        elif len(wire_connection_top) == 0 and self.experiment_ing:  # 判断拆除器材
            self.experiment_end += 1
            if self.experiment_end > 100:
                self.experiment_ing = False
                self.first_end = True  # 打开再次做实验的门

    def all_replace_gather_free(self, gather, free):
        list(gather[0].values())[0]['equ'] = list(free[0].values())[0]['equ']
        list(gather[0].values())[0]['post'] = list(free[0].values())[0]['post']
        list(gather[0].values())[0]['frequency'] = list(free[0].values())[0]['frequency']
        list(gather[-1].values())[0]['equ'] = list(free[-1].values())[0]['equ']
        list(gather[-1].values())[0]['post'] = list(free[-1].values())[0]['post']
        list(gather[-1].values())[0]['frequency'] = list(free[-1].values())[0]['frequency']

    def all_canvas_creation(self):  # 创建画布
        self.equ_name = ['power', 'switch', 'ammeter', 'slide', 'fixed', 'voltmeter']
        self.equ_end = []
        self.equ_close = [(0, 0, 255), (0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]
        self.canvas = np.zeros((self.h_top, self.w_top, 3), dtype="uint8")

    def all_canvas_drow(self, parallel_gather):  # 绘制画布
        line = []
        font = cv2.FONT_HERSHEY_SIMPLEX
        # for parallel_gather1 in parallel_route:
        for terminals in parallel_gather:
            index = self.equ_name.index(list(terminals.keys())[0].split('_')[0])
            name_equ = list(terminals.keys())[0].split('_')[0]
            name_post = list(terminals.keys())[0]

            if name_equ not in self.equ_end or name_equ == 'power':
                equ_box = list(terminals.values())[0]['equ']
                cv2.rectangle(self.canvas, (int(equ_box[0]), int(equ_box[1])), (int(equ_box[2]), int(equ_box[3])), self.equ_close[index], 3)
                cv2.putText(self.canvas, name_equ, (int(equ_box[0]), int(equ_box[1]) + 50), font, 1, (255, 255, 255), 1)
                self.equ_end.append(name_equ)
            if name_post not in self.equ_end or name_post == 'fixed_red':
                equ_post = list(terminals.values())[0]['post']
                cv2.rectangle(self.canvas, (int(equ_post[0]), int(equ_post[1])), (int(equ_post[2]), int(equ_post[3])), self.equ_close[index], 3)
                self.equ_end.append(name_post)
                line.append(center_point(equ_post))
            if len(line) == 2:
                cv2.line(self.canvas, (int(line[0][0]), int(line[0][1])), (int(line[1][0]), int(line[1][1])), (255, 255, 255), 3)  # 9

    def all_reorganization_frame(self, frame_num, frame1, frame2, frame3, frame4):
        """
        frames:需要合成图片的集合，frame的个数是需要合成的图片个数，frame的序列是摆放的位置
        """
        if frame_num == 2:
            pass

        elif frame_num == 3:
            pass

    def all_point_swich(self, flour_top, dough_top, gelatinoid_top, seed_front,
                        dropper_front, dropper_iodine_solution_front, dropper_red_ink_front,
                        press_front, gauze_dough_front, hand_blade_front, knead_doughpress_front,
                        beaker_starch_front, clean_top):
        if flour_top.shape[0] != 0:  # 面粉
            self.point_swich1 = True
            self.point_swich2 = True
            self.point_swich3 = True
            self.point_swich4 = True

        if beaker_starch_front.shape[0] != 0:  # 烧杯淀粉溶液
            self.point_swich5 = True
            self.point_swich6 = True
            self.point_swich7 = True
            self.point_swich8 = True
            self.point_swich9 = True
            self.point_swich10 = True

        if seed_front.shape[0] != 0:  # 花生 or 小麦
            self.point_swich11 = True
            self.point_swich12 = True
            self.point_swich13 = True
            self.point_swich14 = True
            self.point_swich15 = True
            self.point_swich16 = True

    # 1.用药匙取适量面粉，加清水和成面团
    def point1(self, top_true, flour_top, dough_top, dropper_top, dropper_water_top, medicine_spoon_top, medicine_spoon_top_top,
               side_true, flour_side, dough_side, dropper_side, dropper_water_side, medicine_spoon_side, medicine_spoon_top_side,
               front_true, flour_front, dough_front, dropper_front, dropper_water_front, medicine_spoon_front, medicine_spoon_top_front):
        """
            简化版：面团
            晋级版：  1.药匙+药匙头+面粉
                    2.面粉+胶头滴管+胶头滴管清水
                    3.面团
        """
        # top
        if top_true and dough_top.shape[0] != 0:  #
            self.flag1_inertance_top += 1
            if self.flag1_inertance_top > 10:
                return [True, 'top']

        # side
        if side_true and dough_side.shape[0] != 0:
            self.flag1_inertance_side += 1
            if self.flag1_inertance_side > 10:
                return [True, 'side']

        # front
        if front_true and dough_front.shape[0] != 0:
            self.flag1_inertance_front += 1
            if self.flag1_inertance_front > 10:
                return [True, 'front']

        return [False, '']

    # 2.用纱布包着面团
    def point2(self, top_true, dough_top, gauze_top, gauze_dough_top,
               side_true, dough_side, gauze_side, gauze_dough_side,
               front_true, dough_front, gauze_front, gauze_dough_front):
        """
            简化版：纱布包面团
            晋级版：  1.纱布+面团
                    3.纱布包面团
        """
        # top_true
        if top_true and gauze_dough_top.shape[0] != 0:
            self.flag2_inertance_top += 1
            if self.flag2_inertance_top > 15:
                return [True, 'top']

        if side_true and gauze_dough_side.shape[0] != 0:
            self.flag2_inertance_side += 1
            if self.flag2_inertance_side > 15:
                return [True, 'side']

        # front_true
        if front_true and gauze_dough_front.shape[0] != 0:
            self.flag2_inertance_front += 1
            if self.flag2_inertance_front > 15:
                return [True, 'front']

        return [False, '']

    # 3.用纱布包着面团放入盛有清水的烧杯中，轻轻揉挤
    def point3(self, top_true, gauze_dough_top, beaker_top, knead_doughpress_top, beaker_liquid_top,
               side_true, gauze_dough_side, beaker_side, knead_doughpress_side, beaker_liquid_side,
               front_true, gauze_dough_front, beaker_front, knead_doughpress_front, beaker_liquid_front):
        """
            简化版：揉搓面团
            晋级版：  1.纱布包面团+烧杯+烧杯清水
                    2.揉搓面团+烧杯+烧杯清水
                    3.揉搓面团+烧杯+烧杯淀粉溶液
        """
        # top
        if top_true and beaker_top.shape[0] != 0 and knead_doughpress_top.shape[0] != 0:
            beaker_top_box = beaker_top[0][:4]
            knead_doughpress_top_box = knead_doughpress_top[0][:4]
            # if iou(beaker_top_box, knead_doughpress_top_box) > 0:
            self.flag3_inertance_top += 1
            # if self.flag3_inertance_top > 5:
            return [True, 'top']

        # side
        if side_true and beaker_side.shape[0] != 0 and knead_doughpress_side.shape[0] != 0:
            beaker_side_box = beaker_side[0][:4]
            knead_doughpress_side_box = knead_doughpress_side[0][:4]
            # if iou(beaker_side_box, knead_doughpress_side_box) > 0:
            self.flag3_inertance_side += 1
            # if self.flag3_inertance_side > 5:
            return [True, 'side']

        # front
        if front_true and beaker_front.shape[0] != 0 and knead_doughpress_front.shape[0] != 0:
            beaker_front_box = beaker_front[0][:4]
            knead_doughpress_front_box = knead_doughpress_front[0][:4]
            # if iou(beaker_front_box, knead_doughpress_front_box) > 0:
            self.flag3_inertance_front += 1
            # if self.flag3_inertance_front > 5:
            return [True, 'front']

        return [False, '']

    # 4.充分揉挤至不再有白色物质从纱布中渗出来
    def point4(self, top_true, beaker_top, knead_doughpress_top, beaker_liquid_top,
               side_true, beaker_side, knead_doughpress_side, beaker_liquid_side,
               front_true, beaker_front, knead_doughpress_front, beaker_liquid_front):
        """
            简化版：揉搓面团+烧杯+烧杯淀粉溶液30s
            晋级版：  1.揉搓面团+烧杯+烧杯清水
                    2.揉搓面团+烧杯+烧杯淀粉溶液15s
                    3.揉搓面团+烧杯+烧杯淀粉溶液30s
        """
        # top_true
        if top_true and beaker_top.shape[0] != 0 and beaker_liquid_top.shape[0] != 0 and self.class_name[int(beaker_liquid_top[0][5])] == 'beaker_starch':
            beaker_top_box = beaker_top[0][:4]
            beaker_liquid_top_box = beaker_liquid_top[0][:4]
            if iou(beaker_top_box, beaker_liquid_top_box) > 0:
                self.flag4_inertance_top += 1
                if self.flag4_inertance_top > 50:
                    return [True, 'top']

        # side
        if side_true and beaker_side.shape[0] != 0 and beaker_liquid_side.shape[0] != 0 and self.class_name[int(beaker_liquid_side[0][5])] == 'beaker_starch':
            beaker_side_box = beaker_side[0][:4]
            beaker_liquid_side_box = beaker_liquid_side[0][:4]
            if iou(beaker_side_box, beaker_liquid_side_box) > 0:
                self.flag4_inertance_side += 1
                if self.flag4_inertance_side > 50:
                    return [True, 'side']

        # front_true
        if front_true and beaker_front.shape[0] != 0 and beaker_liquid_front.shape[0] != 0 and self.class_name[int(beaker_liquid_front[0][5])] == 'beaker_starch':
            beaker_front_box = beaker_front[0][:4]
            beaker_liquid_front_box = beaker_liquid_front[0][:4]
            if iou(beaker_front_box, beaker_liquid_front_box) > 0:
                self.flag4_inertance_front += 1
                if self.flag4_inertance_front > 50:
                    return [True, 'front']

        return [False, '']

    # 5.打开纱布，展示黄白色的胶状物质
    def point5(self, top_true, gauze_top, gelatinoid_top,
               side_true,gauze_side, gelatinoid_side,
               front_true,gauze_front, gelatinoid_front):
        """
            简化版：纱布+胶状物质
            晋级版： pass
        """
        # top
        if top_true and gauze_top.shape[0] != 0 and gelatinoid_top.shape[0] != 0:
            # gauze_top_box = gauze_top[0][:4]
            # gelatinoid_top_box = gelatinoid_top[0][:4]
            # if iou(gauze_top_box, gelatinoid_top_box) > 0:
            self.flag5_inertance_top += 1
            # if self.flag5_inertance_top > 1:
            return [True, 'top']

        # side
        if side_true and gauze_side.shape[0] != 0 and gelatinoid_side.shape[0] != 0:
            # gauze_side_box = gauze_side[0][:4]
            # gelatinoid_side_box = gelatinoid_side[0][:4]
            # if iou(gauze_side_box, gelatinoid_side_box) > 0:
            self.flag3_inertance_side += 1
            # if self.flag3_inertance_side > 1:
            return [True, 'side']

        # front
        if front_true and gauze_front.shape[0] != 0 and gelatinoid_front.shape[0] != 0:
            # gauze_front_box = gauze_front[0][:4]
            # gelatinoid_front_box = gelatinoid_front[0][:4]
            # if iou(gauze_front_box, gelatinoid_front_box) > 0:
            self.flag3_inertance_front += 1
            # if self.flag3_inertance_front > 1:
            return [True, 'front']

        return [False, '']

    # 6.用滴管吸取适量乳白色液体于试管中
    def point6(self,top_true, dropper_top, dropper_liquid_top, tube_top, tube_liquid_top,
               side_true,dropper_side, dropper_liquid_side, tube_side, tube_liquid_side,
               front_true,dropper_front, dropper_liquid_front, tube_front, tube_liquid_front):
        """
            简化版：试管+试管淀粉溶液
            晋级版：  1.胶头滴管+胶头滴管淀粉溶液+试管+试管没有液体
                    2.胶头滴管+or胶头滴管淀粉溶液+试管+试管淀粉溶液
                    3.没有胶头滴管+试管+试管淀粉溶液
        """
        if top_true and tube_top.shape[0] != 0 and tube_liquid_top.shape[0] != 0 and self.class_name[int(tube_liquid_top[0][5])] == 'tube_starch':
            # tube_top_box = tube_top[0][:4]
            # tube_liquid_top_box = tube_liquid_top[0][:4]
            # if iou(tube_top_box, tube_liquid_top_box) > 0:
            self.flag6_inertance_top += 1
            if self.flag6_inertance_top > 1:
                return [True, 'top']

        elif side_true and tube_side.shape[0] != 0 and tube_liquid_side.shape[0] != 0 and self.class_name[int(tube_liquid_side[0][5])] == 'tube_starch':
            # tube_side_box = tube_side[0][:4]
            # tube_liquid_side_box = tube_liquid_side[0][:4]
            # if iou(tube_side_box, tube_liquid_side_box) > 0:
            self.flag6_inertance_side += 1
            if self.flag6_inertance_side > 1:
                return [True, 'side']

        elif front_true and tube_front.shape[0] != 0 and tube_liquid_front.shape[0] != 0 and self.class_name[int(tube_liquid_front[0][5])] == 'tube_starch':
            # tube_front_box = tube_front[0][:4]
            # tube_liquid_front_box = tube_liquid_front[0][:4]
            # if iou(tube_front_box, tube_liquid_front_box) > 0:
            self.flag6_inertance_front += 1
            if self.flag6_inertance_front > 1:
                return [True, 'front']
        return [False, '']

    # 7.如果取的量超过试管容积的1/3不得分
    def point7(self, top_true,dropper_top, tube_top, tube_end_top, tube_top_top, liquid_level_top, tube_liquid_top,
               side_true,dropper_side, tube_side, tube_end_side, tube_top_side, liquid_level_side, tube_liquid_side,
               front_true,dropper_front, tube_front, tube_end_front, tube_top_front, liquid_level_front, tube_liquid_front):
        """
            简化版：没有胶头滴管+试管+试管口+试管尾+液面+试管淀粉溶液（或蓝色红色液体）
            方法2：简化版：试管+试管溶液（或蓝色红色液体）使用图片的占比
            晋级版：  pass
        """
        # top 没有胶头滴管，液面与试管与试管液体有交集，计算试管口到试管尾距离，液面到试管尾的距离，判断液体高度
        if top_true and dropper_top.shape[0] == 0:  # 没有胶头滴管
            if tube_top.shape[0] != 0 and tube_liquid_top.shape[0] != 0 and tube_end_top.shape[0] != 0 and tube_top_top.shape[0] != 0 and liquid_level_top.shape[0] != 0:
                tube_top_box = tube_top[0][:4]
                tube_liquid_top_box = tube_liquid_top[0][:4]
                liquid_level_top_box = liquid_level_top[0][:4]
                if iou(liquid_level_top_box, tube_top_box) > 0 and iou(liquid_level_top_box, tube_liquid_top_box) > 0:  # 液面与试管与试管液体有交集
                    # 计算试管口到试管尾距离，液面到试管尾的距离，
                    tube_h = distance_box(tube_top_top[0][:4], tube_end_top[0][:4])
                    tube_liquid_h = distance_box(liquid_level_top_box, tube_end_top[0][:4])
                    if tube_liquid_h / tube_h < 0.34:  # 判断液体高度
                        self.flag7_inertance_top += 1
                        if self.flag7_inertance_top > 3:
                            return [True, 'top']


        if top_true and tube_top.shape[0] != 0 and tube_liquid_top.shape[0] != 0 and (self.class_name[int(tube_liquid_top[0][5])] == 'tube_blue_liquid' or self.class_name[int(tube_liquid_top[0][5])] == 'tube_red_liquid'):
            tube_top_box = tube_top[0][:4]
            tube_liquid_top_box = tube_liquid_top[0][:4]
            if 0.33 > w_h_ratio(tube_top_box) and 0.33 > iou(tube_liquid_top_box, tube_top_box, True) > 0:  # 液面与试管与试管液体有交集
                self.flag7_inertance_top += 1
                if self.flag7_inertance_top > 1:
                    return [True, 'top']

        # side
        if side_true and dropper_side.shape[0] == 0:  # 没有胶头滴管
            if tube_side.shape[0] != 0 and tube_liquid_side.shape[0] != 0 and tube_end_side.shape[0] != 0 and tube_top_side.shape[0] != 0 and liquid_level_side.shape[0] != 0:
                tube_side_box = tube_side[0][:4]
                tube_liquid_side_box = tube_liquid_side[0][:4]
                liquid_level_side_box = liquid_level_side[0][:4]
                if iou(liquid_level_side_box, tube_side_box) > 0 and iou(liquid_level_side_box, tube_liquid_side_box) > 0:  # 液面与试管与试管液体有交集
                    # 计算试管口到试管尾距离，液面到试管尾的距离，
                    tube_h = distance_box(tube_top_side[0][:4], tube_end_side[0][:4])
                    tube_liquid_h = distance_box(liquid_level_side_box, tube_end_side[0][:4])
                    if tube_liquid_h / tube_h < 0.34:  # 判断液体高度
                        self.flag7_inertance_side += 1
                        if self.flag7_inertance_side > 3:
                            return [True, 'side']
        if side_true and tube_side.shape[0] != 0 and tube_liquid_side.shape[0] != 0 and (self.class_name[int(tube_liquid_side[0][5])] == 'tube_blue_liquid' or self.class_name[int(tube_liquid_side[0][5])] == 'tube_red_liquid'):
            tube_side_box = tube_side[0][:4]
            tube_liquid_side_box = tube_liquid_side[0][:4]
            if 0.33 > w_h_ratio(tube_side_box) and 0.33 > iou(tube_liquid_side_box, tube_side_box, True) > 0:  # 液面与试管与试管液体有交集
                self.flag7_inertance_side += 1
                if self.flag7_inertance_side > 1:
                    return [True, 'side']

        # front
        if front_true and dropper_front.shape[0] == 0:  # 没有胶头滴管
            if tube_front.shape[0] != 0 and tube_liquid_front.shape[0] != 0 and tube_end_front.shape[0] != 0 and tube_top_front.shape[0] != 0 and liquid_level_front.shape[0] != 0:
                tube_front_box = tube_front[0][:4]
                tube_liquid_front_box = tube_liquid_front[0][:4]
                liquid_level_front_box = liquid_level_front[0][:4]
                if iou(liquid_level_front_box, tube_front_box) > 0 and iou(liquid_level_front_box, tube_liquid_front_box) > 0:  # 液面与试管与试管液体有交集
                    # 计算试管口到试管尾距离，液面到试管尾的距离，
                    tube_h = distance_box(tube_top_front[0][:4], tube_end_front[0][:4])
                    tube_liquid_h = distance_box(liquid_level_front_box, tube_end_front[0][:4])
                    if tube_liquid_h / tube_h < 0.34:  # 判断液体高度
                        self.flag7_inertance_front += 1
                        if self.flag7_inertance_front > 3:
                            return [True, 'front']
        if front_true and tube_front.shape[0] != 0 and tube_liquid_front.shape[0] != 0 and (self.class_name[int(tube_liquid_front[0][5])] == 'tube_blue_liquid' or self.class_name[int(tube_liquid_front[0][5])] == 'tube_red_liquid'):
            tube_front_box = tube_front[0][:4]
            tube_liquid_front_box = tube_liquid_front[0][:4]
            if 0.33 > w_h_ratio(tube_front_box) and 0.33 > iou(tube_liquid_front_box, tube_front_box, True) > 0:  # 液面与试管与试管液体有交集
                self.flag7_inertance_front += 1
                if self.flag7_inertance_front > 1:
                    return [True, 'front']

        return [False, '']

    # 8.滴加碘液得分，滴加红墨水不得分
    def point8(self, top_true, dropper_top, dropper_liquid_top, tube_top, tube_liquid_top,
               side_true, dropper_side, dropper_liquid_side, tube_side, tube_liquid_side,
               front_true, dropper_front, dropper_liquid_front, tube_front, tube_liquid_front):
        """
            简化版：胶头滴管+胶头滴管碘液+试管+试管淀粉溶液  或 试管蓝色液体
            晋级版：  1.胶头滴管+胶头滴管碘液+试管+试管淀粉溶液
                    2.没有胶头滴管+试管+试管蓝色液
        """
        # top
        if top_true and tube_top.shape[0] != 0 and tube_liquid_top.shape[0] != 0 and self.class_name[int(tube_liquid_top[0][5])] == 'tube_blue_liquid':
            # tube_top_box = tube_top[0][:4]
            # tube_liquid_top_box = tube_liquid_top[0][:4]
            # if iou(tube_top_box, tube_liquid_top_box) > 0:
            self.flag8_inertance_top += 1
            if self.flag8_inertance_top > 1:
                return [True, 'top']
        elif top_true and tube_top.shape[0] != 0 and tube_liquid_top.shape[0] != 0 and self.class_name[int(tube_liquid_top[0][5])] == 'tube_starch' \
                and dropper_top.shape[0] != 0 and dropper_liquid_top.shape[0] != 0 and self.class_name[int(dropper_liquid_top[0][5])] == 'dropper_iodine_solution':
            # tube_top_box = tube_top[0][:4]
            # tube_liquid_top_box = tube_liquid_top[0][:4]
            # dropper_top_box = dropper_top[0][:4]
            # dropper_liquid_top_box = dropper_liquid_top[0][:4]
            # if iou(tube_top_box, tube_liquid_top_box) > 0 and iou(dropper_top_box, dropper_liquid_top_box) > 0:
            self.flag8_inertance_top += 1
            if self.flag8_inertance_top > 3:
                return [True, 'top']

        # side
        if side_true and tube_side.shape[0] != 0 and tube_liquid_side.shape[0] != 0 and self.class_name[int(tube_liquid_side[0][5])] == 'tube_blue_liquid':
            # tube_side_box = tube_side[0][:4]
            # tube_liquid_side_box = tube_liquid_side[0][:4]
            # if iou(tube_side_box, tube_liquid_side_box) > 0:
            self.flag8_inertance_side += 1
            if self.flag8_inertance_side > 3:
                return [True, 'side']
        elif side_true and tube_side.shape[0] != 0 and tube_liquid_side.shape[0] != 0 and self.class_name[int(tube_liquid_side[0][5])] == 'tube_starch' \
                and dropper_side.shape[0] != 0 and dropper_liquid_side.shape[0] != 0 and self.class_name[int(dropper_liquid_side[0][5])] == 'dropper_iodine_solution':
            # tube_side_box = tube_side[0][:4]
            # tube_liquid_side_box = tube_liquid_side[0][:4]
            # dropper_side_box = dropper_side[0][:4]
            # dropper_liquid_side_box = dropper_liquid_side[0][:4]
            # if iou(tube_side_box, tube_liquid_side_box) > 0 and iou(dropper_side_box, dropper_liquid_side_box) > 0:
            self.flag8_inertance_side += 1
            if self.flag8_inertance_side > 3:
                return [True, 'side']

        # front
        if front_true and tube_front.shape[0] != 0 and tube_liquid_front.shape[0] != 0 and self.class_name[int(tube_liquid_front[0][5])] == 'tube_blue_liquid':
            # tube_front_box = tube_front[0][:4]
            # tube_liquid_front_box = tube_liquid_front[0][:4]
            # if iou(tube_front_box, tube_liquid_front_box) > 0:
            self.flag8_inertance_front += 1
            if self.flag8_inertance_front > 3:
                return [True, 'front']
        elif front_true and tube_front.shape[0] != 0 and tube_liquid_front.shape[0] != 0 and self.class_name[int(tube_liquid_front[0][5])] == 'tube_starch' \
                and dropper_front.shape[0] != 0 and dropper_liquid_front.shape[0] != 0 and self.class_name[int(dropper_liquid_front[0][5])] == 'dropper_iodine_solution':
            # tube_front_box = tube_front[0][:4]
            # tube_liquid_front_box = tube_liquid_front[0][:4]
            # dropper_front_box = dropper_front[0][:4]
            # dropper_liquid_front_box = dropper_liquid_front[0][:4]
            # if iou(tube_front_box, tube_liquid_front_box) > 0 and iou(dropper_front_box, dropper_liquid_front_box) > 0:
            self.flag8_inertance_front += 1
            if self.flag8_inertance_front > 3:
                return [True, 'front']

        return [False, '']

    # 9.充分震荡摇匀试
    def point9(self, top_true, dropper_top, dropper_liquid_top, tube_top, volatile_liquid_top, tube_liquid_top,
               side_true, dropper_side, dropper_liquid_side, tube_side, volatile_liquid_side, tube_liquid_side,
               front_true, dropper_front, dropper_liquid_front, tube_front, volatile_liquid_front, tube_liquid_front):
        """
            简化版：试管+震荡液体
            晋级版：  1.胶头滴管+胶头滴管碘液+试管+试管淀粉溶液
                    2.试管+震荡液体
                    3.没有胶头滴管+试管+试管蓝色液
        """
        # top
        if top_true and tube_top.shape[0] != 0 and volatile_liquid_top.shape[0] != 0:
            # tube_top_box = tube_top[0][:4]
            # volatile_liquid_top_box = volatile_liquid_top[0][:4]
            # if iou(tube_top_box, volatile_liquid_top_box) > 0:
            self.flag9_inertance_top += 1
            if self.flag9_inertance_top > 3:
                return [True, 'top']

        # side
        if side_true and tube_side.shape[0] != 0 and volatile_liquid_side.shape[0] != 0:
            # tube_side_box = tube_side[0][:4]
            # volatile_liquid_side_box = volatile_liquid_side[0][:4]
            # if iou(tube_side_box, volatile_liquid_side_box) > 0:
            self.flag9_inertance_side += 1
            if self.flag9_inertance_side > 3:
                return [True, 'side']

        # front
        if front_true and tube_front.shape[0] != 0 and volatile_liquid_front.shape[0] != 0:
            # tube_front_box = tube_front[0][:4]
            # volatile_liquid_front_box = volatile_liquid_front[0][:4]
            # if iou(tube_front_box, volatile_liquid_front_box) > 0:
            self.flag9_inertance_front += 1
            if self.flag9_inertance_front > 3:
                return [True, 'front']

        return [False, '']

    # 10.液体变蓝色
    def point10(self, top_true, dropper_top, dropper_liquid_top, tube_top, tube_liquid_top,
                side_true, dropper_side, dropper_liquid_side, tube_side, tube_liquid_side,
                front_true, dropper_front, dropper_liquid_front, tube_front, tube_liquid_front):
        """
            简化版：没有胶头滴管+试管+试管蓝色液体
            晋级版：  1.胶头滴管+胶头滴管碘液+试管+试管淀粉溶液
                    2.没有胶头滴管+试管+试管蓝色液
        """
        # top
        if top_true and tube_top.shape[0] != 0 and tube_liquid_top.shape[0] != 0 and self.class_name[int(tube_liquid_top[0][5])] == 'tube_blue_liquid':
            # tube_top_box = tube_top[0][:4]
            # tube_liquid_top_box = tube_liquid_top[0][:4]
            # if iou(tube_top_box, tube_liquid_top_box) > 0:
            self.flag10_inertance_top += 1
            if self.flag10_inertance_top > 5:
                return [True, 'top']

        # side
        if side_true and tube_side.shape[0] != 0 and tube_liquid_side.shape[0] != 0 and self.class_name[int(tube_liquid_side[0][5])] == 'tube_blue_liquid':
            # tube_side_box = tube_side[0][:4]
            # tube_liquid_side_box = tube_liquid_side[0][:4]
            # if iou(tube_side_box, tube_liquid_side_box) > 0:
            self.flag10_inertance_side += 1
            if self.flag10_inertance_side > 5:
                return [True, 'side']

        # front
        if front_true and tube_front.shape[0] != 0 and tube_liquid_front.shape[0] != 0 and self.class_name[int(tube_liquid_front[0][5])] == 'tube_blue_liquid':
            # tube_front_box = tube_front[0][:4]
            # tube_liquid_front_box = tube_liquid_front[0][:4]
            # if iou(tube_front_box, tube_liquid_front_box) > 0:
            self.flag10_inertance_front += 1
            if self.flag10_inertance_front > 5:
                return [True, 'front']

        return [False, '']

    # 11.取花生、小麦种子各一粒
    def point11(self, top_true, tweezers_top, tweezers_top_top, peanut_top, wheat_top,
                side_true, tweezers_side, tweezers_top_side, peanut_side, wheat_side,
                front_true, tweezers_front, tweezers_top_front, peanut_front, wheat_front):
        """
            简化版：小麦+花生
            晋级版：  1.镊子+镊子头+小麦
                    2.镊子+镊子头+花生
                    3.小麦+花生
        """
        # top
        if top_true and peanut_top.shape[0] != 0 or wheat_top.shape[0] != 0:
            self.flag11_inertance_top += 1
            if self.flag11_inertance_top > 20:
                return [True, 'top']

        # side
        if side_true and peanut_side.shape[0] != 0 or wheat_side.shape[0] != 0:
            self.flag11_inertance_side += 1
            if self.flag11_inertance_side > 20:
                return [True, 'side']

        # front
        if front_true and peanut_front.shape[0] != 0 or wheat_front.shape[0] != 0:
            self.flag11_inertance_front += 1
            if self.flag11_inertance_front > 20:
                return [True, 'front']

        return [False, '']

    # 12.用单面刀片纵向切开
    def point12(self, top_true, hand_blade_top, seed_top,
                side_true, hand_blade_side, seed_side,
                front_true, hand_blade_front, seed_front):
        """
            简化版：纵切小麦+纵切花生
            晋级版：  1.手拿刀片+小麦  有交集
                    2.手拿刀片+花生  有交集
                    3.纵切小麦+纵切花生
        """
        # top
        if top_true and hand_blade_top.shape[0] != 0:
            self.flag12_inertance_top += 1
            if self.flag12_inertance_top > 5:
                return [True, 'top']

        # side
        if side_true and hand_blade_side.shape[0] != 0:
            self.flag12_inertance_side += 1
            if self.flag12_inertance_side > 5:
                return [True, 'side']

        # front
        if front_true and hand_blade_front.shape[0] != 0:
            self.flag12_inertance_front += 1
            if self.flag12_inertance_front > 5:
                return [True, 'front']

        return [False, '']

    # 13.在白纸上A区域挤压花生种子
    def point13(self, top_true, white_paper_top, press_top, seed_top,
                side_true, white_paper_side, press_side, seed_side,
                front_true, white_paper_front, press_front, seed_front):
        """
            简化版：白纸+按压
            晋级版：  1.纵切花生改变位置
                    2.按压
        """
        # top
        if top_true and white_paper_top.shape[0] != 0 and press_top.shape[0] != 0:
            self.flag13_inertance_top += 1
            # if self.flag13_inertance_top > 5:
            return [True, 'top']

        # side
        if side_true and white_paper_side.shape[0] != 0 and press_side.shape[0] != 0:
            self.flag13_inertance_side += 1
            # if self.flag13_inertance_side > 5:
            return [True, 'side']

        # front
        if front_true and white_paper_front.shape[0] != 0 and press_front.shape[0] != 0:
            self.flag13_inertance_front += 1
            # if self.flag13_inertance_front > 5:
            return [True, 'front']

        return [False, '']

    # 14.在白纸上B区域挤压小麦种子
    def point14(self, top_true, white_paper_top, press_top, seed_top,
                side_true, white_paper_side, press_side, seed_side,
                front_true, white_paper_front, press_front, seed_front):
        """
            简化版：白纸+按压    另一个区域
            晋级版：  1.纵切小麦改变位置
                    2.按压
        """
        # top
        if top_true and white_paper_top.shape[0] != 0 and press_top.shape[0] != 0:
            self.flag14_inertance_top += 1
            if self.flag14_inertance_top > 9:
                return [True, 'top']

        # side
        if side_true and white_paper_side.shape[0] != 0 and press_side.shape[0] != 0:
            self.flag14_inertance_side += 1
            if self.flag14_inertance_side > 9:
                return [True, 'side']

        # front
        if front_true and white_paper_front.shape[0] != 0 and press_front.shape[0] != 0:
            self.flag14_inertance_front += 1
            if self.flag14_inertance_front > 9:
                return [True, 'front']

        return [False, '']

    # 15.记录白纸上哪片区域有油脂的斑点
    def point15(self, top_true, white_paper_top, grease_top,
                side_true, white_paper_side, grease_side,
                front_true, white_paper_front, grease_front):
        """
            简化版：白纸+油脂印
            晋级版：  pass
        """
        # top
        if top_true and white_paper_top.shape[0] != 0 and grease_top.shape[0] != 0:
            self.flag15_inertance_top += 1
            # if self.flag15_inertance_top > 5:
            return [True, 'top']

        # side
        if side_true and white_paper_side.shape[0] != 0 and grease_side.shape[0] != 0:
            self.flag15_inertance_side += 1
            # if self.flag15_inertance_side > 5:
            return [True, 'side']

        # front
        if front_true and white_paper_front.shape[0] != 0 and grease_front.shape[0] != 0:
            self.flag15_inertance_front += 1
            # if self.flag15_inertance_front > 5:
            return [True, 'front']

        return [False, '']

    # 16.将用过的实验材料放入废料槽中，其它实验用品归位，清洁桌面，举手示意实验完毕
    def point16(self, top_true, clean_top, equipments_top,
                side_true,  clean_side,
                front_true, clean_front):
        """
            简化版：整理桌面  烧杯、试管、刀片、镊子、白纸、胶头滴管、纱布、碘液、红墨水、种子（包括切开的）
            晋级版：  pass
        """
        in_center_box = False

        if top_true:
            if self.center_box is not None:
                for items in equipments_top:
                    item_box = items[:4]
                    if iou(item_box, self.center_box) > 0:
                        in_center_box = True
                        break

            if not in_center_box or clean_top.shape[0] != 0:
                # print('clean_top', clean_top)
                self.flag16_inertance_top += 1
                # print('equipments_top', equipments_top)
                if self.flag16_inertance_top > 25:
                    return [True, 'top']
        elif side_true and clean_side.shape[0] != 0:
            return [True, 'side']
        elif front_true and clean_front.shape[0] != 0:
            return [True, 'front']
        return [False, '']
