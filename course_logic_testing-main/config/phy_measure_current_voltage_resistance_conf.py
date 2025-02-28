#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/02 17:20
# @Author  : Qinhe
# @File    : phy_measure_current_voltage_resistance_conf.py


PTJDLYDYDZDGX01 = {
    'name': '探究电流与电压、电阻的关系',
    'experimentId': 'PTJDLYDYDZDGX01',
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件
    'modelPath': 'phy_measure_circuit/phy_measure_circuit.pt',
    'modelPath_openvino': '',
    'modelPath_tensorrt': '',
    'modelClass': 'PHY_measure_current_voltage_resistance',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': {
        'power_source': 0,
        'binding_post_red': 1,
        'binding_post_black': 2,
        'wire_connection_red': 3,
        'wire_connection_black': 4,
        'wire_connection_binding_post': 5,
        'switch_off': 6,
        'switch_on': 7,
        'slide_rheostat': 8,
        'gleithretter': 9,
        'above': 10,
        'following': 11,
        'connect_above': 12,
        'connect_following': 13,
        'ammeter': 14,
        'min_1': 15,
        'max_1': 16,
        'pointer_offset': 17,
        'pointer_zero': 18,
        'voltmeter': 19,
        'light': 20,
        'non': 21,
        'dim': 22,
        'bright': 23,
        'fixed_resistor': 24,
        'clean_desk': 25,
        'wire_connection': 26
    },
    'scorePointInfo': {
        '1': {
            'info': '电路连接时开关处于断开状态',
            'score': 1
        },
        '2': {
            'info': '滑动变阻器接一上一下接入',
            'score': 1
        },
        '3': {
            'info': '滑动变阻器电阻最大',
            'score': 1
        },
        '4': {
            'info': '电压表选择合适量程',
            'score': 1
        },
        '5': {
            'info': '电流表选择合适量程',
            'score': 1
        },
        '6': {
            'info': '电压表，电源正负极连接正确',
            'score': 1
        },
        '7': {
            'info': '电流表，电源正负极连接正确',
            'score': 1
        },
        '8': {
            'info': '电压表并联在电阻两端',
            'score': 1
        },
        '9': {
            'info': '电源，开关，滑动变阻器，电阻，电流表串联',
            'score': 1
        },
        '10': {
            'info': '# 闭合开关，电压表指针发生偏转',
            'score': 1
        },
        '11': {
            'info': '闭合开关，电流表指针发生偏转',
            'score': 1
        },
        '12': {
            'info': '改变滑动变阻器电阻，观察电流表示数',
            'score': 1
        },
        '13': {
            'info': '断开开关后再拆电路',
            'score': 1
        },
        '14': {
            'info': '整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '电源',
            'max_cn': 3
        },
        'binding_post_red': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '红',
            'max_cn': 16
        },
        'binding_post_black': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '黑',
            'max_cn': 14
        },
        'wire_connection_red': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '红色',
            'max_cn': 14
        },
        'wire_connection_black': {
            'index': 4,
            'conf': 0.4,
            'CH_name': '黑色',
            'max_cn': 14
        },
        'wire_connection_binding_post': {
            'index': 5,
            'conf': 1,
            'CH_name': '已连接',
            'max_cn': 5
        },
        'switch_off': {
            'index': 6,
            'conf': 0.3,
            'CH_name': '断开',
            'max_cn': 1
        },
        'switch_on': {
            'index': 7,
            'conf': 0.3,
            'CH_name': '闭合',
            'max_cn': 1
        },
        'slide_rheostat': {
            'index': 8,
            'conf': 0.6,
            'CH_name': '滑动变阻器',
            'max_cn': 1
        },
        'gleithretter': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '滑片',
            'max_cn': 1
        },
        'above': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '上',
            'max_cn': 2
        },
        'following': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '下',
            'max_cn': 2
        },
        'connect_above': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '上连接',
            'max_cn': 2
        },
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
    }
}
