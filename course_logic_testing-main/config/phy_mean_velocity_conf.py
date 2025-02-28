PCLWTDPJSD01 = {
    'name':
    '测量物体运动的平均速度',
    'experimentId':
    'PCLWTDPJSD01',  # 实验id
    'modelPath':
    'phy_mean_velocity/phy_mean_velocity.pt',
    'modelClass':
    'PHY_mean_velocity',
    'camUse': ['top', 'front'],
    'model_type':
    "yolo",
    'rotate_type':
    False,
    'labelInfo': [
        "baffle_top", "board_top", "timer_top", "prepare_top", "car_top",
        "inclined_plank_front", "prepare_front", "baffle_front",
        "clean_desk_top"
    ],  #10 1
    'scorePointInfo': {
        '1': {
            'info': '将木板的一端用木块垫起形成斜面',
            'score': 1
        },
        '2': {
            'info': '测量小车即将运动的路程并计入表格中',
            'score': 1
        },
        '3': {
            'info': '将小车从斜面顶端滑下，并开始计时，小车到达斜面底端时停止计时，记录小车的运动时间',
            'score': 1
        },
        '4': {
            'info': '将金属片移至斜面中部某处，测出小车的金属片的距离',
            'score': 1
        },
        '5': {
            'info': '测出小车从斜面顶端滑过斜面上半段路程所用的时间',
            'score': 1
        },
        '6': {
            'info': '将器材放回原位',
            'score': 1
        },
    },
    'modelInfo': {
        'baffle_top': {
            'index': 0,
            'conf': 0.55,
            'CH_name': '挡板',
            'max_cn': 5
        },
        'board_top': {
            'index': 1,
            'conf': 0.55,
            'CH_name': '木板',
            'max_cn': 1
        },
        'timer_top': {
            'index': 2,
            'conf': 0.55,
            'CH_name': '计时器',
            'max_cn': 5
        },
        'prepare_top': {
            'index': 3,
            'conf': 0.55,
            'CH_name': '准备放手小车',
            'max_cn': 5
        },
        'car_top': {
            'index': 4,
            'conf': 0.55,
            'CH_name': '小车',
            'max_cn': 1
        },
        'inclined_plank_front': {
            'index': 5,
            'conf': 0.45,
            'CH_name': '倾斜木板',
            'max_cn': 1
        },
        'prepare_front': {
            'index': 6,
            'conf': 0.55,
            'CH_name': '准备放手小车',
            'max_cn': 1
        },
        'baffle_front': {
            'index': 7,
            'conf': 0.55,
            'CH_name': '挡板',
            'max_cn': 1
        },
        'clean_desk_top': {
            'index': 8,
            'conf': 0.55,
            'CH_name': '桌面整洁',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PCLWTDPJSD01['modelInfo'].keys()))
