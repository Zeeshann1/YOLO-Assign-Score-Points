#!/usr/bin/env python
# coding=utf-8

from deeplearn.yolov5s.models.hrnet_lite import get_model
import torch
import cv2
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import copy
import os
import torch.nn.functional as F
class Regresser():
    def __init__(self, device):
        self.model = get_model(1)
        checkpoint = torch.load("yolov5/weights/phy_convex_lens_imaging/heatmap_lite.pth", map_location = "cpu")
        self.model.load_state_dict(checkpoint)
        self.model.train(False)
        self.model.eval()
        self.device = device
        self.model.to(self.device)
        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((96*2,96)),
            transforms.ToTensor(),
        ])
    def __call__(self, pred_box, img):
        coarse_box = [int(0.5*pred_box[0] + 0.5 * pred_box[2]), int(0.5*pred_box[1] + 0.5 * pred_box[3]),pred_box[2]-pred_box[0],pred_box[3] - pred_box[1]]
        x, y, w, h = coarse_box
        xmin, ymin, xmax, ymax = int(x - 0.5 * w), int(y - 0.5 * h), int(x + 0.5 * w), int(y + 0.5 * h)
        r = 0.7
        crop_xmin = int(x - r*w)
        crop_ymin = int(y - r*h)
        crop_xmax = int(x + r*w)
        crop_ymax = int(y + r*h)
        crop_xmin = max(crop_xmin, 0)
        crop_ymin = max(crop_ymin, 0)
        crop_xmax = min(crop_xmax, 1920)
        crop_ymax = min(crop_ymax, 1080)
        roi = img[crop_ymin:crop_ymax, crop_xmin:crop_xmax]
        img_ = roi
        img_ = Image.fromarray(img_)
        img_ = self.transform(img_).unsqueeze(0)
        with torch.no_grad():
            img_ = img_.to(self.device)
            preds = self.model(img_)
            preds = preds.cpu()
            pred = (preds[0,0].numpy() * 255).astype(np.uint8)
            pred = cv2.resize(pred, (crop_xmax - crop_xmin, crop_ymax - crop_ymin))
            ret, mask = cv2.threshold(pred, 75, 255, cv2.THRESH_BINARY)
            ret, pts = self.get_kps_by_mask(mask)
            if ret:
                pts = np.array(pts, dtype = np.float).reshape((-1, 2))
                pts[:,0] += crop_xmin
                pts[:,1] += crop_ymin
            return ret, pts
    def get_kps_by_mask(self, mask_binary):
        def sort_res(res):
            final_res = []
            res_sort = sorted(res, key = lambda x:x[1])
            if res_sort[0][0] < res_sort[1][0]:
                final_res.append([res_sort[0][0], res_sort[0][1]])
                final_res.append([res_sort[1][0], res_sort[1][1]])
            else:
                final_res.append([res_sort[1][0], res_sort[1][1]])
                final_res.append([res_sort[0][0], res_sort[0][1]])
            if res_sort[2][0] < res_sort[3][0]:
                final_res.append([res_sort[3][0], res_sort[3][1]])
                final_res.append([res_sort[2][0], res_sort[2][1]])
            else:
                final_res.append([res_sort[2][0], res_sort[2][1]])
                final_res.append([res_sort[3][0], res_sort[3][1]])
            return final_res
        h,w = mask_binary.shape[:2]
        contours, _ = cv2.findContours(mask_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        res = []
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                #print(radius)
                res.append((x, y, radius))
        if len(res) == 4:
            return True, sort_res(res)
        elif len(res) < 4:
            return False, None
        else:
            res_sort = sorted(res, key = lambda x:x[1])
            res_tops = [t for t in res_sort if t[1] < h/2]
            res_bottoms = [t for t in res_sort if t[1] > h/2]
            res_tops = sorted(res_tops, key = lambda x: -x[-1])
            if len(res_tops)<2:
                return False, None
            res_tops = res_tops[:2]
            res_bottoms = sorted(res_bottoms, key = lambda x: -x[-1])
            if len(res_bottoms)<2:
                return False, None
            res_bottoms = res_bottoms[:2]
            return True, sort_res(res_tops + res_bottoms)
