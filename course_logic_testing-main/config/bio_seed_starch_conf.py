#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : Qiguangnan
# @File    : bio_seed_starch_conf.py


BYZZZZHYDF01 = {
    'name': '验证种子中含有淀粉',
    'experimentId': 'BYZZZZHYDF01',
    'isSelect': True,
    'modelPath': 'bio_seed_starch/bio_seed_starch.pt',
    'modelClass': 'BIO_seed_starch',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/biology/seed_starch.png',
    'labelInfo': ['peanut_beaker',
                  'corn',
                  'corn_beaker',
                  'blade',
                  'tweezer',
                  'iodine_solution_bottle',
                  'dropper',
                  'red_ink_bottle',
                  'board',
                  'culture_dish',
                  'duster',
                  'reject_box',
                  'hand',
                  'peanut',
                  'cutting_seed'],
    'scorePointInfo': {
        '1': {
            'info': '选取玉米种子',
            'score': 1
        },
        '2': {
            'info': '用镊子夹取种子',
            'score': 1
        },
        '3': {
            'info': '种子放在小木板上',
            'score': 1
        },
        '4': {
            'info': '用刀片将种子切开',
            'score': 1
        },
        '5': {
            'info': '用镊子夹取切好的种子放到培养皿中',
            'score': 1
        },
        '6': {
            'info': '将适量的碘液滴在种子的纵切面上(红墨水不得分)',
            'score': 1
        },
        '7': {
            'info': '正确使用实验用品(正确使用镊子、木板、滴管、培养皿)',
            'score': 2
        },
        '8': {
            'info': '玉米切面变蓝，证明玉米种子中含有淀粉',
            'score': 1
        },
        '9': {
            'info': '将用过的玉米种子放到废料槽中，清理桌面',
            'score': 1
        }
    },
    'modelInfo': {
        'peanut_beaker': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '花生',
            'max_cn': 1
        },
        'corn': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '玉米种子',
            'max_cn': 2
        },
        'corn_beaker': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '玉米',
            'max_cn': 1
        },
        'blade': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '刀片',
            'max_cn': 1
        },
        'tweezer': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '镊子',
            'max_cn': 1
        },
        'iodine_solution_bottle': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '碘液',
            'max_cn': 1
        },
        'dropper': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '滴管',
            'max_cn': 2
        },
        'red_ink_bottle': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '红墨水',
            'max_cn': 1
        },
        'board': {
            'index': 8,
            'conf': 0.6,
            'CH_name': '木板',
            'max_cn': 1
        },
        'culture_dish': {
            'index': 9,
            'conf': 0.6,
            'CH_name': '培养皿',
            'max_cn': 1
        },
        'duster': {
            'index': 10,
            'conf': 0.6,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'reject_box': {
            'index': 11,
            'conf': 0.6,
            'CH_name': '废物缸',
            'max_cn': 1
        },
        'hand': {
            'index': 12,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'peanut': {
            'index': 13,
            'conf': 0.6,
            'CH_name': '花生种子',
            'max_cn': 1
        },
        'cutting_seed': {
            'index': 14,
            'conf': 0.4,
            'CH_name': '切种子',
            'max_cn': 1
        }
    }
}

if __name__ == '__main__':
    print(list(BYZZZZHYDF01['modelInfo'].keys()))
