from PIL import Image
from logger import logger
from .comm import *
from .comm.course_base import ConfigModel
import copy
from utilsg.litF import upload_redis_or_save_json_local
from configg.global_config import SCORE_ROOT_PATH
DEBUG_ = False


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


def all_in(box1, box2):
    return box2[0] <= box1[0] <= box2[2] and box2[1] <= box1[3] <= box2[3]


class BIO_make_leaf_sz(ConfigModel):
    def __init__(self):
        super(BIO_make_leaf_sz, self).__init__()
        self.initScore()

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

    def post_retrace(self, index, *args, **kwargs):
        self.exp_ok[index - 1] = -1

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 10
        self.iou_ = 100.0
        self.width, self.height = 1920, 1080
        self.pre_ok = False
        self.pre_ok_id = -1
        self.is_get_bo = False
        self.next_ok = False
        self.is_put = False
        self.iou1 = 0.
        self.okr = 0
        self.dis = []
        self.is_first = False
        self.has_clue = False
        self.max_score_di = 0.
        self.max_score_ca = 0.
        self.max_score_op = 0.
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

    def exp_filter(self, d_front, d_top, d_side):
        d = {"front": {}, "top": {}, "side": {}}
        for key, vals in d_top.items():
            d["top"][key] = sorted(vals, key=lambda x: -x[4])
        for key, vals in d_front.items():
            d["front"][key] = sorted(vals, key=lambda x: -x[4])
        for key, vals in d_side.items():
            if key in ["滴瓶_取用", "滴瓶_未取用", "标签纸_红色", "标签纸_蓝色"]:
                vals = [
                    val for val in vals
                    if (val[0] + val[2] > 1920) and (val[1] + val[3] > 1080)
                ]
                if len(vals):
                    d["side"][key] = sorted(vals, key=lambda x: -x[4])
            else:
                d["side"][key] = sorted(vals, key=lambda x: -x[4])
        return d

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
        if pred_side != None:
            if pred_side.shape[0]:
                for i in range(0, 4, 2):
                    pred_side[:, 0 + i] = torch.clamp(pred_side[:, 0 + i], 0,
                                                      1920)
                    pred_side[:, 1 + i] = torch.clamp(pred_side[:, 1 + i], 0,
                                                      1080)
            self.preds_side, self.objects_side = self.assign_labels(
                frame_side, pred_side, names_label)
            side_true = True

        if top_true and front_true and side_true:
            if self.width == 0:
                self.width, self.height = frame_top.shape[1], frame_top.shape[
                    0]

            self.rtmp_push_fun(
                top_img=frame_top,
                front_img=frame_front,
                side_img=frame_side,
                top_preds=self.preds_top,
                front_preds=self.preds_front,
                side_preds=self.preds_side)

            d_front = dict()
            d_top = dict()
            d_side = dict()

            def assign_score_fun(index, view):
                self.assignScore(
                    index=index,
                    img=eval(f"self.frame_{view}"),
                    object=eval(f"self.objects_{view}"),
                    conf=0.1,
                    time_frame=eval(f"self.time_{view}"),
                    num_frame=eval(f"self.num_frame_{view}"),
                    name_save=f"{index}.jpg",
                    preds=eval(f"self.preds_{view}"))

            for label, boxes in zip(self.labels, self.preds_front):
                if boxes.size(0) > 0:
                    d_front[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_top):
                if boxes.size(0) > 0:
                    d_top[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_side):
                if boxes.size(0) > 0:
                    d_side[label] = boxes.cpu().numpy()
            self.d = self.exp_filter(d_front, d_top, d_side)
            if DEBUG_:
                show_front = copy.copy(self.frame_front)
                show_top = copy.copy(self.frame_top)
                show_side = copy.copy(self.frame_side)

                self.plot(self.preds_front, show_front)
                self.plot(self.preds_top, show_top)
                self.plot(self.preds_side, show_side)
                tl = tuple(self.desktop_area[:2])
                br = tuple(self.desktop_area[2:])
                cv2.rectangle(show_top, tl, br, (0, 255, 255), 2)
                if len(self.dis):
                    if self.dis.count("红") > self.dis.count("蓝"):
                        cv2.rectangle(show_top, (0, 0), (200, 100),
                                      (0, 0, 255), -1)
                    elif self.dis.count("红") < self.dis.count("蓝"):
                        cv2.rectangle(show_top, (0, 0), (200, 100),
                                      (255, 0, 0), -1)

                cv2.imshow("front_img0", cv2.resize(show_front, (960, 540)))
                cv2.imshow("top_img0", cv2.resize(show_top, (960, 540)))
                cv2.imshow("side_img0", cv2.resize(show_side, (960, 540)))

                cv2.waitKey(1)
            if self.is_first is None:
                if "滴瓶_未取用" in self.d["top"].keys():
                    di = self.d["top"]["滴瓶_未取用"][0]
                    w = min(di[2] - di[0], di[3] - di[1])
                    if w > 0.045 * self.width:
                        self.is_first = False
                    else:
                        self.is_first = True
            self.frame_id += 1
            # 1. 选取清水实验
            if not self.has_clue:
                ret, view = self.j1()
                if ret:
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(1, view)
                    return

            # 2. 选叶片下表皮
            if -1 == self.exp_ok[1]:
                ret, view = self.j2()
                if ret:
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, view)
                    return
            # 3. 用洁净的纱布擦拭载玻片和盖玻片
            if True:
                ret, view, score = self.j3()
                if ret:
                    if score > self.max_score_ca:
                        self.max_score_ca = score
                        self.exp_ok[2] = self.frame_id
                        assign_score_fun(3, view)
                        return

            # 4. 在载玻片中央滴加清水
            if True:
                ret, view, score = self.j4()
                if ret:
                    if score > self.max_score_di:
                        self.max_score_di = score
                        self.exp_ok[3] = self.frame_id
                        assign_score_fun(4, view)
                        if self.exp_ok[0] != -1:
                            assign_score_fun(1, view)
                        return

            # 5. 撕下一小块叶片下表皮
            if -1 == self.exp_ok[4]:
                ret, view = self.j5()
                if ret:
                    self.exp_ok[4] = self.frame_id
                    assign_score_fun(5, view)
                    return

            # 6. 将叶表皮置于载玻片的水滴中, 并用镊子展平
            # 7. 用镊子夹起盖玻片, 使它的一边先接触水滴, 再缓缓放下
            if (-1 != self.exp_ok[4] or -1 != self.exp_ok[3]):
                ret, view, score = self.j6()
                if ret:
                    if score > self.max_score_op:
                        self.max_score_op = score
                        self.exp_ok[5] = self.frame_id
                        assign_score_fun(6, view)
                        for view_ in ["top", "front", "side"]:
                            if view_ != view:
                                self.exp_ok[6] = self.frame_id
                                assign_score_fun(7, view)
                                break

            # 9. 实验结束, 将临时装片直接放入回收烧杯, 整理并清洁桌面
            if -1 != self.exp_ok[3] or (self.frame_id > 1500
                                        and self.has_score()):
                ret, iou_ = self.j9()
                if ret:
                    if iou_ <= self.iou_:
                        self.iou_ = iou_
                        self.exp_ok[8] = self.frame_id
                        assign_score_fun(9, "top")
                        return

    def get_di(self):
        if len(self.dis) <= 10:
            if not (("滴水" in self.d["top"].keys()) or
                    ("滴水" in self.d["front"].keys()) or
                    ("滴水" in self.d["side"].keys())):
                return

            def j_front():

                if ("滴瓶_取用" in self.d["front"].keys()) and (
                        "标签纸_红色" in self.d["front"].keys()):
                    used = self.d["front"]["滴瓶_取用"][0]

                    biaos = self.d["front"]["标签纸_红色"]
                    for biao in biaos:
                        if all_in(biao, used):
                            self.dis.append("红")
                            return True
                    return False

                elif ("滴瓶_取用" in self.d["front"].keys()) and (
                        "标签纸_蓝色" in self.d["front"].keys()):
                    used = self.d["front"]["滴瓶_取用"][0]
                    biaos = self.d["front"]["标签纸_蓝色"]
                    for biao in biaos:
                        if all_in(biao, used):
                            self.dis.append("蓝")
                            return True
                    return False

                return False

            def j_top():
                if ("滴瓶_取用" in self.d["top"].keys()) and (
                        "标签纸_红色" in self.d["top"].keys()):
                    used = self.d["top"]["滴瓶_取用"][0]
                    biaos = self.d["top"]["标签纸_红色"]
                    for biao in biaos:
                        if all_in(biao, used):
                            self.dis.append("红")
                            return True
                    return False
                elif ("滴瓶_取用" in self.d["top"].keys()) and (
                        "标签纸_蓝色" in self.d["top"].keys()):
                    used = self.d["top"]["滴瓶_取用"][0]
                    biaos = self.d["top"]["标签纸_蓝色"]
                    for biao in biaos:
                        if all_in(biao, used):
                            self.dis.append("蓝")
                            return True
                    return False
                elif ("滴瓶_未取用" in self.d["top"].keys()) and (
                        "标签纸_红色" in self.d["top"].keys()):
                    used = self.d["top"]["滴瓶_未取用"][0]
                    biao = self.d["top"]["标签纸_红色"][0]
                    if "标签纸_蓝色" in self.d["top"].keys():
                        biao2 = self.d["top"]["标签纸_蓝色"][0]
                        if iou(used, biao) > 0 and iou(used, biao2):
                            return False
                    if all_in(biao, used):
                        self.dis.append("蓝")
                        return True
                    return False
                elif ("滴瓶_未取用" in self.d["top"].keys()) and (
                        "标签纸_蓝色" in self.d["top"].keys()):
                    used = self.d["top"]["滴瓶_未取用"][0]
                    biao = self.d["top"]["标签纸_蓝色"][0]
                    if "标签纸_红色" in self.d["top"].keys():
                        biao2 = self.d["top"]["标签纸_红色"][0]
                        if iou(used, biao) > 0 and iou(used, biao2):
                            return False
                    if all_in(biao, used):
                        self.dis.append("红")
                        return True
                    return False
                return False

            def j_side():
                if ("滴瓶_取用" in self.d["side"].keys()) and (
                        "标签纸_红色" in self.d["side"].keys()):
                    used = self.d["side"]["滴瓶_取用"][0]
                    biaos = self.d["side"]["标签纸_红色"]
                    for biao in biaos:
                        if all_in(biao, used):
                            self.dis.append("红")

                            return True
                    return False
                elif ("滴瓶_取用" in self.d["side"].keys()) and (
                        "标签纸_蓝色" in self.d["side"].keys()):
                    used = self.d["side"]["滴瓶_取用"][0]
                    biaos = self.d["side"]["标签纸_蓝色"]
                    for biao in biaos:
                        if all_in(biao, used):
                            self.dis.append("蓝")

                            return True
                    return False
                elif ("滴瓶_未取用" in self.d["side"].keys()) and (
                        "标签纸_红色" in self.d["side"].keys()):
                    used = self.d["side"]["滴瓶_未取用"][0]
                    biao = self.d["side"]["标签纸_红色"][0]
                    if "标签纸_蓝色" in self.d["side"].keys():
                        biao2 = self.d["side"]["标签纸_蓝色"][0]
                        if iou(used, biao) > 0 and iou(used, biao2):
                            return False
                    if all_in(biao, used):
                        self.dis.append("蓝")

                        return True
                    return False
                elif ("滴瓶_未取用" in self.d["side"].keys()) and (
                        "标签纸_蓝色" in self.d["side"].keys()):
                    used = self.d["side"]["滴瓶_未取用"][0]
                    biao = self.d["side"]["标签纸_蓝色"][0]
                    if "标签纸_红色" in self.d["side"].keys():
                        biao2 = self.d["side"]["标签纸_红色"][0]
                        if iou(used, biao) > 0 and iou(used, biao2) > 0:
                            return False
                    if all_in(biao, used):
                        self.dis.append("红")

                        return True
                    return False
                return False

        j_front()

        if len(self.dis) > 10:
            self.dis = self.dis[1:]

    # DONE
    def j1(self):
        self.get_di()
        if self.exp_ok[3] != -1 and self.exp_ok[0] == -1 and not (
                self.has_clue):
            if "滴水" in self.d["top"].keys():
                return True, "top"
            if "滴水" in self.d["front"].keys():
                return True, "front"
            if "滴水" in self.d["side"].keys():
                return True, "side"
            if "滴瓶_取用" in self.d["top"].keys():
                return True, "top"
            if "滴瓶_取用" in self.d["front"].keys():
                return True, "front"
            if "滴瓶_取用" in self.d["side"].keys():
                return True, "side"
        # 三种方式进行判断
        # 1. 直接判断当前帧的三个视角取用之后的滴瓶是否存在标签
        # 2. 间接通过没有取用的滴瓶的标签情况推断当前取用的标签
        # 3. 利用之前帧的跟踪情况推断当前取用的滴瓶的标签

        # track + 侧面推理
        if len(self.dis) == 10:
            if self.dis.count("蓝") > self.dis.count("红"):
                self.has_clue = True
                self.retracementScore(1)
                return False, None
                #return True, "side"
            elif self.dis.count("蓝") < self.dis.count("红"):
                self.has_clue = True
                return False, None

        # # 当前帧判断
        # else:
        #     if not(("滴水" in self.d["top"].keys()) or
        #         ("滴水" in self.d["front"].keys()) or
        #         ("滴水" in self.d["side"].keys())):
        #         return False, None
        #     def j_front():
        #         if not("滴瓶_取用" in self.d["front"].keys()):
        #             return False
        #         used = self.d["front"]["滴瓶_取用"][0]
        #         if "标签纸_蓝色" in self.d["front"].keys():
        #             biaos = self.d["front"]["标签纸_蓝色"]
        #             for biao in biaos:
        #                 if all_in(biao, used):
        #                     self.has_clue = True
        #                     self.retracementScore(1)
        #                     return False
        #         elif "标签纸_红色" in self.d["front"].keys():
        #             biaos = self.d["front"]["标签纸_红色"]
        #             for biao in biaos:
        #                 if all_in(biao, used):
        #                     self.has_clue = True
        #                     return True
        #     def j_top():
        #         if not("滴瓶_取用" in self.d["top"].keys()):
        #             return False
        #         used = self.d["top"]["滴瓶_取用"][0]
        #         if "标签纸_蓝色" in self.d["top"].keys():
        #             biaos = self.d["top"]["标签纸_蓝色"]
        #             for biao in biaos:
        #                 if all_in(biao, used):
        #                     self.has_clue = True
        #                     self.retracementScore(1)
        #                     return False
        #         elif "标签纸_红色" in self.d["top"].keys():
        #             biaos = self.d["top"]["标签纸_红色"]
        #             for biao in biaos:
        #                 if all_in(biao, used):
        #                     self.has_clue = True
        #                     return True
        #     def j_side():
        #         if not("滴瓶_取用" in self.d["side"].keys()):
        #             return False
        #         used = self.d["side"]["滴瓶_取用"][0]
        #         if "标签纸_蓝色" in self.d["side"].keys():
        #             biaos = self.d["side"]["标签纸_蓝色"]
        #             for biao in biaos:
        #                 if all_in(biao, used):
        #                     self.has_clue = True
        #                     self.retracementScore(1)
        #                     return False
        #         elif "标签纸_红色" in self.d["side"].keys():
        #             biaos = self.d["side"]["标签纸_红色"]
        #             for biao in biaos:
        #                 if all_in(biao, used):
        #                     self.has_clue = True
        #                     return True

        #     # ret1 = j_top()
        #     # ret2 = j_front()
        #     # ret3 = j_side()

        #     if j_front():
        #         return True, "front"

        return False, None

    def j2(self):
        if self.exp_ok[4] != -1 and self.frame_id - self.exp_ok[4] > 5:
            return True, "side"
        return False, None

    def j3(self):
        def j_top():
            if not ("手" in self.d["top"].keys()):
                return False
            # if not ("载玻片" in self.d["top"].keys()):
            #     return False
            if not ("擦拭载玻片" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            # if len(hands) < 2:
            #     return False
            ca = self.d["top"]["擦拭载玻片"][0]
            # zai = self.d["top"]["载玻片"][0]
            for hand in hands:
                if iou(ca, hand) > 0:
                    return True

            return False

        def j_front():
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("擦拭载玻片" in self.d["front"].keys()):
                return False
            # if not ("载玻片" in self.d["front"].keys()):
            # return False
            hands = self.d["front"]["手"]
            # if len(hands) < 2:
            #     return False
            ca = self.d["front"]["擦拭载玻片"][0]
            # zai = self.d["front"]["载玻片"][0]
            for hand in hands:
                if iou(ca, hand) > 0:
                    return True
            # if iou(ca, hands[0]) > 0 and iou(ca, hands[1]) > 0 and iou(
            #         ca, zai) > 0:
            #     return True
            return False

        def j_side():
            if not ("手" in self.d["side"].keys()):
                return False
            if not ("擦拭载玻片" in self.d["side"].keys()):
                return False
            # if not ("载玻片" in self.d["side"].keys()):
            #     return False
            hands = self.d["side"]["手"]
            # if len(hands) < 2:
            #      return False
            # zai = self.d["side"]["载玻片"][0]
            ca = self.d["side"]["擦拭载玻片"][0]
            for hand in hands:
                if iou(ca, hand) > 0:
                    return True
            # if iou(ca, hands[0]) > 0 and iou(ca, hands[1]) > 0 and iou(
            #         ca, zai) > 0:
            #     return True
            return False

        if j_top():
            return True, "top", self.d["top"]["擦拭载玻片"][0][4]
        elif j_front():
            return True, "front", self.d["front"]["擦拭载玻片"][0][4]
        elif j_side():
            return True, "side", self.d["side"]["擦拭载玻片"][0][4]
        return False, None, 0.

    # DONE
    def j4(self):
        def j_top():
            if ("滴水" in self.d["top"].keys()):
                return True
            # 用滴管在载玻片中央滴一滴清水
            if not ("手" in self.d["top"].keys()):
                return False
            # if not ("载玻片" in self.d["top"].keys()):
            #     return False
            if not ("滴水" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            # zai = self.d["top"]["载玻片"][0]
            di = self.d["top"]["滴水"][0]
            is_ok = False
            for hand in hands:
                if iou(hand, di) > 0:
                    return True
                # if iou(hand, zai) > 0 and iou(di, hand) > 0:
                # is_ok = True
            # return is_ok
            return False

        def j_front():
            if ("滴水" in self.d["front"].keys()):
                return True
            # 用滴管在载玻片中央滴一滴清水
            if not ("手" in self.d["front"].keys()):
                return False
            # if not ("载玻片" in self.d["front"].keys()):
            #     return False
            if not ("滴水" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            # zai = self.d["front"]["载玻片"][0]
            di = self.d["front"]["滴水"][0]
            is_ok = False
            for hand in hands:
                if iou(hand, di) > 0:
                    return True
                    is_ok = True
            return is_ok

        def j_side():
            # 用滴管在载玻片中央滴一滴清水
            # if not ("手" in self.d["side"].keys()):
            #     return False
            # if not ("载玻片" in self.d["side"].keys()):
            # return False
            if ("滴水" in self.d["side"].keys()):
                return True
            return False
            hands = self.d["side"]["手"]
            # zai = self.d["side"]["载玻片"][0]
            di = self.d["side"]["滴水"][0]
            is_ok = False
            for hand in hands:
                if iou(hand, di) > 0:
                    return True
                #if iou(hand, zai) > 0 and iou(di, hand) > 0:
                #    is_ok = True
            return is_ok

        # print("滴水", j_top()[0], j_front()[0], j_side()[0])
        if j_top():
            return True, "top", self.d["top"]["滴水"][0][4]
        elif j_front():
            return True, "front", self.d["front"]["滴水"][0][4]
        elif j_side():
            return True, "side", self.d["side"]["滴水"][0][4]
        return False, None, 0.

    # DONE
    def j5(self):
        if self.next_ok:
            return True, "top"

        def j_top():
            # 3. 用镊子撕取菠菜叶下表皮
            if not ("手" in self.d["top"].keys()):
                return False
            if not ("镊子" in self.d["top"].keys()):
                return False
            if not ("菠菜叶_顶视" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            if len(hands) < 2:
                return False
            bos = self.d["top"]["菠菜叶_顶视"]
            nies = self.d["top"]["镊子"]
            for bo in bos:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, bo) > 0:
                        nie = nie_
                        break
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    if iou(nie, bo) == 0:
                        return False
                    if iou(hands[i1], nie) > 0 and iou(hands[i2], bo) > 0:
                        return True
                    elif iou(hands[i2], nie) > 0 and iou(hands[i1], bo) > 0:
                        return True
            return False

        def j_front():
            # 3. 用镊子撕取菠菜叶下表皮
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("镊子" in self.d["front"].keys()):
                return False
            if not ("菠菜叶_前视" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            if len(hands) < 2:
                return False
            bos = self.d["front"]["菠菜叶_前视"]
            nies = self.d["front"]["镊子"]
            for bo in bos:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, bo) > 0:
                        nie = nie_
                        break
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    if iou(nie, bo) == 0:
                        return False
                    if iou(hands[i1], nie) > 0 and iou(hands[i2], bo) > 0:
                        return True
                    elif iou(hands[i2], nie) > 0 and iou(hands[i1], bo) > 0:
                        return True
            return False

        def j_top2():
            if not ("手" in self.d["top"].keys()):
                return False
            if not ("菠菜叶_顶视" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            if len(hands) < 2:
                return False

            bos = self.d["top"]["菠菜叶_顶视"]
            for bo in bos:
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    return True
            return False

        def j_front2():
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("菠菜叶_前视" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            if len(hands) < 2:
                return False
            bos = self.d["front"]["菠菜叶_前视"]
            for bo in bos:
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    return True
            return False

        if j_top() or j_top2():
            return True, "top"
        elif j_front() or j_front2():
            return True, "front"
        if ("手" in self.d["top"].keys()) and ("镊子" in self.d["top"].keys(
        )) and ("载玻片" in self.d["top"].keys()):
            hands = sorted(self.d["top"]["手"], key=lambda x: -x[4])
            if len(hands) > 1:
                zais = self.d["top"]["载玻片"]
                nies = self.d["top"]["镊子"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
        if "手" in self.d["top"].keys():
            if "操作" in self.d["top"].keys():
                if self.is_get_bo:
                    self.next_ok = True
        if "手" in self.d["front"].keys():
            if "操作" in self.d["front"].keys():
                if self.is_get_bo:
                    self.next_ok = True
        if "手" in self.d["side"].keys():
            if "操作" in self.d["side"].keys():
                if self.is_get_bo:
                    self.next_ok = True

        return False, None

    # DONE
    def j6(self):
        def j_top():
            # 4. 把撕下的表皮放置在载玻片中央并用镊子展平

            if not ("手" in self.d["top"].keys()):
                return False
            if ("操作" in self.d["top"].keys()):
                return True
            if not ("镊子" in self.d["top"].keys()):
                return False
            if not ("载玻片" in self.d["top"].keys()):
                return False

            hands = self.d["top"]["手"]
            if len(hands) < 2:
                return False
            nies = self.d["top"]["镊子"]
            zais = self.d["top"]["载玻片"]

            for zai in zais:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, zai) > 0:
                        nie = nie_
                        break
                if iou(nie, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, nie) > 0:
                        return True
            return False

        def j_front():
            # 4. 把撕下的表皮放置在载玻片中央并用镊子展平

            if not ("手" in self.d["front"].keys()):
                return False
            if ("操作" in self.d["front"].keys()):
                return True
            if not ("镊子" in self.d["front"].keys()):
                return False
            if not ("载玻片" in self.d["front"].keys()):
                return False

            hands = self.d["front"]["手"]
            if len(hands) < 2:
                return False
            nies = self.d["front"]["镊子"]
            zais = self.d["front"]["载玻片"]

            for zai in zais:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, zai) > 0:
                        nie = nie_
                        break
                if iou(nie, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, nie) > 0:

                        return True
            return False

        def j_side():
            # 4. 把撕下的表皮放置在载玻片中央并用镊子展平

            if not ("手" in self.d["side"].keys()):
                return False
            if ("操作" in self.d["side"].keys()):
                return True
            if not ("镊子" in self.d["side"].keys()):
                return False
            if not ("载玻片" in self.d["side"].keys()):
                return False

            hands = self.d["side"]["手"]
            if len(hands) < 2:
                return False
            nies = self.d["side"]["镊子"]
            zais = self.d["side"]["载玻片"]

            for zai in zais:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, zai) > 0:
                        nie = nie_
                        break
                if iou(nie, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, nie) > 0:

                        return True
            return False

        if j_top():
            if "操作" in self.d["top"].keys():
                return True, "top", self.d["top"]["操作"][0][4]
            return True, "top", 0.
        if j_front():
            if "操作" in self.d["front"].keys():
                return True, "front", self.d["front"]["操作"][0][4]
            return True, "front", 0.
        if j_side():
            if "操作" in self.d["side"].keys():
                return True, "side", self.d["side"]["操作"][0][4]
            return True, "side", 0.

        return False, None, 0.

    # DONE
    def j7(self):
        if not self.pre_ok:
            if self.exp_ok[5] != -1:

                def t_front():
                    if "操作" in self.d["front"].keys():
                        return True
                    if ("手" in self.d["front"].keys()) and \
                            ("镊子" in self.d["front"].keys()) and \
                            ("载玻片" in self.d["front"].keys()):

                        hands = self.d["front"]["手"]
                        nies = self.d["front"]["镊子"]
                        zais = self.d["front"]["载玻片"]
                        for zai in zais:
                            nie = nies[0]
                            for nie_ in nies:
                                if iou(zai, nie_) > 0:
                                    nie = nie_
                                    break
                            is_ok = False
                            for hand in hands:
                                if iou(hand, nie) > 0:
                                    is_ok = True
                                    break
                            if is_ok and iou(nie, zai) == 0:
                                return True
                    return False

                def t_top():
                    if "操作" in self.d["top"].keys():
                        return True
                    if ("手" in self.d["top"].keys()) and ( \
                            "镊子" in self.d["top"].keys()) and ( \
                                "载玻片" in self.d["top"].keys()):

                        hands = self.d["top"]["手"]
                        nies = self.d["top"]["镊子"]
                        zais = self.d["top"]["载玻片"]
                        for zai in zais:
                            nie = nies[0]
                            for nie_ in nies:
                                if iou(zai, nie_) > 0:
                                    nie = nie_
                                    break
                            is_ok = False
                            for hand in hands:
                                if iou(hand, nie) > 0:
                                    is_ok = True
                                    break
                            if is_ok and iou(nie, zai) == 0:
                                return True
                    return False

                def t_side():
                    if "操作" in self.d["side"].keys():
                        return True
                    if ("手" in self.d["side"].keys()) and ( \
                            "镊子" in self.d["side"].keys()) and ( \
                                "载玻片" in self.d["side"].keys()):

                        hands = self.d["side"]["手"]
                        nies = self.d["side"]["镊子"]
                        zais = self.d["side"]["载玻片"]
                        for zai in zais:
                            nie = nies[0]
                            for nie_ in nies:
                                if iou(zai, nie_) > 0:
                                    nie = nie_
                                    break
                            is_ok = False
                            for hand in hands:
                                if iou(hand, nie) > 0:
                                    is_ok = True
                                    break
                            if is_ok and iou(nie, zai) == 0:
                                return True
                    return False

                if t_front() or t_top() or t_side():
                    self.pre_ok = True
                    self.pre_ok_id = self.frame_id
        # 至少上一个得分点完成2s之后，才进行该得分点的判断
        if self.frame_id - self.pre_ok_id > 10:

            def j_top():
                if ("操作" in self.d["top"].keys()):
                    return True
                if not ("手" in self.d["top"].keys()):
                    return False
                if not ("镊子" in self.d["top"].keys()):
                    return False
                if not ("载玻片" in self.d["top"].keys()):
                    return False

                hands = self.d["top"]["手"]
                if len(hands) < 2:
                    return False
                nies = self.d["top"]["镊子"]
                zais = self.d["top"]["载玻片"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break

                    is_ok = False
                    if iou(nie, zai) == 0:
                        return False
                    for hand in hands:
                        if iou(hand, nie) > 0:
                            is_ok = True
                    if not is_ok:
                        return False
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
                        x_left = 0.5 * (hands[i1][0] + hands[i1][2])
                        x_right = 0.5 * (hands[i2][0] + hands[i2][2])
                        x_zai = 0.5 * (zai[0] + zai[2])
                        if (x_zai - x_left) * (x_right - x_zai) > 0:
                            return True
                return False

            def j_front():
                if ("操作" in self.d["front"].keys()):
                    return True
                if not ("手" in self.d["front"].keys()):
                    return False
                if not ("镊子" in self.d["front"].keys()):
                    return False
                if not ("载玻片" in self.d["front"].keys()):
                    return False

                hands = self.d["front"]["手"]
                if len(hands) < 2:
                    return False
                nies = self.d["top"]["镊子"]
                zais = self.d["top"]["载玻片"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break

                    is_ok = False
                    if iou(nie, zai) == 0:
                        return False
                    for hand in hands:
                        if iou(hand, nie) > 0:
                            is_ok = True
                    if not is_ok:
                        return False
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
                        x_left = 0.5 * (hands[i1][0] + hands[i1][2])
                        x_right = 0.5 * (hands[i2][0] + hands[i2][2])
                        x_zai = 0.5 * (zai[0] + zai[2])
                        if (x_zai - x_left) * (x_right - x_zai) > 0:
                            return True
                return False

            def j_side():
                if ("操作" in self.d["side"].keys()):
                    return True
                if not ("手" in self.d["side"].keys()):
                    return False
                if not ("镊子" in self.d["side"].keys()):
                    return False
                if not ("载玻片" in self.d["side"].keys()):
                    return False

                hands = self.d["side"]["手"]
                if len(hands) < 2:
                    return False
                nies = self.d["top"]["镊子"]
                zais = self.d["top"]["载玻片"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break

                    is_ok = False
                    if iou(nie, zai) == 0:
                        return False
                    for hand in hands:
                        if iou(hand, nie) > 0:
                            is_ok = True
                    if not is_ok:
                        return False
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
                        x_left = 0.5 * (hands[i1][1] + hands[i1][3])
                        x_right = 0.5 * (hands[i2][1] + hands[i2][3])
                        x_zai = 0.5 * (zai[1] + zai[3])
                        if (x_zai - x_left) * (x_right - x_zai) > 0:
                            return True
                return False

            if j_top():
                self.okr += 1
                if self.okr == 5:
                    return True, "top"
            elif j_front():
                self.okr += 1
                if self.okr == 5:
                    return True, "front"
            elif j_side():
                self.okr += 1
                if self.okr == 5:
                    return True, "side"
            return False, None
        else:
            self.okr = 0
            return False, None
        self.okr = 0
        return False, None

    def j9(self):
        def j_top():
            # 6. 将制作好的装片放入废液缸中

            if not ("手" in self.d["top"].keys()):
                return False
            if not ("废料缸" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            fei = self.d["top"]["废料缸"][0]
            if ("载玻片" in self.d["top"].keys()):
                zai = self.d["top"]["载玻片"][0]
                is_ok = False
                if iou(fei, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, fei) > 0:
                        is_ok = True
                return is_ok

            for hand in hands:
                if fei[0] <= hand[0] <= hand[2] <= fei[2]:
                    if fei[1] <= hand[1] <= hand[3] <= fei[3]:
                        return True
            return False

        def j_front():
            # 6. 将制作好的装片放入废液缸中

            if not ("手" in self.d["front"].keys()):
                return False
            if not ("废料缸" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            fei = self.d["front"]["废料缸"][0]
            if ("载玻片" in self.d["front"].keys()):
                zai = self.d["front"]["载玻片"][0]
                is_ok = False
                if iou(fei, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, fei) > 0:
                        is_ok = True
                return is_ok

            for hand in hands:
                if fei[0] <= hand[0] <= hand[2] <= fei[2]:
                    if fei[1] <= hand[1] <= hand[3] <= fei[3]:
                        return True
            return False

        def j_side():
            # 6. 将制作好的装片放入废液缸中

            if not ("手" in self.d["side"].keys()):
                return False
            if not ("废料缸" in self.d["side"].keys()):
                return False
            hands = self.d["side"]["手"]
            fei = self.d["side"]["废料缸"][0]
            if ("载玻片" in self.d["side"].keys()):
                zai = self.d["side"]["载玻片"][0]
                is_ok = False
                if iou(fei, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, fei) > 0:
                        is_ok = True
                return is_ok

            for hand in hands:
                if fei[0] <= hand[0] <= hand[2] <= fei[2]:
                    if fei[1] <= hand[1] <= hand[3] <= fei[3]:
                        return True
            return False

        if self.is_put == False:
            if j_top():
                self.is_put = True
            elif j_front():
                self.is_put = True
            elif j_side():
                self.is_put = True
            elif self.has_score() and self.frame_id > 1500 and self.j9_2()[0]:
                self.is_put = True
            return self.j9_2()
        else:
            return self.j9_2()

    def j9_2(self):
        # 7、整理桌面
        # 二代
        for key, vals in self.d["top"].items():
            if key == "手":
                continue
            val = vals[0]
            if iou(self.desktop_area, val) > 0:
                return False, 1.0
        return True, 0.


class BIO_make_leaf_yc(ConfigModel):
    def __init__(self):
        super(BIO_make_leaf_yc, self).__init__()
        self.initScore()

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

    def post_retrace(self, index, *args, **kwargs):
        self.exp_ok[index - 1] = -1

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 10
        self.iou_ = 100.0
        self.width, self.height = 1920, 1080
        self.pre_ok = False
        self.pre_ok_id = -1
        self.is_get_bo = False
        self.next_ok = False
        self.is_put = False
        self.iou1 = 0.
        self.okr = 0
        self.dis = []
        self.is_first = False
        self.has_clue = False
        self.max_score_di = 0.
        self.max_score_ca = 0.
        self.max_score_op = 0.
        self.max_score_xi = 0.
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

    def exp_filter(self, d_front, d_top, d_side):
        d = {"front": {}, "top": {}, "side": {}}
        for key, vals in d_top.items():
            d["top"][key] = sorted(vals, key=lambda x: -x[4])
        for key, vals in d_front.items():
            d["front"][key] = sorted(vals, key=lambda x: -x[4])
        for key, vals in d_side.items():
            d["side"][key] = sorted(vals, key=lambda x: -x[4])
        return d

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
        if pred_side != None:
            if pred_side.shape[0]:
                for i in range(0, 4, 2):
                    pred_side[:, 0 + i] = torch.clamp(pred_side[:, 0 + i], 0,
                                                      1920)
                    pred_side[:, 1 + i] = torch.clamp(pred_side[:, 1 + i], 0,
                                                      1080)
            self.preds_side, self.objects_side = self.assign_labels(
                frame_side, pred_side, names_label)
            side_true = True

        if top_true and front_true and side_true:
            if self.width == 0:
                self.width, self.height = frame_top.shape[1], frame_top.shape[
                    0]

            self.rtmp_push_fun(
                top_img=frame_top,
                front_img=frame_front,
                side_img=frame_side,
                top_preds=self.preds_top,
                front_preds=self.preds_front,
                side_preds=self.preds_side)

            d_front = dict()
            d_top = dict()
            d_side = dict()

            def assign_score_fun(index, view):
                self.assignScore(
                    index=index,
                    img=eval(f"self.frame_{view}"),
                    object=eval(f"self.objects_{view}"),
                    conf=0.1,
                    time_frame=eval(f"self.time_{view}"),
                    num_frame=eval(f"self.num_frame_{view}"),
                    name_save=f"{index}.jpg",
                    preds=eval(f"self.preds_{view}"))

            for label, boxes in zip(self.labels, self.preds_front):
                if boxes.size(0) > 0:
                    d_front[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_top):
                if boxes.size(0) > 0:
                    d_top[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_side):
                if boxes.size(0) > 0:
                    d_side[label] = boxes.cpu().numpy()
            self.d = self.exp_filter(d_front, d_top, d_side)
            if DEBUG_:
                show_front = copy.copy(self.frame_front)
                show_top = copy.copy(self.frame_top)
                show_side = copy.copy(self.frame_side)

                self.plot(self.preds_front, show_front)
                self.plot(self.preds_top, show_top)
                self.plot(self.preds_side, show_side)
                tl = tuple(self.desktop_area[:2])
                br = tuple(self.desktop_area[2:])
                cv2.rectangle(show_top, tl, br, (0, 255, 255), 2)
                cv2.imshow("front_img0", cv2.resize(show_front, (960, 540)))
                cv2.imshow("top_img0", cv2.resize(show_top, (960, 540)))
                cv2.imshow("side_img0", cv2.resize(show_side, (960, 540)))

                cv2.waitKey(1)
            self.frame_id += 1
            # 2. 选叶片下表皮
            if -1 == self.exp_ok[1]:
                ret, view = self.j2()
                if ret:
                    self.exp_ok[1] = self.frame_id
                    assign_score_fun(2, view)
                    return
            # 3. 用洁净的纱布擦拭载玻片和盖玻片
            ret, view, score = self.j3()
            if ret:
                if score > self.max_score_ca:
                    self.max_score_ca = score
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, view)
                    return

            # 4. 在载玻片中央滴加清水
            ret, view, score = self.j4()
            if ret:
                if score > self.max_score_di:
                    self.max_score_di = score
                    self.exp_ok[3] = self.frame_id
                    self.exp_ok[0] = self.frame_id
                    assign_score_fun(4, view)
                    assign_score_fun(1, view)
                    return

            # 5. 撕下一小块叶片下表皮
            if -1 == self.exp_ok[4]:
                ret, view = self.j5()
                if ret:
                    self.exp_ok[4] = self.frame_id
                    assign_score_fun(5, view)
                    return

            # 6. 将叶表皮置于载玻片的水滴中, 并用镊子展平
            # 7. 用镊子夹起盖玻片, 使它的一边先接触水滴, 再缓缓放下
            if (-1 != self.exp_ok[4] or -1 != self.exp_ok[3]):
                ret, view, score = self.j6()
                if ret:
                    if score > self.max_score_op:
                        self.max_score_op = score
                        self.exp_ok[5] = self.frame_id
                        assign_score_fun(6, view)
                        for view_ in ["top", "front", "side"]:
                            if view_ != view:
                                self.exp_ok[6] = self.frame_id
                                assign_score_fun(7, view_)
                                break
                        return
            # 8. 吸水
            ret, view, score = self.j8()
            if ret:
                if score > self.max_score_xi:
                    self.max_score_xi = score
                    self.exp_ok[7] = self.frame_id
                    assign_score_fun(8, view)
                    return
            # 9. 实验结束, 将临时装片直接放入回收烧杯, 整理并清洁桌面
            if self.frame_id > 1500 and self.has_score():
                ret, iou_ = self.j9()
                if ret:
                    if iou_ <= self.iou_:
                        self.iou_ = iou_
                        self.exp_ok[8] = self.frame_id
                        assign_score_fun(9, "top")
                        return

    def j2(self):
        if self.exp_ok[4] != -1 and self.frame_id - self.exp_ok[4] > 5:
            return True, "side"
        return False, None

    def j3(self):
        # 擦拭载玻片和盖玻片
        def j_top():
            if not ("手" in self.d["top"].keys()):
                return False
            if not ("擦拭载玻片" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            ca = self.d["top"]["擦拭载玻片"][0]
            for hand in hands:
                if iou(ca, hand) > 0:
                    return True

            return False

        def j_front():
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("擦拭载玻片" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            ca = self.d["front"]["擦拭载玻片"][0]
            for hand in hands:
                if iou(ca, hand) > 0:
                    return True
            return False

        def j_side():
            if not ("手" in self.d["side"].keys()):
                return False
            if not ("擦拭载玻片" in self.d["side"].keys()):
                return False
            hands = self.d["side"]["手"]
            ca = self.d["side"]["擦拭载玻片"][0]
            for hand in hands:
                if iou(ca, hand) > 0:
                    return True
            return False

        if j_top():
            return True, "top", self.d["top"]["擦拭载玻片"][0][4]
        elif j_front():
            return True, "front", self.d["front"]["擦拭载玻片"][0][4]
        elif j_side():
            return True, "side", self.d["side"]["擦拭载玻片"][0][4]
        return False, None, 0.

    # DONE
    def j4(self):
        # 用滴管在载玻片中央滴一滴清水
        def j_top():
            if ("滴清水" in self.d["top"].keys()):
                return True
            if not ("手" in self.d["top"].keys()):
                return False
            if not ("载玻片" in self.d["top"].keys()):
                return False
            if not ("滴瓶_清水_取用" in self.d["top"].keys()):
                if not ("滴瓶_清水_取用" in self.d["front"].keys()):
                    if not ("滴瓶_清水_取用" in self.d["side"].keys()):
                        return False
            hands = self.d["top"]["手"]
            zai = self.d["top"]["载玻片"][0]
            for hand in hands:
                if iou(hand, zai) > 0:
                    return True
            return False

        def j_front():
            if ("滴清水" in self.d["front"].keys()):
                return True
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("载玻片" in self.d["front"].keys()):
                return False
            if not ("滴瓶_清水_取用" in self.d["top"].keys()):
                if not ("滴瓶_清水_取用" in self.d["front"].keys()):
                    if not ("滴瓶_清水_取用" in self.d["side"].keys()):
                        return False
            hands = self.d["front"]["手"]
            zai = self.d["front"]["载玻片"][0]
            for hand in hands:
                if hand[1] + hand[3] < zai[1] + zai[3]:
                    return True
            return False

        def j_side():
            if ("滴清水" in self.d["side"].keys()):
                return True
            if not ("手" in self.d["side"].keys()):
                return False
            if not ("载玻片" in self.d["side"].keys()):
                return False
            if not ("滴瓶_清水_取用" in self.d["top"].keys()):
                if not ("滴瓶_清水_取用" in self.d["front"].keys()):
                    if not ("滴瓶_清水_取用" in self.d["side"].keys()):
                        return False
            hands = self.d["side"]["手"]
            zai = self.d["side"]["载玻片"][0]
            for hand in hands:
                if iou(hand, zai) > 0:
                    return True
            return False

        # if j_top():
        #     if "滴清水" in self.d["top"].keys():
        #         return True, "top", self.d["top"]["滴清水"][0][4]
        #     return True, "top", 0.
        if j_front():
            if "滴清水" in self.d["front"].keys():
                return True, "front", self.d["front"]["滴清水"][0][4]
            return True, "front", 0.
        elif j_side():
            if "滴清水" in self.d["side"].keys():
                return True, "side", self.d["side"]["滴清水"][0][4]
            return True, "side", 0.
        return False, None, 0.

    # DONE
    def j5(self):
        if self.next_ok:
            return True, "top"

        def j_top():
            # . 用镊子撕取菠菜叶下表皮
            if not ("手" in self.d["top"].keys()):
                return False
            if not ("镊子" in self.d["top"].keys()):
                return False
            if not ("菠菜叶_顶视" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            if len(hands) < 2:
                return False
            bos = self.d["top"]["菠菜叶_顶视"]
            nies = self.d["top"]["镊子"]
            for bo in bos:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, bo) > 0:
                        nie = nie_
                        break
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    if iou(nie, bo) == 0:
                        return False
                    if iou(hands[i1], nie) > 0 and iou(hands[i2], bo) > 0:
                        return True
                    elif iou(hands[i2], nie) > 0 and iou(hands[i1], bo) > 0:
                        return True
            return False

        def j_front():
            # 3. 用镊子撕取菠菜叶下表皮
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("镊子" in self.d["front"].keys()):
                return False
            if not ("菠菜叶_前视" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            if len(hands) < 2:
                return False
            bos = self.d["front"]["菠菜叶_前视"]
            nies = self.d["front"]["镊子"]
            for bo in bos:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, bo) > 0:
                        nie = nie_
                        break
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    if iou(nie, bo) == 0:
                        return False
                    if iou(hands[i1], nie) > 0 and iou(hands[i2], bo) > 0:
                        return True
                    elif iou(hands[i2], nie) > 0 and iou(hands[i1], bo) > 0:
                        return True
            return False

        def j_top2():
            if not ("手" in self.d["top"].keys()):
                return False
            if not ("菠菜叶_顶视" in self.d["top"].keys()):
                return False
            hands = self.d["top"]["手"]
            if len(hands) < 2:
                return False

            bos = self.d["top"]["菠菜叶_顶视"]
            for bo in bos:
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    return True
            return False

        def j_front2():
            if not ("手" in self.d["front"].keys()):
                return False
            if not ("菠菜叶_前视" in self.d["front"].keys()):
                return False
            hands = self.d["front"]["手"]
            if len(hands) < 2:
                return False
            bos = self.d["front"]["菠菜叶_前视"]
            for bo in bos:
                i1 = -1
                i2 = -1
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        i1 = i
                        break
                for i in range(len(hands)):
                    if iou(hands[i], bo) > 0:
                        if i != i1:
                            i2 = i
                            break
                if i1 != -1 and i2 != -1 and i1 != i2:
                    self.is_get_bo = True
                    return True
            return False

        if j_top() or j_top2():
            return True, "top"
        elif j_front() or j_front2():
            return True, "front"
        if ("手" in self.d["top"].keys()) and ("镊子" in self.d["top"].keys(
        )) and ("载玻片" in self.d["top"].keys()):
            hands = sorted(self.d["top"]["手"], key=lambda x: -x[4])
            if len(hands) > 1:
                zais = self.d["top"]["载玻片"]
                nies = self.d["top"]["镊子"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
        if "手" in self.d["top"].keys():
            if "操作" in self.d["top"].keys():
                if self.is_get_bo:
                    self.next_ok = True
        if "手" in self.d["front"].keys():
            if "操作" in self.d["front"].keys():
                if self.is_get_bo:
                    self.next_ok = True
        if "手" in self.d["side"].keys():
            if "操作" in self.d["side"].keys():
                if self.is_get_bo:
                    self.next_ok = True

        return False, None

    # DONE
    def j6(self):
        def j_top():
            # 4. 把撕下的表皮放置在载玻片中央并用镊子展平

            if not ("手" in self.d["top"].keys()):
                return False
            if ("操作" in self.d["top"].keys()):
                return True
            if not ("镊子" in self.d["top"].keys()):
                return False
            if not ("载玻片" in self.d["top"].keys()):
                return False

            hands = self.d["top"]["手"]
            if len(hands) < 2:
                return False
            nies = self.d["top"]["镊子"]
            zais = self.d["top"]["载玻片"]

            for zai in zais:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, zai) > 0:
                        nie = nie_
                        break
                if iou(nie, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, nie) > 0:
                        return True
            return False

        def j_front():
            # 4. 把撕下的表皮放置在载玻片中央并用镊子展平

            if not ("手" in self.d["front"].keys()):
                return False
            if ("操作" in self.d["front"].keys()):
                return True
            if not ("镊子" in self.d["front"].keys()):
                return False
            if not ("载玻片" in self.d["front"].keys()):
                return False

            hands = self.d["front"]["手"]
            if len(hands) < 2:
                return False
            nies = self.d["front"]["镊子"]
            zais = self.d["front"]["载玻片"]

            for zai in zais:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, zai) > 0:
                        nie = nie_
                        break
                if iou(nie, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, nie) > 0:

                        return True
            return False

        def j_side():
            # 4. 把撕下的表皮放置在载玻片中央并用镊子展平

            if not ("手" in self.d["side"].keys()):
                return False
            if ("操作" in self.d["side"].keys()):
                return True
            if not ("镊子" in self.d["side"].keys()):
                return False
            if not ("载玻片" in self.d["side"].keys()):
                return False

            hands = self.d["side"]["手"]
            if len(hands) < 2:
                return False
            nies = self.d["side"]["镊子"]
            zais = self.d["side"]["载玻片"]

            for zai in zais:
                nie = nies[0]
                for nie_ in nies:
                    if iou(nie_, zai) > 0:
                        nie = nie_
                        break
                if iou(nie, zai) == 0:
                    return False
                for hand in hands:
                    if iou(hand, nie) > 0:

                        return True
            return False

        if j_top():
            if "操作" in self.d["top"].keys():
                return True, "top", self.d["top"]["操作"][0][4]
            return True, "top", 0.
        if j_front():
            if "操作" in self.d["front"].keys():
                return True, "front", self.d["front"]["操作"][0][4]
            return True, "front", 0.
        if j_side():
            if "操作" in self.d["side"].keys():
                return True, "side", self.d["side"]["操作"][0][4]
            return True, "side", 0.

        return False, None, 0.

    # DONE
    def j7(self):
        if not self.pre_ok:
            if self.exp_ok[5] != -1:

                def t_front():
                    if "操作" in self.d["front"].keys():
                        return True
                    if ("手" in self.d["front"].keys()) and \
                            ("镊子" in self.d["front"].keys()) and \
                            ("载玻片" in self.d["front"].keys()):

                        hands = self.d["front"]["手"]
                        nies = self.d["front"]["镊子"]
                        zais = self.d["front"]["载玻片"]
                        for zai in zais:
                            nie = nies[0]
                            for nie_ in nies:
                                if iou(zai, nie_) > 0:
                                    nie = nie_
                                    break
                            is_ok = False
                            for hand in hands:
                                if iou(hand, nie) > 0:
                                    is_ok = True
                                    break
                            if is_ok and iou(nie, zai) == 0:
                                return True
                    return False

                def t_top():
                    if "操作" in self.d["top"].keys():
                        return True
                    if ("手" in self.d["top"].keys()) and ( \
                            "镊子" in self.d["top"].keys()) and ( \
                                "载玻片" in self.d["top"].keys()):

                        hands = self.d["top"]["手"]
                        nies = self.d["top"]["镊子"]
                        zais = self.d["top"]["载玻片"]
                        for zai in zais:
                            nie = nies[0]
                            for nie_ in nies:
                                if iou(zai, nie_) > 0:
                                    nie = nie_
                                    break
                            is_ok = False
                            for hand in hands:
                                if iou(hand, nie) > 0:
                                    is_ok = True
                                    break
                            if is_ok and iou(nie, zai) == 0:
                                return True
                    return False

                def t_side():
                    if "操作" in self.d["side"].keys():
                        return True
                    if ("手" in self.d["side"].keys()) and ( \
                            "镊子" in self.d["side"].keys()) and ( \
                                "载玻片" in self.d["side"].keys()):

                        hands = self.d["side"]["手"]
                        nies = self.d["side"]["镊子"]
                        zais = self.d["side"]["载玻片"]
                        for zai in zais:
                            nie = nies[0]
                            for nie_ in nies:
                                if iou(zai, nie_) > 0:
                                    nie = nie_
                                    break
                            is_ok = False
                            for hand in hands:
                                if iou(hand, nie) > 0:
                                    is_ok = True
                                    break
                            if is_ok and iou(nie, zai) == 0:
                                return True
                    return False

                if t_front() or t_top() or t_side():
                    self.pre_ok = True
                    self.pre_ok_id = self.frame_id
        # 至少上一个得分点完成2s之后，才进行该得分点的判断
        if self.frame_id - self.pre_ok_id > 10:

            def j_top():
                if ("操作" in self.d["top"].keys()):
                    return True
                if not ("手" in self.d["top"].keys()):
                    return False
                if not ("镊子" in self.d["top"].keys()):
                    return False
                if not ("载玻片" in self.d["top"].keys()):
                    return False

                hands = self.d["top"]["手"]
                if len(hands) < 2:
                    return False
                nies = self.d["top"]["镊子"]
                zais = self.d["top"]["载玻片"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break

                    is_ok = False
                    if iou(nie, zai) == 0:
                        return False
                    for hand in hands:
                        if iou(hand, nie) > 0:
                            is_ok = True
                    if not is_ok:
                        return False
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
                        x_left = 0.5 * (hands[i1][0] + hands[i1][2])
                        x_right = 0.5 * (hands[i2][0] + hands[i2][2])
                        x_zai = 0.5 * (zai[0] + zai[2])
                        if (x_zai - x_left) * (x_right - x_zai) > 0:
                            return True
                return False

            def j_front():
                if ("操作" in self.d["front"].keys()):
                    return True
                if not ("手" in self.d["front"].keys()):
                    return False
                if not ("镊子" in self.d["front"].keys()):
                    return False
                if not ("载玻片" in self.d["front"].keys()):
                    return False

                hands = self.d["front"]["手"]
                if len(hands) < 2:
                    return False
                nies = self.d["top"]["镊子"]
                zais = self.d["top"]["载玻片"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break

                    is_ok = False
                    if iou(nie, zai) == 0:
                        return False
                    for hand in hands:
                        if iou(hand, nie) > 0:
                            is_ok = True
                    if not is_ok:
                        return False
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
                        x_left = 0.5 * (hands[i1][0] + hands[i1][2])
                        x_right = 0.5 * (hands[i2][0] + hands[i2][2])
                        x_zai = 0.5 * (zai[0] + zai[2])
                        if (x_zai - x_left) * (x_right - x_zai) > 0:
                            return True
                return False

            def j_side():
                if ("操作" in self.d["side"].keys()):
                    return True
                if not ("手" in self.d["side"].keys()):
                    return False
                if not ("镊子" in self.d["side"].keys()):
                    return False
                if not ("载玻片" in self.d["side"].keys()):
                    return False

                hands = self.d["side"]["手"]
                if len(hands) < 2:
                    return False
                nies = self.d["top"]["镊子"]
                zais = self.d["top"]["载玻片"]
                for zai in zais:
                    nie = nies[0]
                    for nie_ in nies:
                        if iou(nie_, zai) > 0:
                            nie = nie_
                            break

                    is_ok = False
                    if iou(nie, zai) == 0:
                        return False
                    for hand in hands:
                        if iou(hand, nie) > 0:
                            is_ok = True
                    if not is_ok:
                        return False
                    i1 = -1
                    i2 = -1
                    for i in range(len(hands)):
                        if iou(hands[i], zai) > 0:
                            i1 = i
                            break
                    for i in range(len(hands)):
                        if iou(hands[i], nie) > 0:
                            if i != i1:
                                i2 = i
                                break
                    if i1 != -1 and i2 != -1 and i1 != i2:
                        if iou(hands[i1], zai) > 0 and iou(
                                hands[i2], nie) > 0 and iou(nie, zai) > 0:
                            if self.is_get_bo:
                                self.next_ok = True
                                break
                        x_left = 0.5 * (hands[i1][1] + hands[i1][3])
                        x_right = 0.5 * (hands[i2][1] + hands[i2][3])
                        x_zai = 0.5 * (zai[1] + zai[3])
                        if (x_zai - x_left) * (x_right - x_zai) > 0:
                            return True
                return False

            if j_top():
                self.okr += 1
                if self.okr == 5:
                    return True, "top"
            elif j_front():
                self.okr += 1
                if self.okr == 5:
                    return True, "front"
            elif j_side():
                self.okr += 1
                if self.okr == 5:
                    return True, "side"
            return False, None
        else:
            self.okr = 0
            return False, None
        self.okr = 0
        return False, None

    def j8(self):
        def j_top():
            if "吸水" in self.d["top"].keys():
                return True

        def j_front():
            if "吸水" in self.d["front"].keys():
                return True

        def j_side():
            if "吸水" in self.d["side"].keys():
                return True

        if j_top():
            return True, "top", self.d["top"]["吸水"][0][4]
        if j_front():
            return True, "front", self.d["front"]["吸水"][0][4]
        if j_side():
            return True, "side", self.d["side"]["吸水"][0][4]
        return False, None, 0.

    def j9(self):
        # 9、整理桌面
        for key, vals in self.d["top"].items():
            if key == "手":
                continue
            val = vals[0]
            if iou(self.desktop_area, val) > 0:
                return False, 1.0
        return True, 0.
