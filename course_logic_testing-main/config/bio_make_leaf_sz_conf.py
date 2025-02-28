BZZBCYZP01 = {
    'name':
    '制作叶表皮临时装片(深圳)',
    'experimentId':
    'BZZBCYZP01',  # 实验id
    'modelPath':
    'bio_make_leaf_sz/bio_make_leaf_sz.pt',
    'modelClass':
    'BIO_make_leaf_sz',
    'model_type':
    "yolo",
    'camUse': ['top', 'front', 'side'],
    'rotate_type':
    False,
    'labelInfo': [
        "手", "载玻片", "镊子", "菠菜叶_前视", "菠菜叶_顶视", "滴水", "擦拭载玻片", "废料缸", "操作",
        "滴瓶_取用", "滴瓶_未取用", "标签纸_红色", "标签纸_蓝色"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '选取清水实验',
            'score': 1
        },
        '2': {
            'info': '选叶片下表皮',
            'score': 1
        },
        '3': {
            'info': '用洁净的纱布擦拭载玻片和盖玻片',
            'score': 1
        },
        '4': {
            'info': '在载玻片中央滴加清水',
            'score': 1
        },
        '5': {
            'info': '撕下一小块叶片下表皮',
            'score': 1
        },
        '6': {
            'info': '将叶表皮置于载玻片的水滴中,并用镊子展平',
            'score': 1
        },
        '7': {
            'info': '用镊子夹起盖玻片,使它的一边先接触水滴,再缓缓放下',
            'score': 1
        },
        '8': {
            'info': '在实验记录卡中勾选 A',
            'score': 1,
            "type": 1
        },
        '9': {
            'info': '实验结束,将临时装片直接放入回收烧杯,整理并清洁桌面',
            'score': 1
        },
        '10': {
            'info': '有序正确完成各步骤,确认提交电子实验记录卡',
            'score': 1,
            "type": 1
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
        '菠菜叶_前视': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '菠菜叶',
            'max_cn': 4
        },
        '菠菜叶_顶视': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '菠菜叶',
            'max_cn': 4
        },
        '滴水': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '滴水',
            'max_cn': 1
        },
        '擦拭载玻片': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '擦拭',
            'max_cn': 1
        },
        '废料缸': {
            'index': 7,
            'conf': 0.65,
            'CH_name': '废料缸',
            'max_cn': 5
        },
        '操作': {
            'index': 8,
            'conf': 0.65,
            'CH_name': '操作',
            'max_cn': 1
        },
        '滴瓶_取用': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '滴瓶_取用',
            'max_cn': 2
        },
        '滴瓶_未取用': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '滴瓶_未取用',
            'max_cn': 2
        },
        '标签纸_红色': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '标签纸_红色',
            'max_cn': 3
        },
        '标签纸_蓝色': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '标签纸_蓝色',
            'max_cn': 3
        }
    }
}
BZZBCYZP02 = {
    'name':
    '制作叶表皮临时装片(盐城)',
    'experimentId':
    'BZZBCYZP02',  # 实验id
    'modelPath':
    'bio_make_leaf_yc/bio_make_leaf_yc.pt',
    'modelClass':
    'BIO_make_leaf_yc',
    'model_type':
    "yolo",
    'camUse': ['top', 'front', 'side'],
    'rotate_type':
    False,
    'labelInfo': [
        "手", "载玻片", "镊子", "菠菜叶_前视", "菠菜叶_顶视", "滴清水", "滴生理盐水", "擦拭载玻片", "操作",
        "滴瓶_清水_取用", "滴瓶_清水_未取用", "滴瓶_生理盐水_取用", "滴瓶_生理盐水_未取用", "吸水"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '选取清水实验',
            'score': 2
        },
        '2': {
            'info': '选叶片下表皮',
            'score': 2
        },
        '3': {
            'info': '用洁净的纱布擦拭载玻片和盖玻片',
            'score': 2
        },
        '4': {
            'info': '在载玻片中央滴加清水',
            'score': 2
        },
        '5': {
            'info': '撕下一小块叶片下表皮',
            'score': 2
        },
        '6': {
            'info': '将叶表皮置于载玻片的水滴中,并用镊子或解剖针展平',
            'score': 2
        },
        '7': {
            'info': '用镊子夹起盖玻片,使它的一边先接触水滴,再缓缓放下',
            'score': 2
        },
        '8': {
            'info': '用吸水纸将盖玻片周围多于水吸干',
            'score': 2,
        },
        '9': {
            'info': '实验结束,将临时装片直接放入回收烧杯,整理并清洁桌面',
            'score': 2
        },
        '10': {
            'info': '有序正确完成各步骤,确认提交电子实验记录卡',
            'score': 2,
            "type": 1
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
            'max_cn': 2
        },
        '镊子': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '工具',
            'max_cn': 2
        },
        '菠菜叶_前视': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '菠菜叶',
            'max_cn': 4
        },
        '菠菜叶_顶视': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '菠菜叶',
            'max_cn': 4
        },
        '滴清水': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '滴清水',
            'max_cn': 1
        },
        '滴生理盐水': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '滴生理盐水',
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
            'CH_name': '滴瓶_清水_取用',
            'max_cn': 1
        },
        '滴瓶_清水_未取用': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '滴瓶_清水_未取用',
            'max_cn': 1
        },
        '滴瓶_生理盐水_取用': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '滴瓶_生理盐水_取用',
            'max_cn': 1
        },
        '滴瓶_生理盐水_未取用': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '滴瓶_生理盐水_未取用',
            'max_cn': 1
        },
        '吸水': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '吸水',
            'max_cn': 1
        },
    }
}