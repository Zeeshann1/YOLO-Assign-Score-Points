#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : j.
# @Time    : 2022/6/30 9:15
# @File    : bio_observ_blood_cou.py

import random
import traceback
from .comm import *
from logger import logger

# from .a_score import SCORE
# from config import experimental_site_top as est
# from config import experimental_site_front as esf
# from config import experimental_site_front as ess

"""


"""


class BIO_observ_blood(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(BIO_observ_blood, self).__init__()
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
        self.num1_s = 0
        self.num1_f = 0
        self.num1_t = 0
        self.num1_slide = 0
        self.num2 = 0
        self.num2_t = 0
        self.num2_f = 0
        self.num2_s = 0
        self.num3 = 0
        self.num3_t = 0
        self.num3_f = 0
        self.num3_s = 0
        self.num4 = 0
        self.num4_t = 0
        self.num4_f = 0
        self.num5 = 0
        self.num5_s = 0
        self.num5_f_qm = 0
        self.num5_f_kb = 0
        self.num5_t = 0
        self.num6 = 0
        self.num6_t = 0
        self.num6_f = 0
        self.num6_f_big = 0
        self.num7 = 0
        self.num7_s = 0
        self.num7_f = 0
        self.num7_t = 0
        self.num8 = 0
        self.num8_s = 0
        self.num8_t = 0
        self.num8_f = 0
        self.num9 = 0
        self.num9_t = 0
        self.num9_f = 0
        self.num9_s = 0
        self.num10 = 0
        self.num10_t = 0
        self.num10_f = 0
        self.num10_s = 0
        self.num11 = 0
        self.num12 = 0
        self.num13 = 0
        self.num13_f = 0
        self.num13_t = 0
        self.num14 = 0
        self.num15 = 0
        self.num16 = 0
        self.num17 = 0

        self.clearn_f_num = 0
        self.clearn_time = 0.
        self.clearn_desk_info = []
        self.quxia_blood_info = []

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
        self.blood_stat = False
        # 实验配置参数
        self.hand_coa_front_re = 0.8  # 得分点6 前视角 手与粗准焦螺旋相交面积是粗准焦螺旋面积的0.8倍
        self.hand_coa_front_re10 = 0.8  # 得分点10 前视角 手与粗准焦螺旋相交面积是粗准焦螺旋面积的0.8倍

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
            1选取青霉永久装片得分，选取空白载玻片不得分
            2 选取显微镜得分，选取放大镜不得分
            3 转动转换器，使低倍物镜对准通光孔
            4 通过目镜或显示屏看到明亮的视野
            5 把装片正确固定在载物台上，装片正对通光孔
            6 转动粗准焦螺旋，使镜筒缓慢下降直至物镜接近装片为止
            7 正确调焦，能看到清晰的物像并圈出青霉
            8 描述青霉的形态特点，选A得1分，选B不得分
            9 实验结束，将装片取下，复原显微镜，将实验用品放回原处
            10 举手示意实验完毕，确认分数并签名;


        """
        reject_boxs_front, hands_front, mi_papers_front, blood_glas_front,  blank_glas_front, \
        coarse_ads_front, fine_ads_front, stages_front, reflectors_front, ad_fine_ads_front, \
        ad_coarse_ads_front, exchangers_front, yellow_obls_front, blue_obls_front, red_obls_front, \
        tab_holders_front, heads_front, th_holes_front, magnis_front, eyes_front = self.preds_front

        reject_boxs_side, hands_side, mi_papers_side, blood_glas_side, blank_glas_side, \
        coarse_ads_side, fine_ads_side, stages_side, reflectors_side, ad_fine_ads_side, \
        ad_coarse_ads_side, exchangers_side, yellow_obls_side, blue_obls_side, red_obls_side, \
        tab_holders_side, heads_side, th_holes_side, magnis_side, eyes_side = self.preds_side

        reject_boxs_top, hands_top, mi_papers_top, blood_glas_top, blank_glas_top, \
        coarse_ads_top, fine_ads_top, stages_top, reflectors_top, ad_fine_ads_top, \
        ad_coarse_ads_top, exchangers_top, yellow_obls_top,blue_obls_top, red_obls_top, \
        tab_holders_top, heads_top, th_holes_top, magnis_top, eyes_top = self.preds_top

        try:
            # 1 选取人血涂片标配得分，选取空白载玻片不得分
            if not self.scorePoint1:
                info = self.sele_slide(1, hands_front, blood_glas_front, blank_glas_front,hands_top, blood_glas_top,
                                       stages_top, hands_side, blood_glas_side, blank_glas_side,stages_side,blank_glas_top)
                if info is not None:
                    self.assignScore(*info)
                    pass

            # 记录载玻片在载物台上的帧数
            self.mark_num_slide(hands_front, blood_glas_front, blank_glas_front,hands_top, blood_glas_top, stages_top,
                       hands_side, blood_glas_side, blank_glas_side,stages_side,blank_glas_top)

            # 2 选取显微镜得分，选取放大镜不得分
            if not self.scorePoint2:
                info = self.sele_micro(2, hands_front, exchangers_front, yellow_obls_front, magnis_front, hands_top,
                                       stages_top, magnis_top)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 3 转动转换器，使低倍物镜对准通光孔
            if not self.scorePoint3 and self.scorePoint2:
                info = self.opera_exchanger2(3, hands_front, exchangers_front, yellow_obls_front, reflectors_front,
                                             blue_obls_front,red_obls_front, stages_front, hands_top, exchangers_top,
                                             yellow_obls_top, reflectors_top, blue_obls_top, stages_top)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 4 正确调节遮光器和反光镜
            if not self.scorePoint4:
                info = self.opera_sunshade_refle(4, hands_front, reflectors_front,)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 5 通过目镜或显示屏看到明亮的视野
            if not self.scorePoint5 and self.scorePoint2:
                info = self.observe_light(5, heads_front, coarse_ads_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 6 把装片正确固定在载物台上，装片正对通光孔
            if not self.scorePoint6:
                info = self.opera_blood_slider(6, hands_side, blood_glas_side, stages_side, tab_holders_side,
                                              blank_glas_side, blood_glas_top, stages_top)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 补充: 得分点六一直不出来, 以第七得分点来判定 得分点六判定已经出分
            if not self.scorePoint6 and self.scorePoint7:
                # if self.blood_stat:
                info = self.func_point5_re(6, hands_side, blood_glas_side, stages_side, tab_holders_side, blank_glas_side)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 7 侧看物镜,转动粗准焦螺旋，使镜筒缓慢下降直至物镜接近装片为止
            if not self.scorePoint7:
                info = self.near_blood_slider(7, hands_front, blood_glas_front, stages_front, coarse_ads_front,
                                             yellow_obls_front,red_obls_front,blue_obls_front, ad_coarse_ads_front,
                                             exchangers_front,hands_top,exchangers_top, ad_coarse_ads_top,
                                             ad_fine_ads_front,heads_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 由得分点7辅助判断得分点1
            if self.scorePoint7 and not self.scorePoint1:
                info = self.func_ponit1_re(1, red_obls_front, blue_obls_front, yellow_obls_front, hands_front,
                                           exchangers_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # # 麒麟--只取下载玻片的情况
            if not self.scorePoint11 and (self.scorePoint6 or self.scorePoint5):
                info = self.quxia_blood(11,stages_top,stages_side,blood_glas_top,blood_glas_side)

            # 8 正确使用粗准焦螺旋，使镜筒上升，直到看到清晰的物像为止
            if not self.scorePoint8 and self.scorePoint7:
                info = self.up_lenscone(8, hands_front, coarse_ads_front, heads_front, ad_coarse_ads_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 9 如果物像不清晰，正确使用细准焦螺旋，使看到物像更清晰
            if not self.scorePoint9 and self.scorePoint7:
                info = self.op_fine_ad(9, hands_front, fine_ads_front, heads_front, ad_fine_ads_front)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 10 移动标本能将白细胞放在视野中央
            if not self.scorePoint10 and self.scorePoint7:
                info = self.move_slide(10, hands_front, blood_glas_front,stages_front, stages_top, hands_top, blood_glas_top,
                                stages_side, hands_side, blood_glas_side)
                if info is not None:
                    self.assignScore(*info)
                pass

            # 11 实验结束，将装片取下，复原显微镜，将实验用品放回原处,举手示意实验完毕
            # if not self.scorePoint11:
            #
            #     pass
            # 11
            side_items = [coarse_ads_side, fine_ads_side, stages_side, reflectors_side]
            front_items = [coarse_ads_front, fine_ads_front, stages_front, reflectors_front,
                           exchangers_front]
            top_items = [coarse_ads_top, fine_ads_top, stages_top, reflectors_top,
                         exchangers_top]

            if not self.scorePoint11 and (self.scorePoint1 or self.scorePoint2 or self.scorePoint3):
                info = self.clearn_desk(11, top_items, front_items)
                if info is not None:
                    self.assignScore(*info)
            if self.scorePoint11 and len(self.score_list) != 11:
                if not self.quxia_blood_info and not self.desk_is_clearn([top_items, front_items],
                                                                        [self.center_area_top, self.center_area_front]):
                    self.retracementScore(11)
        except:
            logger.error(traceback.format_exc())

    # 记录载玻片在载物台上的帧数
    def mark_num_slide(self,hands_front, blood_glas_front, blank_glas_front,hands_top, blood_glas_top, stages_top,
                       hands_side, blood_glas_side, blank_glas_side,stages_side,blank_glas_top):

        if self.num1_slide < 50:
            #####记录青霉载玻片
            for stage_top in stages_top:
                for blood_gla_top in blood_glas_top:
                    if iou(stage_top[:4], blood_gla_top[:4]) > 0:
                        self.num1_slide += 1  # 载波片在载物台上标志
            for stage_side in stages_side:
                for blood_gla_side in blood_glas_side:
                    if iou(blood_gla_side[:4], stage_side[:4]) > 0.2 * box_area(blood_gla_side[:4]):
                        self.num1_slide += 1  # 载波片在载物台上标志
            ####记录空白载玻片

            ###### 记录 空白载玻片在载物台上#####
            if hands_top.shape[0] != 0 and blank_glas_top.shape[0] != 0 and stages_top.shape[0] != 0:
                for stage_top in stages_top:
                    for blank_gla_top in blank_glas_top:
                        if iou(blank_gla_top[:4], stage_top[:4]) > 0:
                            self.num1_slide += 1
            if hands_side.shape[0] != 0 and blank_glas_side.shape[0] != 0 and stages_side.shape[0] != 0:
                for stage_side in stages_side:
                    for blank_gla_side in blank_glas_side:
                        if iou(blank_gla_side[:4], stage_side[:4]) > 0.2 * box_area(blank_gla_side[:4]):
                            self.num1_slide += 1
            ######记录 空白载玻片在载物台上#####

    # 1
    def sele_slide(self, score_index, hands_front, blood_glas_front, blank_glas_front,hands_top, blood_glas_top,
                                       stages_top, hands_side, blood_glas_side, blank_glas_side,stages_side,blank_glas_top):
        if blood_glas_top.shape[0] != 0 and hands_top.shape[0] != 0:
            for blood_gla_top in blood_glas_top:
                if pt_in_polygon(center_point(blood_gla_top[:4]), self.center_area_top):
                    self.num1_t += 1

        if blood_glas_top.shape[0] != 0 and stages_top.shape[0] != 0:
            for stage_top in stages_top:
                for blood_gla_top in blood_glas_top:
                    if iou(stage_top[:4],blood_gla_top[:4])>0:
                        self.num1_t += 1
        if blood_glas_side.shape[0] != 0 and stages_side.shape[0] != 0:
            for stage_side in stages_side:
                for blood_gla_side in blood_glas_side:
                    if iou(blood_gla_side[:4], stage_side[:4]) >0.2*box_area(blood_gla_side[:4]):
                        self.num1_s += 1
        if blood_glas_front.shape[0] != 0:
            for blood_gla_front in blood_glas_front:
                if pt_in_polygon(center_point(blood_gla_front[:4]), self.center_area_front):
                    self.num1_f += 1
        if self.num1_t >= 10:
            return score_index,self.frame_top,self.time_top,self.objects_top,self.preds_top
        if self.num1_s >= 10:
            return score_index,self.frame_side,self.time_side,self.objects_side,self.preds_side
        if self.num1_f >= 8:
            return score_index,self.frame_front,self.time_front,self.objects_front,self.preds_front

    # 2
    def sele_micro(self,score_index, hands_front, exchangers_front, yellow_obls_front,magnis_front,hands_top,stages_top,magnis_top):
        if exchangers_front.shape[0] != 0 and hands_front.shape[0] !=0:
            stat1 = False
            for exchanger_front in exchangers_front:
                if pt_in_polygon(center_point(exchanger_front[:4]), self.center_area_front):
                    self.num2_f += 1
            for hand_front in hands_front:
                for exchanger_front in exchangers_front:
                    if iou(hand_front[:4], exchanger_front[:4])>0:
                        self.num2_f += 1
            if self.num2_f > 20:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        if stages_top.shape[0] != 0 and hands_top.shape[0] != 0:
            for stage_top in stages_top:
                if pt_in_polygon(center_point(stage_top[:4]), self.center_area_top):
                    self.num2_t += 1
            # for hand_top in hands_top:
            #     for stage_top in stages_top:
            #         if iou(stage_top[:4], hand_top[:4])>0:
            #             self.num2_t += 1
            if self.num2_t >= 20:
                return score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top
        pass

    # 3.0 转动转换器使低倍物镜对准通光孔
    def exchanger_opera(self, score_index, hands_front, exchangers_front, yellow_obls_front, reflectors_front,
                                             blue_obls_front, stages_front, hands_top, exchangers_top, yellow_obls_top, reflectors_top,
                                             blue_obls_top, stages_top):
        """
        截取的图像是 手在转换器上,小物镜位置比大物镜位置低

        得分点2: 通光孔定义为 载物台中心
        手与转换器有交集面积大于转换器的0.5倍;
        小物镜中心点与载物台中心点水平距离小于大物镜中心点与载物台中心点的水平距离;
        且小物镜与载物台中心点水平距离在一个范围内
        :param score_index:
        :param hands_front:
        :param exchangers_front:
        :param yellow_obls_front:
        :param reflectors_front:
        :param blue_obls_front:
        :return:
        """

        stat1 = False
        stat2 = False
        if hands_top.shape[0] != 0 and exchangers_top.shape[0] != 0:
            for hand_top in hands_top:
                for exchanger_top in exchangers_top:
                    hand_excha_iou_area = iou(hand_top[:4], exchanger_top[:4])
                    excha_area = box_area(exchanger_top[:4])
                    if hand_excha_iou_area > 0.35 * excha_area:
                        stat2 = True
                        break
        if stat2 and blue_obls_front.shape[0] != 0 and yellow_obls_front.shape[0] !=0:
            for yellow_obl_front in yellow_obls_front:
                max_y_box = self.max_y_box(blue_obls_front)
                if center_distance_v(yellow_obl_front[:4], max_y_box[:4]) > 0:
                    # print('小物镜位置在下面')
                    stat1 = True
                # for blue_obl_front in blue_obls_front:
                #     if center_distance_v(yellow_obl_front[:4], blue_obl_front[:4]) > 0:
                #         # print('小物镜位置在下面')
                #         stat1 = True
        if stat1:
            self.num3_f += 1
        if self.num3_f >= 2:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    def max_y_box(self, boxs):
        """
        返回boxs中 垂直方向只最大的box
        :param boxs:
        :return:
        """
        li = []
        for i,box in enumerate(boxs):
            li.append({"i":i,"y":center_point(box[:4])[1],"box":box})
        li = sorted(li,key=lambda da:da["y"])
        box = li[-1]["box"]
        return box

    # 3.1 转动转换器使低倍物镜对准通光孔
    def opera_exchanger2(self,score_index, hands_front, exchangers_front, yellow_obls_front, reflectors_front,
                                             blue_obls_front,red_obls_front, stages_front, hands_top, exchangers_top,
                                             yellow_obls_top, reflectors_top, blue_obls_top, stages_top):
        """
        截取的图像是 手先与转换器有交集,之后小物镜位置在比大物镜位置低,截取的图片是 手与转换器是没有交集的(交集小于0.1倍转换器面积)
        1手与转换器有交集面积大于转换器面积的0.5倍,说明调整了转换器;
        2 手与转换器交集面积小于0.1倍转换器面积,在该状态下,小物镜的位置要比大物镜的位置低;
        :param score_index:
        :param hands_front:
        :param exchangers_front:
        :param yellow_obls_front:
        :param reflectors_front:
        :param blue_obls_front:
        :param stages_front:
        :return:
        """
        stat1 = False
        stat2 = False
        hand_stat = True
        # top hand and excha iou
        if hands_top.shape[0] != 0 and exchangers_top.shape[0] != 0:
            for hand_top in hands_top:
                for exchanger_top in exchangers_top:
                    hand_excha_iou_area = iou(hand_top[:4], exchanger_top[:4])
                    excha_area = box_area(exchanger_top[:4])
                    if hand_excha_iou_area > 0.2 * excha_area:
                        stat2 = True
                        break
        # stat2 = True
        #   front hand and excha iou
        if stat2 and hands_front.shape[0] != 0 and exchangers_front.shape[0] != 0:
            # print('2222')
            for hand_front in hands_front:
                for exchanger_front in exchangers_front:
                    hand_excha_iou_area = iou(hand_front[:4], exchanger_front[:4])
                    excha_area = box_area(exchanger_front[:4])
                    # print(f'hand_excha_iou_area')
                    # print(hand_excha_iou_area)
                    # print(f'hand_excha_iou_area')
                    # print('excha_area')
                    # print(excha_area)
                    # print('excha_area')
                    if hand_excha_iou_area > 0.2 * excha_area:
                        self.flag3 = True
                        break
        if self.flag3 and hands_top.shape[0] != 0 and exchangers_top.shape[0] != 0:
            for hand_top in hands_top:
                for exchanger_top in exchangers_top:
                    if iou(hand_top[:4], exchanger_top[:4]) > 0.1 * box_area(
                            exchanger_top[:4]):
                        hand_stat = False
            pass
        if self.flag3 and hands_front.shape[0] != 0 and exchangers_front.shape[0] != 0:
            for hand_front in hands_front:
                for exchanger_front in exchangers_front:
                    if iou(hand_front[:4], exchanger_front[:4]) > 0.05 * box_area(
                            exchanger_front[:4]):
                        hand_stat = False
        # 手与hongse物镜没有交集
        if self.flag3 and hands_front.shape[0] != 0 and red_obls_front.shape[0] != 0:
            for hand_front in hands_front:
                for red_obl_front in red_obls_front:
                    if iou(hand_front[:4], red_obl_front[:4]) > 0.3*box_area(red_obl_front[:4]):
                        hand_stat = False
        # 手与黄色物镜没有交集
        if self.flag3 and hands_front.shape[0] != 0 and yellow_obls_front.shape[0] != 0:
            for hand_front in hands_front:
                for yellow_obl_front in yellow_obls_front:
                    if iou(hand_front[:4], yellow_obl_front[:4]) > 0.3 * box_area(yellow_obl_front[:4]):
                        hand_stat = False
        if self.flag3 and hand_stat:
            if yellow_obls_front.shape[0] != 0 and blue_obls_front.shape[0] != 0:
                for yellow_obl_front in yellow_obls_front:
                    max_y_box = self.max_y_box(blue_obls_front)
                    if center_distance_v(yellow_obl_front[:4], max_y_box[:4]) > 0:
                        stat1 = True
            if red_obls_front.shape[0] != 0 and blue_obls_front.shape[0] != 0:
                for red_obl_front in red_obls_front:
                    max_y_box = self.max_y_box(blue_obls_front)
                    if center_distance_v(red_obl_front[:4], max_y_box[:4]) > 0:
                        stat1 = True
            if red_obls_front.shape[0] != 0 and yellow_obls_front.shape[0] != 0:
                for red_obl_front in red_obls_front:
                    max_y_box = self.max_y_box(yellow_obls_front)
                    if center_distance_v(red_obl_front[:4], max_y_box[:4]) > 0:
                        stat1 = True
        if stat1:
            self.num3_f += 1
        if self.num3_f >= 2:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    def func_ponit3_re(self, score_index, red_obls_front, blue_obls_front, yellow_obls_front, hands_front,
                       exchangers_front):
        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    def func_ponit1_re(self, score_index, red_obls_front, blue_obls_front, yellow_obls_front, hands_front,
                                           exchangers_front):
        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 4 正确调节遮光器和反光镜
    def opera_sunshade_refle(self, score_index, hands_front, reflectors_front,):
        if hands_front.shape[0] !=0 and reflectors_front.shape[0] !=0:
            for hand_front in hands_front:
                for reflector_front in reflectors_front:
                    hand_refle_iou = iou(hand_front[:4], reflector_front[:4])
                    reflector_area = box_area(reflector_front[:4])
                    if hand_refle_iou > 0.35 * reflector_area:
                        self.num4_f += 1
        if self.num4_f > 5:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 5 通过目镜或显示屏看到明亮的视野
    def observe_light(self,score_index,heads_front,coarse_ads_front):
        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 6 把装片正确固定在载物台上，装片正对通光孔
    def opera_blood_slider(self, score_index, hands_side, blood_glas_side, stages_side,tab_holders_side, blank_glas_side,
                          blood_glas_top, stages_top):
        """
        侧视图:
        在该状态下 载物台有载玻片相交面积 大于载玻片本身面积的0.9倍
        :param score_index:
        :param hands_side:
        :param glass_slides_side:
        :param stages_side:
        :return:
        """
        if blood_glas_top.shape[0] != 0 and stages_top.shape[0] != 0:
            for stage_top in stages_top:
                for blood_gla_top in blood_glas_top:
                    if iou(stage_top[:4], blood_gla_top[:4])>0:
                        self.blood_stat = True

        # 人血涂片 固定
        if blood_glas_side.shape[0] != 0 and stages_side.shape[0] != 0 and tab_holders_side.shape[0] != 0:
            stat1 = False
            stat2 = False  # 压片夹与载片有交集
            stat3 = False  #
            for stage_side in stages_side:
                for blood_gla_side in blood_glas_side:
                    # instage = pt_in_box(center_point(blood_gla_side[:4]),stage_side[:4] )  # 中心点在载物台
                    instage = box1_in_box2(blood_gla_side[:4], stage_side[:4])
                    if instage:
                        # print(instage)
                        stat1 = True
            if stat1:
                for tab_holder_side in tab_holders_side:
                    for blood_gla_side in blood_glas_side:
                        tab_blood_iou = iou(tab_holder_side[:4], blood_gla_side[:4])
                        tab_area = box_area(tab_holder_side)
                        if tab_blood_iou > 0.2 * tab_area:
                            stat2 = True
            if stat2:
                for hand_side in hands_side:
                    for stage_side in stages_side:
                        if not iou(hand_side[:4], stage_side[:4]):
                            self.num5_f_qm += 1
            if self.num5_f_qm >= 3:
                return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

        # 空白载片固定
        if blank_glas_side.shape[0] != 0 and stages_side.shape[0] != 0 and tab_holders_side.shape[0] != 0:
            stat1 = False
            stat2 = False  # 压片夹与载片有交集
            stat3 = False  #
            for stage_side in stages_side:
                for blank_gla_side in blank_glas_side:
                    # instage = pt_in_box(center_point(blank_gla_side[:4]), stage_side[:4])  # 中心点在载物台
                    instage = box1_in_box2(blank_gla_side[:4],stage_side[:4])  # 空白载玻片完全在载物台
                    # print(f"空白==={instage}")
                    if instage:
                        stat1 = True
            if stat1:
                for tab_holder_side in tab_holders_side:
                    for blank_gla_side in blank_glas_side:
                        tab_blood_iou = iou(tab_holder_side[:4], blank_gla_side[:4])
                        tab_area = box_area(tab_holder_side)
                        if tab_blood_iou > 0.2 * tab_area:
                            stat2 = True
            if stat2:
                for hand_side in hands_side:
                    for stage_side in stages_side:
                        if not iou(hand_side[:4], stage_side[:4]):
                            self.num5_f_kb += 1
            if self.num5_f_kb >= 3:
                return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    def func_point5_re(self,score_index,hands_side, blood_glas_side, stages_side, tab_holders_side, blank_glas_side):
        return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side

    # 7 侧看物镜,转动粗准焦螺旋，使镜筒缓慢下降直至物镜接近装片为止
    def near_blood_slider(self,score_index, hands_front, blood_glas_front, stages_front, coarse_ads_front,
                         yellow_obls_front,red_obls_front,blue_obls_front, ad_coarse_ads_front, exchangers_front,
                         hands_top,exchangers_top,ad_coarse_ads_top,ad_fine_ads_front,heads_front):
        """
        前视角:
        1手与粗准焦有交集;
        2 小物镜与载物台中心点的距离 减去 (小物镜半个高+载物台半个高 ) 小于 20个像素
        :param score_index:
        :param hands_front:
        :param blood_glas_front:
        :param stages_front:
        :param coarse_ads_front:
        :param yellow_obl_front:
        :param ad_coarse_ads_front:
        :return:
        """
        # 黄色物镜or红色物镜 离载物台最近
        stat1 = False  # 手转动粗准焦
        stat2 = False
        stat3 = True  # 前视角手转换器交集面积小于转化器面积的0.3倍
        head_stat = False  # 头的状态
        # 判断头位置的状态
        if heads_front.shape[0] != 0 and exchangers_front.shape[0] != 0:
            # 头的y最低点 与转换器 y轴最高点的距离在一个范围内
            for head_front in heads_front:
                for exchanger_front in exchangers_front:
                    head_exch_y_pos = max(head_front[:4][1], head_front[:4][3]) - min(exchanger_front[:4][1],
                                                                                     exchanger_front[:4][3])
                    if head_exch_y_pos < 30:
                        head_stat = True
            # print(f'head stat==={head_stat}')
        if hands_front.shape[0] != 0 and exchangers_front.shape[0] != 0:
            for hand_front in hands_front:
                for exchanger_front in exchangers_front:
                    iou_han_excha = iou(hand_front[:4], exchanger_front[:4])
                    exhca_area = box_area(exchanger_front[:4])
                    if iou_han_excha > 0.5*exhca_area:
                        stat3 = False
        if hands_top.shape[0] != 0 and exchangers_top.shape[0] != 0:
            for hand_top in hands_top:
                for exchanger_top in exchangers_top:
                    iou_han_excha = iou(hand_top[:4], exchanger_top[:4])
                    excha_area = box_area(exchanger_top[:4])
                    if iou_han_excha > 0.5*excha_area:
                        stat3 = False
        # if stat3 and hands_front.shape[0] != 0 and coarse_ads_front.shape[0]!=0:
        #     for hand_front in hands_front:
        #         for coarse_ad_front in coarse_ads_front:
        #             if iou(coarse_ad_front[:4], hand_front[:4])>0.8*box_area(coarse_ad_front[:4]):
        #                 stat1 = True
        #                 break
        if stat3 and ad_coarse_ads_front.shape[0] != 0:
            stat1 = True
        if stat3 and ad_coarse_ads_top.shape[0] != 0:
            stat1 = True
        if stat3 and ad_fine_ads_front.shape[0] != 0:
            stat1 = True
        if stat1 and stages_front.shape[0] != 0 and yellow_obls_front.shape[0] != 0:
            for yellow_obl_front in yellow_obls_front:
                for stage_front in stages_front:
                    sma_sta_y = center_distance_v(yellow_obl_front[:4], stage_front[:4], abs_v=True)
                    sma_h = abs(yellow_obl_front[:4][1] - yellow_obl_front[:4][3])
                    sta_h = abs(stage_front[:4][1] - stage_front[:4][3])
                    # print(f"黄色物镜和载物台垂直中心点的距离 sma_sta_y=={sma_sta_y}")
                    # print(f"红色大了多少像素=={sma_sta_y - (sma_h / 2 + sta_h / 2)}")
                    # print(f"载物台的高=={sta_h}")
                    if sma_sta_y - (sma_h / 2 + sta_h / 2) <= 30:
                        stat2 = True
            pass
        if stat1 and stages_front.shape[0] != 0 and red_obls_front.shape[0] != 0:
            for red_obl_front in red_obls_front:
                for stage_front in stages_front:
                    sma_sta_y = center_distance_v(red_obl_front[:4], stage_front[:4], abs_v=True)
                    sma_h = abs(red_obl_front[:4][1] - red_obl_front[:4][3])
                    sta_h = abs(stage_front[:4][1] - stage_front[:4][3])
                    # print(f"红色物镜和载物台垂直中心点的距离 sma_sta_y=={sma_sta_y}")
                    # print(f"红色大了多少像素=={sma_sta_y - (sma_h / 2 + sta_h / 2)}")
                    # print(f"载物台的高=={sta_h}")
                    if sma_sta_y - (sma_h / 2 + sta_h / 2) <= 30:
                        stat2 = True
        # print(f"载玻片位置  {self.num1_slide}")
        if stat2 and self.num1_slide >= 2:
        # if stat2:
            self.num6_f += 1

        if self.num6_f > 3:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        # 大物镜离载物台最近
        if stat1 and stages_front.shape[0] != 0 and blue_obls_front.shape[0] != 0:
            for blue_obl_front in blue_obls_front:
                for stage_front in stages_front:
                    big_sta_y = center_distance_v(blue_obl_front[:4], stage_front[:4], abs_v=True)
                    big_h = abs(blue_obl_front[:4][1] - blue_obl_front[:4][3])
                    sta_h = abs(stage_front[:4][1] - stage_front[:4][3])
                    # print(f"大物镜和载物台垂直中心点的距离 sma_sta_y=={big_sta_y}")
                    # print(f"大了多少像素=={big_sta_y - (big_h/2+sta_h/2)}")
                    # print(f"载物台的高=={sta_h}")
                    if big_sta_y - (big_h / 2 + sta_h / 2) < 30:
                        # self.num6_f_big += 1
                        stat2 = True
        # print(f"dawujing ==={self.num1_slide}")
        if stat2 and self.num1_slide >= 2:
            self.num6_f_big += 1

        if self.num6_f_big > 3:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

        pass

    def quxia_blood(self, score_index,stages_top,stages_side,blood_glas_top,blood_glas_side):
        if stages_top.shape[0] !=0 and blood_glas_top.shape[0] != 0:
            for stage_top in stages_top:
                for blood_gla_top in blood_glas_top:
                    iou_area = iou(stage_top[:4], blood_gla_top[:4])
                    blood_area = box_area(blood_gla_top[:4])
                    if iou_area < 0.5*blood_area:
                        if len(self.quxia_blood_info) == 0:
                            self.quxia_blood_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                    self.preds_front]

    # 8 正确使用粗准焦螺旋，使镜筒上升，直到看到清晰的物像为止
    def up_lenscone(self, score_index, hands_front, coarse_ads_front, heads_front, ad_coarse_ads_front):
        # return score_index, self.frame_side, self.time_side, self.objects_side, self.preds_side
        return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 9 如果物像不清晰，正确使用细准焦螺旋，使看到物像更清晰
    def op_fine_ad(self, score_index, hands_front, fine_ads_front, heads_front, ad_fine_ads_front):
        if hands_front.shape[0] !=0 and fine_ads_front.shape[0] !=0:
            for hand_front in hands_front:
                for fine_ad_front in fine_ads_front:
                    hand_finead_iou = iou(hand_front[:4], fine_ad_front[:4])
                    finead_area = box_area(fine_ad_front[:4])
                    if hand_finead_iou > 0.8 * finead_area:
                        self.num9_f += 1
        if ad_fine_ads_front.shape[0] != 0:
            self.num9_f += 1
        if self.num9_f >5:
            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    # 10 移动标本能将白细胞放在视野中央
    def move_slide(self, score_index, hands_front, blood_glas_front, stages_front, stages_top, hands_top, blood_glas_top,
                                stages_side, hands_side, blood_glas_side):
        """
        1在 第7得分点 得到后, 手与载物台有交集,交集面积大于手面积的 载物台面积 0.35倍
        2 两个手与载物台都有交集
        :param score_index:
        :param hands_front:
        :param blood_glas_front:
        :param stages_top:
        :param hands_top:
        :param blood_glas_top:
        :param stages_side:
        :param hands_side:
        :param blood_glas_side:
        :return:
        """
        if hands_front.shape[0] !=0 and stages_front.shape[0] != 0:
            stat = False
            n = 0
            for hand_front in hands_front:
                for stage_front in stages_front:
                    # hand_stage_iou = iou(hand_front[:4], stage_front[:4])
                    # stage_area = box_area(stage_front[:4])
                    if iou(hand_front[:4], stage_front[:4]) >0:
                        n += 1
            if n == 2:
                stat = True
            if stat:
                self.num10_f += 1
            if self.num10_f >5:
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front

    def getImageVar(self, image):
        # image = cv2.imread(path)
        # h, w = image.shape[:2]
        # w_s = int(w / 4)
        # w_e = int(w * 3 / 4)
        # h_s = int(h / 4)
        # h_e = int(h * 3 / 4)
        # image = image[w_s:w_e, h_s:h_e]
        img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
        return imageVar

    # 开运算:cv2.morphologyEx() ：先腐蚀再膨胀，有助于消除噪音.
    def morphologyExObloodng(self, img):
        # 这个是颜色的HSV的范围值(分别代表的是H,S,V)，可以根据需求进行删改
        color_dist = {'red': {'Lower': np.array([0, 53, 66]), 'Upper': np.array([74, 76, 187])},
                      'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
                      'green': {'Lower': np.array([77, 54, 47]), 'Upper': np.array([166, 255, 255])},
                      'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
                      }
        # 高斯滤波
        gs_frame = cv2.GaussianBlur(img, (5, 5), 0)

        # 转化成HSV图像
        hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
        # 规定红色区域的HSV.
        # OpenCV中的inRange()函数可实现二值化功能（这点类似threshold()函数
        # cv2.inRange((InputArray src, InputArray lowerb,InputArray upperb, OutputArray dst);
        # 参数1：输入要处理的图像，可以为单通道或多通道。
        # 参数2：包含下边界的数组或标量。
        # 参数3：包含上边界数组或标量。
        # 参数4：输出图像，与输入图像src 尺寸相同且为CV_8U 类型。也可以作为返回值处理
        inRange_hsv = cv2.inRange(hsv, color_dist['green']['Lower'], color_dist['green']['Upper'])

        kernel = np.ones((5, 5), np.uint8)
        obloodng = cv2.morphologyEx(inRange_hsv, cv2.MORPH_OPEN, kernel)  # 处理后的图片 二值图
        count = cv2.countNonZero(obloodng)
        return count

    def fun_judge_imageQuality(self, img, thr=800):
        # binary
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_binary = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 17, 10)
        v_sum = 0
        n = 0
        h, w = img.shape[:2]
        w_s = 10  # int(w/4)
        w_e = w - 10  # int(w*3/4)
        h_s = 10  # int(h/4)
        h_e = h - 10  # int(h*3/4)
        #  calculate
        for i in np.arange(w_s, w_e):
            for j in np.arange(h_s, h_e):

                if img_binary[j][i]:
                    if img[j][i][2] > 240 and img[j][i][0] < 30 and img[j][i][1] < 30:
                        continue
                    q = np.power(int(img_gray[j][i]) - int(img_gray[j][i - 1]), 2)
                    v_sum += q
                    n += 1
        img_qualitey = 0
        img_good = False
        if n > thr:
            img_qualitey = v_sum / n
            img_good = True
        # print("{}: {} :: {} ".format(n, v_sum, img_qualitey))
        # cv2.imshow('img1',img_gray)
        # cv2.imshow('img2',img_binary)
        # cv2.waitKey()
        # if img_qualitey > thr:
        #     img_good = True
        return img_good

    # 清理桌面
    def clearn_desk(self, score_index, top_items, front_items):
        if self.desk_is_clearn([top_items, front_items], [self.center_area_top, self.center_area_front]):  # 只看前视角
            self.clearn_desk_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                     self.preds_front,
                                     self.num_frame_front, self.secs]
            self.clearn_f_num, _, flag = self.duration(self.clearn_f_num, 0.5)
            if flag:
                # self.assignScore(5, self.top_img0, self.top_preds)
                self.clearn_f_num = 0
                return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front
        else:
            self.clearn_f_num = 0

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and time.time() - self.clearn_desk_info[-1] < 2.:
            self.assignScore(*self.clearn_desk_info)
            return True
        if self.quxia_blood_info:
            self.assignScore(*self.quxia_blood_info)

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
