PSPYDHDMCL01 = {
    'name':
    '测量水平运动物体所受的滑动摩擦力',
    'experimentId':
    'PSPYDHDMCL01',  # 实验id
    'modelPath':
    'phy_sliding_friction/phy_sliding_friction.pt',
    'modelClass':
    'PHY_sliding_friction',
    'camUse': ['top', 'front'],
    'model_type':
    "yolo",
    'rotate_type':
    True,
    'labelInfo': [
        "hand", "board_front", "weight_beam", "block",
        "weight_beam_zero_vertical", "clean_desk_front",
        "weight_beam_zero_horizontal", "height", "pull_weight_beam_vertical",
        "board_top", "weight_top", "towel_top", "clean_desk_top",
        "pull_weight_beam_horizontal"
    ],  #10 1
    'scorePointInfo': {
        '1': {
            'info': '将弹簧测力计指针调0',
            'score': 1
        },
        '2': {
            'info': '在桌面上放一较粗糙的木板，用弹簧测力计拉木块在粗糙木板上匀速滑动',
            'score': 1
        },
        '3': {
            'info': '在木块上加放一个重物，用弹簧测力计水平拉木块在粗糙木板上匀速滑动',
            'score': 1
        },
        '4': {
            'info': '取走木板，保持在木块上放的重物不变，用弹簧测力计水平拉木块在桌面上匀速滑动',
            'score': 1
        },
        '5': {
            'info': '整理器材',
            'score': 1
        }
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.55,
            'CH_name': '手',
            'max_cn': 5
        },
        'board_front': {
            'index': 1,
            'conf': 0.55,
            'CH_name': '木板',
            'max_cn': 1
        },
        'weight_beam': {
            'index': 2,
            'conf': 0.55,
            'CH_name': '弹簧测力计',
            'max_cn': 5
        },
        'block': {
            'index': 3,
            'conf': 0.55,
            'CH_name': '木块',
            'max_cn': 5
        },
        'weight_beam_zero_vertical': {
            'index': 4,
            'conf': 0.55,
            'CH_name': '竖直调零',
            'max_cn': 1
        },
        'clean_desk_front': {
            'index': 5,
            'conf': 0.45,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        'weight_beam_zero_horizontal': {
            'index': 6,
            'conf': 0.55,
            'CH_name': '水平调零',
            'max_cn': 1
        },
        'height': {
            'index': 7,
            'conf': 0.55,
            'CH_name': '高度',
            'max_cn': 1
        },
        'pull_weight_beam_vertical': {
            'index': 8,
            'conf': 0.55,
            'CH_name': '竖直拉动弹簧测力计',
            'max_cn': 1
        },
        'board_top': {
            'index': 9,
            'conf': 0.55,
            'CH_name': '木板',
            'max_cn': 1
        },
        'weight_top': {
            'index': 10,
            'conf': 0.55,
            'CH_name': '砝码',
            'max_cn': 5
        },
        'towel_top': {
            'index': 11,
            'conf': 0.55,
            'CH_name': '毛巾',
            'max_cn': 1
        },
        'clean_desk_top': {
            'index': 12,
            'conf': 0.55,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        'pull_weight_beam_horizontal': {
            'index': 13,
            'conf': 0.55,
            'CH_name': '水平拉动弹簧测力计',
            'max_cn': 1
        },
    }
}
