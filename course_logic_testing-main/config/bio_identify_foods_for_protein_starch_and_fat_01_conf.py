#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04 17:20
# @Author  : Qinhe
# @File    : bio_identify_foods_for_protein_starch_and_fat_01_conf.py


BJDSWZHYDBZDFHZF01 = {
    'name': '鉴定食物中含有蛋白质、淀粉和脂肪',
    'experimentId': 'BJDSWZHYDBZDFHZF01',
    'build_cdll_path': 'yolov5/weights/phy_measure_voltage/phy_measure_voltage_nx/libmyplugins.so',  # build/ 的RT文件
    'modelPath': 'bio_identify_foods/bio_identify_foods.pt',
    'modelPath_openvino': '',
    'modelPath_tensorrt': '',
    'modelClass': 'BIO_identify_foods',
    'camUse': ['top', 'side', 'front'],
    'labelInfo': {
        'flour ': 0,
        'dough': 1,
        'gelatinoid': 2,
        'peanut': 3,
        'wheat': 4,
        'slitting_peanut': 5,
        'crosscutting_peanut': 6,
        'slitting_wheat': 7,
        'crosscutting_wheat': 8,
        'iodine_solution': 9,
        'red_ink': 10,
        'dropper': 11,
        'dropper_water': 12,
        'dropper_starch': 13,
        'dropper_iodine_solution': 14,
        'dropper_red_ink': 15,
        'tube': 16,
        'volatile_liquid': 17,
        'tube_starch': 18,
        'tube_blue_liquid': 19,
        'tube_red_liquid ': 20,
        'tube_end': 21,
        'tube_top': 22,
        'liquid_level ': 23,
        'white_paper': 24,
        'press': 25,
        'grease': 26,
        'gauze': 27,
        'gauze_dough': 28,
        'blade': 29,
        'hand_blade': 30,
        'tweezers': 31,
        'tweezers_top': 32,
        'medicine_spoon': 33,
        'medicine_spoon_top': 34,
        'beaker': 35,
        'knead_dough': 36,
        'beaker_water': 37,
        'beaker_starch': 38,
        'clean': 39,
    },
    'scorePointInfo': {
        '1': {
            'info': '用药匙取适量面粉，加清水和成面团',
            'score': 1
        },
        '2': {
            'info': '用纱布包着面团',
            'score': 1
        },
        '3': {
            'info': '用纱布包着面团放入盛有清水的烧杯中，轻轻揉挤',
            'score': 1
        },
        '4': {
            'info': '充分揉挤至不再有白色物质从纱布中渗出来',
            'score': 2
        },
        '5': {
            'info': '打开纱布，展示黄白色的胶状物质',
            'score': 2,
        },
        '6': {
            'info': '用滴管吸取适量乳白色液体于试管中',
            'score': 1
        },
        '7': {
            'info': '如果取的量超过试管容积的1/3不得分',
            'score': 1,
        },
        '8': {
            'info': '滴加碘液得分，滴加红墨水不得分',
            'score': 2,
        },
        '9': {
            'info': '充分震荡摇匀试管',
            'score': 1
        },
        '10': {
            'info': '液体变蓝色',
            'score': 1,
        },
        '11': {
            'info': '取花生、小麦种子各一粒',
            'score': 1,
        },
        '12': {
            'info': '用单面刀片纵向切开',
            'score': 1
        },
        '13': {
            'info': '在白纸上A区域挤压花生种子',
            'score': 1,
        },
        '14': {
            'info': '在白纸上B区域挤压小麦种子',
            'score': 1,
        },
        '15': {
            'info': '记录白纸上哪片区域有油脂的斑点',
            'score': 2
        },
        '16': {
            'info': '将用过的实验材料放入废料槽中，其它实验用品归位，清洁桌面，举手示意实验完毕',
            'score': 1,
        },
    },
    'modelInfo': {
        'flour': {
            'index': 0,
            'conf': 0.6,
            'CH_name': '面粉',
            'max_cn': 1
        },
        'dough': {
            'index': 1,
            'conf': 0.6,
            'CH_name': '面团',
            'max_cn': 1
        },
        'gelatinoid': {
            'index': 2,
            'conf': 0.6,
            'CH_name': '黄白色的胶状物质',
            'max_cn': 1
        },
        'peanut': {
            'index': 3,
            'conf': 0.6,
            'CH_name': '花生',
            'max_cn': 1
        },
        'wheat': {
            'index': 4,
            'conf': 0.6,
            'CH_name': '小麦',
            'max_cn': 1
        },
        'slitting_peanut': {
            'index': 5,
            'conf': 0.6,
            'CH_name': '纵切花生',
            'max_cn': 2
        },
        'crosscutting_peanut': {
            'index': 6,
            'conf': 0.6,
            'CH_name': '横切花生',
            'max_cn': 2
        },
        'slitting_wheat': {
            'index': 7,
            'conf': 0.6,
            'CH_name': '纵切小麦',
            'max_cn': 2
        },
        'crosscutting_wheat': {
            'index': 8,
            'conf': 0.5,
            'CH_name': '横切小麦',
            'max_cn': 2
        },
        'iodine_solution': {
            'index': 9,
            'conf': 0.5,
            'CH_name': '碘液',
            'max_cn': 1
        },
        'red_ink': {
            'index': 10,
            'conf': 0.6,
            'CH_name': '红墨水',
            'max_cn': 1
        },
        'dropper': {
            'index': 11,
            'conf': 0.5,
            'CH_name': '胶头滴管',
            'max_cn': 4
        },
        'dropper_water': {
            'index': 12,
            'conf': 0.6,
            'CH_name': '胶头滴管清水',
            'max_cn': 1
        },
        'dropper_starch': {
            'index': 13,
            'conf': 0.6,
            'CH_name': '胶头滴管淀粉溶液',
            'max_cn': 1
        },
        'dropper_iodine_solution': {
            'index': 14,
            'conf': 0.6,
            'CH_name': '胶头滴管碘液',
            'max_cn': 1
        },

        'dropper_red_ink': {
            'index': 15,
            'conf': 0.6,
            'CH_name': '胶头滴管红墨水',
            'max_cn': 1
        },
        'tube': {
            'index': 16,
            'conf': 0.6,
            'CH_name': '试管',
            'max_cn': 4
        },
        'volatile_liquid': {
            'index': 17,
            'conf': 0.6,
            'CH_name': '震荡液体',
            'max_cn': 1
        },
        'tube_starch': {
            'index': 18,
            'conf': 0.6,
            'CH_name': '试管淀粉溶液',
            'max_cn': 1
        },
        'tube_blue_liquid': {
            'index': 19,
            'conf': 0.3,
            'CH_name': '蓝色液体',
            'max_cn': 1
        },
        'tube_red_liquid': {
            'index': 20,
            'conf': 0.6,
            'CH_name': '红色液体',
            'max_cn': 1
        },
        'tube_end': {
            'index': 21,
            'conf': 0.6,
            'CH_name': '试管尾',
            'max_cn': 1
        },
        'tube_top': {
            'index': 22,
            'conf': 0.6,
            'CH_name': '试管口',
            'max_cn': 1
        },
        'liquid_level': {
            'index': 23,
            'conf': 0.6,
            'CH_name': '液面',
            'max_cn': 1
        },
        'white_paper': {
            'index': 24,
            'conf': 0.6,
            'CH_name': '白纸',
            'max_cn': 1
        },
        'press': {
            'index': 25,
            'conf': 0.6,
            'CH_name': '按压',
            'max_cn': 12
        },
        'grease': {
            'index': 26,
            'conf': 0.6,
            'CH_name': '油脂印',
            'max_cn': 1
        },
        'gauze': {
            'index': 27,
            'conf': 0.6,
            'CH_name': '纱布',
            'max_cn': 1
        },
        'gauze_dough': {
            'index': 28,
            'conf': 0.5,
            'CH_name': '纱布包面团',
            'max_cn': 1
        },
        'blade': {
            'index': 29,
            'conf': 0.5,
            'CH_name': '刀片',
            'max_cn': 1
        },
        'hand_blade': {
            'index': 30,
            'conf': 0.6,
            'CH_name': '手拿刀片',
            'max_cn': 1
        },
        'tweezers': {
            'index': 31,
            'conf': 0.5,
            'CH_name': '镊子',
            'max_cn': 1
        },
        'tweezers_top': {
            'index': 32,
            'conf': 0.6,
            'CH_name': '镊子头',
            'max_cn': 1
        },
        'medicine_spoon': {
            'index': 33,
            'conf': 0.6,
            'CH_name': '药匙',
            'max_cn': 1
        },
        'medicine_spoon_top': {
            'index': 34,
            'conf': 0.6,
            'CH_name': '药匙头',
            'max_cn': 1
        },
        'beaker': {
            'index': 35,
            'conf': 0.6,
            'CH_name': '烧杯',
            'max_cn': 5
        },
        'knead_dough': {
            'index': 36,
            'conf': 0.6,
            'CH_name': '揉搓面团',
            'max_cn': 1
        },
        'beaker_water': {
            'index': 37,
            'conf': 0.6,
            'CH_name': '烧杯清水',
            'max_cn': 2
        },
        'beaker_starch': {
            'index': 38,
            'conf': 0.6,
            'CH_name': '烧杯淀粉溶液',
            'max_cn': 1
        },
        'clean': {
            'index': 39,
            'conf': 0.3,
            'CH_name': '整理桌面',
            'max_cn': 1
        },
    }
}
