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


class PHY_spring_dynamometer(ConfigModel):
    def __init__(self):
        super(PHY_spring_dynamometer, self).__init__()

        self.frame_id = 0
        self.best_weight_beam_zero_horizontal_score = 0
        self.best_weight_beam_zero_vertical_score = 0
        self.uncertain_pulls = []
        self.last_exp_hold = []
        self.last_pos = []
        self.exp_ok = [-1] * 10

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
        front_true = False
        self.frame = frame_top
        front_true = False
        if pred_front != None and pred_front.shape[0]:
            self.preds_front, self.objects_front = self.assign_labels(
                frame_front, pred_front, names_label)
            front_true = True
        if front_true:
            d = dict()

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

            for label, boxes in zip(self.labels, self.preds_front):
                if len(boxes):
                    d[label] = boxes.cpu().numpy()
            self.d = d
            self.frame_id += 1

            # 1. 是否是调整木板
            if self.exp_ok[0] == -1 or (self.exp_ok[0] != -1 and
                                        self.frame_id - self.exp_ok[0] < 3):
                if self.judge_paperboard():
                    self.exp_ok[0] = self.frame_id
                    self.update_last_exp(1)
                    assign_score_fun(1, "front")
                    return

            # 2. 是否水平调零
            if self.exp_ok[1] == -1:
                if self.judge_weight_zero(state="horizontal"):
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, "front")
                    return
            else:
                if self.frame_id - self.exp_ok[1] < 1:
                    if self.judge_weight_zero(state="horizontal"):
                        self.exp_ok[1] = self.frame_id
                        assign_score_fun(2, "front")
                        return
            # 3. 是否第一次双向拉木板
            if self.exp_ok[2] == -1:
                if self.judge_pull_horizontal():
                    self.exp_ok[2] = self.frame_id
                    self.update_last_exp(1)
                    assign_score_fun(3, "front")
                    return
            # 4. 判断是否第二次双向拉木板
            else:
                if self.frame_id - self.exp_ok[2] > 3:
                    if self.judge_pull_horizontal():
                        self.exp_ok[3] = self.frame_id
                        self.update_last_exp(1)
                        assign_score_fun(4, "front")
                        return
            # 6. 竖直调零
            if self.exp_ok[5] == -1:
                if self.judge_weight_zero(state="vertical"):
                    self.exp_ok[5] = self.frame_id
                    assign_score_fun(6, "front")
                    return
            else:
                if self.frame_id - self.exp_ok[5] < 1:
                    if self.judge_weight_zero(state="vertical"):
                        self.exp_ok[5] = self.frame_id
                        assign_score_fun(6, "front")
                        return

            # 7. 判断是否竖直静止拉伸
            ret, pos = self.judge_pull_vertical("still")
            if ret:
                self.exp_ok[6] = self.frame_id
                self.update_last_exp(2)
                self.update_uncertain_pull(
                    self.frame_front, self.preds_front, pos,
                    self.objects_front, self.time_front, self.num_frame_front)
                return
            # 8. 判断是否竖直向上拉伸
            ret, pos = self.judge_pull_vertical("up")
            if ret:
                self.exp_ok[7] = self.frame_id
                self.update_last_exp(2)
                self.update_uncertain_pull(
                    self.frame_front, self.preds_front, pos,
                    self.objects_front, self.time_front, self.num_frame_front)
                return
            # 9. 判断是否竖直向下拉伸
            ret, pos = self.judge_pull_vertical("down")
            if ret:
                self.exp_ok[8] = self.frame_id
                self.update_last_exp(2)
                self.update_uncertain_pull(
                    self.frame_front, self.preds_front, pos,
                    self.objects_front, self.time_front, self.num_frame_front)
                return

            if self.judge_clean_desk():
                if len(self.last_exp_hold) == 3:
                    count_exp1 = self.last_exp_hold.count(1)
                    count_exp2 = self.last_exp_hold.count(2)
                    # 5. 判断是否清理桌面
                    if count_exp1 > count_exp2:
                        if self.exp_ok[4] == -1:
                            self.exp_ok[4] = self.frame_id
                            assign_score_fun(5, "front")
                        return
                    # 10. 判断是否清理桌面
                    else:
                        self.exp_ok[9] = self.frame_id
                        assign_score_fun(10, "front")
                        return

    def update_uncertain_pull(self, frame, top_preds, pos, objects_top,
                              time_top, num_frame_top):
        if len(self.uncertain_pulls) != 3:
            self.uncertain_pulls.append((copy.deepcopy(frame), top_preds, pos))
            self.uncertain_pulls = sorted(
                self.uncertain_pulls, key=lambda x: x[-1])  # 从小到大
        else:
            if pos < self.uncertain_pulls[0][-1]:
                self.uncertain_pulls[0] = (copy.deepcopy(frame), top_preds,
                                           pos)
            elif pos > self.uncertain_pulls[2][-1]:
                self.uncertain_pulls[2] = (copy.deepcopy(frame), top_preds,
                                           pos)
            else:
                dis_old = abs(
                    abs(self.uncertain_pulls[1][-1] -
                        self.uncertain_pulls[0][-1]) -
                    abs(self.uncertain_pulls[1][-1] -
                        self.uncertain_pulls[2][-1]))
                dis_new = abs(
                    abs(self.uncertain_pulls[0][-1] - pos) -
                    abs(pos - self.uncertain_pulls[2][-1]))
                if dis_new < dis_old:
                    self.uncertain_pulls[1] = (copy.deepcopy(frame), top_preds,
                                               pos)
            # self.assignScore(7, self.uncertain_pulls[1][0], self.uncertain_pulls[1][1])
            conf_c = 0.1
            self.assignScore(
                index=7,
                img=self.uncertain_pulls[1][0],
                object=objects_top,
                conf=conf_c,
                time_frame=time_top,
                num_frame=num_frame_top,
                name_save="7.jpg",
                preds=self.uncertain_pulls[1][1])
            # self.assignScore(8, self.uncertain_pulls[0][0], self.uncertain_pulls[0][1])
            conf_c = 0.1
            self.assignScore(
                index=8,
                img=self.uncertain_pulls[0][0],
                object=objects_top,
                conf=conf_c,
                time_frame=time_top,
                num_frame=num_frame_top,
                name_save="8.jpg",
                preds=self.uncertain_pulls[0][1])
            # self.assignScore(9, self.uncertain_pulls[2][0], self.uncertain_pulls[2][1])
            conf_c = 0.1
            self.assignScore(
                index=9,
                img=self.uncertain_pulls[2][0],
                object=objects_top,
                conf=conf_c,
                time_frame=time_top,
                num_frame=num_frame_top,
                name_save="9.jpg",
                preds=self.uncertain_pulls[2][1])

    def update_last_exp(self, exp_num):
        self.last_exp_hold.append(exp_num)
        if len(self.last_exp_hold) > 3:
            self.last_exp_hold = self.last_exp_hold[1:]

    def reset(self):
        self.frame_id = 0
        self.res = []
        self.last_exp_hold = []
        self.last_pos = []

    def judge_weight_zero(self, state="vertical"):
        res = self.d

        if state == "vertical":
            if "pull_weight_beam_vertical" in res.keys():
                return False
            if not ("weight_beam_zero_vertical" in res.keys()):
                return False
            if not ("weight_beam") in res.keys():
                return False

            if len(res["weight_beam_zero_vertical"]) < 1:
                return False
            if len(res["weight_beam"]) < 1:
                return False
            return True
            weight_beams = sorted(
                res["weight_beam"], key=lambda box: -(box[3] - box[1]))
            if "hook_weight" in res.keys() and len(res["weight_beam"]):
                hook_weight = sorted(
                    res["hook_weight"],
                    key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[0]

                if len(weight_beams) > 1:
                    weight_beams[:2]
                else:
                    weight_beams = [weight_beams[0], weight_beams[0]]
                if iou(hook_weight, weight_beams[0]) > 0 or iou(
                        hook_weight, weight_beams[1]) > 0:
                    return False
            if "hand" in res.keys():
                if len(res["hand"]) > 1:
                    hands = sorted(
                        res["hand"],
                        key=lambda box: -(box[2] - box[0]) * (box[3] - box[1])
                    )[:2]
                else:
                    hands = [res["hand"][0], res["hand"][0]]
                y_weight_beam = 0.5 * (weight_beams[0][3] + weight_beams[0][1])
                y_hand1 = 0.5 * (hands[0][3] + hands[0][1])
                y_hand2 = 0.5 * (hands[1][3] + hands[1][1])
                if y_hand1 > y_weight_beam and y_hand2 > y_weight_beam:
                    return False
            weight_beam_zero_vertical = \
            sorted(res["weight_beam_zero_vertical"], key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[0]
            if weight_beam_zero_vertical[
                    -2] > self.best_weight_beam_zero_vertical_score:
                self.best_weight_beam_zero_vertical_score = weight_beam_zero_vertical[
                    -2]
            else:
                return False
        else:
            if "pull_weight_beam_horizontal" in res.keys():
                return False
            if not ("weight_beam_zero_horizontal" in res.keys()):
                return False
            if not ("hand" in res.keys()):
                return False
            if len(res["hand"]) < 2:
                return False
            hands = sorted(
                res["hand"],
                key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[:2]
            weight_beam_zero_horizontal = \
            sorted(res["weight_beam_zero_horizontal"], key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[0]
            x = 0.5 * (weight_beam_zero_horizontal[0] +
                       weight_beam_zero_horizontal[2])
            if not (1920 * 0.1 < x < 1920 * 0.9):
                return False

            if not (iou(hands[0], weight_beam_zero_horizontal)
                    and iou(hands[1], weight_beam_zero_horizontal)):
                return False
            if weight_beam_zero_horizontal[
                    -2] > self.best_weight_beam_zero_horizontal_score:
                self.best_weight_beam_zero_horizontal_score = weight_beam_zero_horizontal[
                    -2]
            else:
                return False
        return True

    def judge_paperboard(self, ):
        res = self.d
        if not ("paperboard" in res.keys()):
            return False
        if not ("hand" in res.keys()):
            return False
        if len(res["paperboard"]) < 1:
            return False
        if len(res["hand"]) < 2:
            return False
        paperboard = sorted(
            res["paperboard"],
            key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[0]
        hands = sorted(
            res["hand"],
            key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[:2]
        if iou(paperboard, hands[0]) > 0 and iou(
                paperboard, hands[1]) > 0 and iou(hands[0], hands[1]) > 0:
            return True
        return False

    def judge_pull_horizontal(self, ):
        res = self.d
        if not ("paperboard" in res.keys()):
            return False
        if not ("hand" in res.keys()):
            return False
        if not ("weight_beam" in res.keys()):
            return False
        if not ("pull_weight_beam_horizontal" in res.keys()):
            return False
        if len(res["paperboard"]) < 1:
            return False
        if len(res["hand"]) < 2:
            return False
        if len(res["weight_beam"]) < 2:
            return False
        if len(res["head"]) < 1:
            return False
        hands = sorted(
            res["hand"],
            key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[:2]
        weight_beams = sorted(
            res["weight_beam"], key=lambda box: -(box[2] - box[0]))[:2]
        hand_left, hand_right = hands[0], hands[1]
        if hands[0][0] > hands[1][0]:
            hand_left, hand_right = hands[1], hands[0]
        weight_beam_left, weight_beam_right = weight_beams[0], weight_beams[1]
        if weight_beams[0][0] > weight_beams[1][0]:
            weight_beam_left, weight_beam_right = weight_beams[
                1], weight_beams[0]
        if iou(hand_left, weight_beam_left) > 0 and iou(
                hand_right, weight_beam_right) > 0:
            if hand_left[0] < weight_beam_left[0] and hand_right[
                    2] > weight_beam_right[2]:
                return True
        return False

    def judge_clean_desk(self):
        res = self.d
        if not ("clean_desk" in res.keys()):
            return False
        if not ("head" in res.keys()):
            return False
        if len(res["head"]) < 1:
            return False
        if len(res["clean_desk"]) < 1:
            return False
        clean_desk = res["clean_desk"][0]
        if "weight_beam" in res.keys():
            weight_beams = sorted(
                res["weight_beam"], key=lambda box: -(box[3] - box[1]))
            if len(weight_beams) == 1:
                weight_beam = weight_beams[0]
                height = weight_beam[3] - weight_beam[1]
                width = weight_beam[2] - weight_beam[0]
                if width < height:
                    return False
            elif len(weight_beams) > 1:
                y_clean_desk = clean_desk[1]
                if y_clean_desk - weight_beams[0][3] < 50:
                    return False
                elif y_clean_desk - weight_beams[1][3] < 50:
                    return False

        if "hook_weight" in res.keys():
            hook_weight = sorted(
                res["hook_weight"],
                key=lambda box: -(box[2] - box[0]) * (box[3] - box[1]))[0]
            y_hook_weight = hook_weight[3]
            y_clean_desk = clean_desk[1]
            if y_clean_desk - y_hook_weight < 50:
                return False
        # if clean_desk[-1] < 0.6:
        #    return False
        for key, val in res.items():
            if key == "clean_desk" or key == "head" or key == "hand":
                continue
            for box in val:
                if iou(clean_desk, box) > 0:
                    return False
        return True

    def judge_pull_vertical(self, state="still"):
        res = self.d
        if not ("weight_beam" in res.keys()):
            return False, -1
        if not ("hook_weight" in res.keys()):
            return False, -1
        if not ("pull_weight_beam_vertical" in res.keys()):
            return False, -1
        if not ("hand" in res.keys()):
            return False, -1
        if len(res["weight_beam"]) < 1:
            return False, -1
        if len(res["hook_weight"]) < 1:
            return False, -1

        weight_beam = sorted(
            res["weight_beam"], key=lambda box: -(box[3] - box[1]))[0]
        hook_weight = sorted(
            res["hook_weight"], key=lambda box: -(box[3] - box[1]))[0]
        hands = sorted(
            res["hand"],
            key=lambda box: -(box[3] - box[1]) * (box[2] - box[0]))
        if len(hands) > 1:
            hands = hands[:2]
            if iou(weight_beam, hands[0]) > 0 and iou(weight_beam,
                                                      hands[1]) > 0:
                return False, -1
        else:
            hands = [hands[0], hands[0]]
        if iou(hook_weight, hands[0]) > 0 or iou(hook_weight, hands[1]) > 0:
            return False, -1

        width = weight_beam[2] - weight_beam[0]
        height = weight_beam[3] - weight_beam[1]
        if width > height:
            return False, -1
        if True:
            p_y = 0.5 * (weight_beam[1] + weight_beam[3])
            self.last_pos.append(p_y)
            if state == "still":
                if len(self.last_pos) > 5:
                    self.last_pos = self.last_pos[1:]
                    for i in range(len(self.last_pos) - 1):
                        if abs(self.last_pos[i + 1] - self.last_pos[i]) > 10:
                            return False, -1
            else:
                if len(self.last_pos) > 5:
                    self.last_pos = self.last_pos[1:]
                    if state == "up":
                        for i in range(len(self.last_pos) - 1):
                            if self.last_pos[i + 1] > self.last_pos[i]:
                                return False, -1
                    elif state == "down":
                        for i in range(len(self.last_pos) - 1):
                            if self.last_pos[i + 1] < self.last_pos[i]:
                                return False, -1
                    return True, p_y
        return False, -1
