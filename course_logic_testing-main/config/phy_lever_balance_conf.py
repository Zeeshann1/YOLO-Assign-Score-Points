#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/15 16:22
# @Author  : caibaojun
# @File    : phy_lever_balance_conf.py


PTJGGPHDTJ01 = {
    'name': '探究杠杆平衡的条件',
    'experimentId': 'PTJGGPHDTJ01',
    'isSelect': False,
    'build_cdll_path': '',
    # 'modelPath': 'yolov5/weights/phy_lever_balance/phy_lever_balance.pt',
    'modelPath': 'phy_lever_balance/phy_lever_balance.pt',
    'modelClass': 'PHY_lever_balance',
    'modelPath_openvino': '',  # 模型路径
    'modelPath_tensorrt': '',  # 模型路径
    'camUse': ['top', 'front'],
    'imgPath': 'icons/physics/tjggphdtj.jpg',
    'labelInfo': ["hand",
                  "gel_pen",
                  "paper",
                  "lever",
                  "nut",
                  "iron_pole",
                  "slider",
                  "spring_ergometer",
                  "hook_weight",
                  "boutn",
                  "clean_desk",
                  "head",
                  "eye"],
    'scorePointInfo': {
        '1': {
            'info': '将杠杆的中点支在铁架台上',
            'score': 1
        },
        '2': {
            'info': '调节杠杆两端的螺母,使杠杆在水平位置平衡',
            'score': 1
        },
        '3': {
            'info': '完成弹簧测力计调零',
            'score': 1
        },
        '4': {
            'info': '在杠杆两侧悬挂不同数量钩码,调节钩码位置使杠杆水平位置保持平衡',
            'score': 2
        },
        '5': {
            'info': '将钩码悬挂在杠杆上,在杠杆支点同侧用弹簧测力计竖直向上拉杠杆,使杠杆在水平位置保持平衡',
            'score': 2
        },

        '6': {
            'info': '改变钩码个数,位置以及弹簧测力计拉杠杆的位置,再完成几组实验',
            'score': 2
        },
        '7': {
            'info': '整理实验器材,清理桌面',
            'score': 1
        },
        # '8': {
        #     'info': '观察并记录动力F1,阻力F2,动力臂l1,阻力臂l2的数据',
        #     'score': 1
        # },
        # '9': {
        #     'info': '处理实验数据,得出实验结论',
        #     'score': 1
        # }
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'gel_pen': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '笔',
            'max_cn': 1
        },
        'paper': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '纸',
            'max_cn': 1
        },
        'lever': {
            'index': 3,
            'conf': 0.75,
            'CH_name': '天平',
            'max_cn': 1
        },
        'nut': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '螺母',
            'max_cn': 2
        },
        'iron_pole': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '铁杆',
            'max_cn': 1
        },
        'slider': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '滑块',
            'max_cn': 2
        },
        'spring_ergometer': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '弹簧测力计',
            'max_cn': 1
        },
        'hook_weight': {
            'index': 8,
            'conf': 0.6,
            'CH_name': '钩码',
            'max_cn': 8
        },
        'boutn': {
            'index': 9,
            'conf': 0.6,
            'CH_name': '黑旋钮',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 10,
            'conf': 0.6,
            'CH_name': '桌面干净',
            'max_cn': 1
        },
        'head': {
            'index': 11,
            'conf': 0.6,
            'CH_name': '头',
            'max_cn': 1
        },
        'eye': {
            'index': 12,
            'conf': 0.6,
            'CH_name': '眼睛',
            'max_cn': 2
        }
    }
}

if __name__ == '__main__':
    print(list(PTJGGPHDTJ01['modelInfo'].keys()))
