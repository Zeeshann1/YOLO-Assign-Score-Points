BZZRKQZP01 = {
    'name':
    '制作人口腔临时装片',
    'experimentId':
    'BZZRKQZP01',  # 实验id
    'modelPath':
    'bio_make_kq/bio_make_kq.pt',
    'modelClass':
    'BIO_make_kq',
    'model_type':
    "yolo",
    'camUse': ['top', 'front', 'side'],
    'rotate_type':
    False,
    'labelInfo': [
        "手", "载玻片", "镊子", "洋葱", "取用洋葱", "滴清水", "滴碘液", "擦拭载玻片", "操作",
        "滴瓶_清水_取用", "滴瓶_清水_未取用", "滴瓶_碘液_取用", "滴瓶_碘液_未取用", "吸水", "喝水", "吐水",
        "取样"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '擦拭载玻片和盖玻片',
            'score': 1
        },
        '2': {
            'info': '用滴管在载玻片中央滴一滴生理盐水',
            'score': 1
        },
        '3': {
            'info': '用清水漱口',
            'score': 1
        },
        '4': {
            'info': '用消毒的牙签在自己的口腔内侧壁上轻轻刮几下',
            'score': 2
        },
        '5': {
            'info': '把牙签上附有碎屑的一端，放在载玻片的生理盐水中涂抹几下',
            'score': 1
        },
        '6': {
            'info': '用镊子夹住盖玻片一侧的边缘，使它的另一侧先接触水滴',
            'score': 2
        },
        '7': {
            'info': '将盖玻片缓缓放平，避免产生气泡',
            'score': 2
        },
        '8': {
            'info': '在盖玻片的一侧滴一滴碘酒',
            'score': 2,
        },
        '9': {
            'info': '用吸水纸从盖玻片的另一侧吸引，重复2～3次，使碘酒浸润标本的全部',
            'score': 1
        },
        '10': {
            'info': '对材料用具进行整理，恢复到实验前的状态',
            'score': 2,
        }
    },
    'modelInfo': {
        '手': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '手',
            'max_cn': 5
        },
        '载玻片': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '载玻片',
            'max_cn': 5
        },
        '镊子': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '工具',
            'max_cn': 2
        },
        '洋葱': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '洋葱',
            'max_cn': 4
        },
        '取用洋葱': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '取用洋葱',
            'max_cn': 1
        },
        '滴清水': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '滴生理盐水',
            'max_cn': 1
        },
        '滴碘液': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '滴碘液',
            'max_cn': 1
        },
        '擦拭载玻片': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '擦拭',
            'max_cn': 1
        },
        '操作': {
            'index': 8,
            'conf': 0.65,
            'CH_name': '操作',
            'max_cn': 1
        },
        '滴瓶_清水_取用': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '滴瓶_生理盐水_取用',
            'max_cn': 1
        },
        '滴瓶_清水_未取用': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '滴瓶_生理盐水_未取用',
            'max_cn': 1
        },
        '滴瓶_碘液_取用': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '滴瓶_碘液_取用',
            'max_cn': 1
        },
        '滴瓶_碘液_未取用': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '滴瓶_碘液_未取用',
            'max_cn': 1
        },
        '吸水': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '吸水',
            'max_cn': 1
        },
        '喝水': {
            'index': 14,
            'conf': 0.2,
            'CH_name': '漱口',
            'max_cn': 1
        },
        '吐水': {
            'index': 15,
            'conf': 0.2,
            'CH_name': '漱口',
            'max_cn': 1
        },
        '取样': {
            'index': 16,
            'conf': 0.2,
            'CH_name': '取样',
            'max_cn': 1
        },
    }
}
