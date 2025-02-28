#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 09:42
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_04_conf.py


CNACLRYPZ04 = {
    'name': '一定溶质质量分数的NaCl溶液的配制(稀释)',
    'experimentId': 'CNACLRYPZ04',
    'modelPath': 'about_weight/about_weight_2.18.pt',
    'modelClass': 'CHEM_allocate_solution_04',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/chemistry/allocate_solution.png',
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
        '点火器': 79,
        '石蕊试剂': 80,
        '洗瓶': 81,
        '废液缸': 82,
        '托盘杆': 83,
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
    'faultPointInfo': {
        '1': {
            'info': '瓶塞放置错误',
            'score': 0
        },
        '2': {
            'info': '读取示数时眼睛要平视液面',
            'score': 0
        },
        '3': {
            'info': '',
            'score': 0
        }
    },
    'scorePointInfo': {
        '1': {
            'info': '向量筒中倾倒所需的氯化钠溶液至规定体积或接近规定体积；若接近规定体积，将量筒水平放置，用胶头滴管逐滴滴加至规定体积',
            'score': 1
        },
        '2': {
            'info': '把量取的氯化钠溶液全部倒入烧杯中',
            'score': 1
        },
        '3': {
            'info': '向量筒中倾倒蒸馏水至规定体积或接近规定体积；若接近规定体积，将量筒水平放置，用胶头滴管逐滴滴加蒸馏水至规定体积',
            'score': 1
        },
        '4': {
            'info': '把量取的蒸馏水也全部倒入烧杯中',
            'score': 1
        },
        '5': {
            'info': '用玻璃棒搅拌，混匀',
            'score': 1
        },
        '6': {
            'info': '将所得的溶液转移到指定容器中',
            'score': 1
        },
        '7': {
            'info': '清洗仪器，整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'eye': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '眼睛',
            'max_cn': 6
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
        'scale': {
            'index': 4,
            'conf': 0.6,
            'CH_name': '电子天平',
            'max_cn': 1
        },
        'salver': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '电子天平托盘',
            'max_cn': 2
        },
        'scale_on': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '天平开',
            'max_cn': 1
        },
        'scale_zero': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '天平置零',
            'max_cn': 1
        },
        'scale_off': {
            'index': 8,
            'conf': 0.6,
            'CH_name': '天平关',
            'max_cn': 1
        },
        'scale_not_zero': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '天平非零',
            'max_cn': 1
        },
        'wild_mouth_bottle': {
            'index': 24,
            'conf': 0.6,
            'CH_name': '广口瓶',
            'max_cn': 1
        },
        'narrow_mouth_bottle': {
            'index': 25,
            'conf': 0.5,
            'CH_name': '细口瓶',
            'max_cn': 2
        },
        'narrow_mouth_bottleneck': {
            'index': 26,
            'conf': 0.5,
            'CH_name': '细口瓶口',
            'max_cn': 2
        },
        'stopper_up': {
            'index': 27,
            'conf': 0.6,
            'CH_name': '瓶塞未倒放',
            'max_cn': 1
        },
        'stopper_down': {
            'index': 28,
            'conf': 0.6,
            'CH_name': '瓶塞倒放',
            'max_cn': 1
        },
        'measuring_cylinder': {
            'index': 29,
            'conf': 0.6,
            'CH_name': '量筒',
            'max_cn': 1
        },
        'measuring_cylinder_bottom': {
            'index': 30,
            'conf': 0.6,
            'CH_name': '量筒底',
            'max_cn': 1
        },
        'water_column': {
            'index': 32,
            'conf': 0.5,
            'CH_name': '水柱',
            'max_cn': 1
        },
        'liquid': {
            'index': 33,
            'conf': 0.5,
            'CH_name': '液体',
            'max_cn': 1
        },
        'salt_granule': {
            'index': 34,
            'conf': 0.3,
            'CH_name': '食盐颗粒',
            'max_cn': 3
        },
        'spoon': {
            'index': 35,
            'conf': 0.5,
            'CH_name': '药匙',
            'max_cn': 1
        },
        'spoon_u': {
            'index': 36,
            'conf': 0.5,
            'CH_name': '药匙勺',
            'max_cn': 1
        },
        'beaker': {
            'index': 37,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 38,
            'conf': 0.5,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'dropper': {
            'index': 39,
            'conf': 0.5,
            'CH_name': '胶头滴管',
            'max_cn': 1
        },
        'label': {
            'index': 74,
            'conf': 0.3,
            'CH_name': '标签',
            'max_cn': 5
        },
    }
}

if __name__ == '__main__':
    # print(CNACLRYPZ03['modelInfo'].keys())
    print([k['CH_name'] for k in CNACLRYPZ03['modelInfo'].values()])
