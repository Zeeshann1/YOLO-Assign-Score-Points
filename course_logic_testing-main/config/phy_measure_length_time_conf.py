#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : cbj
# @File    : phy_measure_length_time_conf.py


PYKDCCLCDYBCLSJ01 = {
    'name': '用刻度尺测量长度用表测量时间',
    'experimentId': 'PYKDCCLCDYBCLSJ01',
    'isSelect': False,
    'modelPath': 'phy_measure_length_time/phy_measure_length_time.pt',
    'modelClass': 'PHY_measure_length_time',
    'camUse': ['top', 'front'],
    'imgPath': 'icons/physics/ykdcclcdybclsj.jpg',  # C:\Users\caibaojun\Desktop\git\aiexhibition_windows\icons\physics\ykdcclcdybclsj.jpg
    'labelInfo': ["hand",  # 手
                  "head",  # 头
                  "ruler",  # 尺子
                  "stopwatch",  # 停表
                  "hand_ruler_object",  # 手 尺子 待测物体
                  "hand_stopwatch"  # 手_停表
                  ],
    'scorePointInfo': {
        '1': {
            'info': '根据对测量的精确程度的要求能正确选择刻度尺',
            'score': 2
        },
        '2': {
            'info': '能正确放置刻度处;对准刻度线,有刻度的一边紧贴被测物体且与被测长度保持平行',
            'score': 2
        },
        '3': {
            'info': '能准确将视线正对刻度线',
            'score': 2
        },
        '4': {
            'info': '能正确使用停表的 归零 开始 暂停',
            'score': 2
        },
        '5': {
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
        'head': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '头',
            'max_cn': 1
        },
        'ruler': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '尺子',
            'max_cn': 2
        },
        'stopwatch': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '停表',
            'max_cn': 1
        },
        'hand_ruler_object': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '手_尺子_待测物体',
            'max_cn': 1
        },
        'hand_stopwatch': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '手_停表',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PYKDCCLCDYBCLSJ01['modelInfo'].keys()))
