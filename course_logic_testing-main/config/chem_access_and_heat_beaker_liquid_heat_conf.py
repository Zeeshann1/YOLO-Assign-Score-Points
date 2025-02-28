#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : Caibaojun
# @Time    : 2021/12/22 12:45
# @File    : chem_access_and_heat_beaker_liquid_heat_conf.py


CSJDQYYJRZSBZYTJR01 = {
    'name': '试剂的取用与加热之烧杯中液体加热',
    'experimentId': 'CSJDQYYJRZSBZYTJR01',
    'isSelect': False,
    'modelPath': 'chem_access_and_heat_beaker_liquid_heat/chem_access_and_heat_beaker_liquid_heat.pt',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\yolov5\weights\phy_measure_length_time.pt
    'modelClass': 'CHEM_access_and_heat_beaker_liquid_heat',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/chemistry/CSJDQYYJRZSBZYTJR.png',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\icons\cjwdjclwd.png
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

                    "oil_column",  # 油柱
                    "scale",  # 电子天平
                    "narrow_bottle",  # 细口瓶
                    "iron_ring",  # 铁圈
                    "iron_pole",  # 铁杆
                    "tube",  # 试管
                    "tube_mouth",  # 试管口
                    "tube_foot",  # 试管底部
                    "iron_clamp_head",  # 铁试管夹头
                    "iron_clamp",  # 铁试管夹

                    "wood_clamp",  # 木试管夹
                    "wood_clamp_head",  # 木试管夹头
                    "clean_water",  # 澄清透明试剂
                    "solid_reagent",  # 固体试剂
                    "matchbox",  # 火柴盒
                    "wood",  # 木块
                  ],
    'scorePointInfo': {
        '1': {
            'info': '放置铁架台',
            'score': 1
        },
        '2': {
            'info': '放置酒精灯',
            'score': 1
        },
        '3': {
            'info': '调节铁圈高度',
            'score': 1
        },
        '4': {
            'info': '放置石棉网',
            'score': 1
        },
        '5': {
            'info': '放置烧杯',
            'score': 2
        },
        '6': {
            'info': '点燃酒精灯,外焰加热',
            'score': 2
        },
        '7': {
            'info': '加热结束后,用灯帽盖灭酒精灯',
            'score': 2
        },
        '8': {
            'info': '清理桌面',
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
        'narrow_bottle': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '细口瓶',
            'max_cn': 1
        },
        'iron_ring': {
            'index': 19,
            'conf': 0.6,
            'CH_name': '铁圈',
            'max_cn': 1
        },
        'iron_pole': {
            'index': 20,
            'conf': 0.6,
            'CH_name': '铁杆',
            'max_cn': 1
        },
        'tube': {
            'index': 21,
            'conf': 0.6,
            'CH_name': '试管',
            'max_cn': 1
        },
        'tube_mouth': {
            'index': 22,
            'conf': 0.6,
            'CH_name': '试管口',
            'max_cn': 1
        },
        'tube_foot': {
            'index': 23,
            'conf': 0.6,
            'CH_name': '试管底部',
            'max_cn': 1
        },
        'iron_clamp_head': {
            'index': 24,
            'conf': 0.6,
            'CH_name': '铁试管夹头',
            'max_cn': 1
        },
        'iron_clamp': {
            'index': 25,
            'conf': 0.6,
            'CH_name': '铁试管夹',
            'max_cn': 1
        },
        'wood_clamp': {
            'index': 26,
            'conf': 0.6,
            'CH_name': '木试管夹',
            'max_cn': 1
        },
        'wood_clamp_head': {
            'index': 27,
            'conf': 0.6,
            'CH_name': '木试管夹头',
            'max_cn': 1
        },
        'clean_water': {
            'index': 28,
            'conf': 0.6,
            'CH_name': '澄清透明试剂',
            'max_cn': 1
        },
        'solid_reagent': {
            'index': 29,
            'conf': 0.6,
            'CH_name': '固体试剂',
            'max_cn': 1
        },
        'matchbox': {
            'index': 30,
            'conf': 0.6,
            'CH_name': '火柴盒',
            'max_cn': 1
        },
        'wood': {
            'index': 31,
            'conf': 0.6,
            'CH_name': '木块',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(CSJDQYYJRZSBZYTJR01['modelInfo'].keys()))
