from PIL import Image
from logger import logger
from .comm import *
from .comm.course_base import ConfigModel
import copy

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


class PHY_induced_current_2(ConfigModel):
    def __init__(self):
        super(PHY_induced_current_2, self).__init__()
        self.initScore()

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 8
        self.pos_top = []
        self.pos_front = []
        self.moving_front = []
        self.moving_top = []
        self.count = []
        self.width, self.height = 0, 0
        self.is_first = None
        self.iou_ = 100.0
    def exp_filter(self, d_front, d_top):
        d = {"front": {}, "top": {}}
        if "开关闭合_前视" in d_front.keys() and "开关断开_前视" in d_front.keys():
            s_on = d_front["开关闭合_前视"][0]
            s_off = d_front["开关断开_前视"][0]
            res = "off"
            if s_on[4] > s_off[4]:
                res = "on"
            for key, vals in d_front.items():
                if res == "on":
                    if key == "开关断开_前视":
                        continue
                else:
                    if key == "开关闭合_前视":
                        continue
                d["front"][key] = vals
        else:
            d["front"] = d_front

        if "开关闭合_顶视" in d_top.keys() and "开关断开_顶视" in d_top.keys():
            s_on = d_top["开关闭合_顶视"][0]
            s_off = d_top["开关断开_顶视"][0]
            res = "off"
            if s_on[4] > s_off[4]:
                res = "on"
            for key, vals in d_top.items():
                if res == "on":
                    if key == "开关断开_顶视":
                        continue
                else:
                    if key == "开关闭合_顶视":
                        continue
                d["top"][key] = vals
        else:
            d["top"] = d_top
        # 前视和顶视冲突 - 相信顶视
        if "开关闭合_前视" in d["front"].keys() and "开关断开_顶视" in d["top"].keys():
            d["front"]["开关断开_前视"] = d["front"]["开关闭合_前视"]
            del d["front"]["开关闭合_前视"]
        if "开关断开_前视" in d["front"].keys() and "开关闭合_顶视" in d["top"].keys():
            d["front"]["开关闭合_前视"] = d["front"]["开关断开_前视"]
            del d["front"]["开关断开_前视"]
        if "连接完成_顶视" in d["top"].keys():
            flag = False
            for key, vals in d["top"].items():
                if key == "连接完成_顶视":
                    continue
                val = vals[0]
                if iou(val, d["top"]["连接完成_顶视"][0]) == 0:
                    flag = True
                    break
            if flag:
                del d["top"]["连接完成_顶视"]
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
            if self.width == 0:
                self.width, self.height = frame_top.shape[1], frame_top.shape[0]
            
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
                    if "前视" in label:
                        d_front[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_top):
                if boxes.size(0) > 0:
                    if "顶视" in label:
                        d_top[label] = boxes.cpu().numpy()
            self.d = self.exp_filter(d_front, d_top)
            if DEBUG_:
                show_front = copy.copy(self.frame_front)
                show_top = copy.copy(self.frame_top)
                self.plot(self.preds_front, show_front)
                self.plot(self.preds_top, show_top)
               
                cv2.rectangle(show_top, 
                    (self.width//4, int(self.height * 0.55)), 
                    (3*self.width//4, self.height), (0,255,255),2)
                cv2.imshow("front_img0", cv2.resize(show_front, (960,540)))
                cv2.imshow("top_img0", cv2.resize(show_top, (960,540)))
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
            # 1. 将金属导体（线圈框）两端用细线系住后吊在铁架台上
            if -1 == self.exp_ok[0]:
                ret, view = self.j1()
                if ret:
                    if DEBUG_:
                        print("exp ok 1")
                    self.exp_ok[0] = self.frame_id
                    if view == "front":
                        assign_score_fun(1, "front")

                    else:
                        assign_score_fun(1, "top")

                    return
            # 2. 将蹄形磁铁穿过金属导体（线圈框）后放在铁架台上
            if -1 == self.exp_ok[1] and -1 != self.exp_ok[0]:
                ret, view = self.j2()
                if ret:
                    if DEBUG_:
                        print("exp ok 2")
                    self.exp_ok[1] = self.frame_id
                    if view == "front":
                        assign_score_fun(2, "front")
                    else:
                        assign_score_fun(2, "top")
                    return
            # 3. 连接电路，连接过程中开关处于断开状态
            if -1 == self.exp_ok[2] and -1 != self.exp_ok[0]:
                if self.j3():
                    if DEBUG_:
                        print("exp ok 3")
                    self.exp_ok[2] = self.frame_id
                    assign_score_fun(3, "top")

                    return

            # 4. 用导线将灵敏电流计、金属导体（线圈框）、开关连接成电路
            if -1 == self.exp_ok[3] and -1 != self.exp_ok[0]:
                if self.j4():
                    if DEBUG_:
                        print("exp ok 4")
                    self.exp_ok[3] = self.frame_id

                    return
            # 5. 金属导体（线圈框）静止时，闭合开关观察灵敏电流计的示数
            if -1 == self.exp_ok[4] and -1 != self.exp_ok[3]:
                ret, view = self.j5()
                if ret:
                    if DEBUG_:
                        print("exp ok 5")
                    self.exp_ok[4] = self.frame_id

                    if view == "front":
                        assign_score_fun(5, "front")
                    else:
                        assign_score_fun(5, "top")

                    return
            # 6. 上下移动金属导体（线圈框一边）过程中，闭合开关观察灵敏电流计的示数
            if -1 == self.exp_ok[5] and -1 != self.exp_ok[3]:
                ret, view = self.j6()
                if ret:
                    if DEBUG_:
                        print("exp ok 6")
                    assign_score_fun(4, "top")
                    self.exp_ok[5] = self.frame_id
                    if view == "front":
                        assign_score_fun(6, "front")
                    else:
                        assign_score_fun(6, "top")
                    return
            # 7. 前后移动金属导体（线圈框一边）过程中，闭合开关使金属导体（线圈框一边）完全穿过蹄形磁铁再返回原来位置时，观察灵敏电流计的示数
            if -1 == self.exp_ok[6] and -1 != self.exp_ok[3]:
                ret, view = self.j7()
                if ret:
                    if DEBUG_:
                        print("exp ok 7")
                    self.exp_ok[6] = self.frame_id
                    if view == "front":
                        assign_score_fun(7, "front")
                    else:
                        assign_score_fun(7, "top")

                    return
            # 8. 拆除电路，整理实验器材
            if -1 != self.exp_ok[3]:
                ret, iou_ = self.j8()
                if ret:
                    if DEBUG_:
                        print("exp ok 8", iou_)
                    if iou_ <= self.iou_ :
                        self.iou_ = iou_
                        self.exp_ok[7] = self.frame_id
                        assign_score_fun(8, "top")
                        return

    # DONE

    def j1(self):
        # 1. 将金属导体（线圈框）两端用细线系住后吊在铁架台上
        def j_top():

            if not ("线圈_顶视" in self.d["top"].keys()):
                return False
            if not ("铁架台_顶视" in self.d["top"].keys()):
                return False
            coil = self.d["top"]["线圈_顶视"][0]
            platform = self.d["top"]["铁架台_顶视"][0]
            if iou(coil, platform):
                return True
            return False

        def j_front():
            if not ("线圈_前视" in self.d["front"].keys()):
                return False
            if not ("铁架台_前视" in self.d["front"].keys()):
                return False
            coil = self.d["front"]["线圈_前视"][0]
            platform = self.d["front"]["铁架台_前视"][0]
            if iou(coil, platform):
                return True
            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    # DONE
    def j2(self):
        # 2. 将蹄形磁铁穿过金属导体（线圈框）后放在铁架台上
        if not (self.j1()[0]):
            return False, None

        def j_top():
            if not ("线圈穿过磁铁_顶视" in self.d["top"].keys()):
                return False
            return True

        def j_front():
            if not ("线圈穿过磁铁_前视" in self.d["front"].keys()):
                return False
            return True

        if j_top():
            return True, "top"
        elif j_front():
            return True, "front"
        return False, None

    ## DONE ##
    def j3(self):
        # 3. 连接电路，连接过程中开关处于断开状态
        ## 器材是否都有
        if not ("电流表_顶视" in self.d["top"].keys()):
            return False
        if not ("铁架台_顶视" in self.d["top"].keys()):
            return False
        if not ("开关断开_顶视" in self.d["top"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            return False
        ## 投票连接好前100 帧内的开关断开闭合情况
        # 还没连接好
        if self.exp_ok[3] == -1:
            if ("开关闭合_顶视" in self.d["top"].keys()) or (
                    "开关闭合_前视" in self.d["front"].keys()):
                self.count += [1]
            elif ("开关断开_顶视" in self.d["top"].keys()) or (
                    "开关断开_前视" in self.d["front"].keys()):
                self.count += [0]
            if len(self.count) > 100:
                self.count = self.count[1:]
        else:
            count_on = len([c for c in self.count if c == 1])
            count_off = len(self.count) - count_on
            if count_on > count_off:
                return False
            return True
        return False

    # DONE
    def j4(self):
        # 4. 用导线将灵敏电流计、金属导体（线圈框）、开关连接成电路

        ## 器材是否都有
        if not ("电流表_顶视" in self.d["top"].keys()):
            return False
        if not ("铁架台_顶视" in self.d["top"].keys()) and not (
                "铁架台_前视" in self.d["front"].keys()):
            return False
        if not ("开关断开_顶视" in self.d["top"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            return False
        if not ("线圈_前视" in self.d["front"].keys()) and not (
                "线圈_顶视" in self.d["top"].keys()):
            return False
        if not ("铁架台_顶视" in self.d["top"].keys()):
            return False
        ## 用导线来判断
        # if "导线_顶视" in self.d["top"].keys():
        #     lines = self.d["top"]["导线_顶视"]
        #     platform = self.d["top"]["铁架台_顶视"][0]
        #     a = self.d["top"]["电流表_顶视"][0]
        #     switch = self.d["top"]["开关断开_顶视"][0] if "开关断开_顶视" in self.d[
        #         "top"].keys() else self.d["top"]["开关闭合_顶视"][0]
        #     ap = False
        #     sa = False
        #     sp = False
        #     ## 线圈和开关连接
        #     for line in lines:
        #         if iou(line, platform) and iou(line, switch):
        #             sp = True
        #             break
        #     ## 线圈和电流表连接
        #     for line in lines:
        #         if iou(line, platform) and iou(line, a):
        #             ap = True
        #             break
        #     ## 电流表和开关连接
        #     for line in lines:
        #         if iou(line, a) and iou(line, switch):
        #             sa = True
        #             break
        #     if sa and sp and ap:
        #         return True
        ## 用得分点来判断
        if "连接完成_顶视" in self.d["top"].keys():
            
            return True
        
        return False

    # DONE
    def j5(self):
        # 5. 金属导体（线圈框）静止时，闭合开关观察灵敏电流计的示数
        ## 开关必须是闭合的
        if not ("开关闭合_前视" in self.d["front"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            if DEBUG_:
                print("开关闭合")
            return False, None
        if ("开关断开_前视" in self.d["front"].keys()) or (
                "开关断开_顶视" in self.d["top"].keys()):
            if DEBUG_:
                print("开关断开")
            return False, None
        ## 器材都ok
        if not ("电流表_顶视" in self.d["top"].keys()):
            if DEBUG_:
                print("电流表")
            return False, None
        if not ("铁架台_顶视" in self.d["top"].keys()) and not (
                "铁架台_前视" in self.d["front"].keys()):
            if DEBUG_:
                print("铁架台")
            return False, None
        if not ("开关断开_顶视" in self.d["top"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            if DEBUG_:
                print("开关断开")
            return False, None
        if not ("线圈_前视" in self.d["front"].keys()) and not (
                "线圈_顶视" in self.d["top"].keys()):
     
            return False, None
        ## 前视静止判断
        def j_front():
            if "线圈_前视" in self.d["front"].keys():
                coil = self.d["front"]["线圈_前视"][0]
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.pos_front.append((x, y))
                if len(self.pos_front) > 10:
                    self.pos_front = self.pos_front[1:]
                pos_npy = np.array(self.pos_front, dtype=np.float)
                var_x = pos_npy[:, 0].var()
                var_y = pos_npy[:, 1].var()

                if var_x < 8 and var_y < 8:
                    return True
            return False

        ## 顶视静止判断
        def j_top():
            if "线圈_顶视" in self.d["top"].keys():
                coil = self.d["top"]["线圈_顶视"][0]
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.pos_top.append((x, y))
                if len(self.pos_top) > 10:
                    self.pos_top = self.pos_top[1:]
                pos_npy = np.array(self.pos_top, dtype=np.float)
                var_x = pos_npy[:, 0].var()
                var_y = pos_npy[:, 1].var()

                if var_x < 8 and var_y < 8:
                    return True
            return False

        if j_front() and j_top():
            return True, "front"
        return False, None

    # DONE
    def j6(self):
        # 6. 上下移动金属导体（线圈框一边）过程中，闭合开关观察灵敏电流计的示数
        ## 开关必须是闭合的
        if not ("开关闭合_前视" in self.d["front"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            return False, None
        if ("开关断开_前视" in self.d["front"].keys()) or (
                "开关断开_顶视" in self.d["top"].keys()):
            return False, None
        ## 器材都ok
        if not ("电流表_顶视" in self.d["top"].keys()):
            return False, None
        if not ("铁架台_顶视" in self.d["top"].keys()) and not (
                "铁架台_前视" in self.d["front"].keys()):
            return False, None
        if not ("开关断开_顶视" in self.d["top"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            return False, None
        if not ("线圈_前视" in self.d["front"].keys()) and not (
                "线圈_顶视" in self.d["top"].keys()):
            return False, None
        if not ("移动线圈_前视" in self.d["front"].keys()) and not (
                "移动线圈_顶视" in self.d["top"].keys()):
            return False, None
        ## 前视竖直速度判断
        def j_front():
            if ("线圈_前视" in self.d["front"].keys()):
                coil = self.d["front"]["线圈_前视"][0]
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.moving_front.append((x, y))
                if len(self.moving_front) > 10:
                    self.moving_front = self.moving_front[1:]
                else:
                    return False
                pos_npy = np.array(self.moving_front, dtype=np.float)

                var_y = pos_npy[:, 1].var()

                if var_y > 100:
                    return True
            return False

        ## 顶视判断其位移是否很大，位移不大则是在上下动
        def j_top():
            if "线圈_顶视" in self.d["top"].keys():
                coil = self.d["top"]["线圈_顶视"][0]
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.moving_top.append((x, y))
                if len(self.moving_top) > 10:
                    self.moving_top = self.moving_top[1:]
                else:
                    return False
                pos_npy = np.array(self.moving_top, dtype=np.float)
                var_x = pos_npy[:, 0].var()
                var_y = pos_npy[:, 1].var()
                if var_x > 100 or var_y > 100:
                    return False
                return True
            return False

        if j_front() and j_top():
            return True, "front"
        return False, None

    # DONE
    def j7(self):
        # 7. 前后移动金属导体（线圈框一边）过程中，闭合开关使金属导体（线圈框一边）完全穿过蹄形磁铁再返回原来位置时，观察灵敏电流计的示数
        ## 开关必须是闭合的
        if not ("开关闭合_前视" in self.d["front"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            return False, None
        if ("开关断开_前视" in self.d["front"].keys()) or (
                "开关断开_顶视" in self.d["top"].keys()):
            return False, None
        ## 器材都ok
        if not ("电流表_顶视" in self.d["top"].keys()):
            return False, None
        if not ("铁架台_顶视" in self.d["top"].keys()) and not (
                "铁架台_前视" in self.d["front"].keys()):
            return False, None
        if not ("开关断开_顶视" in self.d["top"].keys()) and not (
                "开关闭合_顶视" in self.d["top"].keys()):
            return False, None
        if not ("线圈_前视" in self.d["front"].keys()) and not (
                "线圈_顶视" in self.d["top"].keys()):
            return False, None
        if not ("移动线圈_前视" in self.d["front"].keys()) and not (
                "移动线圈_顶视" in self.d["top"].keys()):
            return False, None
        ## 前视水平速度判断
        def j_front():
            if ("线圈_前视" in self.d["front"].keys()):
                coil = self.d["front"]["线圈_前视"][0]
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.moving_front.append((x, y))
                if len(self.moving_front) > 10:
                    self.moving_front = self.moving_front[1:]
                else:
                    return False
                pos_npy = np.array(self.moving_front, dtype=np.float)

                var_x = pos_npy[:, 0].var()

                if var_x > 100:
                    return True
            return False

        ## 顶视判断其位移是否很大，位移大则是在水平动
        def j_top():
            if "线圈_顶视" in self.d["top"].keys():
                coil = self.d["top"]["线圈_顶视"][0]
                x = int(0.5 * coil[0] + 0.5 * coil[2])
                y = int(0.5 * coil[1] + 0.5 * coil[3])
                self.moving_top.append((x, y))
                if len(self.moving_top) > 10:
                    self.moving_top = self.moving_top[1:]
                else:
                    return False
                pos_npy = np.array(self.moving_top, dtype=np.float)
                var_x = pos_npy[:, 0].var()
                var_y = pos_npy[:, 1].var()
                if var_x > 100 or var_y > 100:
                    return True

            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    # DONE
    def j8(self):
        
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
            area = [0.25 * self.width, 0.55 * self.height, 0.75 * self.width, self.height]
            for key, vals in self.d["top"].items():
                val = vals[0]
                # if DEBUG_:
                #     print(iou(area, val))
                if iou(area, val) > 0:
                    return False, 1.0
            return True, 0.

        return False, 1.0
