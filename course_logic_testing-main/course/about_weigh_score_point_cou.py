# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 9:22
# @Author  : Qiguangnan
# @File    : about_weigh_score_point_cou.py

"""
有关称量的实验得分点
"""

try:
    from com_conf import DEBUG
except:
    DEBUG = False
from .comm import *


class AboutWeigh(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(AboutWeigh, self).__init__()
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
        self.scorePoint19 = False
        self.scorePoint20 = False

        self.faultPoint1 = False
        self.faultPoint2 = False
        self.faultPoint3 = False
        self.faultPoint4 = False
        self.faultPoint5 = False
        self.faultPoint6 = False
        self.faultPoint7 = False
        self.faultPoint8 = False

        self.initScaleOpen()  # 初始化打开电子天平
        self.initScaleZero()  # 初始化电子天平置零
        self.initWaterInCylinder()  # 初始化向量筒中加入水
        self.initDropWater2Cylinder()  # 初始化胶头滴管向量筒中滴加水
        self.initWaterVolume()  # 初始化量筒内液体体积估计
        self.initReadCylinderDiaplayData()  # 初始读取量筒示数
        self.initWater2Beaker()  # 初始化水从量筒倒入烧杯
        self.initStirDissolve()  # 初始化搅拌溶解(玻璃棒在烧杯中搅拌)
        self.initTransferLiquid()  # 初始化转移液体(将液体从烧杯倒入细口瓶)
        self.initClearnDesk()  # 初始化清理桌面

        self.initScaleBalance()  # 初始化天平平衡
        self.initSetRider()  # 初始化设置游码
        self.initPlaceWeighPaper()  # 初始化放置称量纸
        self.initUseSpoon()  # (托盘天平)使用药匙
        self.initStopperUpend()  # (托盘天平)瓶塞倒放
        self.initPatWeigh()  # 初始化轻拍
        self.initWeighBalance()  # 初始化称量天平平衡

        self.initNarrowStopperNoUpend()  # 初始化细口瓶瓶塞未倒放
        self.initWildStopperNoUpend()  # 初始化广口瓶瓶塞未倒放
        self.initLabelNoTowardPalm()  # 初始化标签未朝向手心

    def initScaleBalance(self):
        self.balance_angle_list = []
        self.scale_balance_secs = 0
        self.scale_balance_secs_pre = 0
        self.scale_balance_score_secs = 0
        self.scale_balance_score_secs_pre = 0
        self.balance_info = []

    def initSetRider(self):
        self.set_rider_secs = 0  # 称量前设置游码
        self.set_rider_secs_pre = 0  # 上一帧设置游码

    def initPlaceWeighPaper(self):
        self.place_weigh_paper_secs = 0
        self.place_weigh_paper_secs_pre = 0

    def initUseSpoon(self):  # (托盘天平)使用药匙
        self.use_spoon_thre_num = 5
        self.use_spoon_current_num = 0

    def initStopperUpend(self):  # 初始化瓶塞倒放
        self.stopper_unend_secs = 0
        self.stopper_unend_secs_pre = 0

    def initPatWeigh(self):  # 初始化轻拍
        self.pat_weigh_info = []
        self.pat_weigh_secs = 0
        self.pat_weigh_secs_pre = 0

    def initWeighBalance(self):  # 初始称量时天平平衡
        self.add_NaCl_flag = False  # 添加NaCl

    def initScaleOpen(self):
        self.scale_on_secs = 0  # 打开电子天平秒数
        self.scale_on_secs_pre = 0  # 上一帧打开电子天平秒数
        self.scale_on_info = []  # 记录天平打开信息

    def initScaleZero(self):
        self.scale_zero_secs = 0  # 电子天平置零秒数
        self.scale_zero_secs_pre = 0  # 上一帧电子天平置零秒数
        self.scale_zero_info = []  # 记录电子天平置零信息

    def initWaterInCylinder(self):
        self.water_in_cylinder = False  # 量筒中有水
        self.water_in_cylinder_secs = 0  # 量筒中有水开始秒数
        self.water_in_cylinder_secs_pre = 0  # 上一帧量筒中有水秒数
        self.water_in_cylinder_info = []  # 记录量筒中有水信息(含倒水容器)
        self.water_in_cylinder_info_ = []  # 记录量筒中有水信息

    def initDropWater2Cylinder(self):
        self.drop_water_secs = 0  # 胶头滴管向量筒滴加水开始秒数
        self.drop_water_secs_pre = 0  # 上一帧胶头滴管向量筒滴加水秒数
        self.drop_water_info = []  # 记录胶头滴管向量筒滴加水信息

    def initWaterVolume(self):
        self.cylinder_range = 100  # 100ml
        self.range_ratio = 0.76  # 量程比例系数 满量程所占高度/量筒筒体总高度
        self.liquid_v_list = []
        self.liquid_v_cache_n = 10

    def initReadCylinderDiaplayData(self):
        self.read_display_secs = 0  # 开始读示数秒数
        self.read_display_secs_pre = 0  # 上一帧读示数秒数
        self.see_display_info = []  # 记录读取液面示数信息(眼睛)
        self.see_display_head_info = []  # 记录看页面信息(只检测出头)
        self.read_display_info = []  # 记录读取液面示数信息(眼睛)
        self.read_display_head_info = []  # 记录看页面信息(只检测出头)

    def initWater2Beaker(self):
        self.water_notin_beaker_secs = 0  # 记录烧杯中没有液体的时间点  # todo 待完善证据链(时间间隔)
        self.water_to_beaker_secs = 0  # 记录量筒中添加水的时间
        self.water_in_beaker_secs = 0  # 记录烧杯中有液体的时间点
        self.water_to_beaker_info = []  # 记录量筒中水倒入烧杯
        self.water_beaker_time_interval_THRE = 5  # 烧杯中没水-加水-有水的时间间隔阈值

    def initStirDissolve(self):
        self.stir_dissolve_secs = 0  # 搅拌溶解开始秒数
        self.stir_dissolve_secs_pre = 0  # 前一帧搅拌秒数间
        self.stir_dissolve_info = []  # 记录搅拌信息

    def initTransferLiquid(self):
        self.transfer_liquid_info = []  # 烧杯向细口瓶倾倒液体

    def initClearnDesk(self):
        self.clearn_desk_secs = 0.  # 开始清理桌面秒数
        self.clearn_desk_info = []  # 记录整理桌面的信息

    def initNarrowStopperNoUpend(self):  # 初始化细口瓶瓶塞未倒放
        self.N_stopper_no_unend_secs = 0
        self.N_stopper_no_unend_secs_pre = 0

    def initWildStopperNoUpend(self):  # 初始化广口瓶瓶塞未倒放
        self.W_stopper_no_unend_secs = 0
        self.W_stopper_no_unend_secs_pre = 0

    def initLabelNoTowardPalm(self):  # 初始化标签未朝向手心
        self.label_no_tpward_palm_secs = 0
        self.label_no_tpward_palm_secs_pre = 0

    def post_assign(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def post_error(self, index, *args, **kwargs):
        exec(f'self.faultPoint{index} = True')

    def getMeasuringCylindersMouthBox(self, measuring_cylinder_front_box, measuring_cylinder_bottom_front_box):
        """
        由量筒、量筒底的检测框 返回量筒口大致位置
        :param measuring_cylinder_front_box:
        :param measuring_cylinder_bottom_front_box:
        :return:
        """
        measuring_cylinder_mouth_front_box = deepcopy(measuring_cylinder_front_box)
        w = measuring_cylinder_front_box[2] - measuring_cylinder_front_box[0]  # 量筒宽
        h = measuring_cylinder_front_box[3] - measuring_cylinder_front_box[1]  # 量筒高
        w_b = measuring_cylinder_bottom_front_box[2] - measuring_cylinder_bottom_front_box[0]  # 量筒底宽
        h_b = measuring_cylinder_bottom_front_box[3] - measuring_cylinder_bottom_front_box[1]  # 量筒底高
        d = max(w_b, h_b)
        if center_distance_v(measuring_cylinder_front_box, measuring_cylinder_bottom_front_box) >= 0:  # 量筒底在上
            if center_distance_h(measuring_cylinder_front_box, measuring_cylinder_bottom_front_box) >= 0:  # 量筒底在左上
                if w > d:
                    measuring_cylinder_mouth_front_box[0] = measuring_cylinder_mouth_front_box[2] - d
                if h > d:
                    measuring_cylinder_mouth_front_box[1] = measuring_cylinder_mouth_front_box[3] - d
                # 返回右下
            else:  # 量筒底在右上
                if h > d:
                    measuring_cylinder_mouth_front_box[1] = measuring_cylinder_mouth_front_box[3] - d
                if w > d:
                    measuring_cylinder_mouth_front_box[2] = measuring_cylinder_mouth_front_box[0] + d
                # 返回左下
        else:  # 量筒底在下
            if center_distance_h(measuring_cylinder_front_box, measuring_cylinder_bottom_front_box) >= 0:  # 量筒底在左下
                if w > d:
                    measuring_cylinder_mouth_front_box[0] = measuring_cylinder_mouth_front_box[2] - d
                if h > d:
                    measuring_cylinder_mouth_front_box[3] = measuring_cylinder_mouth_front_box[1] + d
                # 返回右上
            else:  # 量筒底在右下
                if w > d:
                    measuring_cylinder_mouth_front_box[2] = measuring_cylinder_mouth_front_box[0] + d
                if h > d:
                    measuring_cylinder_mouth_front_box[3] = measuring_cylinder_mouth_front_box[1] + d
        return measuring_cylinder_mouth_front_box  # 返回左下

    @try_decorator
    def water2beaker(self, measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                     liquids_front):
        """
        量筒水倒入烧杯中
        :param measuring_cylinders_front: 前视量筒
        :param measuring_cylinder_bottoms_front: 前视量筒底
        :param beakers_front: 前视烧杯
        :param liquids_front: 前视液体
        :return:
        """
        if (measuring_cylinders_front.shape[0] > 0
                and beakers_front.shape[0] > 0
                and measuring_cylinder_bottoms_front.shape[0] > 0
                and self.water_in_cylinder):  # 检测到量筒 量筒底 烧杯、量筒中已有水
            cylinder_front_box = measuring_cylinders_front[0][:4]  # 量筒
            cylinder_bottom_front_box = measuring_cylinder_bottoms_front[0][:4]  # 量筒底
            cylinder_mouth_front_box = self.getMeasuringCylindersMouthBox(cylinder_front_box,
                                                                          cylinder_bottom_front_box)  # 量筒口框
            cylinder_b_d = center_distance_v(cylinder_front_box, cylinder_bottom_front_box)  # 量筒底 和量筒 中心垂直距离
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                if (cylinder_b_d > 0  # 量筒底高于量筒中心
                        and min_dis_boxes(cylinder_mouth_front_box,
                                          beaker_front_box) < self.h_front * 0.028):  # # 量筒口贴近烧杯
                    if not self.water_to_beaker_info or cylinder_b_d > self.water_to_beaker_info[-2]:
                        box = combineBox(cylinder_front_box, cylinder_bottom_front_box, beaker_front_box)
                        self.water_to_beaker_info = [self.frame_front, self.time_front, self.objects_front,
                                                     self.preds_front, self.num_frame_front, box, cylinder_b_d,
                                                     self.secs]
                    else:
                        self.water_to_beaker_info[-1] = self.secs
                    return
        if self.water_to_beaker_info and self.secs - self.water_to_beaker_info[-1] > 1:
            return self.water_to_beaker_info[:5]

    def openScale(self, score_index, scales_top, scale_offs_top, scale_ons_top, scale_zeros_top, scale_not_zeros_top):
        """
        打开电子天平
        :param score_index: 得分点索引
        :param scales_top: 顶部天平
        :param scale_offs_top: 顶部 天平关
        :param scale_ons_top: 顶部 天平开
        :param scale_zeros_top: 顶部 天平0
        :param scale_not_zeros_top: 顶部天平非零
        :return:
        """
        if scales_top.shape[0] > 0:
            scale_top_box = scales_top[0][:4]
            if pt_in_polygon(center_point(scale_top_box), self.center_area_top):
                if (scale_offs_top.shape[0] == 0
                        and (scale_ons_top.shape[0] + scale_zeros_top.shape[0] + scale_not_zeros_top.shape[
                            0] != 0)):  # 天平打开
                    display_in_scale = False
                    if scale_ons_top.shape[0] > 0:
                        scale_on_box = scale_ons_top[0][:4]
                        if box1_in_box2(scale_on_box, scale_top_box):
                            display_in_scale = True
                    if not display_in_scale and scale_zeros_top.shape[0] > 0:
                        scale_zero_box = scale_zeros_top[0][:4]
                        if box1_in_box2(scale_zero_box, scale_top_box):
                            display_in_scale = True
                    if not display_in_scale and scale_not_zeros_top.shape[0] > 0:
                        scale_notzero_box = scale_not_zeros_top[0][:4]
                        if box1_in_box2(scale_notzero_box, scale_top_box):
                            display_in_scale = True
                    if display_in_scale:
                        self.scale_on_info = [score_index, self.frame_top, self.time_top, self.objects_top,
                                              self.preds_top, self.num_frame_top, scale_top_box, None, self.secs]
                        self.scale_on_secs, self.scale_on_secs_pre, flag = self.duration(self.scale_on_secs, 2,
                                                                                         self.scale_on_secs_pre, 1)
                        if flag:
                            return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                    self.num_frame_top]

    def scaleSetZero(self, score_index, hands_top, salvers_top, scales_top, hands_front, salvers_front, scales_front,
                     scale_zeros_top):
        salver_top_box = self.salverBox(salvers_top, scales_top)
        salver_front_box = self.salverBox(salvers_front, scales_front, 'front')
        if self.handNotOnScale(hands_top, salver_top_box, hands_front, salver_front_box):
            if scale_zeros_top.shape[0] > 0:
                self.scale_zero_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                        self.num_frame_top]
                self.scale_zero_secs, self.scale_zero_secs_pre, flag = self.duration(self.scale_zero_secs,
                                                                                     1.5,
                                                                                     self.scale_zero_secs_pre,
                                                                                     0.6)
                if flag:
                    return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                            self.num_frame_top]

    @try_decorator
    def stopperUpend(self, wild_stopper_upends_front, wild_stopper_no_upends_front,
                     wild_stopper_upends_top, wild_stopper_no_upends_top):
        """
        广口瓶瓶塞倒放
        Args:
            wild_stopper_upends_front:
            wild_stopper_no_upends_front:
            wild_stopper_upends_top:
            wild_stopper_no_upends_top:
        Returns:
        """
        record = ''
        if wild_stopper_upends_front.shape[0] > 0:  # 前视瓶塞倒放
            record = "front"
        elif wild_stopper_no_upends_front.shape[0] == 0 and wild_stopper_upends_top.shape[0] > 0:  # 顶视瓶塞倒放 前视没有瓶塞未倒放
            record = "top"
        if record:
            self.stopper_unend_secs, self.stopper_unend_secs_pre, flag = self.duration(
                self.stopper_unend_secs,
                2,
                self.stopper_unend_secs_pre,
                1
            )
            if flag:
                if record == "front":
                    return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                            self.num_frame_front]
                else:
                    return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    @try_decorator
    def stopperNoUpend(self, stopper_upends_front, stopper_no_upends_front,
                       stopper_upends_top, stopper_no_upends_top, type='narrow'):
        record = ''
        if stopper_no_upends_front.shape[0] > 0:  # 前视瓶塞未倒放
            record = "front"
        elif stopper_upends_front.shape[0] == 0 and stopper_no_upends_top.shape[0] > 0:  # 顶视瓶塞未倒放 前视没有瓶塞倒放
            record = "top"
        if record:
            if type == 'narrow':
                self.N_stopper_no_unend_secs, self.N_stopper_no_unend_secs_pre, flag = self.duration(
                    self.N_stopper_no_unend_secs,
                    2,
                    self.N_stopper_no_unend_secs_pre,
                    1
                )
            else:
                self.W_stopper_no_unend_secs, self.W_stopper_no_unend_secs_pre, flag = self.duration(
                    self.W_stopper_no_unend_secs,
                    2,
                    self.W_stopper_no_unend_secs_pre,
                    1
                )
            if flag:
                if record == "front":
                    return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                            self.num_frame_front]
                else:
                    return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    def get_angle(self, left_bar_box, right_bar_box):
        """
        托盘天平由两个托盘杆得出平衡时的角度和当前角度
        :param left_bar_box:
        :param right_bar_box:
        :return:
        """
        center_d = (center_point(left_bar_box)[0] + center_point(right_bar_box)[
            0]) / 2 - self.w_front / 2  # 天平中心距图片中心距离
        h = high(left_bar_box) - high(right_bar_box)
        w = center_point(right_bar_box)[0] - center_point(left_bar_box)[0]
        angle = (math.atan(h / w) / math.pi) * 180  # 计算当前角度
        angle_balance = (center_d / (self.h_front / 2)) * 6  # 计算平衡角度
        if DEBUG:  # 可视化
            u_l_point = (int(center_point(left_bar_box)[0]), int(left_bar_box[1]))
            u_r_point = (int(center_point(right_bar_box)[0]), int(right_bar_box[1]))
            d_l_point = (int(center_point(left_bar_box)[0]), int(left_bar_box[3]))
            d_r_point = (int(center_point(right_bar_box)[0]), int(right_bar_box[3]))

            cv2.line(self.frame_front, u_l_point, u_r_point, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.line(self.frame_front, d_l_point, d_r_point, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(self.frame_front, f"current_angle: {angle:.2f}",
                        (u_r_point[0] + 20, u_r_point[1]), 0, 0.6, (0, 0, 255), 1,
                        lineType=cv2.LINE_AA)
            cv2.putText(self.frame_front, f"balance_angle: {angle_balance:.2f}",
                        (d_r_point[0] + 20, d_r_point[1]), 0, 0.6, (0, 0, 255), 1,
                        lineType=cv2.LINE_AA)

        return angle, angle_balance

    @try_decorator
    def scaleBalance(self, hands_front, salver_bars_front, salvers_top, weigh_papers_top):
        """
        托盘天平平衡
        :param hands_front: 前视手
        :param salver_bars_front: 托盘杆
        :param salvers_top: 顶视托盘
        :param weigh_papers_top: 顶视称量纸
        :return:
        """
        if salver_bars_front.shape[0] == 2:
            left_bar_box, right_bar_box = separate_left_right(salver_bars_front[0][:4],
                                                              salver_bars_front[1][:4])  # 区分左右
            angle, angle_balance = self.get_angle(left_bar_box, right_bar_box)  # 当前角度 平衡角度
            if len(self.balance_angle_list) == 20:
                self.balance_angle_list.pop(0)
            self.balance_angle_list.append(angle)
            if (len(self.balance_angle_list) == 20
                    and (abs(sum(self.balance_angle_list[-10:]) / 10 - angle_balance) < 2)):  # 误差 2°以内
                self.scale_balance_secs, self.scale_balance_secs_pre, flag = self.duration(self.scale_balance_secs,
                                                                                           2,
                                                                                           self.scale_balance_secs_pre,
                                                                                           1)
                if flag:
                    angle_abs = abs(self.balance_angle_list[-1] - angle_balance)
                    if not self.balance_info or angle_abs < self.balance_info[-1]:
                        self.balance_info = [self.frame_front, self.time_front, self.objects_front,
                                             self.preds_front, self.num_frame_front, angle_abs]
            if self.balance_info and hands_front.shape[0] > 0:
                left_nut_area = self.get_nut_area_front_bar(left_bar_box)
                right_nut_area = self.get_nut_area_front_bar(right_bar_box, 'right')
                for nut_area in left_nut_area, right_nut_area:
                    hand_nut_iou = 0
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        hand_nut_iou += iou(hand_front_box, nut_area)
                    if hand_nut_iou == 0:
                        self.scale_balance_score_secs, self.scale_balance_score_secs_pre, flag = self.duration(
                            self.scale_balance_score_secs,
                            2,
                            self.scale_balance_score_secs_pre,
                            1)
                        if flag:
                            return self.balance_info[:6]
                        break

    def get_nut_area_front_bar(self, bar_box, orientation='left'):
        """
        由托盘杆的位置推出大致调节螺母的位置
        :param bar_box: 托盘杆的位置
        :param orientation: 方位
        :return:
        """
        w = width(bar_box)
        h = high(bar_box)
        nut_area = deepcopy(bar_box)
        nut_area[3] = bar_box[1] + h / 2  # 下边界 1/2 处
        nut_area[1] = bar_box[1] + h / 4  # 上边界 上1/4 处
        if orientation == 'left':
            nut_area[0] = bar_box[0] - w * 1.5
            nut_area[2] = bar_box[0]
        else:
            nut_area[0] = bar_box[2]
            nut_area[2] = bar_box[2] + w * 1.5
        # 画框
        # cv2.rectangle(self.frame_front, (int(nut_area[0]), int(nut_area[1])), (int(nut_area[2]), int(nut_area[3])), [0, 0, 255], 2, cv2.LINE_AA)
        return nut_area

    @try_decorator
    def setRider(self, salver_bars_front, tweezers_front, riders_front, tweezers_top, riders_top):
        """
        游码调节到称量位置
        :param salver_bars_front: 托盘杆
        :return:
        """
        if salver_bars_front.shape[0] == 2:
            left_bar_box, right_bar_box = separate_left_right(salver_bars_front[0][:4], salver_bars_front[1][:4])
            l_h, r_h = high(left_bar_box), high(right_bar_box)
            if r_h > l_h * 1.1:
                self.set_rider_secs, self.set_rider_secs_pre, flag = self.duration(self.set_rider_secs, 2,
                                                                                   self.set_rider_secs_pre, 1)
                if flag:
                    return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                            self.num_frame_front]
            else:
                self.initSetRider()

    @try_decorator
    def weighPaperOnScale(self, scales_top, weigh_papers_top):
        """
        判断托盘天平两边托盘上有称量纸
        :param scales_top: 顶视托盘天平
        :param weigh_papers_top: 顶视称量纸
        :return:
        """
        if scales_top.shape[0] == 1 and weigh_papers_top.shape[0] >= 2:
            scale_top_box = scales_top[0][:4]
            w = width(scale_top_box)
            if pt_in_polygon(center_point(scale_top_box), self.center_area_top):
                left, right = False, False
                for weigh_paper_top in weigh_papers_top:
                    weigh_paper_top_box = weigh_paper_top[:4]
                    if pt_in_box(center_point(weigh_paper_top_box), scale_top_box):
                        d = center_distance_h(scale_top_box, weigh_paper_top_box)
                        if d > 0 and abs(d) > w / 4:  # 称量纸在左
                            if left is True:
                                continue
                            else:
                                left = True
                        elif d < 0 and abs(d) > w / 4:
                            if right is True:
                                continue
                            else:
                                right = True
                if left and right:
                    self.place_weigh_paper_secs, self.place_weigh_paper_secs_pre, flag = self.duration(
                        self.place_weigh_paper_secs,
                        2,
                        self.place_weigh_paper_secs_pre,
                        1)
                    if flag:
                        return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    @try_decorator
    def useSpoon(self, salt_granules_front, wild_mouth_bottles_front, spoons_front, scales_front,
                 hands_front, salt_granules_top, wild_mouth_bottles_top, spoons_top, hands_top,
                 scales_top):
        """
        判断使用药匙
        :param salt_granules_front: 前视食盐颗粒
        :param wild_mouth_bottles_front: 前视广口瓶
        :param spoons_front: 前视药匙
        :param scales_front: 前视托盘天平
        :param hands_front: 前视手
        :param salt_granules_top: 顶视食盐颗粒
        :param wild_mouth_bottles_top: 顶视广口瓶
        :param spoons_top: 顶视药匙
        :param hands_top: 顶视手
        :param scales_top: 顶视天平
        :return:
        """
        record = ''
        if spoons_front.shape[0] == 1 and hands_front.shape[0] > 0:  # 前视角
            spoon_front_box = spoons_front[0][:4]
            hand_spoon_front = False  # 手拿药匙
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if iou(spoon_front_box, hand_front_box) > 0:
                    hand_spoon_front = True
                    break
            if hand_spoon_front and salt_granules_front.shape[0] > 0:  # 前视药匙和食盐颗粒
                for salt_granule_front in salt_granules_front:
                    salt_granule_front_box = salt_granule_front[:4]
                    if iou(salt_granule_front_box, spoon_front_box) > 0:
                        record = "front"
                        break
            if not record and hand_spoon_front and wild_mouth_bottles_front.shape[0] == 1:  # 前视药匙和广口瓶
                wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
                if (iou(wild_mouth_bottle_front_box, spoon_front_box) > box_area(spoon_front_box) * 0.2
                        and center_distance_v(wild_mouth_bottle_front_box, spoon_front_box)):
                    record = "front"
            if not record and hand_spoon_front and scales_front.shape[0] == 1:
                scale_front_box = scales_front[0][:4]
                if (center_distance_v(scale_front_box, spoon_front_box) > 0  # # 药匙在天平上方
                        and (iou(scale_front_box, spoon_front_box) > 0
                             or (scale_front_box[0] < spoon_front_box[2]
                                 and scale_front_box[2] > spoon_front_box[0]))):  # 药匙天平相交
                    record = "front"
        if not record and spoons_top.shape[0] == 1 and hands_top.shape[0] > 0:  # 顶视角
            spoon_top_box = spoons_top[0][:4]
            hand_spoon_top = False  # 手拿药匙
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(spoon_top_box, hand_top_box) > 0:
                    hand_spoon_top = True
                    break
            if hand_spoon_top and salt_granules_top.shape[0] > 0:  # 顶视药匙和食盐颗粒
                for salt_granule_top in salt_granules_top:
                    salt_granule_top_box = salt_granule_top[:4]
                    if iou(salt_granule_top_box, spoon_top_box) > 0:
                        record = "top"
                        break
            if not record and hand_spoon_top and wild_mouth_bottles_top.shape[0] == 1:  # 顶视药匙和广口瓶
                wild_mouth_bottle_top_box = wild_mouth_bottles_top[0][:4]
                if iou(wild_mouth_bottle_top_box, spoon_top_box) > box_area(spoon_top_box) * 0.2:
                    record = "top"
            if not record and hand_spoon_top and scales_top.shape[0] == 1:  # 药匙 托盘天平
                scale_top_left_box = deepcopy(scales_top[0][:4])
                scale_top_left_box[2] = (scale_top_left_box[0] + scale_top_left_box[2]) / 2
                if iou(scale_top_left_box, spoon_top_box) > 0:
                    record = "top"
        if record == 'front':
            if self.use_spoon_current_num > self.use_spoon_thre_num:
                return [self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front]
            else:
                self.use_spoon_current_num += 1
        if record == "top":
            if self.use_spoon_current_num > self.use_spoon_thre_num:
                return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]
            else:
                self.use_spoon_current_num += 1

    def weighPatNutScale(self, score_index, hands_top, spoons_top, spoon_us_top, spoons_front, spoon_us_front,
                         salver_bars_front, weigh_papers_top, scales_top):  # todo 平衡
        """
        轻拍手腕（或药匙柄）添加氯化钠
        :param score_index: 得分点索引
        :param hands_top: 顶视手
        :param spoons_top: 顶视药匙
        :param spoon_us_top: 顶视药匙勺
        :param spoons_front: 前视药匙
        :param spoon_us_front: 前视药匙勺
        :param salver_bars_front: 前视托盘杆
        :param weigh_papers_top: 顶视称量纸
        :param scales_top: 顶视天平
        :return:
        """
        if (spoons_top.shape[0] == 1
                and salver_bars_front.shape[0] == 2
                and scales_top.shape[0] == 1
                and weigh_papers_top.shape[0] >= 2
                and hands_top.shape[0] >= 2):
            spoon_top_box = spoons_top[0][:4]
            scale_top_box = scales_top[0][:4]
            w = width(scale_top_box)
            for weigh_paper_top in weigh_papers_top:
                weigh_paper_top_box = weigh_paper_top[:4]
                if pt_in_box(center_point(weigh_paper_top_box), scale_top_box):
                    d = center_distance_h(weigh_paper_top_box, scale_top_box)
                    if d > w / 5 and iou(weigh_paper_top_box, spoon_top_box) > 0:  # 称量纸在左
                        if self.patWeigh(hands_top, spoon_top_box, spoon_us_top, spoons_front, spoon_us_front,
                                         weigh_paper_top_box):
                            left_bar_box, right_bar_box = separate_left_right(salver_bars_front[0][:4],
                                                                              salver_bars_front[1][:4])

                            angle, angle_balance = self.get_angle(left_bar_box, right_bar_box)
                            if abs(angle - angle_balance) < 2:
                                return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                        self.num_frame_top]

    @try_decorator
    def weighBalance(self, hands_front, spoons_front, spoon_us_front, salver_bars_front, salvers_front,
                     salt_granules_front, hands_top, spoons_top, spoon_us_top, salvers_top,
                     weigh_papers_top, scales_top, salt_granules_top):
        """
        准确称量NaCL至所需量，天平平衡
        :param hands_front:
        :param spoons_front:
        :param spoon_us_front:
        :param salver_bars_front:
        :param hands_top:
        :param spoons_top:
        :param spoon_us_top:
        :param salvers_top:
        :param weigh_papers_top:
        :param scales_top:
        :return:
        """
        if self.add_NaCl_flag:
            info = self.scaleBalance(hands_front, salver_bars_front, salvers_top, weigh_papers_top)
            if info:
                return info
        elif scales_top.shape[0] == 1:  # 顶视托盘上有食盐颗粒
            scale_top_box = scales_top[0][:4]
            if salt_granules_top.shape[0] > 0:
                for salt_granule_top in salt_granules_top:
                    salt_granule_top_box = salt_granule_top[:4]
                    if iou(salt_granule_top_box, scale_top_box) > box_area(salt_granule_top_box) * 0.8:
                        self.add_NaCl_flag = True
                        return
            if spoon_us_top.shape[0] == 1:  # 药匙勺在托盘上
                spoon_u_top_box = spoon_us_top[0][:4]
                if iou(spoon_u_top_box, scale_top_box) > box_area(spoon_u_top_box) * 0.8:
                    self.add_NaCl_flag = True
                    return
            elif spoons_top.shape[0] == 1:  # 药匙在托盘上
                spoon_top_box = spoons_top[0][:4]
                if iou(spoon_top_box, scale_top_box) > box_area(spoon_top_box) * 0.8:
                    self.add_NaCl_flag = True

    @try_decorator
    def patWeigh(self, hands_top, spoons_top, spoon_us_top, scales_top, wild_mouth_bottles_top,
                 spoons_front, spoon_us_front, scales_front, salvers_front):
        """
        轻拍手腕或者药匙
        :param hands_top: 顶视手
        :param spoons_top: 顶视药匙
        :param spoon_us_top: 顶视药匙勺
        :param scales_top: 顶视天平
        :param wild_mouth_bottles_top: 顶视广口瓶
        :param spoons_front: 前视药匙
        :param spoon_us_front: 前视药匙勺
        :param scales_front: 前视天平
        :param salvers_front: 前视托盘
        :return:
        """
        iou_v = 0
        if self.spoonOnSalver(spoons_front, spoon_us_front, scales_front, salvers_front, spoons_top, spoon_us_top,
                              scales_top):  # 药匙在托盘上方
            if spoons_top.shape[0] == 1:
                spoon_top_box = spoons_top[0][:4]
                if wild_mouth_bottles_top.shape[0] > 0:
                    wild_mouth_bottle_top_box = wild_mouth_bottles_top[0][:4]
                    if iou(wild_mouth_bottle_top_box, spoon_top_box) > 0:  # 广口瓶与药匙相交
                        return
                orientation = 'right'  # 用哪边手拿药匙
                if spoon_us_top.shape[0] > 0:
                    spoon_u_top_box = spoon_us_top[0][:4]  # 药匙勺
                    if center_distance_h(spoon_u_top_box, spoon_top_box) > 0:  # 药匙勺在药匙右边
                        orientation = 'left'
                elif spoon_us_front.shape[0] > 0 and spoons_front.shape[0] > 0:  # 前视药匙和药匙勺
                    spoon_u_front_box = spoon_us_front[0][:4]
                    spoon_front_box = spoons_front[0][:4]
                    if center_distance_h(spoon_front_box, spoon_u_front_box) > 0:  # 前视药匙勺在左， 顶视左手拿
                        orientation = 'left'
                # else:
                #     return
                hand_spoon_num = 0
                spoon_hand_box = None  # 拿药匙的手
                hand_box_list = []  # 未拿药匙得手
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    iou_h_s = iou(spoon_top_box, hand_top_box)
                    if iou_h_s > 0:
                        if orientation == 'right' and spoon_hand_box is None and center_distance_h(hand_top_box,
                                                                                                   spoon_top_box) > 0:  # 右手
                            hand_spoon_num += 1
                        elif orientation == 'left' and spoon_hand_box is None and center_distance_h(spoon_top_box,
                                                                                                    hand_top_box) > 0:  # 左手
                            hand_spoon_num += 1
                        else:
                            iou_v = iou_h_s
                            hand_spoon_num += 1
                        spoon_hand_box = deepcopy(hand_top_box)
                    else:
                        hand_box_list.append(hand_top_box)
                if hand_spoon_num == 2:  # 两只手与药匙相交
                    if iou_v > box_area(spoon_top_box) * 0.:
                        pass
                    else:
                        return
                elif hand_spoon_num == 1 and len(hand_box_list) > 0:  # 一只手与药匙相交
                    iou_v = 0
                    w = spoon_hand_box[2] - spoon_hand_box[0]  # 宽
                    h = spoon_hand_box[3] - spoon_hand_box[1]  # 高
                    spoon_hand_box_ = deepcopy(spoon_hand_box)  # 手腕区域
                    # orientation = 'right'  # 用哪边手拿药匙
                    # if spoon_us_top.shape[0] > 0:
                    #     spoon_u_top_box = spoon_us_top[0][:4]  # 药匙勺
                    #     if (center_distance_h(spoon_u_top_box, spoon_top_box) > 0  # 药匙勺在药匙右边
                    #             and center_distance_h(spoon_u_top_box, spoon_hand_box) > 0):  # 药匙勺在手右边
                    #         orientation = 'left'
                    # elif spoon_us_front.shape[0] > 0 and spoons_front.shape[0] > 0:  # 前视药匙和药匙勺
                    #     spoon_u_front_box = spoon_us_front[0][:4]
                    #     spoon_front_box = spoons_front[0][:4]
                    #     if center_distance_h(spoon_front_box, spoon_u_front_box) > 0:  # 前视药匙勺在左， 顶视左手拿
                    #         orientation = 'left'
                    # elif center_distance_h(spoon_hand_box, spoon_top_box) > 0:  # 顶视手在药匙左
                    #     orientation = 'left'
                    if orientation == 'right':  # 右
                        spoon_hand_box_[0] = spoon_hand_box[2]
                        spoon_hand_box_[2] = spoon_hand_box[2] + w * 1.5

                    else:  # 左
                        spoon_hand_box_[0] = spoon_hand_box[1]
                        spoon_hand_box_[2] = spoon_hand_box[1] - w * 1.5
                    spoon_hand_box_[1] = spoon_hand_box[1] + h * 0.5
                    spoon_hand_box_[3] = spoon_hand_box[3] + h
                    spoon_hand_box[1] += h
                    spoon_hand_box[3] += h  # 扩大拿药匙的手的区域(向下移动一个位置)
                    for hand_top_box in hand_box_list:
                        for area_box in spoon_hand_box, spoon_hand_box_:
                            if DEBUG:
                                cv2.rectangle(self.frame_top, (int(area_box[0]), int(area_box[1])),
                                              (int(area_box[2]), int(area_box[3])), [0, 0, 255], 1, cv2.LINE_AA)
                            iou_v += iou(area_box, hand_top_box)
        if iou_v > 0:
            if not self.pat_weigh_info or iou_v > self.pat_weigh_info[-2]:
                self.pat_weigh_info = [self.frame_top, self.time_top, self.objects_top,
                                       self.preds_top, self.num_frame_top, iou_v, self.secs]
            else:
                self.pat_weigh_info[-1] = self.secs
            self.pat_weigh_secs, self.pat_weigh_secs_pre, flag = self.duration(
                self.pat_weigh_secs,
                2,
                self.pat_weigh_secs_pre,
                1
            )
            if flag:
                return self.pat_weigh_info[:5]

    def spoonOnSalver(self, spoons_front, spoon_us_front, scales_front, salvers_front, spoons_top, spoon_us_top,
                      scales_top, front=True, top=True):
        """
        判断药匙是否在托盘上方，
        :param spoons_front: 前视药匙
        :param spoon_us_front: 前视药匙勺
        :param scales_front: 前视天平
        :param salvers_front: 前视托盘
        :param spoons_top: 顶视药匙
        :param spoon_us_top: 顶视药匙勺
        :param scales_top: 顶视天平
        :return:
        """
        if front and scales_front.shape[0] == 1:  # 前视
            scale_front_up_area = deepcopy(scales_front[0][:4])  # 托盘上方区域
            scale_front_up_area[1] = scale_front_up_area[1] - self.h_front * 0.185
            if salvers_front.shape[0] == 1:
                scale_front_up_area[3] = center_point(salvers_front[0][:4])[1]
            elif salvers_front.shape[0] == 2:
                scale_front_up_area[3] = (center_point(salvers_front[0][:4])[1] + center_point(salvers_front[1][:4])[
                    1]) / 2
            else:
                scale_front_up_area[3] = scale_front_up_area[1] + (
                        scale_front_up_area[3] - scale_front_up_area[1]) * 0.3
            if spoon_us_front.shape[0] == 1:
                spoon_u_front_box = spoon_us_front[0][:4]  # 药匙勺
                if box1_in_box2(spoon_u_front_box, scale_front_up_area):
                    return True
            elif spoons_front.shape[0] == 1:
                spoon_front_box = spoons_front[0][:4]
                if iou(scale_front_up_area, spoon_front_box) > box_area(spoon_front_box) * 0.4:
                    return True
        if top and scales_top.shape[0] == 1:  # 顶视
            scale_top_box = scales_top[0][:4]
            if spoon_us_top.shape[0] == 1:  # 药匙勺
                spoon_u_top_box = spoon_us_top[0][:4]
                if box1_in_box2(spoon_u_top_box, scale_top_box):
                    return True
            elif spoons_top.shape[0] == 1:
                spoon_top_box = spoons_top[0][:4]
                if iou(scale_top_box, spoon_top_box) > box_area(spoon_top_box) * 0.4:
                    return True

    @try_decorator
    def dropWaterIncylinder(self, droppers_front, measuring_cylinders_front, water_columns_front):
        """
        胶头滴管向量筒中滴加液体
        :param droppers_front: 前视胶头滴管
        :param measuring_cylinders_front: 前视量筒
        :param water_columns_front: 前视水柱
        :return:
        """
        if (droppers_front.shape[0] > 0
                and measuring_cylinders_front.shape[0] > 0
                and water_columns_front.shape[0] > 0):
            dropper_front_box = droppers_front[0][:4]
            cylinder_front_box = measuring_cylinders_front[0][:4]
            water_column_front_box = water_columns_front[0][:4]
            dropper_cylinder_d_h = abs(center_distance_h(dropper_front_box, water_column_front_box))  # 滴管 水柱中心水平距离
            dropper_cylinder_d_h_thre = self.h_front * 0.05  # 1080 * 0.05 54 pixel 滴管 量筒 水平方向阈值
            dropper_cylinder_d_v_thre = -self.h_front * 0.05  # 1080 * 0.045 54 pixel 滴管 量筒 垂直方向阈值
            if (dropper_cylinder_d_h < dropper_cylinder_d_h_thre
                    and cylinder_front_box[1] - dropper_front_box[3] > dropper_cylinder_d_v_thre):
                box = combineBox(dropper_front_box, cylinder_front_box)
                self.drop_water_info = [self.frame_front, self.time_front, self.objects_front,
                                        self.preds_front, self.num_frame_front, box, None, self.secs]
                self.drop_water_secs, self.drop_water_secs_pre, flag = self.duration(self.drop_water_secs,
                                                                                     0.8,
                                                                                     self.drop_water_secs_pre,
                                                                                     0.4)
                if flag:
                    return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    @try_decorator
    def water_volume(self, hands_front, measuring_cylinders_front, measuring_cylinder_mouths_front,
                     measuring_cylinder_bottoms_front, water_columns_front, liquid_levels_front):
        """
        估算量筒中水的体积
        Args:
            hands_front:
            measuring_cylinders_front:
            measuring_cylinder_mouths_front:
            measuring_cylinder_bottoms_front:
            water_columns_front:

        Returns:

        """
        if (measuring_cylinders_front.shape[0] > 0
                and measuring_cylinder_mouths_front.shape[0] > 0
                and measuring_cylinder_bottoms_front.shape[0] > 0
                and water_columns_front.shape[0] == 1
                and liquid_levels_front.shape[0] == 1):
            water_column_front_box = water_columns_front[0][:4]
            liquid_level_front_box = liquid_levels_front[0][:4]
            w = width(liquid_level_front_box)
            level_rx = int(liquid_level_front_box[2])
            level_y = int(center_point(liquid_level_front_box)[1])
            if (center_distance_h(water_column_front_box, liquid_level_front_box, True) > w
                    or abs(level_y - water_column_front_box[1]) > w / 4):
                return 0.
            cylinder_front_box = None
            for measuring_cylinder_front in measuring_cylinders_front:
                measuring_cylinder_front_box = measuring_cylinder_front[:4]
                if iou(measuring_cylinder_front_box, water_column_front_box) > box_area(water_column_front_box) * 0.9:
                    cylinder_front_box = measuring_cylinder_front_box
                    break
            if cylinder_front_box is None:
                return 0.
            bottom_front_box = None
            for measuring_cylinder_bottom_front in measuring_cylinder_bottoms_front:
                measuring_cylinder_bottom_front_box = measuring_cylinder_bottom_front[:4]
                if iou(cylinder_front_box, measuring_cylinder_bottom_front_box) > box_area(
                        measuring_cylinder_bottom_front_box) * 0.5:
                    bottom_front_box = measuring_cylinder_bottom_front_box
                    break
            if bottom_front_box is None:
                return 0.
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if iou(hand_front_box, bottom_front_box) > box_area(bottom_front_box) * 0.4:
                    return 0.0
            mouth_front_box = None
            for measuring_cylinder_mouth_front in measuring_cylinder_mouths_front:
                measuring_cylinder_mouth_front_box = measuring_cylinder_mouth_front[:4]
                if (iou(measuring_cylinder_mouth_front_box, cylinder_front_box) > 0
                        and center_distance_h(measuring_cylinder_mouth_front_box, liquid_level_front_box, True) < w / 2
                        and measuring_cylinder_mouth_front_box[3] < level_y):
                    mouth_front_box = measuring_cylinder_mouth_front_box
                    break
            if mouth_front_box is None:
                return 0.
            c_y1 = int(mouth_front_box[1])
            c_y3 = int(water_column_front_box[3])
            v = round(100 * ((c_y3 - level_y) / ((c_y3 - c_y1) * 0.76)), 1)
            if len(self.liquid_v_list) > self.liquid_v_cache_n:
                self.liquid_v_list.pop(0)
            self.liquid_v_list.append(v)
            avg_v = sum(self.liquid_v_list) / len(self.liquid_v_list)
            if abs(avg_v - v) < 2:
                v = avg_v
            if DEBUG:
                cv2.putText(self.frame_front, f"{v:.1f}ml", (level_rx + 20, level_y - 5), 0, 1, (0, 0, 255),
                            thickness=1, lineType=cv2.LINE_AA)
                cv2.arrowedLine(self.frame_front, (level_rx + 140, level_y), (level_rx, level_y), (0, 0, 255),
                                thickness=1, line_type=cv2.LINE_AA, shift=0, tipLength=0.1)
            return v

    @try_decorator
    def stirDissolve(self, glass_rods_front, beakers_front, hands_front, duration_secs=40, reclock_secs=5):
        """
        烧杯中用玻璃棒搅拌
        :param glass_rods_front: 前视玻璃棒
        :param beakers_front: 前视烧杯
        :param hands_front: 前视手
        :param duration_secs: 持续时间
        :param reclock_secs: 重新计时时间
        :return:
        """
        if glass_rods_front.shape[0] > 0 and beakers_front.shape[0] > 0 and hands_front.shape[0] > 0:
            glass_rod_front_box = glass_rods_front[0][:4]
            hand_glass_rod = False
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if iou(hand_front_box, glass_rod_front_box) > 0:
                    hand_glass_rod = True
                    break
            if hand_glass_rod:
                for beaker_front in beakers_front:
                    beaker_front_box = beaker_front[:4]
                    if (iou(glass_rod_front_box, beaker_front_box) > 0
                            and center_distance_v(beaker_front_box, glass_rod_front_box) > 0):
                        self.stir_dissolve_secs, self.stir_dissolve_secs_pre, flag = self.duration(
                            self.stir_dissolve_secs,
                            duration_secs,
                            self.stir_dissolve_secs_pre,
                            reclock_secs)
                        box = combineBox(glass_rod_front_box, beaker_front)
                        self.stir_dissolve_info = [self.frame_front, self.time_front, self.objects_front,
                                                   self.preds_front, self.num_frame_front, box, None, self.secs]
                        if flag:
                            return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    @try_decorator
    def transferLiquid(self, beakers_front, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, hands_front):
        """
        烧杯向细口瓶中转移液体
        :param beakers_front: 前视烧杯
        :param narrow_mouth_bottles_front: 前视细口瓶
        :param narrow_mouth_bottlenecks_front: 前视细口瓶口
        :param hands_front: 前视手
        :return:
        """
        if beakers_front.shape[0] > 0 and hands_front.shape[0] > 0:  # 手 烧杯
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                for bottles_front in [narrow_mouth_bottlenecks_front, narrow_mouth_bottles_front]:
                    for mouth_bottle_front in bottles_front:
                        mouth_bottle_front_box = mouth_bottle_front[:4]
                        d_v = mouth_bottle_front_box[1] - center_point(beaker_front_box)[1]  # 细口瓶上边距烧杯中心距离
                        if (iou(mouth_bottle_front_box, beaker_front_box) > 0  # 烧杯细口瓶相交
                                and d_v > 0  # 烧杯高于细口瓶
                                and w_h_ratio(beaker_front_box) > 1.1):  # 烧杯宽高比 > 1.1
                            box = combineBox(beaker_front_box, mouth_bottle_front_box)
                            if not self.transfer_liquid_info or d_v > self.transfer_liquid_info[-2]:
                                self.transfer_liquid_info = [self.frame_front, self.time_front, self.objects_front,
                                                             self.preds_front, self.num_frame_front, box, d_v,
                                                             self.secs]
                            else:
                                self.transfer_liquid_info[-1] = self.secs
                            return
        if self.transfer_liquid_info and self.secs - self.transfer_liquid_info[-1] > 0.5:
            return self.transfer_liquid_info[:5]

    @try_decorator
    def waterInCylinder(self, water_columns_front, measuring_cylinders_front, containers_front=None,
                        duration_secs=2, reclock_secs=1):
        """
        量筒中有水
        :param water_columns_front: 前视水柱
        :param measuring_cylinders_front: 前视量筒
        :param containers_front: 前视倒水容器
        :param duration_secs: 持续时间
        :param reclock_secs: 重新计时间隔
        :return:
        """
        if water_columns_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0:
            water_column_front_box = water_columns_front[0][:4]
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            h_water = high(water_column_front_box)
            h_cylinder = high(measuring_cylinder_front_box)
            w_cylinder = width(measuring_cylinder_front_box)
            if (pt_in_polygon(center_point(measuring_cylinder_front_box), self.center_area_front)
                    and iou(measuring_cylinder_front_box, water_column_front_box) >
                    box_area(water_column_front_box) * 0.8
                    and h_water > h_cylinder * 0.1 and h_cylinder > w_cylinder):
                if containers_front is not None and containers_front.shape[0] > 0:
                    for container_front in containers_front:
                        container_front_box = container_front[:4]
                        measuring_cylinder_mouth_front_box = deepcopy(water_column_front_box)
                        measuring_cylinder_mouth_front_box[3] -= w_cylinder
                        if (container_front_box[1] > measuring_cylinder_front_box[1] > container_front_box[3]  # 容器在量筒上方
                                and iou(container_front_box, measuring_cylinder_mouth_front_box) > 0):  # 容器与量筒口有交集
                            self.water_in_cylinder_info = [self.frame_front, self.time_front, self.objects_front,
                                                           self.preds_front, self.num_frame_front, h_water, self.secs]
                self.water_in_cylinder_secs, self.water_in_cylinder_secs_pre, flag = self.duration(
                    self.water_in_cylinder_secs,
                    duration_secs,
                    self.water_in_cylinder_secs_pre,
                    reclock_secs)
                if flag:
                    self.water_in_cylinder = True
                    if not self.water_in_cylinder_info_ or self.water_in_cylinder_info_[-2] < h_water:
                        self.water_in_cylinder_info_ = [self.frame_front, self.time_front, self.objects_front,
                                                        self.preds_front, self.num_frame_front, h_water, self.secs]
                if self.water_in_cylinder_info and self.secs - self.water_in_cylinder_info[-1] > 1.5:
                    return self.water_in_cylinder_info
                elif self.water_in_cylinder_info_ and self.secs - self.water_in_cylinder_info_[-1] > 1.5:
                    return self.water_in_cylinder_info_

    def salverBox(self, salvers, scales, view='top'):
        """
        由电子天平、电子天平托盘 得出 电子天平托盘 box 防止只检测出电子天平的情况
        :param salvers: 电子天平托盘
        :param scales: 电子天平
        :param view:
        :return:
        """
        ratio = (0.08, 0.3) if view == 'top' else (0.09, 0.5)
        w = self.w_top if view == 'top' else self.w_front
        if salvers.shape[0] > 0:  # 称量盘
            return salvers[0][:4]
        elif scales.shape[0] > 0:  # 整个天平
            salver_box = deepcopy(scales[0][:4])
            x = (salver_box[2] - salver_box[0]) * ratio[0]
            y = (salver_box[3] - salver_box[1]) * ratio[1]
            dis_h_r = (center_point(salver_box)[0] / w - 0.5) / 0.5
            salver_box[0] += x * (1 + dis_h_r)
            if view == 'top':
                salver_box[1] += x * 0.5
            salver_box[2] -= x * (1 - dis_h_r)
            salver_box[3] -= y
            # if view=='top': # 绘图
            #     cv2.rectangle(self.top_img0, (int(salver_box[0]), int(salver_box[1])), (int(salver_box[2]), int(salver_box[3])), (255, 0, 0), -1, cv2.LINE_AA)
            # else: # 绘图
            #     cv2.rectangle(self.front_img0, (int(salver_box[0]), int(salver_box[1])), (int(salver_box[2]), int(salver_box[3])), (255, 0, 0), -1, cv2.LINE_AA)
            return salver_box

    @try_decorator
    def readDisplayData(self, water_columns_front, heads_front, eyes_front):
        """
        读量筒液面示数
        :param water_columns_front: 前视水柱
        :param heads_front: 前视头
        :param eyes_front: 前视眼睛
        :return:
        """
        # if self.is_teach and self.water_to_beaker_flag:
        #     if self.see_display_info:
        #         self.faultyOperation(2, '读取示数时眼睛要平视液面', *self.see_display_info[1:4])
        #     if self.see_display_head_info:
        #         self.faultyOperation(2, '读取示数时眼睛要平视液面', *self.see_display_head_info[1:4])
        if water_columns_front.shape[0] == 0:
            return
        water_column_front_box = water_columns_front[0][:4]  # 水柱
        water_column_center_point_up = (
            (water_column_front_box[0] + water_column_front_box[2]) / 2, water_column_front_box[1])  # 水柱液面中心点
        v_d_thre_b = self.h_front * 0.3  # 判错用
        # v_d_thre = self.h_front * 0.14  # 眼睛和液面垂直距离阈值 1080 * 1920 约 150 pixel
        v_d_thre = self.h_front * 0.2  # 眼睛和液面垂直距离阈值 1080 * 1920 约 150 pixel
        head_front_box = None  # 离水柱最近的头的检测框box
        dis_head_water = 0
        if heads_front.shape[0] > 0:  # 选距离水柱最近的头
            for head_front in heads_front:
                head_front_box_ = head_front[:4]
                dis_head_water_ = distance_point(center_point(head_front_box_), water_column_center_point_up)
                if dis_head_water == 0 or dis_head_water_ < dis_head_water:
                    head_front_box = head_front_box_
                    dis_head_water = dis_head_water_
        if (head_front_box is not None
                and abs(center_point(head_front_box)[1] - water_column_front_box[1]) < v_d_thre_b):
            if eyes_front.shape[0] > 0:  # 眼睛
                eye_front_boxes = []
                for eye_front in eyes_front:
                    eye_front_box_ = eye_front[:4]
                    if box1_in_box2(eye_front_box_, head_front_box):
                        eye_front_boxes.append(eye_front_box_)
                eye_center_h = 0
                if len(eye_front_boxes) == 1:
                    eye_center_h = center_point(eye_front_boxes[0])[1]  # 眼睛中心高度
                elif len(eye_front_boxes) == 2:
                    eye_center_h = (center_point(eye_front_boxes[0])[1] + center_point(eye_front_boxes[1])[1]) / 2
                if eye_center_h != 0:  # 以眼睛计算
                    dis_eye_water = abs(eye_center_h - water_column_front_box[1])  # 眼睛与液面垂直距离
                    box = combineBox(*eye_front_boxes, water_column_front_box)
                    if not self.see_display_info or dis_eye_water < self.see_display_info[-2]:
                        self.see_display_info = [self.frame_front, self.time_front, self.objects_front,
                                                 self.preds_front, self.num_frame_front, box, dis_eye_water, self.secs]
                    else:
                        self.see_display_info[-1] = self.secs

                    if dis_eye_water < v_d_thre:
                        self.read_display_secs, self.read_display_secs_pre, flag = self.duration(self.read_display_secs,
                                                                                                 0.5,
                                                                                                 self.read_display_secs_pre,
                                                                                                 0.3)
                        if flag:
                            if not self.read_display_info or dis_eye_water < self.read_display_info[-2]:
                                self.read_display_info = [self.frame_front, self.time_front,
                                                          self.objects_front, self.preds_front, self.num_frame_front,
                                                          box, dis_eye_water, self.secs]
                            else:
                                self.read_display_info[-1] = self.secs
                            if self.read_display_head_info:
                                self.read_display_head_info[-1] = self.secs

            else:  # 以头中心算
                box = combineBox(head_front_box, water_column_front_box)
                if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                    self.see_display_head_info = [self.frame_front, self.time_front,
                                                  self.objects_front, self.preds_front, self.num_frame_front,
                                                  box, dis_head_water, self.secs]
                else:
                    self.see_display_head_info[-1] = self.secs
                if abs(center_point(head_front_box)[1] - water_column_front_box[1]) < v_d_thre:
                    self.read_display_secs, self.read_display_secs_pre, flag = self.duration(self.read_display_secs,
                                                                                             0.5,
                                                                                             self.read_display_secs_pre,
                                                                                             0.3)
                    if flag:
                        if not self.read_display_head_info or dis_head_water < self.read_display_head_info[-2]:
                            self.read_display_head_info = [self.frame_front, self.time_front,
                                                           self.objects_front, self.preds_front,
                                                           self.num_frame_front, box,
                                                           dis_head_water, self.secs]
                        else:
                            self.read_display_head_info[-1] = self.secs
                        if self.read_display_info:
                            self.read_display_info[-1] = self.secs

        if self.read_display_info and self.secs - self.read_display_info[-1] > 1.5:  # 1.5 秒后赋分
            # if self.dropper_water_flag:
            #     x = int(self.see_display_score[4])
            #     if x < self.w_front / 4:
            #         x1, x2 = 0, int(self.w_front / 2)
            #     elif x < (self.w_front / 4) * 3:
            #         x1, x2 = int(x - self.w_front / 4), int(x + self.w_front / 4)
            #     else:
            #         x1, x2 = int(self.w_front / 2), int(self.w_front)
            #     self.plot(self.see_display_score[2], self.see_display_score[1])
            #     img2 = self.see_display_score[1][:, x1:x2, :]
            #     img = np.hstack([self.dropper_water_frame, img2])
            #     self.see_display_score[1] = img
            #     self.see_display_score[2] = None
            return self.read_display_info[:6]
        elif self.read_display_head_info and self.secs - self.read_display_head_info[-1] > 1:
            return self.read_display_head_info[:6]

    def handNotOnScale(self, hands_top, salver_top_box, hands_front, salver_front_box):
        """
        判断手和天平相交（判断天平称量或者置零时，手不能在托盘上）
        :param hands_top: 顶视手
        :param salver_top_box: 顶视托盘
        :param hands_front: 前视手
        :param salver_front_box: 前视托盘
        :return: bool
        """
        hand_salver_top_flag = True  # 手和托盘没有交集？
        hand_salver_front_flag = True  # 手和托盘没有交集？
        if hands_top.shape[0] > 0 and salver_top_box is not None:
            if pt_in_polygon(center_point(salver_top_box), self.center_area_top):
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, salver_top_box) > box_area(salver_top_box) * 0.25:
                        hand_salver_top_flag = False
        if not hand_salver_top_flag and hands_front.shape[0] > 0 and salver_front_box is not None:
            if pt_in_polygon(center_point(salver_front_box), self.center_area_front):
                for hand_front in hands_front:  # 前视 手与天平是否相交
                    hand_front_box = hand_front[:4]
                    if iou(salver_front_box, hand_front_box) > box_area(salver_front_box) * 0.4:
                        hand_salver_front_flag = False
        if hand_salver_top_flag or hand_salver_front_flag:  # 手不在托盘上
            return True

    # 量筒是否在电子天平托盘上
    def cylinderOnSalver(self, scales_top, salvers_top, measuring_cylinders_top,
                         measuring_cylinder_bottoms_top, scales_front, salvers_front,
                         measuring_cylinders_front, measuring_cylinder_bottoms_front):
        """
        判断量筒是否在天平托盘上
        :param scales_top: 顶视 天平
        :param salvers_top: 顶视 托盘
        :param measuring_cylinders_top: 顶视量筒
        :param hands_front: 前视手
        :param scales_front: 前视天平
        :param salvers_front: 前视托盘
        :param measuring_cylinders_front: 前视量筒
        :param measuring_cylinder_bottoms_front: 前视量筒底
        :return: bool
        """
        salver_top_box = self.salverBox(salvers_top, scales_top)
        salver_front_box = self.salverBox(salvers_front, scales_front, 'front')
        if (measuring_cylinder_bottoms_front.shape[0] > 0  # 前视 量筒底
                and measuring_cylinders_front.shape[0] > 0  # 前视 量筒
                and salver_front_box is not None):
            measuring_cylinder_front_box = measuring_cylinders_front[0][:4]
            measuring_cylinder_bottom_front_box = measuring_cylinder_bottoms_front[0][:4]
            w = measuring_cylinder_bottom_front_box[2] - measuring_cylinder_bottom_front_box[0]
            if (iou(measuring_cylinder_bottom_front_box, salver_front_box) > 0
                    and center_distance_h(measuring_cylinder_front_box, measuring_cylinder_bottom_front_box,
                                          True) < w / 3
                    and abs(center_distance_h(measuring_cylinder_bottom_front_box,
                                              salver_front_box)) < self.h_front * 0.052):
                return True
        elif (salver_top_box is not None
              and pt_in_polygon(center_point(salver_top_box), self.center_area_top)):  # 顶视
            if measuring_cylinders_top.shape[0] > 0 and measuring_cylinder_bottoms_top.shape[0] > 0:
                measuring_cylinder_top_box = measuring_cylinders_top[0][:4]  # 量筒
                measuring_cylinder_bottom_top_box = measuring_cylinder_bottoms_top[0][:4]  # 量筒底
                d = distance_box(measuring_cylinder_top_box, measuring_cylinder_bottom_top_box) * 2
                salver_w = (salver_top_box[2] - salver_top_box[1]) / 2
                r = min(salver_w / d, 1)
                if (iou(measuring_cylinder_bottom_top_box, salver_top_box) == box_area(
                        measuring_cylinder_bottom_top_box)
                    and iou(measuring_cylinder_top_box, salver_top_box)) > box_area(measuring_cylinder_top_box) * r:
                    return True
            elif measuring_cylinders_top.shape[0] > 0:
                measuring_cylinder_top_box = measuring_cylinders_top[0][:4]  # 量筒
                d = distance_box(measuring_cylinder_top_box, salver_top_box) * 2
                salver_w = (salver_top_box[2] - salver_top_box[1]) / 2
                r = min(salver_w / d, 1)
                if (iou(measuring_cylinder_top_box, salver_top_box)) > box_area(measuring_cylinder_top_box) * r:
                    return True
            elif measuring_cylinder_bottoms_top.shape[0] > 0:
                measuring_cylinder_bottom_top_box = measuring_cylinder_bottoms_top[0][:4]  # 量筒底
                if iou(measuring_cylinder_bottom_top_box, salver_top_box) == box_area(
                        measuring_cylinder_bottom_top_box):
                    return True

    @try_decorator
    def label_no_toward_palm(self, hands_front, labels_front):  # 标签未朝手心
        if labels_front.shape[0] > 0 and hands_front.shape[0] > 0:
            for label_front in labels_front:
                label_front_box = label_front[:4]
                hand_label = False
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if iou(hand_front_box, label_front_box) > 0:
                        hand_label = True
                        break
                if hand_label and center_point(label_front_box)[1] < (self.h_front / 2):
                    self.label_no_tpward_palm_secs, self.label_no_tpward_palm_secs_pre, flag = self.duration(
                        self.label_no_tpward_palm_secs,
                        1.5,
                        self.label_no_tpward_palm_secs_pre,
                        1)
                    if flag:
                        return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]

    def updateInfoList(self, score_index, info_list, view='front', step=1.):
        """
        更新记录信息
        :param score_index: 得分点列表
        :param info_list: 记录信息列表self.cylinder_on_salver = False  # 量筒在天平上
        self.cylinder_on_salver_secs = 0
        self.cylinder_on_salver_secs_pre = 0
        self.cylinder_not_on_salver_secs = 0
        self.cylinder_not_on_salver_secs_pre = 0
        :param view: 视角
        :param step: 间隔时长
        :return:
        """
        update = False
        if len(info_list) == 0:
            update = True
        else:
            l = len(info_list)
            if self.secs - info_list[-1][-1] > l * step:
                update = True
            if update and l == 3:
                info_list.pop(0)
        if update:
            if view == 'front':
                info_list.append([score_index, self.frame_front, self.time_front, self.objects_front,
                                  self.preds_front, self.num_frame_front, self.secs])
            else:
                info_list.append([score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                  self.num_frame_top, self.secs])
        return info_list

    @try_decorator
    def clearnDesk(self, items_views, center_area_views, views=None):
        """
        整理桌面
        :param score_index: 得分点索引
        :param items_views: 所用视角目标
        :param center_area_views: 所用视角操作区域
        :return:
        """
        if self.desk_is_clearn(items_views, center_area_views, views):
            self.clearn_desk_info = [self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_desk_secs, _, flag = self.duration(self.clearn_desk_secs, 2)
            if flag:
                self.clearn_desk_secs = 0
                return self.clearn_desk_info[:5]
        else:
            self.clearn_desk_secs = 0

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:  # 结束前 2s 内有记录
            self.assignScore(*self.clearn_desk_info[:6])
