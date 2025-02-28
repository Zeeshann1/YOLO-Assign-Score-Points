PXMJXXLCD01 = {
    'name':
    '斜面机械效率测定',
    'experimentId':
    'PXMJXXLCD01',  # 实验id
    'modelPath':
    'phy_mechanical_efficiency/phy_mechanical_efficiency.pt',
    'modelClass':
    'PHY_mechanical_efficiency',
    'camUse': ['top', 'front'],
    'model_type':
    "yolo",
    'rotate_type':
    False,
    'labelInfo': [
        "hand", "board_front", "weight_beam", "block",
        "weight_beam_zero_vertical", "clean_desk_front",
        "weight_beam_zero_horizontal", "height", "pull_weight_beam_vertical",
        "board_top", "weight_top", "towel_top", "clean_desk_top",
        "pull_weight_beam_horizontal"
    ],  #10 1
    'scorePointInfo': {
        '1': {
            'info': '搭建好实验所需装置',
            'score': 1
        },
        '2': {
            'info': '弹簧测力计调零',
            'score': 1
        },
        '3': {
            'info': '称量记录物块重量',
            'score': 1
        },
        '4': {
            'info': '保持斜面勤写程度较缓，测量斜面高度，在该斜面高度下，匀速拉动物块，记录弹簧测力计示数',
            'score': 1
        },
        '5': {
            'info': '提高斜面倾斜度至较陡，测量斜面高度，匀速拉动物块并记录弹簧测力计示数',
            'score': 1
        },
        '6': {
            'info': '提高斜面倾斜度至陡，测量斜面高度，匀速拉动物块并记录弹簧测力计示数',
            'score': 1
        },
        '7': {
            'info': '保持斜面勤写程度陡，改变斜面粗糙程度，匀速拉动物块并记录弹簧测力计示数',
            'score': 1
        },
        '8': {
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
            'CH_name': '称重',
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

if __name__ == '__main__':
    print(list(PXMJXXLCD01['modelInfo'].keys()))
