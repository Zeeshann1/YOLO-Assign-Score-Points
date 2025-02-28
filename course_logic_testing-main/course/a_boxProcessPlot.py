#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 10:49
# @Author  : Qiguangnan
# @File    : a_boxProcessPlot.py


import cv2
import torch
import torchvision
import numpy as np
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PIL import Image, ImageDraw, ImageFont


class BPP(QThread):
    send_frame = pyqtSignal(object)

    def __init__(self, detectQueue, boxQueue):
        super(BPP, self).__init__()
        self.detectQueue = detectQueue
        self.boxQueue = boxQueue
        self.nms = NMS([])

    def setNMS(self,
               names,
               conf_thres_base=0.3,
               iou_thres_base=0.45,
               conf_thres_list=None,
               iou_thres_list=None,
               max_cn_list=None,
               colors=None,
               EN_CH_map=None
               ):
        self.nms = NMS(names, conf_thres_base, iou_thres_base, conf_thres_list, iou_thres_list, max_cn_list, colors,
                       EN_CH_map)

    def run(self):

        while True:
            if self.detectQueue.empty():
                self.msleep(10)
                continue
            else:
                preds, shape0, shape1, img0s = self.detectQueue.get()
                preds = self.nms.non_max_suppression(preds, shape0, shape1)
                self.boxQueue.put((preds, img0s))
                self.nms.plot(preds, img0s)
                self.send_frame.emit(img0s[0])


class NMS:

    def __init__(
            self,
            names,
            conf_thres_base=0.6,
            iou_thres_base=0.45,
            conf_thres_list=None,
            iou_thres_list=None,
            max_cn_list=None,
            colors=None,
            EN_CH_map=None):
        """
        :param info_queue: (preds, imgs)
        :param names: the names of model
        :param conf_thres_base: basic confidence threshold for all classes
        :param iou_thres_base:  basic iou threshold for all classes
        :param conf_thres_list: confidence threshold for each class
        :param iou_thres_list:  iou threshold for each class
        :param max_cn_list:  maximum number of each class， 0 indicates that the number is uncertain
        :param colors: customize the colors for each class
        :param EN_CH_map: English Chinese map
        """
        self.names = names
        self.conf_thres_list = conf_thres_list
        if self.conf_thres_list:
            self.conf_thres_base = min(self.conf_thres_list)
        else:
            self.conf_thres_base = conf_thres_base
        self.iou_thres_list = iou_thres_list

        if self.iou_thres_list:
            self.iou_thres_base = min(self.iou_thres_list)
        else:
            self.iou_thres_base = iou_thres_base
            self.iou_thres_list = [self.iou_thres_base] * len(self.names)

        self.max_cn_list = max_cn_list
        if self.max_cn_list is None:
            self.max_cn_list = [0] * len(self.names)
        if colors:
            self.colors = colors
        else:
            # self.colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255], [255, 0, 255],
            #                [255, 127, 0], [0, 255, 127], [127, 0, 255], [127, 255, 0], [0, 127, 255], [255, 0, 127],
            #                [191, 63, 255], [255, 63, 191], [191, 255, 63], [255, 127, 127], [127, 255, 127],
            #                [127, 127, 255], [63, 255, 191], [63, 191, 255], [255, 191, 63], [63, 127, 191],
            #                [63, 191, 127], [191, 63, 127], [191, 191, 63], [191, 63, 191], [63, 191, 191],
            #                [127, 127, 0], [127, 0, 127], [0, 127, 127], [127, 0, 0], [0, 127, 0], [0, 0, 127],
            #                [63, 63, 191], [63, 191, 63], [191, 63, 63], [191, 127, 63], [127, 63, 191], [127, 191, 63],
            #
            #                [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255], [255, 0, 255],
            #                [255, 127, 0], [0, 255, 127], [127, 0, 255], [127, 255, 0], [0, 127, 255], [255, 0, 127],
            #                [191, 63, 255], [255, 63, 191], [191, 255, 63], [255, 127, 127], [127, 255, 127],
            #                [127, 127, 255], [63, 255, 191], [63, 191, 255], [255, 191, 63], [63, 127, 191],
            #                [63, 191, 127], [191, 63, 127], [191, 191, 63], [191, 63, 191], [63, 191, 191],
            #                [127, 127, 0], [127, 0, 127], [0, 127, 127], [127, 0, 0], [0, 127, 0], [0, 0, 127],
            #                [63, 63, 191], [63, 191, 63], [191, 63, 63], [191, 127, 63], [127, 63, 191], [127, 191, 63]
            #                ]
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
            assert self.names == list(self.EN_CH_map.keys())
            self.label_bg_map = {}
            self.label_bg()

    def label_bg(self):  ## Making Chinese background
        for n, (key, value) in enumerate(self.EN_CH_map.items()):
            name_CHS = value  ## Chinese Label
            char_l = (len(name_CHS) * 2 + 7) * 9  ## length of character
            bg_ch = np.array(self.colors[n], dtype=np.uint8)
            bg_ch = np.broadcast_to(bg_ch, (18, char_l, 3))
            pil_bg = Image.fromarray(bg_ch)
            draw = ImageDraw.Draw(pil_bg)
            fontStyle = ImageFont.truetype("simsun.ttc", 18)
            draw.text((5, 0), name_CHS, (255, 255, 255), font=fontStyle)
            self.label_bg_map[key] = np.asarray(pil_bg)

    def plot(self, preds, img0s):
        for pred, img0 in zip(preds, img0s):
            # if pred.shape[0] == 0:
            #     return
            # for x1, y1, x2, y2, conf, cl in reversed(pred):
            #     self.plot_one_box(img0, x1, y1, x2, y2, conf, cl)
            for items in reversed(pred):
                if items.shape[0] == 0:
                    continue
                for x1, y1, x2, y2, conf, cl in items:
                    self.plot_one_box(img0, x1, y1, x2, y2, conf, cl)

    def plot_one_box(self, img0, x1, y1, x2, y2, conf, cl):
        x1, y1, x2, y2, cl = int(x1), int(y1), int(x2), int(y2), int(cl)
        color = self.colors[cl]
        cv2.rectangle(img0, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)  # plot rectangle frame
        name = self.names[cl]
        if self.EN_CH_map:
            label = f'{"  " * len(self.EN_CH_map[name])} {conf:.2f}'
            h, w, _ = img0.shape
            y, x, _ = self.label_bg_map[name].shape
            px, py = x1, y1
            if w - px < x:
                px = w - x
            if py < y:
                py = y
            img0[py - y:py, px:px + x] = self.label_bg_map[name]  ## Chinese characters background
        else:
            label = f'{name} {conf:.2f}'
            t_size = cv2.getTextSize(label, 0, fontScale=0.6, thickness=2)[0]
            cv2.rectangle(img0, (x1 - 1, y1), (x1 + t_size[0], y1 - t_size[1] - 3), color, -1, cv2.LINE_AA)  # bg
        cv2.putText(img0, label, (x1, y1 - 3), 0, 0.6, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    def non_max_suppression(self, prediction, shape0, shape1):
        nc = prediction.shape[2] - 5  # number of classes
        xc = prediction[..., 4] > self.conf_thres_base  # candidates
        max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()

        # output = [torch.zeros((0, 6), device=prediction.device)] * prediction.shape[0]
        output = []
        for xi, x in enumerate(prediction):
            x = x[xc[xi]]  # confidence
            if not x.shape[0]:
                continue
            # Compute conf
            x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf
            # Box (center x, center y, width, height) to (x1, y1, x2, y2)
            box = self.xywh2xyxy(x[:, :4])
            # Detections matrix nx6 (xyxy, conf, cls)
            i, j = (x[:, 5:] > self.conf_thres_base).nonzero(as_tuple=False).T
            x = torch.cat((box[i], x[i, j + 5, None], j[:, None].float()), 1)
            # Check shape
            n = x.shape[0]  # number of boxes
            if not n:  # no boxes
                continue
            elif n > max_nms:  # excess boxes
                x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence

            # NMS 对每一类分别进行nms 坐标转换回原图
            # res = torch.zeros((0, 6), device=prediction.device)
            res = []
            for i in range(nc):  ## 对每个类进行最大抑制
                max_cn = self.max_cn_list[i]  # 该类别最大的数量
                ca = x[x[:, 5] == i]  ## 单类别结果
                if self.conf_thres_list:
                    ca = ca[ca[:, 4] > self.conf_thres_list[i]]
                if ca.shape[0] != 0:
                    boxes, scores = ca[:, :4], ca[:, 4]
                    index = torchvision.ops.nms(boxes, scores, self.iou_thres_list[i])
                    ca = ca[index]
                    if max_cn != 0 and ca.shape[0] > max_cn:
                        ca = ca[ca[:, 4].argsort(descending=True)][:max_cn]
                    ca[:, :4] = self.scale_coords(shape0, ca[:, :4], shape1).round()
                # res = torch.cat((res, ca), 0)
                res.append(ca)
            output.append(res)
        return output

    def xywh2xyxy(self, x):
        # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
        return y

    def clip_coords(self, boxes, img_shape):
        # Clip bounding xyxy bounding boxes to image shape (height, width)
        boxes[:, 0].clamp_(0, img_shape[1])  # x1
        boxes[:, 1].clamp_(0, img_shape[0])  # y1
        boxes[:, 2].clamp_(0, img_shape[1])  # x2
        boxes[:, 3].clamp_(0, img_shape[0])  # y2

    def scale_coords(self, img0_shape, coords, img1_shape):
        # Rescale coords (xyxy) from img1_shape to img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new

        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
        coords[:, [0, 2]] -= pad[0]  # x padding
        coords[:, [1, 3]] -= pad[1]  # y padding
        coords[:, :4] /= gain
        self.clip_coords(coords, img0_shape)
        return coords
