#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_sz_conf.py

CNACLRYPZ_sz = {
    'name': '配制100g 3%的NaCl溶液(深圳)',
    'experimentId': 'CNACLRYPZ_sz',
    'isSelect': False,
    'modelPath': 'about_weight/about_weight_6.6.pt',
    'modelClass': 'CHEM_allocate_solution_sz',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/chemistry/allocate_solution.png',
    'labelInfo': {
    "手": 0,
    "眼睛": 1,
    "头": 2,
    "抹布": 3,
    "电子天平": 4,
    "电子天平托盘": 5,
    "天平开": 6,
    "天平置零": 7,
    "天平关": 8,
    "天平非零": 9,
    "托盘天平": 10,
    "托盘天平托盘": 11,
    "托盘杆": 12,
    "调平螺母": 13,
    "砝码": 14,
    "砝码盒": 15,
    "砝码镊子": 16,
    "游码": 17,
    "金属块": 18,
    "橡皮": 19,
    "物块": 20,
    "容量瓶": 21,
    "容量瓶刻度线": 22,
    "容量瓶塞": 23,
    "容量瓶肚": 24,
    "量筒": 25,
    "量筒底": 26,
    "水柱": 27,
    "液面": 28,
    "广口瓶": 29,
    "广口瓶瓶塞未倒放": 30,
    "广口瓶瓶塞倒放": 31,
    "细口瓶": 32,
    "细口瓶口": 33,
    "细口瓶瓶塞未倒放": 34,
    "细口瓶瓶塞倒放": 35,
    "标签": 36,
    "称量纸": 37,
    "液体": 38,
    "食盐颗粒": 39,
    "药匙": 40,
    "药匙勺": 41,
    "烧杯": 42,
    "玻璃棒": 43,
    "胶头滴管": 44,
    "桌面水": 45,
    "大理石": 46,
    "木块": 47,
    "酒精灯火焰": 48,
    "酒精灯": 49,
    "酒精灯帽": 50,
    "酒精灯帽摆放错": 51,
    "试管": 52,
    "试管口": 53,
    "试管架": 54,
    "木试管夹": 55,
    "木试管夹头": 56,
    "铁试管夹": 57,
    "铁试管夹头": 58,
    "纸槽": 59,
    "镊子": 60,
    "底座": 61,
    "铁杆": 62,
    "铁圈": 63,
    "石棉网": 64,
    "直角短导气管": 65,
    "直角长导气管": 66,
    "橡胶管": 67,
    "橡皮塞": 68,
    "集气瓶": 69,
    "集气瓶口": 70,
    "毛玻璃片": 71,
    "木条燃烧": 72,
    "木条熄灭": 73,
    "澄清透明试剂": 74,
    "石灰水浑浊": 75,
    "紫色液体": 76,
    "粉红液体": 77,
    "火柴盒": 78,
    "蜡烛燃烧": 79,
    "蜡烛熄灭": 80,
    "滴瓶": 81,
    "气泡反应": 82,
    "点火器": 83,
    "洗瓶": 84,
    "石蕊试剂": 85,
    "废液缸": 86,
    "手握试管": 87,
    "导管接头": 88,
    "轻拍": 89,
    "标签纸": 90,
    "贴标签": 91,
    "笔": 92,
    "写字": 93,
    '导管端头': 94,
    '导管_导管': 95,
    '锥形瓶': 96,
    '锥形瓶口': 97,
    '长颈漏斗': 98,
    '长颈漏斗U': 99,
    '气体反应': 100,
    '写标签': 101,
    '预留62': 102,
    '预留63': 103,
    '预留64': 104,
    '预留65': 105,
    '预留66': 106,
    '预留67': 107,
    '预留68': 108,
    '预留69': 109,
    '预留70': 110,
    '预留71': 111,
    '预留72': 112,
    '预留73': 113,
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
            'info': '能正确计算并填写NaCl的质量和H2O的体积',
            'score': 1,
            'type': 1,
        },
        '2': {
            'info': '能选用100 mL量筒量取液体',
            'score': 1
        },
        '3': {
            'info': '取用水时能瓶塞倒放',
            'score': 1
        },
        '4': {
            'info': '能正确使用胶头滴管定容',
            'score': 1
        },
        '5': {
            'info': '能平视凹液面最低处',
            'score': 1,
            'type': 2,
        },
        '6': {
            'info': '能选用玻璃棒搅拌',
            'score': 1
        },
        '7': {
            'info': '能正确使用玻璃棒搅拌',
            'score': 1
        },
        '8': {
            'info': '能正确书写标签内容',
            'score': 1,
            'type': 1,
        },
        '9': {
            'info': '药品归位、清洗仪器、整理实验台',
            'score': 1
        },
        '10': {
            'info': '讲文明、懂礼貌',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 4
        },
        'eye': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '眼睛',
            'max_cn': 4
        },
        'head': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '头',
            'max_cn': 4
        },
        'duster': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'measuring_cylinder': {
            'index': 25,
            'conf': 0.6,
            'CH_name': '量筒',
            'max_cn': 2
        },
        'measuring_cylinder_bottom': {
            'index': 26,
            'conf': 0.6,
            'CH_name': '量筒底',
            'max_cn': 2
        },
        'water_column': {
            'index': 27,
            'conf': 0.6,
            'CH_name': '水柱',
            'max_cn': 1
        },
        'liquid_level': {
            'index': 28,
            'conf': 0.6,
            'CH_name': '液面',
            'max_cn': 1
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
            'conf': 0.6,
            'CH_name': '瓶塞未倒放',
            'max_cn': 2
        },
        'narrow_stopper_upend': {
            'index': 35,
            'conf': 0.6,
            'CH_name': '瓶塞倒放',
            'max_cn': 2
        },
        'label': {
            'index': 36,
            'conf': 0.3,
            'CH_name': '标签',
            'max_cn': 5
        },
        'liquid': {
            'index': 38,
            'conf': 0.5,
            'CH_name': '液体',
            'max_cn': 2
        },
        'salt_granule': {
            'index': 39,
            'conf': 0.3,
            'CH_name': '食盐颗粒',
            'max_cn': 1
        },
        'beaker': {
            'index': 42,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 2
        },
        'glass_rod': {
            'index': 43,
            'conf': 0.4,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'dropper': {
            'index': 44,
            'conf': 0.45,
            'CH_name': '胶头滴管',
            'max_cn': 1
        },
        'label_paper': {
            'index': 90,
            'conf': 0.4,
            'CH_name': '标签纸',
            'max_cn': 2
        },
        'labelling': {
            'index': 91,
            'conf': 0.7,
            'CH_name': '贴标签',
            'max_cn': 1
        },
        'pen': {
            'index': 92,
            'conf': 0.4,
            'CH_name': '笔',
            'max_cn': 2
        },
        'writing': {
            'index': 93,
            'conf': 0.4,
            'CH_name': '写字',
            'max_cn': 1
        },
        'write_label': {
            'index': 101,
            'conf': 0.6,
            'CH_name': '写标签',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    # print(CNACLRYPZ01['modelInfo'].keys())
    print([k['CH_name'] for k in CNACLRYPZ_sz['modelInfo'].values()])
