#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : cbj
# @File    : phy_measure_length_time_conf.py


PCJWDJCLWD01 = {
    'name': '常见温度计测量温度',
    'experimentId': 'PCJWDJCLWD01',
    'isSelect': False,
    'modelPath': 'phy_measure_temperature/phy_measure_temperature.pt',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\yolov5\weights\phy_measure_length_time.pt
    'modelClass': 'PHY_measure_temperature',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/physics/cjwdjclwd.png',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\icons\cjwdjclwd.png
    'labelInfo': ["beaker",  # 烧杯
                    "thermometer",  #  温度计
                    # "liquid_column",  # 水柱
                    "water_column",  # 水柱
                    "glass_bubble",  # 玻璃泡
                    "hand",  # 手
                    "head",  # 头
                    "eye",  # 眼睛
                  ],
    'scorePointInfo': {
        '1': {
            'info': '会估测温度,能正确选择合适的温度计',
            'score': 2
        },
        '2': {
            'info': '测量时玻璃泡完全浸没于被测液体中,且没有碰到容器底部或容器壁',
            'score': 2
        },
        '3': {
            'info': '读数时玻璃泡没有离开被测液体',
            'score': 2
        },
        '4': {
            'info': '待温度计的液注稳定后读数,读数时视线要与温度计中液柱的液面相平',
            'score': 2
        },
        '5': {
            'info': '实验结束后能及时整理仪器',
            'score': 2
        },
    },
    'modelInfo': {
        'beaker': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '烧杯',
            'max_cn': 1
        },
        'thermometer': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '温度计',
            'max_cn': 2
        },
        'water_column': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '水柱',
            'max_cn': 1
        },
        'glass_bubble': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '玻璃泡',
            'max_cn': 1
        },
        'hand': {
            'index': 4,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'head': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '头',
            'max_cn': 1
        },
        'eye': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '眼睛',
            'max_cn': 2
        },
    }
}

if __name__ == '__main__':
    print(list(PCJWDJCLWD01['modelInfo'].keys()))
