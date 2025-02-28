#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 16:00
# @Author  : Wupenghui
# @File    : chem_acid_base_neutralization_reaction_conf.py

CHEMSJZHFY01 = {
    'name': '认识酸和碱的中和反应',
    'experimentId': 'CHEMSJZHFY01',
    'modelPath': 'chem_acid_base_neutralization_reaction/acid_base_neutralization_reaction.pt',
    'modelClass': 'CHEM_acid_base_neutralization_reaction',  #
    'camUse': ['top', 'side', 'front'],
    'labelInfo': ['手',
                  '烧杯',
                  '胶头滴管',
                  '试剂瓶',
                  '玻璃柱',
                  '温度计液泡',
                  '试管',
                  '红色液柱',
                  '手拿抹布',
                  '清理桌面，整理实验器材'],
    'scorePointInfo': {
        '1': {
            'info': '向小烧杯中滴加适量氢氧化钠溶液',
            'score': 1
        },
        '2': {
            'info': '向小烧杯滴加2~3滴酚酞试液',
            'score': 1
        },
        '3': {
            'info': '反应前测量溶液温度并观察实验现象',
            'score': 1
        },
        '4': {
            'info': '用胶头滴管吸取稀盐酸逐滴加入上述小烧杯中',
            'score': 1
        },
        '5': {
            'info': '边加盐酸边用玻璃棒轻轻的搅拌，当溶液刚好变成无色时停止滴加稀盐酸',
            'score': 1
        },
        '6': {
            'info': '反应后测量溶液温度并观察实验现象',
            'score': 1
        },
        '7': {
            'info': '取烧杯溶液中的少许溶液，转移到试管中',
            'score': 1
        },
        '8': {
            'info': '向试管滴加一滴稀氢氧化钠溶液，观察颜色的变化',
            'score': 1
        },
        '9': {
            'info': '实验结束收拾实验器材',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.35,
            'CH_name': '手',
            'max_cn': 2
        },
        'beaker': {
            'index': 1,
            'conf': 0.35,
            'CH_name': '烧杯',
            'max_cn': 1
        },
        'dropper': {
            'index': 2,
            'conf': 0.35,
            'CH_name': '胶头滴管',
            'max_cn': 1
        },
        'reagent_bottle': {
            'index': 3,
            'conf': 0.35,
            'CH_name': '试剂瓶',
            'max_cn': 3
        },
        'glass_column': {
            'index': 4,
            'conf': 0.35,
            'CH_name': '玻璃柱',
            'max_cn': 1
        },
        'thermometer_vacuole': {
            'index': 5,
            'conf': 0.35,
            'CH_name': '温度计液泡',
            'max_cn': 1
        },
        'test_tube': {
            'index': 6,
            'conf': 0.35,
            'CH_name': '试管',
            'max_cn': 1
        },
        'red_liquid_column': {
            'index': 7,
            'conf': 0.35,
            'CH_name': '红色液柱',
            'max_cn': 1
        },
        'hand_duster': {
            'index': 8,
            'conf': 0.35,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 9,
            'conf': 0.35,
            'CH_name': '清理桌面，整理实验器材',
            'max_cn': 1
        }

    }
}

