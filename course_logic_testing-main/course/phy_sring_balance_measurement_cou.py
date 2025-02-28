#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/9 16:28
# @Author  : Wupenghui
# @File    : phy_sring_balance_measurement_cou.py

import random
from .comm import *
from .comm.course_base import ConfigModel

# from config.phy_sring_balance_measurement_conf import PYTHCLJCL01

class PHY_sring_balance_measurement_cou(ConfigModel):

    def __init__(self):
        super(PHY_sring_balance_measurement_cou, self).__init__()


    def score_process(self, top_true, front_true, side_true):  # 赋分逻辑部分

        if front_true:
            hand, eye, weight_beam, weight_beam_zero, hook_weight, hand_pull_ring, silver_strip_proportion, \
            clean_desk, head = self.preds_front


        # 观察并记录弹簧测力计量程和最小分度值，完成弹簧测力计调零
        # 标签head与hand存在 And hand与wight_beam IoU大于0 and (head与wight_beam or hand IoU大于0)
        if not self.scorePoint1:
            if weight_beam_zero.shape[0] != 0:
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
            else:
                if hand.shape[0] == 2 and weight_beam.shape[0] != 0:
                    if iou(hand[0][:4], weight_beam[0][:4]) > 0.25 * box_area(hand[0][:4]) and \
                            iou(hand[1][:4], weight_beam[0][:4]) > 0.25 * box_area(hand[1][:4]):
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

        if not self.scorePoint2 and self.scorePoint1:
            if weight_beam_zero.shape[0] != 0:
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
            else:
                if hand.shape[0] == 2 and weight_beam.shape[0] != 0:
                    if iou(hand[0][:4], weight_beam[0][:4]) > 0.25 * box_area(hand[0][:4]) and \
                            iou(hand[1][:4], weight_beam[0][:4]) > 0.25 * box_area(hand[1][:4]):
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

        # 在弹簧测力计的挂钩上悬挂合适的物体
        # 3、标签hand与hook_weight IoU大于阈值, 所有hand与weight_beam IoU 大于0 And 标签silver_strip_proportion在hook_weight上方
        if not self.scorePoint3:
            if hand.shape[0] == 2 and hook_weight.shape[0] != 0 and weight_beam.shape[0] != 0:
                if iou(hand[0][:4], weight_beam[0][:4]) > 0 or iou(hand[0][:4], hook_weight[0][:4]) > \
                        0.85 * box_area(hook_weight[0][:4]):
                    self.flag3 = True
                if iou(hand[1][:4], weight_beam[0][:4]) > 0 or iou(hand[1][:4], hook_weight[0][:4]) > \
                        0.85 * box_area(hook_weight[0][:4]):
                    self.flag3_1 = True

            if self.flag3 is True and self.flag3_1 is True and silver_strip_proportion.shape[0] != 0 \
                    and hook_weight.shape[0] != 0:
                if adjoin(hook_weight[0][:4], silver_strip_proportion[0][:4]) is True:
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

            # 物体静止时，观察并记录弹簧测力计示数
            # 4、标签hand与hook_weight IoU为0 And 标签silver_strip_proportion在hook_weight上方
        if not self.scorePoint4 and self.scorePoint3 and hand.shape[0] != 0 and hook_weight.shape[0] != 0 and \
                silver_strip_proportion.shape[0] != 0:
            hand_count = 0
            for _hand in hand:
                hand_box = _hand[:4]
                if iou(hook_weight[0][:4], hand_box) == 0:
                    hand_count += 1
            if hand_count == hand.shape[0]:
                self.flag4 = True
            if self.flag4 is True:
                if adjoin(hook_weight[0][:4], silver_strip_proportion[0][:4]) is True:
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

        if (not self.scorePoint5 and clean_desk.shape[0] != 0 and self.scorePoint4) or \
                (self.scorePoint4 and weight_beam.shape[0] == 0 and hook_weight.shape[
                    0] == 0 and not self.scorePoint5):
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
    # logger.info('赋分进程结束')
