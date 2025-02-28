PXDPCGL01 = {
    'name': '小灯泡测功率(0-1)',
    'experimentId': 'PXDPCGL01',  # 实验id
    'modelPath': "phy_small_light_test_power/small_light_test_power_v2.pt",
    'modelClass': 'PHY_small_light_test_power',
    'camUse': ['top'],
    'labelInfo': ['power_source',
                 'ammeter',
                 'slide_rheostat',
                 'gleithretter',
                 'wire_connection_red',
                 'wire_connection_black',
                 'connect_above',
                 'connect_following',
                 'wire_connection',
                 'min',
                 'pointer_offset',
                 'max',
                 'pointer_zero',
                 'switch_off',
                 'switch_on',
                 'clean_desk',
                 'wire_connection_binding_post',
                 'light_non',
                 'voltmeter',
                 'light_dim',
                 'l',
                 'light_bright'],
    'scorePointInfo': {
        '1': {
            'info': '电源、开关、灯、电流表、滑动变阻器串联',
            'score': 2
        },
        '2': {
            'info': '电压表、灯座并联',
            'score': 1
        },
        '3': {
            'info': '接线时开关断开',
            'score': 2
        },
        '4': {
            'info': '电流表、电压表正极流入，负极流出',
            'score': 1
        },
        '5': {
            'info': '变阻器链接一上一下，滑块最大一端，电阻最大',
            'score': 1
        },
        '6': {
            'info': '开关闭合，电流表，电压表发生偏转',
            'score': 1
        },
        '7': {
            'info': '电流表电压表选择合适的量程',
            'score': 1
        },
        '8': {
            'info': '整理桌面',
            'score': 1
        },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.3,
            'CH_name': '电源',
            'max_cn': 3
        },
        'ammeter': {
            'index': 1,
            'conf': 0.3,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'slide_rheostat': {
            'index': 2,
            'conf': 0.3,
            'CH_name': '变阻器',
            'max_cn': 1
        },
        'gleithretter': {
            'index': 3,
            'conf': 0.3,
            'CH_name': '滑片',
            'max_cn': 1
        },
        'wire_connection_red': {
            'index': 4,
            'conf': 0.3,
            'CH_name': '接线',#红色接线端-接线
            'max_cn': 20
        },
        'wire_connection_black': {
            'index': 5,
            'conf': 0.3,
            'CH_name': '接线',#黑色接线端-接线
            'max_cn': 20
        },
        'connect_above': {
            'index': 6,
            'conf': 0.4,
            'CH_name': '接线1',#滑动变阻器_上端_接线
            'max_cn': 2
        },
        'connect_following': {
            'index': 7,
            'conf': 0.4,
            'CH_name': '接线2',#滑动变阻器_下端_接线
            'max_cn': 2
        },
        'wire_connection': {
            'index': 8,
            'conf': 0.3,
            'CH_name': '连接',#导线连接
            'max_cn': 20
        },
        'min': {
            'index': 9,
            'conf': 0.3,
            'CH_name': '量程',#小量程
            'max_cn': 1
        },
        'pointer_offset': {
            'index': 10,
            'conf': 0.3,
            'CH_name': '指针',#发生偏转，不在0刻度
            'max_cn': 2
        },
        'max': {
            'index': 11,
            'conf': 0.3,
            'CH_name': '量程',#大量程
            'max_cn': 1
        },
        'pointer_zero': {
            'index': 12,
            'conf': 0.3,
            'CH_name': '指针',#在0刻度
            'max_cn': 2
        },
        'switch_off': {
            'index': 13,
            'conf': 0.3,
            'CH_name': '开关',#开关断开
            'max_cn': 1
        },
        'switch_on': {
            'index': 14,
            'conf': 0.3,
            'CH_name': '开关',#开关闭合
            'max_cn': 1
        },
        'clean_desk': {
            'index': 15,
            'conf': 0.3,
            'CH_name': '清理',
            'max_cn': 1
        },
        'wire_connection_binding_post': {
            'index': 16,
            'conf': 0.3,
            'CH_name': '电源',#电池不分正负极
            'max_cn': 1
        },
        'light_non': {
            'index': 17,
            'conf': 0.3,
            'CH_name': '灯座',#小灯泡不亮-底座
            'max_cn': 1
        },
        'voltmeter': {
            'index': 18,
            'conf': 0.3,
            'CH_name': '电压表',
            'max_cn': 1
        },
        'light_dim': {
            'index': 19,
            'conf': 0.3,
            'CH_name': '灯座',#小灯泡弱光-底座
            'max_cn': 1
        },
        'l': {
            'index': 20,
            'conf': 0.1,
            'CH_name': '灯亮',#小灯泡亮
            'max_cn': 1
        },
        'light_bright': {
            'index': 21,
            'conf': 0.3,
            'CH_name': '灯座',#小灯泡亮-底座
            'max_cn': 1
        },
    },
}
