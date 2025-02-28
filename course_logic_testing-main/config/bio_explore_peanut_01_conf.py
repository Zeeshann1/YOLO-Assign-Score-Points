#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04 17:20
# @Author  : Qinhe
# @File    : bio_explore_peanut_01_conf.py


BTJHSGSDXDBY01 = {
    'name': '探究花生果实大小的变异',
    'experimentId': 'BTJHSGSDXDBY01',
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件
    'modelPath': 'bio_explore_peanut/bio_explore_peanut.pt',
    'modelPath_openvino': '',
    'modelPath_tensorrt': '',
    'modelClass': 'BIO_explore_peanut',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': {
        'big_peanut': 0,
        'little_peanut': 1,
        'beaker': 2,
        'take_peanut': 3,
        'ruler': 4,
        'triangle': 5,
        'use_triangle': 6,
        'wrong_use_triangle': 7,
        'nonius': 8,
        'nonius_peanut': 9,
        'one_measuring': 10,
        'two_measuring': 11,
        'nonius_peanut_wrong': 12,
        'write': 13,
        'pen_hand': 14,
        'table': 15,
        'calculator': 16,
        'key_down': 17,
        'hand_calculator': 18,
        'clean': 19,
    },
    'scorePointInfo': {
        '1': {
            'info': '随机选取花生果实得分，未随机选取的不得分',
            'score': 1
        },
        '2': {
            'info': '在实验过程中，能正确使用实验用品',
            'score': 1
        },
        '3': {
            'info': '用测量工具依次测量 3 枚大品种花生果实长轴的长度',
            'score': 1
        },
        '4': {
            'info': '用测量工具依次测量 3 枚小品种花生果实长轴的长度',
            'score': 1
        },
        '5': {
            'info': '将测量得到的数据如实记录在电子实验记录卡中',
            'score': 1,
            "type": 1
        },
        '6': {
            'info': '利用计算器算出平均值，记录在电子实验记录卡中',
            'score': 1
        },
        '7': {
            'info': '分析实验数据，推测花生果实大小变异的原因，选 B 得分',
            'score': 1,
            "type": 1
        },
        '8': {
            'info': '分析实验数据，推测花生果实大小变异的原因，选 A 得分',
            'score': 1,
            "type": 1
        },
        '9': {
            'info': '将测量过的大、小品种果实分别放入原来的烧杯中， 其它实验用品归位，清洁桌面',
            'score': 1
        },
        '10': {
            'info': '有序正确完成各步骤，确认提交电子实验记录卡',
            'score': 1,
            "type": 1
        },
    },
    'modelInfo': {
        'big_peanut': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '大花生',
            'max_cn': 3
        },
        'little_peanut': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '小花生',
            'max_cn': 3
        },
        'beaker': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '烧杯',
            'max_cn': 2
        },
        'take_peanut': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '取花生',
            'max_cn': 1
        },
        'ruler': {
            'index': 4,
            'conf': 0.6,
            'CH_name': '直尺',
            'max_cn': 1
        },
        'triangle': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '三角板',
            'max_cn': 2
        },
        'use_triangle': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '使用三角板',
            'max_cn': 1
        },
        'wrong_use_triangle': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '使用三角板有误差',
            'max_cn': 1
        },
        'one_measuring': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '一个测量工具测花生',
            'max_cn': 1
        },
        'two_measuring': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '二个测量工具测花生',
            'max_cn': 1
        },
        'nonius': {
            'index': 10,
            'conf': 0.6,
            'CH_name': '游标卡尺',
            'max_cn': 1
        },
        'nonius_peanut': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '游标卡尺测花生',
            'max_cn': 1
        },
        'onius_peanut_wrong': {
            'index': 12,
            'conf': 0.6,
            'CH_name': '游标卡尺测花生未卡好',
            'max_cn': 1
        },
        'write': {
            'index': 13,
            'conf': 0.6,
            'CH_name': '手拿笔写字',
            'max_cn': 1
        },
        'pen_hand': {
            'index': 14,
            'conf': 0.6,
            'CH_name': '手拿笔不写字',
            'max_cn': 1
        },

        'table': {
            'index': 15,
            'conf': 0.6,
            'CH_name': '表格',
            'max_cn': 1
        },
        'calculator': {
            'index': 16,
            'conf': 0.6,
            'CH_name': '计算器',
            'max_cn': 1
        },
        'key_down': {
            'index': 17,
            'conf': 0.6,
            'CH_name': '按计算器',
            'max_cn': 1
        },
        'hand_calculator': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '手拿计算器',
            'max_cn': 1
        },
        'clean': {
            'index': 19,
            'conf': 0.3,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
    }
}


'''
'connect_following': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '下连接',
            'max_cn': 2
        },
        'ammeter': {
            'index': 14,
            'conf': 0.6,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'min_1': {
            'index': 15,
            'conf': 0.2,
            'CH_name': 'min',
            'max_cn': 2
        },
        'max_1': {
            'index': 16,
            'conf': 0.2,
            'CH_name': 'max',
            'max_cn': 2
        },
        'pointer_offset': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '偏转',
            'max_cn': 2
        },
        'pointer_zero': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '0刻度',
            'max_cn': 2
        },
        'voltmeter': {
            'index': 19,
            'conf': 0.5,
            'CH_name': '电压表',
            'max_cn': 1
        },
        'light': {
            'index': 20,
            'conf': 1,
            'CH_name': '小灯泡',
            'max_cn': 1
        },
        'non': {
            'index': 21,
            'conf': 1,
            'CH_name': '不亮',
            'max_cn': 1
        },
        'dim': {
            'index': 22,
            'conf': 1,
            'CH_name': '弱光',
            'max_cn': 1
        },
        'bright': {
            'index': 23,
            'conf': 1,
            'CH_name': '正常光',
            'max_cn': 1
        },
        'fixed_resistor': {
            'index': 24,
            'conf': 0.6,
            'CH_name': '电阻',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 25,
            'conf': 0.6,
            'CH_name': '整理',
            'max_cn': 1
        },
        'wire_connection': {
            'index': 26,
            'conf': 0.3,
            'CH_name': '导线',
            'max_cn': 9
        },
'''