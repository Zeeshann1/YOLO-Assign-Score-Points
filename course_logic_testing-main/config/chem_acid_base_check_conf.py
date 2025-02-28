#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/18 16:00
# @Author  : Wupenghui
# @File    : chem_acid_base_check_conf.py

CHEMSJJC01 = {
    'name': '酸碱检测',
    'experimentId': 'CHEMSJJC01',
    'modelPath': 'chem_acid_base_check_cou/chem_acid_base_check_cou.pt',
    'modelClass': 'CHEM_acid_base_check',
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
            'info': '瓶塞倒放、标签朝向手心',
            'score': 1
        },
        '2': {
            'info': '试剂瓶口紧挨试管口 ',
            'score': 1
        },
        '3': {
            'info': '将待测液分别加入已编号的试管中，分别滴加石蕊试液，振荡试管（胶头滴管于试管正上方垂直滴加液体）',
            'score': 1
        },
        '4': {
            'info': '能正确汇报盐酸和 NaOH 溶液的酸碱性，观察并记录现象，得出结论',
            'score': 1
        },
        '5': {
            'info': '将待测液分别加入已编号的试管中，分别滴加酚酞试液，振荡试管（胶头滴管于试管正上方垂直滴加液体）',
            'score': 1
        },
        '6': {
            'info': "能正确汇报盐酸和 NaOH 溶液的酸碱性，观察并记录现象，得出结论",
            'score': 1
        },
        '7': {
            'info': '能正确选用玻璃棒蘸取待测液 ',
            'score': 1
        },
        '8': {
            'info': '用玻璃棒蘸取 NaOH 溶液，滴在 pH 试纸上（将pH试纸放在表面皿上，用洁净且干燥的玻璃棒蘸取待测液点在pH试纸上）',
            'score': 1
        },
        '9': {
            'info': '能正确选用 pH 试纸测酸碱度',
            'score': 1
        },
        '10': {
            'info': '将试纸显示的颜色与标准比色卡比较，报告测得的 pH（将试纸显示的颜色与标准比色卡比较，报告测得的 pH）',
            'score': 1
        },
        '11': {
            'info': '药品归位，清理试验台，清洗仪器，整理桌面',
            'score': 1
        },
        '12': {
            'info': '文明懂礼貌',
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

