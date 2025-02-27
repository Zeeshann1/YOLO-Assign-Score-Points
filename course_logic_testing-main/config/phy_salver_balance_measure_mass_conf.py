#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/02/26 15:50
# @Author  : lld
# @File    : phy_salver_balance_measure_mass_conf.py


PTPTPCZL01 = {
    'name': '用托盘天平测量金属块的质量',
    'experimentId': 'PTPTPCZL01',
    'isSelect': False,
    'modelPath': 'phy_salver_balance_measure_mass/phy_salver_balance_measure_mass.pt',
    'modelClass': 'PHY_salver_balance_measure_mass',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/physics/TPTPCZL.jpg',
    'labelInfo': {
        '手': 0,
        '眼睛': 1,
        '头': 2,
        '抹布': 3,
        '电子天平': 4,
        '电子天平托盘': 5,
        '天平开': 6,
        '天平置零': 7,
        '天平关': 8,
        '天平非零': 9,
        '托盘天平': 10,
        '托盘天平托盘': 11,
        '调平螺母': 12,
        '砝码': 13,
        '砝码盒': 14,
        '砝码镊子': 15,
        '游码': 16,
        '金属块': 17,
        '橡皮': 18,
        '物块': 19,
        '容量瓶': 20,
        '容量瓶刻度线': 21,
        '容量瓶塞': 22,
        '容量瓶肚': 23,
        '广口瓶': 24,
        '细口瓶': 25,
        '细口瓶口': 26,
        '瓶塞未倒放': 27,
        '瓶塞倒放': 28,
        '量筒': 29,
        '量筒底': 30,
        '称量纸': 31,
        '水柱': 32,
        '液体': 33,
        '食盐颗粒': 34,
        '药匙': 35,
        '药匙勺': 36,
        '烧杯': 37,
        '玻璃棒': 38,
        '胶头滴管': 39,
        '桌面水': 40,
        "大理石": 41,
        "木块": 42,
        "酒精灯火焰": 43,
        "酒精灯": 44,
        "酒精灯帽": 45,
        "酒精灯帽摆放错": 46,
        "试管": 47,
        "试管口": 48,
        "试管架": 49,
        "木试管夹": 50,
        "木试管夹头": 51,
        "纸槽": 52,
        "镊子": 53,
        "底座": 54,
        "铁杆": 55,
        "铁圈": 56,
        "铁试管夹": 57,
        "铁试管夹头": 58,
        "石棉网": 59,
        "直角短导气管": 60,
        "直角长导气管": 61,
        "橡胶管": 62,
        "橡皮塞": 63,
        "集气瓶": 64,
        "集气瓶口": 65,
        "毛玻璃片": 66,
        "木条燃烧": 67,
        "木条熄灭": 68,
        "澄清透明试剂": 69,
        "石灰水浑浊": 70,
        "紫色液体": 71,
        "粉红液体": 72,
        "火柴盒": 73,
        "标签": 74,
        '蜡烛燃烧': 75,
        '蜡烛熄灭': 76,
        '滴瓶': 77,
        '气泡反应': 78,
        '预留39': 79,
        '预留40': 80,
        '预留41': 81,
        '预留42': 82,
        '预留43': 83,
        '预留44': 84,
        '预留45': 85,
        '预留46': 86,
        '预留47': 87,
        '预留48': 88,
        '预留49': 89,
        '预留50': 90,
        '预留51': 91,
        '预留52': 92,
        '预留53': 93,
        '预留54': 94,
        '预留55': 95,
        '预留56': 96,
        '预留57': 97,
        '预留58': 98,
        '预留59': 99,
        '预留60': 100,
        '预留61': 101,
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
            'info': '用镊子将游码移到标尺的零刻度处。',
            'score': 1
        },
        '2': {
            'info': '并根据指针偏向情况，调节平衡螺母使天平平衡。',
            'score': 1
        },
        '3': {
            'info': '能正确在左盘放被测物，右盘放砝码。',
            'score': 1
        },
        '4': {
            'info': '能用镊子由大到小放置砝码，轻拿轻放。',
            'score': 1
        },
        '5': {
            'info': '称量时会根据指针偏向情况，通过加减砝码或移动游码使天平平衡，并正确读出物体质量的数据。',
            'score': 1
        },
        '6': {
            'info': '实验结束后能及时整理器材。',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '手',
            'max_cn': 2
        },
        'head': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '头',
            'max_cn': 1
        },
        'eye': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '眼睛',
            'max_cn': 2
        },
        'duster': {
            'index': 3,
            'conf': 0.8,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'salver': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '托盘',
            'max_cn': 2
        },
        'weight_tweezer': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '砝码镊子',
            'max_cn': 1
        },
        'nut': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '螺母',
            'max_cn': 2
        },
        'metal_block': {
            'index': 8,
            'conf': 0.7,
            'CH_name': '金属块',
            'max_cn': 3
        },
        'weight': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '砝码',
            'max_cn': 10
        },
        'weight_box': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '砝码盒',
            'max_cn': 1
        },
        'salver_balance': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '托盘天平',
            'max_cn': 1
        },
        'cursor': {
            'index': 12,
            'conf': 0.45,
            'CH_name': '游码',
            'max_cn': 1
        },
    },
    'faultPointInfo': {
        '1': {
            'info': '打点计时器平放地固定在铁架台上',
            'score': 0
        },
        '2': {
            'info': '打点计时器未固定紧',
            'score': 0
        },
        '3': {
            'info': '自由落体运动时，纸带未展平',
            'score': 0
        }
    },
}

if __name__ == '__main__':
    print(list(PTPTPCZL01['modelInfo'].keys()))#打印字典中PTPTPCZL01的标签名字列表
