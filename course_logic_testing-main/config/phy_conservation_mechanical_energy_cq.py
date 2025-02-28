PYZJXNSHDL01 = {
    'name': '验证机械能守恒定律',
    'experimentId': 'PYZJXNSHDL01',  # 实验id
    'build_cdll_path': 'PHY_conservation_mechanical_energy/PHY_conservation_mechanical_energy.so',  # build/ 的RT文件
    'modelPath': 'PHY_conservation_mechanical_energy/PHY_conservation_mechanical_energy.pt',
    'modelPath_openvino': 'PHY_conservation_mechanical_energy/PHY_conservation_mechanical_energy.xml',
    'modelPath_tensorrt': 'PHY_conservation_mechanical_energy/PHY_conservation_mechanical_energy.engine',
    'modelClass': 'PHY_conservation_mechanical_energy_cou',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': [
                    "head",
                    "hand",
                    "ticker_timer",
                    "paper_tape",
                    "ruler",
                    "setsquare",
                    "pen",
                    "hand_pen",
                    "irosupport",
                    "weight",
                    "weight_paper",
                    "push_button",
                    "desktop"
                 ],#10 1
    'scorePointInfo': {
        '1': {
            'info': '把打点计时器竖直地固定在铁架台上',
            'score': 1
        },
        '2': {
            'info': '正确连线,检查振动片工作是否正常',
            'score': 1
        },
        '3': {
            'info': '纸带下端固定重物，上端穿过限位孔，上提纸带使重物靠近打点计时器',
            'score': 1
        },
        '4': {
            'info': '先接通电源,然后让重物由静止开始自由下落',
            'score': 1
        },
        '5': {
            'info': '打完一条纸带,及时断开电源',
            'score': 1
        },
        '6': {
            'info': '正确选择纸带,标上五个记数点',
            'score': 1
        },
        '7': {
            'info': '正确测量出各个要求的距离',
            'score': 1
        },
        '8': {
            'info': '计算UB、UD ，并填入表格',
            'score': 1,
            'value': True
        },
        '9': {
            'info': '计算物体从B点到D点减少的重力势能减少量和相应动能的增加量,比较后能得出正确结论',
            'score': 1,
            'value': True
        },
        '10': {
            'info': '布列器材便于操作；取放仪器运作规范；操作有条不紊；遵守纪律；做完实验，整理复原器材',
            'score': 1
        }
    },
    'faultPointInfo': {
        '1': {
            'info': '打点计时器平放地固定在铁架台上',
            'score': 0
        },
        '2': {
            'info': '打点计时器未固定紧',
            'score': 0
        },
        '3': {
            'info': '自由落体运动时，纸带未展平',
            'score': 0
        }
    },
    'modelInfo': {
        'head': {
            'index': 0,
            'conf': 0.65,
            'CH_name': '头',
            'max_cn': 1
        },
        'hand': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '手',
            'max_cn': 2
        },
        'ticker_timer': {
            'index': 2,
            'conf': 0.7,
            'CH_name': '打点计时器',
            'max_cn': 2
        },
        'paper_tape': {
            'index': 3,
            'conf': 0.4,
            'CH_name': '纸带',
            'max_cn': 2
        },
        'ruler': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '直尺',
            'max_cn': 1
        },
        'setsquare': {
            'index': 5,
            'conf': 0.4,
            'CH_name': '三角板',
            'max_cn': 1
        },
        'pen': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '笔',
            'max_cn': 3
        },
        'hand_pen': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '手拿笔',
            'max_cn': 1
        },
        'irosupport': {
            'index': 8,
            'conf': 0.3,
            'CH_name': '卡槽铁架台',
            'max_cn': 1
        },
        'weight': {
            'index': 9,
            'conf': 0.65,
            'CH_name': '重物',
            'max_cn': 1
        },
        'weight_paper': {
            'index': 10,
            'conf': 0.65,
            'CH_name': '重物纸带',
            'max_cn': 1
        },
        'push_button': {
            'index': 11,
            'conf': 0.26,
            'CH_name': '按压开关',
            'max_cn': 1
        },
        'desktop': {
            'index': 12,
            'conf': 0.65,
            'CH_name': '桌面',
            'max_cn': 1
        }
    }
}
