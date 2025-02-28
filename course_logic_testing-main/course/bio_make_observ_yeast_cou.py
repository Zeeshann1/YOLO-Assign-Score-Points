#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : j.
# @Time    : 2022/4/15 15:32
# @File    : bio_make_observ_yeast_cou.py

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


# from .a_score import SCORE
# from config import experimental_site_top as est
# from config import experimental_site_front as esf
# from config import experimental_site_front as ess


class BIO_make_observ_yeast(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(BIO_make_observ_yeast, self).__init__(*args, **kwargs)
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
        self.scorePoint10 = False
        self.scorePoint11 = False
        self.scorePoint12 = False
        self.scorePoint13 = False
        self.scorePoint14 = False
        self.scorePoint15 = False
        self.scorePoint16 = False
        self.scorePoint17 = False
        self.scorePoint18 = False

        # 时长标记
        self.flagtime1 = 0.
        self.flagtime1_2 = 0.
        self.flagtime2 = 0.
        self.flagtime2_2 = 0.
        self.flagtime2_2_1 = 0.
        self.flagtime2_2_2 = 0.
        self.flagtime3 = 0.
        self.flagtime3_2 = 0.
        self.flagtime4 = 0.
        self.flagtime4_2 = 0.
        self.flagtime5 = 0.
        self.flagtime5_2 = 0.
        self.flagtime6 = 0.
        self.flagtime6_2 = 0.
        self.flagtime7 = 0.
        self.flagtime7_2 = 0.
        self.flagtime8 = 0.
        self.flagtime8_2 = 0.

        # 次数标记
        self.num1 = 0
        self.num2 = 0
        self.num2_f = 0
        self.num2_s = 0
        self.num3 = 0
        self.num3_f = 0
        self.num3_s = 0
        self.num4 = 0
        self.num5 = 0
        self.num6 = 0
        self.num7 = 0
        self.num8 = 0
        self.num9 = 0
        self.num10 = 0
        self.num11 = 0
        self.num12 = 0
        self.num13 = 0
        self.num14 = 0
        self.num15 = 0
        self.num16 = 0
        self.num17 = 0

        self.clearn_f_num = 0
        self.clearn_time = 0.
        self.clearn_desk_info = []

        self.scoreframe2 = 0
        self.scoreframe3 = 0
        self.scoreframe3_2 = 0
        self.scoreframe4 = 0

        self.set_center_box = False  # 设置中心操作区域

        # 实验标志
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.flag3a = False
        self.flag3b = False
        self.flag3c = False
        self.flag4 = False
        self.flag4a = False
        self.flag4b = False
        self.flag4c = False
        self.flag5 = False
        self.flag6 = False
        self.flag7 = False
        self.flag8 = False
        self.flag9 = False
        self.flag10 = False
        self.flag11 = False
        self.flag12 = False
        self.flag13 = False
        self.flag14 = False
        self.flag15 = False
        self.flag16 = False

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
        # if not self.set_center_box:
        #     self.setCenterBox(self.front_preds[0].device, est, esf)  # 设置操作中心区域

        # *-------------------------------------------------* 以下为赋分逻辑部分
        """
            主要用前视角
        """
        beakers_front, yeast_lis_front, hands_front, clean_cloths_front, glass_slides_front, \
        glass_covers_front, tweezers_front, droppers_front, ab_papers_front, coarse_ads_front, fine_ads_front, \
        stages_front, reflectors_front, clean_glasss_front, drop_yeasts_front, cover_slides_front, \
        ad_fine_ads_front, ad_coarse_ads_front, ab_paper_ops_front, exchangers_front, sma_oblenses_front, \
        big_oblenses_front, tab_holders_front, heads_front, eyes_front, th_holes_front, clear_ims_front = self.preds_front

        beakers_side, yeast_lis_side, hands_side, clean_cloths_side, glass_slides_side, \
        glass_covers_side, tweezers_side, droppers_side, ab_papers_side, coarse_ads_side, fine_ads_side, \
        stages_side, reflectors_side, clean_glasss_side, drop_yeasts_side, cover_slides_side, \
        ad_fine_ads_side, ad_coarse_ads_side, ab_paper_ops_side, exchangers_side, sma_oblenses_side, \
        big_oblenses_side, tab_holders_side, heads_side, eyes_side, th_holes_side, clear_ims_side = self.preds_side

        beakers_top, yeast_lis_top, hands_top, clean_cloths_top, glass_slides_top, \
        glass_covers_top, tweezers_top, droppers_top, ab_papers_top, coarse_ads_top, fine_ads_top, \
        stages_top, reflectors_top, clean_glasss_top, drop_yeasts_top, cover_slides_top, \
        ad_fine_ads_top, ad_coarse_ads_top, ab_paper_ops_top, exchangers_top, sma_oblenses_top, \
        big_oblenses_top, tab_holders_top, heads_top, eyes_top, th_holes_top, clear_ims_top = self.preds_top

        try:
            # 1 擦拭载玻片和盖玻片
            if not self.scorePoint1:
                info = self.clean_glass_func(1, hands_front, hands_side, clean_cloths_front, clean_cloths_side,
                                             glass_slides_front, glass_slides_side, clean_glasss_front,
                                             clean_glasss_side)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 2 用滴管将酵母菌滴在载玻片中央
            if not self.scorePoint2:
                info = self.drop_yeast_func(2, hands_side, droppers_front, glass_slides_front, drop_yeasts_front,
                                            hands_side, droppers_side, glass_slides_side, drop_yeasts_side)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 3 用镊子夹住盖玻片一侧,让盖玻片另一侧先接触酵母菌培养液,再缓缓放平,避免盖玻片下有气泡
            if not self.scorePoint3:
                info = self.opera_cover_func(3, hands_front, glass_slides_front, glass_covers_front, tweezers_front,
                                             cover_slides_front,
                                             hands_side, glass_slides_side, glass_covers_side, tweezers_side,
                                             cover_slides_side)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 4 正确使用显微镜
            #
            """
            得分点部分
            1.用一个较大的光圈对准通光孔
            2.转动转换器使低倍物镜对准通光孔，使视野中出现亮斑 
            3.转动粗准焦螺旋使镜筒上升
            4.将玻片标本放在载物台上使标本正对通光孔中央 
            5.用压片夹住标本
            6.顺时针转动粗准焦螺旋使镜筒下降,眼睛注视物镜防止压碎玻片标本
            7.左眼看目镜,逆时针转动粗准焦螺旋使镜筒缓缓上升直至看清细胞
            8.调节细准焦螺旋使图像更加清晰
            """
            """
            得分点1: 光圈与通光孔无法识别 默认得分;
            得分点2: 手与转换器有交集,小物镜中心点与反光镜中心点水平距离小于大物镜中心点与反光镜中心点的水平距离;
            得分点3: 手与粗准焦螺旋有交集;
            得分点4: 载玻片标本完全包含在载物台上;
            得分点5: 压片夹与载玻片标本有交集;
            得分点6: 手与粗准焦螺旋有交集且头部与转换器垂直方向距离在一个阈值内--说明注视物镜;
            得分点7: 手与粗准焦螺旋有交集
            得分点8: 手与细准焦螺旋有交集;

            """
            if not self.scorePoint4 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):

                # # 操作 反光镜+粗准焦螺旋+细准焦螺旋 给分
                # info = self.opera_microscope_func(4,hands_front,reflectors_front,coarse_ads_front,fine_ads_front,ad_coarse_ads_front,
                #                   ad_fine_ads_front, hands_side,reflectors_side,coarse_ads_side,fine_ads_side,
                #                   ad_coarse_ads_side,ad_fine_ads_side)
                # if info is not None:
                #     self.assignScore(*info)
                #     pass
                # pass

                info = self.opera_aperture(4, hands_front, exchangers_front, sma_oblenses_front, reflectors_front,
                                           big_oblenses_front, stages_front)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 5 转动转换器使低倍物镜对准通光孔，使视野中出现亮斑
            if not self.scorePoint5 and self.scorePoint4:
                info = self.opera_exchanger2(5, hands_front, exchangers_front, sma_oblenses_front, reflectors_front,
                                             big_oblenses_front, stages_front)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 6 转动粗准焦螺旋使镜筒上升
            if not self.scorePoint6 and self.scorePoint5:
                info = self.opera_coarse(6, hands_front, coarse_ads_front, ad_coarse_ads_front)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 7 将玻片标本放在载物台上使标本正对通光孔中央
            if not self.scorePoint7 and self.scorePoint5:
                info = self.opera_glass_slider(7, hands_side, glass_slides_side, stages_side)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 8 用压片夹住标本
            if not self.scorePoint8 and self.scorePoint5:
                info = self.opera_tabhold(8, hands_side, glass_slides_side, tab_holders_side, stages_side)
                if info is not None:
                    self.assignScore(*info)

            # 9 顺时针转动粗准焦螺旋使镜筒下降,眼睛注视物镜防止压碎玻片标本
            if not self.scorePoint9 and self.scorePoint5:
                info = self.opera_shun_coarse2(9, hands_front, coarse_ads_front, heads_front, eyes_front, stages_front,
                                               ad_coarse_ads_front)
                if info is not None:
                    self.assignScore(*info)

            # 10 左眼看目镜,逆时针转动粗准焦螺旋使镜筒缓缓上升直至看清细胞
            if not self.scorePoint10 and self.scorePoint5:
                info = self.opera_ni_coarse2(10, hands_front, coarse_ads_front, heads_front, eyes_front,
                                             ad_coarse_ads_front)
                if info is not None:
                    self.assignScore(*info)

            # 11 调节细准焦螺旋使图像更加清晰
            if not self.scorePoint11 and self.scorePoint5:
                info = self.opera_fine_ads(11, hands_front, fine_ads_front, ad_fine_ads_front)
                if info is not None:
                    self.assignScore(*info)

            # 12
            if not self.scorePoint12 and self.scorePoint1:
                info = self.clear_image1(12)
                if info is not None:
                    self.assignScore(*info)

            # # 13 # 实验结束后擦拭载玻片和盖玻片
            if not self.scorePoint13 and self.scorePoint5:
                info = self.clean_glass_func2(13, hands_front, hands_side, clean_cloths_front, clean_cloths_side,
                                              glass_slides_front, glass_slides_side, clean_glasss_front,
                                              clean_glasss_side)
                if info is not None:
                    self.assignScore(*info)
                    pass
                pass

            # 14 实验结束后能及时整理仪器
            side_items = [beakers_side, yeast_lis_side, clean_cloths_side, glass_slides_side, glass_covers_side,
                          tweezers_side, droppers_side, ab_papers_side, coarse_ads_side, fine_ads_side, stages_side,
                          reflectors_side]
            front_items = [beakers_front, yeast_lis_front, clean_cloths_front, glass_slides_front, glass_covers_front,
                           tweezers_front, droppers_front, ab_papers_front, coarse_ads_front, fine_ads_front,
                           stages_front,
                           reflectors_front]
            top_items = [beakers_top, yeast_lis_top, clean_cloths_top, glass_slides_top, glass_covers_top,
                         tweezers_top, droppers_top, ab_papers_top, coarse_ads_top, fine_ads_top, stages_top,
                         reflectors_top]
            if not self.scorePoint14 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):
                info = self.clearn_desk(14, top_items, front_items)
                if info is not None:
                    self.assignScore(*info)

            if self.scorePoint14 and len(self.score_list) != 14:
                if not self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):
                    self.retracementScore(14)
        except:
            logger.error(traceback.format_exc())

    # 1
    def clean_glass_func(self, score_index, hands_front, hands_side, clean_cloths_front, clean_cloths_side,
                         glass_slides_front, glass_slides_side, clean_glasss_front, clean_glasss_side):

        stat1 = False
        if hands_side.shape[0] != 0 and clean_cloths_side.shape[0] != 0:
            for clean_cloth_side in clean_cloths_side:
                for hand_side in hands_side:
                    if iou(hand_side[:4], clean_cloth_side[:4]) > 0:
                        stat1 = True
                        break
        if hands_front.shape[0] != 0 and clean_cloths_front.shape[0] != 0:
            for clean_cloth_front in clean_cloths_front:
                for hand_front in hands_front:
                    if iou(hand_front[:4], clean_cloth_front[:4]) > 0:
                        stat1 = True
                        break
        if clean_cloths_side.shape[0] != 0 and glass_slides_side.shape[0] != 0 and stat1:
            for clean_cloth_side in clean_cloths_side:
                for glass_slide_side in glass_slides_side:
                    if iou(clean_cloth_side[:4], glass_slide_side[:4]) > 0:
                        self.num1 += 1
                        # return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

        if clean_cloths_front.shape[0] != 0 and glass_slides_front.shape[0] != 0 and stat1:
            for clean_cloth_front in clean_cloths_front:
                for glass_slide_front in glass_slides_front:
                    if iou(clean_cloth_front[:4], glass_slide_front[:4]) > 0:
                        self.num1 += 1
                        # return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        # if clean_glasss_front.shape[0] != 0:
        #     self.num1 += 1
        # return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        # if clean_glasss_side.shape[0] != 0:
        #     self.num1 += 1
        # return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side
        if self.num1 >= 5:
            return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # 2 用滴管将酵母菌滴在载玻片中央
    def drop_yeast_func(self, score_index, hands_front, droppers_front, glass_slides_front, drop_yeasts_front,
                        hands_side, droppers_side, glass_slides_side, drop_yeasts_side):
        """
        前视角:
            1手与滴管有交集,
            2 滴管的底边
        :param score_index:
        :param hands_front:
        :param droppers_front:
        :param glass_slides_front:
        :param drop_yeasts_front:
        :param hands_side:
        :param droppers_side:
        :param glass_slides_side:
        :param drop_yeasts_side:
        :return:
        """
        stat1 = False
        if hands_front.shape[0] != 0 and droppers_front.shape[0] != 0:
            for dropper_front in droppers_front:
                for hand_front in hands_front:
                    if iou(hand_front[:4], dropper_front[:4]) > 0:
                        stat1 = True
                        break
        if hands_side.shape[0] != 0 and droppers_side.shape[0] != 0:
            for dropper_side in droppers_side:
                for hand_side in hands_side:
                    if iou(hand_side[:4], dropper_side[:4]) > 0:
                        stat1 = True
                        break
        if droppers_front.shape[0] != 0 and glass_slides_front.shape[0] != 0:
            if stat1:
                for glass_slide_front in glass_slides_front:
                    for dropper_front in droppers_front:
                        dropper_stat_v = glass_slide_front[:4][1] - dropper_front[:4][3] < \
                                         abs(glass_slide_front[:4][1] - glass_slide_front[:4][3])
                        dropper_stat_h = center_distance_h(dropper_front[:4], glass_slide_front[:4], abs_v=True) < \
                                         0.2 * abs(glass_slide_front[:4][0] - glass_slide_front[:4][2])
                        if dropper_stat_v and dropper_stat_h:
                            self.num2_f += 1
        if droppers_side.shape[0] != 0 and glass_slides_side.shape[0] != 0:
            if stat1:
                for glass_slide_side in glass_slides_side:
                    for dropper_side in droppers_side:
                        if iou(glass_slide_side[:4], dropper_side[:4]) > 0:
                            if center_distance_v(glass_slide_side[:4], dropper_side[:4], abs_v=True) < \
                                    0.6 * abs(glass_slide_side[:4][1] - glass_slide_side[:4][3]):
                                self.num2_s += 1
        if drop_yeasts_front.shape[0] != 0:
            self.num2_f += 1
            if self.num2_f >= 5:
                self.num2_f = 0
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        if drop_yeasts_side.shape[0] != 0:
            self.num2_s += 1
            if self.num2_s >= 5:
                self.num2_s = 0
                return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # # 3 用镊子夹住盖玻片一侧,让盖玻片另一侧先接触酵母菌培养液,再缓缓放平,避免盖玻片下有气泡
    def opera_cover_func(self, score_index, hands_front, glass_slides_front, glass_covers_front, tweezers_front,
                         cover_slides_front,
                         hands_side, glass_slides_side, glass_covers_side, tweezers_side, cover_slides_side):
        """
        1 手与镊子有交集
        2 在1下镊子与载玻片有交集,
        3 在2下 盖玻片与载玻片有交集 且 盖玻片与载玻片水平方向距离小于0.3倍载玻片的宽
        :param score_index:
        :param hands_front:
        :param glass_slides_front:
        :param glass_covers_front:
        :param tweezers_front:
        :param cover_slides_front:
        :param hands_side:
        :param glass_slides_side:
        :param glass_covers_side:
        :param tweezers_side:
        :param cover_slides_side:
        :return:
        """

        # 手与镊子有交集
        if hands_front.shape[0] != 0 and tweezers_front.shape[0] != 0:
            for hand_front in hands_front:
                for tweezer_front in tweezers_front:
                    if iou(hand_front[:4], tweezer_front[:4]) > 0:
                        self.flag3 = True

        if hands_side.shape[0] != 0 and tweezers_side.shape[0] != 0:
            for hand_side in hands_side:
                for tweezer_side in tweezers_side:
                    if iou(hand_side[:4], tweezer_side[:4]) > 0:
                        self.flag3 = True

        if tweezers_front.shape[0] != 0 and glass_slides_front.shape[0] != 0 and self.flag3:
            for tweezer_front in tweezers_front:
                for glass_slide_front in glass_slides_front:
                    if iou(glass_slide_front[:4], tweezer_front[:4]) > 0:
                        self.flag3a = True
        # 镊子与载玻片有交集
        if tweezers_side.shape[0] != 0 and glass_slides_side.shape[0] != 0 and self.flag3:
            for tweezer_side in tweezers_side:
                for glass_slide_side in glass_slides_side:
                    if iou(glass_slide_side[:4], tweezer_side[:4]) > 0:
                        self.flag3a = True
        if glass_covers_front.shape[0] != 0 and glass_slides_front.shape[0] != 0 and self.flag3a:
            for glass_cover_front in glass_covers_front:
                for glass_slide_front in glass_slides_front:
                    sli_cov_iou = iou(glass_cover_front[:4], glass_slide_front[:4]) > 0
                    sli_cov_pos = center_distance_h(glass_cover_front[:4], glass_slide_front[:4], abs_v=True) < \
                                  0.3 * (glass_slide_front[:4][0] - glass_slide_front[:4][2])
                    if sli_cov_iou and sli_cov_pos > 0:
                        self.flag3 = False
                        self.flag3a = False
                        self.num3_f += 1
        if glass_covers_side.shape[0] != 0 and glass_slides_side.shape[0] != 0 and self.flag3a:
            for glass_cover_side in glass_covers_side:
                for glass_slide_side in glass_slides_side:
                    sli_cov_iou = iou(glass_cover_side[:4], glass_slide_side[:4]) > 0
                    sli_cov_pos = center_distance_h(glass_cover_side[:4], glass_slide_side[:4], abs_v=True) < \
                                  0.3 * (glass_slide_side[:4][0] - glass_slide_side[:4][2])
                    if sli_cov_iou and sli_cov_pos:
                        self.flag3 = False
                        self.flag3a = False
                        self.num3_s += 1
        if cover_slides_front.shape[0] != 0:
            self.num3_f += 1

        if cover_slides_side.shape[0] != 0:
            self.num3_s += 1
        if self.num3_f > 3:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        if self.num3_s > 3:
            return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # 4
    # def opera_microscope_func(self,score_index,hands_front,reflectors_front,coarse_ads_front,fine_ads_front,
    #                           ad_coarse_ads_front, ad_fine_ads_front, hands_side,reflectors_side,coarse_ads_side,
    #                           fine_ads_side, ad_coarse_ads_side,ad_fine_ads_side):
    #     """
    #     删减版使用显微镜
    #     :param score_index:
    #     :param hands_front:
    #     :param reflectors_front:
    #     :param coarse_ads_front:
    #     :param fine_ads_front:
    #     :param ad_coarse_ads_front:
    #     :param ad_fine_ads_front:
    #     :param hands_side:
    #     :param reflectors_side:
    #     :param coarse_ads_side:
    #     :param fine_ads_side:
    #     :param ad_coarse_ads_side:
    #     :param ad_fine_ads_side:
    #     :return:
    #     """
    #     # 手与反光镜有交集
    #     if hands_front.shape[0] != 0 and reflectors_front.shape[0] != 0:
    #         for hand_front in hands_front:
    #             for reflector_front in reflectors_front:
    #                 if iou(hand_front[:4], reflector_front[:4]) > 0:
    #                     self.flag4 = True
    #     if hands_side.shape[0] != 0 and reflectors_side.shape[0] != 0:
    #         for hand_side in hands_side:
    #             for reflector_side in reflectors_side:
    #                 if iou(hand_side[:4], reflector_side[:4]) > 0:
    #                     self.flag4 = True
    #     # 手与粗准焦螺旋有交集
    #     if hands_front.shape[0] != 0 and coarse_ads_front.shape[0] != 0:
    #         for hand_front in hands_front:
    #             for coarse_ad_front in coarse_ads_front:
    #                 if iou(hand_front[:4], coarse_ad_front[:4]) > 0:
    #                     self.flag4a = True
    #     if hands_side.shape[0] != 0 and coarse_ads_side.shape[0] != 0:
    #         for hand_side in hands_side:
    #             for coarse_ad_side in coarse_ads_side:
    #                 if iou(hand_side[:4], coarse_ad_side[:4]) > 0:
    #                     self.flag4a = True
    #     if hands_front.shape[0] != 0 and fine_ads_front.shape[0] != 0:
    #         for hand_front in hands_front:
    #             for fine_ad_front in fine_ads_front:
    #                 if iou(hand_front[:4], fine_ad_front[:4])>0:
    #                     self.flag4b = True
    #     if hands_side.shape[0] != 0 and fine_ads_side.shape[0] != 0:
    #         for hand_side in hands_side:
    #             for fine_ad_side in fine_ads_side:
    #                 if iou(hand_side[:4], fine_ad_side[:4]) > 0:
    #                     self.flag4b = True
    #     if self.flag4 + self.flag4a + self.flag4b >1 :
    #         return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4.1 用一个较大的光圈对准通光孔
    # 4.1 4
    def opera_aperture(self, score_index, hands_front, exchangers_front, sma_oblenses_front, reflectors_front,
                       big_oblenses_front, stages_front):
        """
        用一个较大的光圈对准通光孔: 默认得分
        前视角
        因为看不见调节通光孔的动作(通光孔调节器在载物台下方) 默认手与载物台的交集面积大于载物台面积的 0.25倍
        :param score_index:
        :param hands_front:
        :param exchangers_front:
        :param sma_oblenses_front:
        :param reflectors_front:
        :param big_oblenses_front:
        :return:
        """
        if hands_front.shape[0] != 0 and stages_front.shape[0] != 0:
            # for hand_front in hands_front:
            #     for stage_front in stages_front:
            #         hand_sta_iou_area=iou(hand_front[:4], stage_front[:4])
            #         stage_area = box_area(stage_front[:4])
            #         if hand_sta_iou_area> 0.22*stage_area:
            #             self.num4 += 1
            self.num4 = 1
            if self.num4 >= 1:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4.2 5 转动转换器使低倍物镜对准通光孔，使视野中出现亮斑
    def opera_exchanger(self, score_index, hands_front, exchangers_front, sma_oblenses_front, reflectors_front,
                        big_oblenses_front, stages_front):
        """
        截取的图像是 手在转换器上,小物镜位置比大物镜位置低

        得分点2: 通光孔定义为 载物台中心
        手与转换器有交集面积大于转换器的0.5倍;
        小物镜中心点与载物台中心点水平距离小于大物镜中心点与载物台中心点的水平距离;
        且小物镜与载物台中心点水平距离在一个范围内
        :param score_index:
        :param hands_front:
        :param exchangers_front:
        :param sma_oblenses_front:
        :param reflectors_front:
        :param big_oblenses_front:
        :return:
        """
        if hands_front.shape[0] != 0 and exchangers_front.shape[0] != 0 and sma_oblenses_front.shape[0] != 0 and \
                reflectors_front.shape[0] != 0 and big_oblenses_front.shape[0] != 0 and stages_front.shape[0] != 0:

            stat1 = False
            stat2 = False
            for hand_front in hands_front:
                for exchanger_front in exchangers_front:
                    hand_echa_iou_area = iou(hand_front[:4], exchanger_front[:4])
                    excha_area = box_area(exchanger_front[:4])
                    if hand_echa_iou_area > 0.5 * excha_area:
                        # self.flag5 = True  # 手调整过转换器
                        stat2 = True
                        break
            # if self.flag5:
            # for stage_front in stages_front:
            #     sma_sta_pos = torch.tensor([[0.0],[0.0],[0.0],[0.0]])
            #     big_sta_pos = torch.tensor([[0.0],[0.0],[0.0],[0.0]])
            #     for sma_oblense_front in sma_oblenses_front:
            #         sma_sta_pos = center_distance_h(sma_oblense_front[:4],stage_front[:4],abs_v=True)
            #     for big_oblense_front in big_oblenses_front:
            #         big_sta_pos = center_distance_h(big_oblense_front[:4],stage_front[:4],abs_v=True)
            #     if sma_sta_pos < big_sta_pos:
            #         stat1 = True
            if stat2:
                for sma_oblense_front in sma_oblenses_front:
                    for big_oblense_front in big_oblenses_front:
                        if center_distance_v(sma_oblense_front[:4], big_oblense_front[:4]) > 0:
                            # print('小物镜位置在下面')
                            stat1 = True
            if stat1:
                # for stage_front in stages_front:
                #     for sma_oblense_front in sma_oblenses_front:
                #         sma_sta_pos = center_distance_h(sma_oblense_front[:4],stage_front[:4],abs_v=True)
                #         # print(f"小物镜与载物台中心点水平距离距离==={sma_sta_pos}")
                #         if sma_sta_pos < 20:
                #             self.num5 += 1
                self.num5 += 1
            if self.num5 >= 3:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    #
    def opera_exchanger2(self, score_index, hands_front, exchangers_front, sma_oblenses_front, reflectors_front,
                         big_oblenses_front, stages_front):
        """
        截取的图像是 手先与转换器有交集,之后小物镜位置在比大物镜位置低,截取的图片是 手与转换器是没有交集的(交集小于0.1倍转换器面积)
        :param score_index:
        :param hands_front:
        :param exchangers_front:
        :param sma_oblenses_front:
        :param reflectors_front:
        :param big_oblenses_front:
        :param stages_front:
        :return:
        """
        if hands_front.shape[0] != 0 and exchangers_front.shape[0] != 0 and sma_oblenses_front.shape[0] != 0 and \
                reflectors_front.shape[0] != 0 and big_oblenses_front.shape[0] != 0 and stages_front.shape[0] != 0:

            stat1 = False
            hand_stat = True
            for hand_front in hands_front:
                for exchanger_front in exchangers_front:
                    hand_echa_iou_area = iou(hand_front[:4], exchanger_front[:4])
                    excha_area = box_area(exchanger_front[:4])
                    if hand_echa_iou_area > 0.5 * excha_area:
                        self.flag5 = True  # 手调整过转换器
                        break
            if self.flag5:
                for hand_front in hands_front:
                    for exchanger_front in exchangers_front:
                        if iou(hand_front[:4], exchanger_front[:4]) > 0.1 * box_area(exchanger_front[:4]):
                            hand_stat = False
                if hand_stat:
                    for sma_oblense_front in sma_oblenses_front:
                        for big_oblense_front in big_oblenses_front:
                            if center_distance_v(sma_oblense_front[:4], big_oblense_front[:4]) > 0:
                                # print('小物镜位置在下面')
                                stat1 = True
            if stat1:
                self.num5 += 1
            if self.num5 >= 3:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        pass

    # 4.3 6 转动粗准焦螺旋使镜筒上升
    def opera_coarse(self, score_index, hands_front, coarse_ads_front, ad_coarse_ads_front):
        """
        手与粗准焦螺旋有交集,交集的面积大于粗准焦螺旋面积的0.8倍;

        :param score_index:
        :param hands_front:
        :param coarse_ads_front:
        :return:
        """
        if hands_front.shape[0] != 0 and coarse_ads_front.shape[0] != 0:
            for hand_front in hands_front:
                for coarse_ad_front in coarse_ads_front:
                    hand_coa_area = iou(hand_front[:4], coarse_ad_front[:4])
                    coa_area = box_area(coarse_ad_front)
                    if hand_coa_area > 0.8 * coa_area:
                        self.num6 += 1
            if ad_coarse_ads_front.shape[0]:
                # print("tiaojie cu cunzai66666666666666666666666")
                self.num6 += 1
            if self.num6 >= 3:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4.4 7将玻片标本放在载物台上使标本正对通光孔中央
    def opera_glass_slider(self, score_index, hands_side, glass_slides_side, stages_side):
        """
        侧视图:
        手与载玻片有交集;
        在该状态下 载物台有载玻片相交面积 大于载玻片本身面积的0.9倍
        :param score_index:
        :param hands_side:
        :param glass_slides_side:
        :param stages_side:
        :return:
        """
        if hands_side.shape[0] != 0 and glass_slides_side.shape[0] != 0 and stages_side.shape[0] != 0:
            stat1 = False
            for hand_side in hands_side:
                for glass_slide_side in glass_slides_side:
                    if iou(hand_side[:4], glass_slide_side[:4]) > 0:
                        stat1 = True  #
                        break
            if stat1:
                for stage_side in stages_side:
                    for glass_slide_side in glass_slides_side:
                        sta_gla_iou = iou(stage_side[:4], glass_slide_side[:4])
                        if sta_gla_iou > 0.9 * box_area(glass_slide_side[:4]):
                            self.num7 += 1
            if self.num7 >= 3:
                return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # 4.5 8用压片夹住标本
    def opera_tabhold(self, score_index, hands_side, glass_slides_side, tab_holders_side, stages_side):
        """
        逻辑:
        手与载玻片有交集,载玻片与压片夹有交集;载玻片完全在载物台上
        :param score_index:
        :param hands_side:
        :param glass_slides_side:
        :param tab_holders_side:
        :return:
        """
        if hands_side.shape[0] != 0 and glass_slides_side.shape[0] != 0 and tab_holders_side.shape[0] != 0:
            stat1 = False
            for hand_side in hands_side:
                for glass_slide_side in glass_slides_side:
                    if iou(hand_side[:4], glass_slide_side[:4]) > 0:
                        stat1 = True
            if stat1:
                for glass_slide_side in glass_slides_side:
                    for tab_holder_side in tab_holders_side:
                        if iou(glass_slide_side[:4], tab_holder_side[:4]):
                            self.num8 += 1
            if self.num8 >= 3:
                return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # 4.6  9 顺时针转动粗准焦螺旋使镜筒下降,眼睛注视物镜防止压碎玻片标本
    def opera_shun_coarse2(self, score_index, hands_front, coarse_ads_front, heads_front, eyes_front, stages_front,
                           ad_coarse_ads_front):
        """
        手与粗准焦螺旋有交集;
        在该状态下 头与载物台垂直方向距离在一个范围
        :param score_index:
        :param hands_front:
        :param coarse_ads_front:
        :param heads_front:
        :param eyes_front:
        :param stages_front:
        :param ad_coarse_ads_front:
        :return:
        """
        if hands_front.shape[0] != 0 and coarse_ads_front.shape[0] != 0 and heads_front.shape[0] != 0:
            stat1 = False
            for hand_front in hands_front:
                for coarse_ad_front in coarse_ads_front:
                    # if iou(hand_front[:4], coarse_ad_front[:4])>0:
                    #     stat1 = True
                    hand_coarse_area = iou(hand_front[:4], coarse_ad_front[:4])
                    coarse_area = box_area(coarse_ad_front)
                    if hand_coarse_area > 0.8 * coarse_area:
                        stat1 = True
            if ad_coarse_ads_front.shape[0] != 0:
                stat1 = True
            if stat1:
                for head_front in heads_front:
                    for stage_front in stages_front:
                        head_sta_v = center_distance_v(head_front[:4], stage_front[:4], abs_v=True)
                        # print(f"头与载物台垂直方向的距离: {head_sta_v}")
                        if head_sta_v < 150:
                            self.num9 += 1
            if self.num9 >= 3:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        pass

    # 4.7  10 左眼看目镜,逆时针转动粗准焦螺旋使镜筒缓缓上升直至看清细胞
    def opera_ni_coarse2(self, score_index, hands_front, coarse_ads_front, heads_front, eyes_front,
                         ad_coarse_ads_front):
        """
        手与粗准焦螺旋有交集,交集的面积大于粗准焦螺旋本身面积的0.8 倍
        :param score_index:
        :param hands_front:
        :param coarse_ads_front:
        :param heads_front:
        :param eyes_front:
        :param ad_coarse_ads_front:
        :return:
        """

        stat1 = False
        stat2 = True
        if hands_front.shape[0] != 0 and coarse_ads_front.shape[0] != 0:
            for hand_front in hands_front:
                for coarse_ad_front in coarse_ads_front:
                    hand_coarse_area = iou(hand_front[:4], coarse_ad_front[:4])
                    coarse_area = box_area(coarse_ad_front)
                    if hand_coarse_area > 0.8 * coarse_area:
                        stat1 = True
            if ad_coarse_ads_front.shape[0] != 0:
                stat1 = True
                # print('tiao cuzhunjiao biaoqian')
            if stat1 and heads_front.shape[0] == 0:
                # print('not check head')
                # stat1 = True
                self.num10 += 1
            elif stat1 and heads_front.shape[0] != 0:
                for head_front in heads_front:
                    for hand_front in hands_front:
                        if iou(head_front[:4], hand_front[:4]) > 0:
                            stat2 = False
                            # print('hand sucess')
                            continue
        if stat1 and stat2:
            self.num10 += 1
        if self.num10 >= 3:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4.8  11 调节细准焦螺旋使图像更加清晰
    def opera_fine_ads(self, score_index, hands_front, fine_ads_front, ad_fine_ads_front):
        """
        调节细准焦螺旋 用手与西准焦螺旋的iou来判断会有瑕疵;
        调整为用整体标签来判断

        :param score_index:
        :param hands_front:
        :param fine_ads_front:
        :param ad_fine_ads_front:
        :return:
        """
        # if hands_front.shape[0] != 0 and fine_ads_front.shape[0] != 0:
        #     for hand_front in hands_front:
        #         for fine_ad_front in fine_ads_front:
        #             hand_fine_area = iou(hand_front[:4], fine_ad_front[:4])
        #             fine_area = box_area(fine_ad_front)
        #             if hand_fine_area > 0.92*fine_area:
        #                 self.num11 += 1

        if ad_fine_ads_front.shape[0] != 0:
            self.num11 += 1
        if self.num11 >= 3:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 12
    def clear_image1(self, score_index):
        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    def clean_glass_func2(self, score_index, hands_front, hands_side, clean_cloths_front, clean_cloths_side,
                          glass_slides_front, glass_slides_side, clean_glasss_front, clean_glasss_side):
        stat1 = False
        if hands_side.shape[0] != 0 and clean_cloths_side.shape[0] != 0:
            for clean_cloth_side in clean_cloths_side:
                for hand_side in hands_side:
                    if iou(hand_side[:4], clean_cloth_side[:4]) > 0:
                        stat1 = True
                        break
        if hands_front.shape[0] != 0 and clean_cloths_front.shape[0] != 0:
            for clean_cloth_front in clean_cloths_front:
                for hand_front in hands_front:
                    if iou(hand_front[:4], clean_cloth_front[:4]) > 0:
                        stat1 = True
                        break
        if clean_cloths_side.shape[0] != 0 and glass_slides_side.shape[0] != 0 and stat1:
            for clean_cloth_side in clean_cloths_side:
                for glass_slide_side in glass_slides_side:
                    if iou(clean_cloth_side[:4], glass_slide_side[:4]) > 0:
                        self.num13 += 1

        if clean_cloths_front.shape[0] != 0 and glass_slides_front.shape[0] != 0 and stat1:
            for clean_cloth_front in clean_cloths_front:
                for glass_slide_front in glass_slides_front:
                    if iou(clean_cloth_front[:4], glass_slide_front[:4]) > 0:
                        self.num13 += 1

        if clean_glasss_front.shape[0] != 0:
            self.num13 += 1

        if clean_glasss_side.shape[0] != 0:
            self.num13 += 1
        if self.num13 >= 5:
            return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # 清理桌面
    def clearn_desk(self, score_index, top_items, front_items):
        # if self.desk_is_clearn(top_items, front_items):
        #     self.clearn_desk_info = [8, self.front_img0, self.front_preds, time.time()]
        #     self.clearn_time, _, flag = self.duration(self.clearn_time, 2)
        #     if flag:
        #         self.scorePoint4 = True
        #         self.assignScore(8, self.front_img0, self.front_preds)
        # else:
        #     self.clearn_time = 0

        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):  # 只看前视角
            self.clearn_desk_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                     self.preds_front,
                                     self.num_frame_front, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 0.5)
            if flag:
                self.clearn_f_num = 0
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        else:
            self.clearn_f_num = 0

    # def desk_is_clearn(self, top_items, front_items):
    #     for items in top_items:
    #         if items.shape[0] == 0:
    #             continue
    #         else:
    #             for item in items:
    #                 item_box = item[:4]
    #                 if pt_in_box(center_point(item_box), self.center_box_top) > 0:
    #                     return False
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
