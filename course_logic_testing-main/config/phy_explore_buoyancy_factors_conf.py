PTJFLDXYNXYSYG01 = {
    'name': '探究浮力大小与那些因素有关',
    'experimentId': 'PTJFLDXYNXYSYG01',  # 实验id
    'modelPath': "phy_explore_buoyancy_factors/phy_explore_buoyancy_factors_v1.pt",
    'modelClass': 'PHY_explore_buoyancy_factors',
    'camUse': ['front'],
    'labelInfo': ['beaker_water',
             'water',
             'spring_dynamometer',
             'hand',
             'beaker',
             'eye',
             'stone',
             'stone_desktop',
             'egg',
             'glass_rod',
             'salt',
             'mouth_bottle',
             'spoon',
             'clear',
             'pen',
             'zero'],
    'scorePointInfo': {
        '1': {
            'info': '在烧杯中加入适量的水，并将鸡蛋放入水中,鸡蛋沉在底部',
            'score': 1
        },
        '2': {
                'info': '并加盐搅拌，观察鸡蛋是否漂浮（浮在水面）',
                'score': 2
            },
        '3': {
            'info': '弹簧测力计调零',
            'score': 1
        },
        '4': {
            'info': '弹簧测力计测金属块，保持静止并记录弹簧测力计示数',
            'score': 2
        },
        '5': {
            'info': '弹簧测力计挂上金属块，并放入水中，记录并观察弹簧测力计示数',
            'score': 2
        },
        '6': {
            'info': '整理桌面',
            'score': 2
        },
    },
    'modelInfo': {
        'beaker_water': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '烧杯水面',
            'max_cn': 2
        },
        'water': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '烧杯水柱',
            'max_cn': 2
        },
        'spring_dynamometer': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '簧测力计',
            'max_cn': 1
        },
        'hand': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '手',
            'max_cn': 2
        },
        'beaker': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 2
        },
        'eye': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '眼睛',
            'max_cn': 2
        },
        'stone': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '物块',
            'max_cn': 1
        },
        'stone_desktop': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '物块离开桌面',
            'max_cn': 1
        },
        'egg': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '鸡蛋',
            'max_cn': 1
        },
        'glass_rod': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '玻璃棒',
            'max_cn': 1
        },
        'salt': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '盐',
            'max_cn': 1
        },
        'mouth_bottle': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '管口瓶',
            'max_cn': 1
        },
        'spoon': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '勺子',
            'max_cn': 1
        },
        'clear': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'pen': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '笔',
            'max_cn': 1
        },
        'zero': {
            'index': 15,
            'conf': 0.5,
            'CH_name': '调零',
            'max_cn': 1
        }
    }
}

if __name__ == '__main__':
    print(list(PTJFLDXYNXYSYG01['modelInfo'].keys()))
