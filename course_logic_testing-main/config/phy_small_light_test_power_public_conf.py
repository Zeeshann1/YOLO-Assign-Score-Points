PXDPCGLGKK01 = {
    'name': '小灯泡测功率(公开课)',
    'experimentId': 'PXDPCGLGKK01',  # 实验id
    'modelPath': "PHY_small_light_test_power_pubilc/PHY_small_light_test_power_pubilc_20220306.pt",
    'modelClass': 'PHY_small_light_test_power_pubilc',
    'camUse': ['top'],
    'model_type':'Tensorrt6',
    'labelInfo': ['power_source',
                     'ammeter',
                     'voltmeter',
                     'clear',
                     'light',
                     'voltmeter_blue',
                     'slide_rheostat',
                     'gleithretter',
                     'point',
                     'switch',
                     'light_base',
                     'a_v_label',
                     'pointer',
                     'v_color_label',
                     'wire_binding',
                     'wire_con',
                     'rheostat_up',
                     'rheostat_down',
                     'two',"min_max"],
    'scorePointInfo': {
        '1': {
            'info': '串联连线',
            'score': 1
        },
        '2': {
            'info': '并联',
            'score': 1
        },
        '3': {
            'info': '滑动变阻器阻值最大',
            'score': 1
        },
        '4': {
            'info': '滑动变阻器一上一下接线',
            'score': 1
        },
        '5': {
            'info': '灯泡亮',
            'score': 1
        },
        '6': {
            'info': '接线时开关断开',
            'score': 1
        },
        '7': {
            'info': '电压表正进负出(默认)',
            'score': 0
        },
        '8': {
            'info': '电流表正进负出(默认)',
            'score': 0
        },
        '9': {
            'info': '电压表指针发生偏转(默认)',
            'score': 0
        },
        '10': {
            'info': '电流表指针发生偏转(默认)',
            'score': 0
        },
        '11': {
            'info': '拆除线路时开关断开',
            'score': 1
        },
        '12': {
            'info': '整理桌面',
            'score': 1
        },
        '13': {
            'info': '电压表选择合适量程',
            'score': 0
        },
        '14': {
            'info': '电流表选择合适量程',
            'score': 0
        },
        # '14': {
        #     'info': '错误：滑动变阻器同上接线',
        #     'score': 0
        # },
        # '15': {
        #     'info': '错误：滑动变阻器同下接线',
        #     'score': 0
        # },

    },
    'faultPointInfo': {
        '1':{
            'info': '电压表串联',
            'score': 0
        },
        '2':{
            'info': '电流表并联',
            'score': 0
        },
        '3':{
            'info': '滑动变阻器同上',
            'score': 0
        },
        '4':{
            'info': '滑动变阻器同下',
            'score': 0
        },
        # '5':{
        #     'info': '接线时开关闭合',
        #     'score': 0
        # },
        # '6':{
        #     'info': '拆线时开关闭合',
        #     'score': 0
        # },
    },
    'modelInfo': {
        'power_source': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '电源',
            'max_cn': 3
        },
        'ammeter': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '电流表',
            'max_cn': 1
        },
        'voltmeter': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '电压表_黑色_贴黄色标签',
            'max_cn': 1
        },
        'clear': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
        'light': {
            'index': 4,
            'conf': 0.2,
            'CH_name': '灯泡_亮',#红色接线端-接线
            'max_cn': 1
        },
        'voltmeter_blue': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '电压表_蓝色',#黑色接线端-接线
            'max_cn': 1
        },
        'slide_rheostat': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '滑动变阻器',#滑动变阻器_上端_接线
            'max_cn': 1
        },
        'gleithretter': {
            'index': 7,
            'conf': 0.2,
            'CH_name': '滑片',#滑动变阻器_下端_接线
            'max_cn': 1
        },
        'point': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '操作区域',#导线连接
            'max_cn': 1
        },
        'switch': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '开关',#小量程
            'max_cn': 1
        },
        'light_base': {
            'index': 10,
            'conf': 0.2,
            'CH_name': '灯座',#发生偏转，不在0刻度
            'max_cn': 1
        },
        'a_v_label': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '电流表标识_A',#大量程
            'max_cn': 1
        },
        'pointer': {
            'index': 12,
            'conf': 0.2,
            'CH_name': '指针',#在0刻度
            'max_cn': 2
        },
        'v_color_label': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '电压表标识_V',#开关断开
            'max_cn': 1
        },
        'wire_binding': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '接线柱接线',#开关闭合
            'max_cn': 20
        },
        'wire_con': {
            'index': 15,
            'conf': 0.5,
            'CH_name': '导线连接两端接线柱',
            'max_cn': 10
        },
        'rheostat_up': {
            'index': 16,
            'conf': 0.5,
            'CH_name': '滑动变阻器上接线',#电池不分正负极
            'max_cn': 2
        },
        'rheostat_down': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '滑动变阻器下接线',#小灯泡不亮-底座
            'max_cn': 2
        },
        'two': {
            'index': 18,
            'conf': 0.5,
            'CH_name': '并联接线',
            'max_cn': 2
        },
        'min_max': {
            'index': 19,
            'conf': 0.2,
            'CH_name': '电表（电压、电流）接线柱',
            'max_cn': 2
        },
    },
}