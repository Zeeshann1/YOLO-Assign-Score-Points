CHEMSDHXXZ01 = {
    'name': '酸的化学性质',
    'experimentId': 'CHEMSDHXXZ01',  # 实验id
    'modelPath': 'chem_properties_of_acids_cou/chem_properties_of_acids_cou.pt',
    'modelClass': 'CHEM_properties_of_acids',
    'camUse': ['front', 'top', 'side'],
    'labelInfo': ['hand',
                  'test_tube',
                  'red_liquid_column',
                  'dropper',
                  'solution_reagent_bottle',
                  'HCHO_reagent_bottle',
                  'HCHO_liquid_column',
                  'Fe_reagent_bottle',
                  'tweezers',
                  'Zn_reagent_bottle',
                  'CuO_reagent_bottle',
                  'medicinal_ladle',
                  'burn_alcohol_lamp',
                  'hand_duster',
                  'clean_desk'],
    'scorePointInfo': {
        '1': {
            'info': '向试管中加入稀硫酸，滴加石蕊试液，振荡，观察并记录现象',
            'score': 1
        },
        '2': {
            'info': '取锌粒放入试管中，向试管中滴加稀硫酸，观察并记录现象',
            'score': 1
        },
        '3': {
            'info': '取生锈的铁钉放入试管中，向试管中滴加稀硫酸后加热，观察并记录现象',
            'score': 1
        },
        '4': {
            'info': '取少量氧化铜放入试管中，向试管中滴加稀硫酸后加热，观察并记录现象',
            'score': 2
        },
        '5': {
            'info': '向试管中加入组氣化钠溶液，滴加酚猷试液，振荡，再滴加稀硫酸，边滴边振荡，至溶液颜色发生变化，观察并记录现象',
            'score': 2
        },
        '6': {
            'info': '向试管中加入稀硫酸，滴加碳酸钠溶液，观察并记录现象',
            'score': 1
        },
        '7': {
            'info': '清洗仪器，整理桌面',
            'score': 1
        }
    },
    'modelInfo': {
        'hand': {
            'index': 0,
            'conf': 0.3,
            'CH_name': '手',
            'max_cn': 2
        },
        'test_tube': {
            'index': 1,
            'conf': 0.3,
            'CH_name': '试管',
            'max_cn': 3
        },
        'red_liquid_column': {
            'index': 2,
            'conf': 0.3,
            'CH_name': '红色液柱',
            'max_cn': 1
        },
        'dropper': {
            'index': 3,
            'conf': 0.3,
            'CH_name': '胶头滴管',
            'max_cn': 1
        },
        'solution_reagent_bottle': {
            'index': 4,
            'conf': 0.3,
            'CH_name': '溶液试剂瓶',
            'max_cn': 1
        },
        'HCHO_reagent_bottle': {
            'index': 5,
            'conf': 0.3,
            'CH_name': '石蕊试剂瓶',
            'max_cn': 1
        },
        'HCHO_liquid_column': {
            'index': 6,
            'conf': 0.3,
            'CH_name': '石蕊液柱',
            'max_cn': 1
        },
        'Fe_reagent_bottle': {
            'index': 7,
            'conf': 0.3,
            'CH_name': '铁锈试剂瓶',
            'max_cn': 1
        },
        'tweezers': {
            'index': 8,
            'conf': 0.3,
            'CH_name': '镊子',
            'max_cn': 1
        },
        'Zn_reagent_bottle': {
            'index': 9,
            'conf': 0.3,
            'CH_name': '锌粒试剂瓶',
            'max_cn': 1
        },
        'CuO_reagent_bottle': {
            'index': 10,
            'conf': 0.3,
            'CH_name': '氧化铜试剂瓶',
            'max_cn': 1
        },
        'medicinal_ladle': {
            'index': 11,
            'conf': 0.3,
            'CH_name': '药勺',
            'max_cn': 1
        },
        'burn_alcohol_lamp': {
            'index': 12,
            'conf': 0.3,
            'CH_name': '燃烧酒精灯',
            'max_cn': 1
        },
        'hand_duster': {
            'index': 13,
            'conf': 0.3,
            'CH_name': '手拿抹布',
            'max_cn': 1
        },
        'clean_desk': {
            'index': 14,
            'conf': 0.3,
            'CH_name': '清理桌面',
            'max_cn': 1
        }
    }
}
if __name__ == '__main__':
    print(list(CHEMSDHXXZ01['modelInfo'].keys()))