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


class PHY_mean_velocity(ConfigModel):
    def __init__(self):
        super(PHY_mean_velocity, self).__init__()
        self.initScore()

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 6
        self.labels = [
            "baffle_top", "board_top", "timer_top", "prepare_top", "car_top",
            "inclined_plank_front", "prepare_front", "baffle_front",
            "clean_desk_top"
        ]
        self.ori_pos = None
        self.ori_pos2 = None

    def exp_filter(self, d):
        d_new = {"top": dict(), "front": dict()}
        d_top = d["top"]
        d_front = d["front"]
        for key, vals in d_top.items():
            if "top" in key:
                d_new["top"][key] = vals

        for key, vals in d_front.items():
            if "front" in key:
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
            # 1. 将木板的一端用木块垫起形成斜面，将金属片固定在斜面底端
            if -1 == self.exp_ok[0]:
                if self.judge_score1():
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(1, "front")
                    return
            # 2. 测量小车即将运动的路程并计入表格中
            if -1 == self.exp_ok[1]:
                if -1 != self.exp_ok[
                        0] and self.frame_id - self.exp_ok[0] > 100:
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, "front")
                    return
            # 3. 将小车从斜面顶端滑下，并开始计时，小车到达斜面底端时停止计时，记录小车的运动时间
            if -1 == self.exp_ok[2]:
                if self.judge_score3():
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, "top")
                    return
            # 4、将金属片移至斜面中部某处，测出小车的金属片的距离
            if -1 == self.exp_ok[3]:
                if self.judge_score4():
                    self.exp_ok[3] = self.frame_id
                    assign_score_fun(4, "top")
                    return
            # 5. 测出小车从斜面顶端滑过斜面上半段路程所用的时间
            if -1 == self.exp_ok[4] and -1 != self.exp_ok[3]:
                if self.judge_score5():
                    self.exp_ok[4] = self.frame_id
                    assign_score_fun(5, "top")
                    return
            # 6. 将器材放回原位
            if -1 == self.exp_ok[5] and -1 != self.exp_ok[4]:
                if self.judge_clean():
                    self.exp_ok[5] = self.frame_id
                    assign_score_fun(6, "top")
                    return

    def judge_score1(self):
        res = self.d
        # 1. 将木板的一端用木块垫起形成斜面，将金属片固定在斜面底端
        if not ("board_top" in res["top"].keys()):
            return False
        if not ("inclined_plank_front" in res["front"].keys()):
            return False
        if not ("car_top" in res["top"].keys()):
            return False
        if not ("prepare_top" in res["top"].keys()) and not (
                "prepare_front" in res["front"].keys()):
            return False
        inclined_plank_front = sorted(
            res["front"]["inclined_plank_front"], key=lambda box: -box[4])[0]
        car_top = sorted(res["top"]["car_top"], key=lambda box: -box[4])[0]
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]
        if iou(car_top, board_top) == 0:
            return False
        w = inclined_plank_front[2] - inclined_plank_front[0]
        h = inclined_plank_front[3] - inclined_plank_front[1]
        theta = math.atan(h / w) / np.pi * 180
        #print("theta", theta)
        if theta > 20:
            return False
        return True

    def judge_score3(self):
        res = self.d
        # 3. 将小车从斜面顶端滑下，并开始计时，小车到达斜面底端时停止计时，记录小车的运动时间
        if not ("board_top" in res["top"].keys()):
            return False
        if not ("inclined_plank_front" in res["front"].keys()):
            return False
        if not ("car_top" in res["top"].keys()):
            return False

        inclined_plank_front = sorted(
            res["front"]["inclined_plank_front"], key=lambda box: -box[4])[0]
        car_top = sorted(res["top"]["car_top"], key=lambda box: -box[4])[0]
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]
        if ("baffle_front" in res["front"].keys()):
            baffle_front = sorted(
                res["front"]["baffle_front"], key=lambda box: -box[4])[0]
            if iou(inclined_plank_front, baffle_front):
                return False
        if ("baffle_top" in res["top"].keys()):
            baffle_top = sorted(
                res["top"]["baffle_top"], key=lambda box: -box[4])[0]
            if iou(baffle_top, board_top):
                return False
        if iou(car_top, board_top) < 0.05:
            return False
        # 都不在，说明已经跑出去了
        if not ("prepare_top" in res["top"].keys()) and not (
                "prepare_front" in res["front"].keys()):
            if self.ori_pos is None:
                return False
            if iou(car_top, self.ori_pos) == 0:
                return True
        # 还没跑出去
        else:
            if self.ori_pos is None:
                self.ori_pos = car_top
        return False

    def judge_score4(self):
        res = self.d
        # 4. 将金属片移至斜面中部某处，测出小车的金属片的距离
        if not ("board_top" in res["top"].keys()):
            return False
        if not ("inclined_plank_front" in res["front"].keys()):
            return False
        if not ("car_top" in res["top"].keys()):
            return False
        if not ("prepare_top" in res["top"].keys()) and not (
                "prepare_front" in res["front"].keys()):
            return False
        if not ("baffle_top" in res["top"].keys()) and not (
                "baffle_front" in res["front"].keys()):
            return False

        inclined_plank_front = sorted(
            res["front"]["inclined_plank_front"], key=lambda box: -box[4])[0]
        car_top = sorted(res["top"]["car_top"], key=lambda box: -box[4])[0]
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]

        if iou(car_top, board_top) == 0:
            return False

        return True

    def judge_score5(self):
        res = self.d
        # 5. 测出小车从斜面顶端滑过斜面上半段路程所用的时间
        if not ("board_top" in res["top"].keys()):
            return False
        if not ("inclined_plank_front" in res["front"].keys()):
            return False
        if not ("car_top" in res["top"].keys()):
            return False
        if not ("baffle_top" in res["top"].keys()) and not (
                "baffle_front" in res["front"].keys()):
            return False
        inclined_plank_front = sorted(
            res["front"]["inclined_plank_front"], key=lambda box: -box[4])[0]
        car_top = sorted(res["top"]["car_top"], key=lambda box: -box[4])[0]
        board_top = sorted(res["top"]["board_top"], key=lambda box: -box[4])[0]

        if iou(car_top, board_top) == 0:
            return False
        # 都不在，说明已经跑出去了
        if not ("prepare_top" in res["top"].keys()) and not (
                "prepare_front" in res["front"].keys()):
            if self.ori_pos2 is None:
                return False
            if iou(car_top, self.ori_pos2) == 0:
                return True
        # 还没跑出去
        else:
            if self.ori_pos2 is None:
                self.ori_pos2 = car_top
        return False

    def judge_clean(self):
        res = self.d
        # 8. 整理器材
        if "clean_desk_top" in res["top"].keys():
            return True
        # if "clean_desk_front" in res["front"].keys():
        #     return True
        return False
