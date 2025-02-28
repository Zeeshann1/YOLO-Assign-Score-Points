from logger import logger
from .comm import *
from .comm.course_base import ConfigModel
import copy


def iou(box1, box2):
    xmin = max(box1[0], box2[0])
    ymin = max(box1[1], box2[1])
    xmax = min(box1[2], box2[2])
    ymax = min(box1[3], box2[3])
    if xmax <= xmin or ymax < ymin:
        return 0

    inter_area = (ymax - ymin) * (xmax - xmin)
    if inter_area <= 0:
        return 0
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    if area1 <= 0:
        return 0
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    if area2 <= 0:
        return 0

    return inter_area / (area1 + area2 - inter_area)


class PHY_mechanical_efficiency(ConfigModel):
    def __init__(self):
        super(PHY_mechanical_efficiency, self).__init__()
        self.initScore()

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 8
        self.labels = [
            "hand", "board_front", "weight_beam", "block",
            "weight_beam_zero_vertical", "clean_desk_front",
            "weight_beam_zero_horizontal", "height",
            "pull_weight_beam_vertical", "board_top", "weight_top",
            "towel_top", "clean_desk_top", "pull_weight_beam_horizontal"
        ]
        self.images = []

    def exp_filter(self, d):
        d_new = {"top": dict(), "front": dict()}
        d_top = d["top"]
        d_front = d["front"]
        for key, vals in d_top.items():
            if key in [
                    "board_top", "weight_beam", "block", "hand",
                    "weight_beam_zero_horizontal",
                    "pull_weight_beam_horizontal", "towel_top", "weight_top",
                    "clean_desk_top"
            ]:
                d_new["top"][key] = vals

        for key, vals in d_front.items():
            if key in [
                    "board_front", "weight_beam", "block", "hand",
                    "weight_beam_zero_vertical", "height",
                    "pull_weight_beam_vertical", "clean_desk_front"
            ]:
                d_new["front"][key] = vals
        return d_new

    def run_one_result_process(
            self, frame_top, frame_front, frame_side, pred_top, pred_front,
            pred_side, time_top, time_front, time_side, num_frame_top,
            num_frame_front, num_frame_side, path_save, names_label):
        self.time_top = time_top
        self.time_front = time_front
        self.time_side = time_side
        self.num_frame_top = num_frame_top
        self.num_frame_front = num_frame_front
        self.num_frame_side = num_frame_side
        self.frame_top = frame_top
        self.frame_front = frame_front
        self.frame_side = frame_side
        self.image = frame_front
        top_true = False
        front_true = False

        if pred_top != None and pred_top.shape[0]:
            self.preds_top, self.objects_top = self.assign_labels(
                frame_top, pred_top, names_label)
            top_true = True
        if pred_front != None and pred_front.shape[0]:
            self.preds_front, self.objects_front = self.assign_labels(
                frame_front, pred_front, names_label)
            front_true = True
        if top_true and front_true:
            self.pred = self.preds_front
            self.rtmp_push_fun(
                top_img=frame_top,
                front_img=frame_front,
                side_img=frame_side,
                top_preds=self.preds_top,
                front_preds=self.preds_front,
                side_preds=None)

            def assign_score_fun(index, view):
                if view == "front":
                    self.assignScore(
                        index=index,
                        img=self.frame_front,
                        object=self.objects_front,
                        conf=0.1,
                        time_frame=self.time_front,
                        num_frame=self.num_frame_front,
                        name_save=f"{index}.jpg",
                        preds=self.preds_front)
                elif view == "top":
                    self.assignScore(
                        index=index,
                        img=self.frame_top,
                        object=self.objects_top,
                        conf=0.1,
                        time_frame=self.time_top,
                        num_frame=self.num_frame_top,
                        name_save=f"{index}.jpg",
                        preds=self.preds_top)

            def assign_score_fun2(index, img, pred):
                self.assignScore(
                    index=index,
                    img=img,
                    object=self.objects_front,
                    conf=0.1,
                    time_frame=self.time_front,
                    num_frame=self.num_frame_front,
                    name_save=f"{index}.jpg",
                    preds=pred)

            d = {"top": dict(), "front": dict()}
            for label, boxes in zip(self.labels, self.preds_top):
                if len(boxes):
                    d["top"][label] = boxes.cpu().numpy()

            for label, boxes in zip(self.labels, self.preds_front):
                if len(boxes):
                    d["front"][label] = boxes.cpu().numpy()

            self.d = self.exp_filter(d)
            self.frame_id += 1
            # 1. 搭建好实验所需装置
            if -1 == self.exp_ok[0]:
                if self.judge_score1():
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(1, "front")
                    return
            # 2. 弹簧测力计调零
            if -1 == self.exp_ok[1]:
                if self.judge_score2():
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, "front")
                    return
            # 3. 称量记录物块重量
            if -1 == self.exp_ok[2] and -1 != self.exp_ok[1]:
                if self.judge_score3():
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, "front")
                    return
            # 4、5、6、7
            res = self.judge_height()
            if res["status"]:
                if res["mode"] == "smooth":
                    self.update_heights(res["height"])
                elif res["mode"] == "rough":
                    if -1 != self.exp_ok[2]:
                        if -1 == self.exp_ok[3]:
                            self.exp_ok[3] = self.frame_id
                            assign_score_fun2(4, self.images[0][1],
                                             self.images[0][2])
                        if -1 == self.exp_ok[4]:
                            self.exp_ok[4] = self.frame_id
                            assign_score_fun2(5, self.images[1][1],
                                             self.images[1][2])
                        if -1 == self.exp_ok[5]:
                            self.exp_ok[5] = self.frame_id
                            assign_score_fun2(6, self.images[2][1],
                                             self.images[2][2])
                        if -1 == self.exp_ok[6]:
                            self.exp_ok[6] = self.frame_id
                            assign_score_fun(7, "front")
            # 8. 整理器材
            if -1 == self.exp_ok[7] and -1 != self.exp_ok[6]:
                if self.judge_clean():
                    self.exp_ok[7] = self.frame_id
                    assign_score_fun(8, "top")
                    return

    def update_heights(self, height):
        if len(self.images) == 0:
            self.images.append((height, self.image, self.pred))
            #self.images = sorted(self.images, key = lambda x:x[0])
        elif len(self.images) == 1:
            if height > self.images[0][0] + 10:
                self.images.append((height, self.image, self.pred))
        elif len(self.images) == 2:
            if height > self.images[1][0] + 10:
                self.images.append((height, self.image, self.pred))
        elif len(self.images) == 3:
            if height > self.images[2][0] + 10:
                self.images[-1] = (height, self.image, self.pred)

    def judge_score1(self):
        res = self.d
        # 1. 搭建好实验所需装置
        if not ("board_top" in res["top"].keys()):
            return False
        if not ("height" in res["front"].keys()):
            return False
        return True

    def judge_score2(self):
        res = self.d
        # 2. 弹簧测力计调零

        if not ("weight_beam" in res["front"].keys()):
            return False
        if not ("hand" in res["front"].keys()):
            return False
        if ("weight_beam_zero_vertical" in res["front"].keys()):
            return True
        return False

    def judge_score3(self):
        res = self.d
        # 3. 称量记录物块重量
        if not ("weight_beam" in res["front"].keys()):
            return False
        if not ("block" in res["front"].keys()):
            return False

        if not ("pull_weight_beam_vertical" in res["front"].keys()):
            return False
        block = sorted(res["front"]["block"], key=lambda box: -box[4])[0]
        pull_weight_beam_vertical = sorted(
            res["front"]["pull_weight_beam_vertical"],
            key=lambda box: -box[4])[0]
        if iou(block, pull_weight_beam_vertical):
            return True
        return False

    def judge_height(self):
        res = self.d
        r = {"status": False, "height": 0, "mode": "smooth"}
        # 4. 保持斜面勤写程度较缓，测量斜面高度，在该斜面高度下，匀速拉动物块，记录弹簧测力计示数
        # 5. 提高斜面倾斜度至较陡，测量斜面高度，匀速拉动物块并记录弹簧测力计示数
        # 6. 提高斜面倾斜度至陡，测量斜面高度，匀速拉动物块并记录弹簧测力计示数
        # 7. 保持斜面倾斜程度陡，改变斜面粗糙程度，匀速拉动物块并记录弹簧测力计示数
        if not ("height" in res["front"].keys()):
            return r
        if not ("block" in res["top"].keys()):
            return r
        if not ("weight_beam" in res["top"].keys()):
            return r
        if not ("board_top" in res["top"].keys()):
            return r
        if not ("hand" in res["top"].keys()):
            return r
        block = sorted(res["top"]["block"], key=lambda box: -box[4])[0]
        weight_beam = sorted(
            res["top"]["weight_beam"], key=lambda box: -box[4])[0]
        hands = sorted(res["top"]["hand"], key=lambda box: -box[4])
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]
        height = sorted(res["front"]["height"], key=lambda box: -box[4])[0]
        h = height[3] - height[1]
        r["height"] = h
        if iou(block, board_top) == 0:
            return r
        if iou(weight_beam, board_top) == 0:
            return r
        # 粗糙模式
        if ("towel_top" in res["top"].keys()):
            towel_top = sorted(
                res["top"]["towel_top"], key=lambda box: -box[4])[0]
            # 非粗糙模式
            if iou(towel_top, board_top) == 0:
                if "pull_weight_beam_horizontal" in res["top"].keys():
                    r["status"] = True
                return r
            if "pull_weight_beam_horizontal" in res["top"].keys():
                #### 记录height####
                r["mode"] = "rough"
                r["status"] = True
                return r
            return r
        # 非粗糙模式
        else:
            if "pull_weight_beam_horizontal" in res["top"].keys():
                #### 记录height####
                r["status"] = True
                return r
            return r

    def judge_clean(self):
        res = self.d
        # 8. 整理器材
        if "clean_desk_top" in res["top"].keys():
            return True
        # if "clean_desk_front" in res["front"].keys():
        #     return True
        return False