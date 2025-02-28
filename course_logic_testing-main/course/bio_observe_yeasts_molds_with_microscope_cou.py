#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 15:04
# @Author  : Qiguangnan
# @File    : bio_seed_starch_cou.py

from .comm import *
from .comm.course_base import ConfigModel


# from config.bio_observe_yeasts_molds_with_microscope import BXWJGCJMJHMJ01
# from utilsg.litF import uploaded_images, encode_image_jpg, upload_redis_or_save_json_local, ts2ft
# from configg.global_config import SCORE_ROOT_PATH
# from .comm import Plot
#
# from logger import logger


class BIO_observe_yeasts_molds(ConfigModel):
    def __init__(self):
        super(BIO_observe_yeasts_molds, self).__init__()

        self.wipe_conf = 0.0
        self.cover_conf = 0.0
        self.dye_conf = 0.0
        self.observe_conf = 0.0
        self.daub_conf = 0.0
        self.clean_conf = 0.0

        self.d_time = 0.

    def run_one_result_process(self, frame_top, frame_front, frame_side,
                               pred_top, pred_front, pred_side,
                               time_top, time_front, time_side,
                               num_frame_top,
                               num_frame_front,
                               num_frame_side,
                               path_save,
                               names_label):
        front_true = False
        top_true = False
        if pred_front != None and pred_front.shape[0]:
            front_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            front_true = True

        self.rtmp_push_fun(top_img=frame_top,front_img=frame_front,side_img=frame_side,
                           top_preds=None,front_preds=front_preds,side_preds=None)

        if front_true:
            # *-------------------------------------------------* 以下为赋分逻辑部分

            # [front_preds], [front_img0] = preds, img0s
            wipe, cover, dye, observe, daub, clean = front_preds

            # 1 擦拭载玻片与盖玻片
            if "1" in self.exper_score_ids and (not self.scorePoint1 and wipe.shape[0] != 0) \
                    or (wipe.shape[0] != 0 and self.wipe_conf < wipe[0][5]):
                self.wipe_conf = wipe[0][5]
                # self.assignScore(1, frame_front, front_preds)
                conf_c = self.wipe_conf
                self.assignScore(index=1,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="wipe_1.jpg",
                                 preds=front_preds
                                 )

            # 2 正确制作酵母菌培养液临时装片，盖玻片45°角一边先接触培养液再缓缓放下
            if "2" in self.exper_score_ids and (not self.scorePoint2 and cover.shape[0] != 0) \
                    or (cover.shape[0] != 0 and self.cover_conf < cover[0][5]):
                self.cover_conf = cover[0][5]
                # self.assignScore(2, frame_front, front_preds)
                conf_c = self.cover_conf
                self.assignScore(index=2,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="cover_2.jpg",
                                 preds=front_preds
                                 )

            # 3 染色时必须将临时装片从载物台上取下，在盖玻片的一边滴碘液，另一边用吸水纸吸引
            if "3" in self.exper_score_ids and (not self.scorePoint3 and dye.shape[0] != 0) \
                    or (dye.shape[0] != 0 and self.dye_conf < dye[0][5]):
                self.dye_conf = dye[0][5]
                # self.assignScore(3, frame_front, front_preds)
                conf_c = self.dye_conf
                self.assignScore(index=3,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="dye_3.jpg",
                                 preds=front_preds
                                 )

            # 4 用放大镜观察长有青霉的橘子皮
            if "4" in self.exper_score_ids and (not self.scorePoint4 and observe.shape[0] != 0) \
                    or (observe.shape[0] != 0 and self.observe_conf < observe[0][5]):
                self.observe_conf = observe[0][5]
                # self.assignScore(4, frame_front, front_preds)
                conf_c = self.observe_conf
                self.assignScore(index=4,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="observe_4.jpg",
                                 preds=front_preds
                                 )

            # 5 将解剖针上的青霉均匀涂抹在载玻片上
            if "5" in self.exper_score_ids and not self.scorePoint5 and daub.shape[0] != 0 \
                    or (daub.shape[0] != 0 and self.daub_conf < daub[0][5]):
                self.daub_conf = daub[0][5]
                # self.assignScore(5, frame_front, front_preds)
                conf_c = self.daub_conf
                self.assignScore(index=1,
                                 img=frame_front,
                                 object=objects_front,
                                 conf=conf_c,
                                 time_frame=time_front,
                                 num_frame=num_frame_front,
                                 name_save="daub_5.jpg",
                                 preds=front_preds
                                 )

            # 6 实验结束后能及时整理器材
            if "6" in self.exper_score_ids and (not self.scorePoint6 and clean.shape[0] != 0) \
                    or (clean.shape[0] != 0 and self.clean_conf < clean[0][5]):
                self.clean_conf = clean[0][5]
                # self.assignScore(6, frame_front, front_preds)
            conf_c = self.clean_conf
            self.assignScore(index=1,
                             img=frame_front,
                             object=objects_front,
                             conf=conf_c,
                             time_frame=time_front,
                             num_frame=num_frame_front,
                             name_save="clean_6.jpg",
                             preds=front_preds
                             )
