PAJMDYL01 = {
    'name': '阿基米德原理',
    'experimentId': 'PAJMDYL01',  # 实验id
    'modelPath': "phy_archimedes_principle/phy_archimedes_principle_v1.pt",
    'modelClass': 'PHY_archimedes_principle',
    'camUse': ['front'],
    'labelInfo': ['spring_dynamometer',
                  'pen',
                  'paper',
                  'stone',
                  'eye',
                  'hand',
                  'zero',
                  'stone_desktop',
                  'bottle_water_surface',
                  'bottle_water',
                  'measuring_bottle',
                  'beaker',
                  'beaker_water',
                  'clear',
                  'beaker_water_surface'],
    'scorePointInfo': {
        '1': {
            'info': '在量筒中倒入适量水，观察并记录量筒中水面的对应示数',
            'score': 1
        },
        '2': {
            'info': '完成弹簧测力计调零',
            'score': 1
        },
        '3': {
            'info': '弹簧测力计测金属块，保持静止并记录示数',
            'score': 1
        },
        '4': {
            'info': '弹簧测力计挂上金属块，并放入水中',
            'score': 1
        },
        '5': {
            'info': '整理器材',
            'score': 1
        },
    },
    'modelInfo': {
        'spring_dynamometer': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '弹簧测力器',
            'max_cn': 1
        },
        'pen': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '笔',
            'max_cn': 1
        },
        'paper': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '纸',
            'max_cn': 1
        },
        'stone': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '物块',
            'max_cn': 1
        },
        'eye': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '眼睛',
            'max_cn': 2
        },
        'hand': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '手',
            'max_cn': 2
        },
        'zero': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '调零',
            'max_cn': 1
        },
        'stone_desktop': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '物块离开桌面',
            'max_cn': 1
        },
        'bottle_water_surface': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '量筒水面',
            'max_cn': 1
        },
        'bottle_water': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '量筒水柱',
            'max_cn': 1
        },
        'measuring_bottle': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '量筒',
            'max_cn': 1
        },
        'beaker': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '烧杯',
            'max_cn': 2
        },
        'beaker_water': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '烧杯水柱',
            'max_cn': 2
        },
        'clear': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'beaker_water_surface': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '烧杯水面',
            'max_cn': 2
        },
    }
}

PAJMDJMCL01 = {
    'name': '用弹簧测力计测量力的大小',
    'experimentId': 'PAJMDJMCL01',  # 实验id
    'modelPath': "phy_archimedes_principle/phy_archimedes_rub_220605.pt",
    # "phy_archimedes_principle/phy_archimedes_rub_220514.pt",
    'modelClass': 'PHY_archimedes_rub',
    'camUse': ['top', 'front', 'side'],
    'labelInfo': ['car', 'spring_dynamometer', 'beaker_water_surface', 'beaker_water', 'beaker', 'eye', 'hand', 'line',
                  'stone', 'conn', 'spring_car', 'spring_stone', 'towel', 'head'],
    'scorePointInfo': {
        '1': {
            'info': '选择较小的石块进行测量',
            'score': 1
        },
        '2': {
            'info': '正确输入弹簧测力计的量程',
            'score': 1,
            'type': 1
        },
        '3': {
            'info': '对弹簧测力计进行调零',
            'score': 1
        },
        '4': {
            'info': '将小石块用细线系好，并竖直挂在弹簧测力计挂钩上',
            'score': 1
        },
        '5': {
            'info': '待示数稳定后测出重力G的大小',
            'score': 1,
            'type': 1
        },
        '6': {
            'info': '将小石块缓慢浸入水中',
            'score': 1
        },
        '7': {
            'info': '待示数稳定后读出此时拉力F的大小',
            'score': 1,
            'type': 1
        },
        '8': {
            'info': '拉着木块在实验台上匀速直线滑动',
            'score': 1
        },
        '9': {
            'info': '读出受到的摩擦力f的大小',
            'score': 1,
            'type': 1
        },
        '10': {
            'info': '实验结束后能及时整理仪器；能和监考老师文明礼貌交流',
            'score': 1
        },
    },
    'modelInfo': {
        'car': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '小车',
            'max_cn': 1
        },
        'spring_dynamometer': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '弹簧测力计',
            'max_cn': 1
        },
        'beaker_water_surface': {
            'index': 2,
            'conf': 0.4,
            'CH_name': '烧杯水面',
            'max_cn': 2
        },
        'beaker_water': {
            'index': 3,
            'conf': 0.4,
            'CH_name': '烧杯水柱',
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
            'conf': 0.2,
            'CH_name': '眼睛',
            'max_cn': 2
        },
        'hand': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '手',
            'max_cn': 2
        },
        'line': {
            'index': 7,
            'conf': 0.2,
            'CH_name': '细线',
            'max_cn': 1
        },
        'stone': {
            'index': 8,
            'conf': 0.1,
            'CH_name': '石头',
            'max_cn': 2
        },
        'conn': {
            'index': 9,
            'conf': 0.3,
            'CH_name': '测力计——小车连接处',
            'max_cn': 1
        },
        'spring_car': {
            'index': 10,
            'conf': 0.2,
            'CH_name': '测力计和小车',
            'max_cn': 1
        },
        'spring_stone': {
            'index': 11,
            'conf': 0.2,
            'CH_name': '测力计和石头',
            'max_cn': 1
        },
        'towel': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '毛巾',
            'max_cn': 1
        },
        'head': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '头',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PAJMDYL01['modelInfo'].keys()))
    print(list(PAJMDJMCL01['modelInfo'].keys()))
