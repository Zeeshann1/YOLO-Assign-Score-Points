#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/13 16:22
# @Author  : Qiguangnan
# @File    : chem_weigh_dissolve_conf.py

'''
电子天平、量筒(50ml)、胶头滴管、药匙、烧杯（100ml）、玻璃棒、蒸馏水、氯化钠、称量纸
'''

CWZDCLYRJ01 = {
    'name': '物质的称量与溶解',
    'experimentId': 'CWZDCLYRJ01',
    'modelPath': 'chem_weigh_dissolve/chem_weigh_dissolve.pt',
    'modelClass': 'CHEM_weight_dissolve',
    'camUse': ['top', 'front'],
    'labelInfo': ['hand',
                  'eye',
                  'head',
                  'scale',
                  'scale_on',
                  'scale_zero',
                  'salver',
                  'weight_paper',
                  'bottle_NaCL',
                  'NaCL_powder',
                  'scale_off',
                  'scale_notzero',
                  'spoon',
                  'spoon_u',
                  'stopper_not_up',
                  'stopper_up',
                  'measuring_cylinder',
                  'beaker',
                  'block',
                  'reserved_2', # reserved_2 # 细口瓶口
                  'water_column',
                  'reserved_3', # reserved_3
                  'reserved_4', # reserved_4
                  'glass_rod',
                  'bottle_n_m',
                  'reserved_5', # reserved_5
                  'reserved_6', # reserved_6
                  'duster',
                  'dropper',
                  'liquid',
                  'liquid_on_desk',
                  'reserved_7', # reserved_7
                  ],
    'scorePointInfo': {
        '1': {
            'info': '水平放置电子天平，打开电源',
            'score': 1
        },
        '2': {
            'info': '烧杯放置在称量盘上，按“去皮(清零)“键，示数归为零',
            'score': 1
        },
        '3': {
            'info': '用药匙取固体药品，最后轻拍手腕(或药匙柄)添加至规定量',
            'score': 2
        },
        '4': {
            'info': '向量筒中倾倒蒸馏水至规定体积或接近规定体积，若接近规定体积，用胶头滴管逐滴滴加蒸馏水至规定体积',
            'score': 2
        },
        '5': {
            'info': '把量取的蒸馏水全部倒入烧杯中',
            'score': 1
        },
        '6': {
            'info': '用玻璃棒搅拌，至固体药品全部溶解',
            'score': 1
        },
        '7': {
            'info': '将所得的溶液转移到指定容器中',
            'score': 1
        },
        '8': {
            'info': '清洗仪器，整理桌面',
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
        'eye': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '眼睛',
            'max_cn': 6
        },
        'head': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '头',
            'max_cn': 4
        },
        'scale': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '天平',
            'max_cn': 1
        },
        'scale_on': {
            'index': 5,
            'conf': 0.7,
            'CH_name': '天平打开',
            'max_cn': 1
        },
        'scale_zero': {
            'index': 5,
            'conf': 0.7,
            'CH_name': '天平置零',
            'max_cn': 1
        },
        'salver': {
            'index': 6,
            'conf': 0.4,
            'CH_name': '托盘',
            'max_cn': 1
        },
        'weight_paper': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '称量纸',
            'max_cn': 1
        },
        'bottle_NaCL': {
            'index': 8,
            'conf': 0.7,
            'CH_name': '盐',
            'max_cn': 1
        },
        'NaCL_powder': {
            'index': 9,
            'conf': 0.5,
            'CH_name': 'NaCL颗粒',
            'max_cn': 1
        },
        'scale_off': {
            'index': 10,
            'conf': 0.7,
            'CH_name': '天平关',
            'max_cn': 1
        },
        'scale_notzero': {
            'index': 11,
            'conf': 0.7,
            'CH_name': '天平开',
            'max_cn': 1
        },
        'spoon': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '药匙',
            'max_cn': 1
        },
        'spoon_u': {
            'index': 13,
            'conf': 0.6,
            'CH_name': '药匙勺',
            'max_cn': 1
        },
        'stopper_not_up': {
            'index': 14,
            'conf': 0.6,
            'CH_name': '瓶塞朝下',
            'max_cn': 1
        },
        'stopper_up': {
            'index': 15,
            'conf': 0.6,
            'CH_name': '瓶塞朝上',
            'max_cn': 1
        },
        'measuring_cylinder': {
            'index': 16,
            'conf': 0.6,
            'CH_name': '量筒',
            'max_cn': 1
        },
        'beaker': {
            'index': 17,
            'conf': 0.6,
            'CH_name': '烧杯',
            'max_cn': 3
        },
        'block': {
            'index': 18,
            'conf': 0.5,
            'CH_name': '物块',
            'max_cn': 1
        },
        'reserved_2': {
            'index': 19,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'water_column': {
            'index': 20,
            'conf': 0.6,
            'CH_name': '水柱',
            'max_cn': 1
        },
        'reserved_3': {
            'index': 21,
            'conf': 0.5,
            'CH_name': '',
            'max_cn': 1
        },
        'reserved_4': {
            'index': 22,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 23,
            'conf': 0.6,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'bottle_n_m': {
            'index': 24,
            'conf': 0.6,
            'CH_name': '细口瓶',
            'max_cn': 2
        },
        'reserved_5': {
            'index': 25,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'reserved_6': {
            'index': 26,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'duster': {
            'index': 27,
            'conf': 0.5,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'dropper': {
            'index': 28,
            'conf': 0.5,
            'CH_name': '滴管',
            'max_cn': 1
        },
        'liquid': {
            'index': 29,
            'conf': 0.5,
            'CH_name': '液体',
            'max_cn': 2
        },
        'liquid_on_desk': {
            'index': 30,
            'conf': 0.5,
            'CH_name': '桌面水',
            'max_cn': 1
        },
        'reserved_7': {
            'index': 31,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
    }
}