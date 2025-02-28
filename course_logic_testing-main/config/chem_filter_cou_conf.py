#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 16:00
# @Author  : Wupenghui
# @File    : chem_filter_cou_conf.py

CHEMGL01 = {
    'name': '过滤',
    'experimentId': 'CHEMGL01',
    'modelPath': 'chem_filter_cou/chem_filter_cou.pt',
    'modelClass': 'CHEM_filter_cou',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': ['hand',
                  'folded_filter_paper',
                  'beaker',
                  'glass_rod',
                  'funnel',
                  'funnel_mouth',
                  'retort_stand',
                  'siderosphere',
                  "wash_bottle",
                  'liquid_cleaned',
                  'coarse_salt_liquid',
                  'duster',
                  'hand_duster',
                  'clean_desk'],
    'scorePointInfo': {
        '1': {
            'info': '折叠滤纸并展开放入漏斗',
            'score': 0.5
        },
        '2': {
            'info': '滤纸紧贴漏斗内壁',
            'score': 1
        },
        '3': {
            'info': '按由下往上的顺序搭建过滤装置',
            'score': 0.5
        },
        '4': {
            'info': '漏斗下端尖嘴紧靠烧杯内壁',
            'score': 0.5
        },
        '5': {
            'info': '烧杯尖嘴紧靠玻璃棒',
            'score': 0.5
        },
        '6': {
            'info': "玻璃棒下端轻靠三层滤纸一侧",
            'score': 0.5
        },
        '7': {
            'info': '滤液澄清',
            'score': 1
        },
        '8': {
            'info': '拆卸装置，整理桌面',
            'score': 0.5
        }
    },
    'faultPointInfo': {
        '1': {
            'info': '自上向下搭建实验装置',
            'score': 0
            },
        '2': {
            'info': '玻璃棒引流时末端未靠在三层滤纸处',
            'score': 0
        },
        '3': {
          'info': '过滤烧杯大小选取错误',
          'score': 0  
        }
        },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.35,
            'CH_name': '手',
            'max_cn': 2
        },
        'folded_filter_paper': {
            'index': 1,
            'conf': 0.35,
            'CH_name': '折叠滤纸',
            'max_cn': 1
        },
        'beaker': {
            'index': 2,
            'conf': 0.35,
            'CH_name': '烧杯',
            'max_cn': 3
        },
        'glass_rod': {
            'index': 3,
            'conf': 0.35,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'funnel': {
            'index': 4,
            'conf': 0.35,
            'CH_name': '漏斗',
            'max_cn': 1
        },
        'funnel_mouth': {
            'index': 5,
            'conf': 0.35,
            'CH_name': '漏斗嘴',
            'max_cn': 1
        },
        'retort_stand': {
            'index': 6,
            'conf': 0.35,
            'CH_name': '铁架台',
            'max_cn': 1
        },
        'siderosphere': {
            'index': 7,
            'conf': 0.35,
            'CH_name': '铁圈',
            'max_cn': 1
        },
        'wash_bottle': {
            'index': 8,
            'conf': 0.35,
            'CH_name': '洗瓶',
            'max_cn': 1
        },
        'liquid_cleaned': {
            'index': 9,
            'conf': 0.35,
            'CH_name': '澄清滤液',
            'max_cn': 1
        },
        'coarse_salt_liquid': {
            'index': 10,
            'conf': 0.35,
            'CH_name': '粗盐液体',
            'max_cn': 1
        },
        'duster': {
            'index': 11,
            'conf': 0.35,
            'CH_name': '抹布',
            'max_cn': 1
        },
        'hand_duster': {
            'index': 12,
            'conf': 0.35,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 13,
            'conf': 0.35,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'hand_glass_rod_and_beaker': {
            'index': 14,
            'conf': 0.35,
            'CH_name': '手拿玻璃棒及烧杯',
            'max_cn': 1
        }

    }
}

