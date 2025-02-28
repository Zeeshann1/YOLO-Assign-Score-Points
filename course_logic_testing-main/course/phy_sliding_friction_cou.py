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


class PHY_sliding_friction(ConfigModel):
    def __init__(self):
        super(PHY_sliding_friction, self).__init__()

        self.initScore()

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 5
        self.labels = [
            "hand", "board_front", "weight_beam", "block",
            "weight_beam_zero_vertical", "clean_desk_front",
            "weight_beam_zero_horizontal", "height",
            "pull_weight_beam_vertical", "board_top", "weight_top",
            "towel_top", "clean_desk_top", "pull_weight_beam_horizontal"
        ]

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

            d = {"top": dict(), "front": dict()}
            for label, boxes in zip(self.labels, self.preds_top):
                if len(boxes):
                    d["top"][label] = boxes.cpu().numpy()

            for label, boxes in zip(self.labels, self.preds_front):
                if len(boxes):
                    d["front"][label] = boxes.cpu().numpy()

            self.d = self.exp_filter(d)
            self.frame_id += 1
            # 1. 将弹簧测力计指针水平调“0”
            if -1 == self.exp_ok[0]:
                if self.judge_zero():
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(1, "top")
            # 2. 在桌面上放一较粗糙的木板，用弹簧测力计拉木块在粗糙木板上匀速滑动
            if -1 == self.exp_ok[1] and -1 != self.exp_ok[0]:
                if self.judge_exp1():
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, "top")
            # 3. 在木块上加放一个重物，用弹簧测力计水平拉木块在粗糙木板上匀速滑动
            if -1 == self.exp_ok[2] and -1 != self.exp_ok[1]:
                if self.judge_exp2():
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, "top")
            # 4. 取走木板，保持在木块上放的重物不变，用弹簧测力计水平拉木块在桌面上匀速滑动
            if (-1 == self.exp_ok[3]) and -1 != self.exp_ok[2]:
                if self.judge_exp3():
                    self.exp_ok[3] = self.frame_id
                    assign_score_fun(4, "top")
            # 5. 整理器材
            if (-1 == self.exp_ok[4]) and -1 != self.exp_ok[1]:
                if self.judge_clean():
                    self.exp_ok[4] = self.frame_id
                    assign_score_fun(5, "top")

    def judge_zero(self):
        res = self.d
        if "weight_beam_zero_horizontal" in res["top"].keys():
            return True
        return False

    def judge_exp1(self):
        res = self.d
        # 在桌面上放一较粗糙的木板，用弹簧测力计拉木块在粗糙木板上匀速滑动
        if not "board_top" in res["top"].keys():
            return False
        if not "weight_beam" in res["top"].keys():
            return False
        if not "block" in res["top"].keys():
            return False
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]
        weight_beam = sorted(
            res["top"]["weight_beam"], key=lambda box: -box[4])[0]
        block = sorted(res["top"]["block"], key=lambda box: -box[4])[0]
        if iou(board_top, weight_beam) == 0:
            return False
        if iou(board_top, block) == 0:
            return False
        if "pull_weight_beam_horizontal" in res["top"].keys():
            return True
        # else:
        #     hands = res["top"]["hand"]
        #     num_iou_with_weight_beam = 0
        #     for hand in hands:
        #         if iou(hand, weight_beam):
        #             num_iou_with_weight_beam += 1
        #     if num_iou_with_weight_beam == 1:
        #         return True
        return False

    def judge_exp2(self):
        res = self.d
        # 在木块上加放一个重物，用弹簧测力计水平拉木块在粗糙木板上匀速滑动
        if not "board_top" in res["top"].keys():
            return False
        if not "weight_beam" in res["top"].keys():
            return False
        if not "block" in res["top"].keys():
            return False
        if not "weight_top" in res["top"].keys():
            return False
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]
        weight_beam = sorted(
            res["top"]["weight_beam"], key=lambda box: -box[4])[0]
        block = sorted(res["top"]["block"], key=lambda box: -box[4])[0]
        weight_top = sorted(
            res["top"]["weight_top"], key=lambda box: -box[4])[0]
        if iou(board_top, weight_beam) == 0:
            return False
        if iou(board_top, block) == 0:
            return False
        if iou(weight_top, block) == 0:
            return False
        if "pull_weight_beam_horizontal" in res["top"].keys():
            return True
        # else:
        #     hands = res["top"]["hand"]
        #     num_iou_with_weight_beam = 0
        #     for hand in hands:
        #         if iou(hand, weight_beam):
        #             num_iou_with_weight_beam += 1
        #     if num_iou_with_weight_beam == 1:
        #         return True
        return False

    def judge_exp3(self):
        res = self.d
        # 取走木板，保持在木块上放的重物不变，用弹簧测力计水平拉木块在桌面上匀速滑动
        if not "weight_beam" in res["top"].keys():
            return False
        if not "block" in res["top"].keys():
            return False
        if not "weight_top" in res["top"].keys():
            return False
        if not ("board_top" in res["top"].keys()):
            return False
        weight_beam = sorted(
            res["top"]["weight_beam"], key=lambda box: -box[4])[0]
        block = sorted(res["top"]["block"], key=lambda box: -box[4])[0]
        weight_top = sorted(
            res["top"]["weight_top"], key=lambda box: -box[4])[0]

        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]
        if iou(board_top, weight_beam):
            return False
        if iou(board_top, block):
            return False
        if iou(weight_top, block) == 0:
            return False
        if "pull_weight_beam_horizontal" in res["top"].keys():
            return True
        # else:
        #     hands = res["top"]["hand"]
        #     num_iou_with_weight_beam = 0
        #     for hand in hands:
        #         if iou(hand, weight_beam):
        #             num_iou_with_weight_beam += 1
        #     if num_iou_with_weight_beam == 1:
        #         return True
        return False

    def judge_clean(self):
        res = self.d
        if "clean_desk_top" in res["top"].keys():
            return True
        # if "clean_desk_front" in res["front"].keys():
        #     return True
        return False
