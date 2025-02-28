#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/5/12
# @Author  : Qiguangnan
# @File    : chem_co2_produce_property_sz_conf.py


CCO2ZQHXZ_sz = {
    'name': '二氧化碳的实验室制取与性质(深圳锥形瓶)',
    'experimentId': 'CCO2ZQHXZ_sz',
    'isSelect': False,
    'modelPath': 'chem_co2_produce_property/co2_6.6.pt',
    'modelClass': 'CHEM_co2_produce_property_sz',
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
        "大理石": [46, ""],
        "木块": [47, ""],
        "酒精灯火焰": [48, ""],
        "酒精灯": [49, ""],
        "酒精灯帽": [50, ""],
        "酒精灯帽摆放错": [51, ""],
        "试管": [52, ""],
        "试管口": [53, ""],
        "试管架": [54, ""],
        "木试管夹": [55, ""],
        "木试管夹头": [56],
        "铁试管夹": [57],
        "铁试管夹头": [58],
        "纸槽": [59],
        "镊子": [60],
        "底座": [61],
        "铁杆": [62],
        "铁圈": [63],
        "石棉网": [64],
        "直角短导气管": [65],
        "直角长导气管": [66],
        "橡胶管": [67],
        "橡皮塞": [68],
        "集气瓶": [69],
        "集气瓶口": [70],
        "毛玻璃片": [71],
        "木条燃烧": [72],
        "木条熄灭": [73],
        "澄清透明试剂": [74],
        "石灰水浑浊": [75],
        "紫色液体": [76],
        "粉红液体": [77],
        "火柴盒": [78],
        "蜡烛燃烧": [79],
        "蜡烛熄灭": [80],
        "滴瓶": [81],
        "气泡反应": [82],
        "点火器": [83],
        "洗瓶": [84],
        "石蕊试剂": [85],
        "废液": [86],
        "手握试管": [87],
        "导管接头": [88],
        "轻拍": [89],
        "标签纸": [90, "label_paper"],
        "贴标签": [91, "labelling"],
        "笔": [92, "pen"],
        "写字": [93, "writting"],
        '导管端头': [94],
        '导管_导管': [95],
        '锥形瓶': [96],
        '锥形瓶口': [97],
        '长颈漏斗': [98],
        '长颈漏斗U': [99],
        '气体反应': [100],
        '预留61': [101],
        '预留62': [102],
        '预留63': [103],
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
        '预留81': 121,
        '预留82': 122,
        '预留83': 123,
        '预留84': 124,
        '预留85': 125,
        '预留86': 126,
        '预留87': 127
    },
    'scorePointInfo': {
        '1': {
            'info': '能正确选用镊子或药匙取用固体药品',
            'score': 1
        },
        '2': {
            'info': '能正确组装制取CO2的发生和收集装置',
            'score': 1
        },
        '3': {
            'info': '能正确选用稀盐酸',
            'score': 1
        },
        '4': {
            'info': '能从长颈漏斗口加入稀盐酸，直到没过长颈漏斗下端管口（液封）',
            'score': 1
        },
        '5': {
            'info': '能将燃着的木条放在集气瓶口验满并记录',
            'score': 1,
            'type': 2
        },
        '6': {
            'info': '能用灯帽盖灭酒精灯',
            'score': 1
        },
        '7': {
            'info': '能观察紫色石蕊溶液的颜色变化并记录',
            'score': 1,
            'type': 2
        },
        '8': {
            'info': '实验结束，能将固体和液体分开回收',
            'score': 1
        },
        '9': {
            'info': '药品归位、清洗仪器、整理实验台',
            'score': 1
        },
        '10': {
            'info': '讲文明、懂礼貌',
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
        'duster': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'wild_mouth_bottle': {
            'index': 29,
            'conf': 0.5,
            'CH_name': '广口瓶',
            'max_cn': 1
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
        'narrow_mouth_bottleneck': {
            'index': 33,
            'conf': 0.5,
            'CH_name': '细口瓶口',
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
        'liquid': {
            'index': 38,
            'conf': 0.6,
            'CH_name': '液体',
            'max_cn': 2
        },
        'spoon': {
            'index': 40,
            'conf': 0.6,
            'CH_name': '药匙',
            'max_cn': 2
        },
        'spoon_u': {
            'index': 41,
            'conf': 0.6,
            'CH_name': '药匙勺',
            'max_cn': 2
        },
        'beaker': {
            'index': 42,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 4
        },
        'marble': {
            'index': 46,
            'conf': 0.4,
            'CH_name': '大理石',
            'max_cn': 6
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
        'tube_mouth': {
            'index': 53,
            'conf': 0.4,
            'CH_name': '试管口',
            'max_cn': 0
        },
        'tube_stand': {
            'index': 54,
            'conf': 0.5,
            'CH_name': '试管架',
            'max_cn': 2
        },
        'tweezer': {
            'index': 60,
            'conf': 0.4,
            'CH_name': '镊子',
            'max_cn': 1
        },
        'short_gas_pipe': {
            'index': 65,
            'conf': 0.6,
            'CH_name': '直角短管',
            'max_cn': 1
        },
        'long_gas_pipe': {
            'index': 66,
            'conf': 0.6,
            'CH_name': '直角长管',
            'max_cn': 1
        },
        'rubber_hose': {
            'index': 67,
            'conf': 0.6,
            'CH_name': '橡胶管',
            'max_cn': 1
        },
        'rubber_stopper': {
            'index': 68,
            'conf': 0.6,
            'CH_name': '橡皮塞',
            'max_cn': 1
        },
        'gas_bottle': {
            'index': 69,
            'conf': 0.6,
            'CH_name': '集气瓶',
            'max_cn': 1
        },
        'gas_bottle_mouth': {
            'index': 70,
            'conf': 0.6,
            'CH_name': '集气瓶口',
            'max_cn': 1
        },
        'frosted_glass_plate': {
            'index': 71,
            'conf': 0.4,
            'CH_name': '毛玻璃片',
            'max_cn': 1
        },
        'wood_burning': {
            'index': 72,
            'conf': 0.4,
            'CH_name': '木条燃烧',
            'max_cn': 1
        },
        'wood_extinguish': {
            'index': 73,
            'conf': 0.35,
            'CH_name': '木条熄灭',
            'max_cn': 1
        },
        'purple_liquid': {
            'index': 76,
            'conf': 0.4,
            'CH_name': '紫色液体',
            'max_cn': 2
        },
        'pink_liquid': {
            'index': 77,
            'conf': 0.4,
            'CH_name': '粉色液体',
            'max_cn': 1
        },
        'matchbox': {
            'index': 78,
            'conf': 0.5,
            'CH_name': '火柴盒',
            'max_cn': 1
        },
        'liquid_waste': {
            'index': 86,
            'conf': 0.4,
            'CH_name': '废液',
            'max_cn': 1
        },
        'pipe_joint': {
            'index': 88,
            'conf': 0.4,
            'CH_name': '接头',
            'max_cn': 2
        },
        'pipe_end': {
            'index': 94,
            'conf': 0.4,
            'CH_name': '导管端头',
            'max_cn': 3
        },
        'pipe_pipe': {
            'index': 95,
            'conf': 0.4,
            'CH_name': '导管_导管',
            'max_cn': 1
        },
        'conical_flask': {
            'index': 96,
            'conf': 0.6,
            'CH_name': '锥形瓶',
            'max_cn': 1
        },
        'conical_flask_mouth': {
            'index': 97,
            'conf': 0.6,
            'CH_name': '锥形瓶口',
            'max_cn': 1
        },
        'long_neck_funnel': {
            'index': 98,
            'conf': 0.6,
            'CH_name': '长颈漏斗',
            'max_cn': 1
        },
        'long_neck_funnel_u': {
            'index': 99,
            'conf': 0.6,
            'CH_name': '长颈漏斗U',
            'max_cn': 1
        },
        'gas_reaction': {
            'index': 100,
            'conf': 0.55,
            'CH_name': '反应',
            'max_cn': 1
        },
        'solid_waste': {
            'index': 102,
            'conf': 0.6,
            'CH_name': '废料',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(CCO2ZQHXZ_sz['modelInfo'].keys()))
