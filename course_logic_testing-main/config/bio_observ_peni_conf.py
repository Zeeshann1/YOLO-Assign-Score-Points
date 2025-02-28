#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : j.
# @Time    : 2022/5/10 12:47
# @File    : bio_observ_peni_conf.py


BGCQMYJZP01 = {
    'name': '观察青霉永久装片-深圳',
    'experimentId': 'BGCQMYJZP01',
    'isSelect': False,
    'modelPath': 'bio_observ_peni/bio_observ_peni.pt',
    'modelClass': 'BIO_observ_peni',
    'camUse': ['front', 'side', 'top'],
    'imgPath': 'icons/biology/gcqmyyzp.png',
    'labelInfo': [
                    "reject_box", # 废料槽
                    "hand",  # 手
                    "mi_paper", # 擦镜纸
                    "peni_gla", # 青霉载玻片
                    "blank_gla", # 空白载玻片
                    "coarse_ad", # 粗准焦螺旋
                    "fine_ad", # 细准焦螺旋
                    "stage", # 载物台
                    "reflector", # 反光镜
                    "ad_fine_ad", # 调节细准焦螺旋
                    "ad_coarse_ad",  # 调节粗准焦螺旋
                    "exchanger",  # 转换器
                    "yellow_obl",  # 黄色物镜
                    "blue_obl",  # 蓝色物镜
                    "red_obl",  # 红色物镜
                    "tab_holder", # 压片夹
                    "head",  #头
                    "th_hole", # 通光孔
                    "magni", # 放大镜
                    "eye", # 眼睛
                  ],
    'scorePointInfo': {
        '1': {
            'info': '选取青霉永久装片得分，选取空白载玻片不得分',
            'score': 1
        },
        '2': {
            'info': '选取显微镜得分，选取放大镜不得分',
            'score': 1
        },
        '3': {
            'info': '转动转换器，使低倍物镜对准通光孔',
            'score': 1
        },
        '4': {
            'info': '通过目镜或显示屏看到明亮的视野',
            'score': 1
        },
        '5': {
            'info': '把装片正确固定在载物台上，装片正对通光孔',
            'score': 1
        },
        '6': {
            'info': '转动粗准焦螺旋，使镜筒缓慢下降直至物镜接近装片为止',
            'score': 1
        },
        '7': {
            'info': '正确调焦，能看到清晰的物像并圈出青霉',
            'score': 1,
            'type': 3
        },
        '8': {
            'info': '描述青霉的形态特点，选A得1分，选B不得分',
            'score': 1,
            'type': 1
        },
        '9': {
            'info': '实验结束，将装片取下，复原显微镜，将实验用品放回原处',
            'score': 1
        },
        '10': {
            'info': '举手示意实验完毕，确认分数并签名',
            'score': 1
        },
    },
    'modelInfo': {
        'reject_box ': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '废料槽',
            'max_cn': 1
        },
        'hand': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'mi_paper': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '擦镜纸',
            'max_cn': 1
        },
        'peni_gla': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '青霉载玻片',
            'max_cn': 1
        },
        'blank_gla': {
            'index': 4,
            'conf': 0.4,
            'CH_name': '空白载玻片',
            'max_cn': 1
        },
        'coarse_ad': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '粗准焦螺旋',
            'max_cn': 2
        },
        'fine_ad': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '细准焦螺旋',
            'max_cn': 2
        },
        'stage': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '载物台',
            'max_cn': 1
        },
        'reflector': {
            'index': 8,
            'conf': 0.6,
            'CH_name': '反光镜',
            'max_cn': 1
        },
        'ad_fine_ad': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '调节细准焦螺旋',
            'max_cn': 2
        },
        'ad_coarse_ad': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '调节粗准焦螺旋',
            'max_cn': 2
        },
        'exchanger': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '转换器',
            'max_cn': 1
        },
        'yellow_obl': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '黄色物镜',
            'max_cn': 1
        },
        'blue_obl': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '蓝色物镜',
            'max_cn': 1
        },
        'red_obl': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '红色物镜',
            'max_cn': 1
        },
        'tab_holder': {
            'index': 15,
            'conf': 0.5,
            'CH_name': '压片夹',
            'max_cn': 2
        },
        'head': {
            'index': 16,
            'conf': 0.5,
            'CH_name': '头',
            'max_cn': 1
        },

        'th_hole': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '通光孔',
            'max_cn': 1
        },
        'magni': {
            'index': 18,
            'conf': 0.5,
            'CH_name': '放大镜',
            'max_cn': 1
        },
        'eye': {
            'index': 19,
            'conf': 0.5,
            'CH_name': '眼睛',
            'max_cn': 2
        },

    }
}

if __name__ == '__main__':
    print(list(BGCQMYJZP01['modelInfo'].keys()))
    print(len(list(BGCQMYJZP01['modelInfo'].keys())))
