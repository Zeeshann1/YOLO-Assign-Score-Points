#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 09:00
# @Author  : Wupenghui
# @File    : chem_check_Na2CO3_NaCl.py

CHEMJYTSNHLHN = {
    'name': '谁是碳酸钠-深圳',
    'experimentId': 'CHEMJYTSNHLHN',  # 实验id
    'modelPath': 'chem_check_Na2CO3_NaCl_cou/chem_check_Na2CO3_NaCl_cou.pt',
    'modelClass': 'CHEM_check_Na2CO3_NaCl',
    'camUse': ['front', 'top', 'side'],
    'labelInfo': ['hand',
                  'test_tube',
                  'bottle_stopper_positive',
                  'bottle_stopper_opposite',
                  'dropper',
                  'dropper_bottle',
                  'reagent_bottle',
                  'read_liquid_column',
                  'label_paper',
                  'reagent_wooden_stopper'
                  'hand_duster',
                  'test_area'],
    'scorePointInfo': {
        '1': {
            'info': '能正确选用药品',
            'score': 1
        },
        '2': {
            'info': '能正确选用试管、胶头滴管等用品',
            'score': 1
        },
        '3': {
            'info': '能用倾倒法取待测溶液',
            'score': 1
        },
        '4': {
            'info': '瓶塞倒放',
            'score': 1
        },
        '5': {
            'info': '细口瓶瓶口紧挨试管口',
            'score': 1
        },
        '6': {
            'info': '胶头滴管悬垂于试管口上方滴加药品',
            'score': 1
        },
        '7': {
            'info': '能左右振荡试管',
            'score': 1
        },
        '8': {
            'info': '能正确填写实验记录',
            'score': 1,
            'type': 1
        },
        '9': {
            'info': '药品归位、清洗仪器、整理实验台',
            'score': 1
        },
        '10': {
            'info': '讲文明、懂礼貌',
            'score': 1,
            'type': 1
        }

    },

    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.4,
            'CH_name': '手',
            'max_cn': 2
        },
        'test_tube': {
            'index': 1,
            'conf': 0.4,
            'CH_name': '试管',
            'max_cn': 8
        },
        'bottle_stopper_positive': {
            'index': 2,
            'conf': 0.4,
            'CH_name': '瓶塞正放',
            'max_cn': 2
        },
        'bottle_stopper_opposite': {
            'index': 3,
            'conf': 0.4,
            'CH_name': '瓶塞倒放',
            'max_cn': 2
        },
        'dropper': {
            'index': 4,
            'conf': 0.4,
            'CH_name': '胶头滴管',
            'max_cn': 1
        },
        'dropper_bottle': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '滴瓶',
            'max_cn': 2
        },
        'reagent_bottle': {
            'index': 6,
            'conf': 0.4,
            'CH_name': '试剂瓶',
            'max_cn': 2
        },
        'read_liquid_column': {
          'index': 7,
          'conf': 0.4,
          'CH_name': '红色液柱',
          'max_cn': 1
        },
        'label_paper': {
            'index': 8,
            'conf': 0.3,
            'CH_name': '标签纸',
            'max_cn': 8
        },
        'reagent_wooden_stopper': {
            'index': 9,
            'conf': 0.7,
            'CH_name': '带塞试剂瓶',
            'max_cn': 7
        },
        'hand_duster': {
            'index': 10,
            'conf': 0.4,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'test_area': {
            'index': 11,
            'conf': 0.3,
            'CH_name': '实验区域',
            'max_cn': 1
        }

    }
}
# if __name__ == '__main__':
#     print(list(CHEMJJHZF01['modelInfo'].keys()))
