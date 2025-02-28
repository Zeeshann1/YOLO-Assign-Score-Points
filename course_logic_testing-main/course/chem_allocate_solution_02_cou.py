#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 14:34
# @Author  : Qiguangnan
# @File    : phy_density_liquid_02_cou.py

'''
一定溶质质量分数的氯化钠溶液配置(托盘天平)
'''

from .about_weigh_score_point_cou import AboutWeigh


class CHEM_allocate_solution_02(AboutWeigh):

    def __init__(self, *args, **kwargs):
        super(CHEM_allocate_solution_02, self).__init__(*args, **kwargs)


    def score_process(self, *args):  # 赋分逻辑部分
        (hands_front, eyes_front, heads_front, dusters_front, scale_es_front, salver_es_front, scale_ons_front,
         scale_offs_front, scales_front, salvers_front, salver_bars_front, nuts_front, weights_front, weight_boxs_front,
         tweezer_ws_front, riders_front, measuring_cylinders_front, measuring_cylinder_mouths_front,
         measuring_cylinder_bottoms_front, water_columns_front, liquid_levels_front, wild_mouth_bottles_front,
         wild_stopper_upends_front, wild_stopper_no_upends_front, narrow_mouth_bottles_front,
         narrow_mouth_bottlenecks_front, narrow_stopper_upends_front, narrow_stopper_no_upends_front, labels_front,
         label_papers_front, labellings_front, pens_front, writtings_front, write_labels_front, weigh_papers_front,
         beakers_front, liquids_front, salt_granules_front, spoons_front, spoon_us_front, glass_rods_front,
         droppers_front, dropper_hs_front, dropper_ws_front) = self.preds_front
        """
        ['手', '眼睛', '头', '抹布', '电子天平', '托盘', '天平开', 
        '天平关', '托盘天平', '托盘', '托盘杆', '调平螺母', '砝码', '砝码盒', 
        '镊子', '游码', '量筒', '量筒底', '水柱', 
        '液面', '广口瓶', '瓶塞未倒放', '瓶塞倒放', 
        '细口瓶', '细口瓶口', '瓶塞未倒放', '瓶塞倒放', 
        '标签', '称量纸', '液体', '食盐颗粒', '药匙', '药匙勺', 
        '烧杯', '玻璃棒', '胶头滴管', '量筒口']
        """
        (hands_top, eyes_top, heads_top, dusters_top, scale_es_top, salver_es_top, scale_ons_top, scale_offs_top,
         scales_top, salvers_top, salver_bars_top, nuts_top, weights_top, weight_boxs_top, tweezer_ws_top, riders_top,
         measuring_cylinders_top, measuring_cylinder_mouths_top, measuring_cylinder_bottoms_top, water_columns_top,
         liquid_levels_top, wild_mouth_bottles_top, wild_stopper_upends_top, wild_stopper_no_upends_top,
         narrow_mouth_bottles_top, narrow_mouth_bottlenecks_top, narrow_stopper_upends_top,
         narrow_stopper_no_upends_top, labels_top, label_papers_top, labellings_top, pens_top, writtings_top,
         write_labels_top, weigh_papers_top, beakers_top, liquids_top, salt_granules_top, spoons_top, spoon_us_top,
         glass_rods_top, droppers_top, dropper_hs_top, dropper_ws_top) = self.preds_top

        water_v = self.water_volume(hands_front, measuring_cylinders_front, measuring_cylinder_mouths_front,
                                    measuring_cylinder_bottoms_front, water_columns_front, liquid_levels_front)

        # 1. 将天平放在水平台面，调节天平平衡
        if not self.scorePoint1 and len(self.score_list) == 0:
            info = self.scaleBalance(hands_front, salver_bars_front, salvers_top, weigh_papers_top)
            if info:
                self.assignScore(1, *info[:5])
                self.initScaleBalance()  # 初始化 下面称量时还要判断平衡

        # 2. 在两个托盘上放置称量纸
        if not self.scorePoint2:
            info = self.weighPaperOnScale(scales_top, weigh_papers_top)
            if info:
                self.assignScore(2, *info[:5])

        # 3. 将游码滑到需要称量的位置(配合砝码)
        if not self.scorePoint3 and self.scorePoint2:
            info = self.setRider(salver_bars_front, tweezer_ws_front, riders_front, tweezer_ws_top, riders_top)
            if info:
                self.assignScore(3, *info[:5])

        # 4. 取氯化钠固体时瓶塞倒放
        if not self.scorePoint4:
            info = self.stopperUpend(wild_stopper_upends_front, wild_stopper_no_upends_front,
                                     wild_stopper_upends_top, wild_stopper_no_upends_top)
            if info:
                self.assignScore(4, *info[:5])

        # 5. 用药匙取氯化钠
        if not self.scorePoint5:
            info = self.useSpoon(salt_granules_front, wild_mouth_bottles_front, spoons_front, scales_front,
                                 hands_front, salt_granules_top, wild_mouth_bottles_top, spoons_top, hands_top,
                                 scales_top)
            if info:
                self.assignScore(5, *info[:5])

        # 6. 轻拍手腕（或药匙柄）添加氯化钠
        if not self.scorePoint6:
            info = self.patWeigh(hands_top, spoons_top, spoon_us_top, scales_top, wild_mouth_bottles_top,
                                 spoons_front, spoon_us_front, scales_front, salvers_front)
            if info:
                self.assignScore(6, *info[:5])

        # 7. 准确称量NaCL至所需量，天平平衡
        if not self.scorePoint7 and self.scorePoint2 and (self.scorePoint3 or self.scorePoint5):
            info = self.weighBalance(hands_front, spoons_front, spoon_us_front, salver_bars_front, salvers_front,
                                     salt_granules_front, hands_top, spoons_top, spoon_us_top, salvers_top,
                                     weigh_papers_top, scales_top, salt_granules_top)
            if info:
                self.assignScore(7, *info[:5])

        # 8. 向量筒中倾倒蒸馏水，接近至所需量
        if not self.scorePoint8:
            info = self.waterInCylinder(water_columns_front, measuring_cylinders_front, narrow_mouth_bottles_front)
            if info:
                self.assignScore(8, *info[:5])

        # 9 量筒水平放置，用胶头滴管逐滴滴加蒸馏水至所需量
        if not self.scorePoint9:
            info = self.dropWaterIncylinder(droppers_front, measuring_cylinders_front, water_columns_front)
            if info:
                self.assignScore(9, *info[:5])

        # 10. 读数时，视线与量筒内液体的凹液面的最低处保持水平
        if not self.scorePoint10:
            info = self.readDisplayData(water_columns_front, heads_front, eyes_front)
            if info:
                self.assignScore(10, *info[:5])

        # 11. 把量取的蒸馏水全部倒入烧杯中
        if not self.scorePoint11:
            info = self.water2beaker(measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                                     liquids_front)
            if info is not None:
                self.assignScore(11, *info[:5])

        # 12. 在烧杯中溶解NaCl，用玻璃棒搅拌
        if not self.scorePoint12:
            info = self.stirDissolve(glass_rods_front, beakers_front, hands_front, 20, 8)
            if info is not None:
                self.assignScore(12, *info[:5])

        # 13. 将配制好的溶液转移至贴有标签的指定容器中
        if not self.scorePoint13:
            info = self.transferLiquid(beakers_front, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front,
                                       hands_front)
            if info is not None:
                self.assignScore(13, *info[:5])

        # 14. 清洗仪器，整理桌面
        top_items = [scales_top, salvers_top, weights_top, weight_boxs_top, tweezer_ws_top, wild_mouth_bottles_top,
                     narrow_mouth_bottles_top, measuring_cylinders_top,
                     weigh_papers_top, spoons_top, beakers_top, glass_rods_top, droppers_top]

        front_items = [scales_front, salvers_front, weights_front, weight_boxs_front, tweezer_ws_front,
                       wild_mouth_bottles_front, narrow_mouth_bottles_front,
                       measuring_cylinders_front, spoons_front, beakers_front, glass_rods_front, droppers_front]

        if not self.scorePoint14 and len(self.score_list) > 5:
            info = self.clearnDesk([top_items, front_items],
                                   [self.center_area_top, self.center_area_front],
                                   ['top', 'front'])
            if info:
                self.assignScore(14, *info[:5])
        if self.scorePoint14 and len(self.score_list) != 14:
            if not self.desk_is_clearn([top_items, front_items],
                                       [self.center_area_top, self.center_area_front],
                                       ['top', 'front']):
                self.retracementScore(14)

        if not self.faultPoint5:
            info = self.stopperNoUpend(narrow_stopper_upends_front, narrow_stopper_no_upends_front,
                                       narrow_stopper_upends_top, narrow_stopper_no_upends_top)
            if info:
                self.assignError(5, *info[:5])

        if not self.faultPoint6:
            info = self.stopperNoUpend(wild_stopper_upends_front, wild_stopper_no_upends_front,
                                       wild_stopper_upends_top, wild_stopper_no_upends_top)
            if info:
                self.assignError(6, *info[:5])

        if not self.faultPoint7:
            info = self.label_no_toward_palm(hands_front, labels_front)
            if info:
                self.assignError(7, *info[:5])
