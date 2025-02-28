#!/usr/bin/python3.6.10
# -*- coding: utf-8 -*-
# @Author  : j.
# @Time    : 2022/4/15 15:06
# @File    : bio_make_observ_yeast_conf.py


BZZGCJMJZP01 = {
    'name': '制作观察酵母菌装片',
    'experimentId': 'BZZGCJMJZP01',
    'isSelect': False,
    'modelPath': 'bio_make_observ_yeast/bio_make_observ_yeast.pt',
    'modelClass': 'BIO_make_observ_yeast',
    'camUse': ['front', 'side', 'top'],
    'imgPath': 'icons/biology/zzgcjmjzp.png',
    'labelInfo': [
                    "beaker", # 烧杯
                    "yeast_li", # 酵母菌液
                    "hand",  # 手(正,俯,侧)
                    "clean_cloth", # 清洁布
                    "glass_slide", # 载玻片
                    "glass_cover", # 盖玻片
                    "tweezer", # 镊子
                    "dropper", # 滴管
                    "ab_paper", # 吸水纸
                    "coarse_ad", # 粗准焦螺旋
                    "fine_ad", # 细准焦螺旋
                    "stage", # 载物台
                    "reflector", # 反光镜
                    "clean_glass", # 清洁载玻片和盖玻片
                    "drop_yeast", # 酵母菌滴在载玻片
                    "cover_slide", # 盖玻片盖在滴有酵母菌的载玻片上
                    "ad_fine_ad", # 调节细准焦螺旋
                    "ad_coarse_ad",  # 调节粗准焦螺旋
                    "ab_paper_op", # 吸水纸吸多余水
                    "exchanger", # 转换器
                    "sma_oblense",  # 小物镜
                    "big_oblense", # 大物镜
                    "tab_holder", # 压片夹
                    "head",  #头
                    "eye", # 眼睛
                    "th_hole",  # 通光孔
                    "clear_im",  # 小白上清晰的像
                  ],
    'scorePointInfo': {
        '1': {
            'info': '拇指和食指夹住载玻片边缘，用纱布来回擦拭载玻片',
            'score': 1
        },
        '2': {
            'info': '用滴管将酵母菌滴在载玻片中央',
            'score': 1
        },
        '3': {
            'info': '用镊子夹取盖玻片，盖玻片一侧边缘触碰到水滴，使盖玻片与载玻片成45度角、缓缓盖在酵母菌液上，盖玻片下无大的影响观察的气泡',
            'score': 1
        },
        # '4': {
        #     'info': '正确使用显微镜', # (先转动反光镜视野出现亮斑,转动粗准焦螺旋使镜筒上升,将玻片标本放在载物台使标本目镜正对通光孔中央,用压片夹住标本,顺时针转动粗准焦使镜筒下降,眼睛注视物镜防止压碎玻片标本,左眼看目镜,逆时针转动粗准焦螺旋看清细胞,调准细准焦螺旋更加清晰)
        #     'score': 1
        # },
        '4': {
            'info': '用一个较大的光圈对准通光孔',
            'score': 1
        },
        '5': {
            'info': '转动转换器使低倍物镜对准通光孔，使视野中出现亮斑 ',
            'score': 1
        },
        '6': {
            'info': '转动粗准焦螺旋使镜筒上升',
            'score': 1
        },
        '7': {
            'info': '将玻片标本放在载物台上使标本正对通光孔中央',
            'score': 1
        },
        '8': {
            'info': '用压片夹住标本',
            'score': 1
        },
        '9': {
            'info': '顺时针转动粗准焦螺旋使镜筒下降,眼睛注视物镜防止压碎玻片标本',
            'score': 1
        },
        '10': {
            'info': '左眼看目镜,逆时针转动粗准焦螺旋使镜筒缓缓上升直至看清细胞',
            'score': 1
        },
        '11': {
            'info': '调节细准焦螺旋使图像更加清晰',
            'score': 1
        },
        '12': {
            'info': '成清晰的像',
            'score': 1
        },

        '13': {
            'info': '实验结束后擦拭载玻片和盖玻片',
            'score': 1
        },

        '14': {
            'info': '实验结束后及时整理仪器',
            'score': 1
        },

    },
    'modelInfo': {
        'beaker ': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '烧杯',
            'max_cn': 1
        },
        'yeast_li': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '酵母菌液',
            'max_cn': 1
        },
        'hand': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'clean_cloth': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '清洁布',
            'max_cn': 1
        },
        'glass_slide': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '载玻片',
            'max_cn': 1
        },
        'glass_cover': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '盖玻片',
            'max_cn': 1
        },
        'tweezer': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '镊子',
            'max_cn': 1
        },
        'dropper': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '滴管',
            'max_cn': 1
        },
        'ab_paper': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '吸水纸',
            'max_cn': 1
        },
        'coarse_ad': {
            'index': 9,
            'conf': 0.6,
            'CH_name': '粗准焦螺旋',
            'max_cn': 2
        },
        'fine_ad': {
            'index': 10,
            'conf': 0.6,
            'CH_name': '细准焦螺旋',
            'max_cn': 2
        },
        'stage': {
            'index': 11,
            'conf': 0.6,
            'CH_name': '载物台',
            'max_cn': 1
        },
        'reflector': {
            'index': 12,
            'conf': 0.6,
            'CH_name': '反光镜',
            'max_cn': 1
        },
        'clean_glass': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '清洁载玻片和盖玻片',
            'max_cn': 1
        },
        'drop_yeast': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '酵母菌滴在载玻片',
            'max_cn': 1
        },
        'cover_slide': {
            'index': 15,
            'conf': 0.5,
            'CH_name': '盖玻片盖在滴有酵母菌的载玻片上',
            'max_cn': 1
        },
        'ad_fine_ad': {
            'index': 16,
            'conf': 0.5,
            'CH_name': '调节细准焦螺旋',
            'max_cn': 1
        },
        'ad_coarse_ad': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '调节粗准焦螺旋',
            'max_cn': 1
        },
        'ab_paper_op': {
            'index': 18,
            'conf': 0.5,
            'CH_name': '吸水纸吸多余水',
            'max_cn': 1
        },
        'exchanger': {
            'index': 19,
            'conf': 0.5,
            'CH_name': '转换器',
            'max_cn': 1
        },
        'sma_oblense': {
            'index': 20,
            'conf': 0.5,
            'CH_name': '小物镜',
            'max_cn': 1
        },
        'big_oblense': {
            'index': 21,
            'conf': 0.5,
            'CH_name': '大物镜',
            'max_cn': 1
        },
        'tab_holder': {
            'index': 22,
            'conf': 0.5,
            'CH_name': '压片夹',
            'max_cn': 1
        },
        'head': {
            'index': 23,
            'conf': 0.5,
            'CH_name': '头',
            'max_cn': 1
        },
        'eye': {
            'index': 24,
            'conf': 0.5,
            'CH_name': '眼睛',
            'max_cn': 2
        },
        'th_hole': {
            'index': 25,
            'conf': 0.5,
            'CH_name': '通光孔',
            'max_cn': 1
        },
        'clear_im': {
            'index': 26,
            'conf': 0.5,
            'CH_name': '清晰的像',
            'max_cn': 2
        }
    }
}

if __name__ == '__main__':
    print(list(BZZGCJMJZP01['modelInfo'].keys()))
    print(len(list(BZZGCJMJZP01['modelInfo'].keys())))
