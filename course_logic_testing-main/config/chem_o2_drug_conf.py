CO2ZQYYP01 = {
	'name': '氧气的制取(有药品)',
	'experimentId': 'CO2ZQYYP01',  # 实验id
	'modelPath': 'chem_o2_drug/chem_o2_drug_v1.1.pt',
	'modelClass': 'CHEM_O2_drug',
	'camUse': ['top','front'],
    'labelInfo': ['l_tube_head',
                  'l_rubber_tube',
                  'l_hand',
                  'l_sink',
                  'l_burner',
                  'l_lamp_cap',
                  'l_container',
                  'l_coverglass',
                  'l_holder_bottom',
                  'l_holder_bottom_knob',
                  'l_holder_clip',
                  'l_tube',
                  'l_towel',
                  'l_save_tube',
                  'l_spoon',
                  'l_potassium_permanganate',
                  'l_sodium_chloride',
                  'l_matchbox',
                  'l_paper_slot',
                  'l_lighter',
                  'l_burner_bottom',
                  's_hand_tube_water_sink',
                  'l_tube_bottom',
                  's_burner_holder_tube',
                  'l_flame',
                  's_burner_holder_tube_sink',
                  's_burner_holder_tube_sink_hand',
                  'l_clear',
                  'l_burner_bottom_knob',
                  'l_spoon_chloride',
                  'l_spoon_permanganate',
                  'l_matches'],
    'scorePointInfo': {
        '1': {
            'info': '将导管伸入水中，用手捂试管或微热试管',
            'score': 0.5
        },
        '2': {
            'info': '导管口有气泡',
            'score': 1
        },
        '3': {
            'info': '按由下往上、从左至右的顺序搭建装置',
            'score': 1
        },
        '4': {
            'info': '铁甲夹在距离试管口三分之一处',
            'score': 0.5
        },
        '5': {
            'info': '试管口略向下倾斜',
            'score': 0.5
        },
        '6': {
            'info': '集气瓶盛满水，盖上毛玻璃片',
            'score': 0.5
        },
        '7': {
            'info': '将集气瓶倒置在水槽中',
            'score': 0.5
        },
        '8': {
            'info': '拆卸装置，整理桌面',
            'score': 0.5
        },
        '9': {
            'info': '添加药品',
            'score': 0.5
        },
        '10': {
            'info': '将药品送入到试管最底部',
            'score': 0.5
        },
        '11': {
            'info': '酒精灯加热',
            'score': 0.5
        },
        '12': {
            'info': '熄灭酒精灯',
            'score': 0.5
        },
    },
    'modelInfo': {
        'l_tube_head': {
            'index': 0,
            'conf': 0.5,
            'CH_name': '试管头（橡胶头）',
            'max_cn': 1
        },
        'l_rubber_tube': {
            'index': 1,
            'conf': 0.5,
            'CH_name': '橡胶管',
            'max_cn': 1
        },
        'l_hand': {
            'index': 2,
            'conf': 0.5,
            'CH_name': '手',
            'max_cn': 2
        },
        'l_sink': {
            'index': 3,
            'conf': 0.5,
            'CH_name': '水槽',
            'max_cn': 1
        },
        'l_burner': {
            'index': 4,
            'conf': 0.5,
            'CH_name': '酒精灯',
            'max_cn': 1
        },
        'l_lamp_cap': {
            'index': 5,
            'conf': 0.5,
            'CH_name': '灯帽',
            'max_cn': 1
        },
        'l_container': {
            'index': 6,
            'conf': 0.5,
            'CH_name': '容器',
            'max_cn': 2
        },
        'l_coverglass': {
            'index': 7,
            'conf': 0.5,
            'CH_name': '盖片',
            'max_cn': 1
        },
        'l_holder_bottom': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '支架底座',
            'max_cn': 1
        },
        'l_holder_bottom_knob': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '支架底座旋钮',
            'max_cn': 1
        },
        'l_holder_clip': {
            'index': 10,
            'conf': 0.5,
            'CH_name': '支架加试管的夹子',
            'max_cn': 1
        },
        'l_tube': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '试管',
            'max_cn': 1
        },
        'l_towel': {
            'index': 12,
            'conf': 0.5,
            'CH_name': '毛巾',
            'max_cn': 1
        },
        'l_save_tube': {
            'index': 13,
            'conf': 0.5,
            'CH_name': '存放试管架子',
            'max_cn': 1
        },
        'l_spoon': {
            'index': 14,
            'conf': 0.5,
            'CH_name': '勺子',
            'max_cn': 1
        },
        'l_potassium_permanganate': {
            'index': 15,
            'conf': 0.5,
            'CH_name': '高锰酸钾',
            'max_cn': 1
        },
        'l_sodium_chloride': {
            'index': 16,
            'conf': 0.5,
            'CH_name': '氯化钠',
            'max_cn': 1
        },
        'l_matchbox': {
            'index': 17,
            'conf': 0.5,
            'CH_name': '火柴盒',
            'max_cn': 1
        },
        'l_paper_slot': {
            'index': 18,
            'conf': 0.5,
            'CH_name': '纸槽',
            'max_cn': 1
        },
        'l_lighter': {
            'index': 19,
            'conf': 0.5,
            'CH_name': '点火器',
            'max_cn': 1
        },
        'l_burner_bottom': {
            'index': 20,
            'conf': 0.5,
            'CH_name': '酒精灯底座',
            'max_cn': 1
        },
        's_hand_tube_water_sink': {
            'index': 21,
            'conf': 0.3,
            'CH_name': '手握试管放在水中',
            'max_cn': 1
        },
        'l_tube_bottom': {
            'index': 22,
            'conf': 0.5,
            'CH_name': '试管底部（后期会有反应物）',
            'max_cn': 1
        },
        's_burner_holder_tube': {
            'index': 23,
            'conf': 0.3,
            'CH_name': '酒精灯+支架+试管',
            'max_cn': 1
        },
        'l_flame': {
            'index': 24,
            'conf': 0.5,
            'CH_name': '火焰',
            'max_cn': 1
        },
        's_burner_holder_tube_sink': {
            'index': 25,
            'conf': 0.3,
            'CH_name': '酒精灯+支架+试管+水槽',
            'max_cn': 1
        },
        's_burner_holder_tube_sink_hand': {
            'index': 26,
            'conf': 0.3,
            'CH_name': '酒精灯+支架+试管+水槽+手',
            'max_cn': 1
        },
        'l_clear': {
            'index': 27,
            'conf': 0.5,
            'CH_name': '清洁桌面',
            'max_cn': 1
        },
        'l_burner_bottom_knob': {
            'index': 28,
            'conf': 0.5,
            'CH_name': '酒精灯底座—旋钮',
            'max_cn': 1
        },
        'l_spoon_chloride': {
            'index': 29,
            'conf': 0.5,
            'CH_name': '勺子里氯化钠（白色）',
            'max_cn': 1
        },
        'l_spoon_permanganate': {
            'index': 30,
            'conf': 0.5,
            'CH_name': '勺子里高锰酸钾（黑色）',
            'max_cn': 1
        },
        'l_matches': {
            'index': 31,
            'conf': 0.5,
            'CH_name': 'undefined',
            'max_cn': 1
        }
    }

}
