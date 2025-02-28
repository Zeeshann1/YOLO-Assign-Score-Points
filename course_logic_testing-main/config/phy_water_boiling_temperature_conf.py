#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/11/22 15:18
# @File    : phy_water_boiling_temperature_conf.py


PTJSFTSWDBHDTD01 = {
    'name': '探究水沸腾时温度变化的特点',
    'experimentId': 'PTJSFTSWDBHDTD01',
    'isSelect': False,
    'modelPath': 'phy_water_boiling_temperature/phy_water_boiling_temperature.pt',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\yolov5\weights\phy_measure_length_time.pt
    'modelClass': 'PHY_water_boiling_temperature',
    'camUse': ['side', 'front'],
    'imgPath': 'icons/physics/TJSFTSWDBHDTD.png',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\icons\cjwdjclwd.png
    'labelInfo': [
                    "hand",  # 手
                    "flame",  # 火焰
                    "alcohol_burner", # 酒精灯
                    "lamp_cap", # 灯帽
                    "asbestos_net", # 石棉网
                    "match",  # 打火机
                    "thermometer", # 温度计
                    "glass_bubble", # 玻璃泡
                    "holder", # 盖板
                    "beaker", # 小烧杯
                    "measure_cup", # 量杯
                    "water_column", # 水柱
                    "match_flame",  # 打火机点燃酒精灯
                    "stop_watch", # 停表
                    "hand_stop_watch", # 手_停表
                    "base", # 底座
                  ],
    'scorePointInfo': {
        '1': {
            'info': '在烧杯中倒入适量的水，盖住盖板',
            'score': 2
        },
        '2': {
            'info': '能使用火柴点燃酒精灯,调整酒精灯的位置,用酒精灯外焰给水加热',
            'score': 2
        },
        '3': {
            'info': '能正确固定温度计,让液泡与被测液体充分接触,不碰壁,不碰底',
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
            'max_cn': 1
        },
        'alcohol_burner': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '酒精灯',
            'max_cn': 1
        },
        'lamp_cap': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '灯帽',
            'max_cn': 1
        },
        'asbestos_net': {
            'index': 4,
            'conf': 0.6,
            'CH_name': '石棉网',
            'max_cn': 1
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
            'max_cn': 3
        },

        'glass_bubble': {
                    'index': 7,
                    'conf': 0.2,
                    'CH_name': '玻璃泡',
                    'max_cn': 1
                },
        'holder': {
                    'index': 8,
                    'conf': 0.6,
                    'CH_name': '盖板',
                    'max_cn': 1
                },
        'beaker': {
                    'index': 9,
                    'conf': 0.6,
                    'CH_name': '小烧杯',
                    'max_cn': 1
                },
        'measure_cup': {
                'index': 10,
                'conf': 0.6,
                'CH_name': '量杯',
                'max_cn': 1
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
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PTJSFTSWDBHDTD01['modelInfo'].keys()))
