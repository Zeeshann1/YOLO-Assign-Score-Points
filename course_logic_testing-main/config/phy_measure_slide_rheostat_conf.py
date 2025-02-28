#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 17:20
# @Author  : Qinhe
# @File    : phy_measure_slide_rheostat_conf.py


PYHDBZQGBDLZDDL01 = {
    'name': '用滑动变阻器改变电路中的电流（公司）',
    'experimentId': 'PYHDBZQGBDLZDDL01',
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件

    # 'modelPath': 'yolov5/weights/phy_measure_ammeter/phy_measure_ammeter.pt',
    'modelPath': 'phy_measure_circuit/phy_measure_circuit.pt',
    'modelPath_openvino': '',
    'modelPath_tensorrt': '',
    'modelClass': 'PHY_measure_slide_rheostat_01',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': ['power_source',
                  'binding_post_red',
                  'binding_post_black',
                  'wire_connection_red',
                  'wire_connection_black',
                  'wire_connection_binding_post',
                  'switch_off',
                  'switch_on',
                  'slide_rheostat',
                  'gleithretter',
                  'above',
                  'following',
                  'connect_above',
                  'connect_following',
                  'ammeter',
                  'min_1',
                  'max_1',
                  'pointer_offset',
                  'pointer_zero',
                  'voltmeter',
                  'light',
                  'non',
                  'dim',
                  'bright',
                  'fixed_resistor',
                  'clean_desk',
                  'wire_connection'],
    'scorePointInfo': {
        '1': {
            'info': '电路连接时开关处于断开状态',
            'score': 1
        },
        '2': {
            'info': '滑动变阻器连接一上一下两个接线柱',
            'score': 1
        },
        '3': {
            'info': '滑片位于滑动变阻器的一端，使其连入电路中的阻值最大',
            'score': 1
        },
        '4': {
            'info': '电流表选择合适量程',
            'score': 1
        },
        '5': {
            'info': '电流表，电源正负极连接正确',
            'score': 1
        },
        '6': {
            'info': '电源，开关，滑动变阻器，电流表串联',
            'score': 1
        },
        '7': {
            'info': '闭合开关，电流表指针发生偏转',
            'score': 1
        },
        '8': {
            'info': '改变滑动变阻器电阻，观察电流表示数',
            'score': 1
        },
        '9': {
            'info': '断开开关后再拆电路',
            'score': 1
        },
        '10': {
            'info': '整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '电源',
            'max_cn': 2
        },
        'binding_post_red': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '未连接',
            'max_cn': 6
        },
        'binding_post_black': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '未连接',
            'max_cn': 5
        },
        'wire_connection_red': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '已连接',
            'max_cn': 5
        },
        'wire_connection_black': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '已连接',
            'max_cn': 5
        },
        'wire_connection_binding_post': {
            'index': 5,
            'conf': 0.5,
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
            'conf': 0.5,
            'CH_name': '滑动变阻器',
            'max_cn': 1
        },
        'gleithretter': {
            'index': 9,
            'conf': 0.3,
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
            'CH_name': '0.6A',
            'max_cn': 1
        },
        'max_1': {
            'index': 16,
            'conf': 0.2,
            'CH_name': '3A',
            'max_cn': 1
        },
        'pointer_offset': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '偏转',
            'max_cn': 1
        },
        'pointer_zero': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '0刻度',
            'max_cn': 1
        },
        'voltmeter': {
            'index': 19,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'light': {
            'index': 20,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'non': {
            'index': 21,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'dim': {
            'index': 22,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'bright': {
            'index': 23,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'fixed_resistor': {
            'index': 24,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 25,
            'conf': 0.2,
            'CH_name': '整理',
            'max_cn': 1
        },
        'wire_connection': {
            'index': 26,
            'conf': 0.6,
            'CH_name': '导线',
            'max_cn': 4
        },
    }
}


PYHDBZQGBDLZDDL02 = {
    'name': '用滑动变阻器改变电路中的电流（黄浦，杨浦，金山）',
    'experimentId': 'PYHDBZQGBDLZDDL02',
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件

    # 'modelPath': 'yolov5/weights/phy_measure_ammeter/phy_measure_ammeter.pt',
    'modelPath': 'phy_measure_circuit/phy_measure_circuit.pt',
    'modelPath_openvino': '',
    'modelPath_tensorrt': '',
    'modelClass': 'PHY_measure_slide_rheostat_02',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': ['power_source',
                  'binding_post_red',
                  'binding_post_black',
                  'wire_connection_red',
                  'wire_connection_black',
                  'wire_connection_binding_post',
                  'switch_off',
                  'switch_on',
                  'slide_rheostat',
                  'gleithretter',
                  'above',
                  'following',
                  'connect_above',
                  'connect_following',
                  'ammeter',
                  'min_1',
                  'max_1',
                  'pointer_offset',
                  'pointer_zero',
                  'voltmeter',
                  'light',
                  'non',
                  'dim',
                  'bright',
                  'fixed_resistor',
                  'clean_desk',
                  'wire_connection'],
    'scorePointInfo': {
        '1': {
            'info': '电路连接时开关处于断开状态',
            'score': 1
        },
        '2': {
            'info': '滑动变阻器连接一上一下两个接线柱',
            'score': 1
        },
        '3': {
            'info': '滑片位于滑动变阻器的一端，使其连入电路中的阻值最大',
            'score': 1
        },
        '4': {
            'info': '电流表选择合适量程',
            'score': 1
        },
        '5': {
            'info': '电流表，电源正负极连接正确',
            'score': 1
        },
        '6': {
            'info': '电源，开关，滑动变阻器，电流表串联',
            'score': 1
        },
        '7': {
            'info': '闭合开关，电流表指针发生偏转',
            'score': 1
        },
        '8': {
            'info': '改变滑动变阻器电阻，观察电流表示数',
            'score': 1
        },
        '9': {
            'info': '断开开关后再拆电路',
            'score': 1
        },
        '10': {
            'info': '整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '电源',
            'max_cn': 2
        },
        'binding_post_red': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '未连接',
            'max_cn': 6
        },
        'binding_post_black': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '未连接',
            'max_cn': 5
        },
        'wire_connection_red': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '已连接',
            'max_cn': 5
        },
        'wire_connection_black': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '已连接',
            'max_cn': 5
        },
        'wire_connection_binding_post': {
            'index': 5,
            'conf': 0.5,
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
            'CH_name': '0.6A',
            'max_cn': 1
        },
        'max_1': {
            'index': 16,
            'conf': 0.2,
            'CH_name': '3A',
            'max_cn': 1
        },
        'pointer_offset': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '偏转',
            'max_cn': 1
        },
        'pointer_zero': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '0刻度',
            'max_cn': 1
        },
        'voltmeter': {
            'index': 19,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'light': {
            'index': 20,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'non': {
            'index': 21,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'dim': {
            'index': 22,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'bright': {
            'index': 23,
            'conf': 1,
            'CH_name': '',
            'max_cn': 1
        },
        'fixed_resistor': {
            'index': 24,
            'conf': 1,
            'CH_name': '',
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
            'conf': 0.6,
            'CH_name': '导线',
            'max_cn': 4
        },
    }
}
