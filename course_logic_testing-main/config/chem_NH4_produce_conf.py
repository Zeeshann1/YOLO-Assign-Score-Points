#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/7/2
# @Author  : Qiguangnan
# @File    : chem_NH4_produce_conf.py


CNH4ZQPQ = {
    'name': '实验室制取氨气并进行喷泉实验',
    'experimentId': 'CNH4ZQPQ',
    'modelPath': 'chem_NH4_produce_fountain/NH4_7.2.pt',
    'modelClass': 'CHEM_nh4_produce_fountain',
    'camUse': ['front', 'top'],
    'imgPath': 'icons/chemistry/co2_produce_property.png',
    'labelInfo': {
        "手": [0, "hand"],
        "眼睛": [1, "eye"],
        "头": [2, "head"],
        "抹布": [3, "duster"],
        "电子天平": [4, ""],
        "电子天平托盘": [5, ""],
        "天平开": [6, ""],
        "天平置零": [7, ""],
        "天平关": [8, ""],
        "天平非零": [9, ""],
        "托盘天平": [10, "scale"],
        "托盘天平托盘": [11, "salver"],
        "托盘杆": [12, "salver_bar"],
        "调平螺母": [13, "nut"],
        "砝码": [14, "weight"],
        "砝码盒": [15, "weight_box"],
        "砝码镊子": [16, "tweezer"],
        "游码": [17, "rider"],
        "金属块": [18, ""],
        "橡皮": [19, ""],
        "物块": [20, ""],
        "容量瓶": [21, ""],
        "容量瓶刻度线": [22, ""],
        "容量瓶塞": [23, ""],
        "容量瓶肚": [24, ""],
        "量筒": [25, "measuring_cylinder"],
        "量筒底": [26, "measuring_cylinder_bottom"],
        "水柱": [27, "water_column"],
        "液面": [28, "liquid_level"],
        "广口瓶": [29, "wild_mouth_bottle"],
        "广口瓶瓶塞未倒放": [30, "wild_stopper_no_upend"],
        "广口瓶瓶塞倒放": [31, "wild_stopper_upend"],
        "细口瓶": [32, "narrow_mouth_bottle"],
        "细口瓶口": [33, "narrow_mouth_bottleneck"],
        "细口瓶瓶塞未倒放": [34, "narrow_stopper_no_upend"],
        "细口瓶瓶塞倒放": [35, "narrow_stopper_upend"],
        "标签": [36, "label"],
        "称量纸": [37, "weigh_paper"],
        "液体": [38, "liquid"],
        "食盐颗粒": [39, "salt_granule"],
        "药匙": [40, "spoon"],
        "药匙勺": [41, "spoon_u"],
        "烧杯": [42, "beaker"],
        "玻璃棒": [43, "glass_rod"],
        "胶头滴管": [44, "dropper"],
        "桌面水": [45, ""],
        "大理石": [46, "marble"],
        "木块": [47, ""],
        "酒精灯火焰": [48, "alcohol_lamp_flam"],
        "酒精灯": [49, "alcohol_lamp"],
        "酒精灯帽": [50, "alcohol_lamp_cap"],
        "酒精灯帽摆放错": [51, "alcohol_lamp_cap_false"],
        "试管": [52, "tube"],
        "试管口": [53, "tube_mouth"],
        "试管架": [54, "tube_stand"],
        "木试管夹": [55, "wooden_tube_holder"],
        "木试管夹头": [56, "wooden_tube_holder_h"],
        "铁试管夹": [57, "iron_tube_holder"],
        "铁试管夹头": [58, "iron_tube_holder_h"],
        "纸槽": [59, "paper_slot"],
        "镊子": [60, "tweezer"],
        "底座": [61, "pedestal"],
        "铁杆": [62, "iron_pole"],
        "铁圈": [63, "iron_ring"],
        "石棉网": [64, "asbestosed_gauze"],
        "直角短导气管": [65, "short_gas_pipe"],
        "直角长导气管": [66, "long_gas_pipe"],
        "橡胶管": [67, "rubber_hose"],
        "橡皮塞": [68, "rubber_stopper"],
        "集气瓶": [69, "gas_bottle"],
        "集气瓶口": [70, "gas_bottle_mouth"],
        "毛玻璃片": [71, "frosted_glass_plate"],
        "木条燃烧": [72, "wood_burning"],
        "木条熄灭": [73, "wood_extinguish"],
        "澄清透明试剂": [74, "clarify_reagent"],
        "石灰水浑浊": [75, "turbid_whitewash"],
        "紫色液体": [76, "purple_liquid"],
        "粉红液体": [77, "pink_liquid"],
        "火柴盒": [78, "matchbox"],
        "蜡烛燃烧": [79],
        "蜡烛熄灭": [80],
        "滴瓶": [81],
        "气泡反应": [82],
        "点火器": [83],
        "洗瓶": [84],
        "石蕊试剂": [85],
        "废液": [86, "liquid_waste"],
        "手握试管": [87],
        "导管接头": [88],
        "轻拍": [89],
        "标签纸": [90, "label_paper"],
        "贴标签": [91, "labelling"],
        "笔": [92, "pen"],
        "写字": [93, "writting"],
        '导管端头': [94, "pipe_end"],
        '导管_导管': [95, "pipe_pipe"],
        '锥形瓶': [96, "conical_flask"],
        '锥形瓶口': [97, "conical_flask_mouth"],
        '长颈漏斗': [98, "long_neck_funnel"],
        '长颈漏斗U': [99, "long_neck_funnel_u"],
        '气体反应': [100, ""],
        '写标签': [101, "write_label"],
        '废料': [102, "solid_waste"],
        '试管刷': [103, "turn_brush"],
        '预留64': [104],
        '预留65': [105],
        '预留66': [106],
        '预留67': [107],
        '预留68': [108],
        '预留69': [109],
        '预留70': [110],
        '预留71': [111],
        '预留72': [112],
        '预留73': [113],
        '预留74': 114,
        '预留75': 115,
        '预留76': 116,
        '预留77': 117,
        '预留78': 118,
        '预留79': 119,
        '预留80': 120,
        '止水夹': [121, ""],
        '红色液体': [122, "red_liquid"],
        '试纸': [123, "test_paper"],
        '烧瓶口': [124, "flask"],
        '烧瓶肚': [125, "flask_belly"],
        '棉花': [126, "cotton"],
        '固体粉末': [127, "solid_powder"]
    },
    'scorePointInfo': {
        '1': {
            'info': '药品取用量恰当',
            'score': 2
        },
        '2': {
            'info': '药品在纸上进行混合',
            'score': 2
        },
        '3': {
            'info': '药品用纸槽送入试管中',
            'score': 2
        },
        '4': {
            'info': '正确组装制取氨气装置',
            'score': 4
        },
        '5': {
            'info': '大试管管口向下倾斜',
            'score': 2
        },
        '6': {
            'info': '加热方法正确',
            'score': 2
        },
        '7': {
            'info': '烧瓶口向下收集氨气',
            'score': 2
        },
        '8': {
            'info': '导管口伸入瓶底',
            'score': 2
        },
        '9': {
            'info': '烧瓶口有棉花',
            'score': 2
        },
        '10': {
            'info': '用湿润的红色石蕊试纸放在瓶口验满',
            'score': 2
        },
        '11': {
            'info': '红色石蕊试纸变蓝',
            'score': 2
        },
        '12': {
            'info': '正确组装喷泉实验装置',
            'score': 3
        },
        '13': {
            'info': '胶头滴管装好水',
            'score': 2
        },
        '14': {
            'info': '烧杯中的水中加入酚酞试液',
            'score': 2
        },
        '15': {
            'info': '喷泉实验成功',
            'score': 3
        },
        '16': {
            'info': '烧瓶中喷入水量超过1/2',
            'score': 2
        },
        '17': {
            'info': '遵守实验室规则',
            'score': 1
        },
        '18': {
            'info': '如实填写实验现象与数据',
            'score': 1
        },
        '19': {
            'info': '器材及时清洗、复位放置',
            'score': 1
        },
        '20': {
            'info': '桌面保持清洁',
            'score': 1
        }
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 0
        },
        'scale': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '电子天平',
            'max_cn': 1
        },
        'salver': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '托盘',
            'max_cn': 1
        },
        'wild_mouth_bottle': {
            'index': 29,
            'conf': 0.5,
            'CH_name': '广口瓶',
            'max_cn': 2
        },
        'wild_stopper_no_upend': {
            'index': 30,
            'conf': 0.5,
            'CH_name': '瓶塞未倒放',
            'max_cn': 2
        },
        'wild_stopper_upend': {
            'index': 31,
            'conf': 0.5,
            'CH_name': '瓶塞倒放',
            'max_cn': 2
        },
        'narrow_mouth_bottle': {
            'index': 32,
            'conf': 0.5,
            'CH_name': '细口瓶',
            'max_cn': 2
        },
        'narrow_stopper_no_upend': {
            'index': 34,
            'conf': 0.5,
            'CH_name': '瓶塞未倒放',
            'max_cn': 2
        },
        'narrow_stopper_upend': {
            'index': 35,
            'conf': 0.5,
            'CH_name': '瓶塞倒放',
            'max_cn': 2
        },
        'weigh_paper': {
            'index': 37,
            'conf': 0.5,
            'CH_name': '称量纸',
            'max_cn': 2
        },
        'liquid': {
            'index': 38,
            'conf': 0.6,
            'CH_name': '液体',
            'max_cn': 3
        },
        'spoon': {
            'index': 40,
            'conf': 0.6,
            'CH_name': '药匙',
            'max_cn': 2
        },
        'beaker': {
            'index': 42,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 3
        },
        'dropper': {
            'index': 44,
            'conf': 0.4,
            'CH_name': '胶头滴管',
            'max_cn': 3
        },
        'alcohol_lamp_flam': {
            'index': 48,
            'conf': 0.5,
            'CH_name': '火焰',
            'max_cn': 1
        },
        'alcohol_lamp': {
            'index': 49,
            'conf': 0.5,
            'CH_name': '酒精灯',
            'max_cn': 1
        },
        'alcohol_lamp_cap': {
            'index': 50,
            'conf': 0.5,
            'CH_name': '酒精灯帽',
            'max_cn': 1
        },
        'alcohol_lamp_cap_false': {
            'index': 51,
            'conf': 0.5,
            'CH_name': '酒精灯帽摆放错',
            'max_cn': 1
        },
        'tube': {
            'index': 52,
            'conf': 0.4,
            'CH_name': '试管',
            'max_cn': 0
        },
        'iron_tube_holder': {
            'index': 57,
            'conf': 0.4,
            'CH_name': '试管夹',
            'max_cn': 2
        },
        'iron_tube_holder_h': {
            'index': 58,
            'conf': 0.4,
            'CH_name': '试管夹头',
            'max_cn': 2
        },
        'paper_slot': {
            'index': 59,
            'conf': 0.4,
            'CH_name': '纸槽',
            'max_cn': 2
        },
        'pedestal': {
            'index': 61,
            'conf': 0.4,
            'CH_name': '底座',
            'max_cn': 2
        },
        'rubber_hose': {
            'index': 67,
            'conf': 0.6,
            'CH_name': '橡胶管',
            'max_cn': 2
        },
        'rubber_stopper': {
            'index': 68,
            'conf': 0.6,
            'CH_name': '橡皮塞',
            'max_cn': 2
        },
        'pipe_joint': {
            'index': 88,
            'conf': 0.4,
            'CH_name': '接头',
            'max_cn': 4
        },
        'pipe_end': {
            'index': 94,
            'conf': 0.3,
            'CH_name': '导管端头',
            'max_cn': 4
        },
        'flatjaw_pinchcock': {
            'index': 121,
            'conf': 0.4,
            'CH_name': '止水夹',
            'max_cn': 1
        },
        'red_liquid': {
            'index': 122,
            'conf': 0.7,
            'CH_name': '红色液体',
            'max_cn': 1
        },
        'test_paper': {
            'index': 123,
            'conf': 0.3,
            'CH_name': '试纸',
            'max_cn': 3
        },
        'flask_mouth': {
            'index': 124,
            'conf': 0.4,
            'CH_name': '烧瓶口',
            'max_cn': 1
        },
        'flask_belly': {
            'index': 125,
            'conf': 0.65,
            'CH_name': '烧瓶',
            'max_cn': 1
        },
        'cotton': {
            'index': 126,
            'conf': 0.6,
            'CH_name': '棉花',
            'max_cn': 3
        },
        'solid_powder': {
            'index': 127,
            'conf': 0.7,
            'CH_name': '固体粉末',
            'max_cn': 2
        },
    }
}

if __name__ == '__main__':
    print(list(CNH4ZQPQ['modelInfo'].keys()))
    print([value['CH_name'] for value in CNH4ZQPQ['modelInfo'].values()])