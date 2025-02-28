#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/12/03 16:00
# @Author  : Wupenghui
# @File    : chem_hcl_h2so4_check_conf.py

CHEMXYSYXLSDJB01 = {
    'name': '稀盐酸与稀硫酸的鉴别',
    'experimentId': 'CHEMXYSYXLSDJB01',
    'modelPath': 'chem_hcl_h2so4_check_cou/chem_hcl_h2so4_check_cou.pt',
    'modelClass': 'CHEM_hcl_h2so4_check',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': ['hand',   # 0
                  'dropper',  # 1
                  'HCHO_liquid_column',  # 2
                  'test_tube',  # 3
                  'double_test_tube',  # 4
                  'glass_rod',  # 5
                  'cork_upend',  # 6
                  'wooden_cork_upend',  # 7
                  'cork_non_upend',  # 8
                  'wooden_cork_non_upend',  # 9
                  "reagent_bottle",  # 10
                  'tagboard',  # 11
                  'spot_plate',  # 12
                  'Phenolphthalein_liquid_column',  # 13
                  'PH_test_strips_cas_initial',  # 14
                  'PH_test_strips_cas_color',  # 15
                  'shade_guide',  # 16
                  'hand_duster',  # 17
                  'clean_desk'],  # 18
    'scorePointInfo': {
        '1': {
            'info': '向两支盛有待测液的试管中分别滴加氯化钡（或硝酸钡）溶液',
            'score': 2
        },
        '2': {
            'info': '清洗仪器，整理桌面 ',
            'score': 2
        }
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.35,
            'CH_name': '手',
            'max_cn': 2
        },
        'dropper': {
            'index': 1,
            'conf': 0.35,
            'CH_name': '胶头滴管',
            'max_cn': 1
        },
        'HCHO_liquid_column': {
            'index': 2,
            'conf': 0.35,
            'CH_name': '石蕊试液液柱',
            'max_cn': 1
        },
        'test_tube': {
            'index': 3,
            'conf': 0.35,
            'CH_name': '试管',
            'max_cn': 2
        },
        'double_test_tube': {
            'index': 4,
            'conf': 0.35,
            'CH_name': '双试管',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 5,
            'conf': 0.35,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'cork_upend': {
            'index': 6,
            'conf': 0.35,
            'CH_name': '玻璃瓶塞倒放',
            'max_cn': 1
        },
        'wooden_cork_upend': {
            'index': 7,
            'conf': 0.35,
            'CH_name': '木塞倒放',
            'max_cn': 1
        },
        'cork_non_upend': {
            'index': 8,
            'conf': 0.35,
            'CH_name': '玻璃瓶塞未倒放',
            'max_cn': 1
        },
        'wooden_cork_non_upend': {
            'index': 9,
            'conf': 0.35,
            'CH_name': '木塞未倒放',
            'max_cn': 1
        },
        'reagent_bottle': {
            'index': 10,
            'conf': 0.35,
            'CH_name': '试剂瓶',
            'max_cn': 1
        },
        'tagboard': {
            'index': 11,
            'conf': 0.35,
            'CH_name': '标签纸',
            'max_cn': 1
        },
        'spot_plate': {
            'index': 12,
            'conf': 0.35,
            'CH_name': '点滴板',
            'max_cn': 1
        },
        'Phenolphthalein_liquid_column': {
            'index': 13,
            'conf': 0.35,
            'CH_name': '酚酞试液液柱',
            'max_cn': 1
        },
        'PH_test_strips_cas_initial': {
            'index': 14,
            'conf': 0.35,
            'CH_name': '未变色PH试纸',
            'max_cn': 1
        },
        'PH_test_strips_cas_color': {
            'index': 15,
            'conf': 0.35,
            'CH_name': '变色PH试纸',
            'max_cn': 1
        },
        'shade_guide': {
            'index': 16,
            'conf': 0.35,
            'CH_name': '比色板',
            'max_cn': 1
        },
        'hand_duster': {
            'index': 17,
            'conf': 0.35,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 18,
            'conf': 0.35,
            'CH_name': '整理桌面',
            'max_cn': 1
        },

    }
}

