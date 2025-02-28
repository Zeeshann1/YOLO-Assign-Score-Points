PTJGYDLDXFX01 = {
    'name':
    '探究什么情况下磁可以生电(深圳)',
    'experimentId':
    'PTJGYDLDXFX01',  # 实验id
    'modelPath':
    'phy_induced_current_ration/phy_induced_current_ration.pt',
    'modelClass':
    'PHY_induced_current_ration',
    'model_type':
    "yolo",
    'camUse': ['top', 'front'],
    'rotate_type':
    False,
    'labelInfo': [
        "磁铁", "线圈", "电流表_顶视", "连接完成_顶视", "移动线圈_顶视", "移动线圈_前视",
        "磁铁_N_前视", "磁铁_S_前视", "G_顶视", "A_顶视", "磁铁_N_顶视", "磁铁_S_顶视", 
        "蓝色_顶视", "绿色_顶视"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '选择灵敏电流计进行实验',
            'score': 1
        },
        '2': {
            'info': '将蹄形磁铁按图所示放置,连接成闭合回路',
            'score': 1
        },
        '3': {
            'info': '连接成闭合回路',
            'score': 1
        },
        '4': {
            'info': '将蹄形磁铁N极在上,线圈向里运动(不是来回运动),正确报告电表偏转的方向',
            'score': 1,
            "type": 2
        },
        '5': {
            'info': '将蹄形磁铁N极在上,线圈向外运动(不是来回运动),正确报告电表偏转的方向',
            'score': 1,
            "type": 2
        },
        '6': {
            'info': '将蹄形磁铁S极在上,线圈向里运动(不是来回运动),正确报告电表偏转的方向',
            'score': 1,
            "type": 2
        },
        '7': {
            'info': '将蹄形磁铁S极在上,线圈向外运动(不是来回运动),正确报告电表偏转的方向',
            'score': 1,
            "type": 2
        },
        '8': {
            'info': '得出感应电流的方向与导体运动方向有关',
            'score': 1,
            "type": 1
        },
        '9': {
            'info': '得出感应电流的方向与磁场方向有关',
            'score': 1,
            "type": 1
        },
        '10': {
            'info': '实验结束后能及时整理器材,能和监考老师文明礼貌交流',
            'score': 1
        }
    },
    'modelInfo': {
        '磁铁': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '磁铁',
            'max_cn': 5
        },
        '线圈': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '线圈',
            'max_cn': 1
        },
        '电流表_顶视': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '电流_顶视',
            'max_cn': 2
        },
        '连接完成_顶视': {
            'index': 3,
            'conf': 0.55,
            'CH_name': '连接完成_顶视',
            'max_cn': 1
        },
        '移动线圈_顶视': {
            'index': 4,
            'conf': 0.65,
            'CH_name': '移动线圈_顶视',
            'max_cn': 1
        },
        '移动线圈_前视': {
            'index': 5,
            'conf': 0.65,
            'CH_name': '移动线圈_前视',
            'max_cn': 1
        },
        '磁铁_N_前视': {
            'index': 6,
            'conf': 0.65,
            'CH_name': '磁铁_N_前视',
            'max_cn': 5
        },
        '磁铁_S_前视': {
            'index': 7,
            'conf': 0.65,
            'CH_name': '磁铁_S_前视',
            'max_cn': 5
        },
        'G_顶视': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '灵敏电流计',
            'max_cn': 1
        },
        'A_顶视': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '电流表',
            'max_cn': 1
        },
        '磁铁_N_顶视': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '磁铁_N_顶视',
            'max_cn': 1
        },
        '磁铁_S_顶视': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '磁铁_S_顶视',
            'max_cn': 1
        },
        '蓝色_顶视': {
            'index': 12,
            'conf': 0.65,
            'CH_name': '蓝色电路板_顶视',
            'max_cn': 1
        },
        '绿色_顶视': {
            'index': 13,
            'conf': 0.65,
            'CH_name': '绿色电路板_顶视',
            'max_cn': 1
        },
        

    }
}