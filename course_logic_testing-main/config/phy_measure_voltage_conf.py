#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 17:20
# @Author  : Qinhe
# @File    : phy_measure_voltage_conf.py

PYDYBCDY01 = {
    'name': '用电压表测电压（公司）',
    'experimentId': 'PYDYBCDY01',  # 实验id
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件
    # 'modelPath': 'phy_measure_voltage/phy_measure_voltage.pt',
    'modelPath': 'phy_measure_circuit/phy_measure_circuit.pt',
    'modelPath_openvino': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_1.xml',
    'modelPath_tensorrt': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/phy_measure_voltage_1.engine',
    'modelClass': 'PHY_measure_voltage_01',
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
                  'wire_connection'],#18 1
    'scorePointInfo': {
        '1': {
            'info': '电路连接时开关处于断开状态',
            'score': 2
        },
        '2': {
            'info': '电压表选择合适量程',
            'score': 1
        },
        '3': {
            'info': '电压表，电源正负极连接正确',
            'score': 2
        },
        '4': {
            'info': '电源，开关，小灯泡串联',
            'score': 1
        },
        '5': {
            'info': '小灯泡，电压表并联',
            'score': 1
        },
        '6': {
            'info': '闭合开关，电压表指针发生偏转',
            'score': 1
        },
        '7': {
            'info': '断开开关后再拆电路',
            'score': 1
        },
        '8': {
            'info': '整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.3,
            'CH_name': '电源',
            'max_cn': 3
        },
        'binding_post_red': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '红',
            'max_cn': 5
        },
        'binding_post_black': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '黑',
            'max_cn': 5
        },
        'wire_connection_red': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '红色',
            'max_cn': 4
        },
        'wire_connection_black': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '黑色',
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
            'conf': 0.75,
            'CH_name': '断开',
            'max_cn': 1
        },
        'switch_on': {
            'index': 7,
            'conf': 0.85,
            'CH_name': '闭合',
            'max_cn': 1
        },
        'slide_rheostat': {
            'index': 8,
            'conf': 1,
            'CH_name': '滑动变阻器',
            'max_cn': 1
        },
        'gleithretter': {
            'index': 9,
            'conf': 1,
            'CH_name': '滑片',
            'max_cn': 1
        },
        'above': {
            'index': 10,
            'conf': 1,
            'CH_name': '未连接',
            'max_cn': 2
        },
        'following': {
            'index': 11,
            'conf': 1,
            'CH_name': '未连接',
            'max_cn': 2
        },
        'connect_above': {
            'index': 12,
            'conf': 1,
            'CH_name': '已连接',
            'max_cn': 2
        },
        'connect_following': {
            'index': 13,
            'conf': 1,
            'CH_name': '已连接',
            'max_cn': 2
        },
        'ammeter': {
            'index': 14,
            'conf': 1,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'min_1': {
            'index': 15,
            'conf': 0.7,
            'CH_name': '3V',
            'max_cn': 1
        },
        'max_1': {
            'index': 16,
            'conf': 0.7,
            'CH_name': '15V',
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
            'conf': 0.8,
            'CH_name': '0刻度',
            'max_cn': 1
        },
        'voltmeter': {
            'index': 19,
            'conf': 0.2,
            'CH_name': '电压表',
            'max_cn': 1
        },
        'light': {
            'index': 20,
            'conf': 0.3,
            'CH_name': '小灯泡',
            'max_cn': 1
        },
        'non': {
            'index': 21,
            'conf': 0.7,
            'CH_name': '不亮',
            'max_cn': 1
        },
        'dim': {
            'index': 22,
            'conf': 0.6,
            'CH_name': '弱光',
            'max_cn': 1
        },
        'bright': {
            'index': 23,
            'conf': 0.1,
            'CH_name': '正常光',
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
            'conf': 0.2,
            'CH_name': '导线',
            'max_cn': 5
        },
    }
}


PYDYBCDY02 = {
    'name': '用电压表测电压（黄浦，杨浦，金山）',
    'experimentId': 'PYDYBCDY02',  # 实验id
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件
    # 'modelPath': 'phy_measure_voltage/phy_measure_voltage.pt',
    'modelPath': 'phy_measure_circuit/phy_measure_circuit.pt',
    'modelPath_openvino': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_1.xml',
    'modelPath_tensorrt': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/phy_measure_voltage_1.engine',
    'modelClass': 'PHY_measure_voltage_02',
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
                  'wire_connection'],#18 1
    'scorePointInfo': {
        '1': {
            'info': '电路连接时开关处于断开状态',
            'score': 2
        },
        '2': {
            'info': '电压表选择合适量程',
            'score': 1
        },
        '3': {
            'info': '电压表，电源正负极连接正确',
            'score': 2
        },
        '4': {
            'info': '电源，开关，小灯泡串联',
            'score': 1
        },
        '5': {
            'info': '小灯泡，电压表并联',
            'score': 1
        },
        '6': {
            'info': '闭合开关，电压表指针发生偏转',
            'score': 1
        },
        '7': {
            'info': '断开开关后再拆电路',
            'score': 1
        },
        '8': {
            'info': '整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.3,
            'CH_name': '电源',
            'max_cn': 3
        },
        'binding_post_red': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '红',
            'max_cn': 5
        },
        'binding_post_black': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '黑',
            'max_cn': 5
        },
        'wire_connection_red': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '红色',
            'max_cn': 4
        },
        'wire_connection_black': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '黑色',
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
            'conf': 0.75,
            'CH_name': '断开',
            'max_cn': 1
        },
        'switch_on': {
            'index': 7,
            'conf': 0.85,
            'CH_name': '闭合',
            'max_cn': 1
        },
        'slide_rheostat': {
            'index': 8,
            'conf': 1,
            'CH_name': '滑动变阻器',
            'max_cn': 1
        },
        'gleithretter': {
            'index': 9,
            'conf': 1,
            'CH_name': '滑片',
            'max_cn': 1
        },
        'above': {
            'index': 10,
            'conf': 1,
            'CH_name': '未连接',
            'max_cn': 2
        },
        'following': {
            'index': 11,
            'conf': 1,
            'CH_name': '未连接',
            'max_cn': 2
        },
        'connect_above': {
            'index': 12,
            'conf': 1,
            'CH_name': '已连接',
            'max_cn': 2
        },
        'connect_following': {
            'index': 13,
            'conf': 1,
            'CH_name': '已连接',
            'max_cn': 2
        },
        'ammeter': {
            'index': 14,
            'conf': 1,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'min_1': {
            'index': 15,
            'conf': 0.7,
            'CH_name': '3V',
            'max_cn': 1
        },
        'max_1': {
            'index': 16,
            'conf': 0.7,
            'CH_name': '15V',
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
            'conf': 0.8,
            'CH_name': '0刻度',
            'max_cn': 1
        },
        'voltmeter': {
            'index': 19,
            'conf': 0.2,
            'CH_name': '电压表',
            'max_cn': 1
        },
        'light': {
            'index': 20,
            'conf': 0.3,
            'CH_name': '小灯泡',
            'max_cn': 1
        },
        'non': {
            'index': 21,
            'conf': 0.7,
            'CH_name': '不亮',
            'max_cn': 1
        },
        'dim': {
            'index': 22,
            'conf': 0.6,
            'CH_name': '弱光',
            'max_cn': 1
        },
        'bright': {
            'index': 23,
            'conf': 0.1,
            'CH_name': '正常光',
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
            'conf': 0.2,
            'CH_name': '导线',
            'max_cn': 5
        },
    }
}

if __name__ == '__main__':
    print(list(PYDYBCDY01['modelInfo'].keys()))
