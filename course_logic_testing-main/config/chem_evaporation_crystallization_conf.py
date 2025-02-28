
CHEMJJHZF01 = {
    'name': '结晶和蒸发',
    'experimentId': 'CHEMJJHZF01',  # 实验id
    'modelPath': 'chem_evaporation_crystallization_cou/chem_evaporation_crystallization_cou.pt',
    'modelClass': 'CHEM_evaporation_crystallization',
    'camUse': ['front', 'top', 'side'],
    'labelInfo': ['hand',
                  'retort_stand',
                  'siderosphere',
                  'evaporating_dish',
                  'alcohol_lamp',
                  'glass_rod',
                  'asbestos_network',
                  'beaker',
                  'flame',
                  'hand_duster',
                  'clean_desk',
                  'crucible_tongs',
                  'hand_glass_rod_beaker',
                  'alcohol_lamp_cap'],
    'scorePointInfo': {
        '1': {
            'info': '自下而上搭建蒸发装置',
            'score': 1
        },
        '2': {
            'info': '正确转移液体',
            'score': 1
        },
        '3': {
            'info': '用酒精灯外焰加热',
            'score': 1
        },
        '4': {
            'info': '用玻璃棒搅拌',
            'score': 2
        },
        '5': {
            'info': '有大量晶体析出时，停止加热，用余热蒸干',
            'score': 2
        },
        '6': {
            'info': '将蒸发皿置于石棉网上，冷却至室温',
            'score': 2
        },
        '7': {
            'info': '拆卸装置，清洗仪器，整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.3,
            'CH_name': '手',
            'max_cn': 2
        },
        'retort_stand': {
            'index': 1,
            'conf': 0.3,
            'CH_name': '铁架台',
            'max_cn': 1
        },
        'siderosphere': {
            'index': 2,
            'conf': 0.3,
            'CH_name': '铁圈',
            'max_cn': 1
        },
        'evaporating_dish': {
            'index': 3,
            'conf': 0.3,
            'CH_name': '蒸发皿',
            'max_cn': 1
        },
        'alcohol_lamp': {
            'index': 4,
            'conf': 0.3,
            'CH_name': '酒精灯',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 5,
            'conf': 0.3,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'asbestos_network': {
            'index': 6,
            'conf': 0.3,
            'CH_name': '石棉网',
            'max_cn': 1
        },
        'beaker': {
          'index': 7,
          'conf': 0.3,
          'CH_name': '烧杯',
          'max_cn': 2
        },
        'flame': {
            'index': 8,
            'conf': 0.3,
            'CH_name': '火焰',
            'max_cn': 1
        },
        'hand_duster': {
            'index': 9,
            'conf': 0.3,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 10,
            'conf': 0.3,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'crucible_tongs': {
            'index': 11,
            'conf': 0.3,
            'CH_name': '坩埚钳',
            'max_cn': 1

        },
        'hand_glass_rod_beaker': {
            'index': 12,
            'conf': 0.35,
            'CH_name': '手拿玻璃棒及烧杯',
            'max_cn': 1
        },
        'alcohol_lamp_cap': {
            'index': 13,
            'conf': 0.35,
            'CH_name': '酒精灯帽',
            'max_cn': 1
        }

    }
}
# if __name__ == '__main__':
#     print(list(CHEMJJHZF01['modelInfo'].keys()))