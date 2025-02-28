#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 16:22
# @Author  : Qiguangnan
# @File    : bio_seed_starch_conf.py


BXWJGCJMJHMJ01 = {
    'name': '用显微镜观察酵母菌和霉菌',  # 实验名称
    'experimentId': 'BXWJGCJMJHMJ01',  # 实验id
    'build_cdll_path': 'bio_observe_yeasts_molds_with_microscope/bio_observe_yeasts_molds_with_microscope.so',  # build/ 的RT文件  # C:\Users\caibaojun\Desktop\xin_git1\aiexhibitionservice\yolov5\weights\bio_seed_starch\bio_seed_starch_nx
    'modelPath': 'bio_observe_yeasts_molds_with_microscope/bio_observe_yeasts_molds_with_microscope.pt',  # 模型路径
    'modelPath_openvino': 'bio_observe_yeasts_molds_with_microscope/bio_observe_yeasts_molds_with_microscope.xml',  # 模型路径
    'modelPath_tensorrt': 'ybio_observe_yeasts_molds_with_microscope/bio_observe_yeasts_molds_with_microscope.engine',  # 模型路径
    'modelClass': 'BIO_observe_yeasts_molds',  # 赋分线程类
    'camUse': ['front'],  # 用到的摄像头视角
    'labelInfo': ['wipe', 'cover', 'dye', 'observe', 'daub', 'clean'],#15 2
    'scorePointInfo': {
        '1': {
            'info': '擦拭载玻片与盖玻片',
            'score': 1
        },
        '2': {
            'info': '正确制作酵母菌培养液临时装片，盖玻片45°角一边先接触培养液再缓缓放下',
            'score': 1
        },
        '3': {
            'info': '染色时必须将临时装片从载物台上取下，在盖玻片的一边滴碘液，另一边用吸水纸吸引',
            'score': 1
        },
        '4': {
            'info': '用放大镜观察长有青霉的橘子皮',
            'score': 1
        },
        '5': {
            'info': '将解剖针上的青霉均匀涂抹在载玻片上',
            'score': 1
        },
        '6': {
            'info': '实验结束后能及时整理器材',
            'score': 1
        }
    },
    'modelInfo': {
        'wipe': {
            'index': 0,
            'conf': 0.4,
            'CH_name': '擦载玻片',
            'max_cn': 2
        },
        'cover': {
            'index': 1,
            'conf': 0.4,
            'CH_name': '盖盖玻片',
            'max_cn': 2
        },
        'dye': {
            'index': 2,
            'conf': 0.4,
            'CH_name': '染色',
            'max_cn': 1
        },
        'observe': {
            'index': 3,
            'conf': 0.4,
            'CH_name': '用放大镜观察橘子皮上霉菌',
            'max_cn': 1
        },
        'daub': {
            'index': 4,
            'conf': 0.4,
            'CH_name': '将青霉涂在载玻片',
            'max_cn': 1
        },
        'clean': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '整理器材',
            'max_cn': 1
        }
    }
}

