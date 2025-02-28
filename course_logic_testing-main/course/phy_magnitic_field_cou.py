from .comm import *
from .comm.course_base import ConfigModel
from logger import logger


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


class PHY_magnitic_field(ConfigModel):
    def __init__(self):
        super(PHY_magnitic_field, self).__init__()
        self.initScore()

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 5
        self.labels = [
            "hand", "needle", "device", "switch_on", "switch_off", "line",
            "power", "power_pos", "power_neg", "clean_desk", "hand_on_switch"
        ]
        self.circuit_type = 0
        self.circuit_type_changed = False
        self.connect_device_power = False
        self.connect_device_switch = False
        self.connect_power_switch = False

    def exp_filter(self, d):
        if not ("power" in d.keys()):
            return d
        if not ("device" in d.keys()):
            return d
        d_new = dict()
        power = sorted(d["power"], key=lambda x: -x[-1])[0]
        device = sorted(d["device"], key=lambda x: -x[-1])[0]
        for key, vals in d.items():
            vals_new = []
            if key == "power_pos":
                for val in vals:
                    if iou(power, val) > 0:
                        vals_new.append(val)
            elif key == "power_neg":
                for val in vals:
                    if iou(power, val) > 0:
                        vals_new.append(val)
            elif key == "needle":
                for val in vals:
                    if iou(device, val) > 0:
                        vals_new.append(val)
            else:
                vals_new = vals
            if len(vals_new):
                d_new[key] = vals_new
        return d_new

    def run_one_result_process(
            self, frame_top, frame_front, frame_side, pred_top, pred_front,
            pred_side, time_top, time_front, time_side, num_frame_top,
            num_frame_front, num_frame_side, path_save, names_label):
        #logger.info("Processing Magnet")
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

        if pred_top != None and pred_top.shape[0]:
            self.preds_top, self.objects_top = self.assign_labels(
                frame_top, pred_top, names_label)
            top_true = True

        if top_true:

            self.rtmp_push_fun(
                top_img=frame_top,
                front_img=frame_front,
                side_img=frame_side,
                top_preds=self.preds_top,
                front_preds=None,
                side_preds=None)
            self.frame = frame_top
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

            for label, boxes in zip(self.labels, self.preds_top):
                if len(boxes):
                    d[label] = boxes.cpu().numpy()

            # self.d = d
            self.d = self.exp_filter(d)

            self.frame_id += 1
            # 1. 正确使用实验器材连接电路
            ret = self.judge_equipment()
            if -1 == self.exp_ok[0]:
                if ret:
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(1, "top")
                    return
            # 2. 在通电螺线管两端放置小磁针
            if -1 == self.exp_ok[1] and -1 != self.exp_ok[0]:
                if self.judge_needles():
                    self.exp_ok[1] = self.frame_id
                    conf_c = 0.1
                    assign_score_fun(2, "top")
                    return
            # 3. 闭合开关，观察小磁针，并说出小磁针N极的指向
            if -1 == self.exp_ok[2] and -1 != self.exp_ok[1]:
                if self.judge_circuit():
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, "top")
                    return
            # 4. 改变电流方向，再次说出小磁针N极的指向
            if (-1 == self.exp_ok[3]) and -1 != self.exp_ok[2]:
                if self.judge_exp_time():
                    self.exp_ok[3] = self.frame_id
                    assign_score_fun(4, "top")
                    return
            # 5. 实验结束后能及时整理仪器
            if (-1 == self.exp_ok[4]) and -1 != self.exp_ok[1]:
                if self.judge_clean():
                    self.exp_ok[4] = self.frame_id
                    assign_score_fun(5, "top")
                    return

    def judge_equipment(self):
        res = self.d
        if not ("needle" in res.keys()):
            return False
        if not ("device" in res.keys()):
            return False
        if not ("power" in res.keys()):
            return False
        if not ("line" in res.keys()):
            return False
        if not (len(res["line"]) >= 3):
            return False
        if not ("switch_on" in res.keys()) and not (
                "switch_off" in res.keys()):
            return False

        device = sorted(res["device"], key=lambda box: -box[4])[0]
        power = sorted(res["power"], key=lambda box: -box[4])[0]
        lines = res["line"]
        if "switch_on" in res.keys():
            switch = sorted(res["switch_on"], key=lambda box: -box[4])[0]
        elif "switch_off" in res.keys():
            switch = sorted(res["switch_off"], key=lambda box: -box[4])[0]
        else:
            return False

        # 判断电路连接情况
        line_device_switch = None
        line_device_power = None
        line_power_switch = None
        # 判断电源和设备是否连接
        best_biou = 0
        for idx, line in enumerate(lines):
            biou_device = iou(line, device) + iou(line, device)
            biou_power = iou(line, power) + iou(line, power)
            biou = biou_device + biou_power
            if biou_device and biou_power:
                if biou > best_biou:
                    line_device_power = line
                    best_biou = biou

        # 判断电源和开关是否连接
        best_biou = 0
        for idx, line in enumerate(lines):
            biou_switch = iou(line, switch) + iou(line, switch)
            biou_power = iou(line, power) + iou(line, power)
            biou = biou_switch + biou_power
            if biou_switch and biou_power:
                if biou > best_biou:
                    line_power_switch = line
                    best_biou = biou

        # 判断设备和开关是否连接
        best_biou = 0
        for idx, line in enumerate(lines):
            biou_device = iou(line, device) + iou(line, device)
            biou_switch = iou(line, switch) + iou(line, switch)
            biou = biou_device + biou_switch
            if biou_device and biou_switch:
                if biou > best_biou:
                    line_device_switch = line
                    best_biou = biou

        circuit_type = 0

        power_point = (power[0], 0.5 * (power[1] + power[3]))
        if ("power_pos" in res.keys()) and ("power_neg" in res.keys()):
            power_poss = sorted(
                res["power_pos"],
                key=lambda box: (power_point[0] - 0.5 * (box[0] + box[2]))**2 +
                (power_point[1] - 0.5 * (box[1] + box[3]))**2)
            power_poss = [(power_pos, "pos") for power_pos in power_poss]
            power_negs = sorted(
                res["power_neg"],
                key=lambda box: (power_point[0] - 0.5 * (box[0] + box[2]))**2 +
                (power_point[1] - 0.5 * (box[1] + box[3]))**2)
            power_negs = [(power_neg, "neg") for power_neg in power_negs]

            power_pts = power_poss + power_negs

            power_pts = sorted(
                power_pts,
                key=lambda power_: (power_point[0] - 0.5 * (power_[0][
                    0] + power_[0][2]))**2 + (power_point[1] - 0.5 * (power_[
                        0][1] + power_[0][3]))**2)
            if power_pts[0][1] != power_pts[-1][1]:
                if line_device_power is not None and iou(
                        power_pts[0][0], line_device_power):
                    # 正极和电源相连 = 1
                    if power_pts[0][1] == "pos":
                        circuit_type = 1
                    # 负极和电源相连 = 2
                    else:
                        circuit_type = 2
                elif line_power_switch is not None and iou(
                        power_pts[0][0], line_power_switch):
                    # 正极和开关相连 = 负极和电源相连 = 2
                    if power_pts[0][1] == "pos":
                        circuit_type = 2
                    # 负极和开关相连 = 正极和电源相连 = 1
                    else:
                        circuit_type = 1
                elif line_device_power is not None and iou(
                        power_pts[-1][0], line_device_power):
                    # 正极和电源相连 = 1
                    if power_pts[-1][1] == "pos":
                        circuit_type = 1
                    # 负极和电源相连 = 2
                    else:
                        circuit_type = 2
                elif line_power_switch is not None and iou(
                        power_pts[-1][0], line_power_switch):
                    # 正极和开关相连 = 负极和电源相连 = 2
                    if power_pts[-1][1] == "pos":
                        circuit_type = 2
                    # 负极和开关相连 = 正极和电源相连 = 1
                    else:
                        circuit_type = 1
        if circuit_type:
            if self.circuit_type:
                if self.circuit_type != circuit_type:
                    self.circuit_type_changed = True
            self.circuit_type = circuit_type
            # print(self.circuit_type)
        # 如果手挡住了，就用之前的来看
        if "hand_on_switch" in res.keys():
            if self.connect_device_power and self.connect_device_switch and self.connect_power_switch:
                return True
        # 手没挡住，并且只有部分可见(组装过程中)

        self.connect_device_switch = self.connect_device_switch or not (
            line_device_switch is None)
        self.connect_device_power = self.connect_device_power or not (
            line_device_power is None)
        self.connect_power_switch = self.connect_power_switch or not (
            line_power_switch is None)

        # 手没挡住，就要看全部
        if (line_device_switch is None) or (line_device_power is None) or (
                line_power_switch is None):
            return False
        if iou(line_device_switch, line_device_power) > 0.9:
            return False
        if iou(line_device_switch, line_power_switch) > 0.9:
            return False
        if iou(line_device_power, line_power_switch) > 0.9:
            return False
        return True

    def judge_needles(self):
        res = self.d
        if not ("needle" in res.keys()):
            return False
        return True

    def judge_circuit(self):
        res = self.d
        if not ("needle" in res.keys()):
            return False
        if not ("device" in res.keys()):
            return False
        if not ("power" in res.keys()):
            return False
        if not ("line" in res.keys()):
            return False
        if not ("switch_on" in res.keys()) and not (
                "hand_on_switch" in res.keys()):
            return False

        device = sorted(res["device"], key=lambda box: -box[4])[0]
        power = sorted(res["power"], key=lambda box: -box[4])[0]
        lines = res["line"]
        if "switch_on" in res.keys():
            switch = sorted(res["switch_on"], key=lambda box: -box[4])[0]
        else:
            switch = sorted(res["hand_on_switch"], key=lambda box: -box[4])[0]
        # 判断电路连接情况
        line_device_switch = None
        line_device_power = None
        line_power_switch = None
        # 判断电源和设备是否连接
        best_biou = 0
        for idx, line in enumerate(lines):
            biou_device = iou(line, device) + iou(line, device)
            biou_power = iou(line, power) + iou(line, power)
            biou = biou_device + biou_power
            if biou_device and biou_power:
                if biou > best_biou:
                    line_device_power = line
                    best_biou = biou

        # 判断电源和开关是否连接
        best_biou = 0
        for idx, line in enumerate(lines):
            biou_switch = iou(line, switch) + iou(line, switch)
            biou_power = iou(line, power) + iou(line, power)
            biou = biou_switch + biou_power
            if biou_switch and biou_power:
                if biou > best_biou:
                    line_power_switch = line
                    best_biou = biou

        # 判断设备和开关是否连接
        best_biou = 0
        for idx, line in enumerate(lines):
            biou_device = iou(line, device) + iou(line, device)
            biou_switch = iou(line, switch) + iou(line, switch)
            biou = biou_device + biou_switch
            if biou_device and biou_switch:
                if biou > best_biou:
                    line_device_switch = line
                    best_biou = biou

        # 如果手挡住了，就用之前的来看
        if "hand_on_switch" in res.keys():
            if self.connect_device_power and self.connect_device_switch and self.connect_power_switch:
                return True
        # 手没挡住，并且只有部分可见(组装过程中)

        self.connect_device_switch = self.connect_device_switch or not (
            line_device_switch is None)
        self.connect_device_power = self.connect_device_power or not (
            line_device_power is None)
        self.connect_power_switch = self.connect_power_switch or not (
            line_power_switch is None)

        # 手没挡住，就要看全部
        if (line_device_switch is None) or (line_device_power is None) or (
                line_power_switch is None):
            return False
        if iou(line_device_switch, line_device_power) > 0.9:
            return False
        if iou(line_device_switch, line_power_switch) > 0.9:
            return False
        if iou(line_device_power, line_power_switch) > 0.9:
            return False
        return True

    def judge_exp_time(self):
        # print(self.circuit_type)
        return self.circuit_type_changed

    def judge_clean(self):
        res = self.d

        if "clean_desk" in res.keys():
            return True

        if not ("hand" in res.keys()):
            return False
        hands = sorted(res["hand"], key=lambda box: -box[4])
        for hand in hands:
            hand_y = hand[1]
            if hand_y < 30:
                return True
        return False
