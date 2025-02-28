#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/13 17:20
# @Author  : Wupenghui
# @File    : phy_sring_balance_measurement_conf.py

PYTHCLJCL01 = {
    'name': '用弹簧测力计测力',
    'experimentId': 'PYTHCLJCL01',
    'modelPath': 'phy_sring_balance_measurement/phy_sring_balance_measurement.pt',
    'modelClass': 'PHY_sring_balance_measurement_cou',
    'camUse': ['front'],
    'labelInfo': ['hand',
                  'eye',
                  'weight_beam',
                  'weight_beam_zero',
                  'hook_weight',
                  'hand_pull_ring',
                  'silver_strip_proportion',
                  'clean_desk',
                  "head"],
    'scorePointInfo': {
        '1': {
            'info': '观察并记录弹簧测力计的量程和最小分度值',
            'score': 1
        },
        '2': {
            'info': '完成弹簧测力计调零',
            'score': 1
        },
        '3': {
            'info': '在弹簧测力计的挂钩上悬挂合适的物体',
            'score': 1
        },
        '4': {
            'info': '物体静止时，观察并记录弹簧测力计示数',
            'score': 1
        },
        '5': {
            'info': '整理实验器材',
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
        'eye': {
            'index': 1,
            'conf': 0.35,
            'CH_name': '眼睛',
            'max_cn': 2
        },
        'weight_beam': {
            'index': 2,
            'conf': 0.35,
            'CH_name': '弹簧测力计',
            'max_cn': 1
        },
        'weight_beam_zero': {
            'index': 3,
            'conf': 0.35,
            'CH_name': '弹簧测力计调零',
            'max_cn': 1
        },
        'hook_weight': {
            'index': 4,
            'conf': 0.35,
            'CH_name': '钩码',
            'max_cn': 1
        },
        'hand_pull_ring': {
            'index': 5,
            'conf': 0.35,
            'CH_name': '手拉拉环',
            'max_cn': 1
        },
        'silver_strip_proportion': {
            'index': 6,
            'conf': 0.35,
            'CH_name': '银色铁片面积',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 7,
            'conf': 0.35,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'head': {
            'index': 8,
            'conf': 0.35,
            'CH_name': '头',
            'max_cn': 1
        },
    }
}

