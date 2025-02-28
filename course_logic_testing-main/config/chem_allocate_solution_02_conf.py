#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_02_conf.py

CNACLRYPZ02 = {
    'name': '一定溶质质量分数的NaCl溶液配置(托盘天平)(公开课)',
    'experimentId': 'CNACLRYPZ02',
    'isSelect': False,
    'modelPath': 'about_weight/about_weight_7.25.pt',
    'modelClass': 'CHEM_allocate_solution_02',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/chemistry/allocate_solution.png',
    'labelInfo': {
        "手": {"index": 0, "EN": "hand", "conf": 0.6, "max_cn": 4},
        "眼睛": {"index": 1, "EN": "eye", "conf": 0.6, "max_cn": 6},
        "头": {"index": 2, "EN": "head", "conf": 0.6, "max_cn": 4},
        "抹布": {"index": 3, "EN": "duster", "conf": 0.6, "max_cn": 1},
        "电子天平": {"index": 4, "EN": "scale_e", "conf": 0.6, "max_cn": 1},
        "电子天平托盘": {"index": 5, "EN": "salver_e", "conf": 0.6, "max_cn": 1},
        "天平开": {"index": 6, "EN": "scale_on", "sub_labels": ["天平置零", "天平非零"], "conf": 0.6, "max_cn": 1},
        "天平关": {"index": 7, "EN": "scale_off", "conf": 0.6, "max_cn": 1},
        "托盘天平": {"index": 8, "EN": "scale", "conf": 0.6, "max_cn": 1},
        "托盘天平托盘": {"index": 9, "EN": "salver", "conf": 0.6, "max_cn": 2},
        "托盘杆": {"index": 10, "EN": "salver_bar", "conf": 0.6, "max_cn": 2, "visible": False},
        "调平螺母": {"index": 11, "EN": "nut", "conf": 0.5, "max_cn": 2},
        "砝码": {"index": 12, "EN": "weight", "conf": 0.4, "max_cn": 6},
        "砝码盒": {"index": 13, "EN": "weight_box", "conf": 0.6, "max_cn": 2},
        "砝码镊子": {"index": 14, "EN": "tweezer_w", "conf": 0.5, "max_cn": 2},
        "游码": {"index": 15, "EN": "rider", "conf": 0.4, "max_cn": 1},
        "量筒": {"index": 16, "EN": "measuring_cylinder", "conf": 0.5, "max_cn": 2},
        "量筒口": {"index": 17, "EN": "measuring_cylinder_mouth", "conf": 0.6, "max_cn": 2, "visible": False},
        "量筒底": {"index": 18, "EN": "measuring_cylinder_bottom", "conf": 0.6, "max_cn": 2},
        "水柱": {"index": 19, "EN": "water_column", "conf": 0.6, "max_cn": 2},
        "液面": {"index": 20, "EN": "liquid_level", "conf": 0.6, "max_cn": 2, "visible": False},
        "容量瓶": {"index": 21, "EN": "volumetric_flask", "conf": 0.6, "max_cn": 1},
        "容量瓶刻度线": {"index": 22, "EN": "volumetric_flask_line", "conf": 0.6, "max_cn": 1},
        "容量瓶塞": {"index": 23, "EN": "volumetric_flask_stopper", "conf": 0.6, "max_cn": 1},
        "容量瓶肚": {"index": 24, "EN": "volumetric_flask_belly", "conf": 0.6, "max_cn": 1},
        "烧瓶口": {"index": 25, "EN": "flask_mouth", "conf": 0.6, "max_cn": 1},
        "烧瓶肚": {"index": 26, "EN": "flask_belly", "conf": 0.6, "max_cn": 1},
        "金属块": {"index": 27, "EN": "metal_block", "conf": 0.6, "max_cn": 2},
        "橡皮": {"index": 28, "EN": "eraser_block", "conf": 0.6, "max_cn": 2},
        "物块": {"index": 29, "EN": "block", "conf": 0.6, "max_cn": 2},
        "广口瓶": {"index": 30, "EN": "wild_mouth_bottle", "conf": 0.6, "max_cn": 1},
        "广口瓶瓶塞倒放": {"index": 31, "EN": "wild_stopper_upend", "conf": 0.6, "max_cn": 1},
        "广口瓶瓶塞未倒放": {"index": 32, "EN": "wild_stopper_no_upend", "conf": 0.6, "max_cn": 1},
        "细口瓶": {"index": 33, "EN": "narrow_mouth_bottle", "conf": 0.6, "max_cn": 2},
        "细口瓶口": {"index": 34, "EN": "narrow_mouth_bottleneck", "conf": 0.6, "max_cn": 2},
        "细口瓶瓶塞倒放": {"index": 35, "EN": "narrow_stopper_upend", "conf": 0.6, "max_cn": 2},
        "细口瓶瓶塞未倒放": {"index": 36, "EN": "narrow_stopper_no_upend", "conf": 0.6, "max_cn": 2},
        "标签": {"index": 37, "EN": "label", "conf": 0.3, "max_cn": 5},
        "标签纸": {"index": 38, "EN": "label_paper", "conf": 0.6, "max_cn": 1},
        "贴标签": {"index": 39, "EN": "labelling", "conf": 0.6, "max_cn": 1},
        "笔": {"index": 40, "EN": "pen", "conf": 0.6, "max_cn": 2},
        "写字": {"index": 41, "EN": "writting", "conf": 0.6, "max_cn": 1},
        "写标签": {"index": 42, "EN": "write_label", "conf": 0.6, "max_cn": 1},
        "称量纸": {"index": 43, "EN": "weigh_paper", "conf": 0.7, "max_cn": 4},
        "烧杯": {"index": 44, "EN": "beaker", "conf": 0.6, "max_cn": 2},
        "液体": {"index": 45, "EN": "liquid", "conf": 0.5, "max_cn": 2},
        "食盐颗粒": {"index": 46, "EN": "salt_granule", "conf": 0.4, "max_cn": 2},
        "药匙": {"index": 47, "EN": "spoon", "conf": 0.5, "max_cn": 2},
        "药匙勺": {"index": 48, "EN": "spoon_u", "conf": 0.5, "max_cn": 2, "visible": False},
        "玻璃棒": {"index": 49, "EN": "glass_rod", "conf": 0.5, "max_cn": 1},
        "胶头滴管": {"index": 50, "EN": "dropper", "conf": 0.5, "max_cn": 1},
        "滴管头": {"index": 51, "EN": "dropper_h", "conf": 0.5, "max_cn": 1, "visible": False},
        "滴管_透明试剂": {"index": 52, "EN": "dropper_w", "conf": 0.5, "max_cn": 1, "visible": False},
        "滴管_石蕊": {"index": 53, "EN": "dropper_litmus", "conf": 0.5, "max_cn": 1, "visible": False},
        "滴管_预留": {"index": 54, "EN": "dropper_yuliu", "conf": 0.5, "max_cn": 1, "visible": False},
        "大理石": {"index": 55, "EN": "marble", "conf": 0.5, "max_cn": 4},
        "木块": {"index": 56, "EN": "wood_block", "conf": 0.6, "max_cn": 1},
        "酒精灯火焰": {"index": 57, "EN": "alcohol_lamp_flam", "conf": 0.5, "max_cn": 1},
        "酒精灯": {"index": 58, "EN": "alcohol_lamp", "conf": 0.6, "max_cn": 1},
        "酒精灯帽": {"index": 59, "EN": "alcohol_lamp_cap", "conf": 0.6, "max_cn": 1},
        "酒精灯帽摆放错": {"index": 60, "EN": "alcohol_lamp_cap_false", "conf": 0.6, "max_cn": 1},
        "试管": {"index": 61, "EN": "tube", "conf": 0.6, "max_cn": 4},
        "试管口": {"index": 62, "EN": "tube_mouth", "conf": 0.6, "max_cn": 4},
        "试管架": {"index": 63, "EN": "tube_stand", "conf": 0.6, "max_cn": 1},
        "木试管夹": {"index": 64, "EN": "wooden_tube_holder", "conf": 0.6, "max_cn": 1},
        "木试管夹头": {"index": 65, "EN": "wooden_tube_holder_h", "conf": 0.6, "max_cn": 1},
        "铁试管夹": {"index": 66, "EN": "iron_tube_holder", "conf": 0.6, "max_cn": 1},
        "铁试管夹头": {"index": 67, "EN": "iron_tube_holder_h", "conf": 0.6, "max_cn": 1},
        "锥形瓶": {"index": 68, "EN": "conical_flask", "conf": 0.6, "max_cn": 1},
        "锥形瓶口": {"index": 69, "EN": "conical_flask_mouth", "conf": 0.6, "max_cn": 1},
        "长颈漏斗": {"index": 70, "EN": "long_neck_funnel", "conf": 0.6, "max_cn": 1},
        "长颈漏斗U": {"index": 71, "EN": "long_neck_funnel_u", "conf": 0.6, "max_cn": 1},
        "直角短导气管": {"index": 72, "EN": "short_gas_pipe", "conf": 0.6, "max_cn": 1},
        "直角长导气管": {"index": 73, "EN": "long_gas_pipe", "conf": 0.6, "max_cn": 1},
        "导管端头": {"index": 74, "EN": "pipe_end", "conf": 0.6, "max_cn": 3, "visible": False},
        "导管_导管": {"index": 75, "EN": "pipe_pipe", "conf": 0.6, "max_cn": 2, "visible": False},
        "导管接头": {"index": 76, "EN": "pipe_joint", "conf": 0.6, "max_cn": 2, "visible": False},
        "橡胶管": {"index": 77, "EN": "rubber_hose", "conf": 0.6, "max_cn": 1},
        "橡皮塞": {"index": 78, "EN": "rubber_stopper", "conf": 0.6, "max_cn": 2},
        "集气瓶": {"index": 79, "EN": "gas_bottle", "conf": 0.6, "max_cn": 1},
        "集气瓶口": {"index": 80, "EN": "gas_bottle_mouth", "conf": 0.6, "max_cn": 1},
        "毛玻璃片": {"index": 81, "EN": "frosted_glass_plate", "conf": 0.6, "max_cn": 1},
        "澄清透明试剂": {"index": 82, "EN": "clarify_reagent", "conf": 0.6, "max_cn": 2},
        "石灰水浑浊": {"index": 83, "EN": "turbid_whitewash", "conf": 0.6, "max_cn": 1},
        "紫色液体": {"index": 84, "EN": "purple_liquid", "conf": 0.6, "max_cn": 2},
        "粉红液体": {"index": 85, "EN": "pink_liquid", "conf": 0.6, "max_cn": 1},
        "红色液体": {"index": 86, "EN": "red_liquid", "conf": 0.6, "max_cn": 1},
        "纸槽": {"index": 87, "EN": "paper_slot", "conf": 0.6, "max_cn": 1},
        "镊子": {"index": 88, "EN": "tweezer", "conf": 0.6, "max_cn": 1},
        "底座": {"index": 89, "EN": "pedestal", "conf": 0.6, "max_cn": 1},
        "铁杆": {"index": 90, "EN": "iron_pole", "conf": 0.6, "max_cn": 1},
        "铁圈": {"index": 91, "EN": "iron_ring", "conf": 0.6, "max_cn": 1},
        "石棉网": {"index": 92, "EN": "asbestosed_gauze", "conf": 0.6, "max_cn": 1},
        "木条燃烧": {"index": 93, "EN": "wood_burning", "conf": 0.5, "max_cn": 1},
        "木条熄灭": {"index": 94, "EN": "wood_extinguish", "conf": 0.5, "max_cn": 1},
        "火柴盒": {"index": 95, "EN": "matchbox", "conf": 0.6, "max_cn": 1},
        "蜡烛燃烧": {"index": 96, "EN": "candle_burn", "conf": 0.6, "max_cn": 1},
        "蜡烛熄灭": {"index": 97, "EN": "candle_quench", "conf": 0.6, "max_cn": 2},
        "滴瓶": {"index": 98, "EN": "drop_bottle", "conf": 0.6, "max_cn": 1},
        "气体反应": {"index": 99, "EN": "gas_reaction", "sub_labels": ["气泡反应"], "conf": 0.6, "max_cn": 1},
        "未反应": {"index": 100, "EN": "no_reaction", "conf": 0.6, "max_cn": 1},
        "点火器": {"index": 101, "EN": "igniter", "conf": 0.6, "max_cn": 1},
        "洗瓶": {"index": 102, "EN": "wash_bottle", "conf": 0.6, "max_cn": 1},
        "棉花": {"index": 103, "EN": "cotton", "conf": 0.6, "max_cn": 1},
        "试管刷": {"index": 104, "EN": "turn_brush", "conf": 0.6, "max_cn": 1},
        "石蕊试剂": {"index": 105, "EN": "litmus", "conf": 0.6, "max_cn": 1},
        "手握试管": {"index": 106, "EN": "hand_tube", "conf": 0.6, "max_cn": 1},
        "轻拍": {"index": 107, "EN": "pat", "conf": 0.6, "max_cn": 1, "visible": False},
        "废液": {"index": 108, "EN": "liquid_waste", "conf": 0.6, "max_cn": 1},
        "废料": {"index": 109, "EN": "solid_waste", "conf": 0.6, "max_cn": 1},
        "止水夹": {"index": 110, "EN": "flatjaw_pinchcock", "conf": 0.6, "max_cn": 1},
        "试纸": {"index": 111, "EN": "test_paper", "conf": 0.6, "max_cn": 2},
        "固体粉末": {"index": 112, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留113": {"index": 113, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留114": {"index": 114, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留115": {"index": 115, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留116": {"index": 116, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留117": {"index": 117, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留118": {"index": 118, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留119": {"index": 119, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留120": {"index": 120, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留121": {"index": 121, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留122": {"index": 122, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留123": {"index": 123, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留124": {"index": 124, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留125": {"index": 125, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留126": {"index": 126, "EN": "", "conf": 0.6, "max_cn": 1},
        "预留127": {"index": 127, "EN": "", "conf": 0.6, "max_cn": 1},
    },
    'scorePointInfo': {
        '1': {
            'info': '将天平放在水平台面，调节天平平衡',
            'score': 1
        },
        '2': {
            'info': '在两个托盘上放置称量纸',
            'score': 1
        },
        '3': {
            'info': '将游码滑到需要称量的位置(配合砝码)',
            'score': 1
        },
        '4': {
            'info': '取氯化钠固体时瓶塞倒放',
            'score': 1
        },
        '5': {
            'info': '用药匙取氯化钠',
            'score': 1
        },
        '6': {
            'info': '轻拍手腕（或药匙柄）来少量添加氯化钠',
            'score': 1
        },
        '7': {
            'info': '准确称量NaCL至所需量，天平平衡',
            'score': 1
        },
        '8': {
            'info': '向量筒中倾倒蒸馏水，接近至所需量',
            'score': 1
        },
        '9': {
            'info': '量筒水平放置，用胶头滴管逐滴滴加蒸馏水至所需量',
            'score': 1
        },
        '10': {
            'info': '读数时，视线与量筒内液体的凹液面的最低处保持水平',
            'score': 1
        },
        '11': {
            'info': '把量取的蒸馏水全部倒入烧杯中',
            'score': 1
        },
        '12': {
            'info': '在烧杯中溶解NaCl，用玻璃棒搅拌',
            'score': 1
        },
        '13': {
            'info': '将配制好的溶液转移至贴有标签的指定容器中',
            'score': 1
        },
        '14': {
            'info': '清洗仪器，整理桌面',
            'score': 1
        },
    },
    'faultPointInfo': {
        '1': {
            'info': '没有用镊子将游码拨至左侧零位',
            'score': 0
        },
        '2': {
            'info': '没有在天平两侧放置称量纸',
            'score': 0
        },
        '3': {
            'info': '用手直接取砝码',
            'score': 0
        },
        '4': {
            'info': '药品砝码放置错误',
            'score': 0
        },
        '5': {
            'info': '取蒸馏水时瓶塞未倒放',
            'score': 0
        },
        '6': {
            'info': '取氯化钠时瓶塞未倒放',
            'score': 0
        },
        '7': {
            'info': '标签未朝向手心',
            'score': 0
        }
    },
    'modelInfo': {
        "hand": {
            "index": 0,
            "conf": 0.6,
            "CH_name": "手",
            "max_cn": 4
        },
        "eye": {
            "index": 1,
            "conf": 0.6,
            "CH_name": "眼睛",
            "max_cn": 6
        },
        "head": {
            "index": 2,
            "conf": 0.6,
            "CH_name": "头",
            "max_cn": 4
        },
        "duster": {
            "index": 3,
            "conf": 0.6,
            "CH_name": "抹布",
            "max_cn": 1
        },
        "scale_e": {
            "index": 4,
            "conf": 0.6,
            "CH_name": "电子天平",
            "max_cn": 1
        },
        "salver_e": {
            "index": 5,
            "conf": 0.6,
            "CH_name": "托盘",
            "max_cn": 1
        },
        "scale_on": {
            "index": 6,
            "conf": 0.6,
            "CH_name": "天平开",
            "max_cn": 1
        },
        "scale_off": {
            "index": 7,
            "conf": 0.6,
            "CH_name": "天平关",
            "max_cn": 1
        },
        "scale": {
            "index": 8,
            "conf": 0.6,
            "CH_name": "托盘天平",
            "max_cn": 1
        },
        "salver": {
            "index": 9,
            "conf": 0.6,
            "CH_name": "托盘",
            "max_cn": 2
        },
        "salver_bar": {
            "index": 10,
            "conf": 0.6,
            "CH_name": "托盘杆",
            "max_cn": 2,
            "visible": False
        },
        "nut": {
            "index": 11,
            "conf": 0.5,
            "CH_name": "调平螺母",
            "max_cn": 2
        },
        "weight": {
            "index": 12,
            "conf": 0.4,
            "CH_name": "砝码",
            "max_cn": 6
        },
        "weight_box": {
            "index": 13,
            "conf": 0.6,
            "CH_name": "砝码盒",
            "max_cn": 2
        },
        "tweezer_w": {
            "index": 14,
            "conf": 0.5,
            "CH_name": "砝码镊子",
            "max_cn": 2
        },
        "rider": {
            "index": 15,
            "conf": 0.4,
            "CH_name": "游码",
            "max_cn": 1
        },
        "measuring_cylinder": {
            "index": 16,
            "conf": 0.6,
            "CH_name": "量筒",
            "max_cn": 2
        },
        "measuring_cylinder_mouth": {
            "index": 17,
            "conf": 0.5,
            "CH_name": "量筒口",
            "max_cn": 2,
            "visible": False
        },
        "measuring_cylinder_bottom": {
            "index": 18,
            "conf": 0.6,
            "CH_name": "量筒底",
            "max_cn": 2
        },
        "water_column": {
            "index": 19,
            "conf": 0.6,
            "CH_name": "水柱",
            "max_cn": 2
        },
        "liquid_level": {
            "index": 20,
            "conf": 0.6,
            "CH_name": "液面",
            "max_cn": 2,
            "visible": False
        },
        "wild_mouth_bottle": {
            "index": 30,
            "conf": 0.6,
            "CH_name": "广口瓶",
            "max_cn": 2
        },
        "wild_stopper_upend": {
            "index": 31,
            "conf": 0.6,
            "CH_name": "瓶塞倒放",
            "max_cn": 1
        },
        "wild_stopper_no_upend": {
            "index": 32,
            "conf": 0.6,
            "CH_name": "瓶塞未倒放",
            "max_cn": 1
        },
        "narrow_mouth_bottle": {
            "index": 33,
            "conf": 0.6,
            "CH_name": "细口瓶",
            "max_cn": 2
        },
        "narrow_mouth_bottleneck": {
            "index": 34,
            "conf": 0.6,
            "CH_name": "细口瓶口",
            "max_cn": 2
        },
        "narrow_stopper_upend": {
            "index": 35,
            "conf": 0.6,
            "CH_name": "瓶塞倒放",
            "max_cn": 2
        },
        "narrow_stopper_no_upend": {
            "index": 36,
            "conf": 0.6,
            "CH_name": "瓶塞未倒放",
            "max_cn": 2
        },
        "label": {
            "index": 37,
            "conf": 0.3,
            "CH_name": "标签",
            "max_cn": 5
        },
        "label_paper": {
            "index": 38,
            "conf": 0.6,
            "CH_name": "标签纸",
            "max_cn": 1
        },
        "labelling": {
            "index": 39,
            "conf": 0.6,
            "CH_name": "贴标签",
            "max_cn": 1
        },
        "pen": {
            "index": 40,
            "conf": 0.6,
            "CH_name": "笔",
            "max_cn": 2
        },
        "writting": {
            "index": 41,
            "conf": 0.6,
            "CH_name": "写字",
            "max_cn": 1
        },
        "write_label": {
            "index": 42,
            "conf": 0.6,
            "CH_name": "写标签",
            "max_cn": 1
        },
        "weigh_paper": {
            "index": 43,
            "conf": 0.7,
            "CH_name": "称量纸",
            "max_cn": 4
        },
        "beaker": {
            "index": 44,
            "conf": 0.6,
            "CH_name": "烧杯",
            "max_cn": 2
        },
        "liquid": {
            "index": 45,
            "conf": 0.5,
            "CH_name": "液体",
            "max_cn": 2
        },
        "salt_granule": {
            "index": 46,
            "conf": 0.3,
            "CH_name": "食盐颗粒",
            "max_cn": 2
        },
        "spoon": {
            "index": 47,
            "conf": 0.5,
            "CH_name": "药匙",
            "max_cn": 2
        },
        "spoon_u": {
            "index": 48,
            "conf": 0.5,
            "CH_name": "药匙勺",
            "max_cn": 2,
            "visible": False
        },
        "glass_rod": {
            "index": 49,
            "conf": 0.5,
            "CH_name": "玻璃棒",
            "max_cn": 1
        },
        "dropper": {
            "index": 50,
            "conf": 0.5,
            "CH_name": "胶头滴管",
            "max_cn": 1
        },
        "dropper_h": {
            "index": 51,
            "conf": 0.3,
            "CH_name": "滴管头",
            "max_cn": 1,
            "visible": False
        },
        "dropper_w": {
            "index": 52,
            "conf": 0.3,
            "CH_name": "滴管_透明试剂",
            "max_cn": 1,
            "visible": False
        }
    }
}

if __name__ == '__main__':
    for label in CNACLRYPZ02['modelInfo'].keys():
        # print(label + "s_front, ", end='')
        print(label + "s_top, ", end='')

    # print([k['CH_name'] for k in CNACLRYPZ02['modelInfo'].values()])
