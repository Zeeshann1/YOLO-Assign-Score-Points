PTJTDLXGCC01 = {
    'name':
    '探究通电螺线管外部磁场方向',
    'experimentId':
    'PTJTDLXGCC01',  # 实验id
    'modelPath':
    'phy_magnitic_field/phy_magnitic_field.pt',
    'modelClass':
    'PHY_magnitic_field',
    'camUse': ['top'],
    'rotate_type':
    False,
    'labelInfo': [
        "hand", "needle", "device", "switch_on", "switch_off", "line", "power",
        "power_pos", "power_neg", "clean_desk", "hand_on_switch"
    ],  #10 1
    'scorePointInfo': {
        '1': {
            'info': '正确使用实验器材连接电路',
            'score': 1
        },
        '2': {
            'info': '在通电螺线管两端放置小磁针',
            'score': 1
        },
        '3': {
            'info': '闭合开关，观察小磁针，并说出小磁针N极的指向',
            'score': 1
        },
        '4': {
            'info': '改变电流方向，再次说出小磁针N极的指向',
            'score': 1
        },
        '5': {
            'info': '实验结束后能及时整理仪器',
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
        'needle': {
            'index': 1,
            'conf': 0.55,
            'CH_name': '小磁针',
            'max_cn': 5
        },
        'device': {
            'index': 2,
            'conf': 0.55,
            'CH_name': '实验装置',
            'max_cn': 5
        },
        'switch_on': {
            'index': 3,
            'conf': 0.55,
            'CH_name': '开关闭合',
            'max_cn': 5
        },
        'switch_off': {
            'index': 4,
            'conf': 0.55,
            'CH_name': '开关打开',
            'max_cn': 5
        },
        'line': {
            'index': 5,
            'conf': 0.45,
            'CH_name': '导线',
            'max_cn': 5
        },
        'power': {
            'index': 6,
            'conf': 0.55,
            'CH_name': '电源',
            'max_cn': 5
        },
        'power_pos': {
            'index': 7,
            'conf': 0.55,
            'CH_name': '电源正极',
            'max_cn': 5
        },
        'power_neg': {
            'index': 8,
            'conf': 0.55,
            'CH_name': '电源负极',
            'max_cn': 5
        },
        'clean_desk': {
            'index': 9,
            'conf': 0.55,
            'CH_name': '桌面整洁',
            'max_cn': 5
        },
        'hand_on_switch': {
            'index': 10,
            'conf': 0.55,
            'CH_name': '调整开关',
            'max_cn': 5
        },
    }
}

if __name__ == '__main__':
    print(list(PTJTDLXGCC01['modelInfo'].keys()))
