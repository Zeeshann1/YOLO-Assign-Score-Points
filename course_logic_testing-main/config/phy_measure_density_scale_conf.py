#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : Qiguangnan
# @File    : phy_measure_density_scale_conf.py


PCLWKMD02 = {
    'name': '测定物块的密度',
    'experimentId': 'PCLWKMD01',  # 实验id
    'build_cdll_path': 'phy_measure_density_scale/phy_measure_density_scale_nx/libmyplugins.so',  # build/ 的RT文件
    'modelPath': 'chem_weigh_dissolve/chem_weigh_dissolve.pt',  # 'phy_measure_density_scale/phy_measure_density_scale_2.pt',
    'modelPath_openvino': 'phy_measure_density_scale/phy_measure_density_scale_2.xml',
    'modelPath_tensorrt': 'phy_measure_density_scale/phy_measure_density_scale_nx/phy_measure_density_scale_2.engine',
    'modelClass': 'PHY_measure_density_scale',
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
                  'reserved_2',  # reserved_2 # 细口瓶口
                  'water_column',
                  'reserved_3',  # reserved_3
                  'reserved_4',  # reserved_4
                  'glass_rod',
                  'bottle_n_m',
                  'reserved_5',  # reserved_5
                  'reserved_6',  # reserved_6
                  'duster',
                  'dropper',
                  'liquid',
                  'liquid_on_desk',
                  'reserved_7',  # reserved_7
                  ],
    'scorePointInfo': {
        '1': {
            'info': '打开电子天平',
            'score': 1
        },
        '2': {
            'info': '检查电子天平初始示数，若不为0进行清零操作',
            'score': 1
        },
        '3': {
            'info': '将系有细线的金属块置于电子天平中央，记录电子天平的示数',
            'score': 2
        },
        '4': {
            'info': '在量筒中倒入适量的水',
            'score': 1
        },
        '5': {
            'info': '观察并记录量筒中水面对应的示数',
            'score': 1
        },
        '6': {
            'info': '将系有细线的金属块放入量筒并㓎没在水中',
            'score': 2
        },
        '7': {
            'info': '观察并记录量筒中水面对应的示数',
            'score': 1
        },
        '8': {
            'info': '整理实验器材清理桌面',
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
            'conf': 0.4,
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
            'index': 4,
            'conf': 0.6,
            'CH_name': '天平开',
            'max_cn': 1
        },
        'scale_zero': {
            'index': 5,
            'conf': 0.7,
            'CH_name': '天平开',
            'max_cn': 1
        },
        'salver': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '托盘',
            'max_cn': 1
        },
        'weight_paper': {
            'index': 7,
            'conf': 0.99,
            'CH_name': '称量纸',
            'max_cn': 1
        },
        'bottle_NaCL': {
            'index': 9,
            'conf': 0.99,
            'CH_name': '盐',
            'max_cn': 1
        },
        'NaCL_powder': {
            'index': 10,
            'conf': 0.99,
            'CH_name': 'NaCL颗粒',
            'max_cn': 1
        },
        'scale_off': {
            'index': 11,
            'conf': 0.7,
            'CH_name': '天平关',
            'max_cn': 1
        },
        'scale_notzero': {
            'index': 12,
            'conf': 0.7,
            'CH_name': '天平开',
            'max_cn': 1
        },
        'spoon': {
            'index': 13,
            'conf': 0.99,
            'CH_name': '药匙',
            'max_cn': 1
        },
        'spoon_u': {
            'index': 14,
            'conf': 0.99,
            'CH_name': '药匙勺',
            'max_cn': 1
        },
        'stopper_not_up': {
            'index': 15,
            'conf': 0.99,
            'CH_name': '瓶塞朝下',
            'max_cn': 1
        },
        'stopper_up': {
            'index': 16,
            'conf': 0.99,
            'CH_name': '瓶塞朝上',
            'max_cn': 1
        },
        'measuring_cylinder': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '量筒',
            'max_cn': 1
        },
        'beaker': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '烧杯',
            'max_cn': 2
        },
        'block': {
            'index': 19,
            'conf': 0.5,
            'CH_name': '物块',
            'max_cn': 1
        },
        'reserved_2': {
            'index': 20,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'water_column': {
            'index': 21,
            'conf': 0.6,
            'CH_name': '水柱',
            'max_cn': 1
        },
        'reserved_3': {
            'index': 22,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'reserved_4': {
            'index': 23,
            'conf': 0.99,
            'CH_name': '',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 23,
            'conf': 0.99,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'bottle_n_m': {
            'index': 24,
            'conf': 0.99,
            'CH_name': '细口瓶',
            'max_cn': 1
        },
        'reserved_5': {
            'index': 26,
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
            'conf': 0.6,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'dropper': {
            'index': 28,
            'conf': 0.99,
            'CH_name': '滴管',
            'max_cn': 1
        },
        'liquid': {
            'index': 29,
            'conf': 0.5,
            'CH_name': '液体',
            'max_cn': 1
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
