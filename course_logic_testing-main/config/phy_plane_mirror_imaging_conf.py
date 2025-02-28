#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/25 09:05
# @Author  : Wupenghui
# @File    : phy_plane_mirror_imaging_conf.py

PHYPMJCX01 = {
    'name': '平面镜成像',
    'experimentId': 'PHYPMJCX01',
    'modelPath': 'phy_plane_mirror_imaging/phy_plane_mirror_imaging.pt',
    'modelClass': 'PHY_plane_mirror_imaging',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': ['hand',   # 0
                  'candle',  # 1
                  'glass_plate',  # 2
                  'paper',  # 3
                  'ruler',  # 4
                  'pen',  # 5
                  'clen_desk'],  # 6
    'scorePointInfo': {
        '1': {
            'info': '将玻璃板竖直置于纸上',
            'score': 1
        },
        '2': {
            'info': '在纸上记下玻璃板的位置',
            'score': 1
        },
        '3': {
            'info': '在玻璃板前竖直放置一只点燃的蜡烛',
            'score': 1
        },
        '4': {
            'info': '在玻璃板后竖直放置另一只未点燃的蜡烛B，移动蜡烛B，从玻璃板前不同位置看去，蜡烛B好像点燃似的    能在玻璃板的另一侧确定物体的像',
            'score': 1
        },
        '5': {
            'info': '在纸上记下蜡烛A、B的位置',
            'score': 1
        },
        '6': {
            'info': '能测量物体到平面镜的距离及所成像到平面镜的距离',
            'score': 1
        },
        '7': {
            'info': '能改变物体的位置，再次测量物距和像距',
            'score': 1
        },
        '8': {
            'info': '改变蜡烛A的位置，再做两次实验',
            'score': 1
        },
        '9': {
            'info': '实验结束，及时整理桌面  整理实验器材',
            'score': 1
        },
        '10': {
            'info': '整理分析实验现象，得出数据',
            'score': 1
        }
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.35,
            'CH_name': '手',
            'max_cn': 2
        },
        'candle': {
            'index': 1,
            'conf': 0.35,
            'CH_name': '蜡烛',
            'max_cn': 3
        },
        'glass_plate': {
            'index': 2,
            'conf': 0.35,
            'CH_name': '玻璃板',
            'max_cn': 1
        },
        'paper': {
            'index': 3,
            'conf': 0.35,
            'CH_name': '白纸',
            'max_cn': 2
        },
        'ruler': {
            'index': 4,
            'conf': 0.35,
            'CH_name': '尺子',
            'max_cn': 1
        },
        'pen': {
            'index': 5,
            'conf': 0.35,
            'CH_name': '笔',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 6,
            'conf': 0.35,
            'CH_name': '整理桌面',
            'max_cn': 1
        },

    }
}