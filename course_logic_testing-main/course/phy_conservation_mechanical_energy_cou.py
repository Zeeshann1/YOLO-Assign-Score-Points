#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 14:50
# @Author  : Wangqingfeng
# @File    : pyh_conservaton_mechanical_energy_cou.py

from .comm import *
from .comm.course_base import ConfigModel


class PHY_conservation_mechanical_energy_cou(ConfigModel):
    def __init__(
            self
    ):
        super(PHY_conservation_mechanical_energy_cou, self).__init__()

        self.initScore()

    def initScore(self):
        self.d_time = 0.
        self.flag_weight_paper = False
        self.flag_picked = False
        self.num_picked = 0
        self.num_7 = 0
        self.num_8 = 0
        self.num_9 = 0
        self.desktop_info = []
        self.clean_desk = {}

    # def run_one_result_process(self, frame_top, frame_front, frame_side,
    #                            pred_top, pred_front, pred_side,
    #                            time_top, time_front, time_side,
    #                            num_frame_top,
    #                            num_frame_front,
    #                            num_frame_side,
    #                            path_save,
    #                            names_label):
    def score_process(self,top_true,front_true,side_true):
        # front_true = True
        # top_true = True
        # side_true = True
        # front_preds = None
        # top_preds = None
        # side_preds = None
        # device_use = "cuda :0"
        # if pred_front != None and pred_front.shape[0]:
        #     front_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
        #     front_true = True
        #     device_use = pred_front.device
        # if pred_top != None and pred_top.shape[0]:
        #     top_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
        #     top_true = True
        #     device_use = pred_top.device
        # if pred_side != None and pred_side.shape[0]:
        #     side_preds, objects_side = self.assign_labels(frame_side, pred_side, names_label)
        #     side_true = True
        #     device_use = pred_side.device
        #
        #
        # self.rtmp_push_fun(top_img=frame_top,front_img=frame_front,side_img=frame_side,
        #                    top_preds=top_preds,front_preds=front_preds,side_preds=side_preds)

        if top_true or front_true or side_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分
            # [top_preds, side_preds, front_preds], [top_img0, side_img0, front_img0] = preds, img0s
            if top_true:
                head_top, hand_top, ticker_timer_top, paper_tape_top, ruler_top, setsquare_top, pen_top, hand_pen_top, \
                irosupport_top, weight_top, weight_paper_top, push_button_top, desktop_top =  self.preds_top #top_preds

            if side_true:
                head_side, hand_side, ticker_timer_side, paper_tape_side, ruler_side, setsquare_side, pen_side, \
                hand_pen_side, irosupport_side, weight_side, weight_paper_side, push_button_side, desktop_side = self.preds_side

            if front_true:
                head_front, hand_front, ticker_timer_front, paper_tape_front, ruler_front, setsquare_front, \
                pen_front, hand_pen_front, \
                irosupport_front, weight_front, weight_paper_front, push_button_front, desktop_front = self.preds_front

            """
            1、把打点计时器竖直地固定在铁架台上        ticker_timer_top irosupport_top desktop_top
             打点计时器，卡槽铁架台存在且相交，并且位于桌面边缘
            2、正确连线,检查振动片工作是否正常        
              手按压开关出现      
            3、纸带下端固定重物，上端穿过限位孔，上提纸带使重物靠近打点计时器  
             纸带靠近边缘，重物纸带靠近打点计时器，按压开关发生
            4、先接通电源,然后让重物由静止开始自由下落   
              按压开关发生，纸带靠近边缘且较长（一直保留此图，直到纸带消失前且低头捡纸带）
            5、打完一条纸带,及时断开电源    
               纸带到桌面上，或者再次由按压开关发生
            6、正确选择纸带,标上五个记数点  
                纸带，手拿笔同时发生且第一次发生相交（或直尺同时出现）
            7、正确测量出各个要求的距离                
              纸带、手拿笔、直尺同时出现且相交
            8、计算UB、UD ，并填入表格           
                 默认给分，可以从小白获取数值
            9、计算物体从B点到D点减少的重力势能减少量和相应动能的增加量,比较后能得出正确结论
                默认给分，可以从小白获取数值
            10、布列器材便于操作；取放仪器运作规范；操作有条不紊；遵守纪律；做完实验，整理复原器材 
                在1，5发生后，且打点计时器；卡槽等放到桌面不在边缘                     
            """
            if not self.flag_weight_paper and \
                    ((top_true and weight_paper_top.shape[0] != 0 and weight_paper_top[0][5] > 0.5)
                     or (side_true and weight_paper_side.shape[0] != 0 and weight_paper_side[0][5] > 0.5)
                     or (front_true and weight_paper_front.shape[0] != 0 and weight_paper_front[0][5] > 0.5)
                    ):
                self.flag_weight_paper = True

            if top_true and desktop_top.shape[0] != 0 and desktop_top[0][5] > 0.7:
                self.desktop_info = desktop_top[0]
            # 1、把打点计时器竖直地固定在铁架台上        folded_filter_paper和funnel存在且交并比不为0
            if not self.scorePoint1 and top_true and front_true:
                if ticker_timer_top.shape[0] != 0 and irosupport_top.shape[0] != 0 \
                        and ticker_timer_front.shape[0] != 0 and irosupport_front.shape[0] != 0:
                    if (((ticker_timer_front[0][3] - ticker_timer_front[0][1]) >
                         (ticker_timer_front[0][2] - ticker_timer_front[0][0]) * 4 / 3 or
                         ((ticker_timer_front[0][3] - ticker_timer_front[0][1]) > 30))  # 打点计时器竖直固定
                            and
                            irosupport_front[0][3] > ticker_timer_front[0][1] and
                            irosupport_front[0][3] + (irosupport_front[0][2] - irosupport_front[0][0]) * 3 / 2
                            < ticker_timer_front[0][3] and
                            ticker_timer_top[0][1] < self.desktop_info[3] and
                            ticker_timer_top[0][3] > self.desktop_info[3] + (
                                    ticker_timer_top[0][3] - ticker_timer_top[0][1]) / 4 and
                            irosupport_top[0][3] > self.desktop_info[3] and
                            irosupport_top[0][3] > ticker_timer_top[0][1] and
                            irosupport_top[0][0] > ticker_timer_top[0][0] and
                            irosupport_top[0][0] < ticker_timer_top[0][2]
                            and irosupport_top[0][1] > ticker_timer_top[0][1] and
                            irosupport_top[0][3] < ticker_timer_top[0][3]):
                        self.scorePoint1 = True
                        # self.assignScore(1, top_img0, top_preds)
                        # self.assignScore(1, front_img0, front_preds)
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
                        return

            # 2、正确连线,检查振动片工作是否正常
            if not self.scorePoint2 and self.flag_weight_paper and ((front_true and weight_front.shape[0] == 0 and
                                                                     weight_paper_front.shape[
                                                                         0] == 0) or not front_true):
                if top_true and push_button_top.shape[0] != 0:
                    self.scorePoint2 = True
                    # self.assignScore(2, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=2,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="2.jpg",
                                     preds=self.preds_top
                                     )
                    return
                elif side_true and push_button_side.shape[0] != 0:
                    self.scorePoint2 = True
                    # self.assignScore(2, side_img0, side_preds)
                    conf_c = 0.1
                    self.assignScore(index=2,
                                     img=self.frame_side,
                                     object=self.objects_side,
                                     conf=conf_c,
                                     time_frame=self.time_side,
                                     num_frame=self.num_frame_side,
                                     name_save="2.jpg",
                                     preds=self.preds_side
                                     )
                    return
                elif front_true and push_button_front.shape[0] != 0:
                    self.scorePoint2 = True
                    # self.assignScore(2, front_img0, front_preds)
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
                    return

            # 3、纸带下端固定重物，上端穿过限位孔，上提纸带使重物靠近打点计时器
            if self.scorePoint1 and self.scorePoint2 and not self.scorePoint3 and self.flag_weight_paper \
                    and front_true and weight_front.shape[0] == 0 and \
                    weight_paper_front.shape[0] == 0:
                if top_true and push_button_top.shape[0] != 0:
                    self.scorePoint3 = True
                    # self.assignScore(3, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=3,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="3.jpg",
                                     preds=self.preds_top
                                     )
                elif side_true and push_button_side.shape[0] != 0:
                    self.scorePoint3 = True
                    # self.assignScore(3, side_img0, side_preds)
                    conf_c = 0.1
                    self.assignScore(index=3,
                                     img=self.frame_side,
                                     object=self.objects_side,
                                     conf=conf_c,
                                     time_frame=self.time_side,
                                     num_frame=self.num_frame_side,
                                     name_save="3.jpg",
                                     preds=self.preds_side
                                     )
                elif front_true and push_button_front.shape[0] != 0:
                    self.scorePoint3 = True
                    # self.assignScore(3, front_img0, front_preds)
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
                if top_true and paper_tape_top.shape[0] != 0 and desktop_top.shape[0] != 0 and \
                        paper_tape_top[0][3] > desktop_top[0][3] and \
                        (ticker_timer_top.shape[0] != 0 and \
                         abs(paper_tape_top[0][0] - ticker_timer_top[0][0]) < \
                         (ticker_timer_top[0][2] - ticker_timer_top[0][0])) and \
                        (ticker_timer_top[0][3] / 2 + ticker_timer_top[0][1] / 2 < paper_tape_top[0][3]):
                    self.scorePoint3 = True
                    # self.assignScore(3, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=3,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="3.jpg",
                                     preds=self.preds_top
                                     )

                if side_true and weight_paper_side.shape[0] != 0 and desktop_side.shape[0] != 0:
                    f_x = (desktop_side[0][2] - desktop_side[0][0]) / 3 / (desktop_side[0][3] - desktop_side[0][1])
                    if weight_paper_side[0][2] > \
                            desktop_side[0][2] - f_x * (desktop_side[0][3] - weight_paper_side[0][3]):
                        self.scorePoint3 = True
                        # self.assignScore(3, side_img0, side_preds)
                        conf_c = 0.1
                        self.assignScore(index=3,
                                         img=self.frame_side,
                                         object=self.objects_side,
                                         conf=conf_c,
                                         time_frame=self.time_side,
                                         num_frame=self.num_frame_side,
                                         name_save="3.jpg",
                                         preds=self.preds_side
                                         )

            # 4、先接通电源,然后让重物由静止开始自由下落
            if self.scorePoint1 and not self.scorePoint4 and front_true and weight_front.shape[0] == 0 and \
                    weight_paper_front.shape[0] == 0:
                if top_true and push_button_top.shape[0] != 0:
                    self.scorePoint4 = True
                    # self.assignScore(4, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=4,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="4.jpg",
                                     preds=self.preds_top
                                     )
                    return
                elif side_true and push_button_side.shape[0] != 0:
                    self.scorePoint4 = True
                    # self.assignScore(4, side_img0, side_preds)
                    conf_c = 0.1
                    self.assignScore(index=4,
                                     img=self.frame_side,
                                     object=self.objects_side,
                                     conf=conf_c,
                                     time_frame=self.time_side,
                                     num_frame=self.num_frame_side,
                                     name_save="4.jpg",
                                     preds=self.preds_side
                                     )
                    return
                elif front_true and push_button_front.shape[0] != 0:
                    self.scorePoint4 = True
                    # self.assignScore(4, front_img0, front_preds)
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
                    return

            # just if have picked the papertap
            if self.scorePoint4 and not self.scorePoint5:
                self.num_picked += 1
                if front_true and hand_front.shape[0] == 0:
                    self.flag_picked = True

            # 5、打完一条纸带,及时断开电源
            if self.scorePoint4 and not self.scorePoint5 and (self.flag_picked or self.num_picked > 1):
                if top_true and push_button_top.shape[0] != 0:
                    self.scorePoint5 = True
                    # self.assignScore(5, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=5,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="5.jpg",
                                     preds=self.preds_top
                                     )
                    return
                elif side_true and push_button_side.shape[0] != 0:
                    self.scorePoint5 = True
                    # self.assignScore(5, side_img0, side_preds)
                    conf_c = 0.1
                    self.assignScore(index=5,
                                     img=self.frame_side,
                                     object=self.objects_side,
                                     conf=conf_c,
                                     time_frame=self.time_side,
                                     num_frame=self.num_frame_side,
                                     name_save="5.jpg",
                                     preds=self.preds_side
                                     )
                    return
                elif front_true and push_button_front.shape[0] != 0:
                    self.scorePoint5 = True
                    # self.assignScore(5, front_img0, front_preds)
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
                    return

            # 6、正确选择纸带,标上五个记数点
            if not self.scorePoint6:
                if top_true and paper_tape_top.shape[0] != 0 and hand_pen_top.shape[0] != 0 and \
                        iou(paper_tape_top[0][:4], hand_pen_top[0][:4]) > 25:  # todo
                    self.scorePoint6 = True
                    # self.assignScore(6, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=6,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="6.jpg",
                                     preds=self.preds_top
                                     )
                    return

            # count num after 6
            if self.scorePoint6:
                self.num_7 += 1

            # print("num7:: {} num8:{} num9:{}".format(self.num_7,self.num_8,self.num_9))
            # 7、正确测量出各个要求的距离
            if not self.scorePoint7 and self.scorePoint3 and self.num_7 > 1:
                if top_true and paper_tape_top.shape[0] != 0 and hand_pen_top.shape[0] != 0 and \
                        (ruler_top.shape[0] != 0 or setsquare_top.shape[0] != 0) and \
                        iou(paper_tape_top[0][:4], hand_pen_top[0][:4]) > 15:
                    for item_ruler in ruler_top:
                        if iou(item_ruler[:4], paper_tape_top[0][:4]) > 15:
                            # (item_ruler[2] - item_ruler[0]) * (item_ruler[3] - item_ruler[1])/3:
                            self.scorePoint7 = True
                            # self.assignScore(7, top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=self.frame_top,
                                             object=self.objects_top,
                                             conf=conf_c,
                                             time_frame=self.time_top,
                                             num_frame=self.num_frame_top,
                                             name_save="7.jpg",
                                             preds=self.preds_top
                                             )
                            break
                    if self.scorePoint7:
                        return
                    for item_setsquare in setsquare_top:
                        if iou(item_setsquare[:4], paper_tape_top[0][:4]) > 15:
                            self.scorePoint7 = True
                            # self.assignScore(7,  top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=self.frame_top,
                                             object=self.objects_top,
                                             conf=conf_c,
                                             time_frame=self.time_top,
                                             num_frame=self.num_frame_top,
                                             name_save="7.jpg",
                                             preds=self.preds_top
                                             )
                            break
                    if self.scorePoint7:
                        return

                if side_true and paper_tape_side.shape[0] != 0 and hand_pen_side.shape[0] != 0 and \
                        (ruler_side.shape[0] != 0 or setsquare_side.shape[0] != 0) and \
                        iou(paper_tape_side[0][:4], hand_pen_side[0][:4]) > 15:
                    for item_ruler in ruler_side:
                        if iou(item_ruler[:4], paper_tape_side[0][:4]) > 15:
                            # (item_ruler[2] - item_ruler[0]) * (item_ruler[3] - item_ruler[1])/3:
                            self.scorePoint7 = True
                            # self.assignScore(7, top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=self.frame_side,
                                             object=self.objects_side,
                                             conf=conf_c,
                                             time_frame=self.time_side,
                                             num_frame=self.num_frame_side,
                                             name_save="7.jpg",
                                             preds=self.preds_side
                                             )
                            break
                    if self.scorePoint7:
                        return
                    for item_setsquare in setsquare_side:
                        if iou(item_setsquare[:4], paper_tape_side[0][:4]) > 15:
                            self.scorePoint7 = True
                            # self.assignScore(7,  top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=self.frame_side,
                                             object=self.objects_side,
                                             conf=conf_c,
                                             time_frame=self.time_side,
                                             num_frame=self.num_frame_side,
                                             name_save="7.jpg",
                                             preds=self.preds_side
                                             )
                            break
                    if self.scorePoint7:
                        return

            # count num after 7
            if self.scorePoint7:
                self.num_8 += 1

            # 8、计算UB、UD ，并填入表格
            if not self.scorePoint8 and self.scorePoint7 and self.num_8 > 10 and top_true and hand_pen_top.shape[
                0] != 0:
                self.scorePoint8 = True
                # self.assignScore(8, top_img0, top_preds)
                conf_c = 0.1
                self.assignScore(index=8,
                                 img=self.frame_top,
                                 object=self.objects_top,
                                 conf=conf_c,
                                 time_frame=self.time_top,
                                 num_frame=self.num_frame_top,
                                 name_save="8.jpg",
                                 preds=self.preds_top
                                 )
                return

            # count num after 8
            if self.scorePoint8:
                self.num_9 += 1
            # 9、计算物体从B点到D点减少的重力势能减少量和相应动能的增加量,比较后能得出正确结论
            if not self.scorePoint9 and self.scorePoint8 and self.num_9 > 5 and top_true and hand_pen_top.shape[0] != 0:
                self.scorePoint9 = True
                # self.assignScore(9, top_img0, top_preds)
                conf_c = 0.1
                self.assignScore(index=9,
                                 img=self.frame_top,
                                 object=self.objects_top,
                                 conf=conf_c,
                                 time_frame=self.time_top,
                                 num_frame=self.num_frame_top,
                                 name_save="9.jpg",
                                 preds=self.preds_top
                                 )
                return

            # 10、布列器材便于操作；取放仪器运作规范；操作有条不紊；遵守纪律；做完实验，整理复原器材
            if not self.scorePoint10 and self.scorePoint9:
                if top_true and irosupport_top.shape[0] != 0 and desktop_top.shape[0] != 0 and \
                        box1_in_box2(irosupport_top[0][:4], desktop_top[0][:4]):
                    self.scorePoint10 = True
                    # self.assignScore(10, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=10,
                                     img=self.frame_top,
                                     object=self.objects_top,
                                     conf=conf_c,
                                     time_frame=self.time_top,
                                     num_frame=self.num_frame_top,
                                     name_save="10.jpg",
                                     preds=self.preds_top
                                     )
                    self.clean_desk = {}
                    return

            if not self.scorePoint9 and self.scorePoint5:
                if top_true and irosupport_top.shape[0] != 0 and desktop_top.shape[0] != 0 and \
                        box1_in_box2(irosupport_top[0][:4], desktop_top[0][:4]):
                    self.scorePoint10 = True
                    # self.assignScore(10, top_img0, top_preds)
                    conf_c = 0.1
                    # self.assignScore(index=10,
                    #                  img=self.frame_top,
                    #                  object=self.objects_top,
                    #                  conf=conf_c,
                    #                  time_frame=self.time_top,
                    #                  num_frame=self.num_frame_top,
                    #                  name_save="10.jpg",
                    #                  preds=self.preds_top
                    #                  )
                    self.clean_desk={"index":10,"img":self.frame_top,"object":self.objects_top,
                                     "conf":conf_c,"time_frame":self.time_top,"num_frame":self.num_frame_top,
                                     "name_save":"10.jpg","preds":self.preds_top}
                    return

    def end(self):
        if "index" in self.clean_desk.keys():
            self.assignScore(index=self.clean_desk["index"],
                             img=self.clean_desk["img"],
                             object=self.clean_desk["object"],
                             conf=self.clean_desk["conf"],
                             time_frame=self.clean_desk["time_frame"],
                             num_frame=self.clean_desk["num_frame"],
                             name_save=self.clean_desk["name_save"],
                             preds=self.clean_desk["preds"],
                             )
