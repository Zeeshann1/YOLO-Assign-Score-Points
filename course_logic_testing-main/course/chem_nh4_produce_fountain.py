# -*- coding: utf-8 -*-
# @Time    : 2022/7/2 10:42
# @Author  : Qiguangnan
# @File    : chem_nh4_produce_fountain.py


# -*- coding: utf-8 -*-
# @Time    : 2022/3/1 10:37
# @Author  : Qiguangnan
# @File    : chem_co2_produce_property_sz_cou.py

"""
二氧化碳的制取和性质(试管)
"""

from .comm import *
from copy import deepcopy

experimental_site_front = [[0.223, 0.],
                           [0.303, 0.61],
                           [0.315, 0.665],
                           [0.343, 0.71],
                           [0.385, 0.74],
                           [0.424, 0.75],
                           [0.576, 0.75],
                           [0.615, 0.74],
                           [0.657, 0.71],
                           [0.685, 0.665],
                           [0.697, 0.61],
                           [0.777, 0.]]

experimental_site_top = [[0.35, 1.0],
                         [0.35, 0.72],
                         [0.36, 0.65],
                         [0.38, 0.61],
                         [0.41, 0.58],
                         [0.45, 0.56],
                         [0.55, 0.56],
                         [0.59, 0.58],
                         [0.62, 0.61],
                         [0.64, 0.65],
                         [0.65, 0.72],
                         [0.65, 1.0]]


class CHEM_nh4_produce_fountain(ConfigModel):

    def __init__(self):
        super(CHEM_nh4_produce_fountain, self).__init__()
        self.init_flag = False
        self.last_frame_info = []

    def initScore(self):
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


        self.init_weigt_powder()
        self.init_mix_solid()
        self.init_tube_lean()
        self.init_correct_heat()
        self.init_correct_collect_gas()
        self.init_paper_solt_to_tube()
        self.init_clearn_desk()

    def init_weigt_powder(self):
        self.weigt_powder_front_info = []
        self.weigt_powder_top_info = []

    def init_mix_solid(self):
        self.mix_solid_info = []

    def init_tube_lean(self):
        self.tube_hold = False
        self.tube_hold_secs = 0

    def init_correct_heat(self):
        self.heat_info_list = []

    def init_correct_collect_gas(self):
        self.lask_flask_secs = 0

    def init_paper_solt_to_tube(self):
        self.paper_solt_to_tube_front_info = []
        self.paper_solt_to_tube_top_info = []

    def init_clearn_desk(self):  # 初始化整理桌面
        self.clearn_desk_secs = 0.  # 开始清理桌面秒数
        self.clearn_desk_info = []  # 记录整理桌面的信息

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def score_process(self, *args):  # 赋分逻辑部分
        if not self.init_flag:
            self.initScore()
            self.init_flag = True

            self.center_operation_area_front = (
                    np.array(experimental_site_front) * [self.w_front, self.h_front]).astype(np.int32)
            self.center_area_top = (np.array(experimental_site_top) * [self.w_top, self.h_top]).astype(np.int32)
            self.init_flag = True

        (hands_top, scales_top, salvers_top, wild_mouth_bottles_top, wild_stopper_no_upends_top,
         wild_stopper_upends_top,
         narrow_mouth_bottles_top, narrow_stopper_no_upends_top, narrow_stopper_upends_top, weigh_papers_top,
         liquids_top, spoons_top, beakers_top, droppers_top, alcohol_lamp_flams_top, alcohol_lamps_top,
         alcohol_lamp_caps_top, alcohol_lamp_cap_falses_top, tubes_top, iron_tube_holders_top,
         iron_tube_holder_hs_top,
         paper_slots_top, pedestals_top, rubber_hoses_top, rubber_stoppers_top, pipe_joints_top, pipe_ends_top,
         flatjaw_pinchcocks_top, red_liquids_top, test_papers_top, flask_mouths_top, flask_bellys_top, cottons_top,
         solid_powders_top) = self.preds_top
        """
        CN_list = ['手', '电子天平', '托盘', '广口瓶', '瓶塞未倒放', '瓶塞倒放', '细口瓶', '瓶塞未倒放', '瓶塞倒放', '称量纸', '液体', '药匙', '烧杯', '胶头滴管',
                   '火焰', '酒精灯', '酒精灯帽', '酒精灯帽摆放错', '试管', '试管夹', '试管夹头', '纸槽', '底座', '橡胶管', '橡皮塞', '接头', '导管端头', '红色液体',
                   '试纸', '烧瓶口', '烧瓶', '棉花', '固体粉末']
        """

        (hands_front, scales_front, salvers_front, wild_mouth_bottles_front, wild_stopper_no_upends_front,
         wild_stopper_upends_front, narrow_mouth_bottles_front, narrow_stopper_no_upends_front,
         narrow_stopper_upends_front, weigh_papers_front, liquids_front, spoons_front, beakers_front, droppers_front,
         alcohol_lamp_flams_front, alcohol_lamps_front, alcohol_lamp_caps_front, alcohol_lamp_cap_falses_front,
         tubes_front, iron_tube_holders_front, iron_tube_holder_hs_front, paper_slots_front, pedestals_front,
         rubber_hoses_front, rubber_stoppers_front, pipe_joints_front, pipe_ends_front, flatjaw_pinchcocks_front,
         red_liquids_front, test_papers_front, flask_mouths_front, flask_bellys_front, cottons_front,
         solid_powders_front) = self.preds_front

        self.last_frame_info = [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]

        # 1. 药品取用量恰当
        if not self.scorePoint1:
            info = self.weigt_powder(solid_powders_front, scales_front, salvers_front, weigh_papers_front,
                                     solid_powders_top, scales_top, salvers_top, weigh_papers_top)
            if info is not None:
                self.assignScore(1, *info[:5])

        # 2. 药品在纸上进行混合
        if not self.scorePoint2:
            info = self.mix_solid(solid_powders_top, weigh_papers_top, spoons_top)
            if info is not None:
                self.assignScore(2, *info[:5])

        # 3. 药品用纸槽送入试管中
        if not self.scorePoint3:
            info = self.paper_solt_to_tube(hands_front, paper_slots_front, tubes_front,
                                           hands_top, paper_slots_top, tubes_top)
            if info is not None:
                self.assignScore(3, *info[:5])

        # 4. 正确组装制取氨气装置
        if not self.scorePoint4:
            info = self.ssemble_nh4_device(tubes_front, rubber_stoppers_front, pipe_joints_front, flask_mouths_front,
                                           flask_bellys_front)
            if info is not None:
                self.assignScore(4, *info[:5])

        # 5. 大试管管口向下倾斜
        if not self.scorePoint5:
            info = self.tube_lean(tubes_front, rubber_stoppers_front, iron_tube_holders_front, alcohol_lamps_front,
                                  tubes_top, rubber_stoppers_top, iron_tube_holders_top, alcohol_lamps_top)
            if info is not None:
                self.assignScore(5, *info[:5])

        # 6. 加热方法正确
        if not self.scorePoint6:
            info = self.correct_heat(alcohol_lamps_top, tubes_top, rubber_stoppers_top, iron_tube_holders_top)
            if info is not None:
                self.assignScore(6, *info[:5])

        # 7. 烧瓶口向下收集氨气
        if not self.scorePoint7:
            info = self.correct_collect_gas(flask_mouths_front, flask_bellys_front)
            if info is not None:
                self.assignScore(7, *info[:5])

        # 8. 导管口伸入瓶底
        if not self.scorePoint8 and (self.scorePoint7 or self.scorePoint6):
            info = self.pipe_to_bottom(pipe_ends_top, flask_bellys_top)
            if info is not None:
                self.assignScore(8, *info[:5])

        # 9. 烧瓶口有棉花
        if not self.scorePoint9:
            info = self.cotton_in_mouth(hands_front, cottons_front, flask_mouths_front)
            if info is not None:
                self.assignScore(9, *info[:5])

        # 10.用湿润的红色石蕊试纸放在瓶口验满
        if not self.scorePoint10:
            info = self.check_fill(test_papers_front, cottons_front, flask_mouths_front)
            if info is not None:
                self.assignScore(10, *info[:5])
                self.assignScore(11, *info[:5])

        # 12.正确组装喷泉实验装置
        if not self.scorePoint12:
            info = self.ssemble_fountain_device(hands_front, flask_bellys_front, flask_mouths_front,
                                                rubber_stoppers_front, pipe_joints_front, beakers_front, liquids_front)
            if info is not None:
                self.assignScore(12, *info[:5])

        # 13.胶头滴管装好水
        if not self.scorePoint13:
            info = self.water_in_dropper(flask_mouths_front, rubber_stoppers_front, droppers_front)
            if info is not None:
                self.assignScore(13, *info[:5])

        # 14.烧杯中的水中加入酚酞试液
        if not self.scorePoint14:
            info = self.drop_phenothalin(droppers_front, beakers_front, liquids_front)
            if info is not None:
                self.assignScore(14, *info)

        # 15.喷泉实验成功
        if not self.scorePoint15:
            info = self.fountain_success(red_liquids_front, flask_mouths_front, flask_bellys_front, red_liquids_top,
                                         flask_bellys_top)
            if info is not None:
                self.assignScore(15, *info)
        # 16.烧瓶中喷入水量超过1/2
        if not self.scorePoint16:
            info = self.fountain_more_water(red_liquids_front, flask_bellys_front, red_liquids_top, flask_bellys_top)
            if info is not None:
                self.assignScore(16, *info)
                if not self.scorePoint14:
                    self.assignScore(14, *info)

        items_top = [scales_top, wild_mouth_bottles_top, narrow_mouth_bottles_top, beakers_top, alcohol_lamps_top,
         tubes_top, pedestals_top, red_liquids_top, flask_bellys_top]
        """
            ['手', '电子天平', '托盘', '广口瓶', '瓶塞未倒放', '瓶塞倒放', '细口瓶', '瓶塞未倒放', '瓶塞倒放', '称量纸', '液体', '药匙', '烧杯', '胶头滴管',
                   '火焰', '酒精灯', '酒精灯帽', '酒精灯帽摆放错', '试管', '试管夹', '试管夹头', '纸槽', '底座', '橡胶管', '橡皮塞', '接头', '导管端头', '红色液体',
                   '试纸', '烧瓶口', '烧瓶', '棉花', '固体粉末']
        """
        items_front = [scales_front, narrow_mouth_bottles_front, beakers_front,
         alcohol_lamps_front, tubes_front, pedestals_front,
         red_liquids_front, flask_mouths_front, flask_bellys_front]

        if (not self.scorePoint19 and len(self.score_list) > 2):  # 药品归位、清洗仪器、整理实验台
            info = self.clearn_desk(["top", "front"], [items_top, items_front],
                                    [self.center_area_top, self.center_operation_area_front])
            if info:
                self.assignScore(19, *info[:5])
                self.assignScore(20, *info[:5])


    def update_info_list(self, info_lists_pre, info_list, step=1.):
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

    @try_decorator
    def weigt_powder(self, solid_powders_front, scales_front, salvers_front, weigh_papers_front,
                     solid_powders_top, scales_top, salvers_top, weigh_papers_top):
        record = False
        if solid_powders_front.shape[0] > 0 and scales_front.shape[0] > 0 and solid_powders_top.shape[0] > 0:
            scale_front_box = scales_front[0][:4]
            for solid_powder_front in solid_powders_front:
                solid_powder_front_box = solid_powder_front[:4]
                iou_p = iou(scale_front_box, solid_powder_front_box)
                if iou_p > box_area(solid_powder_front_box) * 0.7:
                    record = True
                    if not self.weigt_powder_front_info or iou_p > self.weigt_powder_front_info[-2]:
                        self.weigt_powder_front_info = [self.frame_front, self.time_front, self.objects_front,
                                                        self.preds_front, self.num_frame_front, iou_p,
                                                        self.secs]
        if not record and solid_powders_top.shape[0] > 0:
            if scales_top.shape[0] > 0:
                scale_top_box = scales_top[0][:4]
                for solid_powder_top in solid_powders_top:
                    solid_powder_topt_box = solid_powder_top[:4]
                    iou_p = iou(scale_top_box, solid_powder_topt_box)
                    if iou_p > box_area(solid_powder_topt_box):
                        if not self.weigt_powder_top_info or iou_p > self.weigt_powder_top_info[-2]:
                            self.weigt_powder_top_info = [self.frame_top, self.time_top, self.objects_top,
                                                          self.preds_top, self.num_frame_top, iou_p,
                                                          self.secs]
            elif weigh_papers_top.shape[0] > 0:
                for weigh_paper_top in weigh_papers_top:
                    weigh_papers_top_box = weigh_paper_top[0][:4]
                    for solid_powder_top in solid_powders_top:
                        solid_powder_topt_box = solid_powder_top[:4]
                        iou_p = iou(weigh_papers_top_box, solid_powder_topt_box)
                        if iou_p > box_area(solid_powder_topt_box):
                            if not self.weigt_powder_top_info or iou_p > self.weigt_powder_top_info[-2]:
                                self.weigt_powder_top_info = [self.frame_top, self.time_top, self.objects_top,
                                                              self.preds_top, self.num_frame_top, iou_p,
                                                              self.secs]
        if self.weigt_powder_front_info:
            if self.secs - self.weigt_powder_front_info[-1] > 5:
                return self.weigt_powder_front_info[:5]
        elif self.weigt_powder_top_info:
            if self.secs - self.weigt_powder_top_info[-1] > 5:
                return self.weigt_powder_top_info[:5]

    @try_decorator
    def mix_solid(self, solid_powders_top, weigh_papers_top, spoons_top):
        if solid_powders_top.shape[0] == 1 and weigh_papers_top.shape[0] > 0 and spoons_top.shape[0] > 0:
            solid_powder_top_box = solid_powders_top[0][:4]
            for weigh_paper_top in weigh_papers_top:
                weigh_paper_top_box = weigh_paper_top[:4]
                for spoon_top in spoons_top:
                    spoon_top_box = spoon_top[:4]
                    if (iou(solid_powder_top_box, weigh_paper_top_box) > 0
                            and iou(spoon_top_box, solid_powder_top_box) > 0):
                        self.mix_solid_info = [self.frame_top, self.time_top, self.objects_top,
                                               self.preds_top, self.num_frame_top, self.secs]
        if self.mix_solid_info and self.secs - self.mix_solid_info[-1] > 10:
            return self.mix_solid_info[:5]

    @try_decorator
    def paper_solt_to_tube(self, hands_front, paper_slots_front, tubes_front,
                           hands_top, paper_slots_top, tubes_top):
        record = False
        if paper_slots_front.shape[0] > 0 and tubes_front.shape[0] > 0 and hands_front.shape[0] > 0:
            for paper_slot_front in paper_slots_front:
                paper_slot_front_box = paper_slot_front[:4]
                for tube_front in tubes_front:
                    tube_front_box = tube_front[:4]
                    hand_tube = False
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, tube_front_box) > 0:
                            hand_tube = True
                            break
                    iou_r = iou(tube_front_box, paper_slot_front_box)
                    if iou_r > 0 and hand_tube:
                        record = True
                        if not self.paper_solt_to_tube_front_info or iou_r > self.paper_solt_to_tube_front_info[-2]:
                            self.paper_solt_to_tube_front_info = [self.frame_front, self.time_front, self.objects_front,
                                                                  self.preds_front, self.num_frame_front, iou_r,
                                                                  self.secs]
                        else:
                            self.paper_solt_to_tube_front_info[-1] = self.secs
        if not record and paper_slots_top.shape[0] > 0 and tubes_top.shape[0] > 0 and hands_top.shape[0] > 0:
            for paper_slot_top in paper_slots_top:
                paper_slot_top_box = paper_slot_top[:4]
                for tube_top in tubes_top:
                    tube_top_box = tube_top[:4]
                    iou_r = iou(tube_top_box, paper_slot_top_box)
                    hand_tube = False
                    for hand_top in hands_front:
                        hand_top_box = hand_top[:4]
                        if iou(hand_top_box, tube_top_box) > 0:
                            hand_tube = True
                            break
                    if iou_r > 0 and hand_tube:
                        if not self.paper_solt_to_tube_top_info or iou_r > self.paper_solt_to_tube_top_info[-2]:
                            self.paper_solt_to_tube_top_info = [self.frame_top, self.time_top, self.objects_top,
                                                                self.preds_top, self.num_frame_top, iou_r, self.secs]
                        else:
                            self.paper_solt_to_tube_top_info[-1] = self.secs

        if self.paper_solt_to_tube_front_info:
            if self.secs - self.paper_solt_to_tube_front_info[-1] > 5:
                return self.paper_solt_to_tube_front_info[:5]
        elif self.paper_solt_to_tube_top_info:
            if self.secs - self.paper_solt_to_tube_top_info[-1] > 5:
                return self.paper_solt_to_tube_top_info[:5]

    @try_decorator
    def ssemble_nh4_device(self, tubes_front, rubber_stoppers_front, pipe_joints_front, flask_mouths_front,
                           flask_bellys_front):
        if self.tube_hold:
            rubber_stopper_box = None
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                for rubber_stopper_front in rubber_stoppers_front:
                    rubber_stopper_front_box = rubber_stopper_front[:4]
                    if iou(tube_front_box, rubber_stopper_front_box) > 0:
                        rubber_stopper_box = deepcopy(rubber_stopper_front_box)
            if rubber_stopper_box is not None and flask_mouths_front.shape[0] > 0 and pipe_joints_front.shape[0] > 0:
                flask_mouth_front_box = flask_mouths_front[0][:4]
                for pipe_joint_front in pipe_joints_front:
                    pipe_joint_front_box = pipe_joint_front[:4]
                    if (rubber_stopper_box[3] > pipe_joint_front_box[1]
                            and center_distance_v(pipe_joint_front_box, flask_mouth_front_box) > 0):
                        return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]

    @try_decorator
    def tube_lean(self, tubes_front, rubber_stoppers_front, iron_tube_holders_front, alcohol_lamps_front,
                  tubes_top, rubber_stoppers_top, iron_tube_holders_top, alcohol_lamps_top):
        if (not self.tube_hold
                and alcohol_lamps_top.shape[0] > 0
                and tubes_top.shape[0] > 0
                and rubber_stoppers_top.shape[0] > 0
                and iron_tube_holders_top.shape[0] > 0):
            alcohol_lamp_top_box = alcohol_lamps_top[0][:4]
            iron_tube_holder_top = iron_tube_holders_top[0][:4]
            for tube_top in tubes_top:
                tube_top_box = tube_top[:4]
                if iou(tube_top_box, alcohol_lamp_top_box) > 0 and iou(iron_tube_holder_top, tube_top_box) > 0:
                    self.tube_hold = True
                    self.tube_hold_secs = self.secs

        if self.tube_hold and tubes_front.shape[0] > 0 and rubber_stoppers_front.shape[0] > 0:
            for rubber_stopper_front in rubber_stoppers_front:
                rubber_stopper_front_box = rubber_stopper_front[:4]
                for tube_front in tubes_front:
                    tube_front_box = tube_front[:4]
                    if (iou(tube_front_box, rubber_stopper_front_box) > 0
                            and center_distance_v(rubber_stopper_front_box, tube_front_box) > 0):
                        return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]

    @try_decorator
    def correct_heat(self, alcohol_lamps_top, tubes_top, rubber_stoppers_top, iron_tube_holders_top):
        if (self.tube_hold
                and alcohol_lamps_top.shape[0] > 0
                and tubes_top.shape[0] > 0
                and rubber_stoppers_top.shape[0] > 0
                and iron_tube_holders_top.shape[0] > 0):
            alcohol_lamp_top_box = alcohol_lamps_top[0][:4]
            iron_tube_holder_top = iron_tube_holders_top[0][:4]
            for tube_top in tubes_top:
                tube_top_box = tube_top[:4]
                if iou(tube_top_box, alcohol_lamp_top_box) > 0 and iou(iron_tube_holder_top, tube_top_box) > 0:
                    heat_info = [self.frame_front, self.time_front, self.objects_front,
                                 self.preds_front, self.num_frame_front, self.secs]
                    self.heat_info_list = self.update_info_list(self.heat_info_list, heat_info, step=3)
        if len(self.heat_info_list) > 0 and self.heat_info_list[-1][-1] - self.tube_hold_secs > 30:
            info = self.heat_info_list[0] if len(self.heat_info_list) == 1 else self.heat_info_list[1]
            return info[:5]

    @try_decorator
    def correct_collect_gas(self, flask_mouths_front, flask_bellys_front):
        if self.tube_hold and self.secs - self.tube_hold_secs > 30:
            if flask_bellys_front.shape[0] > 0:
                self.lask_flask_secs = self.secs
                if flask_mouths_front.shape[0] > 0:
                    flask_mouth_front_box = flask_mouths_front[0][:4]
                    flask_belly_front_box = flask_bellys_front[0][:4]
                    if center_distance_v(flask_mouth_front_box, flask_belly_front_box) > 0:
                        return [self.frame_front, self.time_front, self.objects_front,
                                self.preds_front, self.num_frame_front]
            elif flask_mouths_front.shape[0] > 0 and self.secs - self.lask_flask_secs > 10:
                flask_mouth_front_box = flask_mouths_front[0][:4]
                if flask_mouth_front_box[1] < self.h_front * 0.2:
                    return [self.frame_front, self.time_front, self.objects_front,
                            self.preds_front, self.num_frame_front]

    @try_decorator
    def pipe_to_bottom(self, pipe_ends_top, flask_bellys_top):
        if pipe_ends_top.shape[0] > 0 and flask_bellys_top.shape[0] > 0:
            flask_belly_top_box = flask_bellys_top[0][:4]
            for pipe_end_top in pipe_ends_top:
                pipe_end_top_box = pipe_end_top[:4]
                if iou(pipe_end_top_box, flask_belly_top_box) > box_area(pipe_end_top_box) * 0.6:
                    return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    @try_decorator
    def cotton_in_mouth(self, hands_front, cottons_front, flask_mouths_front):
        if cottons_front.shape[0] > 0 and flask_mouths_front.shape[0] > 0 and hands_front.shape[0] > 0:
            flask_mouth_front_box = flask_mouths_front[0][:4]
            for cotton_front in cottons_front:
                cotton_front_box = cotton_front[:4]
                hand_cotton = False
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if iou(hand_front_box, cotton_front_box) > 0:
                        hand_cotton = True
                        break
                if (not hand_cotton
                        and iou(flask_mouth_front_box, cotton_front_box) > 0
                        and flask_mouth_front_box[1] < self.h_front / 3):
                    return [self.frame_front, self.time_front, self.objects_front,
                            self.preds_front, self.num_frame_front]

    @try_decorator
    def check_fill(self, test_papers_front, cottons_front, flask_mouths_front):
        if test_papers_front.shape[0] > 0 and flask_mouths_front.shape[0] > 0:
            flask_mouth_front_box = flask_mouths_front[0][:4]
            for test_paper_front in test_papers_front:
                test_paper_front_box = test_paper_front[:4]
                if min_dis_boxes(flask_mouth_front_box, test_paper_front_box) < self.h_front * 0.06:
                    return [self.frame_front, self.time_front, self.objects_front,
                            self.preds_front, self.num_frame_front]
        elif test_papers_front.shape[0] > 0 and cottons_front.shape[0] > 0:
            cotton_front_box = cottons_front[0][:4]
            for test_paper_front in test_papers_front:
                test_paper_front_box = test_paper_front[:4]
                if min_dis_boxes(cotton_front_box, test_paper_front_box) < self.h_front * 0.06:
                    return [self.frame_front, self.time_front, self.objects_front,
                            self.preds_front, self.num_frame_front]

    @try_decorator
    def ssemble_fountain_device(self, hands_front, flask_bellys_front, flask_mouths_front, rubber_stoppers_front,
                                pipe_joints_front, beakers_front, liquids_front):
        if (rubber_stoppers_front.shape[0] > 0
                and flask_mouths_front.shape[0] > 0
                and beakers_front.shape[0] > 0):
            flask_mouth_front_box = flask_mouths_front[0][:4]
            for rubber_stopper_front in rubber_stoppers_front:
                rubber_stopper_front_box = rubber_stopper_front[:4]
                if iou(rubber_stopper_front_box, flask_mouth_front_box) > 0:
                    for beaker_front in beakers_front:
                        beaker_front_box = beaker_front[:4]
                        liquid_in_beaker = False
                        for liquid_front in liquids_front:
                            liquid_front_box = liquid_front[:4]
                            if (iou(liquid_front_box, beaker_front_box) > box_area(liquid_front_box) * 0.6
                                    and center_distance_v(liquid_front_box, beaker_front_box) > 0):
                                liquid_in_beaker = True
                                break
                        if (liquid_in_beaker
                                and flask_mouth_front_box[3] < beaker_front_box[1]
                                and center_distance_h(flask_mouth_front_box, beaker_front_box, True) < width(
                                    beaker_front_box) * 1.5):
                            return [self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front]

    @try_decorator
    def water_in_dropper(self, flask_mouths_front, rubber_stoppers_front, droppers_front):
        if flask_mouths_front.shape[0] > 0 and rubber_stoppers_front.shape[0] > 0 and droppers_front.shape[0] > 0:
            flask_mouth_front_box = flask_mouths_front[0][:4]
            for rubber_stopper_front in rubber_stoppers_front:
                rubber_stopper_front_box = rubber_stopper_front[:4]
                for dropper_front in droppers_front:
                    dropper_front_box = dropper_front[:4]
                    if (iou(rubber_stopper_front_box, flask_mouth_front_box) > 0
                            and iou(dropper_front_box, rubber_stopper_front_box) > 0
                            and center_distance_v(dropper_front_box, rubber_stopper_front_box) > 0):
                        return [self.frame_front, self.time_front, self.objects_front,
                                self.preds_front, self.num_frame_front]

    @try_decorator
    def drop_phenothalin(self, droppers_front, beakers_front, liquids_front):
        if droppers_front.shape[0] > 0 and beakers_front.shape[0] > 0 and liquids_front.shape[0] > 0:
            for beaker_front in beakers_front:
                beaker_front_box = beaker_front[:4]
                for dropper_front in droppers_front:
                    dropper_front_box = dropper_front[:4]
                    for liquid_front in liquids_front:
                        liquid_front_box = liquid_front[:4]
                        if (iou(beaker_front_box, liquid_front_box) > box_area(liquid_front_box) * 0.7
                                and center_distance_v(liquid_front_box, beaker_front_box) > 0
                                and min_dis_boxes(beaker_front_box, dropper_front_box) < self.h_front * 0.1
                                and center_distance_v(beaker_front_box, dropper_front_box) > 0):
                            return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                    self.num_frame_front]

    # 15.喷泉实验成功
    @try_decorator
    def fountain_success(self, red_liquids_front, flask_mouths_front, flask_bellys_front, red_liquids_top,
                         flask_bellys_top):
        if red_liquids_front.shape[0] > 0:  # 前视红色液体
            red_liquid_front_box = red_liquids_front[0][:4]
            if center_point(red_liquid_front_box)[1] < self.h_front * 0.7:
                return [self.frame_front, self.time_front, self.objects_front, self.preds_front, self.num_frame_front]
        if red_liquids_top.shape[0] > 0 and flask_bellys_top.shape[0] > 0:
            red_liquid_top_box = red_liquids_top[0][:4]
            flask_belly_top_box = flask_bellys_top[0][:4]
            if iou(red_liquid_top_box, flask_belly_top_box) > box_area(red_liquid_top_box) * 0.6:
                return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    @try_decorator
    def fountain_more_water(self, red_liquids_front, flask_bellys_front, red_liquids_top, flask_bellys_top):
        if red_liquids_front.shape[0] > 0 and flask_bellys_front.shape[0] > 0:  # 前视红色液体
            red_liquid_front_box = red_liquids_front[0][:4]
            flask_belly_front_box = flask_bellys_front[0][:4]  # 烧瓶肚
            if w_h_ratio(flask_belly_front_box) < 1.2:
                if red_liquid_front_box[1] < flask_belly_front_box[1] + high(flask_belly_front_box) / 2:
                    return [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                            self.num_frame_front]
        if red_liquids_top.shape[0] > 0 and flask_bellys_top.shape[0] > 0:
            red_liquid_top_box = red_liquids_top[0][:4]
            flask_belly_top_box = flask_bellys_top[0][:4]
            if (iou(red_liquid_top_box, flask_belly_top_box) > box_area(red_liquid_top_box) * 0.9
                    and box_area(red_liquid_top_box) > box_area(flask_belly_top_box) * 0.65):
                return [self.frame_top, self.time_top, self.objects_top, self.preds_top, self.num_frame_top]

    @try_decorator
    def clearn_desk(self, views, items_views, center_area_views):
        """
        整理桌面
        :param views: 视角列表
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

    @try_decorator
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


    def end(self, *args, **kwargs):
        self.assignScore(17, *self.last_frame_info[:5])
        self.assignScore(18, *self.last_frame_info[:5])
        if not self.scorePoint19 and self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:  # 结束前 2s 内有记录
            self.assignScore(19, *self.clearn_desk_info[:5])
            self.assignScore(20, *self.clearn_desk_info[:5])
