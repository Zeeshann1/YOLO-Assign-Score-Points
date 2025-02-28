#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/12/7 13:01
# @File    : phy_heat_capacity_conf.py


PCDWZDBRR01 = {
    'name': '测定物质的比热容',
    'experimentId': 'PCDWZDBRR01',
    'isSelect': False,
    'modelPath': 'phy_heat_capacity/phy_heat_capacity.pt',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\yolov5\weights\phy_measure_length_time.pt
    'modelClass': 'PHY_heat_capacity',
    'camUse': ['side', 'front'],
    'imgPath': 'icons/physics/CDWZDBRR.png',
    'labelInfo': [
                    "hand",  # 手
                    "flame",  # 火焰
                    "alcohol_burner", # 酒精灯
                    "lamp_cap", # 灯帽
                    "asbestos_net", # 石棉网
                    "match",  # 打火机
                    "thermometer", # 温度计
                    "glass_bubble", # 玻璃泡
                    "beaker", # 小烧杯
                    "measure_cup", # 量杯
                    "water_column", # 水柱
                    "match_flame",  # 打火机点燃酒精灯
                    "stop_watch", # 停表
                    "hand_stop_watch", # 手_停表
                    "base", # 底座
                    "oil_column",  # 油柱
                    "scale"  # 电子天平
                  ],
    'scorePointInfo': {
        '1': {
            'info': '称取相同质量的水和油分别倒入两只烧杯中',
            'score': 2
        },
        '2': {
            'info': '加热用温度计测量两液体的初温度t1 预先设定好液体加热的末温度t2',
            'score': 2
        },
        '3': {
            'info': '分别用酒精灯给两液体加热,记录下加热时刻',
            'score': 2
        },
        # '4': {
        #     'info': '能正确测量多组温度数据',
        #     'score': 2
        # },
        '4': {
            'info': '实验结束后能及时整理仪器',
            'score': 2
        },
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'flame': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '火焰',
            'max_cn': 2
        },
        'alcohol_burner': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '酒精灯',
            'max_cn': 2
        },
        'lamp_cap': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '灯帽',
            'max_cn': 2
        },
        'asbestos_net': {
            'index': 4,
            'conf': 0.6,
            'CH_name': '石棉网',
            'max_cn': 2
        },
        'match': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '打火机',
            'max_cn': 1
        },
        'thermometer': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '温度计',
            'max_cn': 2
        },

        'glass_bubble': {
                    'index': 7,
                    'conf': 0.4,
                    'CH_name': '玻璃泡',
                    'max_cn': 2
                },
        'holder': {
                    'index': 8,
                    'conf': 0.5,
                    'CH_name': '固定器',
                    'max_cn': 2
        },
        'beaker': {
                    'index': 9,
                    'conf': 0.6,
                    'CH_name': '小烧杯',
                    'max_cn': 2
                },
        'measure_cup': {
                'index': 10,
                'conf': 0.6,
                'CH_name': '量杯',
                'max_cn': 2
        },
        'water_column': {
                'index': 11,
                'conf': 0.6,
                'CH_name': '水柱',
                'max_cn': 1
        },
        'match_flame': {
                    'index': 12,
                    'conf': 0.6,
                    'CH_name': '打火机点燃酒精灯',
                    'max_cn': 1
                },
        'stop_watch': {
                    'index': 13,
                    'conf': 0.6,
                    'CH_name': '停表',
                    'max_cn': 1
                },
        'hand_stop_watch': {
                    'index': 14,
                    'conf': 0.6,
                    'CH_name': '手拿停表',
                    'max_cn': 1
                },
        'base': {
            'index': 15,
            'conf': 0.6,
            'CH_name': '底座',
            'max_cn': 2
        },
        'oil_column': {
            'index': 16,
            'conf': 0.6,
            'CH_name': '油柱',
            'max_cn': 1
        },
        'scale': {
            'index': 17,
            'conf': 0.6,
            'CH_name': '电子天平',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PCDWZDBRR01['modelInfo'].keys()))
