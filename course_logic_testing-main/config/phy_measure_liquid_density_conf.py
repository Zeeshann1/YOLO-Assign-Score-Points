#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04/22 15:50
# @Author  : lld
# @File    : phy_measure_liquid_density_conf.py


PTPTPCYTMD01 = {
    'name': '测量液体的密度',
    'experimentId': 'PTPTPCYTMD01',
    'isSelect': False,
    #'modelPath': 'phy_measure_metal_density/phy_measure_metal_density.engine',
    'modelPath': 'phy_measure_liquid_density/phy_measure_liquid_density.pt',
    'modelClass': 'PHY_measure_liquid_density',
    'camUse': ['top', 'front', 'side'],
    'imgPath': 'icons/physics/measure_density.png',
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
            'info': '将天平放在水平桌面上，用镊子将游码归零',
            'score': 1
        },
        '2': {
            'info': '调节平衡螺母使天平平衡',
            'score': 1
        },
        '3': {
            'info': '选择小烧杯进行测量',
            'score': 1
        },
        '4': {
            'info': '按照左物右码操作',
            'score': 1
        },
        '5': {
            'info': '从大到小添加游码',
            'score': 1
        },
        '6': {
            'info': '用镊子移动游码，直至天平平衡',
            'score': 1
        },
        '7': {
            'info': '读出烧杯和盐水的总质量m',
            'score': 1 ,
            "type": 1,  # 0,默认;1-qianduan ; 2- suanfapanduan; 3- chuanrutuxiang
        },
        '8': {
            'info': '往量筒中倒入适量的盐水，把量筒放在水平桌面上',
            'score': 1
        },
        '9': {
            'info': '读出量筒中盐水的体积V',
            'score': 1
        },
        '10': {
            'info': '取完盐水后用毛巾将小烧杯外壁擦干;实验结束后能及时整理器材;能和监考老师文明礼貌交流',
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
            'conf': 0.6,
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
            'CH_name': '废液缸',
            'max_cn': 1
        },
        'weight': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '砝码',
            'max_cn': 5
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
            'conf': 0.5,
            'CH_name': '游码',
            'max_cn': 1
        },
        'measuring_cylinder': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '量筒',
            'max_cn': 1
        },
        'cylinder_bottom': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '量筒底',
            'max_cn': 1
        },
        'water_column': {
            'index': 15,
            'conf': 0.6,
            'CH_name': '水柱',
            'max_cn': 1
        },
        'beaker': {
            'index': 16,
            'conf': 0.7,
            'CH_name': '烧杯',
            'max_cn': 1
        },
        'liquid': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '液体',
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
    print(list(PTPTPCYTMD01['modelInfo'].keys()))#打印字典中PTPTPCJSMD01的标签名字列表
