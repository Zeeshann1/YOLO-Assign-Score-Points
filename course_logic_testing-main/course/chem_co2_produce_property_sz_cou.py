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

experimental_site_top = [[0.3, 1.0],
                         [0.3, 0.62],
                         [0.31, 0.55],
                         [0.33, 0.51],
                         [0.36, 0.48],
                         [0.4, 0.46],
                         [0.6, 0.46],
                         [0.64, 0.48],
                         [0.67, 0.51],
                         [0.69, 0.55],
                         [0.7, 0.62],
                         [0.7, 1.0]]

class CHEM_co2_produce_property_sz(ConfigModel):

    def __init__(self):
        super(CHEM_co2_produce_property_sz, self).__init__()
        self.init_flag = False
        self.judget_g = False
        self.last_frame_info = []
        self.last_reaction_secs = 0

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

        self.init_check_gas_tightness()  # 初始化检验气密性(导气管伸入水中，手握试管)
        self.init_correct_assemble_exp_facility_z()  # 初始化组装实验装置(锥形瓶)
        self.init_tweezer_marble()  # 初始化用镊子夹取大理石
        self.init_tube_slow_up()  # 初始化试管加入大理石缓慢竖起
        self.init_pour_hcl_to_tube()  # 初始化向试管中加入稀盐酸
        self.init_select_HCl_z()  # 初始化选择稀盐酸(锥形瓶)
        self.init_correct_add_HCl_z()  # 初始化向长颈漏斗中加入稀盐酸
        self.init_tighten_rubber_stopper()  # 初始化塞紧橡胶塞
        self.init_tube_v_restriction()  # 初始化试管内液体体积限制
        self.init_tube_holder_distance()  # 初始化试管夹距离
        self.init_collect_gas()  # 初始化收集二氧化碳
        self.init_check_gas_fill()  # 初始化验满
        self.init_gas_fill()  # 初始化已验满
        self.init_gas_bottle_up()  # 初始化集气瓶正放
        self.init_extinguish_alcohol_lamp()  # 初始化熄灭酒精灯
        self.init_co2_to_lime_water()  # 初始化通入澄清石灰水
        self.init_lime_water_turbid()  # 初始化澄清石灰水变浑浊
        self.init_litmus_color_change()  # 初始化石蕊变色
        self.init_separate_liquid_solid()  # 初始化固体液体分开
        self.init_clearn_desk()  # 初始化整理桌面

    def init_check_gas_tightness(self):  # 初始化检验气密性(导气管伸入水中，手握试管)
        # self.hold_tube_secs = 0.  # 手握试管时间
        # self.hold_tube_secs_pre = 0.  # 手握试管时间
        self.tube_rubber_stopper = False  # 试管口有橡皮塞
        self.hold_tube_info_1 = []  # 手握试管信息记录
        self.hold_tube_info_2 = []  # 手握试管信息记录

    def init_correct_assemble_exp_facility_z(self):  # 初始化组装实验装置
        self.assemble_facility_z_secs = 0.
        self.assemble_facility_z_secs_pre = 0.
        self.assemble_facility_z_duration = 2
        self.assemble_facility_z_reclock = 1
        self.assemble_facility_z_info = []

    def init_tweezer_marble(self):  # 初始化用镊子夹取大理石
        self.tweezer_marble_thre_num = 4  # 至少检测出4次
        self.tweezer_marble_curr_num = 0
        self.tweezer_marble_info = []

    def init_tube_slow_up(self):  # 初始化试管加入大理石缓慢竖起
        self.TUBE_H_THRE = 1.1  # 试管水平宽高比阈值
        self.TUBE_V_THRE = 0.5  # 试管竖直宽高比阈值
        self.tube_h_info = []  # 试管平放
        self.tube_v_info = []  # 试管竖起

    def init_pour_hcl_to_tube(self):  # 初始化向试管中加入稀盐酸
        self.reaction_flag = False  # 反应标志
        self.reaction_s_secs = 0  # 开始反应的时间
        self.reaction_s_secs_pre = 0  # 开始反应的时间
        self.pour_hcl_info = []

    def init_select_HCl_z(self):  # 初始化选择稀盐酸(锥形瓶)
        self.select_HCl_z_info = []
        self.select_HCl_z_secs = 0
        self.select_HCl_z_secs_pre = 0
        self.check_select_HCl_z_info = False
        self.reastion_z_info = []
        self.reaction_z_secs = 0
        self.reaction_z_secs_pre = 0  # 开始反应的时间

    def init_correct_add_HCl_z(self):  # 初始化向长颈漏斗中加入稀盐酸
        self.gas_reaction_z_flag = False  # 反应标志
        self.gas_reaction_z_secs = 0  # 开始反应的时间
        self.gas_reaction_z_secs_pre = 0  # 开始反应的时间
        self.add_hcl_z_infos = []  # 记录加盐酸信息
        self.add_hcl_z_secs = 0
        self.add_hcl_z_secs_pre = 0
        self.check_add_hcl_z_infos = False
        self.add_hcl_done_z_info = []  # 记录加盐酸信息
        self.add_hcl_done_z_secs = 0  # 添加稀盐酸完成
        self.add_hcl_done_z_secs_pre = 0  # 添加稀盐酸完成

    def init_tighten_rubber_stopper(self):
        self.tighten_rubber_stopper_secs = 0
        self.tighten_rubber_stopper_secs_pre = 0
        self.tighten_rubber_stopper_thre_num = 4
        self.tighten_rubber_stopper_curr_num = 0
        self.tighten_rubber_stopper_info = []

    def init_tube_v_restriction(self):
        self.V_R_THRE = 0.7  # 溶液高度 / 试管高度
        self.v_r_list = []

    def init_tube_holder_distance(self):  # 初始化试管夹距离
        self.TUBE_HOLDER_D = 0.5  # 试管夹距试管口 1/2
        self.tube_holder_d_list = []

    def init_collect_gas(self):  # 初始化收集二氧化碳
        self.collect_gas_flag_secs = 0
        self.collect_gas_flag_secs_pre = 0
        self.collect_gas_secs = 0
        self.collect_gas_secs_pre = 0
        self.collect_gas_flag = False

    def init_check_gas_fill(self):  # 初始化验满
        self.BUTN_BOTTLE_D_THRE = self.h_front * 0.03  # 约
        self.check_gas_fill_flag = False
        self.check_gas_fill_info = []  # 记录验满信息

    def init_gas_fill(self):  # 初始化已验满
        self.EXTINGUISH_BOTTLE_D_THRE = self.h_front * 0.06
        self.gas_fill_flag = False
        self.gas_fill_info = []
        self.gas_fill_info_default = []
        self.gas_fill_secs = 0
        self.gas_fill_secs_pre = 0

    def init_gas_bottle_up(self):  # 初始化集气瓶正放
        self.gas_bottle_up_secs = 0
        self.gas_bottle_up_secs_pre = 0

    def init_extinguish_alcohol_lamp(self):  # 初始化熄灭酒精灯
        self.alcohol_burn_flag = False
        self.alcohol_burn_secs = 0
        self.alcohol_burn_secs_pre = 0
        self.alcohol_burn_duration_THRE = 2  # 判断酒精灯燃烧持续时间阈值
        self.alcohol_burn_interval_THRE = 1  # 判断酒精灯燃烧间隔时间阈值
        self.last_alcohol_burn_secs = 0  # 酒精灯燃烧时间
        self.alcohol_with_cap = 0  # 酒精灯盖帽时间
        self.BURN_EXTINGUISH_INTERVAL_THRE = 0.5  # 酒精灯燃烧和熄灭时间间隔阈值
        self.flame_cap_info = []  # 记录灯帽在火焰附近信息
        self.last_flame_info = []  # 最后一张燃烧的画面
        self.cap_lamp_cap_top_info = []  # 记录盖灯帽的信息
        self.cap_lamp_cap_front_info = []  # 记录盖灯帽的信息

    def init_co2_to_lime_water(self):  # 初始化通入澄清石灰水
        self.co2_limewater_secs = 0
        self.co2_limewater_secs_pre = 0
        self.co2_to_lime_water_flag = False

    def init_lime_water_turbid(self):  # 初始化澄清石灰水变浑浊
        self.lime_water_turbid_secs = 0
        self.lime_water_turbid_secs_pre = 0

    def init_litmus_color_change(self):  # 初始化石蕊变色
        self.init_litmus_purple()
        self.init_litmus_purple_top()
        self.init_litmus_pink()
        self.init_litmus_pink_top()
        self.litmus_color_change_secs = 0
        self.litmus_color_change_check = False

    def init_litmus_purple(self):
        self.litmus_purple_secs = 0
        self.litmus_purple_n = 0
        self.LITMUS_PURPLE_N_THRED = 10
        self.litmus_purple_info = []

    def init_litmus_purple_top(self):
        self.litmus_purple_top_secs = 0
        self.litmus_purple_n_top = 0
        self.LITMUS_PURPLE_N_TOP_THRED = 10
        self.litmus_purple_top_info = []

    def init_litmus_pink(self):
        self.litmus_pink_secs = 0
        self.litmus_pink_n = 0
        self.LITMUS_PINK_N_THRE = 10
        self.litmus_pink_info = []
        self.litmus_only_pink_info = []  # 只检测出粉红
        self.litmus_pink_info_lit = []

    def init_litmus_pink_top(self):
        self.litmus_pink_top_secs = 0
        self.litmus_pink_n_top = 0
        self.LITMUS_PINK_N_TOP_THRE = 10
        self.litmus_pink_top_info = []
        self.litmus_only_pink_top_info = []

    def init_separate_liquid_solid(self):  # 初始化固体液体分开
        self.seprate_liquid_info = []
        self.interlude_flag = False  # 倒固体和液体间歇标志
        self.seprate_solid_info = []

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
            self.center_operation_area_front = (
                    np.array(experimental_site_front) * [self.w_front, self.h_front]).astype(np.int32)
            self.init_flag = True

        (hands_top, dusters_top, wild_mouth_bottles_top, wild_stopper_no_upends_top, wild_stopper_upends_top,
         narrow_mouth_bottles_top, narrow_mouth_bottlenecks_top, narrow_stopper_no_upends_top,
         narrow_stopper_upends_top, liquids_top, spoons_top, spoon_us_top, beakers_top, marbles_top,
         alcohol_lamp_flams_top, alcohol_lamps_top, alcohol_lamp_caps_top, alcohol_lamp_cap_falses_top,
         tubes_top, tube_mouths_top, tube_stands_top, tweezers_top, short_gas_pipes_top, long_gas_pipes_top,
         rubber_hoses_top, rubber_stoppers_top, gas_bottles_top, gas_bottle_mouths_top,
         frosted_glass_plates_top, wood_burnings_top, wood_extinguishs_top, purple_liquids_top,
         pink_liquids_top, matchboxs_top, liquid_wastes_top, pipe_joints_top, pipe_ends_top, pipe_pipes_top,
         conical_flasks_top, conical_flask_mouths_top, long_neck_funnels_top, long_neck_funnel_us_top,
         gas_reactions_top, solid_wastes_top) = self.preds_top
        if not self.judget_g:
            min_y = self.h_top
            for items in self.preds_top:
                for item in items:
                    if item[1] < min_y:
                        min_y = item[1]
            if min_y > self.h_top * 0.14 and min_y != self.h_top:  # 一代
                self.center_area_top = (np.array(experimental_site_top) * [self.w_top, self.h_top]).astype(np.int32)
            self.judget_g = True

        """
        ['手', '抹布', '广口瓶', '广口瓶瓶塞倒放', '广口瓶瓶塞未倒放',
        '细口瓶', '细口瓶口', '细口瓶瓶塞未倒放', 
        '细口瓶瓶塞倒放', '液体', '药匙', '药匙勺', '烧杯', '大理石'
        '火焰', '酒精灯', '酒精灯帽', '酒精灯帽摆放错',
        '试管', '试管口', '试管架', '镊子', '直角短管', '直角长管', 
        '橡胶管', '橡皮塞', '集气瓶', '集气瓶口', 
        '毛玻璃片', '木条燃烧', '木条熄灭', '紫色液体', 
        '粉色液体', '火柴盒', '废液', '导管接头', '导管端头', '导管_导管',
        '锥形瓶', '锥形瓶口', '长颈漏斗', '长颈漏斗U', 
        '反应', '废料']
        """
        (hands_front, dusters_front, wild_mouth_bottles_front, wild_stopper_no_upends_front, wild_stopper_upends_front,
         narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, narrow_stopper_no_upends_front,
         narrow_stopper_upends_front, liquids_front, spoons_front, spoon_us_front, beakers_front, marbles_front,
         alcohol_lamp_flams_front, alcohol_lamps_front, alcohol_lamp_caps_front, alcohol_lamp_cap_falses_front,
         tubes_front, tube_mouths_front, tube_stands_front, tweezers_front, short_gas_pipes_front, long_gas_pipes_front,
         rubber_hoses_front, rubber_stoppers_front, gas_bottles_front, gas_bottle_mouths_front,
         frosted_glass_plates_front, wood_burnings_front, wood_extinguishs_front, purple_liquids_front,
         pink_liquids_front, matchboxs_front, liquid_wastes_front, pipe_joints_front, pipe_ends_front, pipe_pipes_front,
         conical_flasks_front, conical_flask_mouths_front, long_neck_funnels_front, long_neck_funnel_us_front,
         gas_reactions_front, solid_wastes_front) = self.preds_front

        self.last_frame_info = [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]
        if gas_reactions_front.shape[0] > 0:
            self.last_reaction_secs = self.secs

        # 1. 能正确选用镊子或药匙取用固体药品
        if not self.scorePoint1:
            info = self.tweezer_marble(hands_front, tweezers_front, spoons_front, wild_mouth_bottles_front,
                                       marbles_front, conical_flask_mouths_front,
                                       hands_top, tweezers_top, spoons_top, wild_mouth_bottles_top,
                                       marbles_top, conical_flask_mouths_top)
            if info is not None:
                self.assignScore(1, *info[:5])

        if not self.scorePoint2:  # 能正确组装制取CO2的发生和收集装置
            info = self.correct_assemble_exp_facility_z(conical_flasks_front, conical_flask_mouths_front,
                                                        rubber_stoppers_front, long_neck_funnel_us_front,
                                                        gas_bottles_front, long_gas_pipes_front,
                                                        pipe_ends_front, pipe_pipes_front, frosted_glass_plates_front,
                                                        conical_flasks_top, rubber_stoppers_top,
                                                        long_neck_funnel_us_top, pipe_joints_top,
                                                        gas_bottles_top, frosted_glass_plates_top,
                                                        long_gas_pipes_top)
            if info is not None:
                self.assignScore(2, *info[:5])

        if not self.scorePoint3:  # 能正确选用稀盐酸
            info = self.select_HCl_z(narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front,
                                     long_neck_funnel_us_front, conical_flasks_front, conical_flask_mouths_front,
                                     gas_reactions_front)
            if info is not None:
                self.assignScore(3, *info[:5])

        if not self.scorePoint4:  # 能从长颈漏斗口加入稀盐酸，直到没过长颈漏斗下端管口（液封）
            info = self.correct_add_HCl_z(narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front,
                                          long_neck_funnel_us_front, conical_flasks_front, conical_flask_mouths_front,
                                          gas_reactions_front, rubber_stoppers_front, narrow_mouth_bottles_top,
                                          narrow_mouth_bottlenecks_top, long_neck_funnel_us_top, hands_top)
            if info is not None:
                if self.scorePoint3:
                    self.retracementScore(3)
                self.assignScore(3, *info[:5])
                self.assignScore(4, *info[:5])

        if not self.scorePoint5:  # 能将燃着的木条放在集气瓶口验满并记录
            if not self.check_gas_fill_flag:  # 燃烧的木条验满
                self.check_gas_fill(wood_burnings_front, gas_bottles_front, gas_bottle_mouths_front,
                                    frosted_glass_plates_front, wood_burnings_top, gas_bottles_top,
                                    frosted_glass_plates_top)
            if not self.gas_fill_flag:
                self.gas_fill(wood_extinguishs_front, gas_bottles_front, gas_bottle_mouths_front, wood_burnings_front,
                              frosted_glass_plates_front,
                              wood_extinguishs_top, gas_bottles_top, wood_burnings_top, frosted_glass_plates_top)
            if self.check_gas_fill_info:  # 木条燃烧 验满操作
                if self.gas_fill_info and self.check_gas_fill_info[-1] < self.gas_fill_info[-1]:
                    img1 = self.crop_frame(self.check_gas_fill_info[-2], self.check_gas_fill_info[0],
                                           self.check_gas_fill_info[3])
                    img2 = self.crop_frame(self.gas_fill_info[-2], self.gas_fill_info[0], self.gas_fill_info[3])
                    img = np.hstack([img1, img2])
                    self.assignScore(5, img, self.check_gas_fill_info[1], self.check_gas_fill_info[2], None,
                                     self.check_gas_fill_info[4])
                elif self.gas_fill_info_default and self.check_gas_fill_info[-1] < self.gas_fill_info_default[-1]:  # 默认
                    img1 = self.crop_frame(self.check_gas_fill_info[-2], self.check_gas_fill_info[0],
                                           self.check_gas_fill_info[3])
                    img2 = self.crop_frame(self.gas_fill_info_default[-2], self.gas_fill_info_default[0],
                                           self.gas_fill_info_default[3])
                    img = np.hstack([img1, img2])
                    self.assignScore(5, img, self.check_gas_fill_info[1], self.check_gas_fill_info[2], None,
                                     self.check_gas_fill_info[4])
                elif self.secs - self.check_gas_fill_info[-1] > 10:
                    self.assignScore(5, *self.check_gas_fill_info[:5])

        if not self.scorePoint6:  # 能用灯帽盖灭酒精灯
            info = self.extinguish_alcohol_lamp(hands_front, alcohol_lamp_flams_front, alcohol_lamps_front,
                                                alcohol_lamp_caps_front,
                                                hands_top, alcohol_lamp_flams_top, alcohol_lamps_top,
                                                alcohol_lamp_caps_top)
            if info is not None:
                self.assignScore(6, *info[:5])

        if not self.scorePoint7:  # 能观察紫色石蕊溶液的颜色变化并记录
            info = self.litmus_color_change(tubes_front, pipe_pipes_front, purple_liquids_front, pink_liquids_front,
                                            tubes_top, purple_liquids_top, pink_liquids_top)
            if info:
                self.assignScore(7, *info[:5])
        if (self.scorePoint7
                and purple_liquids_front.shape[0] + pink_liquids_front.shape[0] > 0
                and self.secs - self.litmus_color_change_secs > 45):
            if not self.litmus_color_change_check:
                self.init_litmus_color_change()
                self.litmus_color_change_check = True
            info = self.litmus_color_change(tubes_front, pipe_pipes_front, purple_liquids_front, pink_liquids_front,
                                            tubes_top, purple_liquids_top, pink_liquids_top)
            if info:
                self.retracementScore(7)
                self.assignScore(7, *info[:5])

        if not self.scorePoint8:  # 实验结束，能将固体和液体分开回收
            info = self.separate_liquid_solid(conical_flasks_front, conical_flask_mouths_front, liquid_wastes_front,
                                              beakers_front, marbles_front,
                                              conical_flasks_top, conical_flask_mouths_top, liquid_wastes_top,
                                              marbles_top, beakers_top)
            if info:
                self.assignScore(8, *info[:5])

        items_top = [wild_mouth_bottles_top,
                     narrow_mouth_bottles_top,
                     beakers_top,
                     alcohol_lamps_top,
                     tubes_top,
                     gas_bottles_top,
                     conical_flasks_top, long_neck_funnel_us_top,
                     ]
        """
            ['广口瓶'
            '细口瓶'
            '烧杯'
            '酒精灯', 
            '试管',
            '集气瓶'
            '锥形瓶', '长颈漏斗U', 
            ]
        """
        items_front = [wild_mouth_bottles_front,
                       narrow_mouth_bottles_front,
                       beakers_front,
                       alcohol_lamps_front,
                       gas_bottles_front,
                       conical_flasks_front, long_neck_funnel_us_front,
                       ]

        if (not self.scorePoint9 and len(self.score_list) > 2):  # 药品归位、清洗仪器、整理实验台
            info = self.clearn_desk(["top", "front"], [items_top, items_front],
                                    [self.center_area_top, self.center_operation_area_front])
            if info:
                self.assignScore(9, *info[:5])
                self.assignScore(10, *info[:5])
                if not self.scorePoint8:
                    if self.seprate_liquid_info:
                        self.assignScore(8, *self.seprate_liquid_info[:5])
                    elif self.secs - self.last_reaction_secs > 0.2:
                        self.assignScore(8, *self.last_frame_info[:5])

        if self.scorePoint9 and len(self.score_list) < 8:
            if not self.desk_is_clearn(["top", "front"], [items_top, items_front],
                                       [self.center_area_top, self.center_operation_area_front]):
                self.retracementScore(9)

    def hold_tube(self, tubes_front, rubber_stoppers_front, short_gas_pipes_front, hand_front_box):
        if tubes_front.shape[0] != 0:  # 前视检测到试管
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                if iou(hand_front_box, tube_front_box) > 0:
                    return True
        if rubber_stoppers_front.shape[0] == 1:  # 试管没检测到 检测到橡皮塞
            rubber_stopper_front_box = rubber_stoppers_front[0][:4]
            if min_dis_boxes(rubber_stopper_front_box, hand_front_box) < self.h_front * 0.045:
                return True
        elif (rubber_stoppers_front.shape[0] == 0
              and short_gas_pipes_front.shape[0] == 1):  # 试管橡皮塞都没检测到，只检测到短直角导管
            short_gas_pipe_front_box = short_gas_pipes_front[0][:4]
            if min_dis_boxes(short_gas_pipe_front_box, hand_front_box) < self.h_front * 0.03:
                return True

    def check_gas_tightness(self, score_index, hands_front, beakers_front, liquids_front, long_gas_pipes_front,
                            short_gas_pipes_front, tubes_front, rubber_stoppers_front, hands_top, rubber_stoppers_top):
        """
        检验气密性：(导管伸入水中，用手捂住试管)
        :param score_index: 得分点索引
        :param hands_front: 前视手
        :param beakers_front: 前视烧杯
        :param liquids_front: 前视液体
        :param long_gas_pipes_front: 前视长直角导管
        :param short_gas_pipes_front: 前视短直角导管
        :param tubes_front: 前视试管
        :param rubber_stoppers_front: 前视橡皮塞
        :param hands_top: # 顶视手
        :param rubber_stoppers_top: 顶视橡皮塞
        :return:
        """
        hold_tube_1 = False  # 一只手握住试管
        hold_tube_2 = False  # 两只手握住试管
        if not self.tube_rubber_stopper and tubes_front.shape[0] > 0 and rubber_stoppers_front.shape[0] > 0:
            rubber_stopper_front_box = rubber_stoppers_front[0][:4]
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                if iou(tube_front_box, rubber_stopper_front_box) > 0:
                    self.tube_rubber_stopper = True
        long_gas_pipe_in_water = False  # 直角长导气管伸入水中
        if (long_gas_pipes_front.shape[0] == 1
                and beakers_front.shape[0] != 0
                and liquids_front.shape[0] != 0):
            long_gas_pipe_front_box = long_gas_pipes_front[0][:4]  # 长直角导管
            for liquid_front in liquids_front:
                liquid_front_box = liquid_front[:4]
                if iou(long_gas_pipe_front_box, liquid_front_box) > 0:
                    for beaker_front in beakers_front:
                        beaker_front_box = beaker_front[:4]
                        if iou(beaker_front_box, liquid_front_box) > box_area(liquid_front_box) * 0.6:
                            long_gas_pipe_in_water = True
                            break
                if long_gas_pipe_in_water:
                    break
        if self.tube_rubber_stopper and long_gas_pipe_in_water:
            hand_front_box_list = []
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if pt_in_polygon(center_point(hand_front_box), self.center_area_front):
                    hand_front_box_list.append(deepcopy(hand_front_box))
            if len(hand_front_box_list) == 1:
                if self.hold_tube(tubes_front, rubber_stoppers_front, short_gas_pipes_front, hand_front_box_list[0]):
                    hold_tube_2 = True
            elif len(hand_front_box_list) == 2:
                if (iou(hand_front_box_list[0], hand_front_box_list[1]) > 0
                        and (self.hold_tube(tubes_front, rubber_stoppers_front, short_gas_pipes_front,
                                            hand_front_box_list[0])
                             or self.hold_tube(tubes_front, rubber_stoppers_front, short_gas_pipes_front,
                                               hand_front_box_list[1]))):
                    hold_tube_2 = True
                else:
                    for hand_front_box in hand_front_box_list:
                        if self.hold_tube(tubes_front, rubber_stoppers_front, short_gas_pipes_front, hand_front_box):
                            hold_tube_1 = True
            else:
                for hand_front_box in hand_front_box_list:
                    if self.hold_tube(tubes_front, rubber_stoppers_front, short_gas_pipes_front, hand_front_box):
                        hold_tube_1 = True
        if (not hold_tube_1
                and not hold_tube_2
                and self.tube_rubber_stopper
                and long_gas_pipe_in_water
                and rubber_stoppers_top.shape[0] == 1
                and hands_top.shape[0] > 0):
            rubber_stopper_top_box = rubber_stoppers_top[0][:4]
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if min_dis_boxes(rubber_stopper_top_box, hand_top_box) < self.h_top * 0.045:
                    hold_tube_1 = True
                    break
        if hold_tube_1:
            self.update_info_list(score_index, self.hold_tube_info_1)
            if self.hold_tube_info_2:
                self.hold_tube_info_2[-1][-1] = self.secs
        if hold_tube_2:
            self.update_info_list(score_index, self.hold_tube_info_2)

        if self.hold_tube_info_2:
            if self.secs - self.hold_tube_info_2[-1][-1] > 2.0:
                if len(self.hold_tube_info_2) == 1:
                    return self.hold_tube_info_2[0][:6]
                else:
                    return self.hold_tube_info_2[1][:6]
        elif self.hold_tube_info_1 and self.secs - self.hold_tube_info_1[-1][-1] > 2.0:
            if len(self.hold_tube_info_1) == 1:
                return self.hold_tube_info_1[0][:6]
            else:
                return self.hold_tube_info_1[1][:6]

    @try_decorator
    def tweezer_marble(self, hands_front, tweezers_front, spoons_front, wild_mouth_bottles_front,
                       marbles_front, conical_flask_mouths_front,
                       hands_top, tweezers_top, spoons_top, wild_mouth_bottles_top,
                       marbles_top, conical_flask_mouths_top):
        """
        用镊子/药匙夹取大理石
        :param hands_front: 前视手
        :param tweezers_front: 前视镊子
        :param spoons_front: 前视药匙
        :param wild_mouth_bottles_front: 前视广口瓶
        :param marbles_front: 前视大理石
        :param conical_flask_mouths_front: 前视锥形瓶口
        :param hands_top: 顶视手
        :param tweezers_top: 顶视镊子
        :param spoons_top: 顶视药匙
        :param wild_mouth_bottles_top: 顶视广口瓶
        :param marbles_top: 顶视大理石
        :return:
        """
        record = self.take_marble_tool(hands_front, tweezers_front, wild_mouth_bottles_front,
                                       marbles_front, conical_flask_mouths_front,
                                       hands_top, tweezers_top, wild_mouth_bottles_top,
                                       marbles_top, conical_flask_mouths_top)
        if record is None:
            record = self.take_marble_tool(hands_front, spoons_front, wild_mouth_bottles_front,
                                           marbles_front, conical_flask_mouths_front,
                                           hands_top, spoons_top, wild_mouth_bottles_top,
                                           marbles_top, conical_flask_mouths_top)
        if record:
            if self.tweezer_marble_curr_num < self.tweezer_marble_thre_num:
                self.tweezer_marble_curr_num += 1
            else:
                if record == 'top':
                    tweezer_marble_info = [self.frame_top, self.time_top, self.objects_top,
                                           self.preds_top, self.num_frame_top]
                else:
                    tweezer_marble_info = [self.frame_front, self.time_front, self.objects_front,
                                           self.preds_front, self.num_frame_front]
                return tweezer_marble_info

    def take_marble_tool(self, hands_front, tools_front, wild_mouth_bottles_front,
                         marbles_front, mouths_front,
                         hands_top, tools_top, wild_mouth_bottles_top,
                         marbles_top, mouths_top):
        if tools_front.shape[0] == 1 and hands_front.shape[0] > 0:
            tweezer_front_box = tools_front[0][:4]
            if tweezer_front_box[3] < self.h_front * 0.85:
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if (  # pt_in_polygon(center_point(hand_front_box), self.center_area_front)
                            iou(hand_front_box, tweezer_front_box) > 0):  # 操作区手拿镊子
                        if wild_mouth_bottles_front.shape[0] > 0:
                            wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
                            if (iou(wild_mouth_bottle_front_box, tweezer_front_box) > 0
                                    and center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0):
                                return 'front'
                        if marbles_front.shape[0] > 0:
                            for marble_front in marbles_front:
                                marble_front_box = marble_front[:4]
                                if iou(marble_front_box, tweezer_front_box) > 0:
                                    return 'front'
                        if mouths_front.shape[0] > 0:
                            conical_flask_mouth_front_box = mouths_front[0][:4]
                            if iou(tweezer_front_box, conical_flask_mouth_front_box) > 0:
                                return 'front'
        if tools_top.shape[0] > 0 and hands_top.shape[0] > 0:
            tweezer_top_box = tools_top[0][:4]
            if tweezer_top_box[1] > self.h_front * 0.15:
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, tweezer_top_box) > 0:
                        if wild_mouth_bottles_top.shape[0] > 0:
                            wild_mouth_bottle_top_box = wild_mouth_bottles_top[0][:4]
                            if iou(wild_mouth_bottle_top_box, tweezer_top_box):
                                return 'top'
                        if marbles_top.shape[0] > 0:
                            for marble_top in marbles_top:
                                marble_top_box = marble_top[:4]
                                if iou(marble_top_box, tweezer_top_box) > 0:
                                    return 'top'
                        if mouths_top.shape[0] > 0:
                            conical_flask_mouth_top_box = mouths_top[0][:4]
                            if iou(conical_flask_mouth_top_box, tweezer_top_box) > 0:
                                return 'top'

    @try_decorator
    def correct_assemble_exp_facility_z(self, conical_flasks_front, conical_flask_mouths_front, rubber_stoppers_front,
                                        long_neck_funnel_us_front, gas_bottles_front, long_gas_pipes_front,
                                        pipe_ends_front, pipe_pipes_front, frosted_glass_plates_front,
                                        conical_flasks_top, rubber_stoppers_top, long_neck_funnel_us_top,
                                        pipe_joints_top, gas_bottles_top, frosted_glass_plates_top, long_gas_pipes_top,
                                        frosted_glass=False):
        if self.assemble_exp_facility_z(conical_flasks_front, conical_flask_mouths_front, rubber_stoppers_front,
                                        long_neck_funnel_us_front, gas_bottles_front, long_gas_pipes_front,
                                        pipe_ends_front, pipe_pipes_front, frosted_glass_plates_front, frosted_glass):
            self.assemble_facility_z_secs, self.assemble_facility_z_secs_pre, flag = self.duration(
                self.assemble_facility_z_secs,
                self.assemble_facility_z_duration,
                self.assemble_facility_z_secs_pre,
                self.assemble_facility_z_reclock
            )
            if flag:
                self.assemble_facility_z_info = [self.frame_front, self.time_front, self.objects_front,
                                                 self.preds_front, self.num_frame_front]
                return self.assemble_facility_z_info
        elif self.assemble_exp_facility_z_top(conical_flasks_top, rubber_stoppers_top, long_neck_funnel_us_top,
                                              pipe_joints_top, gas_bottles_top, frosted_glass_plates_top,
                                              long_gas_pipes_top, frosted_glass):
            self.assemble_facility_z_secs, self.assemble_facility_z_secs_pre, flag = self.duration(
                self.assemble_facility_z_secs,
                self.assemble_facility_z_duration,
                self.assemble_facility_z_secs_pre,
                self.assemble_facility_z_reclock
            )
            if flag:
                self.assemble_facility_z_info = [self.frame_top, self.time_top, self.objects_top,
                                                 self.preds_top, self.num_frame_top]
                return self.assemble_facility_z_info

    def assemble_exp_facility_z(self, conical_flasks_front, conical_flask_mouths_front, rubber_stoppers_front,
                                long_neck_funnel_us_front, gas_bottles_front, long_gas_pipes_front,
                                pipe_ends_front, pipe_pipes_front, frosted_glass_plates_front,
                                frosted_glass=False):
        """
        正确组装实验装置(锥形瓶)
        :param conical_flasks_front: 锥形瓶
        :param conical_flask_mouths_front: 锥形瓶口
        :param rubber_stoppers_front: 橡皮塞
        :param long_neck_funnel_us_front: 长颈漏斗U
        :param gas_bottles_front: 集气瓶
        :param long_gas_pipes_front: 长直角导管
        :param pipe_ends_front: 导管端头
        :param pipe_pipes_front: 导管_导管
        :param frosted_glass_plates_front: 毛玻璃片
        :return:
        """
        if frosted_glass and frosted_glass_plates_front.shape[0] == 0:
            return
        if (  # conical_flasks_front.shape[0] == 1
                conical_flask_mouths_front.shape[0] == 1
                and rubber_stoppers_front.shape[0] > 0
                and long_neck_funnel_us_front.shape[0] == 1):
            # conical_flask_front_box = conical_flasks_front[0][:4]  # 锥形瓶
            conical_flask_mouth_front_box = conical_flask_mouths_front[0][:4]  # 锥形瓶口
            long_neck_funnel_u_top_box = long_neck_funnel_us_front[0][:4]  # 长颈漏斗U
            rubber_stopper_in_flask_mouth = False
            for rubber_stopper_front in rubber_stoppers_front:
                rubber_stopper_front_box = rubber_stopper_front[:4]
                if (  # center_distance_h(conical_flask_front_box, rubber_stopper_front_box, True) < width(
                        # rubber_stopper_front_box)
                        iou(conical_flask_mouth_front_box, rubber_stopper_front_box) > 0
                        and center_distance_v(conical_flask_mouth_front_box, rubber_stopper_front_box) > 0
                        and center_distance_v(rubber_stopper_front_box, long_neck_funnel_u_top_box) > 0):
                    rubber_stopper_in_flask_mouth = True
                    break
            if rubber_stopper_in_flask_mouth and gas_bottles_front.shape[0] > 0:
                gas_bottle_front_box = gas_bottles_front[0][:4]
                if frosted_glass:
                    frosted_glass_plate_front_box = frosted_glass_plates_front[0][:4]
                    if (center_distance_v(gas_bottle_front_box, frosted_glass_plate_front_box) > 0
                            and center_distance_h(gas_bottle_front_box, frosted_glass_plate_front_box, True) < width(
                                gas_bottle_front_box)):
                        pass
                    else:
                        return
                if pipe_pipes_front.shape[0] == 1:
                    pipe_pipe_front_box = pipe_pipes_front[0][:4]
                    if (iou(gas_bottle_front_box, pipe_pipe_front_box) > 0
                            and center_distance_v(gas_bottle_front_box, pipe_pipe_front_box) > 0):
                        return True
                if long_gas_pipes_front.shape[0] == 1:
                    long_gas_pipe_front_box = long_gas_pipes_front[0][:4]
                    if (iou(gas_bottle_front_box, long_gas_pipe_front_box) > 0
                            and center_distance_v(gas_bottle_front_box, long_gas_pipe_front_box) > 0):
                        return True
                if pipe_ends_front.shape[0] > 0:
                    for pipe_end_front in pipe_ends_front:
                        pipe_end_front_box = pipe_end_front[:4]
                        if iou(gas_bottle_front_box, pipe_end_front_box) > box_area(pipe_end_front_box) * 0.6:
                            return True

    @try_decorator
    def assemble_exp_facility_z_top(self, conical_flasks_top, rubber_stoppers_top, long_neck_funnel_us_top,
                                    pipe_joints_top, gas_bottles_top, frosted_glass_plates_top, long_gas_pipes_top,
                                    frosted_glass):
        """

        :param conical_flasks_top: 顶视锥形瓶
        :param rubber_stoppers_top: 顶视橡皮塞
        :param long_neck_funnel_us_top: 顶视长颈漏斗U
        :param pipe_joints_top: 顶视导管接头
        :param gas_bottles_top: 顶视集气瓶
        :param frosted_glass_plates_top: 顶视毛玻璃片
        :param frosted_glass: 是否考虑毛玻璃片
        :return:
        """
        if (conical_flasks_top.shape[0] == 1
                and rubber_stoppers_top.shape[0] == 1
                and long_neck_funnel_us_top.shape[0] == 1):
            conical_flask_top_box = conical_flasks_top[0][:4]
            rubber_stopper_top_box = rubber_stoppers_top[0][:4]
            long_neck_funnel_u_top_box = long_neck_funnel_us_top[0][:4]
            if (iou(conical_flask_top_box, rubber_stopper_top_box) > 0
                    and min_dis_boxes(rubber_stopper_top_box, long_neck_funnel_u_top_box) < self.h_top * 0.1):
                if long_gas_pipes_top.shape[0] > 0:
                    long_gas_pipe_top_box = long_gas_pipes_top[0][:4]
                    if gas_bottles_top.shape[0] > 0:
                        gas_bottle_top_box = gas_bottles_top[0][:4]
                        if iou(long_gas_pipe_top_box, gas_bottle_top_box) > 0:
                            return True
                    elif frosted_glass_plates_top.shape[0] > 0:
                        frosted_glass_plate_top_box = frosted_glass_plates_top[0][:4]
                        if iou(long_gas_pipe_top_box, frosted_glass_plate_top_box) > 0:
                            return True
                elif pipe_joints_top.shape[0] > 0:
                    for pipe_joint_top in pipe_joints_top:
                        pipe_joint_top_box = pipe_joint_top[:4]
                        if gas_bottles_top.shape[0] > 0:
                            gas_bottle_top_box = gas_bottles_top[0][:4]
                            if min_dis_boxes(pipe_joint_top_box, gas_bottle_top_box) < self.h_top * 0.1:
                                return True
                        elif frosted_glass_plates_top.shape[0] > 0:
                            frosted_glass_plate_top_box = frosted_glass_plates_top[0][:4]
                            if min_dis_boxes(pipe_joint_top_box, frosted_glass_plate_top_box) < self.h_top * 0.1:
                                return True

    @try_decorator
    def select_HCl_z(self, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, long_neck_funnel_us_front,
                     conical_flasks_front, conical_flask_mouths_front, gas_reactions_front):
        """
        选用稀盐酸
        :param narrow_mouth_bottles_front: 前视细口瓶
        :param narrow_mouth_bottlenecks_front: 前视细口瓶口
        :param long_neck_funnel_us_front: 前视长颈漏斗U
        :param conical_flasks_front: 前视锥形瓶
        :param conical_flask_mouths_front: 前视锥形瓶口
        :param gas_reactions_front: 前视气体反应
        :return:
        """
        object_box = self.select_HCl_z_(narrow_mouth_bottlenecks_front, long_neck_funnel_us_front, conical_flasks_front,
                                        conical_flask_mouths_front)
        if object_box is None:
            object_box = self.select_HCl_z_(narrow_mouth_bottles_front, long_neck_funnel_us_front, conical_flasks_front,
                                            conical_flask_mouths_front)
        if object_box is not None:
            self.select_HCl_z_secs, self.select_HCl_z_secs_pre, flag = self.duration(
                self.select_HCl_z_secs,
                1.5,
                self.select_HCl_z_secs_pre,
                1
            )
            if flag:
                self.select_HCl_z_info = [self.frame_front, self.time_front, self.objects_front,
                                          self.preds_front, self.num_frame_front, object_box, self.secs]
                # return self.select_HCl_z_info

        # if not self.select_HCl_z_info and narrow_mouth_bottles_front.shape[0] > 0 and conical_flasks_front.shape[
        #     0] == 1:
        #     conical_flask_front_box = conical_flasks_front[0][:4]
        #     if narrow_mouth_bottles_front.shape[0] > 0:
        #         for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
        #             narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
        #             if (iou(narrow_mouth_bottle_front_box, conical_flask_front_box) > 0
        #                     and center_distance_v(conical_flask_front_box, narrow_mouth_bottle_front_box) > 0):
        #                 object_box = combineBox(conical_flask_front_box, narrow_mouth_bottle_front_box)
        #                 record = True
        #                 self.select_HCl_z_info = [self.frame_front, self.time_front, self.objects_front,
        #                                           self.preds_front, self.num_frame_front, object_box, self.secs]
        #                 break
        #             elif not record and long_neck_funnel_us_front.shape[0] == 1:
        #                 long_neck_funnel_u_front_box = long_neck_funnel_us_front[0][:4]
        #                 if (long_neck_funnel_u_front_box[3] > conical_flask_front_box[1] and
        #                         iou(narrow_mouth_bottle_front_box, long_neck_funnel_u_front_box) > 0):
        #                     object_box = combineBox(conical_flask_front_box, narrow_mouth_bottle_front_box,
        #                                             long_neck_funnel_u_front_box)
        #                     self.select_HCl_z_info = [self.frame_front, self.time_front, self.objects_front,
        #                                               self.preds_front, self.num_frame_front, object_box, self.secs]
        #                     break

        if self.select_HCl_z_info and gas_reactions_front.shape[0] > 0 and conical_flasks_front.shape[0] == 1:
            gas_reaction_front_box = gas_reactions_front[0][:4]
            conical_flask_front_box = conical_flasks_front[0][:4]
            if iou(gas_reaction_front_box, conical_flask_front_box) > box_area(gas_reaction_front_box) * 0.5:
                # if not self.check_select_HCl_z_info and (
                #         not self.select_HCl_z_info or self.secs - self.select_HCl_z_info[-1] > 5):
                #     object_box = combineBox(gas_reaction_front_box, conical_flask_front_box)
                #     self.select_HCl_z_info = [self.frame_front, self.time_front, self.objects_front,
                #                               self.preds_front, self.num_frame_front, object_box, self.secs]
                #     self.check_select_HCl_z_info = True
                self.reaction_z_secs, self.reaction_z_secs_pre, flag = self.duration(
                    self.reaction_z_secs,
                    1.5,
                    self.reaction_z_secs_pre,
                    1
                )
                if flag:
                    object_box = combineBox(conical_flask_front_box, gas_reaction_front_box)
                    self.reastion_z_info = [self.frame_front, self.time_front, self.objects_front,
                                            self.preds_front, self.num_frame_front, object_box, self.secs]
                    img1 = self.crop_frame(self.select_HCl_z_info[-2], self.select_HCl_z_info[0],
                                           self.select_HCl_z_info[3])
                    img2 = self.crop_frame(self.reastion_z_info[-2], self.reastion_z_info[0], self.reastion_z_info[3])
                    img = np.hstack([img1, img2])
                    return [img, self.select_HCl_z_info[1], self.select_HCl_z_info[2], None, self.select_HCl_z_info[4]]

    def select_HCl_z_(self, containers_front, long_neck_funnel_us_front, conical_flasks_front,
                      conical_flask_mouths_front):
        """

        :param containers_front: 容器
        :param long_neck_funnel_us_front: 长颈漏斗
        :param conical_flasks_front: 锥形瓶
        :param conical_flask_mouths_front: 锥形瓶口
        :return:
        """
        if containers_front.shape[0] > 0:
            if conical_flasks_front.shape[0] == 1:
                conical_flask_front_box = conical_flasks_front[0][:4]
                for container_front in containers_front:
                    container_front_box = container_front[:4]
                    if (iou(container_front_box, conical_flask_front_box) > 0
                            and center_distance_v(conical_flask_front_box, container_front_box) > 0):
                        object_box = combineBox(conical_flask_front_box, container_front_box)
                        return object_box
                    elif long_neck_funnel_us_front.shape[0] == 1:
                        long_neck_funnel_u_front_box = long_neck_funnel_us_front[0][:4]
                        if (long_neck_funnel_u_front_box[3] < conical_flask_front_box[1]
                                and iou(container_front_box, long_neck_funnel_u_front_box) > 0):
                            object_box = combineBox(conical_flask_front_box, container_front_box,
                                                    long_neck_funnel_u_front_box)
                            return object_box
            elif conical_flask_mouths_front.shape[0] == 1:
                conical_flask_mouth_front_box = conical_flask_mouths_front[0][:4]
                for container_front in containers_front:
                    container_front_box = container_front[:4]
                    if (iou(container_front_box, conical_flask_mouth_front_box) > 0):
                        object_box = combineBox(conical_flask_mouth_front_box, container_front_box)
                        return object_box
                    elif long_neck_funnel_us_front.shape[0] == 1:
                        long_neck_funnel_u_front_box = long_neck_funnel_us_front[0][:4]
                        if (long_neck_funnel_u_front_box[3] < conical_flask_mouth_front_box[1]
                                and iou(container_front_box, long_neck_funnel_u_front_box) > 0):
                            object_box = combineBox(conical_flask_mouth_front_box, container_front_box,
                                                    long_neck_funnel_u_front_box)
                            return object_box

    @try_decorator
    def correct_add_HCl_z(self, narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, long_neck_funnel_us_front,
                          conical_flasks_front, conical_flask_mouths_front, gas_reactions_front, rubber_stoppers_front,
                          narrow_mouth_bottles_top, narrow_mouth_bottlenecks_top, long_neck_funnel_us_top, hands_top):
        """
        从锥形瓶口加入稀盐酸
        :param narrow_mouth_bottles_front: 前视细口瓶
        :param narrow_mouth_bottlenecks_front: 前视细口瓶口
        :param long_neck_funnel_us_front: 前视长颈漏斗U
        :param conical_flasks_front: 前视锥形瓶
        :param conical_flask_mouths_front: 前视锥形瓶口
        :param rubber_stoppers_front: 前视橡皮塞
        :param gas_reactions_front: 前视锥形瓶中气体反应
        :param narrow_mouth_bottles_top: 顶视细口瓶
        :param narrow_mouth_bottlenecks_top: 顶视细口瓶口
        :param long_neck_funnel_us_top: 顶视长颈漏斗U
        :param hands_top: 顶视手
        :return:
        """

        record, object_box = '', None
        if long_neck_funnel_us_front.shape[0] == 1:  # 前视角
            long_neck_funnel_u_front_box = long_neck_funnel_us_front[0][:4]
            isgo = False
            conical_flask_front_box = None
            if conical_flasks_front.shape[0] == 1:
                conical_flask_front_box = conical_flasks_front[0][:4]
                if long_neck_funnel_u_front_box[3] < conical_flask_front_box[1]:
                    isgo = True
            elif conical_flask_mouths_front.shape[0] == 1:
                conical_flask_front_box = conical_flask_mouths_front[0][:4]
                if long_neck_funnel_u_front_box[3] < conical_flask_front_box[1]:
                    isgo = True
            if isgo and narrow_mouth_bottles_front.shape[0] > 0:
                for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
                    narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
                    if iou(narrow_mouth_bottle_front_box, long_neck_funnel_u_front_box) > 0:
                        object_box = combineBox(conical_flask_front_box, narrow_mouth_bottle_front_box,
                                                long_neck_funnel_u_front_box)
                        record = "front"
                        break
            if (isgo and not record and narrow_mouth_bottlenecks_front.shape[0] > 0):
                for narrow_mouth_bottleneck_front in narrow_mouth_bottlenecks_front:
                    narrow_mouth_bottleneck_front_box = narrow_mouth_bottleneck_front[:4]
                    if iou(narrow_mouth_bottleneck_front_box, long_neck_funnel_u_front_box) > 0:
                        object_box = combineBox(conical_flask_front_box, narrow_mouth_bottleneck_front_box,
                                                long_neck_funnel_u_front_box)
                        record = "front"
                        break
        if (not record and long_neck_funnel_us_top.shape[0] > 0 and hands_top.shape[0] > 0):
            if narrow_mouth_bottlenecks_top.shape[0] > 0:
                for long_neck_funnel_u_top in long_neck_funnel_us_top:
                    long_neck_funnel_u_top_box = long_neck_funnel_u_top[:4]
                    for narrow_mouth_bottleneck_top in narrow_mouth_bottlenecks_top:
                        narrow_mouth_bottleneck_top_box = narrow_mouth_bottleneck_top[:4]
                        if iou(narrow_mouth_bottleneck_top_box, long_neck_funnel_u_top_box) > 0:
                            for hand_top in hands_top:
                                hand_top_box = hand_top[:4]
                                if min_dis_boxes(hand_top_box, narrow_mouth_bottleneck_top_box) < self.h_top * 0.05:
                                    object_box = combineBox(narrow_mouth_bottleneck_top, long_neck_funnel_u_top_box)
                                    record = "top"
                                    break
                        if record:
                            break
                    if not record and narrow_mouth_bottles_top.shape[0] > 0:
                        for narrow_mouth_bottle_top in narrow_mouth_bottles_top:
                            narrow_mouth_bottle_top_box = narrow_mouth_bottle_top[:4]
                            if iou(narrow_mouth_bottle_top_box, long_neck_funnel_u_top_box) > 0:
                                for hand_top in hands_top:
                                    hand_top_box = hand_top[:4]
                                    if iou(hand_top_box, narrow_mouth_bottle_top_box) > 0:
                                        object_box = combineBox(long_neck_funnel_u_top_box, narrow_mouth_bottle_top)
                                        record = "top"
                                        break
                            if record:
                                break
        if record:
            self.add_hcl_z_secs, self.add_hcl_z_secs_pre, flag = self.duration(self.add_hcl_z_secs, 1.5,
                                                                               self.add_hcl_z_secs_pre, 1)
            if flag:
                if record == "front":
                    info = [self.frame_front, self.time_front, self.objects_front,
                            self.preds_front, self.num_frame_front, object_box, self.secs]
                    self.add_hcl_z_infos = self.update_info_list_(self.add_hcl_z_infos, info)
                elif record == "top":
                    info = [self.frame_top, self.time_top, self.objects_top,
                            self.preds_top, self.num_frame_top, object_box, self.secs]
                    self.add_hcl_z_infos = self.update_info_list_(self.add_hcl_z_infos, info)

        if (self.add_hcl_z_infos
                and not self.gas_reaction_z_flag
                and gas_reactions_front.shape[0] == 1
                and conical_flasks_front.shape[0] == 1):
            gas_reaction_front_box = gas_reactions_front[0][:4]
            conical_flask_front_box = conical_flasks_front[0][:4]
            if iou(gas_reaction_front_box, conical_flask_front_box) > box_area(gas_reaction_front_box) * 0.5:
                self.gas_reaction_z_secs, self.gas_reaction_z_secs_pre, flag = self.duration(
                    self.gas_reaction_z_secs,
                    4,
                    self.gas_reaction_z_secs_pre,
                    1
                )
                if flag:
                    self.gas_reaction_z_flag = True
        if self.gas_reaction_z_flag and gas_reactions_front.shape[0] == 1 and conical_flasks_front.shape[
            0] == 1:  # 有气体反应
            gas_reaction_front_box = gas_reactions_front[0][:4]
            conical_flask_front_box = conical_flasks_front[0][:4]
            record = False
            if narrow_mouth_bottles_front.shape[0] == 0:
                record = True
            elif narrow_mouth_bottles_front.shape[0] > 0 and rubber_stoppers_front.shape[0] == 1:
                rubber_stopper_front_box = rubber_stoppers_front[0][:4]
                bottle_under_stoppers = True
                for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
                    narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
                    if center_distance_v(rubber_stopper_front_box, narrow_mouth_bottle_front_box) > 0:
                        bottle_under_stoppers = False
                        break
                if bottle_under_stoppers:
                    record = True
            if record:
                self.add_hcl_done_z_secs, self.add_hcl_done_z_secs_pre, flag = self.duration(
                    self.add_hcl_done_z_secs,
                    2,
                    self.add_hcl_done_z_secs_pre,
                    1
                )
                if flag:
                    object_box = combineBox(gas_reaction_front_box, conical_flask_front_box)
                    self.add_hcl_done_z_info = [self.frame_front, self.time_front, self.objects_front,
                                                self.preds_front, self.num_frame_front, object_box, self.secs]
        if len(self.add_hcl_z_infos) > 0 and self.add_hcl_done_z_info:
            info = self.add_hcl_z_infos[0] if len(self.add_hcl_z_infos) == 1 else self.add_hcl_z_infos[1]
            img1 = self.crop_frame(info[-2], info[0], info[3])
            img2 = self.crop_frame(self.add_hcl_done_z_info[-2], self.add_hcl_done_z_info[0],
                                   self.add_hcl_done_z_info[3])
            img = np.hstack([img1, img2])
            return [img, info[1], info[2], None, info[4]]

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

    def tube_slow_up(self, score_index, hands_front, tubes_front, tweezers_front, marbles_front):  # 试管水平
        """
        试管平放加入大理石，缓慢竖起
        :param score_index: 得分点索引
        :param hands_front: 前视手
        :param tubes_front: 前视试管
        :param tweezers_front: 前视镊子
        :param marbles_front: 前视大理石
        :return:
        """
        if hands_front.shape[0] > 1 and tubes_front.shape[0] > 0:
            record_tube_h = False
            hand_tweezer = False  # 手拿镊子
            hand_tube = False  # 手拿试管
            tube_front_box_ = None
            w_h_r = 0  # 试管宽高比
            if tweezers_front.shape[0] == 1:  # 镊子
                tweezer_front_box = tweezers_front[0][:4]
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if not hand_tweezer and iou(hand_front_box, tweezer_front_box) > 0:  # 手拿镊子
                        hand_tweezer = True
                        continue
                    if not hand_tube:
                        for tube_front in tubes_front:
                            tube_front_box = tube_front[:4]
                            if iou(tube_front_box, hand_front_box) > 0 and iou(tube_front_box, tweezer_front_box) > 0:
                                tube_front_box_ = deepcopy(tube_front_box)
                                hand_tube = True
                                w_h_r = w_h_ratio(tube_front_box_)
                                continue
            if w_h_r > self.TUBE_H_THRE and width(tube_front_box_) > self.h_front * 0.185:
                if hand_tweezer:
                    record_tube_h = True
                elif marbles_front.shape[0] > 0:
                    marble_front_box = marbles_front[0][:4]
                    if iou(marble_front_box, tube_front_box_) > box_area(marble_front_box) * 0.5:
                        record_tube_h = True
                if record_tube_h:
                    if not self.tube_h_info or w_h_r > self.tube_h_info[-2]:
                        self.tube_h_info = [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                            self.num_frame_front, tube_front_box_, w_h_r, self.secs]
                    else:
                        self.tube_h_info[-1] = self.secs
            elif self.tube_h_info and w_h_r == 0:
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if not hand_tube:
                        for tube_front in tubes_front:
                            tube_front_box = tube_front[:4]
                            if iou(tube_front_box, hand_front_box) > box_area(tube_front_box) * 0.3:
                                tube_front_box_ = deepcopy(tube_front_box)
                                w_h_r = w_h_ratio(tube_front_box_)
                                hand_tube = True
                                break
                if (hand_tube
                        and 0 < w_h_r < self.TUBE_V_THRE
                        and high(tube_front_box_) > self.h_front * 0.2):
                    self.tube_v_info = [self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                        self.num_frame_front, tube_front_box_, w_h_r, self.secs]
        if self.tube_h_info and self.tube_v_info:
            img1 = self.crop_frame(self.tube_h_info[-3], self.tube_h_info[0], self.tube_h_info[3])
            img2 = self.crop_frame(self.tube_v_info[-3], self.tube_v_info[0], self.tube_v_info[3])
            img = np.hstack([img1, img2])
            return [score_index, img, self.time_front, self.objects_front, None, self.num_frame_front]

    def pour_hcl_to_tube(self, score_index, gas_reactions_front, narrow_mouth_bottles_front,
                         narrow_mouth_bottlenecks_front, tubes_front, tube_mouths_front,
                         narrow_mouth_bottlenecks_top, tube_mouths_top):
        """
        向试管中倾倒稀盐酸
        :param score_index:
        :param gas_reactions_front: 气体反应
        :param narrow_mouth_bottles_front: 前视细口瓶
        :param narrow_mouth_bottlenecks_front: 前视细口瓶口
        :param tubes_front: 前视试管
        :param tube_mouths_front: 前视试管口
        :param narrow_mouth_bottlenecks_top: 顶视细口瓶口
        :param tube_mouths_top: 顶视试管口
        :return:
        """
        if not self.reaction_flag and gas_reactions_front.shape[0] > 0:
            self.gas_reaction_secs, self.gas_reaction_secs_pre, flag = self.duration(self.gas_reaction_secs,
                                                                                     2,
                                                                                     self.gas_reaction_secs_pre,
                                                                                     1)
            if flag:
                self.reaction_flag = True
        record = False
        b_m_y = 0
        b_y = 0
        if narrow_mouth_bottlenecks_front.shape[0] > 0:  # 细口瓶口
            for narrow_mouth_bottleneck_front in narrow_mouth_bottlenecks_front:
                narrow_mouth_bottleneck_front_box = narrow_mouth_bottleneck_front[:4]
                b_m_y = center_point(narrow_mouth_bottleneck_front_box)[1]
                if not record and b_m_y < self.h_front * 0.6:
                    if tube_mouths_front.shape[0] > 0:  # 试管口
                        for tube_mouth_front in tube_mouths_front:
                            tube_mouth_front_box = tube_mouth_front[:4]
                            if iou(narrow_mouth_bottleneck_front_box, tube_mouth_front_box) > 0:
                                record = 1
                                break
                    if not record and tubes_front.shape[0] > 0:  # 试管
                        for tube_front in tubes_front:
                            tube_mouth_front_box = deepcopy(tube_front[:4])
                            tube_mouth_front_box[3] = tube_mouth_front_box[1] + self.h_front * 0.05
                            if iou(narrow_mouth_bottleneck_front_box, tube_mouth_front_box) > 0:
                                record = 1
                                break
        if not record and narrow_mouth_bottles_front.shape[0] != 0:  # 细口瓶
            for narrow_mouth_bottle_front in narrow_mouth_bottles_front:
                narrow_mouth_bottle_front_box = narrow_mouth_bottle_front[:4]
                b_y = center_point(narrow_mouth_bottle_front_box)[1]
                if not record and b_y < self.h_front * 0.6:
                    if tube_mouths_front.shape[0] > 0:  # 试管口
                        for tube_mouth_front in tube_mouths_front:
                            tube_mouth_front_box = tube_mouth_front[:4]
                            if iou(narrow_mouth_bottle_front_box, tube_mouth_front_box) > 0:
                                record = 2
                                break
                    if not record and tubes_front.shape[0] > 0:  # 试管
                        for tube_front in tubes_front:
                            tube_front_box = tube_front[:4]
                            if iou(narrow_mouth_bottle_front_box, tube_front_box) > 0:
                                record = 2
                                break
        if record == 1:  # 细口瓶口
            if not self.pour_hcl_info or b_m_y < self.pour_hcl_info[-2] or self.secs - self.pour_hcl_info[-1] > 10:
                self.pour_hcl_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                      self.preds_front, self.num_frame_front, b_m_y, b_m_y, self.secs]
            else:
                self.pour_hcl_info[-1] = self.secs
        elif record == 2:  # 细口瓶
            if not self.pour_hcl_info or b_y < self.pour_hcl_info[-3] or self.secs - self.pour_hcl_info[-1] > 10:
                self.pour_hcl_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                      self.preds_front, self.num_frame_front, b_y, self.h_front, self.secs]
            else:
                self.pour_hcl_info[-1] = self.secs
        elif tube_mouths_top.shape[0] > 0 and narrow_mouth_bottlenecks_top.shape[0] > 0:  # 顶视 试管口 细口瓶口
            for narrow_mouth_bottleneck_top in narrow_mouth_bottlenecks_top:
                narrow_mouth_bottleneck_top_box = narrow_mouth_bottleneck_top[:4]
                for tube_mouth_top in tube_mouths_top:
                    tube_mouth_top_box = tube_mouth_top[:4]
                    if iou(tube_mouth_top_box, narrow_mouth_bottleneck_top_box) > 0:
                        if not self.pour_hcl_info:
                            self.pour_hcl_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                  self.preds_front, self.num_frame_front, self.h_front, self.h_front,
                                                  self.secs]
                        else:
                            self.pour_hcl_info[-1] = self.secs
                        break
        if (self.reaction_flag
                and self.pour_hcl_info
                and self.secs - self.pour_hcl_info[-1] > 1.0
                and abs(self.gas_reaction_secs - self.pour_hcl_info[-1]) < 10):
            return self.pour_hcl_info[:6]

    def tighten_rubber_stopper(self, score_index, hands_front, gas_reactions_front, tubes_front, rubber_stoppers_front,
                               tube_holder_head_irons_top, tubes_top, hands_top, rubber_stoppers_top):
        """
        塞紧橡胶塞
        :param score_index: 得分点索引
        :param hands_front: 前视手
        :param gas_reactions_front: 气体反应
        :param tubes_front: 前视试管
        :param rubber_stoppers_front: 前视橡皮塞
        :param tube_holder_head_irons_top: 顶视试管夹头
        :param tubes_top: 顶视试管
        :param hands_top: 顶视手
        :param rubber_stoppers_top: 顶视橡皮塞
        :return:
        """
        record = False
        if (hands_front.shape[0] > 0  # 手
                and gas_reactions_front.shape[0] == 1  # 气泡反应
                and tubes_front.shape[0] > 0  # 试管
                and rubber_stoppers_front.shape[0] == 1):  # 橡皮塞
            gas_reaction_front_box = gas_reactions_front[0][:4]
            rubber_stopper_front_box = rubber_stoppers_front[0][:4]
            hands_front_rubber_stopper = False  # 前视手和橡皮塞
            for hand_front in hands_front:  # 判断手和橡皮塞是否相交
                hand_front_box = hand_front[:4]
                if iou(hand_front_box, rubber_stopper_front_box) > 0:
                    hands_front_rubber_stopper = True
                    break
            if not hands_front_rubber_stopper:
                for tube_front in tubes_front:
                    tube_front_box = tube_front[:4]
                    if (iou(gas_reaction_front_box, tube_front_box) > box_area(gas_reaction_front_box) * 0.5
                            and center_distance_v(gas_reaction_front_box, tube_front_box) > 0
                            and iou(tube_front_box, rubber_stopper_front_box) > box_area(rubber_stopper_front_box) * 0.3
                            and center_distance_v(tube_front_box, rubber_stopper_front_box) > 0):
                        record = True  # 记录
                        self.tighten_rubber_stopper_secs, self.tighten_rubber_stopper_secs_pre, flag = self.duration(
                            self.tighten_rubber_stopper_secs, 2, self.tighten_rubber_stopper_secs_pre, 0.8)
                        if flag:
                            self.tighten_rubber_stopper_info = [score_index, self.frame_front, self.time_front,
                                                                self.objects_front, self.preds_front,
                                                                self.num_frame_front]
                            return self.tighten_rubber_stopper_info
        if (not record
                and gas_reactions_front.shape[0] == 1  # 气泡反应
                and tube_holder_head_irons_top.shape[0] == 1  # 顶视铁试管夹夹头
                and tubes_top.shape[0] > 0  # 顶视试管
                and hands_top.shape[0] > 0  # 顶视手
                and rubber_stoppers_top.shape[0] == 1):  # 顶视橡皮塞
            tube_holder_head_iron_top_box = tube_holder_head_irons_top[0][:4]  # 铁试管夹头
            rubber_stopper_top_box = rubber_stoppers_top[0][:4]
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(hand_top_box, rubber_stopper_top_box) > 0:
                    return
            for tube_top in tubes_top:
                tube_top_box = tube_top[:4]  # 顶视试管
                if (iou(tube_top_box, rubber_stopper_top_box) > 0
                        and iou(tube_top_box, tube_holder_head_iron_top_box) > 0):
                    self.tighten_rubber_stopper_secs, self.tighten_rubber_stopper_secs_pre, flag = self.duration(
                        self.tighten_rubber_stopper_secs, 2, self.tighten_rubber_stopper_secs_pre, 0.8)
                    if flag:
                        self.tighten_rubber_stopper_info = [score_index, self.frame_top, self.time_top,
                                                            self.objects_top, self.preds_top, self.num_frame_top]
                        return self.tighten_rubber_stopper_info

    def tube_v_restriction(self, score_index, hands_front, tubes_front, gas_reactions_front):
        """
        试管中液体体积不超过试管容器的1/3
        :param score_index:
        :param hands_front:前视手
        :param tubes_front:前视试管
        :param gas_reactions_front:前视反应
        :return:
        """
        if (tubes_front.shape[0] > 0
                and gas_reactions_front.shape[0] == 1
                and hands_front.shape[0] > 0):
            gas_reaction_front_box = gas_reactions_front[0][:4]
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                skip = False
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if iou(hand_front_box, tube_front_box) > 0:
                        skip = True
                        break
                if skip:
                    continue
                if (iou(gas_reaction_front_box, tube_front_box) > box_area(gas_reaction_front_box) * 0.6
                        and center_distance_v(gas_reaction_front_box, tube_front_box) > 0):
                    liquid_h = high(gas_reaction_front_box)
                    tube_h = high(tube_front_box)
                    v_r = liquid_h / tube_h
                    if len(self.v_r_list) < 20:
                        self.v_r_list.append(v_r)
                    else:
                        self.v_r_list.pop(0)
                        self.v_r_list.append(v_r)
                    if len(self.v_r_list) == 20 and sum(self.v_r_list[-10:]) / 10 < self.V_R_THRE:
                        return [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]

    def tube_holder_distance(self, score_index, hands_front, tubes_front, tube_holder_head_irons_front,
                             rubber_stoppers_front):
        """
        判断试管夹距试管口距离 1/2
        :param score_index: 得分点索引
        :param hands_front: 前视手
        :param tubes_front: 前视试管
        :param tube_holder_head_irons_front: 前视铁试管夹头
        :param rubber_stoppers_front: 前视橡胶塞
        :return:
        """
        if (hands_front.shape[0] > 0
                and tubes_front.shape[0] > 0  # 试管
                and tube_holder_head_irons_front.shape[0] == 1  # 铁试管夹头
                and rubber_stoppers_front.shape[0] == 1):  # 橡皮塞
            rubber_stopper_front_box = rubber_stoppers_front[0][:4]
            tube_holder_head_iron_front_box = tube_holder_head_irons_front[0][:4]
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if (iou(hand_front_box, rubber_stopper_front_box) > 0
                        or iou(hand_front_box, tube_holder_head_iron_front_box) > 0):
                    return
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                if (iou(tube_front_box, tube_holder_head_iron_front_box) > 0
                        and iou(tube_front_box, rubber_stopper_front_box) > 0):
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, tube_front_box) > 0:
                            return
                    y = center_point(tube_holder_head_iron_front_box)[1]
                    if tube_front[1] < y < tube_front[3]:
                        r = (y - tube_front[1]) / (tube_front[3] - tube_front[1])  # 距离试管口比值
                        if len(self.tube_holder_d_list) < 20:
                            self.tube_holder_d_list.append(r)
                        else:
                            self.tube_holder_d_list.pop(0)
                            self.tube_holder_d_list.append(r)
                        if (len(self.tube_holder_d_list) == 20
                                and sum(self.tube_holder_d_list[-10:]) / 10 < self.TUBE_HOLDER_D):
                            return [score_index, self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front]

    def collect_gas(self, score_index, rubber_hoses_front, gas_bottles_front, frosted_glass_plates_front,
                    long_gas_pipes_front):
        """
        向上排气法收集二氧化碳气体
        :param score_index:
        :param rubber_hoses_front: 橡胶管
        :param gas_bottles_front: 集气瓶
        :param frosted_glass_plates_front: 毛玻璃片
        :param long_gas_pipes_front:  直角长导管
        :return:
        """
        if (rubber_hoses_front.shape[0] == 1
                and gas_bottles_front.shape[0] == 1
                and long_gas_pipes_front.shape[0] == 1):
            rubber_hose_front_box = rubber_hoses_front[0][:4]  # 橡胶管
            gas_bottle_front_box = gas_bottles_front[0][:4]  # 集气瓶
            long_gas_pipes_front_box = long_gas_pipes_front[0][:4]  # 直角导管
            if (center_distance_v(gas_bottle_front_box, rubber_hose_front_box) > 0
                    and iou(long_gas_pipes_front_box, gas_bottle_front_box) > 0
                    and center_distance_v(gas_bottle_front_box, long_gas_pipes_front_box) > 0):
                self.collect_gas_flag_secs, self.collect_gas_flag_secs_pre, flag = self.duration(self.collect_gas_secs,
                                                                                                 4,
                                                                                                 self.collect_gas_secs_pre,
                                                                                                 2)
                if flag:
                    self.collect_gas_flag = True
                if frosted_glass_plates_front.shape[0] > 0:
                    frosted_glass_plate_front_box = frosted_glass_plates_front[0][:4]
                    if (min_dis_boxes(gas_bottle_front_box, frosted_glass_plate_front_box) < self.h_front * 0.03
                            and center_distance_v(gas_bottle_front_box, frosted_glass_plate_front_box) > 0):
                        self.collect_gas_secs, self.collect_gas_secs_pre, flag = self.duration(self.collect_gas_secs,
                                                                                               4,
                                                                                               self.collect_gas_secs_pre,
                                                                                               2)
                        if flag:
                            return [score_index, self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front]

    @try_decorator
    def check_gas_fill(self, wood_burnings_front, gas_bottles_front, gas_bottle_mouths_front,
                       frosted_glass_plates_front, wood_burnings_top, gas_bottles_top, frosted_glass_plates_top):
        """
        验满 将燃着的木条放在集气瓶口验满
        :param wood_burnings_front: 前视燃着的木条
        :param gas_bottles_front: 前视集气瓶
        :param gas_bottle_mouths_front: 前视集气瓶口
        :param frosted_glass_plates_front: 前视毛玻璃片
        :param wood_burnings_top: 顶视燃着的木条
        :param gas_bottles_top: 顶视集气瓶
        :param frosted_glass_plates_top: 顶视毛玻璃片
        :return:
        """
        if (wood_burnings_front.shape[0] == 1
                and (gas_bottles_front.shape[0] + gas_bottle_mouths_front.shape[0] > 0)):  # 前视
            # and frosted_glass_plates_front.shape[0] == 1
            # frosted_glass_plate_front_box = frosted_glass_plates_front[0][:4]
            gas_bottle_mouth_front_box = self.get_gas_bottle_mouth_front_box(gas_bottles_front,
                                                                             gas_bottle_mouths_front)  # 集气瓶口
            wood_burning_front_box = wood_burnings_front[0][:4]
            if min_dis_boxes(wood_burning_front_box, gas_bottle_mouth_front_box) < self.BUTN_BOTTLE_D_THRE:  # 前视满足
                if wood_burnings_top.shape[0] == 1 and gas_bottles_top.shape[0] == 1:  # 顶视复证
                    wood_burning_top_box = wood_burnings_top[0][:4]
                    gas_bottle_top_box = gas_bottles_top[0][:4]
                    if not iou(gas_bottle_top_box, wood_burning_top_box) > 0:
                        return
                self.check_gas_fill_flag = True
                object_box = combineBox(wood_burning_front_box, wood_burning_front_box)
                self.check_gas_fill_info = [self.frame_front, self.time_front, self.objects_front,
                                            self.preds_front, self.num_frame_front, object_box, self.secs]
                return self.check_gas_fill_info
        elif wood_burnings_top.shape[0] == 1:
            wood_burning_top_box = wood_burnings_top[0][:4]
            if gas_bottles_top.shape[0] == 1:
                gas_bottle_top_box = gas_bottles_top[0][:4]
                if min_dis_boxes(gas_bottle_top_box, wood_burning_top_box) < self.h_top * 0.037:
                    self.check_gas_fill_flag = True
                    object_box = combineBox(wood_burning_top_box, gas_bottle_top_box)
                    self.check_gas_fill_info = [self.frame_top, self.time_top, self.objects_top,
                                                self.preds_top, self.num_frame_top, object_box, self.secs]
                    return self.check_gas_fill_info
            elif frosted_glass_plates_top.shape[0] == 1:
                frosted_glass_plate_top_box = frosted_glass_plates_top[0][:4]
                if min_dis_boxes(frosted_glass_plate_top_box, wood_burning_top_box) < self.h_top * 0.037:
                    self.check_gas_fill_flag = True
                    object_box = combineBox(wood_burning_top_box, frosted_glass_plate_top_box)
                    self.check_gas_fill_info = [self.frame_top, self.time_top, self.objects_top,
                                                self.preds_top, self.num_frame_top, object_box, self.secs]
                    return self.check_gas_fill_info

    @staticmethod
    def get_gas_bottle_mouth_front_box(gas_bottles_front, gas_bottle_mouths_front):
        if gas_bottle_mouths_front.shape[0] > 0:
            return gas_bottle_mouths_front[0][:4]
        if gas_bottles_front.shape[0] > 0:
            gas_bottle_mouth_front_box = deepcopy(gas_bottles_front[0][:4])
            gas_bottle_mouth_front_box[3] = gas_bottle_mouth_front_box[1] + (
                    gas_bottle_mouth_front_box[3] - gas_bottle_mouth_front_box[1]) * 0.25
            return gas_bottle_mouth_front_box

    @try_decorator
    def gas_fill(self, wood_extinguishs_front, gas_bottles_front, gas_bottle_mouths_front, wood_burnings_front,
                              frosted_glass_plates_front,
                              wood_extinguishs_top, gas_bottles_top, wood_burnings_top, frosted_glass_plates_top):
        """
        木条熄灭，收集满二氧化碳
        :param wood_extinguishs_front: 前视木条熄灭
        :param gas_bottles_front: 前视集气瓶
        :param gas_bottle_mouths_front: 前视集气瓶口
        :param wood_burnings_front: 前视木条燃烧
        :param frosted_glass_plates_front: 前视毛玻璃片
        :param wood_extinguishs_top: 顶视木条熄灭
        :param gas_bottles_top: 顶视集气瓶
        :param wood_burnings_top: 顶视木条燃烧
        :param frosted_glass_plates_top: 顶视毛玻璃片
        :return:
        """
        if wood_extinguishs_front.shape[0] == 1:  # 前视木条熄灭
            wood_extinguish_front_box = wood_extinguishs_front[0][:4]
            if gas_bottles_front.shape[0] + gas_bottle_mouths_front.shape[0] > 0:  # 集气瓶
                gas_bottle_mouth_front_box = self.get_gas_bottle_mouth_front_box(gas_bottles_front,
                                                                                 gas_bottle_mouths_front)  # 集气瓶口
                if min_dis_boxes(wood_extinguish_front_box, gas_bottle_mouth_front_box) < self.EXTINGUISH_BOTTLE_D_THRE:
                    object_box = combineBox(wood_extinguish_front_box, gas_bottle_mouth_front_box)
                    self.gas_fill_info = [self.frame_front, self.time_front, self.objects_front,
                                          self.preds_front, self.num_frame_front, object_box, self.secs]
        if not self.gas_fill_info and wood_extinguishs_top.shape[0] == 1 and gas_bottles_top.shape[0] == 1:  # 顶视
            wood_extinguish_top_box = wood_extinguishs_top[0][:4]
            gas_bottle_top_box = gas_bottles_top[0][:4]
            if iou(wood_extinguish_top_box, gas_bottle_top_box) > 0:
                object_box = combineBox(wood_extinguish_top_box, gas_bottle_top_box)
                self.gas_fill_info = [self.frame_top, self.time_top, self.objects_top,
                                      self.preds_top, self.num_frame_top, object_box, self.secs]
        if not self.gas_fill_info and wood_extinguishs_top.shape[0] == 1 and frosted_glass_plates_top.shape[0] == 1:  # 顶视
            wood_extinguish_top_box = wood_extinguishs_top[0][:4]
            frosted_glass_plate_top_box = frosted_glass_plates_top[0][:4]
            if iou(wood_extinguish_top_box, frosted_glass_plate_top_box) > 0:
                object_box = combineBox(wood_extinguish_top_box, frosted_glass_plate_top_box)
                self.gas_fill_info = [self.frame_top, self.time_top, self.objects_top,
                                      self.preds_top, self.num_frame_top, object_box, self.secs]
        if self.gas_fill_info and self.secs - self.gas_fill_info[-1] > 4:
            return self.gas_fill_info
        if not self.gas_fill_info and self.check_gas_fill_flag:
            if wood_burnings_front.shape[0] == 0 and wood_burnings_top.shape[0] == 0:  # 没有检测到木条燃烧
                if not self.gas_fill_info_default:
                    self.gas_fill_info_default = [self.frame_front, self.time_front, self.objects_front,
                                                  self.preds_front, self.num_frame_front, None, self.secs]
                self.gas_fill_secs, self.gas_fill_secs_pre, flag = self.duration(self.gas_fill_secs,
                                                                                 5,
                                                                                 self.gas_fill_secs_pre,
                                                                                 2)
                if flag:
                    self.gas_fill_flag = True
                    return self.gas_fill_info_default
            else:
                self.init_gas_fill()

    def gas_bottle_up(self, score_index,
                      hands_front, gas_bottles_front, frosted_glass_plates_front,
                      long_gas_pipes_front,
                      hands_top, gas_bottles_top, frosted_glass_plates_top,
                      long_gas_pipes_top
                      ):
        """
        用毛玻璃片磨砂面盖好集气瓶并正放在桌面上
        :param score_index:
        :param hands_front: 前视手
        :param gas_bottles_front: 前视集气瓶
        :param frosted_glass_plates_front: 前视毛玻璃片
        :param long_gas_pipes_front: 前视直角长导管
        :param hands_top: 顶视手
        :param gas_bottles_top: 顶视集气瓶
        :param frosted_glass_plates_top: 顶视毛玻璃片
        :param long_gas_pipes_top: 顶视直角长导管
        :return:
        """
        if gas_bottles_front.shape[0] == 1 and long_gas_pipes_front.shape[0] == 1:
            gas_bottle_front_box = gas_bottles_front[0][:4]  # 集气瓶
            long_gas_pipe_front_box = long_gas_pipes_front[0][:4]  # 长导管
            if iou(long_gas_pipe_front_box, gas_bottle_front_box) > 0:  # 长导管与集气瓶有交集停止
                return
            if hands_front.shape[0] != 0 and frosted_glass_plates_front.shape[0] == 1:
                frosted_glass_plate_front_box = frosted_glass_plates_front[0][:4]  # 毛玻璃片
                if (iou(gas_bottle_front_box, frosted_glass_plate_front_box) > 0
                        and center_distance_v(frosted_glass_plate_front_box, gas_bottle_front_box) < 0):
                    hand_gas_bottle = False  # 手和集气瓶是否有交集
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, gas_bottle_front_box) > 0:
                            hand_gas_bottle = True
                            break
                    if not hand_gas_bottle:
                        self.gas_bottle_up_secs, self.gas_bottle_up_secs_pre, flag = self.duration(
                            self.gas_bottle_up_secs, 2, self.gas_bottle_up_secs_pre, 1)
                        if flag:
                            return [score_index, self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front]
        elif (gas_bottles_top.shape[0] == 1
              and frosted_glass_plates_top.shape[0] == 1
              and hands_top.shape[0] != 0):
            frosted_glass_plate_top_box = frosted_glass_plates_top[0][:4]  # 顶视毛玻璃片
            gas_bottle_top_box = gas_bottles_top[0][:4]
            if long_gas_pipes_top.shape[0] == 1:  # 顶视长导管与毛玻璃片或集气瓶有交集则停止
                long_gas_pipe_top_box = long_gas_pipes_top[0][:4]
                if (iou(long_gas_pipe_top_box, gas_bottle_top_box) > 0
                        or iou(long_gas_pipe_top_box, frosted_glass_plate_top_box) > 0):
                    return
            if iou(gas_bottle_top_box, frosted_glass_plate_top_box) > box_area(frosted_glass_plate_top_box) * 0.3:
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, gas_bottle_top_box) > 0:
                        return
                self.gas_bottle_up_secs, self.gas_bottle_up_secs_pre, flag = self.duration(
                    self.gas_bottle_up_secs, 2, self.gas_bottle_up_secs_pre, 1)
                if flag:
                    return [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                            self.num_frame_top]

    @try_decorator
    def extinguish_alcohol_lamp(self, hands_front, alcohol_lamp_flams_front, alcohol_lamps_front,
                                alcohol_lamp_caps_front,
                                hands_top, alcohol_lamp_flams_top, alcohol_lamps_top,
                                alcohol_lamp_caps_top):
        """
        用酒精灯帽熄灭酒精灯
        :param hands_front: 前视手
        :param alcohol_lamp_flams_front: 前视酒精灯火焰
        :param alcohol_lamps_front: 前视酒精灯
        :param alcohol_lamp_caps_front: 前视酒精灯帽
        :param hands_top: 顶视手
        :param alcohol_lamp_flams_top: 顶视酒精灯火焰
        :param alcohol_lamps_top: 顶视酒精灯
        :param alcohol_lamp_caps_top: 顶视酒精灯帽
        :return:
        """
        if not self.alcohol_burn_flag:
            alcohol_burn = False
            if alcohol_lamp_flams_front.shape[0] == 1 and alcohol_lamps_front.shape[0] == 1:
                alcohol_lamp_front_box = alcohol_lamps_front[0][:4]
                alcohol_lamp_flam_front_box = alcohol_lamp_flams_front[0][:4]
                if (center_distance_v(alcohol_lamp_front_box, alcohol_lamp_flam_front_box) > 0  # 火焰在酒精灯上
                        and min_dis_boxes(alcohol_lamp_front_box,
                                          alcohol_lamp_flam_front_box) < self.h_front * 0.06):  # 酒精灯上有火焰
                    alcohol_burn = True
            if not alcohol_burn and alcohol_lamp_flams_top.shape[0] == 1 and alcohol_lamps_top.shape[0] == 1:
                alcohol_lamp_top_box = alcohol_lamps_top[0][:4]
                alcohol_lamp_flam_top_box = alcohol_lamp_flams_top[0][:4]
                if min_dis_boxes(alcohol_lamp_top_box, alcohol_lamp_flam_top_box) < self.h_top * 0.06:
                    alcohol_burn = True
            if alcohol_burn:
                self.alcohol_burn_secs, self.alcohol_burn_secs_pre, flag = self.duration(
                    self.alcohol_burn_secs,
                    self.alcohol_burn_duration_THRE,
                    self.alcohol_burn_secs_pre,
                    self.alcohol_burn_interval_THRE
                )
                if flag:
                    self.alcohol_burn_flag = True
            return
        if alcohol_lamps_front.shape[0] > 0 and alcohol_lamp_flams_front.shape[0] > 0:  # 前视 酒精灯 火焰
            alcohol_lamp_front_box = alcohol_lamps_front[0][:4]
            alcohol_lamp_flam_front_box = alcohol_lamp_flams_front[0][:4]
            if (center_distance_v(alcohol_lamp_front_box, alcohol_lamp_flam_front_box) > 0  # 火焰在酒精灯上
                    and min_dis_boxes(alcohol_lamp_front_box,
                                      alcohol_lamp_flam_front_box) < self.h_front * 0.06):  # 酒精灯上有火焰
                self.last_alcohol_burn_secs = self.secs  # 酒精灯燃烧的时间
                object_box = combineBox(alcohol_lamp_front_box, alcohol_lamp_flam_front_box)
                self.last_flame_info = [self.frame_front, self.time_front, self.objects_front,
                                        self.preds_front, self.num_frame_front, object_box, self.secs]
                if alcohol_lamp_caps_front.shape[0] > 0 and hands_front.shape[0] > 0:  # 酒精灯帽
                    alcohol_lamp_cap_front_box = alcohol_lamp_caps_front[0][:4]
                    hand_cap = False  # 手拿酒精灯帽
                    for hand_front in hands_front:
                        hand_front_box = hand_front[:4]
                        if iou(hand_front_box, alcohol_lamp_cap_front_box) > 0:
                            hand_cap = True
                            break
                    if hand_cap and min_dis_boxes(alcohol_lamp_cap_front_box,
                                                  alcohol_lamp_flam_front_box) < self.h_front * 0.05:
                        verify = True  # 顶部验证 暂时去除（视频不同步影响较大）
                        # if alcohol_lamp_caps_top.shape[0] > 0 and alcohol_lamp_flams_top.shape[0] > 0:
                        #     alcohol_lamp_cap_top_box = alcohol_lamp_caps_top[0][:4]
                        #     alcohol_lamp_flam_top_box = alcohol_lamp_flams_top[0][:4]
                        #     print(min_dis_boxes(alcohol_lamp_cap_top_box, alcohol_lamp_flam_top_box))
                        #     if min_dis_boxes(alcohol_lamp_cap_top_box, alcohol_lamp_flam_top_box) > self.h_top * 0.12:  # 顶视灯帽和火焰较远
                        #         verify = False
                        # elif alcohol_lamp_caps_top.shape[0] > 0 and alcohol_lamps_top.shape[0] > 0:  # 顶视灯帽和灯无交集
                        #     alcohol_lamp_cap_top_box = alcohol_lamp_caps_top[0][:4]
                        #     alcohol_lamp_flam_top_box = alcohol_lamp_flams_top[0][:4]
                        #     if min_dis_boxes(alcohol_lamp_cap_top_box, alcohol_lamp_flam_top_box) > self.h_top * 0.6:
                        #         verify = False
                        if verify:
                            object_box = combineBox(alcohol_lamp_front_box, alcohol_lamp_flam_front_box,
                                                    alcohol_lamp_cap_front_box)
                            self.flame_cap_info = [self.frame_front, self.time_front, self.objects_front,
                                                   self.preds_front, self.num_frame_front, object_box, self.secs]

        elif alcohol_lamps_top.shape[0] > 0 and alcohol_lamp_flams_top.shape[0] > 0:  # 顶视 酒精灯 火焰
            alcohol_lamp_top_box = alcohol_lamps_top[0][:4]
            alcohol_lamp_flam_top_box = alcohol_lamp_flams_top[0][:4]
            if min_dis_boxes(alcohol_lamp_top_box, alcohol_lamp_flam_top_box) < self.h_top * 0.06:
                self.last_alcohol_burn_secs = self.secs
                object_box = combineBox(alcohol_lamp_top_box, alcohol_lamp_flam_top_box)
                self.last_flame_info = [self.frame_top, self.time_top, self.objects_top,
                                        self.preds_top, self.num_frame_top, object_box, self.secs]
                if alcohol_lamp_caps_top.shape[0] > 0 and hands_top.shape[0] > 0:  # 顶视酒精灯帽
                    alcohol_lamp_cap_top_box = alcohol_lamp_caps_top[0][:4]
                    hand_cap = False  # 手拿酒精灯帽
                    for hand_top in hands_top:
                        hand_top_box = hand_top[:4]
                        if iou(hand_top_box, alcohol_lamp_cap_top_box) > 0:
                            hand_cap = True
                            break
                    if hand_cap and min_dis_boxes(alcohol_lamp_cap_top_box,
                                                  alcohol_lamp_flam_top_box) < self.h_top * 0.06:
                        object_box = combineBox(alcohol_lamp_top_box, alcohol_lamp_flam_top_box,
                                                alcohol_lamp_cap_top_box)
                        self.flame_cap_info = [self.frame_top, self.time_top, self.objects_top,
                                               self.preds_top, self.num_frame_top, object_box, self.secs]

        if alcohol_lamp_flams_front.shape[0] == 0 and alcohol_lamp_flams_top.shape[0] == 0:  # 顶视前视 无火焰
            if alcohol_lamps_front.shape[0] == 1 and alcohol_lamp_caps_front.shape[0] == 1:  # 前视酒精灯和灯帽
                alcohol_lamp_front_box = alcohol_lamps_front[0][:4]
                alcohol_lamp_cap_front_box = alcohol_lamp_caps_front[0][:4]
                if (iou(alcohol_lamp_front_box, alcohol_lamp_cap_front_box) > 0  # 酒精灯盖帽
                        and center_distance_v(alcohol_lamp_front_box, alcohol_lamp_cap_front_box) > 0
                        and center_distance_h(alcohol_lamp_front_box, alcohol_lamp_cap_front_box, True) < width(
                            alcohol_lamp_cap_front_box)):
                    if self.flame_cap_info and self.secs - self.flame_cap_info[-1] > 2:
                        return self.flame_cap_info
                    elif not self.flame_cap_info and self.last_alcohol_burn_secs > 0:
                        if self.secs - self.last_alcohol_burn_secs < self.BURN_EXTINGUISH_INTERVAL_THRE:
                            object_box = combineBox(alcohol_lamp_front_box, alcohol_lamp_cap_front_box)
                            self.flame_cap_info = [self.frame_front, self.time_front, self.objects_front,
                                                   self.preds_front, self.num_frame_front, object_box, self.secs]
                            img1 = self.crop_frame(self.last_flame_info[-2], self.last_flame_info[0],
                                                   self.last_flame_info[3])
                            img2 = self.crop_frame(self.flame_cap_info[-2], self.flame_cap_info[0],
                                                   self.flame_cap_info[3])
                            img = np.hstack([img1, img2])
                            self.flame_cap_info = [img, self.flame_cap_info[1], self.flame_cap_info[2], None,
                                                   self.flame_cap_info[4], object_box, self.secs]
                            # return self.flame_cap_info
            elif alcohol_lamps_top.shape[0] == 1 and alcohol_lamp_caps_top.shape[0] == 1:  # 顶视酒精灯和灯帽
                alcohol_lamp_top_box = alcohol_lamps_top[0][:4]
                alcohol_lamp_cap_top_box = alcohol_lamp_caps_top[0][:4]
                if iou(alcohol_lamp_top_box, alcohol_lamp_cap_top_box) > box_area(
                        alcohol_lamp_cap_top_box) * 0.1:  # 顶视酒精灯帽
                    if self.flame_cap_info and self.secs - self.flame_cap_info[-1] > 2:
                        return self.flame_cap_info
                    elif not self.flame_cap_info and self.last_alcohol_burn_secs > 0:
                        if self.secs - self.last_alcohol_burn_secs < self.BURN_EXTINGUISH_INTERVAL_THRE:  # 熄灭后有灯帽 和燃烧时差 小于 0.5 秒
                            object_box = combineBox(alcohol_lamp_top_box, alcohol_lamp_cap_top_box)
                            self.flame_cap_info = [self.frame_top, self.time_top, self.objects_top,
                                                   self.preds_top, self.num_frame_top, object_box, self.secs]
                            img1 = self.crop_frame(self.last_flame_info[-2], self.last_flame_info[0],
                                                   self.last_flame_info[3])
                            img2 = self.crop_frame(self.flame_cap_info[-2], self.flame_cap_info[0],
                                                   self.flame_cap_info[3])
                            img = np.hstack([img1, img2])
                            self.flame_cap_info = [img, self.flame_cap_info[1], self.flame_cap_info[2], None,
                                                   self.flame_cap_info[4], object_box, self.secs]
        elif self.flame_cap_info and self.secs - self.flame_cap_info[-1] > 1:
            self.flame_cap_info = []

        if (not self.cap_lamp_cap_front_info
                and (hands_front.shape[0] > 0 and alcohol_lamps_front.shape[0] > 0 and alcohol_lamp_caps_front.shape[
                    0] > 0)):
            alcohol_lamp_front_box = alcohol_lamps_front[0][:4]
            alcohol_lamp_cap_front_box = alcohol_lamp_caps_front[0][:4]
            if (iou(alcohol_lamp_front_box, alcohol_lamp_cap_front_box) > 0  # 酒精灯盖帽
                and center_distance_v(alcohol_lamp_front_box, alcohol_lamp_cap_front_box)) > 0:
                for hand_front in hands_front:
                    hand_front_box = hand_front[:4]
                    if (iou(hand_front_box, alcohol_lamp_cap_front_box) > 0
                            and center_distance_v(alcohol_lamp_cap_front_box, hand_front_box) > 0):
                        self.cap_lamp_cap_front_info = [self.frame_front, self.time_front, self.objects_front,
                                                        self.preds_front, self.num_frame_front, self.secs]

        if (not self.cap_lamp_cap_top_info
                and (hands_top.shape[0] > 0 and alcohol_lamps_top.shape[0] > 0 and alcohol_lamp_caps_top.shape[0] > 0)):
            alcohol_lamp_top_box = alcohol_lamps_top[0][:4]
            alcohol_lamp_cap_top_box = alcohol_lamp_caps_top[0][:4]
            if iou(alcohol_lamp_top_box, alcohol_lamp_cap_top_box) > box_area(alcohol_lamp_cap_top_box) * 0.5:
                for hand_top in hands_top:
                    hand_top_box = hand_top[:4]
                    if iou(hand_top_box, alcohol_lamp_cap_top_box) > box_area(alcohol_lamp_cap_top_box) * 0.3:
                        self.cap_lamp_cap_top_info = [self.frame_top, self.time_top, self.objects_top,
                                                      self.preds_top, self.num_frame_top, self.secs]

    @try_decorator
    def litmus_color_change(self, tubes_front, pipe_pipes_front, purple_liquids_front, pink_liquids_front, tubes_top,
                            purple_liquids_top, pink_liquids_top):
        """
        紫色石蕊试剂变红
        :param tubes_front:  前视试管
        :param pipe_pipes_front: 前视导管-导管
        :param purple_liquids_front: 前视紫色液体
        :param pink_liquids_front: 前视粉红液体
        :param tubes_top: 前视导管-导管
        :param purple_liquids_top: 前视紫色液体
        :param pink_liquids_top: 前视粉红液体
        :return:
        """
        if not self.litmus_purple_info and tubes_front.shape[0] > 0 and purple_liquids_front.shape[0] > 0:
            for purple_liquid_front in purple_liquids_front:
                purple_liquid_front_box = purple_liquid_front[:4]
                is_break = False
                for tube_front in tubes_front:
                    tube_front_box = tube_front[:4]
                    if iou(tube_front_box, purple_liquid_front_box) > box_area(purple_liquid_front_box) * 0.6:
                        if self.litmus_purple_n < self.LITMUS_PURPLE_N_THRED:
                            self.litmus_purple_n += 1
                            is_break = True
                            break
                        elif self.litmus_purple_secs == 0:
                            self.init_litmus_pink()
                            self.litmus_purple_secs = self.secs
                            is_break = True
                            break
                        elif self.secs - self.litmus_purple_secs > 1:
                            object_box = combineBox(tube_front_box, purple_liquid_front_box)
                            self.litmus_purple_info = [self.frame_front, self.time_front, self.objects_front,
                                                       self.preds_front, self.num_frame_front, object_box, self.secs]
                            is_break = True
                            break
                if is_break:
                    break
        if tubes_front.shape[0] > 0 and pink_liquids_front.shape[0] > 0:
            for pink_liquid_front in pink_liquids_front:
                pink_liquid_front_box = pink_liquid_front[:4]
                is_break = False
                for tube_front in tubes_front:
                    tube_front_box = tube_front[:4]
                    if iou(tube_front_box, pink_liquid_front_box) > box_area(pink_liquid_front_box) * 0.6:
                        if self.litmus_pink_n < self.LITMUS_PINK_N_THRE:
                            self.litmus_pink_n += 1
                            self.litmus_pink_secs = self.secs
                            object_box = combineBox(tube_front_box, pink_liquid_front_box)
                            self.litmus_pink_info_lit = [self.frame_front, self.time_front, self.objects_front,
                                                         self.preds_front, self.num_frame_front, object_box, self.secs]
                            is_break = True
                            break
                        else:
                            object_box = combineBox(tube_front_box, pink_liquid_front_box)
                            self.litmus_pink_info = [self.frame_front, self.time_front, self.objects_front,
                                                     self.preds_front, self.num_frame_front, object_box, self.secs]
                            self.litmus_only_pink_info = [self.frame_front, self.time_front, self.objects_front,
                                                          self.preds_front, self.num_frame_front, object_box, self.secs]
                            is_break = True
                            break
                if is_break:
                    break

        if self.litmus_pink_info and self.litmus_purple_info:
            if self.litmus_pink_info[-1] - self.litmus_purple_secs > 0:
                if self.secs - self.litmus_pink_secs > 3:
                    img1 = self.crop_frame(self.litmus_purple_info[-2], self.litmus_purple_info[0],
                                           self.litmus_purple_info[3])
                    img2 = self.crop_frame(self.litmus_pink_info[-2], self.litmus_pink_info[0],
                                           self.litmus_pink_info[3])
                    img = np.hstack([img1, img2])
                    self.litmus_color_change_secs = self.secs
                    return img, self.litmus_pink_info[1], self.litmus_pink_info[2], None, self.litmus_pink_info[4]
            else:
                self.litmus_pink_info = []
                self.litmus_pink_secs = 0

        if self.litmus_pink_info and self.secs - self.litmus_pink_secs > 6:
            self.litmus_color_change_secs = self.secs
            return self.litmus_pink_info[:5]

        if tubes_top.shape[0] > 0 and purple_liquids_top.shape[0] > 0:
            for tube_top in tubes_top:
                tube_top_box = tube_top[:4]
                is_break = False
                if pt_in_polygon(center_point(tube_top_box), self.center_area_top):
                    for purple_liquid_top in purple_liquids_top:
                        purple_liquid_top_box = purple_liquid_top[:4]
                        if iou(purple_liquid_top_box, tube_top_box) > box_area(purple_liquid_top_box) * 0.4:
                            if self.litmus_purple_n_top < self.LITMUS_PURPLE_N_TOP_THRED:
                                self.litmus_purple_n_top += 1
                                is_break = True
                                break
                            elif self.litmus_purple_top_secs == 0:
                                self.init_litmus_pink_top()
                                self.litmus_pink_top_secs = self.secs
                                is_break = True
                                break
                            elif self.secs - self.litmus_purple_top_secs > 1:
                                object_box = combineBox(tube_top_box, purple_liquid_top_box)
                                self.litmus_purple_top_info = [self.frame_top, self.time_top, self.objects_top,
                                                               self.preds_top, self.num_frame_top, object_box,
                                                               self.secs]
                                is_break = True
                                break
                    if is_break:
                        break

        if tubes_top.shape[0] > 0 and pink_liquids_top.shape[0] > 0:
            for tube_top in tubes_top:
                tube_top_box = tube_top[:4]
                is_break = False
                if pt_in_polygon(center_point(tube_top_box), self.center_area_top):
                    for pink_liquid_top in pink_liquids_top:
                        pink_liquid_top_box = pink_liquid_top[:4]
                        if iou(tube_top_box, pink_liquid_top_box) > box_area(pink_liquid_top_box) * 0.4:
                            if self.litmus_pink_n_top < self.LITMUS_PINK_N_TOP_THRE:
                                self.litmus_pink_n_top += 1
                                self.litmus_pink_top_secs = self.secs
                                is_break = True
                                break
                            else:
                                object_box = combineBox(tube_top_box, pink_liquid_top_box)
                                self.litmus_pink_top_info = [self.frame_front, self.time_front, self.objects_front,
                                                             self.preds_front, self.num_frame_front, object_box,
                                                             self.secs]
                                self.litmus_only_pink_top_info = [self.frame_front, self.time_front, self.objects_front,
                                                                  self.preds_front, self.num_frame_front, object_box,
                                                                  self.secs]
                                is_break = True
                                break
                    if is_break:
                        break

        if self.litmus_pink_top_info and self.litmus_purple_top_info:
            if self.litmus_pink_top_info[-1] - self.litmus_purple_top_info > 0:
                if self.secs - self.litmus_pink_top_secs > 3:
                    img1 = self.crop_frame(self.litmus_purple_top_info[-2], self.litmus_purple_top_info[0],
                                           self.litmus_purple_top_info[3])
                    img2 = self.crop_frame(self.litmus_pink_top_info[-2], self.litmus_pink_top_info[0],
                                           self.litmus_pink_top_info[3])
                    img = np.hstack([img1, img2])
                    self.litmus_color_change_secs = self.secs
                    return img, self.litmus_pink_top_info[1], self.litmus_pink_top_info[2], None, \
                           self.litmus_pink_top_info[4]
            else:
                self.litmus_pink_top_info = []
                self.litmus_pink_top_secs = 0

        if self.litmus_pink_top_info and self.secs - self.litmus_pink_top_secs > 6:
            self.litmus_color_change_secs = self.secs
            return self.litmus_pink_top_info[:5]

    @try_decorator
    def separate_liquid_solid(self, conical_flasks_front, conical_flask_mouths_front, liquid_wastes_front,
                              beakers_front, marbles_front, conical_flasks_top, conical_flask_mouths_top,
                              liquid_wastes_top, marbles_top, beakers_top):
        """
        固体和液体分开回收
        :param conical_flasks_front:
        :param conical_flask_mouths_front:
        :param liquid_wastes_front:
        :param beakers_front:
        :param marbles_front:
        :param conical_flasks_top:
        :param conical_flask_mouths_top:
        :param liquid_wastes_top:
        :param marbles_top:
        :param beakers_top:
        :return:
        """
        if (not self.seprate_liquid_info
                and conical_flasks_front.shape[0] > 0
                and conical_flask_mouths_front.shape[0] > 0
                and beakers_front.shape[0] > 0):  # 前视倒废液 锥形瓶 锥形瓶口 烧杯
            conical_flask_front_box = conical_flasks_front[0][:4]
            conical_flask_mouth_front_box = conical_flask_mouths_front[0][:4]
            is_continue = False
            if liquid_wastes_front.shape[0] > 0:
                for liquid_waste_front in liquid_wastes_front:
                    liquid_waste_front_box = liquid_waste_front[:4]
                    if (iou(conical_flask_front_box, liquid_waste_front_box) > box_area(
                            liquid_waste_front_box) * 0.05):  # 锥形瓶中有废液
                        is_continue = True
                        break
            if marbles_front.shape[0] > 0:
                for marble_front in marbles_front:
                    marble_front_box = marble_front[:4]
                    if (iou(conical_flask_front_box, marble_front_box) > box_area(marble_front_box) * 0.05):  # 锥形瓶中有大理石
                        is_continue = True
                        break
            if is_continue:
                for beaker_front in beakers_front:
                    beaker_front_box = beaker_front[:4]
                    if (iou(beaker_front_box, conical_flask_mouth_front_box) > 0
                            and center_distance_v(beaker_front_box, conical_flask_front_box) > 0):
                        object_box = combineBox(conical_flask_front_box, beaker_front_box)
                        self.seprate_liquid_info = [self.frame_front, self.time_front, self.objects_front,
                                                    self.preds_front, self.num_frame_front, object_box,
                                                    self.secs]
                        break

        if (not self.seprate_liquid_info
                and conical_flasks_top.shape[0] > 0):  # 顶视倒废液
            pass

        if self.seprate_liquid_info and not self.interlude_flag:  # 判断中间停顿
            if conical_flasks_front.shape[0] > 0 and conical_flask_mouths_front.shape[0] > 0:
                conical_flask_front_box = conical_flasks_front[0][:4]
                conical_flask_mouth_front_box = conical_flask_mouths_front[0][:4]
                if center_distance_v(conical_flask_front_box, conical_flask_mouth_front_box) > high(
                        conical_flask_mouth_front_box):
                    self.interlude_flag = True

        if self.interlude_flag and not self.seprate_solid_info:  # 判断倒固体
            if conical_flasks_front.shape[0] > 0 and conical_flask_mouths_front.shape[0] > 0 and beakers_front.shape[
                0] > 0:
                conical_flask_front_box = conical_flasks_front[0][:4]
                conical_flask_mouth_front_box = conical_flask_mouths_front[0][:4]
                if center_distance_v(conical_flask_mouth_front_box, conical_flask_front_box) > high(
                        conical_flask_mouth_front_box):
                    for beaker_front in beakers_front:
                        beaker_front_box = beaker_front[:4]
                        if iou(beaker_front_box, conical_flask_mouth_front_box) > 0:
                            object_box = combineBox(conical_flask_front_box, beaker_front_box)
                            self.seprate_solid_info = [self.frame_front, self.time_front, self.objects_front,
                                                       self.preds_front, self.num_frame_front, object_box,
                                                       self.secs]

        if self.seprate_liquid_info and self.seprate_solid_info:
            img1 = self.crop_frame(self.seprate_liquid_info[-2], self.seprate_liquid_info[0],
                                   self.seprate_liquid_info[3])
            img2 = self.crop_frame(self.seprate_solid_info[-2], self.seprate_solid_info[0], self.seprate_solid_info[3])
            img = np.hstack([img1, img2])
            return img, self.seprate_liquid_info[1], self.seprate_liquid_info[2], None, self.seprate_liquid_info[4]

    def co2_to_lime_water(self, score_index, long_gas_pipes_front, tubes_front):
        """
        二氧化碳通入澄清石灰水
        :param score_index:
        :param long_gas_pipes_front: # 长导管
        :param tubes_front:  # 试管
        :return:
        """
        if long_gas_pipes_front.shape[0] == 1 and tubes_front.shape[0] != 0:
            long_gas_pipe_front_box = long_gas_pipes_front[0][:4]
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                if pt_in_polygon(center_point(tube_front_box), self.center_area_front):
                    if iou(long_gas_pipe_front_box, tube_front_box) > 0:
                        self.co2_limewater_secs, self.co2_limewater_secs_pre, flag = self.duration(
                            self.co2_limewater_secs, 4, self.co2_limewater_secs_pre, 2)
                        if flag:
                            self.co2_to_lime_water_flag = True
                            return [score_index, self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front]

    def lime_water_turbid(self, score_index, turbid_whitewashs_front, tubes_front, long_gas_pipes_front):
        """
        澄清石灰水变浑浊
        :param score_index:
        :param turbid_whitewashs_front: # 前视石灰水浑浊
        :param tubes_front: # 前视试管
        :param long_gas_pipes_front: # 前视直角长导管
        :return:
        """
        if turbid_whitewashs_front.shape[0] == 1 and tubes_front.shape[0] > 0:
            turbid_whitewash_front_box = turbid_whitewashs_front[0][:4]
            for tube_front in tubes_front:
                tube_front_box = tube_front[:4]
                if (iou(turbid_whitewash_front_box, tube_front_box) > 0
                        and center_distance_v(turbid_whitewash_front_box, tube_front_box) > 0):
                    if self.co2_to_lime_water_flag:
                        return [score_index, self.frame_front, self.time_front, self.objects_front, self.preds_front,
                                self.num_frame_front]
                    elif long_gas_pipes_front.shape[0] == 0:
                        self.lime_water_turbid_secs, self.lime_water_turbid_secs_pre, flag = self.duration(
                            self.lime_water_turbid_secs, 2, self.lime_water_turbid_secs_pre, 1)
                        if flag:
                            return [score_index, self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front]

    def update_info_list(self, score_index, info_list, view='front', step=1.):
        """
        更新记录信息
        :param score_index: 得分点列表
        :param info_list: 记录信息列表
        :param view: 视角
        :param step: 间隔时长
        :return:
        """
        update = False
        if not info_list:
            update = True
        else:
            length = len(info_list)
            if self.secs - info_list[-1][-1] > length * step:
                update = True
            if update and length == 3:
                info_list.pop(0)
        if update:
            if view == 'front':
                info_list.append([score_index, self.frame_front, self.time_front, self.objects_front,
                                  self.preds_front, self.num_frame_front, self.secs])
            else:
                info_list.append([score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                  self.num_frame_top, self.secs])
        return info_list

    def crop_frame(self, box=None, frame=None, preds=None):
        if box is None:
            x = int(self.w_front) / 2
        else:
            x = int(center_point(box)[0])
        if x < self.w_front / 4:
            x1, x2 = 0, int(self.w_front / 2)
        elif x < (self.w_front / 4) * 3:
            x1, x2 = int(x - self.w_front / 4), int(x + self.w_front / 4)
        else:
            x1, x2 = int(self.w_front / 2), int(self.w_front)
        self.plot(preds, frame)
        return frame[:, x1:x2, :]

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

    @try_decorator
    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if not self.scorePoint3 and self.select_HCl_z_info:
            self.assignScore(3, *self.select_HCl_z_info[:5])
        if not self.scorePoint4 and self.add_hcl_z_infos:
            info = self.add_hcl_z_infos[0] if len(self.add_hcl_z_infos) == 1 else self.add_hcl_z_infos[1]
            self.assignScore(4, *info[:5])
            if not self.scorePoint3:
                self.assignScore(3, *info[:5])
        if not self.scorePoint5 and self.gas_fill_info:
            self.assignScore(5, *self.gas_fill_info[:5])
        if not self.scorePoint6:
            if self.flame_cap_info:
                self.assignScore(6, *self.flame_cap_info[:5])
            elif self.cap_lamp_cap_top_info:
                self.assignScore(6, *self.cap_lamp_cap_top_info[:5])
            elif self.cap_lamp_cap_front_info:
                self.assignScore(6, *self.cap_lamp_cap_front_info[:5])
        if not self.scorePoint7:
            if self.litmus_only_pink_info:
                self.assignScore(7, *self.litmus_only_pink_info[:5])
            elif self.litmus_pink_info_lit and self.litmus_purple_info:
                if self.litmus_pink_info_lit[-1] - self.litmus_purple_secs > 0:
                    img1 = self.crop_frame(self.litmus_purple_info[-2], self.litmus_purple_info[0],
                                           self.litmus_purple_info[3])
                    img2 = self.crop_frame(self.litmus_pink_info_lit[-2], self.litmus_pink_info_lit[0],
                                           self.litmus_pink_info_lit[3])
                    img = np.hstack([img1, img2])
                    self.assignScore(7, img, self.litmus_pink_info_lit[1], self.litmus_pink_info_lit[2], None,
                                     self.litmus_pink_info_lit[4])
            if not self.scorePoint7 and self.litmus_pink_info_lit:
                self.assignScore(7, *self.litmus_pink_info_lit[:5])
        if not self.scorePoint8 and len(self.score_list) > 1:
            if self.seprate_liquid_info:
                self.assignScore(8, *self.seprate_liquid_info[:5])
            elif self.secs - self.last_reaction_secs > 0.2:
                self.assignScore(8, *self.last_frame_info[:5])
        if not self.scorePoint9 and self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:  # 结束前 2s 内有记录
            self.assignScore(9, *self.clearn_desk_info[:5])
        if not self.scorePoint10 and len(self.score_list) > 0:
            self.assignScore(10, *self.last_frame_info[:5])
