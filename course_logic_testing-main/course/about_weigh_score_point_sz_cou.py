# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 9:22
# @Author  : Qiguangnan
# @File    : about_weigh_score_point_sz_cou.py

"""
有关称量的实验得分点
"""

from .comm import *


class AboutWeigh(ConfigModel):

    def __init__(self, *args, **kwargs):
        super(AboutWeigh, self).__init__(*args, **kwargs)
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
        self.scorePoint21 = False
        self.scorePoint22 = False
        self.scorePoint23 = False
        self.scorePoint24 = False
        self.scorePoint25 = False
        self.scorePoint26 = False
        self.scorePoint27 = False
        self.scorePoint28 = False
        self.scorePoint29 = False
        self.scorePoint30 = False

        self.initScaleOpen()  # 初始化打开电子天平
        self.initScaleZero()  # 初始化电子天平置零
        self.init_correct_select_measuring_cylinder()  # 选择正确的量筒
        self.initWaterInCylinder()  # 初始化向量筒中加入水
        self.initDropWater2Cylinder()  # 初始化胶头滴管向量筒中滴加水
        self.initReadCylinderDiaplayData()  # 初始读取量筒示数
        self.initWater2Beaker()  # 初始化水从量筒倒入烧杯
        self.init_no_water_column()
        self.init_select_glass_rod_stir()  # 初始化选择玻璃棒搅拌
        self.init_correct_use_glass_rod_stir()  # 初始化正确使用玻璃棒搅拌
        self.init_auxiliary_glass_rod_stir()  # 辅助判断
        self.initStirDissolve()  # 初始化搅拌溶解(玻璃棒在烧杯中搅拌)
        self.initTransferLiquid()  # 初始化转移液体(将液体从烧杯倒入细口瓶)
        self.init_correct_write_label()  # 初始化写标签
        self.init_stick_label()  # 初始化贴标签
        self.initClearnDesk()  # 初始化清理桌面

        self.initScaleBalance()  # 初始化天平平衡
        self.initSetRider()  # 初始化设置游码
        self.initPlaceWeighPaper()  # 初始化放置称量纸
        self.initUseSpoon()  # (托盘天平)使用药匙
        self.initStopperUpend()  # 瓶塞倒放
        self.initPatWeigh()  # 初始化轻拍
        self.initWeighBalance()  # 初始化称量天平平衡

    def initScaleBalance(self):  # 天平平衡
        self.BALANCE_ANGLE_THRE = 2  # 判断天平平衡阈值
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
        self.stoper_unend_info = []

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

    def init_correct_select_measuring_cylinder(self):  # 选择正确的量筒
        self.small_measuring_cylinder_bottom_area = 0  # 顶视小量筒底面积
        self.large_measuring_cylinder_bottom_area = 0  # 前视小量筒底面积

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
        self.cylinder_front_box = None
        self.drop_water_info_top = []

    def initReadCylinderDiaplayData(self):
        self.read_display_score_secs = 0  # 得分时间
        self.read_display_secs = 0  # 开始读示数秒数
        self.read_display_secs_pre = 0  # 上一帧读示数秒数
        self.see_display_info = []  # 记录读取液面示数信息(眼睛)
        self.see_display_head_info = []  # 记录看页面信息(只检测出头)
        self.read_display_info = []  # 记录读取液面示数信息(眼睛)
        self.read_display_head_info = []  # 记录看页面信息(只检测出头)

    def initWater2Beaker(self):
        self.water_in_beaker_flag = False
        self.water_notin_beaker_secs = 0  # 记录烧杯中没有液体的时间点  # todo 待完善证据链(时间间隔)
        self.water_to_beaker_secs = 0  # 记录量筒中添加水的时间
        self.water_in_beaker_secs = 0  # 记录烧杯中有液体的时间点
        self.water_to_beaker_info = []  # 记录量筒中水倒入烧杯
        self.water_beaker_time_interval_THRE = 5  # 烧杯中没水-加水-有水的时间间隔阈值

    def init_no_water_column(self):
        self.no_water_column_secs = 0
        self.no_water_column_secs_pre = 0
        self.no_water_column_flag = False

    def init_select_glass_rod_stir(self):  # 初始化选择玻璃棒搅拌
        self.select_glass_rod_stir_info = []
        self.select_glass_rod_stir_info_top = []
        self.select_glass_rod_stir_secs = 0
        self.select_glass_rod_stir_secs_pre = 0

    def init_correct_use_glass_rod_stir(self):  # 初始化正确使用玻璃棒搅拌
        self.correct_use_glass_rod_stir_secs = 0
        self.correct_use_glass_rod_stir_secs_pre = 0
        self.correct_use_glass_rod_stir_infos = []

    def init_auxiliary_glass_rod_stir(self):  # 玻璃棒搅拌辅助判断
        self.use_glass_rod_secs = 0
        self.hand_over_beaker = False  # 手在烧杯上方
        self.hand_over_beaker_secs = 0
        self.hand_over_beaker_secs_pre = 0

    def initStirDissolve(self):
        self.stir_dissolve_secs = 0  # 搅拌溶解开始秒数
        self.stir_dissolve_secs_pre = 0  # 前一帧搅拌秒数间
        self.stir_dissolve_info = []  # 记录搅拌信息

    def initTransferLiquid(self):
        self.transfer_liquid_flag = False
        self.transfer_liquid_secs = 0
        self.transfer_liquid_info = []  # 烧杯向细口瓶倾倒液体

    def init_correct_write_label(self):  # 初始化写标签
        self.correct_write_label_info = []  # 记录写标签的赋分信息
        self.correct_write_label_secs = 0
        self.correct_write_label_secs_pre = 0

    def init_stick_label(self):  # 贴标签
        self.stick_label_info = []  # 记录写标签的赋分信息

    def initClearnDesk(self):
        self.clearn_desk_secs = 0.  # 开始清理桌面秒数
        self.clearn_desk_info = []  # 记录整理桌面的信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def getMeasuringCylindersMouthBox(self, measuring_cylinder_front_box, measuring_cylinder_bottom_front_box):
        """
        由量筒、量筒底的检测框返回量筒口大致位置
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
    def water2beaker(self, hands_front, measuring_cylinders_front, measuring_cylinder_bottoms_front, beakers_front,
                     liquids_front):
        """
        量筒水倒入烧杯中
        :param hands_front: 前视手
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
            for measuring_cylinder_front in measuring_cylinders_front:
                cylinder_front_box = measuring_cylinder_front[:4]
                hand_cylinder = False  # 手拿量筒
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if iou(hand_front_box, cylinder_front_box) > box_area(hand_front) * 0.4:
                        hand_cylinder = True
                        break
                if not hand_cylinder:
                    continue
                for measuring_cylinder_bottom_front in measuring_cylinder_bottoms_front:
                    cylinder_bottom_front_box = measuring_cylinder_bottom_front[:4]
                    if iou(cylinder_front_box, cylinder_bottom_front_box) > 0:
                        cylinder_front_box = measuring_cylinders_front[0][:4]  # 量筒
                        cylinder_bottom_front_box = measuring_cylinder_bottoms_front[0][:4]  # 量筒底
                        cylinder_mouth_front_box = self.getMeasuringCylindersMouthBox(cylinder_front_box,
                                                                                      cylinder_bottom_front_box)  # 量筒口框
                        cylinder_b_d = center_distance_v(cylinder_front_box, cylinder_bottom_front_box)  # 量筒底 和量筒中心垂直距离
                        for beaker_front in beakers_front:
                            beaker_front_box = beaker_front[:4]
                            if (cylinder_b_d > 0  # 量筒底高于量筒中心
                                    and min_dis_boxes(cylinder_mouth_front_box,
                                                      beaker_front_box) < self.h_front * 0.028):  # # 量筒口贴近烧杯
                                if not self.water_to_beaker_info or cylinder_b_d > self.water_to_beaker_info[-2]:
                                    box = combineBox(cylinder_front_box, cylinder_bottom_front_box, beaker_front_box)
                                    self.water_to_beaker_info = [self.frame_front, self.time_front, self.objects_front,
                                                                 self.preds_front, self.num_frame_front, box,
                                                                 cylinder_b_d, self.secs]
                                else:
                                    self.water_to_beaker_info[-1] = self.secs
                                return
        if self.water_to_beaker_info and self.secs - self.water_to_beaker_info[-1] > 1:
            self.water_in_beaker_flag = True
            self.water_in_beaker_secs = self.secs
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
    def stopperUpend(self, stopper_upend_front, stopper_no_upend_front, stopper_upend_top,
                     stopper_no_upend_top):  # TODO 细口瓶 ？ 广口瓶
        # hands_front, wild_mouth_bottles_front, narrow_mouth_bottles_front,
        # hands_top, wild_mouth_bottles_top, narrow_mouth_bottles_top
        """
        瓶塞倒放
        :param stopper_upend_front: 前视瓶塞倒放
        :param stopper_no_upend_front: 前视瓶塞未倒放
        :param stopper_upend_top: 顶视瓶塞倒放
        :param stopper_no_upend_top: 顶视瓶塞未倒放
        :param hands_front: 前视手
        :param wild_mouth_bottles_front: 前视广口瓶
        :param narrow_mouth_bottles_front: 前视细口瓶
        :param hands_top: 顶视手
        :param wild_mouth_bottles_top: 顶视广口瓶
        :param narrow_mouth_bottles_top: 顶视细口瓶
        :return:
        """
        record = ''
        if stopper_upend_front.shape[0] > 0:  # 前视瓶塞倒放
            record = "front"
        elif stopper_no_upend_front.shape[0] == 0 and stopper_upend_top.shape[0] > 0:  # 顶视瓶塞倒放 前视没有瓶塞未倒放
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
                    self.stoper_unend_info = [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                              self.num_frame_front, self.secs]
                    #     return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                    #             self.num_frame_front]
                else:
                    self.stoper_unend_info = [self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                              self.num_frame_top, self.secs]
                    # return [self.frame_top, self.time_top, self.objects_top, self.preds_top,
                    #         self.num_frame_top]

    def pour_water_to_cylinder(self, containers_front, measuring_cylinders_front):
        """
        向量筒中倒水
        Args:
            containers_front: 倒水容器
            measuring_cylinders_front: 量筒

        Returns:

        """
        for measuring_cylinder_front in measuring_cylinders_front:
            measuring_cylinder_front_box = measuring_cylinder_front[:4]
            for container_front in containers_front:
                container_front_box = container_front[:4]
                if (center_distance_v(measuring_cylinder_front_box, container_front_box) > 0
                        and iou(measuring_cylinder_front_box, container_front_box)):
                    return True

    def get_angle(self, left_bar_box, right_bar_box):
        """
        托盘天平由两个托盘杆得出平衡时的角度和当前角度
        :param left_bar_box:
        :param right_bar_box:
        :return:
        """
        center_d = (center_point(left_bar_box)[0] + center_point(right_bar_box)[
            0]) / 2 - self.w_front / 2  # 天平中心距图片中心距离
        l_h, r_h = high(left_bar_box), high(right_bar_box)
        h = l_h - r_h
        w = center_point(right_bar_box)[0] - center_point(left_bar_box)[0]
        angle = (math.atan(h / w) / math.pi) * 180  # 计算当前角度
        angle_balance = (center_d / (self.h_front / 2)) * 6  # 计算平衡角度

        # 以下为可视化部分

        point = (int(left_bar_box[0]) - 100, int(left_bar_box[1]) + 140)
        point1 = (int(left_bar_box[0]) - 100, int(left_bar_box[1]) + 180)

        cv2.putText(self.frame_front, f"current: {angle:.2f}", point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(self.frame_front, f"balance: {angle_balance:.2f}", point1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                    2)

        return angle, angle_balance

    def scaleBalance(self, score_index, hands_front, salver_bars_front, salvers_top, weigh_papers_top):
        """
        托盘天平平衡
        :param score_index: 得分点索引
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
                    and (sum(self.balance_angle_list[-10:]) / 10 - angle_balance < self.BALANCE_ANGLE_THRE)):  # 误差 2°以内
                self.scale_balance_secs, self.scale_balance_secs_pre, flag = self.duration(self.scale_balance_secs,
                                                                                           2,
                                                                                           self.scale_balance_secs_pre,
                                                                                           1)
                if flag:
                    angle_abs = abs(self.balance_angle_list[-1] - angle_balance)
                    if not self.balance_info or angle_abs < self.balance_info[-1]:
                        self.balance_info = [score_index, self.frame_front, self.time_front, self.objects_front,
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
        cv2.rectangle(self.frame_front, (int(nut_area[0]), int(nut_area[1])), (int(nut_area[2]), int(nut_area[3])),
                      [0, 0, 255], 2, cv2.LINE_AA)
        return nut_area

    def setRider(self, score_index, salver_bars_front, tweezers_front, riders_front, tweezers_top, riders_top):
        """
        游码调节到称量位置
        :param score_index: 得分点索引
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
                    return [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                            self.num_frame_front]
            else:
                self.initSetRider()

    def weighPaperOnScale(self, score_index, scales_top, weigh_papers_top):
        """
        判断托盘天平两边托盘上有称量纸
        :param score_index: 得分点索引
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
                                return
                            else:
                                left = True
                        elif d < 0 and abs(d) > w / 4:
                            if left is True:
                                return
                            else:
                                right = True
                if left and right:
                    self.place_weigh_paper_secs, self.place_weigh_paper_secs_pre, flag = self.duration(
                        self.place_weigh_paper_secs,
                        2,
                        self.place_weigh_paper_secs_pre,
                        1)
                    if flag:
                        return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                self.num_frame_top]

    def useSpoon(self, score_index, salt_granules_front, wild_mouth_bottles_front, spoons_front, scales_front,
                 hands_front, salt_granules_top, wild_mouth_bottles_top, spoons_top, hands_top,
                 scales_top):
        """
        判断使用药匙
        :param score_index: 得分点索引
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
                return [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                        self.num_frame_front]
            else:
                self.use_spoon_current_num += 1
        if record == "top":
            if self.use_spoon_current_num > self.use_spoon_thre_num:
                return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                        self.num_frame_top]
            else:
                self.use_spoon_current_num += 1

    def weighBalance(self, score_index, hands_front, spoons_front, spoon_us_front, salver_bars_front, salvers_front,
                     salt_granules_front, hands_top, spoons_top, spoon_us_top, salvers_top,
                     weigh_papers_top, scales_top, salt_granules_top):
        """
        准确称量NaCL至所需量，天平平衡
        :param score_index:
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
            info = self.scaleBalance(score_index, hands_front, salver_bars_front, salvers_top, weigh_papers_top)
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

    def patWeigh(self, score_index, hands_top, spoons_top, spoon_us_top, scales_top, wild_mouth_bottles_top,
                 spoons_front, spoon_us_front, scales_front, salvers_front):
        """
        轻拍手腕或者药匙()
        :param score_index: 得分点
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
                            spoon_hand_box = deepcopy(hand_top_box)
                        elif orientation == 'left' and spoon_hand_box is None and center_distance_h(spoon_top_box,
                                                                                                    hand_top_box) > 0:  # 左手
                            hand_spoon_num += 1
                            spoon_hand_box = deepcopy(hand_top_box)
                        else:
                            iou_v = iou_h_s
                            hand_spoon_num += 1
                    else:
                        hand_box_list.append(hand_top_box)
                if hand_spoon_num == 2:  # 两只手与药匙相交
                    if iou_v > box_area(spoon_top_box) * 0.45:
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
                            # 画图
                            cv2.rectangle(self.frame_top, (int(area_box[0]), int(area_box[1])),
                                          (int(area_box[2]), int(area_box[3])), [0, 0, 255], 2,
                                          cv2.LINE_AA)
                            iou_v += iou(area_box, hand_top_box)
        if iou_v > 0:
            if not self.pat_weigh_info or iou_v > self.pat_weigh_info[-2]:
                self.pat_weigh_info = [score_index, self.frame_top, self.time_top, self.objects_top,
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
                return self.pat_weigh_info[:6]

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
        if top and spoons_top.shape[0] == 1:  # 顶视
            scale_top_box = scales_top[0][:4]
            if spoon_us_top.shape[0] == 1:  # 药匙勺
                spoon_u_top_box = spoon_us_top[0][:4]
                if box1_in_box2(spoon_u_top_box, scale_top_box):
                    return True
            elif spoons_top.shape[0] == 1:
                spoon_top_box = spoons_top[0][:4]
                if iou(scale_top_box, spoon_top_box) > box_area(spoon_top_box) * 0.4:
                    return True

    def correct_select_measuring_cylinder(self, hands_front, measuring_cylinders_front, hands_top,
                                          measuring_cylinders_top, measuring_cylinder_bottoms_top,
                                          large=True):  # todo # 待视频补充完成

        """
        正确选择量筒
        :param hands_front:
        :param measuring_cylinders_front:
        :param hands_top:
        :param measuring_cylinders_top:
        :return:
        """

        # if measuring_cylinder_bottoms_top.shape[0] == 2:
        #     pass
        if self.water_in_cylinder:  # 量筒中有水  在量筒与其他无遮挡的情况下比较量筒底面积的大小
            if measuring_cylinder_bottoms_top.shape[0] == 2:
                is_break = False
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    for measuring_cylinder_bottom_top in measuring_cylinder_bottoms_top:
                        measuring_cylinder_bottom_top_box = measuring_cylinder_bottom_top[:4]
                        if iou(measuring_cylinder_bottom_top_box, hand_top_box) > 0:
                            is_break = True
                            break
                    if is_break:
                        break
                measuring_cylinder_bottom_top_1 = measuring_cylinder_bottoms_top[0][:4]
                measuring_cylinder_bottom_top_2 = measuring_cylinder_bottoms_top[1][:4]
                box_area_1 = box_area(measuring_cylinder_bottom_top_1)
                box_area_2 = box_area(measuring_cylinder_bottom_top_2)
                reference_point = [self.w_top / 2, self.h_top]  # 参考点
                d1 = distance_point(reference_point, center_point(measuring_cylinder_bottom_top_1))
                d2 = distance_point(reference_point, center_point(measuring_cylinder_bottom_top_2))

                if large:
                    if (box_area_1 > box_area_2 and d1 < d2) or (box_area_1 < box_area_2 and d1 > d2):
                        return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front
                else:
                    if (box_area_1 < box_area_2 and d1 < d2) or (box_area_1 > box_area_2 and d1 > d2):
                        return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    @try_decorator
    def dropWater2cylinder(self, droppers_front, measuring_cylinders_front, water_columns_front, liquid_levels_front):
        """
        胶头滴管向量筒中滴加液体
        :param droppers_front: 前视胶头滴管
        :param measuring_cylinders_front: 前视量筒
        :param water_columns_front: 前视水柱
        :param liquid_levels_front: 前视液面
        :return:
        """
        if (droppers_front.shape[0] > 0
                and water_columns_front.shape[0] + liquid_levels_front.shape[0] > 0
                and measuring_cylinders_front.shape[0] > 0):
            dropper_front_box = droppers_front[0][:4]
            for measuring_cylinder_front in measuring_cylinders_front:
                measuring_cylinder_front_box = measuring_cylinder_front[:4]
                if water_columns_front.shape[0] > 0:
                    water_column_front_box = water_columns_front[0][:4]
                    dropper_cylinder_d_h = abs(
                        center_distance_h(dropper_front_box, water_column_front_box))  # 滴管 水柱中心水平距离
                else:
                    liquid_level_front_box = liquid_levels_front[0][:4]
                    dropper_cylinder_d_h = abs(center_distance_h(dropper_front_box, liquid_level_front_box))
                dropper_cylinder_d_h_thre = self.h_front * 0.05  # 1080 * 0.05 54 pixel 滴管 量筒 水平方向阈值
                dropper_cylinder_d_v_thre = -self.h_front * 0.05  # 1080 * 0.045 54 pixel 滴管 量筒 垂直方向阈值
                if (dropper_cylinder_d_h < dropper_cylinder_d_h_thre
                        and measuring_cylinder_front_box[1] - dropper_front_box[3] > dropper_cylinder_d_v_thre):
                    box = combineBox(dropper_front_box, measuring_cylinder_front_box)
                    self.drop_water_info = [self.frame_front, self.time_front, self.objects_front,
                                            self.preds_front, self.num_frame_front, box, None, self.secs]
                    self.drop_water_secs, self.drop_water_secs_pre, flag = self.duration(self.drop_water_secs,
                                                                                         0.8,
                                                                                         self.drop_water_secs_pre,
                                                                                         0.4)
                    if flag:
                        return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front
                    return

    @try_decorator
    def dropWater2cylinderTop(self, droppers_top, measuring_cylinders_top, hands_top):
        """
        胶头滴管向量筒中滴加液体
        :param droppers_front: 前视胶头滴管
        :param measuring_cylinders_front: 前视量筒
        :param water_columns_front: 前视水柱
        :param liquid_levels_front: 前视液面
        :return:
        """
        if droppers_top.shape[0] > 0 and measuring_cylinders_top.shape[0] > 0 and hands_top.shape[0] > 0:
            dropper_top_box = droppers_top[0][:4]
            hand_dropper = False
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(dropper_top_box, hand_top_box) > 0:
                    hand_dropper = True
                    break
            if hand_dropper:
                for measuring_cylinder_top in measuring_cylinders_top:
                    cylinder_top_box = measuring_cylinder_top[:4]
                    if iou(cylinder_top_box, dropper_top_box) > 0:
                        self.drop_water_info_top = [self.frame_top, self.time_top, self.objects_top,
                                                    self.preds_top, self.num_frame_top]

    @try_decorator
    def select_glass_rod_stir(self, glass_rods_front, beakers_front, hands_front, liquids_front,
                              glass_rods_top, beakers_top, hands_top, water_in_beaker_flag):
        """
        选用玻璃棒搅拌
        :param glass_rods_front: 前视玻璃棒
        :param beakers_front: 前视烧杯
        :param hands_front: 前视手
        :param liquids_front: 前视液体
        :param water_in_beaker_flag: 烧杯中有水
        :return:
        """
        if self.glass_rod_stir_in_beaker(glass_rods_front, beakers_front, hands_front, liquids_front,
                                         glass_rods_top, beakers_top, hands_top, water_in_beaker_flag):
            self.select_glass_rod_stir_secs, self.select_glass_rod_stir_secs_pre, flag = self.duration(
                self.select_glass_rod_stir_secs,
                3,
                self.select_glass_rod_stir_secs_pre,
                1.5)
            if flag:
                return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    @try_decorator
    def correct_use_glass_rod_stir(self, glass_rods_front, beakers_front, hands_front, liquids_front,
                                   glass_rods_top, beakers_top, hands_top, water_in_beaker_flag):
        """
        正确使用玻璃棒搅拌
        :param glass_rods_front: 前视玻璃棒
        :param beakers_front: 前视烧杯
        :param hands_front: 前视手
        :param liquids_front: 前视液体
        :param water_in_beaker_flag: 烧杯中是否有水
        :return:
        """
        if self.glass_rod_stir_in_beaker(glass_rods_front, beakers_front, hands_front, liquids_front,
                                         glass_rods_top, beakers_top, hands_top, water_in_beaker_flag):
            self.correct_use_glass_rod_stir_secs, self.correct_use_glass_rod_stir_secs_pre, flag = self.duration(
                self.correct_use_glass_rod_stir_secs,
                5,
                self.correct_use_glass_rod_stir_secs_pre,
                4)
            if flag:
                info = [self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front,
                        self.secs]
                self.correct_use_glass_rod_stir_infos = self.update_info_list_(self.correct_use_glass_rod_stir_infos,
                                                                               info)
                # return self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front
        if (len(self.correct_use_glass_rod_stir_infos) > 0
                and self.secs - self.correct_use_glass_rod_stir_infos[-1][-1] > 5):
            if len(self.correct_use_glass_rod_stir_infos) == 1:
                info = self.correct_use_glass_rod_stir_infos[0]
            else:
                info = self.correct_use_glass_rod_stir_infos[1]
            return info

    def update_info_list_(self, info_lists_pre, info_list, step=1.):
        """
        更新记录信息
        :param info_lists_pre: 上一个记录信息列表
        :param info_list: 当前记录信息列表
        :param step: 间隔时长
        :return:
        """
        update = False
        if not info_lists_pre:
            return [info_list]
        else:
            length = len(info_lists_pre)
            if self.secs - info_lists_pre[-1][-1] > length * step:
                update = True
            if update and length == 3:
                info_lists_pre.pop(0)
        if update:
            info_lists_pre.append(info_list)
            return info_lists_pre
        else:
            return info_lists_pre

    def stirDissolve(self, score_index, glass_rods_front, beakers_front, hands_front, duration_secs=40, reclock_secs=5):
        """
        烧杯中用玻璃棒搅拌至全部溶解
        :param score_index: 得分点索引
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
                        self.stir_dissolve_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                   self.preds_front, self.num_frame_front, box, None, self.secs]
                        if flag:
                            return score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front

    def glass_rod_stir_in_beaker(self, glass_rods_front, beakers_front, hands_front, liquids_front,
                                 glass_rods_top, beakers_top, hands_top, water_in_beaker_flag=True):
        """
        烧杯中用玻璃棒搅拌
        :param glass_rods_front: 前视玻璃棒
        :param beakers_front: 前视烧杯
        :param hands_front: 前视手
        :param liquids_front: 前视液体
        :param water_in_beaker_flag: 前视液体
        :return:
        """
        if glass_rods_top.shape[0] == 1 and beakers_top.shape[0] > 0 and hands_top.shape[0] > 0:
            glass_rod_top_box = glass_rods_top[0][:4]
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(hand_top_box, glass_rod_top_box) > 0:
                    for beaker_top in beakers_top:
                        beaker_top_box = beaker_top[:4]
                        if pt_in_polygon(center_point(beaker_top_box), self.center_area_top):
                            if iou(beaker_top_box, glass_rod_top_box) > 0:
                                self.select_glass_rod_stir_info_top = [self.frame_top, self.time_top,
                                                                       self.objects_top, self.preds_top,
                                                                       self.num_frame_top]
        if glass_rods_front.shape[0] > 0 and beakers_front.shape[0] > 0 and hands_front.shape[0] > 0 and \
                liquids_front.shape[0] > 0:
            glass_rod_front_box = glass_rods_front[0][:4]
            if not pt_in_polygon(center_point(glass_rod_front_box), self.center_area_front):
                return
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
                        if water_in_beaker_flag:
                            return True
                        for liquid_front in liquids_front:
                            liquid_front_box = liquid_front[:4]
                            if iou(liquid_front_box, beaker_front_box) > box_area(liquid_front_box) * 0.5:
                                self.select_glass_rod_stir_info = [self.frame_front, self.time_front,
                                                                   self.objects_front, self.preds_front,
                                                                   self.num_frame_front]
                                return True

    @try_decorator
    def auxiliary_glass_rod_stir(self, glass_rods_front, beakers_front, hands_front, liquids_front,
                                 water_in_beaker_flag):
        """
        正确使用玻璃棒搅拌
        :param glass_rods_front: 前视玻璃棒
        :param beakers_front: 前视烧杯
        :param hands_front: 前视手
        :param liquids_front: 前视液体
        :param water_in_beaker_flag: 烧杯中是否有水
        :return:
        """
        record = False
        beaker_front_box = None
        if water_in_beaker_flag and beakers_front.shape[0] > 0 and hands_front.shape[0] > 0:
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if (min_dis_boxes(beaker_front_box, hand_front_box) < self.h_front * 0.2
                            and center_distance_v(beaker_front_box, hand_front_box) > 0
                            and iou(beaker_front_box, hand_front_box) == 0):
                        record = True
                        break
                if record:
                    break

        elif liquids_front.shape[0] > 0 and beakers_front.shape[0] > 0 and hands_front.shape[0] > 0:
            for liquid_front in liquids_front:
                liquid_front_box = liquid_front[:4]
                for beaker_front in beakers_front:
                    beaker_front_box = beaker_front[:4]
                    if iou(liquid_front_box, beaker_front_box) > box_area(liquid_front_box) * 0.5:
                        for hand_front in hands_front:
                            hand_front_box = hand_front[:4]
                            if (min_dis_boxes(beaker_front_box, hand_front_box) < self.h_front * 0.2
                                    and center_distance_v(beaker_front_box, hand_front_box) > 0
                                    and iou(beaker_front_box, hand_front_box) == 0):
                                record = True
                                break
                        if record:
                            break
                if record:
                    break

        if record:
            self.hand_over_beaker_secs, self.hand_over_beaker_secs_pre, flag = self.duration(self.hand_over_beaker_secs,
                                                                                             5,
                                                                                             self.hand_over_beaker_secs_pre,
                                                                                             1.5)
            if flag:
                if glass_rods_front.shape[0] > 0:
                    for glass_rod_front in glass_rods_front:
                        glass_rod_front_box = glass_rod_front[:4]
                        if (iou(beaker_front_box, glass_rod_front_box) > 0
                                and center_distance_v(beaker_front_box, glass_rod_front_box) > 0):
                            self.use_glass_rod_secs = self.secs
                            break
                return True

    @try_decorator
    def transferLiquid(self, beakers_front, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, hands_front):
        """
        烧杯向细口瓶中转移液体
        :param score_index: 得分点索引
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
                                self.transfer_liquid_info = [self.frame_front, self.time_front,
                                                             self.objects_front, self.preds_front, self.num_frame_front,
                                                             box, d_v, self.secs]
                            else:
                                self.transfer_liquid_info[-1] = self.secs
                            return
        if self.transfer_liquid_info and self.secs - self.transfer_liquid_info[-1] > 0.5:
            self.transfer_liquid_secs = self.transfer_liquid_info[-1]
            self.transfer_liquid_flag = True
            return self.transfer_liquid_info[:6]

    @try_decorator
    def correct_write_label(self, write_labels_front, writings_front, hands_front, pens_front, label_papers_front,
                            write_labels_top, writings_top, hands_top, pens_top, label_papers_top):
        """
        正确书写标签内容
        :param write_labels_front: 前视写标签
        :param writings_front: 前视写标签
        :param hands_front: 前视手
        :param pens_front: 前视笔
        :param label_papers_front: 前视标签纸
        :param write_labels_top: 顶视写标签
        :param writings_top: 顶视写标签
        :param hands_top: 顶视手
        :param pens_top: 顶视笔
        :param label_papers_top: 顶视标签纸
        :return:
        """
        view = None
        # pre_write = False
        # if not pre_write and hands_front.shape[0] > 0 and label_papers_front.shape[0] > 0:
        #     for label_paper_front in label_papers_front:
        #         label_paper_front_box = label_paper_front[:4]
        #         pre_write = True
        #         for hand_front in hands_front:
        #             hand_front_box = hand_front[:4]
        #             if not (pt_in_polygon(center_point(label_paper_front_box), self.center_area_front) and
        #                     min_dis_boxes(label_paper_front_box, hand_front_box) < self.h_front * 0.05):
        #                 pre_write = False
        #                 break
        #         if pre_write:
        #             break
        # if not pre_write and hands_top.shape[0] > 0 and label_papers_top.shape[0] > 0:
        #     for label_paper_top in label_papers_top:
        #         label_paper_top_box = label_paper_top[:4]
        #         pre_write = True
        #         for hand_top in hands_top:
        #             hand_top_box = hand_top[:4]
        #             if not (pt_in_polygon(center_point(label_paper_top_box), self.center_area_top) and
        #                     iou(hand_top_box, label_paper_top_box) > 0):
        #                 pre_write = False
        #                 break
        #         if pre_write:
        #             break
        # if writings_front.shape[0] > 0 and pre_write:
        #     view = "front"
        # if view is None and pre_write and writings_top.shape[0] > 0:
        #     view = "top"
        # if view is None and pre_write and pens_front.shape[0] > 0 and label_papers_front.shape[0] > 0:
        #     for pen_front in pens_front:
        #         pen_front_box = pen_front[:4]
        #         for label_paper_front in label_papers_front:
        #             label_paper_front_box = label_paper_front[:4]
        #             if (min_dis_boxes(pen_front_box, label_paper_front_box) < 0.05 * self.h_front
        #                     and center_distance_v(label_paper_front_box, pen_front_box) > 0):
        #                 view = "front"
        #                 break
        #         if view is not None:
        #             break
        # if view is None and pre_write and pens_top.shape[0] > 0 and label_papers_top.shape[0] > 0:
        #     for pen_top in pens_top:
        #         pen_top_box = pen_top[:4]
        #         for label_paper_top in label_papers_top:
        #             label_paper_top_box = label_paper_top[:4]
        #             if min_dis_boxes(pen_top_box, label_paper_top_box) < 0.05 * self.h_top:
        #                 view = "top"
        #                 break
        #         if view is not None:
        #             break
        # # if writings_front.shape[0] == 1 and pens_front.shape[0] > 0 and label_papers_front.shape[0] > 0:
        # #     writing_front_box = writings_front[0][:4]
        # #     for pen_front in pens_front:
        # #         pen_front_box = pen_front[:4]
        # #         if iou(pen_front_box, writing_front_box) > box_area(pen_front_box) * 0.7:
        # #             view = 'front'
        # #             break
        # # if view is None and writings_top.shape[0] > 0 and pens_top.shape[0] > 0 and label_papers_top.shape[0] > 0:
        # #     writing_top_box = writings_top[0][:4]
        # #     for pen_top in pens_top:
        # #         pen_top_box = pen_top[:4]
        # #         if iou(pen_top_box, writing_top_box) > box_area(pen_top_box):
        # #             view = 'top'
        # #             break
        # if view:
        #     self.updateInfoList(None, self.correct_write_label_info, view)
        #
        # if len(self.correct_write_label_info) > 0 and self.secs - self.correct_write_label_info[-1][-1] > 4:
        #     if len(self.correct_write_label_info) == 1:
        #         return self.correct_write_label_info[0][1:6]
        #     else:
        #         return self.correct_write_label_info[1][1:6]

        if write_labels_front.shape[0] + writings_front.shape[0] > 0:
            view = "front"
        elif write_labels_top.shape[0] + writings_top.shape[0] > 0:
            view = "top"
        if view is not None:
            self.correct_write_label_secs, self.correct_write_label_secs_pre, flag = self.duration(
                self.correct_write_label_secs, 1.5, self.correct_write_label_secs_pre, 0.7)
            if flag:
                self.updateInfoList(None, self.correct_write_label_info, view)
        if len(self.correct_write_label_info) > 0 and self.secs - self.correct_write_label_info[-1][-1] > 4:
            if len(self.correct_write_label_info) == 1:
                return self.correct_write_label_info[0][1:6]
            else:
                return self.correct_write_label_info[1][1:6]

    @try_decorator
    def stick_label(self, labellings_front, narrow_mouth_bottles_front, labellings_top, narrow_mouth_bottles_top):
        """
        试剂瓶上贴上标签
        :param labellings_front: 前视贴标签
        :param narrow_mouth_bottles_front: 前视细口瓶
        :param labellings_top: 顶视贴标签
        :param narrow_mouth_bottles_top: 顶视细口瓶
        :return:
        """
        view = None
        if labellings_front.shape[0] > 0 and narrow_mouth_bottles_front.shape[0] > 0:
            labelling_front_box = labellings_front[0][:4]
            for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
                narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
                if iou(narrow_mouth_bottle_front_box, labelling_front_box) > box_area(
                        narrow_mouth_bottle_front_box) * 0.8:
                    view = 'front'
                    break
        if view is None and labellings_top.shape[0] > 0 and narrow_mouth_bottles_top.shape[0] > 0:
            labelling_top_box = labellings_top[0][:4]
            for narrow_mouth_bottle_top in narrow_mouth_bottles_top:
                narrow_mouth_bottle_top_box = narrow_mouth_bottle_top[:4]
                if iou(narrow_mouth_bottle_top_box, labelling_top_box) > box_area(narrow_mouth_bottle_top_box) * 0.8:
                    view = "top"
                    break
        if view:
            self.updateInfoList(None, self.stick_label_info, view)

        if len(self.stick_label_info) > 0 and self.secs - self.stick_label_info[-1][-1] > 2:
            if len(self.stick_label_info) == 1:
                return self.stick_label_info[0][1:6]
            else:
                return self.stick_label_info[1][1:6]

    @try_decorator
    def waterInCylinder(self, score_index, water_columns_front, liquid_levels_front, measuring_cylinders_front,
                        containers_front=None, duration_secs=2, reclock_secs=1):
        """
        量筒中有水
        :param score_index: 分数索引
        :param water_columns_front: 前视水柱
        :param liquid_levels_front: 前视液面
        :param measuring_cylinders_front: 前视量筒
        :param containers_front: 前视倒水容器
        :param duration_secs: 持续时间
        :param reclock_secs: 重新计时间隔
        :return:
        """
        if measuring_cylinders_front.shape[0] > 0:
            for measuring_cylinder_front in measuring_cylinders_front:
                measuring_cylinder_front_box = measuring_cylinder_front[:4]
                h_cylinder = high(measuring_cylinder_front_box)
                w_cylinder = width(measuring_cylinder_front_box)
                h_water = 0
                record = False
                if water_columns_front.shape[0] > 0:
                    water_column_front_box = water_columns_front[0][:4]
                    h_water = high(water_column_front_box)
                    if (  # pt_in_polygon(center_point(measuring_cylinder_front_box), self.center_area_front)
                            # and
                            iou(measuring_cylinder_front_box, water_column_front_box) >
                            box_area(water_column_front_box) * 0.8
                            and h_water > h_cylinder * 0.1 and h_cylinder > w_cylinder):
                        record = True
                elif liquid_levels_front.shape[0] > 0:
                    liquid_level_front_box = liquid_levels_front[0][:4]
                    h_water = measuring_cylinder_front_box[3] - center_point(liquid_level_front_box)[1]
                    if (iou(measuring_cylinder_front_box, liquid_level_front_box) > box_area(
                            liquid_level_front_box) * 0.7
                            and h_water > h_cylinder * 0.1
                            and liquid_level_front_box[1] > measuring_cylinder_front_box[1]):
                        record = True
                if record:
                    if containers_front is not None and containers_front.shape[0] > 0:
                        for container_front in containers_front:
                            container_front_box = container_front[:4]
                            measuring_cylinder_mouth_front_box = deepcopy(measuring_cylinder_front_box)
                            measuring_cylinder_mouth_front_box[3] -= w_cylinder
                            if (container_front_box[1] > measuring_cylinder_front_box[1] > container_front_box[
                                3]  # 容器在量筒上方
                                    and iou(container_front_box, measuring_cylinder_mouth_front_box) > 0):  # 容器与量筒口有交集
                                self.water_in_cylinder_info = [score_index, self.frame_front, self.time_front,
                                                               self.objects_front, self.preds_front,
                                                               self.num_frame_front, h_water, self.secs]
                    self.water_in_cylinder_secs, self.water_in_cylinder_secs_pre, flag = self.duration(
                        self.water_in_cylinder_secs,
                        duration_secs,
                        self.water_in_cylinder_secs_pre,
                        reclock_secs)
                    if flag:
                        self.water_in_cylinder = True
                        if not self.water_in_cylinder_info_ or self.water_in_cylinder_info_[-2] < h_water:
                            self.water_in_cylinder_info_ = [score_index, self.frame_front, self.time_front,
                                                            self.objects_front, self.preds_front, self.num_frame_front,
                                                            h_water, self.secs]
                    if self.water_in_cylinder_info and self.secs - self.water_in_cylinder_info[-1] > 1.5:
                        return self.water_in_cylinder_info
                    elif self.water_in_cylinder_info_ and self.secs - self.water_in_cylinder_info_[-1] > 1.5:
                        return self.water_in_cylinder_info_
                    break

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

    def get_liquid_level_center_point(self, water_columns_front, liquid_levels_front):
        if liquid_levels_front.shape[0] == 1:
            liquid_level_front_box = liquid_levels_front[0][:4]
            return center_point(liquid_level_front_box)
        if liquid_levels_front.shape[0] == 0 and water_columns_front.shape[0] == 1:
            water_column_front_box = water_columns_front[0][:4]  # 水柱
            return (water_column_front_box[0] + water_column_front_box[2]) / 2, water_column_front_box[1]  # 水柱液面中心点

    @try_decorator
    def preReadDisplayData(self, narrow_mouth_bottles_front, measuring_cylinders_front):
        """
        读示数前，细口瓶高于量筒 认为不在读示数
        :param narrow_mouth_bottles_front:
        :param measuring_cylinders_front:
        :return:
        """
        if narrow_mouth_bottles_front.shape[0] > 0 and measuring_cylinders_front.shape[0] > 0:
            for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
                narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
                for measuring_cylinder_front in measuring_cylinders_front:
                    measuring_cylinders_front_box = measuring_cylinder_front[:4]
                    if center_distance_v(measuring_cylinders_front_box, narrow_mouth_bottle_front_box) > 0:
                        return False
        return True

    @try_decorator
    def no_water_column(self, water_columns_front, liquid_levels_front):
        if water_columns_front.shape[0] == 0 and liquid_levels_front.shape[0] == 0:
            self.no_water_column_secs, self.no_water_column_secs_pre, flag = self.duration(
                self.no_water_column_secs, 3, self.no_water_column_secs_pre, 1.5
            )
            if flag:
                self.no_water_column_flag = True

    @try_decorator
    def readDisplayData(self, hands_front, measuring_cylinders_front, water_columns_front, liquid_levels_front,
                        heads_front, eyes_front):
        """
        读量筒液面示数
        :param measuring_cylinders_front: 前视量筒
        :param water_columns_front: 前视水柱
        :param liquid_levels_front: 前视液面
        :param heads_front: 前视头
        :param eyes_front: 前视眼睛
        :return:
        """
        # if self.is_teach and self.water_to_beaker_flag:
        #     if self.see_display_info:
        #         self.faultyOperation(2, '读取示数时眼睛要平视液面', *self.see_display_info[1:4])
        #     if self.see_display_head_info:
        #         self.faultyOperation(2, '读取示数时眼睛要平视液面', *self.see_display_head_info[1:4])

        measuring_cylinder_front_box = None  # 量筒框
        if measuring_cylinders_front.shape[0] > 0:
            liquid_level_center_point = self.get_liquid_level_center_point(water_columns_front, liquid_levels_front)
            if liquid_level_center_point is None:
                return
            for measuring_cylinder_front in measuring_cylinders_front:
                measuring_cylinder_front_box = measuring_cylinder_front[:4]
                if pt_in_box(liquid_level_center_point, measuring_cylinder_front_box):
                    break
            if liquid_level_center_point is None or measuring_cylinder_front_box is None:
                return
        else:
            return

        v_d_thre_b = self.h_front * 0.3  # 判错用
        # v_d_thre = self.h_front * 0.14  # 眼睛和液面垂直距离阈值 1080 * 1920 约 150 pixel
        v_d_thre = self.h_front * 0.14  # 眼睛和液面垂直距离阈值 1080 * 1920 约 150 pixel
        head_front_box = None  # 离水柱最近的头的检测框box
        dis_head_water = 0
        if heads_front.shape[0] > 0:  # 选距离水柱最近的头
            for head_front in heads_front:
                head_front_box_ = head_front[:4]
                dis_head_water_ = distance_point(center_point(head_front_box_), liquid_level_center_point)
                if dis_head_water == 0 or dis_head_water_ < dis_head_water:
                    head_front_box = head_front_box_
                    dis_head_water = dis_head_water_
        if (head_front_box is not None
                and abs(center_point(head_front_box)[1] - liquid_level_center_point[1]) < v_d_thre_b):
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if iou(hand_front_box, head_front_box) > 0.6 * box_area(hand_front_box):
                    return
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
                    dis_eye_water = abs(eye_center_h - liquid_level_center_point[1])  # 眼睛与液面垂直距离
                    box = combineBox(*eye_front_boxes, measuring_cylinder_front_box)
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
                            if (not self.read_display_info
                                    or (dis_head_water < v_d_thre * 0.5
                                        and self.secs - self.read_display_info[-1] > 1)
                                    or dis_head_water < self.read_display_info[-2]):
                                self.read_display_info = [self.frame_front, self.time_front,
                                                          self.objects_front, self.preds_front, self.num_frame_front,
                                                          box, dis_eye_water, self.secs]
                            else:
                                self.read_display_info[-1] = self.secs
                            if self.read_display_head_info:
                                self.read_display_head_info[-1] = self.secs

            else:  # 以头中心算
                box = combineBox(head_front_box, measuring_cylinder_front_box)
                if not self.see_display_head_info or dis_head_water < self.see_display_head_info[-2]:
                    self.see_display_head_info = [self.frame_front, self.time_front,
                                                  self.objects_front, self.preds_front, self.num_frame_front,
                                                  box, dis_head_water, self.secs]
                else:
                    self.see_display_head_info[-1] = self.secs
                if abs(center_point(head_front_box)[1] - liquid_level_center_point[1]) < v_d_thre:
                    self.read_display_secs, self.read_display_secs_pre, flag = self.duration(self.read_display_secs,
                                                                                             0.5,
                                                                                             self.read_display_secs_pre,
                                                                                             0.3)
                    if flag:
                        if (not self.read_display_head_info
                                or (dis_head_water < v_d_thre * 0.5 and self.secs - self.read_display_head_info[-1] > 1)
                                or dis_head_water < self.read_display_head_info[-2]):
                            self.read_display_head_info = [self.frame_front, self.time_front,
                                                           self.objects_front, self.preds_front,
                                                           self.num_frame_front, box,
                                                           dis_head_water, self.secs]
                        else:
                            self.read_display_head_info[-1] = self.secs
                        if self.read_display_info:
                            self.read_display_info[-1] = self.secs

        if self.read_display_info and self.secs - self.read_display_info[-1] > 1.5:  # 1.5 秒后赋分
            self.read_display_score_secs = self.secs
            return self.read_display_info[:6]
        elif self.read_display_head_info and self.secs - self.read_display_head_info[-1] > 1:
            self.read_display_score_secs = self.secs
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
        判断量筒是否在天平的托盘上
        :param scales_top: 顶视 天平
        :param salvers_top: 顶视 托盘
        :param measuring_cylinders_top: 顶视量筒
        :param measuring_cylinder_bottoms_top: 顶视量筒底
        :param scales_front: 前视天平
        :param salvers_front: 前视托盘
        :param measuring_cylinders_front: 前视量筒
        :param measuring_cylinder_bottoms_front: 前视量筒底
        :return:
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

    def clearnDesk(self, views, items_views, center_area_views):
        """
        整理桌面
        :param score_index: 得分点索引
        :param items_views: 所用视角目标
        :param center_area_views: 所用视角操作区域
        :return:
        """
        if self.desk_is_clearn(views, items_views, center_area_views):
            self.clearn_desk_info = [self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_desk_secs, _, flag = self.duration(self.clearn_desk_secs, 2)
            if flag:
                self.clearn_desk_secs = 0
                return self.clearn_desk_info[:5]
        else:
            self.clearn_desk_secs = 0

    def desk_is_clearn(self, views=None, views_items=None, center_areas=None):
        for view, view_items, center_box in zip(views, views_items, center_areas, ):
            for items in view_items:
                for item in items:
                    item_box = item[:4]
                    if view == "front":
                        if (pt_in_polygon(center_point(item_box), center_box) > 0
                                and self.h_front - item_box[3] > self.h_front * 0.15):
                            return False
                    elif pt_in_polygon(center_point(item_box), center_box) > 0:
                        return False
        return True

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:  # 结束前 2s 内有记录
            self.assignScore(*self.clearn_desk_info[:6])
