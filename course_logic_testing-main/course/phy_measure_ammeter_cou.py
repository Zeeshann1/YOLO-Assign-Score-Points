#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : Qinhe
# @File    : phy_measure_ammeter_conf.py


import random
from .comm import *
from .comm.course_base import ConfigModel


# from config.phy_measure_ammeter_conf import PYDLBCDL01
# from utilsg.litF import uploaded_images, encode_image_jpg, upload_redis_or_save_json_local, ts2ft
# from configg.global_config import SCORE_ROOT_PATH
# from .comm import Plot
# from logger import logger

import copy

class PHY_measure_ammeter(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_measure_ammeter, self).__init__()

        self.initScore()

    def initScore(self):
        self.flag1 = []  # 导线两节器材
        self.flag2 = []  # series 串联
        self.flag3 = ''  # min or max
        self.flag4 = 0  # min_num
        self.flag5 = 0  # max_num
        self.flag6 = []  # 正负极
        self.flag7 = []  # 正负极
        self.flag8 = False  # 桌面有东西
        self.flag9 = 0
        self.flag11 = 0
        self.flag12 = 0
        self.flag13 = 0

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
        side_true = False
        device_use = "cuda: 0"
        front1_preds = None
        top_preds = None
        side_preds = None
        if pred_front != None and pred_front.shape[0]:
            front1_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            front_true = True
            device_use = pred_front.device
        if pred_top != None and pred_top.shape[0]:
            top_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
            top_true = True
            device_use = pred_top.device
        if pred_side != None and pred_side.shape[0]:
            side_preds, objects_side = self.assign_labels(frame_side, pred_side, names_label)
            side_true = True
            device_use = pred_side.device

        self.rtmp_push_fun(top_img=frame_top,front_img=frame_front,side_img=frame_side,
                           top_preds=top_preds,front_preds=front1_preds,side_preds=side_preds)

        if top_true or front_true or side_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分
            # [top_preds, side_preds, front1_preds], [top_img0, side_img0, front_img0] = preds, img0s # 检测框和ing
            if not self.set_center_box:
                h, w = frame_top.shape[:2]
                self.center_box = torch.tensor([w * 0.33, h * 0.45, w * 0.72, h * 0.87],
                                               device=device_use)  ## 桌面实验区域，该区域没有物品代表已经整理桌面
                self.set_center_box = True
            if top_true:
                power_source_top, binding_post_red_top, binding_post_black_top, \
                wire_connection_red_top, wire_connection_black_top, \
                switch_off_top, switch_on_top, \
                ammeter_top, min_top, max_top, pointer_offset_top, pointer_zero_top, \
                slide_rheostat_top, gleithretter_top, \
                above_top, following_top, connect_above_top, connect_following_top, \
                clean_desk_top, wire_connection_top = top_preds

            if front_true:
                power_source_front, binding_post_red_front, binding_post_black_front, \
                wire_connection_red_front, wire_connection_black_front, \
                switch_off_front, switch_on_front, \
                ammeter_front, min_front, max_front, pointer_offset_front, pointer_zero_front, \
                slide_rheostat_front, gleithretter_front, \
                above_front, following_front, connect_above_front, connect_following_front, \
                clean_desk_front, wire_connection_front = front1_preds

            if side_true:
                power_source_side, binding_post_red_side, binding_post_black_side, \
                wire_connection_red_side, wire_connection_black_side, \
                switch_off_side, switch_on_side, \
                ammeter_side, min_side, max_side, pointer_offset_side, pointer_zero_side, \
                slide_rheostat_side, gleithretter_side, \
                above_side, following_side, connect_above_side, connect_following_side, \
                clean_desk_side, wire_connection_side = side_preds

            # 开关，小灯泡，指针，min（point4） 只保留一个box

            class_name = ['power_source_top', 'binding_post_red_top', 'binding_post_black_top',
                          'wire_connection_red_top', 'wire_connection_black_top',
                          'switch_off_top', 'switch_on_top',
                          'ammeter_top', 'min_top', 'max_top', 'pointer_offset_top', 'pointer_zero_top',
                          'slide_rheostat_top', 'gleithretter_top',
                          'above_top', 'following_top', 'connect_above_top', 'connect_following_top',
                          'clean_desk_top', 'wire_connection_top']
            # self.flag9 += 1

            # 1.电路连接时开关处于闭合状态
            # 开关使用side或者top, 开关判断依据待确定
            if not self.scorePoint1 and not self.scorePoint6:
                if ((front_true and switch_off_front.shape[0] != 0) or (
                        side_true and switch_off_side.shape[0] != 0)) and \
                        (top_true and wire_connection_top.shape[0] != 0 and wire_connection_red_top.shape[0] != 0 and
                         wire_connection_black_top.shape[0] != 0):  #
                    if switch_off_top.shape[0] != 0 and front_true and switch_off_front.shape[0] != 0:
                        self.scorePoint1 = True
                        # self.assignScore(1, front_img0, front1_preds)
                        conf_c = 0.1
                        self.assignScore(index=1,
                                         img=frame_front,
                                         object=objects_front,
                                         conf=conf_c,
                                         time_frame=time_front,
                                         num_frame=num_frame_front,
                                         name_save="1.jpg",
                                         preds=front1_preds
                                         )
                    elif switch_off_top.shape[0] != 0 and side_true and switch_off_side.shape[0] != 0:
                        self.scorePoint1 = True
                        # self.assignScore(1, side_img0, side_preds)
                        conf_c = 0.1
                        self.assignScore(index=1,
                                         img=frame_side,
                                         object=objects_side,
                                         conf=conf_c,
                                         time_frame=time_side,
                                         num_frame=num_frame_side,
                                         name_save="1.jpg",
                                         preds=side_preds
                                         )

            if not self.scorePoint2 or not self.scorePoint5:
                if top_true and wire_connection_top.shape[0] != 0:
                    for connection_top in wire_connection_top:  # 已连接的导线
                        connection_top_box = connection_top[:4]
                        equipments = []  # 器材
                        connection_posts = []  # 连接导线的接线柱
                        points = []  # 器材——'导线'——器材

                        # 提取与导线有交集的器材   一根导线和N个器材
                        for items in [power_source_top, switch_off_top, switch_on_top, ammeter_top, slide_rheostat_top]:
                            if items.shape[0] != 0:  # items is power_source_top and
                                for item in items:
                                    item_box = item[:4]
                                    wc_iou = iou(connection_top_box, item_box)
                                    if wc_iou > 0:
                                        equipments.append(item)
                        # 判断导线连接的是哪个接线柱   一根导线和N个接线柱
                        for posts in [wire_connection_red_top, wire_connection_black_top,
                                      connect_above_top, connect_following_top]:
                            if posts.shape[0] != 0:
                                for post in posts:
                                    post_box = post[:4]
                                    wc_p_iou = iou(connection_top_box, post_box)
                                    if wc_p_iou > 0:
                                        connection_posts.append(post)
                        # 确定器材和接线柱  有限器材和有限接线柱
                        if len(equipments) >= 2 and len(connection_posts) >= 2:
                            for equ in equipments:
                                for post in connection_posts:
                                    e_r_iou = iou(equ[:4], post[:4])
                                    if e_r_iou > 0:
                                        point = str(class_name[int(equ[5])].split('_')[0] + '_' +
                                                    class_name[int(post[5])].split('_')[-2])  # class_name
                                        points.append(point)
                        # 确定一根导线连接两个器材
                        if len(points) == 2 and points not in self.flag1 and \
                                points[-1].split('_')[0] != points[0].split('_')[0]:
                            self.flag1.append(points)

            # 2.电源，开关，滑动变阻器，电流表串联
            if not self.scorePoint2 and len(self.flag1) != 0:
                # 从U+到U-，跳过V
                # 判断串联
                '''
                ### 可以有两个above或量following   未写入
                '''
                series = copy.deepcopy(self.flag1)
                for serie in series:
                    if len(self.flag2) == 0 and ('power_red' in serie or 'power_black' in serie):
                        if serie[1] in ['power_red', 'power_black']:
                            serie[0], serie[1] = serie[1], serie[0]
                        s = copy.deepcopy(serie)
                        self.flag2.append(s)
                        continue

                    if len(self.flag2) != 0:
                        if (self.flag2[-1][0].split('_')[0] == serie[-1].split('_')[0] or
                            self.flag2[-1][0].split('_')[0] == serie[0].split('_')[0]) and \
                                self.flag2[-1] in self.flag1 and self.flag2[-1] in self.flag2:  # 构成回路后删除串联列表中最后一个
                            self.flag1.remove(self.flag2[-1])
                            self.flag2.remove(self.flag2[-1])
                            continue
                        if self.flag2[-1][-1].split('_')[0] == serie[0].split('_')[0] and \
                                (self.flag2[-1][-1] != serie[0] or self.flag2[-1][-1] == serie[0] == 'slide_above'
                                 or self.flag2[-1][-1] == serie[0] == 'slide_following'):  # 连接在同一器材上并且不是回路
                            self.flag2.append(serie)
                        elif self.flag2[-1][-1].split('_')[0] == serie[1].split('_')[0] and \
                                self.flag2[-1][-1] != serie[1]:
                            serie[0], serie[1] = serie[1], serie[0]
                            self.flag2.append(serie)
                    if len(self.flag2) != 0 and self.flag2[-1][-1] in ['power_red', 'power_black'] \
                            and self.flag2[0][0] != self.flag2[-1][-1]:
                        self.scorePoint2 = True
                        # print(f'{self.flag9}, serie, flag2: {self.flag2}')  # debug
                        # self.assignScore(2, top_img0, top_preds)
                        conf_c = 0.1
                        self.assignScore(index=2,
                                         img=frame_top,
                                         object=objects_top,
                                         conf=conf_c,
                                         time_frame=time_top,
                                         num_frame=num_frame_top,
                                         name_save="2.jpg",
                                         preds=top_preds
                                         )
                        break
                    if len(self.flag2) >= 5:  #
                        for flag2 in self.flag2:
                            if flag2 not in self.flag1:
                                continue
                            self.flag1.remove(flag2)
                        self.flag2.clear()

            # 3.滑动变阻器接入正确且电阻最大
            # 发生在开关闭合之前，
            # 电阻最大由滑片到following和connect_following的距离判断（顶视或侧视或前视）
            # 接入正确
            if not self.scorePoint3 and not self.scorePoint6:
                Plug_rheostat_top, Plug_rheostat_side, Plug_rheostat_front = False, False, False
                Rmax_top, Rmax_side, Rmax_front = False, False, False
                # 接入正确
                if top_true and connect_above_top.shape[0] == 1 and connect_following_top.shape[0] == 1:  # 添加第一个连接的组合
                    Plug_rheostat_top = True
                if side_true and connect_above_side.shape[0] == 1 and connect_following_side.shape[
                    0] == 1:  # 添加第一个连接的组合
                    Plug_rheostat_side = True
                if front_true and connect_above_front.shape[0] == 1 and connect_following_front.shape[
                    0] == 1:  # 添加第一个连接的组合
                    Plug_rheostat_front = True

                # Rmax  求滑片、following连接线与following、connect_following连接线的夹角
                if top_true and following_top.shape[0] != 0 and connect_following_top.shape[0] != 0 and \
                        gleithretter_top.shape[0] != 0:
                    following_top_box = following_top[0][:4]
                    connect_following_top_box = connect_following_top[0][:4]
                    gleithretter_top_box = gleithretter_top[0][:4]
                    oa = int(distance_box(following_top_box, gleithretter_top_box))
                    ob = int(distance_box(following_top_box, connect_following_top_box))
                    ab = int(distance_box(gleithretter_top_box, connect_following_top_box))
                    if oa * ob * ab == 0:
                        # break
                        return
                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                    if 0.25 > coso > -1:
                        Rmax_top = True

                if side_true and following_side.shape[0] != 0 and connect_following_side.shape[0] != 0 and \
                        gleithretter_side.shape[0] != 0:
                    following_side_box = following_side[0][:4]
                    connect_following_side_box = connect_following_side[0][:4]
                    gleithretter_side_box = gleithretter_side[0][:4]
                    oa = int(distance_box(following_side_box, gleithretter_side_box))
                    ob = int(distance_box(following_side_box, connect_following_side_box))
                    ab = int(distance_box(gleithretter_side_box, connect_following_side_box))
                    if oa * ob * ab == 0:
                        # break
                        return
                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                    if 0.25 > coso > -1:
                        Rmax_side = True

                if front_true and following_front.shape[0] != 0 and connect_following_front.shape[0] != 0 and \
                        gleithretter_front.shape[0] != 0:
                    following_front_box = following_front[0][:4]
                    connect_following_front_box = connect_following_front[0][:4]
                    gleithretter_front_box = gleithretter_front[0][:4]
                    oa = int(distance_box(following_front_box, gleithretter_front_box))
                    ob = int(distance_box(following_front_box, connect_following_front_box))
                    ab = int(distance_box(gleithretter_front_box, connect_following_front_box))
                    if oa * ob * ab == 0:
                        # break
                        return
                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                    if 0.25 > coso > -1:
                        Rmax_front = True

                # 接入正确，Rmax，提交图片
                if Plug_rheostat_top and Rmax_top and not self.scorePoint3:
                    self.scorePoint3 = True
                    # self.assignScore(3, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=3,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="3.jpg",
                                     preds=top_preds
                                     )
                if Plug_rheostat_side and Rmax_side and not self.scorePoint3:
                    self.scorePoint3 = True
                    # self.assignScore(3, side_img0, side_preds)
                    conf_c = 0.1
                    self.assignScore(index=3,
                                     img=frame_side,
                                     object=objects_side,
                                     conf=conf_c,
                                     time_frame=time_side,
                                     num_frame=num_frame_side,
                                     name_save="3.jpg",
                                     preds=side_preds
                                     )
                if Plug_rheostat_front and Rmax_front and not self.scorePoint3:
                    self.scorePoint3 = True
                    # self.assignScore(3, front_img0, front1_preds)
                    conf_c = 0.1
                    self.assignScore(index=1,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="1.jpg",
                                     preds=top_preds
                                     )

            # 4.电流表选择合适量程
            if not self.scorePoint4:
                # 从V+到VCC+，或者V-到VCC-
                if top_true and power_source_top.shape[0] != 0:
                    num = 0
                    for power_source in power_source_top:
                        power_source_box = power_source[:4]
                        c_p_iou = iou(self.center_box, power_source_box)
                        if c_p_iou > 0:
                            num += 1

                    # 判断一个电源还是两个电源，统计帧数，差的绝对值，比较出现次数
                    if num == 1:
                        self.flag4 += 1
                    elif num >= 1:
                        self.flag5 += 1
                    if abs(self.flag4 - self.flag5) > 15:
                        self.flag3 = 'min' if self.flag4 > self.flag5 else 'max'

                if self.flag3 != '' and top_true and ammeter_top.shape[0] != 0 and wire_connection_top.shape[0] != 0:
                    ammeter_top_box = ammeter_top[0][:4]
                    # 电流表与导线有交集
                    ac = 0
                    for connection_top in wire_connection_top:
                        connection_top_box = connection_top[:4]
                        a_c_iou = iou(ammeter_top_box, connection_top_box)
                        if a_c_iou > 0:
                            ac += 1

                    # 已连接的红色接线柱与电流表有交集
                    connection_red = []
                    post_red = []
                    connection_black = []
                    post_black = []
                    if wire_connection_red_top.shape[0] != 0:
                        for connection_red_top in wire_connection_red_top:
                            connection_red_top_box = connection_red_top[:4]
                            a_cr_iou = iou(ammeter_top_box, connection_red_top_box)
                            if a_cr_iou > 0:
                                connection_red.append(connection_red_top_box)

                    # 根据config，只选取一个range
                    if min_top.shape[0] != 0 and max_top.shape[0] != 0:
                        range = 'min' if min_top[0][4] > max_top[0][4] else 'max'
                    elif min_top.shape[0] != 0 and max_top.shape[0] == 0:
                        range = 'min'
                    elif min_top.shape[0] == 0 and max_top.shape[0] != 0:
                        range = 'max'

                    if len(connection_red) == 1 and ac > 0 and binding_post_red_top.shape[0] != 0:
                        for post_red_top in binding_post_red_top:  # 未连接的红色接线柱与电流表有交集
                            post_red_top_box = post_red_top[:4]
                            a_pr_iou = iou(ammeter_top_box, post_red_top_box)
                            if a_pr_iou > 0:
                                post_red.append(post_red_top_box)
                        if len(post_red) == 1:  # 使用‘红色接线柱’判断量程
                            oa = int(distance_box(connection_red[0], ammeter_top_box))
                            ob = int(distance_box(connection_red[0], post_red[0]))
                            ab = int(distance_box(ammeter_top_box, post_red[0]))
                            coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                            if self.flag3 == 'min' and 0.25 > coso > -0.25 and range == 'min':  # 70-105度
                                # print(f'{self.flag9}, {self.flag3}, min,  red')  # debug
                                self.scorePoint4 = True
                                # self.assignScore(4, top_img0, top_preds)
                                conf_c = 0.1
                                self.assignScore(index=4,
                                                 img=frame_top,
                                                 object=objects_top,
                                                 conf=conf_c,
                                                 time_frame=time_top,
                                                 num_frame=num_frame_top,
                                                 name_save="4.jpg",
                                                 preds=top_preds
                                                 )

                            elif self.flag3 == 'max' and 0.87 > coso > 0.34 and range == 'max':  # 30-70度
                                # print(f'{self.flag9}, {self.flag3}, max,  red')  # debug
                                self.scorePoint4 = True
                                # self.assignScore(4, top_img0, top_preds)
                                conf_c = 0.1
                                self.assignScore(index=4,
                                                 img=frame_top,
                                                 object=objects_top,
                                                 conf=conf_c,
                                                 time_frame=time_top,
                                                 num_frame=num_frame_top,
                                                 name_save="4.jpg",
                                                 preds=top_preds
                                                 )

                        elif len(post_red) == 0 and binding_post_black_top.shape[0] != 0:
                            for post_black_top in binding_post_black_top:  # 未连接的黑色接线柱与电流表有交集
                                post_black_top_box = post_black_top[:4]
                                v_pb_iou = iou(ammeter_top_box, post_black_top_box)
                                if v_pb_iou > 0:
                                    post_black.append(post_black_top_box)
                            if len(post_black) == 1:  # 使用‘黑色接线柱’判断量程
                                oa = int(distance_box(connection_red[0], ammeter_top_box))
                                ob = int(distance_box(connection_red[0], post_black[0]))
                                ab = int(distance_box(ammeter_top_box, post_black[0]))
                                coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                                if self.flag3 == 'min' and 0.25 > coso > -0.25 and range == 'min':  # 70-105度
                                    # print(f'{self.flag9}, {self.flag3}, min,  black')  # debug
                                    self.scorePoint4 = True
                                    # self.assignScore(4, top_img0, top_preds)
                                    conf_c = 0.1
                                    self.assignScore(index=4,
                                                     img=frame_top,
                                                     object=objects_top,
                                                     conf=conf_c,
                                                     time_frame=time_top,
                                                     num_frame=num_frame_top,
                                                     name_save="4.jpg",
                                                     preds=top_preds
                                                     )

                                elif self.flag3 == 'max' and 0.87 > coso > 0.34 and range == 'max':  # 30-70度
                                    # print(f'{self.flag9}, {self.flag3}, max,  black')  # debug
                                    self.scorePoint4 = True
                                    # self.assignScore(4, top_img0, top_preds)
                                    conf_c = 0.1
                                    self.assignScore(index=4,
                                                     img=frame_top,
                                                     object=objects_top,
                                                     conf=conf_c,
                                                     time_frame=time_top,
                                                     num_frame=num_frame_top,
                                                     name_save="4.jpg",
                                                     preds=top_preds
                                                     )

                            elif len(post_black) == 0 and wire_connection_black_top.shape[0] != 0:
                                for connection_black_top in wire_connection_black_top:  # 已连接的黑色接线柱与电流表有交集
                                    connection_black_top_box = connection_black_top[:4]
                                    v_pb_iou = iou(ammeter_top_box, connection_black_top_box)
                                    if v_pb_iou > 0:
                                        connection_black.append(connection_black_top_box)
                                if len(connection_black) == 1:  # 使用‘导线连接黑色接线柱’判断量程
                                    oa = int(distance_box(connection_red[0], ammeter_top_box))
                                    ob = int(distance_box(connection_red[0], connection_black[0]))
                                    ab = int(distance_box(ammeter_top_box, connection_black[0]))
                                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                                    if self.flag3 == 'min' and 0.25 > coso > -0.25 and range == 'min':  # 70-105度
                                        # print(f'{self.flag9}, {self.flag3}, min,  connection black')  # debug
                                        self.scorePoint4 = True
                                        # self.assignScore(4, top_img0, top_preds)
                                        conf_c = 0.1
                                        self.assignScore(index=4,
                                                         img=frame_top,
                                                         object=objects_top,
                                                         conf=conf_c,
                                                         time_frame=time_top,
                                                         num_frame=num_frame_top,
                                                         name_save="4.jpg",
                                                         preds=top_preds
                                                         )

                                    elif self.flag3 == 'max' and 0.87 > coso > 0.34 and range == 'max':  # 30-70度
                                        # print(f'{self.flag9}, {self.flag3}, max,  connection black')  # debug
                                        self.scorePoint4 = True
                                        # self.assignScore(4, top_img0, top_preds)
                                        conf_c = 0.1
                                        self.assignScore(index=4,
                                                         img=frame_top,
                                                         object=objects_top,
                                                         conf=conf_c,
                                                         time_frame=time_top,
                                                         num_frame=num_frame_top,
                                                         name_save="4.jpg",
                                                         preds=top_preds
                                                         )

            # 5.电流表，电源正负极连接正确
            if not self.scorePoint5 and len(self.flag1) != 0:  #
                if self.scorePoint6:
                    self.scorePoint5 = True
                    # self.assignScore(5, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=5,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="5.jpg",
                                     preds=top_preds
                                     )
                # 判断电源正负极连接
                polaritys = copy.deepcopy(self.flag1)
                if len(self.flag6) == 0:  # 添加第一个连接的组合
                    for polarity in polaritys:
                        if 'power_red' in polaritys:
                            if polarity[1] == 'power_red':  # 调整顺序
                                polarity[0], polarity[1] = polarity[1], polarity[0]
                            p = copy.deepcopy(polarity)
                            self.flag6.append(p)
                            break
                if len(self.flag7) == 0:  # 添加第一个连接的组合
                    for polarity in polaritys:
                        if 'power_black' in polarity:
                            if polarity[1] == 'power_black':  # 调整顺序
                                polarity[0], polarity[1] = polarity[1], polarity[0]
                            p = copy.deepcopy(polarity)
                            self.flag7.append(p)
                            break
                if len(self.flag6) != 0:
                    # 判断有没有两根导线连载同一接线柱上
                    for polarity_gather in self.flag6:
                        for polarity_free in polaritys:
                            # 调整parallel_free的顺序
                            for par_n in polarity_free:
                                if polarity_gather[-1].split('_')[0] == par_n.split('_')[0]:
                                    polarity_free.insert(0, polarity_free.pop(polarity_free.index(par_n)))
                                    break

                            if polarity_gather[-1].split('_')[0] == polarity_free[0].split('_')[0] and \
                                    polarity_gather[-1] != polarity_free[0]:  # 连接在同一器材上的不同接线柱上
                                self.flag6.append(polarity_free)
                            elif polarity_gather[-1].split('_')[0] == polarity_free[1].split('_')[0] and \
                                    polarity_gather[-1] != polarity_free[1]:
                                polarity_free[0], polarity_free[1] = polarity_free[1], polarity_free[0]
                                self.flag6.append(polarity_free)

                        # 判断self.flag7的头和尾
                        if self.flag6[0][0] == 'power_red' and self.flag6[-1][-1] == 'ammeter_red':
                            # print(f'{self.flag9}  polarity,   flag7: {self.flag6}')  # debug
                            self.scorePoint5 = True
                            # self.assignScore(5, top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=5,
                                             img=frame_top,
                                             object=objects_top,
                                             conf=conf_c,
                                             time_frame=time_top,
                                             num_frame=num_frame_top,
                                             name_save="5.jpg",
                                             preds=top_preds
                                             )
                            break
                        if self.flag6[0][0] == 'power_red' and self.flag6[-1][-1] == 'ammeter_black' and \
                                self.flag6[0] in self.flag1:
                            self.flag1.remove(self.flag6[0])
                            self.flag6.clear()

                if len(self.flag7) != 0:
                    # 判断有没有两根导线连载同一接线柱上
                    for polarity_gather in self.flag7:
                        for polarity_free in polaritys:
                            # 调整parallel_free的顺序
                            for par_n in polarity_free:
                                if polarity_gather[-1].split('_')[0] == par_n.split('_')[0]:
                                    polarity_free.insert(0, polarity_free.pop(polarity_free.index(par_n)))
                                    break

                            if polarity_gather[-1].split('_')[0] == polarity_free[0].split('_')[0] and \
                                    polarity_gather[-1] != polarity_free[0]:  # 连接在同一器材上的不同接线柱上
                                self.flag7.append(polarity_free)
                            elif polarity_gather[-1].split('_')[0] == polarity_free[1].split('_')[0] and \
                                    polarity_gather[-1] != polarity_free[1]:
                                polarity_free[0], polarity_free[1] = polarity_free[1], polarity_free[0]
                                self.flag7.append(polarity_free)

                        # 判断self.flag8的头和尾
                        if self.flag7[0][0] == 'power_black' and self.flag7[-1][-1] == 'ammeter_black':
                            # print(f'{self.flag9}  polarity,   flag8: {self.flag7}')  # debug
                            self.scorePoint5 = True
                            # self.assignScore(5, top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=5,
                                             img=frame_top,
                                             object=objects_top,
                                             conf=conf_c,
                                             time_frame=time_top,
                                             num_frame=num_frame_top,
                                             name_save="5.jpg",
                                             preds=top_preds
                                             )
                            break
                        if self.flag7[0][0] == 'power_black' and self.flag7[-1][-1] == 'ammeter_red' and \
                                self.flag7[0] in self.flag1:
                            self.flag1.remove(self.flag7[0])
                            self.flag7.clear()

            # 6.闭合开关，电压表指针发生偏转
            if not self.scorePoint6 and self.scorePoint1:
                if self.flag3 == 'min' and self.scorePoint3 \
                        and ((top_true  and pointer_offset_top.shape[0] != 0 ) or \
                             (side_true and pointer_offset_side.shape[0] != 0)):  #
                    self.scorePoint6 = True
                    # print(f'{self.flag9}, 闭合开关，电压表指针发生偏转, min')
                    # self.assignScore(6, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=6,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="6.jpg",
                                     preds=top_preds
                                     )

                elif self.flag3 == 'max' and self.scorePoint3  and \
                        ((top_true and pointer_offset_top.shape[0] != 0) or \
                         (side_true and pointer_offset_side.shape[0] != 0)):  #
                    self.scorePoint6 = True
                    # print(f'{self.flag9}, 闭合开关，电压表指针发生偏转, max')
                    # self.assignScore(6, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=6,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="6.jpg",
                                     preds=top_preds
                                     )

            # 7.改变滑动变阻器电阻，观察电流表示数
            # 与滑动变阻器是否为Rmax无关，关键在于滑片位置的变化，使用相对平行的水平距离
            # 发生在闭合开关，但为断开开关中间
            if self.scorePoint6 and not self.scorePoint7 and not self.scorePoint8:
                # 改变滑片位置 先求滑片、following连接线与following、connect_following连接线的夹角，
                # 再求相对水平时滑片到following的水平距离（垂直距离恒等），用位移来确定滑片位置发生改变
                if top_true and following_top.shape[0] != 0 and connect_following_top.shape[0] != 0 and \
                        gleithretter_top.shape[0] != 0 and pointer_offset_top.shape[0] != 0:
                    following_top_box = following_top[0][:4]
                    connect_following_top_box = connect_following_top[0][:4]
                    gleithretter_top_box = gleithretter_top[0][:4]
                    oa = distance_box(following_top_box, gleithretter_top_box)
                    ob = distance_box(following_top_box, connect_following_top_box)
                    ab = distance_box(gleithretter_top_box, connect_following_top_box)
                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                    dt = oa * coso
                    if self.flag11 == 0:
                        self.flag11 = dt
                    else:
                        delta_dt = dt - self.flag11

                        if delta_dt > 20:
                            self.scorePoint7 = True
                            # self.assignScore(7, top_img0, top_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=frame_top,
                                             object=objects_top,
                                             conf=conf_c,
                                             time_frame=time_top,
                                             num_frame=num_frame_top,
                                             name_save="7.jpg",
                                             preds=top_preds
                                             )

                if side_true and following_side.shape[0] != 0 and connect_following_side.shape[0] != 0 and \
                        gleithretter_side.shape[0] != 0 and top_true and pointer_offset_top.shape[0] != 0:
                    following_side_box = following_side[0][:4]
                    connect_following_side_box = connect_following_side[0][:4]
                    gleithretter_side_box = gleithretter_side[0][:4]
                    oa = distance_box(following_side_box, gleithretter_side_box)
                    ob = distance_box(following_side_box, connect_following_side_box)
                    ab = distance_box(gleithretter_side_box, connect_following_side_box)
                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                    ds = oa * coso
                    if self.flag12 == 0:
                        self.flag12 = ds
                    else:
                        delta_ds = ds - self.flag12
                        if delta_ds > 20:
                            self.scorePoint7 = True
                            # self.assignScore(7, side_img0, side_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=frame_top,
                                             object=objects_top,
                                             conf=conf_c,
                                             time_frame=time_top,
                                             num_frame=num_frame_top,
                                             name_save="7.jpg",
                                             preds=top_preds
                                             )

                if front_true and following_front.shape[0] != 0 and connect_following_front.shape[0] != 0 and \
                        gleithretter_front.shape[0] != 0 and top_true and pointer_offset_top.shape[0] != 0:
                    following_front_box = following_front[0][:4]
                    connect_following_front_box = connect_following_front[0][:4]
                    gleithretter_front_box = gleithretter_front[0][:4]
                    oa = distance_box(following_front_box, gleithretter_front_box)
                    ob = distance_box(following_front_box, connect_following_front_box)
                    ab = distance_box(gleithretter_front_box, connect_following_front_box)
                    coso = (oa * oa + ob * ob - ab * ab) / (2 * oa * ob)
                    df = oa * coso
                    if self.flag13 == 0:
                        self.flag13 = df
                    else:
                        delta_df = df - self.flag13
                        if delta_df > 20:
                            self.scorePoint7 = True
                            # self.assignScore(7, front_img0, front1_preds)
                            conf_c = 0.1
                            self.assignScore(index=7,
                                             img=frame_top,
                                             object=objects_top,
                                             conf=conf_c,
                                             time_frame=time_top,
                                             num_frame=num_frame_top,
                                             name_save="7.jpg",
                                             preds=top_preds
                                             )

            # 8.断开开关后再拆电路
            # 优化：加入时序 如self.flag3
            if not self.scorePoint8 and self.scorePoint6:
                '''if power_source_top.shape[0] != 0:
                    num = 0
                    for power_source in power_source_top:
                        power_source_box = power_source[:4]
                        c_p_iou = iou(self.center_box, power_source_box)
                        if c_p_iou > 0:
                            num += 1
                    # 判断一个电源还是两个电源，统计帧数，差的绝对值，比较出现次数
                    if num == 1:
                        self.flag4 += 1
                    elif num >= 1:
                        self.flag5 += 1
                    if abs(self.flag4 - self.flag5) > 15:
                        self.flag3 = 'min' if self.flag4 > self.flag5 else 'max'
                # 加到一个list中，只保留最新的20个，使用5元素滤波，如果开关前10个off的个数大于后十个on的个数'''
                if top_true and (switch_off_top.shape[0] != 0 or \
                        binding_post_red_top.shape[0] +  binding_post_black_top.shape[0] > 4):
                    self.scorePoint8 = True
                    # self.assignScore(8, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=8,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="8.jpg",
                                     preds=top_preds
                                     )
                if top_true and switch_off_top.shape[0] != 0 and (
                        switch_off_side.shape[0] != 0 or switch_off_front.shape[0] != 0):
                    r_a_num = 0
                    b_a_num = 0

                    if binding_post_red_top.shape[0] != 0:
                        for post_red_top in binding_post_red_top:
                            post_red_top_box = post_red_top[:4]
                            if switch_off_top.shape[0] != 0:
                                switch_off_top_box = switch_off_top[0][:4]
                                r_s_iou = iou(switch_off_top_box, post_red_top_box)
                                if r_s_iou > 0:
                                    r_a_num += 1
                            if power_source_top.shape[0] != 0:
                                power_source_top_box = power_source_top[0][:4]
                                r_p_iou = iou(power_source_top_box, post_red_top_box)
                                if r_p_iou > 0:
                                    r_a_num += 1
                            if ammeter_top.shape[0] != 0:
                                ammeter_top_box = ammeter_top[0][:4]
                                r_v_iou = iou(ammeter_top_box, post_red_top_box)
                                if r_v_iou > 0:
                                    r_a_num += 1

                    if binding_post_black_top.shape[0] != 0:
                        for post_black_top in binding_post_black_top:
                            post_black_top_box = post_black_top[:4]
                            if switch_off_top.shape[0] != 0:
                                switch_off_top_box = switch_off_top[0][:4]
                                b_s_iou = iou(switch_off_top_box, post_black_top_box)
                                if b_s_iou > 0:
                                    b_a_num += 1
                            if power_source_top.shape[0] != 0:
                                power_source_top_box = power_source_top[0][:4]
                                b_p_iou = iou(power_source_top_box, post_black_top_box)
                                if b_p_iou > 0:
                                    b_a_num += 1
                            if ammeter_top.shape[0] != 0:
                                ammeter_top_box = ammeter_top[0][:4]
                                b_v_iou = iou(ammeter_top_box, post_black_top_box)
                                if b_v_iou > 0:
                                    b_a_num += 1

                    if above_top.shape[0] != 0:
                        for above_tp in above_top:
                            above_tp_box = above_tp[:4]
                            if slide_rheostat_top.shape[0] != 0:
                                slide_rheostat_top_box = slide_rheostat_top[0][:4]
                                s_a_iou = iou(slide_rheostat_top_box, above_tp_box)
                                if s_a_iou > 0:
                                    r_a_num += 1

                    if gleithretter_top.shape[0] != 0:
                        for gleithretter_tp in gleithretter_top:
                            gleithretter_tp_box = gleithretter_tp[:4]
                            if slide_rheostat_top.shape[0] != 0:
                                slide_rheostat_top_box = slide_rheostat_top[0][:4]
                                s_g_iou = iou(slide_rheostat_top_box, gleithretter_tp_box)
                                if s_g_iou > 0:
                                    b_a_num += 1

                    if b_a_num < 2 and r_a_num < 3:
                        # print(f'{self.flag9},  swith off 8,  b_a_num:{b_a_num}, r_a_num:{r_a_num}')
                        self.scorePoint8 = True
                        # self.assignScore(8, top_img0, top_preds)
                        conf_c = 0.1
                        self.assignScore(index=8,
                                         img=frame_top,
                                         object=objects_top,
                                         conf=conf_c,
                                         time_frame=time_top,
                                         num_frame=num_frame_top,
                                         name_save="8.jpg",
                                         preds=top_preds
                                         )

            # 9.整理桌面
            if not self.scorePoint9 and self.scorePoint1 and top_true:  # and self.scorePoint6
                in_center_box = False
                for items in [power_source_top, binding_post_red_top, binding_post_black_top, \
                              wire_connection_red_top, wire_connection_black_top, \
                              switch_off_top, switch_on_top, \
                              ammeter_top, min_top, max_top, pointer_offset_top, pointer_zero_top, \
                              slide_rheostat_top, gleithretter_top, \
                              above_top, following_top, connect_above_top, connect_following_top, \
                              wire_connection_top]:

                    for item in items:
                        item_box = item[:4]
                        if iou(item_box, self.center_box) > 100:
                            in_center_box = True
                            break
                    if in_center_box:
                        break

                if not in_center_box:  # or clean_desk_top.shape[0] != 0
                    # print(f'{self.flag9}, clean')
                    self.scorePoint9 = True
                    # self.assignScore(9, top_img0, top_preds)
                    conf_c = 0.1
                    self.assignScore(index=9,
                                     img=frame_top,
                                     object=objects_top,
                                     conf=conf_c,
                                     time_frame=time_top,
                                     num_frame=num_frame_top,
                                     name_save="9.jpg",
                                     preds=top_preds
                                     )
