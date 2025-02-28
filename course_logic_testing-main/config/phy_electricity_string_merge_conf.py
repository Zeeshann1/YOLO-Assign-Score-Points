PJDDDLCBLSY01 = {
    'name': '简单的电路串并联实验',
    'experimentId': 'PJDDDLCBLSY01',  # 实验id
    'modelPath': 'phy_electricity_string_merge/phy_electricity_string_merge_model.pt',
    'modelClass': 'PHY_electricity_string_merge',
    'point_number': 8,
    'model_type': 'YoloPoint',
    'camUse': ['top'],
    'labelInfo': ['ammeter', 'ammeter_needle', 'battery', 'light_base', 'light_off', 'no_range', 'not_wired_neg', 'not_wired_pos', 'switch', 'small_range', 'wired_neg', 'wired_pos', 'two_connect_line_neg', 'light_open', 'clear'],
    'scorePointInfo': {
        '1': {
            'info': '串联电路-电池接线完毕',
            'score': 1
        },
        '2': {
            'info': '串联电路-开关接线闭合',
            'score': 1
        },
        '3': {
            'info': '串联电路-灯座1接线完毕',
            'score': 0.5
        },
        '4': {
            'info': '串联电路-灯座2接线完毕',
            'score': 0.5
        },
        '5': {
            'info': '串联电路-灯1亮',
            'score': 1
        },
        '6': {
            'info': '串联电路-灯2亮',
            'score': 1
        },
        '7': {
            'info': '并联电路-电池接线完毕',
            'score': 0.5
        },
        '8': {
            'info': '并联电路-开关1接线闭合',
            'score': 0.5
        },
        '9': {
            'info': '并联电路-开关2接线闭合',
            'score': 0.5
        },
        '10': {
            'info': '并联电路-开关3接线闭合',
            'score': 0.5
        },
        '11': {
            'info': '并联电路-灯座1连接完毕',
            'score': 0.5
        },
        '12': {
            'info': '并联电路-灯座2连接完毕',
            'score': 0.5
        },
        '13': {
            'info': '并联电路-灯1亮',
            'score': 0.5
        },
        '14': {
            'info': '并联电路-灯2亮',
            'score': 0.5
        },
        '15': {
            'info': '清洁桌面',
            'score': 0.5
        },
    },
    'modelInfo': {
        'ammeter': {
            'index': 0,
            'conf': 0.2,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'ammeter_needle': {
            'index': 1,
            'conf': 0.2,
            'CH_name': '电流表指针',
            'max_cn': 1
        },
        'battery': {
            'index': 2,
            'conf': 0.2,
            'CH_name': '电池',
            'max_cn': 2
        },
        'light_base': {
            'index': 3,
            'conf': 0.2,
            'CH_name': '灯座',
            'max_cn': 5
        },
        'light_off': {
            'index': 4,
            'conf': 0.2,
            'CH_name': '灯-未亮',
            'max_cn': 1
        },
        'no_range': {
            'index': 5,
            'conf': 0.2,
            'CH_name': '无量程',
            'max_cn': 1
        },
        'not_wired_neg': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '未接线负极',
            'max_cn': 6
        },
        'not_wired_pos': {
            'index': 7,
            'conf': 0.2,
            'CH_name': '未接线正极',
            'max_cn': 6
        },
        'switch': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '开关底座',
            'max_cn': 3
        },
        'small_range': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '小量程',
            'max_cn': 1
        },
        'wired_neg': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '接线负极',
            'max_cn': 6
        },
        'wired_pos': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '接线正极',
            'max_cn': 6
        },
        'two_connect_line_neg': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '并联接线柱负极',
            'max_cn': 1
        },
        'light_open': {
            'index': 13,
            'conf': 0.2,
            'CH_name': '灯亮',
            'max_cn': 2
        },
        'clear': {
            'index': 14,
            'conf': 0.2,
            'CH_name': '清洁桌面',
            'max_cn': 1
        },
        # 'two_connect_line_pos': {
        #     'index': 15,
        #     'conf': 0.2,
        #     'CH_name': '并联接线柱正极',
        #     'max_cn': 1
        # },
    }
}
