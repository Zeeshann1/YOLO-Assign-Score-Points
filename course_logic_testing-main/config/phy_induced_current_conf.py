PTJDTCCGYDL02 = {
    'name':
    '探究导体在磁场中运动时产生感应电流的条件(公开课)',
    'experimentId':
    'PTJDTCCGYDL02',  # 实验id
    'modelPath':
    'phy_induced_current/phy_induced_current_2.pt',
    'modelClass':
    'PHY_induced_current_2',
    'model_type':
    "yolo",
    'camUse': ['top', 'front'],
    'rotate_type':
    False,
    'labelInfo': [
        "电流表_顶视", "铁架台_顶视", "线圈穿过磁铁_顶视", "开关闭合_顶视", "开关断开_顶视", "线圈_顶视",
        "连接完成_顶视", "移动线圈_顶视", "桌面整洁_顶视", "铁架台_前视", "线圈穿过磁铁_前视", "线圈_前视",
        "开关闭合_前视", "开关断开_前视", "移动线圈_前视"
    ],  # 10 1
    'scorePointInfo': {
        '1': {
            'info': '将金属导体（线圈框）两端用细线系住后吊在铁架台上',
            'score': 1
        },
        '2': {
            'info': '将蹄形磁铁穿过金属导体（线圈框）后放在铁架台上',
            'score': 1
        },
        '3': {
            'info': '连接电路，连接过程中开关处于断开状态',
            'score': 1
        },
        '4': {
            'info': '用导线将灵敏电流计、金属导体（线圈框）、开关连接成电路',
            'score': 1
        },
        '5': {
            'info': '金属导体（线圈框）静止时，闭合开关观察灵敏电流计的示数',
            'score': 1
        },
        '6': {
            'info': '上下移动金属导体（线圈框一边）过程中，闭合开关观察灵敏电流计的示数',
            'score': 1
        },
        '7': {
            'info':
            '前后移动金属导体（线圈框一边）过程中，闭合开关使金属导体（线圈框一边）完全穿过蹄形磁铁再返回原来位置时，观察灵敏电流计的示数',
            'score': 1
        },
        '8': {
            'info': '拆除电路，整理实验器材',
            'score': 1
        }
    },
    'modelInfo': {
        '电流表_顶视': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '电流表',
            'max_cn': 5
        },
        '铁架台_顶视': {
            'index': 1,
            'conf': 0.65,
            'CH_name': '铁架台',
            'max_cn': 1
        },
        '线圈穿过磁铁_顶视': {
            'index': 2,
            'conf': 0.65,
            'CH_name': '线圈穿过磁铁',
            'max_cn': 5
        },
        '开关闭合_顶视': {
            'index': 3,
            'conf': 0.65,
            'CH_name': '开关闭合',
            'max_cn': 1
        },
        '开关断开_顶视': {
            'index': 4,
            'conf': 0.65,
            'CH_name': '开关断开',
            'max_cn': 1
        },
        '线圈_顶视': {
            'index': 5,
            'conf': 0.65,
            'CH_name': '线圈',
            'max_cn': 1
        },
        '连接完成_顶视': {
            'index': 6,
            'conf': 0.65,
            'CH_name': '连接完成',
            'max_cn': 1
        },
        '移动线圈_顶视': {
            'index': 7,
            'conf': 0.65,
            'CH_name': '移动线圈',
            'max_cn': 1
        },
        '桌面整洁_顶视': {
            'index': 8,
            'conf': 0.35,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
        '铁架台_前视': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '铁架台',
            'max_cn': 1
        },
        '线圈穿过磁铁_前视': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '线圈穿过磁铁',
            'max_cn': 1
        },
        '线圈_前视': {
            'index': 11,
            'conf': 0.65,
            'CH_name': '线圈',
            'max_cn': 1
        },
        '开关闭合_前视': {
            'index': 12,
            'conf': 0.65,
            'CH_name': '开关闭合',
            'max_cn': 1
        },
        '开关断开_前视': {
            'index': 13,
            'conf': 0.65,
            'CH_name': '开关断开',
            'max_cn': 1
        },
        '移动线圈_前视': {
            'index': 14,
            'conf': 0.65,
            'CH_name': '移动线圈',
            'max_cn': 1
        }
    }
}