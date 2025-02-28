#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 17:20
# @Author  : Qinhe
# @File    : phy_measure_ammeter_conf.py


PYDLBCDL01 = {
    'name': '用电流表测电流（小灯泡）',
    'experimentId': 'PYDLBCDL01',
    'isSelect': False,
    'modelPath': 'phy_measure_A/phy_measure_A.pt',
    'modelClass': 'PHY_measure_A',
    'camUse': ['top', 'side', 'front'],
    'imgPath': 'icons/physics/measure_A.png',
    'scorePointInfo': {
        '1': {
            'info': '电路连接时，开关处于断开状态',
            'score': 1
        },
        '2': {
            'info': '电源、开关、小灯泡、电流表串联',
            'score': 1
        },
        '3': {
            'info': '电流从电流表的”+“接线柱流入，”-“接线柱流出',
            'score': 1
        },
        '4': {
            'info': '闭合开关，电流表指针偏转',
            'score': 1
        },
        '5': {
            'info': '电流表选择合适量程',
            'score': 1
        },
        '6': {
            'info': '断开开关，拆除电路，整理实验器材',
            'score': 1
        }
    },
    'labelInfo': ["手", # 0
                  "电源",
                  "开关闭合",
                  "开关断开",
                  "红色接线柱",
                  "红色接线柱—", # 5
                  "黑色接线柱",
                  "黑色接线柱—",
                  "导线连接",
                  "电流表",
                  "电压表", # 10
                  "指针零刻度",
                  "指针偏转",
                  "小量程",
                  "大量程",
                  "滑动变阻器", # 15
                  "滑片",
                  "灯泡",
                  "灯泡亮", #18
                  "预留1",
                  "预留2",
                  "预留3",
                  "预留4",
                  "预留5",
                  "预留6",
                  "预留7",
                  "预留8",
                  "预留9",
                  "预留10",
                  "预留11",
                  ],
    'modelInfo': {
        's': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'dy': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '电源',
            'max_cn': 3
        },
        'kgbh': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '开关闭合',
            'max_cn': 1
        },
        'kgdk': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '开关断开',
            'max_cn': 1
        },
        'hsjxz': {
            'index': 4,
            'conf': 0.7,
            'CH_name': '正',
            'max_cn': 8
        },
        'hsjxz_': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '正_',
            'max_cn': 8
        },
        'heisjxz': {
            'index': 6,
            'conf': 0.7,
            'CH_name': '负',
            'max_cn': 8
        },
        'heisjxz_': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '负_',
            'max_cn': 8
        },
        'dxlj': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '导线连接',
            'max_cn': 8
        },
        'dlb': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'zz0': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '零刻度',
            'max_cn': 2
        },
        'zz0kd': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '偏转',
            'max_cn': 2
        },
        'xlc': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '小量程',
            'max_cn': 2
        },
        'dlc': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '大量程',
            'max_cn': 2
        },
        'dp': {
            'index': 17,
            'conf': 0.6,
            'CH_name': '灯泡',
            'max_cn': 1
        },
        'dpl': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '灯泡亮',
            'max_cn': 1
        },
    }
}


if __name__ == '__main__':
    print(PYDLBCDL01['modelInfo'].keys())