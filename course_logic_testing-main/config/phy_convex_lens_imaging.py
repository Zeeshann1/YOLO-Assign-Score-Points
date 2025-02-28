PTJTTJCX01 = {
    'name':
    '探究凸透镜成像规律',
    'experimentId':
    'PTJTTJCX01',  # 实验id
    'modelPath':
    'phy_convex_lens_imaging/phy_convex_lens_imaging.pt',
    'modelClass':
    'PHY_convex_lens',
    'camUse': ['top', 'front'],
    'rotate_type':
    True,
    'labelInfo': [
        "head", "optical_source", "optical_screen", "convex_glass",
        "optical_bench", "optical_board", "clean_desk", "optical_screen_top",
        "convex_glass_top", "optical_bench_top", "optical_board_top",
        "clean_desk_top", "clear_image"
    ],  #10 1
    'scorePointInfo': {
        '1': {
            'info': '在光具座上按顺序放置光源、凸透镜和光屏',
            'score': 1
        },
        '2': {
            'info': '调整凸透镜、光屏的高度，使他们的中心和光源的中心大致在同一高度',
            'score': 1
        },
        '3': {
            'info': '寻找实像时，在光屏上出现像后，将光屏前后微调，直到像清晰为止',
            'score': 1
        },
        '4': {
            'info': '在光屏上找到缩小的像，观察并记录物距和像距以及成像情况',
            'score': 1
        },
        '5': {
            'info': '在光屏上找到等大的像，观察并记录物距和像距以及成像情况',
            'score': 1
        },
        '6': {
            'info': '在光屏上找到放大的像，观察并记录物距和像距以及成像情况',
            'score': 1
        },
        '7': {
            'info': '当u<f的时候，观察记录物距及成像情况',
            'score': 1
        },
        '8': {
            'info': '整理实验器材',
            'score': 1
        }
    },
    'modelInfo': {
        'head': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '头',
            'max_cn': 5
        },
        'optical_source': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '光源',
            'max_cn': 5
        },
        'optical_screen': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '光屏',
            'max_cn': 5
        },
        'convex_glass': {
            'index': 3,
            'conf': 0.65,
            'CH_name': '凸透镜',
            'max_cn': 5
        },
        'optical_bench': {
            'index': 4,
            'conf': 0.65,
            'CH_name': '光具座',
            'max_cn': 5
        },
        'optical_board': {
            'index': 5,
            'conf': 0.65,
            'CH_name': '光板',
            'max_cn': 5
        },
        'clean_desk': {
            'index': 6,
            'conf': 0.65,
            'CH_name': '桌面整洁',
            'max_cn': 5
        },
        'optical_screen_top': {
            'index': 7,
            'conf': 0.65,
            'CH_name': '光屏',
            'max_cn': 5
        },
        'convex_glass_top': {
            'index': 8,
            'conf': 0.65,
            'CH_name': '凸透镜',
            'max_cn': 5
        },
        'optical_bench_top': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '光具座',
            'max_cn': 5
        },
        'optical_board_top': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '光板',
            'max_cn': 5
        },
        'clean_desk_top': {
            'index': 11,
            'conf': 0.65,
            'CH_name': '桌面整洁',
            'max_cn': 5
        },
        'clear_image': {
            'index': 12,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 2
        }
    }
}

PTJTTJCX02 = {
    'name':
    '探究凸透镜成像规律(公开课)',
    'experimentId':
    'PTJTTJCX02',  # 实验id
    'modelPath':
    'phy_convex_lens_imaging/phy_convex_lens_imaging_2.pt',
    'modelClass':
    'PHY_convex_lens_2',
    'camUse': ['top', 'front'],
    'model_type':
    "yolo",
    #'crop_top': [300,1920-300,300,1080-150],w
    'rotate_type':
    False,
    'labelInfo': [
        "头", "光源_前视", "光屏_前视", "光源板_前视", "光具座_前视", "凸透镜_前视", "像_前视", "桌面整洁_前视",
        "光源_顶视", "光屏_顶视", "光源板_顶视", "像_顶视", "光具座_顶视", "凸透镜_顶视", "桌面整洁_顶视",
        "凸透镜_镜身_前视", "光屏_屏身_前视"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '观察并记录凸透镜的焦距',
            'score': 1
        },
        '2': {
            'info': '在光具座中央固定好凸透镜（一般放置在整数的刻度处，如50厘米处）',
            'score': 1
        },
        '3': {
            'info': '将LED光源和光屏放置在凸透镜两侧',
            'score': 1
        },
        '4': {
            'info': '调节凸透镜、光源和光屏三者的高度,使光源中心、凸透镜中心和光屏中心在同一高度上',
            'score': 1
        },
        '5': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离大于两倍焦距',
            'score': 1
        },
        '6': {
            'info': '移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止',
            'score': 1
        },
        '7': {
            'info': '观察成像特点，并记录物距和像距',
            'score': 1
        },
        '8': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离等于两倍焦距',
            'score': 1
        },
        '9': {
            'info': '移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止',
            'score': 1
        },
        '10': {
            'info': '观察成像特点，并记录物距和像距',
            'score': 1
        },
        '11': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离大于一倍焦距小于两倍焦距',
            'score': 1
        },
        '12': {
            'info': '移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止',
            'score': 1
        },
        '13': {
            'info': '观察成像特点，并记录物距和像距',
            'score': 1
        },
        '14': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离小于一倍焦距',
            'score': 1
        },
        '15': {
            'info': '移动光屏找像，观察光屏上是否有像',
            'score': 1
        },
        '16': {
            'info': '移去光屏，从光屏一侧透过凸透镜用眼睛观察像',
            'score': 1
        },
        '17': {
            'info': '观察并记录成像情况',
            'score': 1
        },
        '18': {
            'info': '完成实验并整理仪器',
            'score': 1
        }
    },
    # 'faultPointInfo':{
    #   '1': {
    #     'info': '凸透镜位置错误放置，光源、光屏不在凸透镜两侧',
    #     'score': 0
    #   },
    #   '2': {
    #     'info': '光源、凸透镜、光屏中心不等高',
    #     'score': 0
    #   }
    # },
    'modelInfo': {
        '头': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '头',
            'max_cn': 1
        },
        '光源_前视': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '光源',
            'max_cn': 1
        },
        '光屏_前视': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '光屏(安装好)',
            'max_cn': 1
        },
        '光源板_前视': {
            'index': 3,
            'conf': 0.65,
            'CH_name': '光源板(安装好)',
            'max_cn': 1
        },
        '光具座_前视': {
            'index': 4,
            'conf': 0.65,
            'CH_name': '光具座',
            'max_cn': 1
        },
        '凸透镜_前视': {
            'index': 5,
            'conf': 0.65,
            'CH_name': '凸透镜(安装好)',
            'max_cn': 1
        },
        '像_前视': {
            'index': 6,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 1
        },
        '桌面整洁_前视': {
            'index': 7,
            'conf': 0.65,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        '光源_顶视': {
            'index': 8,
            'conf': 0.65,
            'CH_name': '光源',
            'max_cn': 1
        },
        '光屏_顶视': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '光屏(安装好)',
            'max_cn': 1
        },
        '光源板_顶视': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '光源板(安装好)',
            'max_cn': 1
        },
        '像_顶视': {
            'index': 11,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 1
        },
        '光具座_顶视': {
            'index': 12,
            'conf': 0.65,
            'CH_name': '光具座',
            'max_cn': 1
        },
        '凸透镜_顶视': {
            'index': 13,
            'conf': 0.65,
            'CH_name': '凸透镜(安装好)',
            'max_cn': 1
        },
        '桌面整洁_顶视': {
            'index': 14,
            'conf': 0.65,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        '凸透镜_镜身_前视': {
            'index': 15,
            'conf': 0.65,
            'CH_name': '凸透镜',
            'max_cn': 1
        },
        '光屏_屏身_前视': {
            'index': 16,
            'conf': 0.65,
            'CH_name': '光屏',
            'max_cn': 1
        }
    }
}
PTJTTJCX03 = {
    'name':
    '探究凸透镜成像规律(蜡烛)',
    'experimentId':
    'PTJTTJCX03',  # 实验id
    'modelPath':
    'phy_convex_lens_imaging/phy_convex_lens_imaging_3.pt',
    'modelClass':
    'PHY_convex_lens_3',
    'camUse': ['top', 'front'],
    'model_type':
    "yolo",
    #'crop_top': [300,1920-300,300,1080-150],w
    'rotate_type':
    False,
    'labelInfo': [
        "头", "光源_前视", "光屏_前视", "光源板_前视", "光具座_前视", "凸透镜_前视", "像_前视", "桌面整洁_前视",
        "光源_顶视", "光屏_顶视", "光源板_顶视", "像_顶视", "光具座_顶视", "凸透镜_顶视", "桌面整洁_顶视",
        "凸透镜_镜身_前视", "光屏_屏身_前视", "火焰_光源_前视", "火焰_光源_顶视", "蜡烛_前视", "蜡烛_顶视",
        "火焰_像_前视", "火焰_像_顶视"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '观察并记录凸透镜的焦距',
            'score': 1
        },
        '2': {
            'info': '在光具座中央固定好凸透镜（一般放置在整数的刻度处，如50厘米处）',
            'score': 1
        },
        '3': {
            'info': '将火焰光源和光屏放置在凸透镜两侧',
            'score': 1
        },
        '4': {
            'info': '调节凸透镜、光源和光屏三者的高度,使光源中心、凸透镜中心和光屏中心在同一高度上',
            'score': 1
        },
        '5': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离大于两倍焦距',
            'score': 1
        },
        '6': {
            'info': '移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止',
            'score': 1
        },
        '7': {
            'info': '观察成像特点，并记录物距和像距',
            'score': 1
        },
        '8': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离等于两倍焦距',
            'score': 1
        },
        '9': {
            'info': '移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止',
            'score': 1
        },
        '10': {
            'info': '观察成像特点，并记录物距和像距',
            'score': 1
        },
        '11': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离大于一倍焦距小于两倍焦距',
            'score': 1
        },
        '12': {
            'info': '移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止',
            'score': 1
        },
        '13': {
            'info': '观察成像特点，并记录物距和像距',
            'score': 1
        },
        '14': {
            'info': '移动光源到某个位置，使光源离开凸透镜的距离小于一倍焦距',
            'score': 1
        },
        '15': {
            'info': '移动光屏找像，观察光屏上是否有像',
            'score': 1
        },
        '16': {
            'info': '移去光屏，从光屏一侧透过凸透镜用眼睛观察像',
            'score': 1
        },
        '17': {
            'info': '观察并记录成像情况',
            'score': 1
        },
        '18': {
            'info': '完成实验并整理仪器',
            'score': 1
        }
    },
    # 'faultPointInfo':{
    #   '1': {
    #     'info': '凸透镜位置错误放置，光源、光屏不在凸透镜两侧',
    #     'score': 0
    #   },
    #   '2': {
    #     'info': '光源、凸透镜、光屏中心不等高',
    #     'score': 0
    #   }
    # },
    'modelInfo': {
        '头': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '头',
            'max_cn': 1
        },
        '光源_前视': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '光源',
            'max_cn': 1
        },
        '光屏_前视': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '光屏(安装好)',
            'max_cn': 1
        },
        '光源板_前视': {
            'index': 3,
            'conf': 0.65,
            'CH_name': '光源板(安装好)',
            'max_cn': 1
        },
        '光具座_前视': {
            'index': 4,
            'conf': 0.65,
            'CH_name': '光具座',
            'max_cn': 1
        },
        '凸透镜_前视': {
            'index': 5,
            'conf': 0.65,
            'CH_name': '凸透镜(安装好)',
            'max_cn': 1
        },
        '像_前视': {
            'index': 6,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 1
        },
        '桌面整洁_前视': {
            'index': 7,
            'conf': 0.65,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        '光源_顶视': {
            'index': 8,
            'conf': 0.65,
            'CH_name': '光源',
            'max_cn': 1
        },
        '光屏_顶视': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '光屏(安装好)',
            'max_cn': 1
        },
        '光源板_顶视': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '光源板(安装好)',
            'max_cn': 1
        },
        '像_顶视': {
            'index': 11,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 1
        },
        '光具座_顶视': {
            'index': 12,
            'conf': 0.65,
            'CH_name': '光具座',
            'max_cn': 1
        },
        '凸透镜_顶视': {
            'index': 13,
            'conf': 0.65,
            'CH_name': '凸透镜(安装好)',
            'max_cn': 1
        },
        '桌面整洁_顶视': {
            'index': 14,
            'conf': 0.65,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        '凸透镜_镜身_前视': {
            'index': 15,
            'conf': 0.65,
            'CH_name': '凸透镜',
            'max_cn': 1
        },
        '光屏_屏身_前视': {
            'index': 16,
            'conf': 0.65,
            'CH_name': '光屏',
            'max_cn': 1
        },
        '火焰_光源_前视': {
            'index': 17,
            'conf': 0.65,
            'CH_name': '火焰',
            'max_cn': 1
        },
        '火焰_光源_顶视': {
            'index': 18,
            'conf': 0.65,
            'CH_name': '火焰',
            'max_cn': 1
        },
        '蜡烛_前视': {
            'index': 19,
            'conf': 0.65,
            'CH_name': '蜡烛',
            'max_cn': 1
        },
        '蜡烛_顶视': {
            'index': 20,
            'conf': 0.65,
            'CH_name': '蜡烛',
            'max_cn': 1
        },
        '火焰_像_前视': {
            'index': 21,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 1
        },
        '火焰_像_顶视': {
            'index': 22,
            'conf': 0.65,
            'CH_name': '像',
            'max_cn': 1
        },
    }
}
if __name__ == '__main__':
    print(list(PTJTTJCX02['modelInfo'].keys()))
