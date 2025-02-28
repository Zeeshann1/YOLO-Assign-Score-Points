PTJYTNBYQGGK01 = {
	'name': '探究液体内部压强与那些因素有关(公共课)',
	'experimentId': 'PTJYTNBYQGGK01',  # 实验id
	'modelPath': "PHY_water_pressure_public/PHY_water_pressure_public_20220306.pt",
	'modelClass': 'PHY_water_pressure_public',
	'model_type':'yolo',
	'camUse': ['front'],
    'labelInfo': ['towel',
                     'bucket',
                     'hand',
                     'bucket_water_surfacews',
                     'bucket_water_column',
                     'u_water_surfacew',
                     'u',
                     'u_interface',
                     'metal_box',
                     'clip',
                     'knob',
                     'color_label',
                     'clear'],#21 1
	'faultPointInfo': {
        '1':{
            'info': '液体选择错误',
            'score': 0
        },
    },
    'scorePointInfo': {
        '1': {
            'info': '清水：深度1',
            'score': 1
        },
        '2': {
            'info': '清水：深度2',
            'score': 1
        },
        '3': {
            'info': '清水：深度3',
            'score': 1
        },
        '4': {
            'info': '清水：方向1',
            'score': 1
        },
        '5': {
            'info': '清水：方向2',
            'score': 1
        },
        '6': {
            'info': '清水：方向3',
            'score': 1
        },
        '7': {
            'info': '其他液体：深度1',
            'score': 1
        },
		'8': {
			'info': '其他液体：深度2',
			'score': 1
		},
		'9': {
			'info': '其他液体：深度3',
			'score': 1
		},
		'10': {
			'info': '其他液体：方向1',
			'score': 1
		},
		'11': {
			'info': '其他液体：方向2',
			'score': 1
		},
		'12': {
			'info': '其他液体：方向3',
			'score': 1
		},
		'13': {
			'info': '整理桌面',
			'score': 1
		},
    },
    'modelInfo': {
	'towel': {
		'index': 0,
		'conf': 0.5,
		'CH_name': '毛巾',
		'max_cn': 1
	},
	'bucket': {
		'index': 1,
		'conf': 0.5,
		'CH_name': '桶',
		'max_cn': 2
	},
	'hand': {
		'index': 2,
		'conf': 0.5,
		'CH_name': '手',
		'max_cn': 2
	},
	'bucket_water_surfacews': {
		'index': 3,
		'conf': 0.2,
		'CH_name': '桶_水面',
		'max_cn': 2
	},
	'bucket_water_column': {
		'index': 4,
		'conf': 0.5,
		'CH_name': '桶_水柱',
		'max_cn': 2
	},
	'u_water_surfacew': {
		'index': 5,
		'conf': 0.5,
		'CH_name': 'U型管水面',
		'max_cn': 2
	},
	'u': {
		'index': 6,
		'conf': 0.5,
		'CH_name': 'U型器',
		'max_cn': 1
	},
	'u_interface': {
		'index': 7,
		'conf': 0.5,
		'CH_name': 'U型接口',
		'max_cn': 1
	},
	'metal_box': {
		'index': 8,
		'conf': 0.5,
		'CH_name': '金属盒',
		'max_cn': 1
	},
	'clip': {
		'index': 9,
		'conf': 0.5,
		'CH_name': '夹子',
		'max_cn': 2
	},
	'knob': {
		'index': 10,
		'conf': 0.5,
		'CH_name': '旋钮',
		'max_cn': 1
	},
	'color_label': {
		'index': 11,
		'conf': 0.5,
		'CH_name': '颜色贴条',
		'max_cn': 1
	},
	'clear': {
		'index': 12,
		'conf': 0.5,
		'CH_name': '整理桌面',
		'max_cn': 1
	},
}

}
