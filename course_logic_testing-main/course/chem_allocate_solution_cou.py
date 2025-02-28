#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 15:04
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_cou.py

import random
from .comm import *
from .comm.course_base import ConfigModel


class CHEM_allocate_solution(ConfigModel):

    def __init__(self):
        super(CHEM_allocate_solution, self).__init__()

    def run_one_result_process(self, frame_top, frame_front, frame_side,
                               pred_top, pred_front, pred_side,
                               time_top, time_front, time_side,
                               num_frame_top,
                               num_frame_front,
                               num_frame_side,
                               path_save,
                               names_label):
        time_process_start = time.time()

        front_true = False
        top_true = False
        front1_preds = None
        if pred_front != None and pred_front.shape[0]:
            front1_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            front_true = True

        self.rtmp_push_fun(top_img=frame_top,front_img=frame_front,side_img=frame_side,
                           top_preds=None,front_preds=front1_preds,side_preds=None)


        if front_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分
            # [front1_preds], [front_img0] = preds, img0s
            scale_imbalance, scale_balance, spoon_salt, stopper_up, correct_weighing, measuring_water, \
            stir_dissolve, labelling, clean = front1_preds
            if "1" in self.exper_score_ids and not self.scorePoint1 and scale_balance.shape[0] != 0:
                # self.assignScore(1, front_img0, front1_preds)
                conf_c = 0.1
                conf_c = scale_balance[0][5]
                self.assignScore(index=1,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="scale_balance_1.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint1 = True

            if "2" in self.exper_score_ids and not self.scorePoint2 and spoon_salt.shape[0] != 0 and stopper_up.shape[
                0] != 0:
                # self.assignScore(2, front_img0, front1_preds)
                conf_c = 0.1
                conf_c = spoon_salt[0][5]
                self.assignScore(index=2,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="spoon_salt_2.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint2 = True

            if "3" in self.exper_score_ids and not self.scorePoint3 and correct_weighing.shape[0] != 0 and \
                    scale_balance.shape[0] != 0:
                # self.assignScore(3, front_img0, front1_preds)
                conf_c = 0.1
                conf_c = scale_balance[0][5]
                self.assignScore(index=3,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="scale_balance_3.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint3 = True

            if "4" in self.exper_score_ids and not self.scorePoint4 and measuring_water.shape[0] != 0:
                # self.assignScore(4, front_img0, front1_preds)
                conf_c = 0.1
                conf_c = measuring_water[0][5]
                self.assignScore(index=4,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="measuring_water_4.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint4 = True

            if "5" in self.exper_score_ids and not self.scorePoint5 and stir_dissolve.shape[0] != 0:
                # self.assignScore(5, front_img0, front1_preds)
                # conf_c = 0.1
                conf_c = spoon_salt[0][5]
                self.assignScore(index=5,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="spoon_salt_5.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint5 = True

            if "6" in self.exper_score_ids and not self.scorePoint6 and labelling.shape[0] != 0:
                # self.assignScore(6, front_img0, front1_preds)
                # conf_c = 0.1
                conf_c = labelling[0][5]
                self.assignScore(index=6,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="labelling_6.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint6 = True

            if "7" in self.exper_score_ids and not self.scorePoint7 and (self.scorePoint6 or self.scorePoint5) and \
                    clean.shape[0] != 0:
                # self.assignScore(7, front_img0, front1_preds)
                conf_c = 0.1
                conf_c = clean[0][5]
                self.assignScore(index=7,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="clean_7.jpg",
                                 preds=front1_preds
                                 )
                self.scorePoint7 = True
