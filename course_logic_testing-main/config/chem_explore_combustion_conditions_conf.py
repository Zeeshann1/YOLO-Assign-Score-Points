CTJRSTJ01 = {
    'name': '探究燃烧条件',
    'experimentId': 'CTJRSTJ01',  # 实验id
    'modelPath': 'chem_explore_combustion_conditions/chem_explore_combustion_conditions.pt',
    'modelClass': 'CHEM_TJRSTJ',
    'camUse': ['front'],
    'labelInfo': ['hand', 'burner', 'burner_cap', 'clear', 'beaker', 'thin_bottle', 'pour_liquid', 'clip', 'cotton', 'matches', 'flame', 'lighter'],
    'scorePointInfo': {
        '1': {
            'info': '设置对比实验：将酒精倒置在小烧杯',
            'score': 1
        },
        '2': {
            'info': '浸泡在酒精中之后放在酒精灯上进行烘烤，观察是否燃烧',
            'score': 1
        },
        '3': {
            'info': '浸泡在清水中之后放在酒精灯上进行烘烤，观察是否燃烧',
            'score': 1
        },
        '4': {
            'info': '熄灭酒精灯',
            'score': 1
        },
        '5': {
            'info': '清理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '手',
            'max_cn': 5
        },
        'burner': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '酒精灯',
            'max_cn': 1
        },
        'burner_cap': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '酒精灯帽',
            'max_cn': 1
        },
        'clear': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'beaker': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 5
        },
        'thin_bottle': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '细口瓶',
            'max_cn': 5
        },
        'pour_liquid': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '倒液体',
            'max_cn': 5
        },
        'clip': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '夹子',
            'max_cn': 1
        },
        'cotton': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '棉花',
            'max_cn': 5
        },
        'matches': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '火柴',
            'max_cn': 1
        },
        'flame': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '火焰',
            'max_cn': 5
        },
        'lighter': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '点火器',
            'max_cn': 1
        }
    }
}

