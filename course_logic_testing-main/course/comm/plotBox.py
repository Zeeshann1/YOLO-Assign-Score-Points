#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/28 14:06
# @Author  : Qiguangnan
# @File    : plotBox.py


import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Plot:

    def __init__(
            self,
            labels,
            EN_CH_map=None,
            colors=None):
        """
        :param info_queue: (preds, imgs)
        :param labels: the labels of model
        :param colors: customize the colors for each class
        :param EN_CH_map: English Chinese map
        """
        self.labels = list(EN_CH_map.keys())
        if colors:
            self.colors = colors
        else:
            self.colors = [[0, 153, 255], [204, 153, 255], [102, 102, 255], [51, 0, 255], [204, 153, 0],
                           [204, 204, 153], [102, 204, 153], [102, 51, 102], [102, 153, 0], [153, 153, 153],
                           [255, 204, 204], [255, 102, 102], [255, 0, 51], [0, 153, 204], [204, 153, 153],
                           [255, 255, 0], [204, 204, 0], [0, 153, 255], [204, 153, 255], [102, 102, 255], [51, 0, 255],
                           [204, 153, 0], [204, 204, 153], [102, 204, 153], [102, 51, 102], [102, 153, 0],
                           [153, 153, 153], [255, 204, 204], [255, 102, 102], [255, 0, 51], [0, 153, 204],
                           [204, 153, 153], [255, 255, 0], [204, 204, 0],
                           [0, 153, 255], [204, 153, 255], [102, 102, 255], [51, 0, 255], [204, 153, 0],
                           [204, 204, 153], [102, 204, 153], [102, 51, 102], [102, 153, 0], [153, 153, 153],
                           [255, 204, 204], [255, 102, 102], [255, 0, 51], [0, 153, 204], [204, 153, 153],
                           [255, 255, 0], [204, 204, 0], [0, 153, 255], [204, 153, 255], [102, 102, 255], [51, 0, 255],
                           [204, 153, 0], [204, 204, 153], [102, 204, 153], [102, 51, 102], [102, 153, 0],
                           [153, 153, 153], [255, 204, 204], [255, 102, 102], [255, 0, 51], [0, 153, 204],
                           [204, 153, 153], [255, 255, 0], [204, 204, 0]]

        self.EN_CH_map = EN_CH_map
        if self.EN_CH_map:  ## 英文转中文
            # assert self.labels == list(self.EN_CH_map.keys())
            self.label_bg_map = {}
            self.label_bg()

    def label_bg(self):  ## Making Chinese background
        def CN_len(s):
            l = len(s)
            for char in s:
                if u'\u4e00' <= char <= u'\u9fa5':
                    l += 1
            return l

        for n, (key, value) in enumerate(self.EN_CH_map.items()):
            label_CHS = value  ## Chinese Label
            char_l = (CN_len(label_CHS) + 6) * 9  ## length of character
            bg_ch = np.array(self.colors[n], dtype=np.uint8)
            bg_ch = np.broadcast_to(bg_ch, (18, char_l, 3))
            pil_bg = Image.fromarray(bg_ch)
            draw = ImageDraw.Draw(pil_bg)
            fontStyle = ImageFont.truetype("./font/simhei.ttf", 18)
            draw.text((5, 0), label_CHS, (255, 255, 255), font=fontStyle)
            self.label_bg_map[key] = np.asarray(pil_bg)

    def plot(self, pred, img0):
        # for pred, img0 in zip(preds, img0s):
        # if pred.shape[0] == 0:
        #     return
        # for x1, y1, x2, y2, conf, cl in reversed(pred):
        #     self.plot_one_box(img0, x1, y1, x2, y2, conf, cl)
        for i, items in enumerate(pred):
            if items.shape[0] == 0:
                continue
            for *xyxy, in items:
                x1, y1, x2, y2, conf, cl = xyxy[0],xyxy[1],xyxy[2],xyxy[3],xyxy[4],xyxy[-1]#关键点格式xyxyx,conf,point,cl
                self.plot_one_box(img0, x1, y1, x2, y2, conf, i)
        return img0

        # def plot_one_box(self, img0, x1, y1, x2, y2, conf, cl):
        #     x1, y1, x2, y2, cl = int(x1), int(y1), int(x2), int(y2), int(cl)
        #     color = self.colors[cl]
        #     cv2.rectangle(img0, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)  # plot rectangle frame
        #     label_name = self.labels[cl]
        #     if self.EN_CH_map:
        #         text = f'{"  " * len(self.EN_CH_map[label_name])} {conf:.2f}'
        #         h, w, _ = img0.shape
        #         y, x, _ = self.label_bg_map[label_name].shape
        #         px, py = x1, y1
        #         if w - px < x:
        #             px = w - x
        #         if py < y:
        #             py = y
        #         img0[py - y:py, px:px + x] = self.label_bg_map[label_name]  ## Chinese characters background
        #         cv2.putText(img0, text, (px, py - 3), 0, 0.6, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
        #     else:
        #         text = f'{label_name} {conf:.2f}'
        #         t_size = cv2.getTextSize(text, 0, fontScale=0.6, thickness=2)[0]
        #         cv2.rectangle(img0, (x1 - 1, y1), (x1 + t_size[0], y1 - t_size[1] - 3), color, -1, cv2.LINE_AA)  # bg
        #         cv2.putText(img0, text, (x1, y1 - 3), 0, 0.6, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    def plot_one_box(self, img0, x1, y1, x2, y2, conf, i):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        color = self.colors[i]
        cv2.rectangle(img0, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)  # plot rectangle frame
        label_name = self.labels[i]
        if self.EN_CH_map:
            # text = f'{"  " * len(self.EN_CH_map[label_name])} {conf:.2f}'
            text = f'{conf:.2f}'
            h, w, _ = img0.shape
            y, x, _ = self.label_bg_map[label_name].shape
            px, py = x1, y1
            if w - px < x:
                px = w - x
            if py < y:
                py = y
            # print("py:{},y:{},px:{},x:{}".format(py,y,px,x))
            # print("img0:{},label_bg_map:{},::{}".format(img0.shape,self.label_bg_map[label_name].shape,img0[py - y:py, px:px + x].shape))
            try:
                img0[py - y:py, px:px + x] = self.label_bg_map[label_name]  ## Chinese characters background
            except:
                print("plot error", px, x, w)
            # cv2.putText(img0, text, (px, py - 3), 0, 0.6, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(img0, text, (px + x - 45, py - 3), 0, 0.6, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
        else:
            text = f'{label_name} {conf:.2f}'
            t_size = cv2.getTextSize(text, 0, fontScale=0.6, thickness=2)[0]
            cv2.rectangle(img0, (x1 - 1, y1), (x1 + t_size[0], y1 - t_size[1] - 3), color, -1, cv2.LINE_AA)  # bg
            cv2.putText(img0, text, (x1, y1 - 3), 0, 0.6, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    def __call__(self, preds, img0s, *args, **kwargs):
        return self.plot(preds, img0s)
