#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : Qiguangnan
# @File    : chem_allocate_solution_conf.py

CNACLRYPZ01 = {
    'name': '一定浓度的氯化钠溶液配置',
    'experimentId': 'CNACLRYPZ01',  # 实验id
    'build_cdll_path': 'yolov5/weights/chem_allocate_solution/chem_allocate_solution_nx/libmyplugins.so',  # build/ 的RT文件
    'modelPath': 'chem_allocate_solution/chem_allocate_solution_1.pt',
    'modelPath_openvino': 'yolov5/weights/chem_allocate_solution/chem_allocate_solution_1.xml',
    'modelPath_tensorrt': 'yolov5/weights/chem_allocate_solution/chem_allocate_solution_nx/chem_allocate_solution_1.engine',
    'modelClass': 'CHEM_allocate_solution',
    'camUse': ['front'],
    'labelInfo': ['scale_imbalance',
                  'scale_balance',
                  'spoon_salt',
                  'stopper_up',
                  'correct_weighing',
                  'measuring_water',
                  'stir_dissolve',
                  'labelling',
                  'clean'],#9 1
    'scorePointInfo': {
        '1': {
            'info': '调节天平， 使天平平衡',
            'score': 1,
            'isDefault': False,
        },
        '2': {
            'info': '用药匙取NaCl固体，NaCl试剂瓶瓶塞倒置',
            'score': 2,
            'isDefault': False,
        },
        '3': {
            'info': '天平称量NaCl，左物右码并垫称量纸，准确称量',
            'score': 2,
            'isDefault': False,
        },
        '4': {
            'info': '胶头滴管定容；平视读数',
            'score': 2,
            'isDefault': False,
        },
        '5': {
            'info': '在烧杯中溶解NaCl，用玻璃棒搅拌',
            'score': 1,
            'isDefault': False,
        },
        '6': {
            'info': '标签纸上写好溶液名称和浓度，贴在试剂瓶上',
            'score': 1,
            'isDefault': False,
        },
        '7': {
            'info': '整理桌面',
            'score': 1,
            'isDefault': False,
        },
    },
    'modelInfo': {
        'scale_imbalance': {
            'index': 0,
            'conf': 0.99,
            'CH_name': '天平不平衡',
            'max_cn': 1
        },
        'scale_balance': {
            'index': 1,
            'conf': 0.8,
            'CH_name': '天平平衡',
            'max_cn': 1
        },
        'spoon_salt': {
            'index': 2,
            'conf': 0.9,
            'CH_name': '药匙',
            'max_cn': 1
        },
        'stopper_up': {
            'index': 3,
            'conf': 0.9,
            'CH_name': '瓶塞正放',
            'max_cn': 2
        },
        'correct_weighing': {
            'index': 4,
            'conf': 0.89,
            'CH_name': '正确称量',
            'max_cn': 1
        },
        'measuring_water': {
            'index': 5,
            'conf': 0.85,
            'CH_name': '量取蒸馏水',
            'max_cn': 1
        },
        'stir_dissolve': {
            'index': 6,
            'conf': 0.84,
            'CH_name': '玻璃棒搅拌',
            'max_cn': 1
        },
        'labelling': {
            'index': 7,
            'conf': 0.95,
            'CH_name': '贴标签',
            'max_cn': 1
        },
        'clean': {
            'index': 8,
            'conf': 0.91,
            'CH_name': '整理',
            'max_cn': 3
        },
    }
}
