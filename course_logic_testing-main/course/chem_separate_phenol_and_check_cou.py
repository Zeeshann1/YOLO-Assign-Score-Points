#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/12/03 16:54
# @Author  : wupenghui
# @File    : chem_separate_phenol_and_check_cou.py


from .comm import *
from .comm.course_base import ConfigModel
from logger import logger
import copy

class CHEM_separate_phenol_and_check(ConfigModel):
    def __init__(self):
        super(CHEM_separate_phenol_and_check, self).__init__()
        
        self.bbox = []
        self.background = None        
        
        self.flag1_1 = False
        self.flag2_1 = False
        self.flag2_2 = False
        self.flag3_1 = False
        self.flag3_2 = False
        self.flag3_3 = False
        self.flag4_1 = False
        self.flag5_1 = False
        self.flag5_2 = False
        self.flag6_1 = False
        self.flag6_2 = False
        self.flag7_1 = False
        self.flag7_2 = False
        self.flag8_1 = False
        self.flag8_2 = False
        self.flag9_1 = False
        self.flag9_2 = False
        self.flag10_1 = False
        self.flag10_2 = False
        self.flag11_1 = False
        self.flag11_2 = False
        self.flag12_1 = False
        self.flag12_2 = False
        self.flag13_1 = False
        self.flag14_1 = False
        self.flag15_1 = False
        self.flag16_1 = False
        self.flag17_1 = False
        
        self.container_secs = 0.
        self.container_secs_pre = 0.
        self.funnel_secs = 0.
        self.funnel_secs_pre = 0.
        self.stand_still_secs = 0.
        self.stand_still_secs_pre = 0.

    def hand_sth(self, hands, sths):  # 手握某个物体
        if hands.shape[0] != 0 and sths.shape[0] != 0:
            for hand in hands:
                hand_box = hand[:4]
                for sth in sths:
                    if iou(hand_box, sth[:4]) > 0:
                        return True
        return False

    def container_liquid(self, sths, liquids):  # 烧杯/试管中有 液柱
        if liquids.shape[0] == 0 or sths.shape[0] == 0:
            return False
        else:
            for sth in sths:
                sth_box = sth[:4]
                for liquid in liquids:
                    liquid_box = liquid[:4]
            
                    if iou(sth_box, liquid_box) > 0:
                        return True
    
    # def dropper_above_sth(self, dropper, sth):  # 胶头滴管在烧杯/试管上方
    #     tmp_sth = copy.deepcopy(sth)
    #     if dropper.shape[0] != 0 and tmp_sth.shape[0] != 0:
    #         tmp_sth[0][1] = 0
    #         # if iou(tmp_beaker[0][:4], dropper[0][:4]) > 0.6 * box_area(dropper[0][:4]):  # todo 考虑胶头滴管垂直
    #         if iou(tmp_sth[0][:4], dropper[0][:4]) > 0:
    #             return True
    #     else:
    #         return False  
    
    def retort_stand_container_beaker(self, retort_stand, beakers):
        if retort_stand.shape[0] == 0 or beakers.shape[0] == 0:
            return False
        else:
            for beaker in beakers:
                beaker_box = beaker[:4]
                if iou(retort_stand[0][:4], beaker_box) >= 0.65 * box_area(beaker_box):
                    return True
    
    def funnel_close_beaker(self, retort_stand, funnel, beakers):
        if retort_stand.shape[0] == 0 or funnel.shape[0] == 0 or beakers.shape[0] == 0:
            return False
        else:
            use_funnel = copy.deepcopy(funnel)
            h = (use_funnel[0][3] - use_funnel[0][1]) / 2
            use_funnel[0][1] += h 
            if self.retort_stand_container_beaker(retort_stand, beakers):
                for beaker in beakers:
                    beaker_box = beaker[:4]
                    if iou(beaker_box, use_funnel[0][:4]) >= 0.25 * box_area(use_funnel[0][:4]):
                        return True

    def funnel_stand_still_state(self, funnel, retort_stand, siderosphere, color_liquid_column):
        if funnel.shape[0] == 0 or retort_stand.shape[0] == 0 or siderosphere.shape[0] == 0 \
        or color_liquid_column.shape[0] == 0:
            return False
        else:
            funnel_w = funnel[0][2] - funnel[0][0]
            funnel_h = funnel[0][3] - funnel[0][1]
            if (iou(siderosphere[0][:4], funnel[0][:4]) >= 0.1 * box_area(siderosphere[0][:4])) \
            and ((3.5 * funnel_w) < funnel_h) and (self.container_liquid(funnel, color_liquid_column)):
                return True
    
    def funnel_use_state1(self, funnel, retort_stand, siderosphere, beaker, color_liquid_column):
        if funnel.shape[0] == 0 or retort_stand.shape[0] == 0 or siderosphere.shape[0] == 0 \
        or color_liquid_column.shape[0] == 0 or beaker.shape[0] == 0:
            return False
        else:
            funnel_w = funnel[0][2] - funnel[0][0]
            funnel_h = funnel[0][3] - funnel[0][1]
            if (iou(siderosphere[0][:4], funnel[0][:4]) >= 0.1 * box_area(siderosphere[0][:4])) \
            and ((3.5 * funnel_w) < funnel_h) and (self.retort_stand_container_beaker(retort_stand, beaker)) \
            and (not self.container_liquid(beaker, color_liquid_column)) and (self.container_liquid(funnel, color_liquid_column)):
                return True
    
    def funnel_use_state2(self, funnel, retort_stand, siderosphere, beaker, color_liquid_column):
        if funnel.shape[0] == 0 or retort_stand.shape[0] == 0 or siderosphere.shape[0] == 0 \
        or color_liquid_column.shape[0] == 0 or beaker.shape[0] == 0:
            return False
        else:
            funnel_w = funnel[0][2] - funnel[0][0]
            funnel_h = funnel[0][3] - funnel[0][1]
            if (iou(siderosphere[0][:4], funnel[0][:4]) >= 0.1 * box_area(siderosphere[0][:4])) \
            and ((3.5 * funnel_w) < funnel_h) and (self.retort_stand_container_beaker(retort_stand, beaker)) \
            and (self.container_liquid(beaker, color_liquid_column)):
                return True
    
    def phenol_separated_into_beakers(self, color_liquid_columns, beakers):
        if color_liquid_columns.shape[0] < 2 or beakers.shape[0] < 2:
            return False
        else:
            count = 0
            for beaker in beakers:
                use_beaker = copy.deepcopy(beaker)
                h = (use_beaker[3] - use_beaker[1]) / 2
                use_beaker[1] += h
                beaker_box = use_beaker[:4]
                
                for color_liquid_column in color_liquid_columns:
                    color_liquid_column_box = color_liquid_column[:4]
                    
                    if iou(color_liquid_column_box, beaker_box) > 0.6 * box_area(color_liquid_column_box):
                        count += 1
        
        if count == 2:
            return True                    
    
    def score_process(self,top_true,front_true,side_true):  # 赋分逻辑部分
        if top_true or front_true or side_true:
            if front_true:
                hand_front, test_tube_front, dropper_bottle_front, beaker_front, color_liquid_column_front, reagent_botle_front, \
                separating_funnel_front, separating_funnel_head_front, siderosphere_front, retort_stand_front, dropper_front, \
                hand_duster_front, layered_liquid_column_front, glass_rod_front = self.preds_front
            if top_true:
                hand_top, test_tube_top, dropper_bottle_top, beaker_top, color_liquid_column_top, reagent_botle_top, \
                separating_funnel_top, separating_funnel_head_top, siderosphere_top, retort_stand_top, dropper_top, \
                hand_duster_top, layered_liquid_column_top, glass_rod_top = self.preds_top
            if side_true:
                hand_side, test_tube_side, dropper_bottle_side, beaker_side, color_liquid_column_side, reagent_botle_side, \
                separating_funnel_side, separating_funnel_head_side, siderosphere_side, retort_stand_side, dropper_side, \
                hand_duster_side, layered_liquid_column_side, glass_rod_side = self.preds_side

            # 取苯和苯酚混合液适量于大试管（或烧杯）中
            if not self.scorePoint1:
                if not self.flag1_1 and self.hand_sth(hand_front, test_tube_front) \
                and self.container_liquid(test_tube_front, color_liquid_column_front):
                    self.flag1_1 = True
                
                if not self.flag1_1 and self.container_liquid(beaker_front, color_liquid_column_front):
                    self.flag1_1 = True
                
                if self.flag1_1:
                    conf_c = 0.1
                    self.assignScore(index=1,
                                    img=self.frame_front,
                                    object=self.objects_front,
                                    conf=conf_c,
                                    time_frame=self.time_front,
                                    num_frame=self.num_frame_front,
                                    name_save="1.jpg",
                                    preds=self.preds_front
                                    )
     
            
            # 滴加稍过量的浓NaOH溶液
            if not self.scorePoint2:
                if not self.flag2_1 and self.hand_sth(hand_front, test_tube_front) \
                and self.container_liquid(test_tube_front, color_liquid_column_front):
                    self.flag2_1 = True
                
                if not self.flag2_1 and self.container_liquid(beaker_front, color_liquid_column_front):
                    self.flag2_1 = True
                
                if self.flag2_1:
                    if self.container_liquid(beaker_front, layered_liquid_column_front) \
                    or self.container_liquid(test_tube_front, layered_liquid_column_front):
                        self.flag2_2 = True
                
                if self.flag2_2:
                    conf_c = 0.1
                    self.assignScore(index=2,
                                    img=self.frame_front,
                                    object=self.objects_front,
                                    conf=conf_c,
                                    time_frame=self.time_front,
                                    num_frame=self.num_frame_front,
                                    name_save="2.jpg",
                                    preds=self.preds_front
                                    )
          
            
            # 充分振荡
            if not self.scorePoint3:
                if not self.flag3_1 and self.hand_sth(hand_front, test_tube_front) \
                and self.container_liquid(test_tube_front, color_liquid_column_front):
                    self.flag3_1 = True
                
                if not self.flag3_1 and self.container_liquid(beaker_front, color_liquid_column_front):
                    self.flag3_1 = True
                
                if self.flag3_1:
                    if self.container_liquid(beaker_front, layered_liquid_column_front) \
                    or self.container_liquid(test_tube_front, layered_liquid_column_front):
                        self.flag3_2 = True
                
                if self.flag3_2:
                    if self.hand_sth(hand_front, test_tube_front) or self.hand_sth(hand_front, beaker_front):
                        self.container_secs, self.container_secs_pre, self.flag3_3 = self.duration(self.container_secs, 1, 
                                                                                                self.container_secs_pre, 0.1)
                        if self.flag3_3:
                            conf_c = 0.1
                            self.assignScore(index=3,
                                            img=self.frame_front,
                                            object=self.objects_front,
                                            conf=conf_c,
                                            time_frame=self.time_front,
                                            num_frame=self.num_frame_front,
                                            name_save="3.jpg",
                                            preds=self.preds_front
                                            )
                            self.container_secs = 0. 
                            self.container_secs_pre = 0.
           
            # 有关化学方程式
            if not self.scorePoint4 and self.scorePoint3:
                conf_c = 0.1
                self.assignScore(index=4,
                                img=self.frame_front,
                                object=self.objects_front,
                                conf=conf_c,
                                time_frame=self.time_front,
                                num_frame=self.num_frame_front,
                                name_save="4.jpg",
                                preds=self.preds_front
                                )
                            
            # 将反应后的混合物转移到分液漏斗中
            if not self.scorePoint5:
                if self.container_liquid(separating_funnel_head_front, color_liquid_column_front):
                    conf_c = 0.1
                    self.assignScore(index=5,
                                    img=self.frame_front,
                                    object=self.objects_front,
                                    conf=conf_c,
                                    time_frame=self.time_front,
                                    num_frame=self.num_frame_front,
                                    name_save="5.jpg",
                                    preds=self.preds_front
                                    )
                                 

            # 振荡
            if not self.scorePoint6:
                if self.container_liquid(separating_funnel_head_front, color_liquid_column_front):
                    self.flag6_1 = True
                
                if self.flag6_1:
                    self.funnel_secs, self.funnel_secs_pre, self.flag6_2 = self.duration(self.funnel_secs, 1, 
                                                                                        self.funnel_secs_pre, 0.1)
                    if self.flag6_2:
                        conf_c = 0.1
                        self.assignScore(index=6,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="6.jpg",
                                        preds=self.preds_front
                                        )
                        self.funnel_secs = 0. 
                        self.funnel_secs_pre = 0.
                                        
        
            # 静置
            if not self.scorePoint7:
                if self.funnel_stand_still_state(separating_funnel_front, retort_stand_front, siderosphere_front, color_liquid_column_front):
                    self.stand_still_secs, self.stand_still_secs_pre, self.flag7_1 = self.duration(self.stand_still_secs, 10, 
                                                                                                self.stand_still_secs_pre, 0.5)
                    if self.flag7_1:
                        conf_c = 0.1
                        self.assignScore(index=7,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="7.jpg",
                                        preds=self.preds_front
                                        )
                        self.stand_still_secs = 0.
                        self.stand_still_secs_pre = 0.
                    
            
            # 分液,分液漏斗使用正确
            if not self.scorePoint8:
                if not self.flag8_1 and self.funnel_use_state1(separating_funnel_front, retort_stand_front, 
                                                            siderosphere_front, beaker_front, color_liquid_column_front):
                    self.flag8_1 = True
                
                if self.flag8_1 and not self.flag8_2:
                    if self.funnel_use_state2(separating_funnel_front, retort_stand_front, siderosphere_front, 
                                            beaker_front, color_liquid_column_front):
                        self.flag8_2 = True
                
                if self.flag8_2:
                    conf_c = 0.1
                    self.assignScore(index=8,
                                    img=self.frame_front,
                                    object=self.objects_front,
                                    conf=conf_c,
                                    time_frame=self.time_front,
                                    num_frame=self.num_frame_front,
                                    name_save="8.jpg",
                                    preds=self.preds_front
                                    )   
           
            # 分液漏斗下口靠小烧杯A内壁
            if not self.scorePoint9:
                if self.funnel_use_state1(separating_funnel_front, retort_stand_front, 
                                        siderosphere_front, beaker_front, color_liquid_column_front):
                    self.flag9_1 = True
                
                if self.flag9_1:
                    if self.funnel_close_beaker(retort_stand_front, separating_funnel_front, beaker_front):
                        conf_c = 0.1
                        self.assignScore(index=9,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="9.jpg",
                                        preds=self.preds_front
                                        )   
                     
            
            # 上层液体从分液漏斗上口倒入小烧杯B
            if not self.scorePoint10:
                if self.phenol_separated_into_beakers(color_liquid_column_front, beaker_front):
                        conf_c = 0.1
                        self.assignScore(index=10,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="10.jpg",
                                        preds=self.preds_front
                                        )   
                         

            # 向分液所得的下层液体(小烧杯A)中加入适量盐酸
            if not self.scorePoint11:
                if self.phenol_separated_into_beakers(color_liquid_column_front, beaker_front):
                    self.flag11_1 = True
                    
                if self.flag11_1 and beaker_front.shape[0] != 0 and dropper_front.shape[0] != 0 and color_liquid_column_front.shape[0] != 0:
                    beakers = copy.deepcopy(beaker_front)
                    for beaker in beakers:
                        beaker[1] = 0
                        beaker_box1 = beaker[:4]
                        for dropper in dropper_front:
                            dropper_box1 = dropper[:4]
                            
                            if iou(dropper_box1, beaker_box1) > 0.5 * box_area(dropper_box1):
                                conf_c = 0.1
                                self.assignScore(index=11,
                                                img=self.frame_front,
                                                object=self.objects_front,
                                                conf=conf_c,
                                                time_frame=self.time_front,
                                                num_frame=self.num_frame_front,
                                                name_save="11.jpg",
                                                preds=self.preds_front
                                                )   
                          
            
            # 搅拌
            if not self.scorePoint12 and self.scorePoint11:
                if self.phenol_separated_into_beakers(color_liquid_column_front, beaker_front):
                    self.flag12_1 = True
                
                if self.flag12_1:
                    if self.hand_sth(hand_front, glass_rod_front):
                        for beaker in beaker_front:
                            beaker_box2 = beaker[:4]
                            if iou(beaker_box2, glass_rod_front[0][:4]):
                                conf_c = 0.1
                                self.assignScore(index=12,
                                                img=self.frame_front,
                                                object=self.objects_front,
                                                conf=conf_c,
                                                time_frame=self.time_front,
                                                num_frame=self.num_frame_front,
                                                name_save="12.jpg",
                                                preds=self.preds_front
                                                )   
            
            # 有关化学方程式
            if not self.scorePoint13 and self.scorePoint12:
                conf_c = 0.1
                self.assignScore(index=13,
                                img=self.frame_front,
                                object=self.objects_front,
                                conf=conf_c,
                                time_frame=self.time_front,
                                num_frame=self.num_frame_front,
                                name_save="13.jpg",
                                preds=self.preds_front
                                )
                                                   
                        
            # 取适量所得苯酚溶液于小试管中
            if not self.scorePoint14 and self.scorePoint12:
                if self.phenol_separated_into_beakers(color_liquid_column_front, beaker_front):
                    self.flag14_1 = True
                
                if self.flag14_1 and test_tube_front.shape[0] != 0 and color_liquid_column_front.shape[0] != 0:
                    for test_tube in test_tube_front:
                        test_tube_box1 = test_tube[:4]
                        for color_liquid_column in color_liquid_column_front:
                            color_liquid_column_box = color_liquid_column[:4]
                            if iou(test_tube_box1, color_liquid_column_box) > 0.3 * box_area(color_liquid_column_box):
                                conf_c = 0.1
                                self.assignScore(index=14,
                                                img=self.frame_front,
                                                object=self.objects_front,
                                                conf=conf_c,
                                                time_frame=self.time_front,
                                                num_frame=self.num_frame_front,
                                                name_save="14.jpg",
                                                preds=self.preds_front
                                                )   
                                          
            
            # 滴加氯化铁溶液
            if not self.scorePoint15:
                if reagent_botle_front.shape[0] != 0 and hand_front.shape[0] != 0 and color_liquid_column_front.shape[0] != 0 and dropper_front.shape[0] != 0:
                    for reagent_bottle in reagent_botle_front:
                        use_reagent_bottle = copy.deepcopy(reagent_bottle)
                        use_reagent_bottle[1] = 0
                        reagent_box = use_reagent_bottle[:4]
                        for color_liquid_column in color_liquid_column_front:
                            color_liquid_column_box1 = color_liquid_column[:4]
                            for dropper in dropper_front:
                                dropper_box2 = dropper[:4]

                                if iou(reagent_box, color_liquid_column_box1) > 0.35 * box_area(color_liquid_column_box1) \
                                and iou(reagent_box, dropper_box2) > 0.5 * box_area(dropper_box2):
                                    self.flag15_1 = True
                
                if self.flag15_1 and test_tube_front.shape[0] != 0 and dropper_front.shape[0] != 0:
                    for test_tube in test_tube_front:
                        use_test_tube = copy.deepcopy(test_tube)
                        use_test_tube[1] = 0
                        test_tube_box2 = use_test_tube[:4]
                        for dropper in dropper_front:
                            dropper_box3 = dropper[:4]
                            
                            if iou(test_tube_box2, dropper_box3) > 0.5 * box_area(dropper_box3):
                                conf_c = 0.1
                                self.assignScore(index=15,
                                                img=self.frame_front,
                                                object=self.objects_front,
                                                conf=conf_c,
                                                time_frame=self.time_front,
                                                num_frame=self.num_frame_front,
                                                name_save="15.jpg",
                                                preds=self.preds_front
                                                )   
                                self.assignScore(index=16,
                                                img=self.frame_front,
                                                object=self.objects_front,
                                                conf=conf_c,
                                                time_frame=self.time_front,
                                                num_frame=self.num_frame_front,
                                                name_save="16.jpg",
                                                preds=self.preds_front
                                                )   

            
            # 器材及时清洗并复位，桌面保持清洁
            if not self.scorePoint17:
                arr = [self.scorePoint1, self.scorePoint2, self.scorePoint3, self.scorePoint4, self.scorePoint5, self.scorePoint6, self.scorePoint7, 
                    self.scorePoint8, self.scorePoint9, self.scorePoint10, self.scorePoint11, self.scorePoint12, self.scorePoint13, self.scorePoint14, 
                    self.scorePoint15, self.scorePoint16]
                arr = np.array(arr)
                num_true = np.sum(arr != 0)
                if num_true >= 15:
                    self.flag17_1 = True
                
                if self.flag17_1:
                    if hand_duster_front.shape[0] != 0 or hand_duster_top.shape[0] != 0 or hand_duster_side.shape[0] != 0:
                        conf_c = 0.1
                        self.assignScore(index=17,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="17.jpg",
                                        preds=self.preds_front
                                        )      
                        self.assignScore(index=18,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="18.jpg",
                                        preds=self.preds_front
                                        ) 
                        self.assignScore(index=19,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="19.jpg",
                                        preds=self.preds_front
                                        ) 
                        self.assignScore(index=20,
                                        img=self.frame_front,
                                        object=self.objects_front,
                                        conf=conf_c,
                                        time_frame=self.time_front,
                                        num_frame=self.num_frame_front,
                                        name_save="20.jpg",
                                        preds=self.preds_front
                                        )             
    
    def end(self):
        if not self.scorePoint17:
            conf_c = 0.1
            self.assignScore(index=17,
                            img=self.frame_front,
                            object=self.objects_front,
                            conf=conf_c,
                            time_frame=self.time_front,
                            num_frame=self.num_frame_front,
                            name_save="17.jpg",
                            preds=self.preds_front
                            )      
            self.assignScore(index=18,
                            img=self.frame_front,
                            object=self.objects_front,
                            conf=conf_c,
                            time_frame=self.time_front,
                            num_frame=self.num_frame_front,
                            name_save="18.jpg",
                            preds=self.preds_front
                            ) 
            self.assignScore(index=19,
                            img=self.frame_front,
                            object=self.objects_front,
                            conf=conf_c,
                            time_frame=self.time_front,
                            num_frame=self.num_frame_front,
                            name_save="19.jpg",
                            preds=self.preds_front
                            ) 
            self.assignScore(index=20,
                            img=self.frame_front,
                            object=self.objects_front,
                            conf=conf_c,
                            time_frame=self.time_front,
                            num_frame=self.num_frame_front,
                            name_save="20.jpg",
                            preds=self.preds_front
                            )                   



