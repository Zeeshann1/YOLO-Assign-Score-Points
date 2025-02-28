PTJGDFS01 = {
    'name': '探究光的反射规律',
    'experimentId': 'PTJGDFS01',  # 实验id
    'modelPath': 'phy_light_reflex/phy_reflex_video.pth',
    'modelClass': 'PHY_light_reflex',
    'model_type': "VideoModel",
    'seq_length': 16,
    'skip_num': 4,
    'padding': (31, 31, 0, 0), # 上下左右
    'crop_box': (148,0,480,270),# xmin ymin xmax ymax ,默认会先resize到原尺度的1/4
    'camUse': ['front'],
    'labelInfo': [
                "draw_angle",
                "draw_dotted_line",
                "draw_reflection_marks",
                "draw_solid_line",
                "grubbing_sth",
                "hands_up",
                "leave",
                "mark_reflection_point",
                "measure_angle",
                "open_laser",
                "prepare_or_clean",
                "putting_sth",
                "talking",
                "watching"
                ],#10 1
    'scorePointInfo': {
        '1': {
            'info': '将白纸和硬板垂直立在平面镜上',
            'score': 1
        },
        '2': {
            'info': '将激光笔射向平面镜，在白纸上标出入射点',
            'score': 1
        },
        '3': {
            'info': '画出入射光线和反射光线',
            'score': 1
        },
        '4': {
            'info': '画出法线，并标出入射角 i 和反射角 r',
            'score': 1
        },
        '5': {
            'info': '用量角器量出入射角 i 和反射角 r 的大小',
            'score': 1
        },
        '6': {
            'info': '实验结束后，将实验器材放回原处',
            'score': 1
        }
    },
    'modelInfo': {
        'draw_angle': {
            'index': 0,
            'conf': 0.8,
            'CH_name': '标记角度',
            'max_cn': 2
        },
        'draw_dotted_line': {
            'index': 1,
            'conf': 0.8,
            'CH_name': '画垂线',
            'max_cn': 1
        },
        'draw_reflection_marks': {
            'index': 2,
            'conf': 0.8,
            'CH_name': '标记入射/反射线',
            'max_cn': 2
        },
        'draw_solid_line': {
            'index': 3,
            'conf': 0.8,
            'CH_name': '画实线',
            'max_cn': 1
        },
        'grubbing_sth': {
            'index': 4,
            'conf': 0.8,
            'CH_name': '持笔',
            'max_cn': 1
        },
        'hands_up': {
            'index': 5,
            'conf': 0.8,
            'CH_name': '举手示意',
            'max_cn': 1
        },
        'leave': {
            'index': 6,
            'conf': 0.8,
            'CH_name': '(准备)离开座位',
            'max_cn': 1
        },
        'mark_reflection_point': {
            'index': 7,
            'conf': 0.8,
            'CH_name': '标记入射点',
            'max_cn': 1
        },
        'measure_angle': {
            'index': 8,
            'conf': 0.8,
            'CH_name': '测量角度',
            'max_cn': 1
        },
        'open_laser': {
            'index': 9,
            'conf': 0.8,
            'CH_name': '激光器打开',
            'max_cn': 1
        },
        'prepare_or_clean': {
            'index': 10,
            'conf': 0.8,
            'CH_name': '整理物品',
            'max_cn': 1
        },
        'putting_sth': {
            'index': 11,
            'conf': 0.8,
            'CH_name': '持(或按住)直尺',
            'max_cn': 1
        },
        'talking': {
            'index': 12,
            'conf': 0.8,
            'CH_name': '和老师沟通',
            'max_cn': 1
        },
        'watching': {
            'index': 13,
            'conf': 0.8,
            'CH_name': '视线稳定(在实验上)',
            'max_cn': 1
        },
    }
}

if __name__ == '__main__':
    print(list(PTJGDFS01['modelInfo'].keys()))
