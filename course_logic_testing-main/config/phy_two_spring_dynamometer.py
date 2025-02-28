PCLJELPH01 = {
    'name':
    '用弹簧测力计探究二力平衡的条件',
    'experimentId':
    'PCLJELPH01',  # 实验id
    'modelPath':
    'phy_two_spring_dynamometer/phy_two_spring_dynamometer.pt',
    'model_type':
    "yolo",
    'modelClass':
    'PHY_spring_dynamometer',
    'camUse': ['top', 'front'],
    'labelInfo': [
        "hand", "head", "weight_beam", "weight_beam_zero_horizontal",
        "weight_beam_zero_vertical", "paperboard", "hook_weight",
        "pull_weight_beam_horizontal", "pull_weight_beam_vertical",
        "clean_desk"
    ],  #10 1
    'scorePointInfo': {
        '1': {
            'info': '在木板上固定两枚图钉，将木板放在水平桌面上',
            'score': 1
        },
        '2': {
            'info': '完成弹簧测力计调零',
            'score': 1
        },
        '3': {
            'info': '用两个弹簧测力计通过细线分别拉两枚图钉，使木板保持静止',
            'score': 1
        },
        '4': {
            'info': '改变两枚图钉的位置，再完成两次实睑',
            'score': 1
        },
        '5': {
            'info': '整理实验器材',
            'score': 1
        },
        '6': {
            'info': '完成弹簧测力计调零',
            'score': 1
        },
        '7': {
            'info': '当钩码静止时,观察并记录弹簧测力计的示数',
            'score': 1
        },
        '8': {
            'info': '使钩码匀速上升，观察并记录弹簧测力计的示数',
            'score': 1
        },
        '9': {
            'info': '使钩码匀速下降，观察并记录弹簧测力计的示数',
            'score': 1
        },
        '10': {
            'info': '整理实验器材',
            'score': 1
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.4,
            'CH_name': '手',
            'max_cn': 2
        },
        'head': {
            'index': 1,
            'conf': 0.25,
            'CH_name': '头',
            'max_cn': 1
        },
        'weight_beam': {
            'index': 2,
            'conf': 0.25,
            'CH_name': '弹簧测力计',
            'max_cn': 2
        },
        'weight_beam_zero_horizontal': {
            'index': 3,
            'conf': 0.4,
            'CH_name': '水平调零弹簧测力计',
            'max_cn': 1
        },
        'weight_beam_zero_vertical': {
            'index': 4,
            'conf': 0.25,
            'CH_name': '竖直调零弹簧测力计',
            'max_cn': 5
        },
        'paperboard': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '木板',
            'max_cn': 1
        },
        'hook_weight': {
            'index': 6,
            'conf': 0.25,
            'CH_name': '钩码',
            'max_cn': 1
        },
        'pull_weight_beam_horizontal': {
            'index': 7,
            'conf': 0.25,
            'CH_name': '水平拉弹簧测力计',
            'max_cn': 1
        },
        'pull_weight_beam_vertical': {
            'index': 8,
            'conf': 0.25,
            'CH_name': '竖直拉弹簧测力计',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 9,
            'conf': 0.25,
            'CH_name': '清理桌面',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PCLJELPH01['modelInfo'].keys()))
