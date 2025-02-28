from PIL import Image
from logger import logger
from .comm import *
from .comm.course_base import ConfigModel
import copy
from utilsg.litF import upload_redis_or_save_json_local
from configg.global_config import SCORE_ROOT_PATH
DEBUG_ = False


def all_in(box1, box2):
    return box2[0] <= box1[0] <= box2[2] and box2[1] <= box1[3] <= box2[3]


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


class PHY_induced_current_ration(ConfigModel):
    def __init__(self):
        super(PHY_induced_current_ration, self).__init__()
        self.initScore()

    def post_retrace(self, index, *args, **kwargs):
        self.exp_ok[index - 1] = -1

    def retracementScore(self, index, *args, **kwargs):  # 回撤分数
        if index in self.score_list:
            self.score_list.remove(index)
        if str(index) not in self.exper_score_ids:
            exec(f'self.scorePoint{index} = False')  # 将该得分点设置为True 不在判断该得分点
            return
        i_index = self.exper_score_ids.index(str(index))
        self.jsonResultScore["score_pts_info"][i_index]["score_status"] = False
        self.jsonResultScore["score_pts_info"][i_index]["images_url"] = ""
        self.jsonResultScore["score_pts_info"][i_index]["time"] = ""
        self.jsonResultScore["score_pts_info"][i_index]["conf"] = 0.0
        self.jsonResultScore["score_pts_info"][i_index]["frame_num"] = 0

        # call callback server ,sent now score to client and save to redis
        upload_redis_or_save_json_local(
            jsonScoreNow=self.jsonResultScore,
            path=self.path_save,
            call_back_url=self.real_back_url,
            filename="scoreinfo.json",
            dir_local=SCORE_ROOT_PATH,
            up_callback=self.real_status)
        # up_callback=not self.is_mp4)
        # exec(f'self.scorePoint{index} = False')
        self.post_retrace(index, *args, **kwargs)
        return True

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 10
        self.pos_top = []
        self.pos_front = []
        self.moving_front = []
        self.moving_top = []
        self.count = []
        self.width, self.height = 1920, 1080
        self.is_first = False
        self.iou_ = 100.0
        self.has_clue = False
        # self.small_box_front = None
        # self.big_box_front = None
        # self.small_box_top = None
        # self.big_box_top = None
        # self.magnet_types = []

        self.x_front_min_1, self.x_front_max_1 = 9999, -9999
        self.x_front_min_2, self.x_front_max_2 = 9999, -9999

        self.y_front_min_1, self.y_front_max_1 = 9999, -9999
        self.y_front_min_2, self.y_front_max_2 = 9999, -9999

        self.x_top_min_1, self.x_top_max_1 = 9999, -9999
        self.x_top_min_2, self.x_top_max_2 = 9999, -9999

        self.y_top_min_1, self.y_top_max_1 = 9999, -9999
        self.y_top_min_2, self.y_top_max_2 = 9999, -9999
        self.desktop_area = [
            int(self.width * 0.3),
            int(self.height * 0.5),
            int(self.width * 0.7), self.height
        ]

    def has_score(self):
        for score in self.exp_ok:
            if score != -1:
                return True
        return False

    def exp_filter(self, d_front, d_top):
        d = {"front": {}, "top": {}}
        for key, vals in d_top.items():
            if "front" in key:
                continue
            d["top"][key] = vals

        for key, vals in d_front.items():
            if "top" in key:
                continue
            d["front"][key] = vals
        if "线圈" in d["top"].keys() and not ("移动线圈_顶视" in d["top"].keys()):
            coil = d["top"]["线圈"][0]
            magnet = None
            if "磁铁_N_顶视" in d["top"].keys():
                magnet = d["top"]["磁铁_N_顶视"][0]
            elif "磁铁_S_顶视" in d["top"].keys():
                magnet = d["top"]["磁铁_S_顶视"][0]
            if magnet is not None:

                area = [0, 1000, 1920, 1080]
                if iou(area, magnet) > 0 and iou(coil, magnet) > 0:
                    xmin = min(magnet[0], coil[0])
                    ymin = min(magnet[1], coil[1])
                    xmax = min(magnet[2], coil[2])
                    ymax = min(magnet[3], coil[3])
                    box_new = [[xmin, ymin, xmax, ymax, 0.6]]
                    d["top"]["移动线圈_顶视"] = box_new

        return d

    def get_box(self):
        if self.frame_id % 5 == 0:
            self.big_box_top = None
            self.small_box_top = None
            self.big_box_front = None
            self.small_box_front = None

        if "磁铁" in self.d["top"].keys():
            if len(self.d["top"]["磁铁"]) == 1:
                if self.big_box_top is not None and self.small_box_top is not None:
                    magnet = self.d["top"]["磁铁"][0]
                    iou1 = iou(magnet, self.big_box_top)
                    iou2 = iou(magnet, self.small_box_top)
                    if iou1 > iou2:
                        self.big_box_top = magnet
                        self.small_box_top = None
                    else:
                        self.big_box_top = None
                        self.small_box_top = magnet

                elif self.small_box_top is not None and self.small_box_top is None:
                    magnet = self.d["top"]["磁铁"][0]
                    if iou(magnet, self.small_box_top) > 0:
                        self.small_box_top = magnet
                        self.big_box_top = None
                elif self.small_box_top is None and self.small_box_top is not None:
                    magnet = self.d["top"]["磁铁"][0]
                    if iou(magnet, self.big_box_top) > 0:
                        self.small_box_top = None
                        self.big_box_top = magnet

            if len(self.d["top"]["磁铁"]) == 2:
                if self.big_box_top is None and self.small_box_top is None:
                    magnets = sorted(
                        self.d["top"]["磁铁"],
                        key=lambda x: max(x[2] - x[0], x[3] - x[1]))
                    self.small_box_top = magnets[0]
                    self.big_box_top = magnets[1]
                elif self.big_box_top is not None and self.small_box_top is None:
                    magnet1 = self.d["top"]["磁铁"][0]
                    magnet2 = self.d["top"]["磁铁"][1]
                    iou1 = iou(magnet1, self.big_box_top)
                    iou2 = iou(magnet2, self.big_box_top)
                    if iou1 > 0 and iou1 > iou2:
                        self.big_box_top = magnet1
                        self.small_box_top = magnet2
                    elif iou2 > 0 and iou2 > iou1:
                        self.big_box_top = magnet2
                        self.small_box_top = magnet1
                    elif iou1 == iou2 == 0:
                        self.big_box_top = None
                elif self.big_box_top is None and self.small_box_top is not None:
                    magnet1 = self.d["top"]["磁铁"][0]
                    magnet2 = self.d["top"]["磁铁"][1]
                    iou1 = iou(magnet1, self.small_box_top)
                    iou2 = iou(magnet2, self.small_box_top)
                    if iou1 > 0 and iou1 > iou2:
                        self.small_box_top = magnet1
                        self.big_box_top = magnet2
                    elif iou2 > 0 and iou2 > iou1:
                        self.small_box_top = magnet2
                        self.big_box_top = magnet1
                    elif iou1 == iou2 == 0:
                        self.small_box_top = None
                else:
                    magnet1 = self.d["top"]["磁铁"][0]
                    magnet2 = self.d["top"]["磁铁"][1]
                    iou1 = iou(magnet1, self.small_box_top)
                    iou2 = iou(magnet2, self.small_box_top)
                    if iou1 > 0 and iou1 > iou2:
                        self.small_box_top = magnet1
                    elif iou2 > 0 and iou2 > iou1:
                        self.small_box_top = magnet2
                    elif iou1 == iou2 == 0:
                        self.small_box_top = None
                    iou1 = iou(magnet1, self.big_box_top)
                    iou2 = iou(magnet2, self.big_box_top)
                    if iou1 > iou2 > 0:
                        self.big_box_top = magnet1
                    elif iou2 > iou1 > 0:
                        self.big_box_top = magnet2
                    elif iou1 == iou2 == 0:
                        self.big_box_top = None
        if "磁铁" in self.d["front"].keys():
            if len(self.d["front"]["磁铁"]) == 1:
                if self.big_box_front is not None and self.small_box_front is not None:
                    magnet = self.d["front"]["磁铁"][0]
                    iou1 = iou(magnet, self.big_box_front)
                    iou2 = iou(magnet, self.small_box_front)
                    if iou1 > iou2:
                        self.big_box_front = magnet
                        self.small_box_front = None
                    else:
                        self.big_box_front = None
                        self.small_box_front = magnet

                elif self.small_box_front is not None and self.small_box_front is None:
                    magnet = self.d["front"]["磁铁"][0]
                    if iou(magnet, self.small_box_front) > 0:
                        self.small_box_front = magnet
                        self.big_box_front = None
                elif self.small_box_front is None and self.small_box_front is not None:
                    magnet = self.d["front"]["磁铁"][0]
                    if iou(magnet, self.big_box_front) > 0:
                        self.small_box_front = None
                        self.big_box_front = magnet

            if len(self.d["front"]["磁铁"]) == 2:
                if self.big_box_front is None and self.small_box_front is None:
                    magnets = sorted(
                        self.d["front"]["磁铁"],
                        key=lambda x: max(x[2] - x[0], x[3] - x[1]))
                    self.small_box_front = magnets[0]
                    self.big_box_front = magnets[1]
                elif self.big_box_front is not None and self.small_box_front is None:
                    magnet1 = self.d["front"]["磁铁"][0]
                    magnet2 = self.d["front"]["磁铁"][1]
                    iou1 = iou(magnet1, self.big_box_front)
                    iou2 = iou(magnet2, self.big_box_front)
                    if iou1 > 0 and iou1 > iou2:
                        self.big_box_front = magnet1
                        self.small_box_front = magnet2
                    elif iou2 > 0 and iou2 > iou1:
                        self.big_box_front = magnet2
                        self.small_box_front = magnet1
                    elif iou1 == iou2 == 0:
                        self.big_box_front = None
                elif self.big_box_front is None and self.small_box_front is not None:
                    magnet1 = self.d["front"]["磁铁"][0]
                    magnet2 = self.d["front"]["磁铁"][1]
                    iou1 = iou(magnet1, self.small_box_front)
                    iou2 = iou(magnet2, self.small_box_front)
                    if iou1 > 0 and iou1 > iou2:
                        self.small_box_front = magnet1
                        self.big_box_front = magnet2
                    elif iou2 > 0 and iou2 > iou1:
                        self.small_box_front = magnet2
                        self.big_box_front = magnet1
                    elif iou1 == iou2 == 0:
                        self.small_box_front = None
                else:
                    magnet1 = self.d["front"]["磁铁"][0]
                    magnet2 = self.d["front"]["磁铁"][1]
                    iou1 = iou(magnet1, self.small_box_front)
                    iou2 = iou(magnet2, self.small_box_front)
                    if iou1 > 0 and iou1 > iou2:
                        self.small_box_front = magnet1
                    elif iou2 > 0 and iou2 > iou1:
                        self.small_box_front = magnet2
                    elif iou1 == iou2 == 0:
                        self.small_box_front = None
                    iou1 = iou(magnet1, self.big_box_front)
                    iou2 = iou(magnet2, self.big_box_front)
                    if iou1 > 0 and iou1 > iou2:
                        self.big_box_front = magnet1
                    elif iou2 > 0 and iou2 > iou1:
                        self.big_box_front = magnet2
                    elif iou1 == iou2 == 0:
                        self.big_box_front = None
            if self.big_box_top is not None and self.small_box_top is not None:
                xmin_big = self.width - self.big_box_top[2]
                xmax_big = self.width - self.big_box_top[0]

                xmin_small = self.width - self.small_box_top[2]
                xmax_small = self.width - self.small_box_top[0]
                if len(self.d["front"]["磁铁"]) == 1:
                    iou1 = iou([xmin_big, 0, xmax_big, self.height],
                               self.d["front"]["磁铁"][0])
                    iou2 = iou([xmin_small, 0, xmax_small, self.height],
                               self.d["front"]["磁铁"][0])

                    if iou1 > iou2:
                        if self.big_box_front is None:
                            self.big_box_front = self.d["front"]["磁铁"][0]
                    elif iou2 > iou1:
                        if self.small_box_front is None:
                            self.small_box_front = self.d["front"]["磁铁"][0]
                elif len(self.d["front"]["磁铁"]) == 2:
                    magnet1 = self.d["front"]["磁铁"][0]
                    magnet2 = self.d["front"]["磁铁"][1]
                    iou1 = iou([xmin_big, 0, xmax_big, self.height], magnet1)
                    iou2 = iou([xmin_small, 0, xmax_small, self.height],
                               magnet1)

                    iou3 = iou([xmin_big, 0, xmax_big, self.height], magnet2)
                    iou4 = iou([xmin_small, 0, xmax_small, self.height],
                               magnet2)

                    if iou1 > iou2 and iou3 < iou4:
                        if self.big_box_front is None:
                            self.big_box_front = magnet1
                        if self.small_box_front is None:
                            self.small_box_front = magnet2
                    elif iou1 < iou2 and iou3 > iou4:
                        if self.big_box_front is None:
                            self.big_box_front = magnet2
                        if self.small_box_front is None:
                            self.small_box_front = magnet1

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

        time_process_start = time.time()
        top_true = False
        front_true = False

        if pred_top != None:
            if pred_top.shape[0]:
                for i in range(0, 4, 2):
                    pred_top[:, 0 + i] = torch.clamp(pred_top[:, 0 + i], 0,
                                                     1920)
                    pred_top[:, 1 + i] = torch.clamp(pred_top[:, 1 + i], 0,
                                                     1080)
            self.preds_top, self.objects_top = self.assign_labels(
                frame_top, pred_top, names_label)
            top_true = True
        if pred_front != None:
            if pred_front.shape[0]:
                for i in range(0, 4, 2):
                    pred_front[:, 0 + i] = torch.clamp(pred_front[:, 0 + i], 0,
                                                       1920)
                    pred_front[:, 1 + i] = torch.clamp(pred_front[:, 1 + i], 0,
                                                       1080)
            self.preds_front, self.objects_front = self.assign_labels(
                frame_front, pred_front, names_label)
            front_true = True
        #print(names_label, pred_top, self.preds_top)
        if top_true and front_true:
            if self.width == 0:
                self.width, self.height = frame_top.shape[1], frame_top.shape[
                    0]

            self.rtmp_push_fun(
                top_img=frame_top,
                front_img=frame_front,
                side_img=frame_side,
                top_preds=self.preds_top,
                front_preds=self.preds_front,
                side_preds=None)

            d_front = dict()
            d_top = dict()

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
                if boxes.size(0) > 0:
                    d_front[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_top):
                if boxes.size(0) > 0:
                    d_top[label] = boxes.cpu().numpy()
            self.d = self.exp_filter(d_front, d_top)
            # self.get_box()

            if DEBUG_:
                show_front = copy.copy(self.frame_front)
                show_top = copy.copy(self.frame_top)
                preds_front = preds_top = [], []

                # if self.big_box_front is not None:
                #     x = 0.5 * (self.big_box_front[0] + self.big_box_front[2])
                #     y = 0.5 * (self.big_box_front[1] + self.big_box_front[3])
                #     cv2.putText(show_front, "big" ,(int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,255),3)
                # if self.small_box_front is not None:
                #     x = 0.5 * (self.small_box_front[0] + self.small_box_front[2])
                #     y = 0.5 * (self.small_box_front[1] + self.small_box_front[3])
                #     cv2.putText(show_front, "small", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,255),3)
                # if self.big_box_top is not None:
                #     x = 0.5 * (self.big_box_top[0] + self.big_box_top[2])
                #     y = 0.5 * (self.big_box_top[1] + self.big_box_top[3])
                #     cv2.putText(show_top, "big" ,(int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,255),3)
                # if self.small_box_top is not None:
                #     x = 0.5 * (self.small_box_top[0] + self.small_box_top[2])
                #     y = 0.5 * (self.small_box_top[1] + self.small_box_top[3])
                #     cv2.putText(show_top, "small", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,255),3)
                self.plot(self.preds_front, show_front)
                self.plot(self.preds_top, show_top)
                tl = self.desktop_area[:2]
                br = self.desktop_area[2:]
                cv2.rectangle(show_top, tl, br, (0, 255, 255), 2)
                cv2.imshow("front_img0", cv2.resize(show_front, (960, 540)))
                cv2.imshow("top_img0", cv2.resize(show_top, (960, 540)))

                cv2.waitKey(1)

            if self.is_first is None:
                if "电流表_顶视" in self.d["top"].keys():
                    a = self.d["top"]["电流表_顶视"][0]
                    w = min(a[2] - a[0], a[3] - a[1])
                    if w > 0.09 * self.width:
                        self.is_first = False
                    else:
                        self.is_first = True
            self.frame_id += 1
            # 1. 选择灵敏电流计进行实验
            if not self.has_clue:
                if self.j1():
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(1, "top")

            # 2. 将蹄形磁铁按图所示放置
            if -1 == self.exp_ok[1]:
                if self.j2():
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, "top")
                    return
            # 3. 连接成闭合回路
            if -1 == self.exp_ok[2]:
                if self.j3():
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, "top")
                    return
            # 4. 将蹄形磁铁N极在上,线圈向里运动(不是来回运动),正确报告电表偏转的方向
            # 5. 将蹄形磁铁N极在上,线圈向外运动(不是来回运动),正确报告电表偏转的方向
            # 6. 将蹄形磁铁S极在上,线圈向里运动(不是来回运动),正确报告电表偏转的方向
            # 7. 将蹄形磁铁S极在上,线圈向外运动(不是来回运动),正确报告电表偏转的方向
            if -1 != self.exp_ok[2] and -1 == self.exp_ok[3]:
                ret, view, res = self.j4567()
                if ret:
                    self.update(view, res, assign_score_fun)
            # 8. 得出感应电流的方向与导体运动方向有关
            # 9. 得出感应电流的方向与磁场方向有关

            # 10. 实验结束后，将实验器材放回原处
            if -1 != self.exp_ok[2]:
                ret, iou_ = self.j10()
                if ret:
                    if iou_ <= self.iou_:
                        self.iou_ = iou_
                        self.exp_ok[9] = self.frame_id
                        assign_score_fun(10, "top")
                        return

    def j1(self):
        if self.exp_ok[2] == -1:
            return False
        if self.exp_ok[0] == -1 and not (self.has_clue):
            if not ("电流表_顶视" in self.d["top"].keys()):
                return False
            if not ("连接完成_顶视" in self.d["top"].keys()):
                return False
            return True

        if not ("电流表_顶视" in self.d["top"].keys()):
            return False
        if not ("连接完成_顶视" in self.d["top"].keys()):
            return False
        if ("蓝色_顶视" in self.d["top"].keys()):
            bs = self.d["top"]["电流表_顶视"]
            c = self.d["top"]["连接完成_顶视"][0]
            lan = self.d["top"]["蓝色_顶视"][0]
            for b in bs:
                if iou(b, lan) > 0 and iou(b, c) > 0 and iou(lan, c) > 0:
                    self.has_clue = True
                    return False
                if iou(b, lan) > 0 and iou(b, c) == 0 and iou(lan, c) == 0:
                    self.has_clue = True
                    self.retracementScore(1)
                    return False

        if ("紫色_顶视" in self.d["top"].keys()):
            bs = self.d["top"]["电流表_顶视"]
            c = self.d["top"]["连接完成_顶视"][0]
            zi = self.d["top"]["紫色_顶视"][0]
            for b in bs:
                if iou(b, zi) > 0 and iou(b, c) > 0 and iou(zi, c) > 0:
                    self.has_clue = True
                    self.retracementScore(1)
                    return False
                if iou(b, zi) > 0 and iou(b, c) == 0 and iou(zi, c) == 0:
                    self.has_clue = True
                    return False

        if not self.is_first:
            if ("G_顶视" in self.d["top"].keys()):
                bs = self.d["top"]["电流表_顶视"]
                g = self.d["top"]["G_顶视"][0]
                c = self.d["top"]["连接完成_顶视"][0]
                for b in bs:
                    if iou(b, g) > 0 and iou(b, c) > 0:
                        self.has_clue = True
                        return False
                    if iou(b, g) > 0 and iou(b, c) == 0:
                        self.has_clue = True
                        self.retracementScore(1)
                        return False

            if ("A_顶视" in self.d["top"].keys()):
                bs = self.d["top"]["电流表_顶视"]
                a = self.d["top"]["A_顶视"][0]
                c = self.d["top"]["连接完成_顶视"][0]
                for b in bs:
                    if iou(b, a) > 0 and iou(b, c) > 0:
                        self.has_clue = True
                        self.retracementScore(1)
                        return False
                    if iou(b, a) > 0 and iou(b, c) == 0:
                        self.has_clue = True
                        return False
        return False

    def j2(self):

        if not ("电流表_顶视" in self.d["top"].keys()):
            return False
        # if not("磁铁" in self.d["top"].keys()):
        #     return False
        if not ("磁铁_S_前视" in self.d["front"].keys()) and not (
                "磁铁_N_前视" in self.d["front"].keys()) and not (
                    "磁铁_N_顶视" in self.d["top"].keys()) and not (
                        "磁铁_S_顶视" in self.d["top"].keys()):
            return False
        if "磁铁_N_顶视" in self.d["top"].keys():
            return True
            # n = self.d["top"]["磁铁_N_顶视"][0]
            # if self.is_first:
            #     area = [
            #         0.38 * self.width, 0.38 * self.height, 0.65 * self.width,
            #         self.height
            #     ]
            # else:
            #     area = [
            #         0.25 * self.width, 0.55 * self.height, 0.75 * self.width,
            #         self.height
            #     ]
            # if all_in(n, area):
            #     return True
        return False

    def j3(self):
        # 1. 将线圈与灵敏电流计连接
        if not ("线圈" in self.d["top"].keys()) and not (
                "线圈" in self.d["front"].keys()):
            return False
        if not ("电流表_顶视" in self.d["top"].keys()):
            return False
        if not ("连接完成_顶视" in self.d["top"].keys()):
            return False
        return True

    def j4567(self):
        # 4. 将蹄形磁铁N极在上,线圈向里运动(不是来回运动),正确报告电表偏转的方向
        # 5. 将蹄形磁铁N极在上,线圈向外运动(不是来回运动),正确报告电表偏转的方向
        # 6. 将蹄形磁铁S极在上,线圈向里运动(不是来回运动),正确报告电表偏转的方向
        # 7. 将蹄形磁铁S极在上,线圈向外运动(不是来回运动),正确报告电表偏转的方向
        ## 器材都ok

        if not ("电流表_顶视" in self.d["top"].keys()):
            return False, None, [0, 0, 0, 0, -1, "still"]

        if not ("线圈" in self.d["front"].keys()) and not (
                "线圈" in self.d["top"].keys()):

            return False, None, [0, 0, 0, 0, -1, "still"]

        if not ("磁铁" in self.d["front"].keys()) and not (
                "磁铁" in self.d["top"].keys()
                or "磁铁_N_顶视" in self.d["top"].keys()
                or "磁铁_S_顶视" in self.d["top"].keys()):

            return False, None, [0, 0, 0, 0, -1, "still"]

        if not ("移动线圈_前视" in self.d["front"].keys()) and not (
                "移动线圈_顶视" in self.d["top"].keys()):

            return False, None, [0, 0, 0, 0, -1, "still"]
        x_front, y_front, x_top, y_top, m_type = 0, 0, 0, 0, "still"

        ## 前视移动判断

        def j_front():
            if "线圈" in self.d["front"].keys() and "磁铁" in self.d["front"].keys(
            ) and "移动线圈_前视" in self.d["front"].keys():
                coil = self.d["front"]["线圈"][0]
                magnet = self.d["front"]["磁铁"][0]
                move = self.d["front"]["移动线圈_前视"][0]

                m_w = magnet[2] - magnet[0]
                m_h = magnet[3] - magnet[1]
                if m_w >= m_h:
                    m_type = "horizontal"
                else:
                    m_type = "vertical"
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.pos_front.append((x, y))
                if len(self.pos_front) > 10:
                    self.pos_front = self.pos_front[1:]
                if iou(move, magnet) == 0:
                    return False, None
                pos_npy = np.array(self.pos_front, dtype=np.float)
                var_x = pos_npy[:, 0].var()
                var_y = pos_npy[:, 1].var()

                if m_type == "horizontal" and var_x > 100:
                    return True, [x, y, m_type]
            return False, None

        def j_top():
            global m_type, x_top, y_top
            if "线圈" in self.d["top"].keys(
            ) and "移动线圈_顶视" in self.d["top"].keys():
                coil = self.d["top"]["线圈"][0]
                if "磁铁_N_顶视" in self.d["top"].keys():
                    magnet = self.d["top"]["磁铁_N_顶视"][0]
                elif "磁铁_S_顶视" in self.d["top"].keys():
                    magnet = self.d["top"]["磁铁_S_顶视"][0]
                elif "磁铁" in self.d["top"].keys():
                    magnet = self.d["top"]["磁铁"][0]
                else:
                    return False, None
                move = self.d["top"]["移动线圈_顶视"][0]

                m_w = magnet[2] - magnet[0]
                m_h = magnet[3] - magnet[1]
                if m_w >= m_h:
                    m_type = "horizontal"
                else:
                    m_type = "vertical"
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.pos_top.append((x, y))
                if len(self.pos_top) > 10:
                    self.pos_top = self.pos_top[1:]
                if iou(move, magnet) == 0:
                    return False, None
                pos_npy = np.array(self.pos_top, dtype=np.float)
                var_x = pos_npy[:, 0].var()
                var_y = pos_npy[:, 1].var()
                if m_type == "horizontal" and var_x > 100:
                    x_top = x
                    y_top = y
                    return True, [x, y, m_type]
                elif m_type == "vertical" and var_y > 100:
                    x_top = x
                    y_top = y
                    return True, [x, y, m_type]
            return False, None

        magnet_type = -1
        if "磁铁" in self.d["front"].keys():
            if "磁铁_N_前视" in self.d["front"].keys(
            ) and "磁铁_S_前视" in self.d["front"].keys():
                # 利用前视判断magnet_type

                magnet = self.d["front"]["磁铁"][0]
                magnet_n = self.d["front"]["磁铁_N_前视"][0]
                magnet_s = self.d["front"]["磁铁_S_前视"][0]

                yn = 0.5 * (magnet_n[1] + magnet_n[3])
                ys = 0.5 * (magnet_s[1] + magnet_s[3])
                if yn < ys:
                    y = 1
                else:
                    y = 2
                magnet_type = y

        if magnet_type == -1:
            if "磁铁_N_顶视" in self.d["top"].keys():
                magnet_type = 1
            elif "磁铁_S_顶视" in self.d["top"].keys():
                magnet_type = 2
        ret, res = j_top()
        if ret:
            x_top, y_top, m_type = res
            if magnet_type != -1:
                # print("top", x_front, y_front, x_top, y_top, magnet_type,
                #       m_type)

                return True, "top", [
                    x_front, y_front, x_top, y_top, magnet_type, m_type
                ]
        else:
            ret, res = j_front()
            if ret:
                x_front, y_front, m_type = res
                if magnet_type != -1:
                    # print("front", x_front, y_front, x_top, y_top, magnet_type,
                    #       m_type)
                    return True, "front", [
                        x_front, y_front, x_top, y_top, magnet_type, m_type
                    ]

        return False, None, [0, 0, 0, 0, -1, magnet_type, m_type]

    def j10(self):

        if "桌面整洁_顶视" in self.d["top"].keys():
            iou_ = 0.
            for key, vals in self.d["top"].items():
                if key == "桌面整洁_顶视":
                    continue
                val = vals[0]
                iou_ += iou(val, self.d["top"]["桌面整洁_顶视"][0])
            return True, iou_
        # 二代
        if not self.is_first:
            for key, vals in self.d["top"].items():
                val = vals[0]
                # if DEBUG_:
                #     print(iou(area, val))
                if iou(self.desktop_area, val) > 0:
                    return False, 1.0
            return True, 0.
        else:
            for key, vals in self.d["top"].items():
                val = vals[0]
                if iou(self.desktop_area, val) > 0:
                    return False, 1.0
            return True, 0.
        return False, 1.0

    def update(self, view, res, assign_score_fun):
        x_front, y_front, x_top, y_top, magnet_type, m_type = res
        # if DEBUG_:
        #     print(res)
        if view == "top":
            # 左移动 = 向里
            if magnet_type == 1:
                if m_type == "horizontal":
                    if x_top < self.x_top_min_1:  # or y_top < self.y_top_min:
                        self.x_top_min_1 = x_top
                        assign_score_fun(4, view)
                    elif x_top > self.x_top_max_1:
                        self.x_top_max_1 = x_top
                        assign_score_fun(5, view)
                elif m_type == "vertical":
                    if y_top < self.y_top_min_1:  # or y_top < self.y_top_min:
                        self.y_top_min_1 = y_top
                        assign_score_fun(5, view)
                    elif y_top > self.y_top_max_1:
                        self.y_top_max_1 = y_top
                        assign_score_fun(4, view)

            elif magnet_type == 2:
                if m_type == "horizontal":
                    if x_top < self.x_top_min_2:  # or y_top < self.y_top_min:
                        self.x_top_min_2 = x_top
                        assign_score_fun(6, view)
                    elif x_top > self.x_top_max_2:
                        self.x_top_max_2 = x_top
                        assign_score_fun(7, view)
                elif m_type == "vertical":
                    if y_top < self.y_top_min_2:  # or y_top < self.y_top_min:
                        self.y_top_min_2 = y_top
                        assign_score_fun(7, view)
                    elif y_top > self.y_top_max_2:
                        self.y_top_max_2 = y_top
                        assign_score_fun(6, view)
        if view == "front":
            if magnet_type == 1:
                if m_type == "horizontal":
                    if x_front < self.x_front_min_1:  # or y_top < self.y_top_min:
                        self.x_front_min_1 = x_front
                        assign_score_fun(5, view)
                    elif x_front > self.x_front_max_1:
                        self.x_front_max_1 = x_front
                        assign_score_fun(4, view)
            elif magnet_type == 2:
                if m_type == "horizontal":
                    if x_front < self.x_front_min_2:  # or y_top < self.y_top_min:
                        self.x_front_min_2 = x_front
                        assign_score_fun(7, view)
                    elif x_front > self.x_front_max_2:
                        self.x_front_max_2 = x_front
                        assign_score_fun(6, view)
