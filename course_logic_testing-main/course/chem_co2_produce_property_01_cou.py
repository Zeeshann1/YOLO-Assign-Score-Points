# -*- coding: utf-8 -*-
# @Time    : 2022/3/1 10:37
# @Author  : Qiguangnan
# @File    : chem_co2_produce_property_01_cou.py

'''
二氧化碳的制取和性质(试管)
'''

from .comm import *
from copy import deepcopy


class CHEM_co2_produce_property_01(ConfigModel):

    def __init__(self):
        super(CHEM_co2_produce_property_01, self).__init__()
        self.init_flag = False
        if not self.init_flag:
            self.initScore()
            self.init_flag = True

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

        self.faultPoint1 = False
        self.faultPoint2 = False
        self.faultPoint3 = False
        self.faultPoint4 = False
        self.faultPoint5 = False
        self.faultPoint6 = False
        self.faultPoint7 = False
        self.faultPoint8 = False

        self.init_check_gas_tightness()  # 初始化检验气密性(导气管伸入水中，手握试管)
        self.init_tweezer_marble()  # 初始化用镊子夹取大理石
        self.init_tube_slow_up()  # 初始化试管加入大理石缓慢竖起
        self.init_pour_hcl_to_tube()  # 初始化向试管中加入稀盐酸
        self.init_tighten_rubber_stopper()  # 初始化塞紧橡胶塞
        self.init_tube_v_restriction()  # 初始化试管内液体体积限制
        self.init_tube_holder_distance()  # 初始化试管夹距离
        self.init_collect_gas()  # 初始化收集二氧化碳
        self.init_check_gas_fill()  # 初始化验满
        self.init_gas_fill()  # 初始化已验满
        self.init_gas_bottle_up()  # 初始化集气瓶正放
        self.init_co2_to_lime_water()  # 初始化通入澄清石灰水
        self.init_lime_water_turbid()  # 初始化澄清石灰水变浑浊
        self.init_clearn_desk()  # 初始化整理桌面

        self.init_narrow_stopper_noUpend()  # 初始化细口瓶瓶塞未倒放
        self.init_wild_stopper_noUpend()  # 初始化广口瓶瓶塞未倒放
        self.init_label_no_toward_palm()  # 初始化标签未朝向手心

    def init_check_gas_tightness(self):  # 初始化检验气密性(导气管伸入水中，手握试管)
        # self.hold_tube_secs = 0.  # 手握试管时间
        # self.hold_tube_secs_pre = 0.  # 手握试管时间
        self.tube_rubber_stopper = False  # 试管口有橡皮塞
        self.hold_tube_info_1 = []  # 手握试管信息记录
        self.hold_tube_info_2 = []  # 手握试管信息记录

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
        self.gas_reaction_secs = 0  # 开始反应的时间
        self.gas_reaction_secs_pre = 0  # 开始反应的时间
        self.pour_hcl_info = []

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

    def init_gas_fill(self):  # 初始化已验满
        self.EXTINGUISH_BOTTLE_D_THRE = self.h_front * 0.06
        self.gas_fill_info = []
        self.gas_fill_info_default = []
        self.gas_fill_secs = 0
        self.gas_fill_secs_pre = 0

    def init_gas_bottle_up(self):  # 初始化集气瓶正放
        self.gas_bottle_up_secs = 0
        self.gas_bottle_up_secs_pre = 0

    def init_co2_to_lime_water(self):  # 初始化通入澄清石灰水
        self.co2_limewater_secs = 0
        self.co2_limewater_secs_pre = 0
        self.co2_to_lime_water_flag = False

    def init_lime_water_turbid(self):  # 初始化澄清石灰水变浑浊
        self.lime_water_turbid_secs = 0
        self.lime_water_turbid_secs_pre = 0

    def init_clearn_desk(self):  # 初始化整理桌面
        self.clearn_desk_secs = 0.  # 开始清理桌面秒数
        self.clearn_desk_info = []  # 记录整理桌面的信息

    def init_narrow_stopper_noUpend(self):  # 初始化细口瓶瓶塞未倒放
        self.N_stopper_no_unend_secs = 0
        self.N_stopper_no_unend_secs_pre = 0

    def init_wild_stopper_noUpend(self):  # 初始化广口瓶瓶塞未倒放
        self.W_stopper_no_unend_secs = 0
        self.W_stopper_no_unend_secs_pre = 0

    def init_label_no_toward_palm(self):  # 初始化标签未朝向手心
        self.label_no_tpward_palm_secs = 0
        self.label_no_tpward_palm_secs_pre = 0

    def post_assign(self, index, img, preds, tTime, *args, **kwargs):
        exec(f'self.scorePoint{index} = True')

    def post_retrace(self, index, *args, **kwargs):
        exec(f'self.scorePoint{index} = False')

    def post_error(self, index, *args, **kwargs):
        exec(f'self.faultPoint{index} = True')

    def score_process(self, *args):  # 赋分逻辑部分
        # if not self.init_flag:
        #     self.initScore()
        #     self.init_flag = True

        (hands_top, dusters_top, wild_mouth_bottles_top, wild_stopper_upends_top, wild_stopper_no_upends_top,
         narrow_mouth_bottles_top, narrow_mouth_bottlenecks_top, narrow_stopper_upends_top,
         narrow_stopper_no_upends_top, labels_top, beakers_top, liquids_top, spoons_top, spoon_us_top, droppers_top,
         marbles_top, alcohol_lamp_flams_top, alcohol_lamps_top, alcohol_lamp_caps_top, alcohol_lamp_cap_falses_top,
         tubes_top, tube_mouths_top, tube_stands_top, tube_holder_moods_top, tube_holder_head_moods_top,
         tube_holder_irons_top, tube_holder_head_irons_top, short_gas_pipes_top, long_gas_pipes_top, pipe_ends_top,
         pipe_pipes_top, pipe_joints_top, rubber_hoses_top, rubber_stoppers_top, gas_bottles_top, gas_bottle_mouths_top,
         frosted_glass_plates_top, clarify_reagents_top, turbid_whitewashs_top, purple_liquids_top, pink_liquids_top,
         tweezers_top, bases_top, iron_bars_top, wood_burnings_top, wood_extinguishs_top, candle_burnings_top,
         candle_extinguishs_top, gas_reactions_top, igniters_top, hand_tubes_top) = self.preds_top
        '''
        ['手', '抹布', '广口瓶', '瓶塞倒放', '瓶塞未倒放', 
        '细口瓶', '细口瓶口', '瓶塞倒放', 
        '瓶塞未倒放', '标签', '烧杯', '液体', '药匙', '药匙勺', 
        '胶头滴管', '大理石', '火焰', '酒精灯', '酒精灯帽', '酒精灯帽摆放错', 
        '试管', '试管口', '试管架', '木试管夹', '木试管夹头', 
        '铁夹', '铁夹头', '直角短管', '直角长管', '导管端头', '导管_导管', '导管接头',
         '橡胶管', '橡皮塞', '集气瓶', '集气瓶口', '毛玻璃片', '澄清试剂', '浑石灰水',
          '紫色液体', '粉色液体', '镊子', '底座', '金属杆', '木条燃烧', '木条熄灭', 
          '蜡烛燃烧', '蜡烛熄灭', '反应', '点火器', '手握试管']
        '''
        (hands_front, dusters_front, wild_mouth_bottles_front, wild_stopper_upends_front, wild_stopper_no_upends_front,
         narrow_mouth_bottles_front, narrow_mouth_bottlenecks_front, narrow_stopper_upends_front,
         narrow_stopper_no_upends_front, labels_front, beakers_front, liquids_front, spoons_front, spoon_us_front,
         droppers_front, marbles_front, alcohol_lamp_flams_front, alcohol_lamps_front, alcohol_lamp_caps_front,
         alcohol_lamp_cap_falses_front, tubes_front, tube_mouths_front, tube_stands_front, tube_holder_moods_front,
         tube_holder_head_moods_front, tube_holder_irons_front, tube_holder_head_irons_front, short_gas_pipes_front,
         long_gas_pipes_front, pipe_ends_front, pipe_pipes_front, pipe_joints_front, rubber_hoses_front,
         rubber_stoppers_front, gas_bottles_front, gas_bottle_mouths_front, frosted_glass_plates_front,
         clarify_reagents_front, turbid_whitewashs_front, purple_liquids_front, pink_liquids_front, tweezers_front,
         bases_front, iron_bars_front, wood_burnings_front, wood_extinguishs_front, candle_burnings_front,
         candle_extinguishs_front, gas_reactions_front, igniters_front, hand_tubes_front) = self.preds_front

        if not self.scorePoint1:  # 检查气密性，将导管伸入水中，用手捂试管
            info = self.check_gas_tightness(hand_tubes_front, pipe_ends_front, pipe_pipes_front, hands_front,
                                            beakers_front, liquids_front, long_gas_pipes_front, short_gas_pipes_front,
                                            tubes_front, rubber_stoppers_front, hands_top, rubber_stoppers_top)
            if info is not None:
                self.assignScore(1, *info[:5])
                self.assignScore(2, *info[:5])

        if not self.scorePoint3:  # 用镊子夹取大理石
            info = self.tweezer_marble(3, hands_front, tweezers_front, wild_mouth_bottles_front, marbles_front,
                                       hands_top, tweezers_top, wild_mouth_bottles_top, marbles_top)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint4:  # 试管平放，加入大理石后缓慢竖起，大理石滑落至试管底部
            info = self.tube_slow_up(4, hands_front, tubes_front, tweezers_front, marbles_front)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint5:  # 向试管中加入稀盐酸
            info = self.pour_hcl_to_tube(5, gas_reactions_front, narrow_mouth_bottles_front,
                                         narrow_mouth_bottlenecks_front, tubes_front, tube_mouths_front,
                                         narrow_mouth_bottlenecks_top, tube_mouths_top)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint6:  # 塞紧橡胶塞
            info = self.tighten_rubber_stopper(6, hands_front, gas_reactions_front, tubes_front, rubber_stoppers_front,
                                               tube_holder_head_irons_top, tubes_top, hands_top, rubber_stoppers_top)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint7:  # 试管中液体体积不超过试管容器的1/3
            info = self.tube_v_restriction(7, hands_front, tubes_front, gas_reactions_front)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint8:  # 铁夹夹在距试管口近1/3处
            info = self.tube_holder_distance(hands_front, tubes_front, tube_holder_head_irons_front,
                                             rubber_stoppers_front)
            if info is not None:
                if info[-1]:
                    self.assignScore(8, *info[:5])
                else:
                    self.assignError(4, *info[:5])
                    self.scorePoint8 = True

        if not self.scorePoint9:  # 用向上排气法收集CO2
            info = self.collect_gas(9, rubber_hoses_front, gas_bottles_front, frosted_glass_plates_front,
                                    long_gas_pipes_front)
            if info is not None:
                self.assignScore(*info[:6])

        if self.collect_gas_flag and not self.scorePoint10:  # 点燃木条，将燃着的木条放在集气瓶口验满
            info = self.check_gas_fill(10, wood_burnings_front, gas_bottles_front, gas_bottle_mouths_front,
                                       frosted_glass_plates_front, wood_burnings_top, gas_bottles_top,
                                       frosted_glass_plates_top)
            if info is not None:
                self.assignScore(*info[:6])

        if self.check_gas_fill_flag and not self.scorePoint11:  # 木条熄灭,收集满二氧化碳
            info = self.gas_fill(11, wood_extinguishs_front, gas_bottles_front, gas_bottle_mouths_front,
                                 wood_extinguishs_top, gas_bottles_top, frosted_glass_plates_front, wood_burnings_front,
                                 wood_burnings_top)
            if info is not None:
                self.assignScore(*info[:6])

        if self.collect_gas_flag and not self.scorePoint12:  # 用毛玻璃片磨砂面盖好集气瓶并正放在桌面上
            info = self.gas_bottle_up(12, hands_front, gas_bottles_front, frosted_glass_plates_front,
                                      long_gas_pipes_front,
                                      hands_top, gas_bottles_top, frosted_glass_plates_top,
                                      long_gas_pipes_top)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint13:  # 将二氧化碳通入澄清的石灰水中
            info = self.co2_to_lime_water(13, long_gas_pipes_front, tubes_front)
            if info is not None:
                self.assignScore(*info[:6])

        if not self.scorePoint14:  # 澄清的石灰水变浑浊
            info = self.lime_water_turbid(14, turbid_whitewashs_front, tubes_front, long_gas_pipes_front)
            if info is not None:
                if not self.scorePoint13:
                    self.assignScore(13, *info[1:6])
                self.assignScore(*info[:6])

        items_top = [wild_mouth_bottles_top, wild_stopper_no_upends_top, wild_stopper_upends_top,
                     narrow_mouth_bottles_top, narrow_stopper_no_upends_top,
                     narrow_stopper_upends_top, spoons_top, beakers_top, droppers_top,
                     marbles_top, alcohol_lamp_flams_top, alcohol_lamps_top, alcohol_lamp_caps_top,
                     alcohol_lamp_cap_falses_top,
                     tubes_top, tube_stands_top, tube_holder_moods_top,
                     tube_holder_irons_top, tweezers_top, bases_top,
                     rubber_hoses_top, rubber_stoppers_top, gas_bottles_top,
                     frosted_glass_plates_top, wood_burnings_top, wood_extinguishs_top, clarify_reagents_top,
                     turbid_whitewashs_top,
                     purple_liquids_top, pink_liquids_top, candle_burnings_top, candle_extinguishs_top,
                     igniters_top, ]
        '''
        ['广口瓶', '瓶塞未倒放', '瓶塞倒放', 
        '细口瓶', '瓶塞未倒放', 
        '瓶塞倒放', '药匙', '药匙勺', '烧杯', '胶头滴管', 
        '大理石', '火焰', '酒精灯', '酒精灯帽', '酒精灯帽摆放错', 
        '试管', '试管口', '试管架', '木试管夹',
         '铁夹', '镊子', '底座', '金属杆', 
         '橡胶管', '橡皮塞', '集气瓶', 
         '毛玻璃片', '木条燃烧', '木条熄灭', '澄清试剂', '浑石灰水', 
         '紫色液体', '粉色液体', '蜡烛燃烧', '蜡烛熄灭', '反应', 
         '点火器', '手握试管', '导管接头', '导管端头', '导管_导管']
        '''
        items_front = [wild_mouth_bottles_front, wild_stopper_no_upends_front, wild_stopper_upends_front,
                       narrow_mouth_bottles_front, narrow_stopper_no_upends_front,
                       narrow_stopper_upends_front, spoons_front, beakers_front,
                       droppers_front, marbles_front, alcohol_lamp_flams_front,
                       alcohol_lamp_cap_falses_front, tubes_front, tube_stands_front, tube_holder_moods_front,
                       tube_holder_head_moods_front, tube_holder_irons_front, tube_holder_head_irons_front,
                       tweezers_front,
                       bases_front, iron_bars_front, short_gas_pipes_front, long_gas_pipes_front, rubber_hoses_front,
                       rubber_stoppers_front, gas_bottles_front,
                       wood_burnings_front, wood_extinguishs_front, clarify_reagents_front, turbid_whitewashs_front,
                       purple_liquids_front, pink_liquids_front, candle_burnings_front, candle_extinguishs_front,
                       igniters_front]

        if (not self.scorePoint15 and len(self.score_list) > 5):  # 清洗仪器，整理桌面
            info = self.clearn_desk(15, [items_top, items_front], [self.center_area_top, self.center_area_front])
            if info:
                self.assignScore(*info)
        if self.scorePoint7 and len(self.score_list) != 15:
            if not self.desk_is_clearn([items_top, items_front], [self.center_area_top, self.center_area_front]):
                self.retracementScore(15)

        if not self.faultPoint1:
            info = self.stopperNoUpend(narrow_stopper_upends_front, narrow_stopper_no_upends_front,
                                       narrow_stopper_upends_top, narrow_stopper_no_upends_top)
            if info:
                self.assignError(1, *info[:5])

        if not self.faultPoint2:
            info = self.stopperNoUpend(wild_stopper_upends_front, wild_stopper_no_upends_front,
                                       wild_stopper_upends_top, wild_stopper_no_upends_top)
            if info:
                self.assignError(2, *info[:5])

        if not self.faultPoint3:
            info = self.label_no_toward_palm(hands_front, labels_front)
            if info:
                self.assignError(3, *info[:5])

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

    def check_gas_tightness(self, hand_tubes_front, pipe_ends_front, pipe_pipes_front, hands_front,
                            beakers_front, liquids_front, long_gas_pipes_front, short_gas_pipes_front,
                            tubes_front, rubber_stoppers_front, hands_top, rubber_stoppers_top):
        '''
        检验气密性：(导管伸入水中，用手捂住试管)橡皮塞
        :return:
        '''
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
            self.update_info_list(self.hold_tube_info_1)
            if self.hold_tube_info_2:
                self.hold_tube_info_2[-1][-1] = self.secs
        if hold_tube_2:
            self.update_info_list(self.hold_tube_info_2)

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

    def tweezer_marble(self, score_index, hands_front, tweezers_front, wild_mouth_bottles_front, marbles_front,
                       hands_top, tweezers_top, wild_mouth_bottles_top, marbles_top):
        '''
        用镊子夹取大理石
        :param score_index: 得分点索引
        :param hands_front: 前视手
        :param tweezers_front: 前视镊子
        :param wild_mouth_bottles_front: 前视广口瓶
        :param marbles_front: 前视大理石
        :param hands_top: 顶视手
        :param tweezers_top: 顶视镊子
        :param wild_mouth_bottles_top: 顶视广口瓶
        :param marbles_top: 顶视大理石
        :return:
        '''
        record = False
        if tweezers_front.shape[0] == 1 and hands_front.shape[0] > 0:
            tweezer_front_box = tweezers_front[0][:4]
            for hand_front in hands_front:
                hand_front_box = hand_front[:4]
                if (pt_in_polygon(center_point(hand_front_box), self.center_area_front)
                        and iou(hand_front_box, tweezer_front_box) > 0):
                    if wild_mouth_bottles_front.shape[0] > 0:
                        wild_mouth_bottle_front_box = wild_mouth_bottles_front[0][:4]
                        if (iou(wild_mouth_bottle_front_box, tweezer_front_box) > 0
                                and center_distance_v(wild_mouth_bottle_front_box, tweezer_front_box) > 0):
                            record = 'front'
                    if not record and marbles_front.shape[0] > 0:
                        marble_front_box = marbles_front[0][:4]
                        if iou(marble_front_box, tweezer_front_box) > 0:
                            record = 'front'
        if not record and tweezers_top.shape[0] > 0 and hands_top.shape[0] > 0:
            tweezer_top_box = tweezers_top[0][:4]
            for hand_top in hands_top:
                hand_top_box = hand_top[:4]
                if iou(hand_top_box, tweezer_top_box) > 0:
                    if wild_mouth_bottles_top.shape[0] > 0:
                        wild_mouth_bottle_top_box = wild_mouth_bottles_top[0][:4]
                        if iou(wild_mouth_bottle_top_box, tweezer_top_box):
                            record = 'top'
                    if not record and marbles_top.shape[0] > 0:
                        marble_top_box = marbles_top[0][:4]
                        if iou(marble_top_box, tweezer_top_box) > 0:
                            record = 'top'
        if record:
            if self.tweezer_marble_curr_num < self.tweezer_marble_thre_num:
                self.tweezer_marble_curr_num += 1
            else:
                if record == 'top':
                    tweezer_marble_info = [score_index, self.frame_top, self.time_top, self.objects_top,
                                           self.preds_top, self.num_frame_top]
                else:
                    tweezer_marble_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                           self.preds_front, self.num_frame_front]
                return tweezer_marble_info

    def tube_slow_up(self, score_index, hands_front, tubes_front, tweezers_front, marbles_front):  # 试管水平
        '''
        试管平放加入大理石，缓慢竖起
        :param score_index: 得分点索引
        :param hands_front: 前视手
        :param tubes_front: 前视试管
        :param tweezers_front: 前视镊子
        :param marbles_front: 前视大理石
        :return:
        '''
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
        '''
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
        '''
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
        '''
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
        '''
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
        '''
        试管中液体体积不超过试管容器的1/3
        :param score_index:
        :param hands_front:前视手
        :param tubes_front:前视试管
        :param gas_reactions_front:前视反应
        :return:
        '''
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

    def tube_holder_distance(self, hands_front, tubes_front, tube_holder_head_irons_front,
                             rubber_stoppers_front):
        '''
        判断试管夹距试管口距离 1/2
        :param hands_front: 前视手
        :param tubes_front: 前视试管
        :param tube_holder_head_irons_front: 前视铁试管夹头
        :param rubber_stoppers_front: 前视橡胶塞
        :return:
        '''
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
                        if len(self.tube_holder_d_list) == 20:
                            if sum(self.tube_holder_d_list[-10:]) / 10 < self.TUBE_HOLDER_D:
                                flag = True
                            else:
                                flag = False
                            return [self.frame_front, self.time_front, self.objects_front,
                                    self.preds_front, self.num_frame_front, flag]

    def collect_gas(self, score_index, rubber_hoses_front, gas_bottles_front, frosted_glass_plates_front,
                    long_gas_pipes_front):
        '''
        向上排气法收集二氧化碳气体
        :param score_index:
        :param rubber_hoses_front: 橡胶管
        :param gas_bottles_front: 集气瓶
        :param frosted_glass_plates_front: 毛玻璃片
        :param long_gas_pipes_front:  直角长导管
        :return:
        '''
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

    def check_gas_fill(self, score_index, wood_burnings_front, gas_bottles_front, gas_bottle_mouths_front,
                       frosted_glass_plates_front, wood_burnings_top, gas_bottles_top, frosted_glass_plates_top):
        '''
        验满 将燃着的木条放在集气瓶口验满
        :param score_index:
        :param wood_burnings_front: 前视燃着的木条
        :param gas_bottles_front: 前视集气瓶
        :param gas_bottle_mouths_front: 前视集气瓶口
        :param frosted_glass_plates_front: 前视毛玻璃片
        :param wood_burnings_top: 顶视燃着的木条
        :param gas_bottles_top: 顶视集气瓶
        :param frosted_glass_plates_top: 顶视毛玻璃片
        :return:
        '''
        if (wood_burnings_front.shape[0] == 1
                and (gas_bottles_front.shape[0] + gas_bottle_mouths_front.shape[0] > 0)):
            # and frosted_glass_plates_front.shape[0] == 1
            # frosted_glass_plate_front_box = frosted_glass_plates_front[0][:4]
            gas_bottle_mouth_front_box = self.get_gas_bottle_mouth_front_box(gas_bottles_front,
                                                                             gas_bottle_mouths_front)  # 集气瓶口
            wood_burning_front_box = wood_burnings_front[0][:4]

            if min_dis_boxes(wood_burning_front_box, gas_bottle_mouth_front_box) < self.BUTN_BOTTLE_D_THRE:
                self.check_gas_fill_flag = True
                return [score_index, self.frame_front, self.time_front, self.objects_front,
                        self.preds_front, self.num_frame_front]
        elif wood_burnings_top.shape[0] == 1 and gas_bottles_top.shape[0] == 1:
            wood_burning_top_box = wood_burnings_top[0][:4]
            gas_bottle_top_box = gas_bottles_top[0][:4]
            if iou(gas_bottle_top_box, wood_burning_top_box) > 0:
                self.check_gas_fill_flag = True
                return [score_index, self.frame_top, self.time_top, self.objects_top,
                        self.preds_top, self.num_frame_top]

    @staticmethod
    def get_gas_bottle_mouth_front_box(gas_bottles_front, gas_bottle_mouths_front):
        if gas_bottle_mouths_front.shape[0] == 1:
            return gas_bottle_mouths_front[0][:4]
        if gas_bottles_front.shape[0] == 1:
            gas_bottle_mouth_front_box = deepcopy(gas_bottles_front[0][:4])
            gas_bottle_mouth_front_box[3] = gas_bottle_mouth_front_box[1] + (
                    gas_bottle_mouth_front_box[3] - gas_bottle_mouth_front_box[1]) * 0.25
            return gas_bottle_mouths_front

    def gas_fill(self, score_index, wood_extinguishs_front, gas_bottles_front, gas_bottle_mouths_front,
                 wood_extinguishs_top, gas_bottles_top, frosted_glass_plates_front, wood_burnings_front,
                 wood_burnings_top):
        '''
        木条熄灭，收集满二氧化碳
        :param score_index:
        :param wood_extinguishs_front: 前视木条熄灭
        :param gas_bottles_front: 前视集气瓶
        :param gas_bottle_mouths_front: 前视集气瓶口
        :param wood_extinguishs_top: 顶视木条熄灭
        :param gas_bottles_top: 顶视集气瓶
        :param frosted_glass_plates_front: 前视毛玻璃片
        :param wood_burnings_front: 前视木条燃烧
        :param wood_burnings_top: 顶视木条燃烧
        :return:
        '''
        if wood_extinguishs_front.shape[0] == 1:  # 前视木条熄灭
            wood_extinguish_front_box = wood_extinguishs_front[0][:4]
            if gas_bottles_front.shape[0] + gas_bottle_mouths_front.shape[0] > 0:  # 集气瓶
                gas_bottle_mouth_front_box = self.get_gas_bottle_mouth_front_box(gas_bottles_front,
                                                                                 gas_bottle_mouths_front)  # 集气瓶口
                if min_dis_boxes(wood_extinguish_front_box, gas_bottle_mouth_front_box) < self.EXTINGUISH_BOTTLE_D_THRE:
                    self.gas_fill_info = [score_index, self.frame_front, self.time_front, self.objects_front,
                                          self.preds_front, self.num_frame_front, self.secs]
        if not self.gas_fill_info and wood_extinguishs_top.shape[0] == 1 and gas_bottles_top.shape[0] == 1:  # 顶视
            wood_extinguish_top_box = wood_extinguishs_top[0][:4]
            gas_bottle_top_box = gas_bottles_top[0][:4]
            if iou(wood_extinguish_top_box, gas_bottle_top_box) > 0:
                self.gas_fill_info = [score_index, self.frame_top, self.time_top, self.objects_top,
                                      self.preds_top, self.num_frame_top, self.secs]
        if self.gas_fill_info and self.secs - self.gas_fill_info[-1] > 2:
            return self.gas_fill_info[:6]
        if not self.gas_fill_info:
            if wood_burnings_front.shape[0] == 0 and wood_burnings_top.shape[0] == 0:  # 没有检测到木条燃烧
                if not self.gas_fill_info_default:
                    self.gas_fill_info_default = [score_index, self.frame_front, self.time_front, self.objects_front,
                                                  self.preds_front, self.num_frame_front, self.secs]
                self.gas_fill_secs, self.gas_fill_secs_pre, flag = self.duration(self.gas_fill_secs,
                                                                                 5,
                                                                                 self.gas_fill_secs_pre,
                                                                                 2)
                if flag:
                    return self.gas_fill_info_default
            else:
                self.init_gas_fill()

    def gas_bottle_up(self, score_index,
                      hands_front, gas_bottles_front, frosted_glass_plates_front,
                      long_gas_pipes_front,
                      hands_top, gas_bottles_top, frosted_glass_plates_top,
                      long_gas_pipes_top
                      ):
        '''
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
        '''
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

    def co2_to_lime_water(self, score_index, long_gas_pipes_front, tubes_front):
        '''
        二氧化碳通入澄清石灰水
        :param score_index:
        :param long_gas_pipes_front: # 长导管
        :param tubes_front:  # 试管
        :return:
        '''
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
        '''
        澄清石灰水变浑浊
        :param score_index:
        :param turbid_whitewashs_front: # 前视石灰水浑浊
        :param tubes_front: # 前视试管
        :param long_gas_pipes_front: # 前视直角长导管
        :return:
        '''
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

    def update_info_list(self, info_list, view='front', step=1.):
        '''
        更新记录信息
        :param score_index: 得分点列表
        :param info_list: 记录信息列表
        :param view: 视角
        :param step: 间隔时长
        :return:
        '''
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
                info_list.append([self.frame_front, self.time_front, self.objects_front,
                                  self.preds_front, self.num_frame_front, self.secs])
            else:
                info_list.append([self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                  self.num_frame_top, self.secs])
        return info_list

    def crop_frame(self, box, frame, preds):
        x = int(center_point(box)[0])
        if x < self.w_front / 4:
            x1, x2 = 0, int(self.w_front / 2)
        elif x < (self.w_front / 4) * 3:
            x1, x2 = int(x - self.w_front / 4), int(x + self.w_front / 4)
        else:
            x1, x2 = int(self.w_front / 2), int(self.w_front)
        self.plot(preds, frame)
        return frame[:, x1:x2, :]

    def clearn_desk(self, score_index, items_views, center_area_views):
        '''
        整理桌面
        :param score_index: 得分点索引
        :param items_views: 所用视角目标
        :param center_area_views: 所用视角操作区域
        :return:
        '''
        if self.desk_is_clearn(items_views, center_area_views):
            self.clearn_desk_info = [score_index, self.frame_top, self.time_top, self.objects_top, self.preds_top,
                                     self.num_frame_top, self.secs]
            self.clearn_desk_secs, _, flag = self.duration(self.clearn_desk_secs, 2)
            if flag:
                self.clearn_desk_secs = 0
                return self.clearn_desk_info[:6]
        else:
            self.clearn_desk_secs = 0

    def end(self):  # 实验结束时判断是否整理桌面，如果有 赋分
        if self.clearn_desk_info and self.secs - self.clearn_desk_info[-1] < 2.:  # 结束前 2s 内有记录
            self.assignScore(*self.clearn_desk_info[:6])
