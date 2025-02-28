#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/7/1 09:00
# @Author  : Wupenghui
# @File    : chem_separate_phenol_and_check_conf.py

CHEMFLBHBFJBFDJY = {
    'name': '分离苯和苯酚及苯酚的检验',
    'experimentId': 'CHEMFLBHBFJBFDJY',  # 实验id
    'modelPath': 'chem_separate_phenol_and_check_cou/chem_separate_phenol_and_check_cou.pt',
    'modelClass': 'CHEM_separate_phenol_and_check',
    'camUse': ['front', 'top', 'side'],
    'labelInfo': ['hand',
                  'test_tube',
                  'dropper_bottle', 
                  'beaker', 
                  'color_liquid_column', 
                  'reagent_botle', 
                  'separating_funnel', 
                  'separating_funnel_head', 
                  'siderosphere', 
                  'retort_stand', 
                  'dropper', 
                  'hand_duster', 
                  'layered_liquid_column', 
                  'glass_rod'],    
    'scorePointInfo': {
        '1': {
            'info': '取苯和苯酚混合液适量于大试管（或烧杯）中',
            'score': 2
        },
        '2': {
            'info': '滴加稍过量的浓NaOH溶液',
            'score': 4
        },
        '3': {
            'info': '充分振荡',
            'score': 2
        },
        
        '4': {
            'info': '有关化学方程式',
            'score': 2
        },
        
        '5': {
            'info': '将反应后的混合物转移到分液漏斗中',
            'score': 2
        },
        '6': {
            'info': '振荡',
            'score': 4
        },
        '7': {
            'info': '静置',
            'score': 2
        },
        '8': {
            'info': '分液。分液漏斗使用正确',
            'score': 2
        },
        '9': {
            'info': '分液漏斗下口靠小烧杯A内壁',
            'score': 2
        },
        '10': {
            'info': '上层液体从分液漏斗上口倒入小烧杯B', 
            'score': 2
        },
        '11': {
            'info': '向分液所得的下层液体(小烧杯A)中加入适量盐酸',
            'score': 2
        }, 
        '12': {
            'info': '搅拌',
            'score': 2
        }, 
        
        '13':{
           'info': '有关化学方程式',
           'score': 2 
        },
        
        '14': {
            'info': '取适量所得苯酚溶液于小试管中', 
            'score': 2
        }, 
        '15': {
            'info': '滴加氯化铁溶液',
            'score': 2
        }, 
        '16': {
            'info': '现象明显', 
            'score': 2
        }, 
        
        
        '17': {
            'info': '实验常规。遵守实验室规则', 
            'score': 1
        },
        '18': {
            'info': '及时、如实填写实验现象与数据', 
            'score': 1
        },
        '19': {
            'info': '器材及时清洗、复位放置', 
            'score': 1
        },
        '20' : {
            'info': '桌面保持清洁',
            'score': 1
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
            'max_cn': 4
        },
         'dropper_bottle': {
            'index': 2, 
            'conf': 0.4, 
            'CH_name': '滴瓶',
            'max_cn': 1
        }, 
        'beaker': {
            'index': 3,
            'conf': 0.4,
            'CH_name': '烧杯',
            'max_cn': 3
        },       
        'color_liquid_column': {
            'index': 4,
            'conf': 0.3,
            'CH_name': '有色液柱',
            'max_cn': 3
        }, 
        'reagent_bottle': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '试剂瓶',
            'max_cn': 3
        },
        'separating_funnel': {
            'index': 6,
            'conf': 0.4,
            'CH_name': '分液漏斗',
            'max_cn': 1
        },
        'separating_funnel_head': {
            'index': 7,
            'conf': 0.4,
            'CH_name': '分液漏斗漏斗头',
            'max_cn': 1
        },
        'siderosphere': {
            'index': 8,
            'conf': 0.3,
            'CH_name': '铁圈',
            'max_cn': 1
        },
        'retort_stand': {
          'index': 9,
          'conf': 0.4,
          'CH_name': '铁架台',
          'max_cn': 1
        },
        'dropper': {
            'index': 10,
            'conf': 0.4,
            'CH_name': '胶头滴管',
            'max_cn': 3
        },
        'hand_duster': {
            'index': 11,
            'conf': 0.7,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'layered_liquid_column': {
            'index': 12,
            'conf': 0.4,
            'CH_name': '分层液柱',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 13, 
            'conf': 0.4, 
            'CH_name': '玻璃棒',
            'max_cn': 1
        }
    }
}
# if __name__ == '__main__':
#     print(list(CHEMJJHZF01['modelInfo'].keys()))
