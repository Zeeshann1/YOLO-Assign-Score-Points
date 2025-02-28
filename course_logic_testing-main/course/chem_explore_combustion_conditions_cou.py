from .comm import *
from .comm.course_base import ConfigModel


class CHEM_TJRSTJ(ConfigModel):
    def __init__(self):
        super(CHEM_TJRSTJ, self).__init__()
        self.re_init()

    def re_init(self):
        # 到液体
        self.pour_liquid_img = []
        self.pour_liquid_img_time = []
        self.pour_liquid_box = []
        # beifen
        self.bb_box = []
        self.pour_liquid_img_bak = []
        self.pour_liquid_img_bak_time = []
        self.pour_liquid_box_bak = []
        # 酒精灯是否燃烧
        self.burner_stop = False
        # 棉花燃烧
        self.cotton_flame_start = False
        self.cotton_not_flame_img = []
        self.cotton_not_flame_img_time = []
        self.cotton_flame_img = []
        self.cotton_flame_img_time = []
        # 熄灭酒精灯
        self.slake_burner_img = []
        self.slake_burner_img_time = []
        # 清洁桌面
        self.clear_img = []
        self.clear_img_time = []
        self.clear_bool = False
        # 保存分数
        self.save_1 = False
        self.save_2 = False
        self.save_3 = False
        self.save_4 = False
        self.save_5 = False
        self.save_6 = False
        self.not_draw_img = True

    def iou(self, predicted_bound, ground_truth_bound):
        '''
        功能：计算两个矩形的iou
        '''
        pxmin, pymin, pxmax, pymax = predicted_bound
        gxmin, gymin, gxmax, gymax = ground_truth_bound
        parea = (pxmax - pxmin) * (pymax - pymin)  # 计算P的面积
        garea = (gxmax - gxmin) * (gymax - gymin)  # 计算G的面积
        xmin = max(pxmin, gxmin)  # 得到左下顶点的横坐标
        ymin = max(pymin, gymin)  # 得到左下顶点的纵坐标
        xmax = min(pxmax, gxmax)  # 得到右上顶点的横坐标
        ymax = min(pymax, gymax)  # 得到右上顶点的纵坐标
        w = xmax - xmin
        h = ymax - ymin
        if w <= 0 or h <= 0:
            return 0
        area = w * h  # G∩P的面积
        IoU = area / (parea + garea - area)
        return IoU

    def two_iou(self, box1, box2, th):
        for i in range(len(box1)):
            for j in range(len(box2)):
                if self.iou(box1[i][:4], box2[j][:4]) > th:
                    return True
        return False

    def box_include(self, box1, box2):
        '''
        功能：判断两个矩形框是否为包含关系
        '''
        x1, y1, x2, y2 = box1[0], box1[1], box1[2], box1[3]
        x3, y3, x4, y4 = box2[0], box2[1], box2[2], box2[3]
        if x1 < x3 and y1 < y3 and x4 < x2 and y4 < y2:
            return True
        elif x3 < x1 and y3 < y1 and x2 < x4 and y2 < y4:
            return True
        else:
            return False

    def ignition(self, img, det, result_key):
        ignition_box = det['ignition'][0]
        ignition_score = det['ignition'][0][4]
        if not self.ignition_bool and ignition_score > 0.7:
            self.ignition_img.append(self.draw(img.copy(), [ignition_box], ['ignition']))
            self.ignition_img_time.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            if len(self.ignition_img) > 5:
                self.ignition_bool = True

    def pour_liquid(self, img, det, result_key):
        pour_liquid_box = det['pour_liquid'][0]
        if len(self.pour_liquid_img) < 2 and 'thin_bottle' in result_key and 'beaker' in result_key:
            beaker_box = det['beaker']
            thin_box = det['thin_bottle']
            pour_beaker_iou = self.two_iou(det['pour_liquid'], beaker_box, 0.1)  # 倒置标签与烧杯是否有交集
            pour_thin_iou = self.two_iou(det['pour_liquid'], thin_box, 0.1)  # 倒置标签与烧杯是否有交集
            thin_beaker = self.two_iou(thin_box, beaker_box, 0)  # 细口瓶与烧杯是否有交集
            if pour_beaker_iou and pour_thin_iou and thin_beaker:
                if len(self.pour_liquid_img) == 0:
                    self.pour_liquid_img.append(self.draw(img.copy(), [pour_liquid_box], ['pour_liquid']))
                    self.pour_liquid_img_time.append([self.objects_, self.time_, self.num_frame_, self.preds_])
                    self.pour_liquid_box.append(pour_liquid_box)
                    return
                elif len(self.pour_liquid_img) == 1:
                    box = self.pour_liquid_box[0]
                    if self.iou(box[:4], pour_liquid_box[:4]) < 0.3:
                        self.pour_liquid_img.append(self.draw(img.copy(), [pour_liquid_box], ['pour_liquid']))
                        self.pour_liquid_img_time.append([self.objects_, self.time_, self.num_frame_, self.preds_])
                        self.pour_liquid_box.append(pour_liquid_box)
                        return
                else:
                    return

    def pour_liquid_bak(self, img, det, result_key):
        # 1、细口瓶烧杯相交，2、细口瓶的中心点高于烧杯，3、手拿烧杯或者手拿细口瓶或者都拿
        thin_bottle_box = det['thin_bottle']
        beaker_box = det['beaker']
        hand_box = det['hand']
        assert len(thin_bottle_box) == len(beaker_box) == len(hand_box)
        for i in range(len(hand_box)):
            for j in range(len(thin_bottle_box)):
                h_t_iou = self.iou(hand_box[i][:4], thin_bottle_box[j][:4]) > 0.1
                for k in range(len(beaker_box)):
                    t_b_iou = self.iou(thin_bottle_box[j][:4], beaker_box[k][:4]) > 0
                    t_c_y = (thin_bottle_box[j][:4][1] + thin_bottle_box[j][:4][3]) / 2
                    b_c_y = (beaker_box[k][:4][1] + beaker_box[k][:4][3]) / 2
                    if h_t_iou and t_b_iou and t_c_y < b_c_y:
                        if len(self.bb_box) == 0:
                            self.bb_box.append(beaker_box[k])
                            self.pour_liquid_img_bak.append(
                                self.draw(img.copy(), [hand_box[i], thin_bottle_box[k], beaker_box[j]],
                                          ['hand_box', 'thin_bottle_box', 'beaker_box']))
                            self.pour_liquid_img_bak_time.append(
                                [self.objects_, self.time_, self.num_frame_, self.preds_])
                            self.pour_liquid_box_bak = []
                        else:
                            if len(self.pour_liquid_img_bak) < 2 and self.iou(self.bb_box[0][:4],
                                                                              beaker_box[k][:4]) < 0.6:
                                self.pour_liquid_img_bak.append(
                                    self.draw(img.copy(), [hand_box[i], thin_bottle_box[k], beaker_box[j]],
                                              ['hand_box', 'thin_bottle_box', 'beaker_box']))
                                self.pour_liquid_img_bak_time.append(
                                    [self.objects_, self.time_, self.num_frame_, self.preds_])

    def slake_burner(self, img, det, result_key):
        burner_box = det['burner'][0]
        burner_cap_box = det['burner_cap'][0]
        if burner_box[1] > burner_cap_box[1] and len(self.slake_burner_img) == 0 and self.iou(burner_box[:4],
                                                                                              burner_cap_box[:4]) > 0:
            self.slake_burner_img = self.draw(img.copy(), [burner_box, burner_cap_box], ['burner', 'burner_cap'])
            self.slake_burner_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def clear(self, img, det, result_key):
        x_c = img.shape[1] / 2
        y_c = img.shape[0] / 4 * 3
        clear_box = det['clear'][0]
        if clear_box[0] < x_c < clear_box[2]:  # and clear_box[1]<y_c<clear_box[3]:
            if not self.clear_bool:
                for key in result_key:
                    # if key == 'clear' or key == 'beaker' or key == 'thin_bottle' or key == 'hand': continue
                    if key == 'clear' or key == 'hand': continue
                    box = det[key][0][:4]
                    if self.iou(clear_box[:4], box) > 0.05:
                        self.clear_bool = True
                        break
            if not self.clear_bool and len(self.clear_img) == 0:
                self.clear_img = self.draw(img.copy(), [clear_box], ['clear'])
                self.clear_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def cotton_flame(self, img, det, result_key):
        cotton_box = det['cotton']
        flame_box = det['flame']
        clip_box = det['clip'][0]
        burner_box = det['burner'][0]
        flame_burner_iou_1 = self.iou(flame_box[0][:4], burner_box[:4]) > 0 or self.iou(flame_box[1][:4],
                                                                                        burner_box[:4]) > 0
        cotton_clip_iou_1 = (self.iou(cotton_box[0][:4], clip_box[:4]) > 0 or self.iou(cotton_box[1][:4],
                                                                                       clip_box[:4]) > 0)  # 棉花和夹子是否有交集
        if flame_box[-1][0] == 0 and flame_burner_iou_1:
            # 只有一个火焰，且和酒精灯有交集，说明棉花没有燃烧
            cotton_flame_iou_1 = self.iou(cotton_box[0][:4], flame_box[0][:4]) > 0 or self.iou(cotton_box[1][:4],
                                                                                               flame_box[0][
                                                                                               :4]) > 0  # 棉花和火焰是否有交集
            flame_flame_iou_1 = False
        elif flame_box[-1][0] != 0 and flame_burner_iou_1:
            cotton_flame_iou_1 = self.iou(cotton_box[0][:4], flame_box[0][:4]) > 0 or self.iou(cotton_box[1][:4],
                                                                                               flame_box[0][
                                                                                               :4]) > 0 or self.iou(
                cotton_box[0][:4], flame_box[1][:4]) > 0 or self.iou(cotton_box[1][:4], flame_box[1][:4]) > 0
            flame_flame_iou_1 = self.iou(flame_box[0][:4], flame_box[1][:4]) == 0
        else:
            cotton_flame_iou_1 = False
            flame_flame_iou_1 = False

        # 棉花和火焰有交集、棉花和夹子有交集
        if not self.cotton_flame_start and cotton_flame_iou_1 and flame_burner_iou_1 and cotton_clip_iou_1:
            self.cotton_flame_start = True
            return
        # 1、棉花和火焰没有交集
        # 2、夹子和棉花有交集
        if flame_box[-1][0] == 0 and len(
                self.cotton_not_flame_img) == 0 and self.cotton_flame_start and cotton_flame_iou_1 and cotton_clip_iou_1:
            self.cotton_not_flame_img = self.draw(img.copy(),
                                                  [cotton_box[0], cotton_box[1], flame_box[0], flame_box[1], clip_box],
                                                  ['cotton', 'cotton', 'flame', 'flame', 'clip'])
            self.cotton_not_flame_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            return

        if len(self.cotton_flame_img) == 0 and self.cotton_flame_start and flame_box[-1][
            0] != 0 and cotton_flame_iou_1 and flame_flame_iou_1:
            self.cotton_flame_img = self.draw(img.copy(),
                                              [cotton_box[0], cotton_box[1], flame_box[0], flame_box[1], clip_box],
                                              ['cotton', 'cotton', 'flame', 'flame', 'clip'])
            self.cotton_flame_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            return

    def draw(self, img, boxs, label):
        '''
        功能：画图，box是列表，对应的label也是一个列表
        '''
        if not self.not_draw_img:
            self.plot(self.results, img)
            return img
        assert len(boxs) == len(label)
        for i in range(len(boxs)):
            box = boxs[i]
            if box[0] == 0: continue
            cv2.rectangle(img, (int(box[0]), int(box[1])), \
                          (int(box[2]), int(box[3])), (0, 255, 255), 8)
            lab = f"{label[i]}: {box[-1]:.2f}"
            cv2.putText(img,
                        lab, (int(box[0]), int(box[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 123), 2)
        return img

    def save_score_fun(self, frame_front, preds, objects, time, num_frame, type='win'):
        # 判断是否倒置溶液
        if len(self.pour_liquid_img) > 0:
            if len(self.pour_liquid_img) == 1 and not self.save_1:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '1.jpg', self.pour_liquid_img[0])
                else:
                    self.assignScore(
                        index=1,
                        img=self.pour_liquid_img[0].copy(),
                        object=self.pour_liquid_img_time[0][0],
                        conf=0.1,
                        time_frame=self.pour_liquid_img_time[0][1],
                        num_frame=self.pour_liquid_img_time[0][2],
                        name_save="1.jpg",
                        preds=self.pour_liquid_img_time[0][3])
                # self.assignScore(1, self.pour_liquid_img[0], self.pour_liquid_img_time[0])
                self.save_1 = True
        # 酒精灯点燃时，判断到液体是否有结果
        if self.burner_stop:
            if len(self.pour_liquid_img_bak) > 0:
                if len(self.pour_liquid_img_bak) == 1 and not self.save_1:
                    if time is None and type != 'win':
                        cv2.imwrite(self.save_path + '1.jpg', self.pour_liquid_img_bak[0])
                    else:
                        self.assignScore(
                            index=1,
                            img=self.pour_liquid_img_bak[0].copy(),
                            object=self.pour_liquid_img_bak_time[0][0],
                            conf=0.1,
                            time_frame=self.pour_liquid_img_bak_time[0][1],
                            num_frame=self.pour_liquid_img_bak_time[0][2],
                            name_save="1.jpg",
                            preds=self.pour_liquid_img_bak_time[0][3])
                    # self.assignScore(1, self.pour_liquid_img_bak[0], self.pour_liquid_img_bak_time[0])
                    self.save_1 = True
        if len(self.slake_burner_img) > 0 and not self.save_5:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '4.jpg', self.slake_burner_img)
            else:
                self.assignScore(
                    index=4,
                    img=self.slake_burner_img.copy(),
                    object=self.slake_burner_img_time[0],
                    conf=0.1,
                    time_frame=self.slake_burner_img_time[1],
                    num_frame=self.slake_burner_img_time[2],
                    name_save="4.jpg",
                    preds=self.slake_burner_img_time[3])
            # self.assignScore(4, self.slake_burner_img, self.slake_burner_img_time)
            self.save_5 = True
        if len(self.cotton_not_flame_img) > 0 and not self.save_3:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '2.jpg', self.cotton_not_flame_img)
            else:
                self.assignScore(
                    index=2,
                    img=self.cotton_not_flame_img.copy(),
                    object=self.cotton_not_flame_img_time[0],
                    conf=0.1,
                    time_frame=self.cotton_not_flame_img_time[1],
                    num_frame=self.cotton_not_flame_img_time[2],
                    name_save="2.jpg",
                    preds=self.cotton_not_flame_img_time[3])
            # self.assignScore(2, self.cotton_not_flame_img, self.cotton_not_flame_img_time)
            self.save_3 = True
        if len(self.cotton_flame_img) > 0 and not self.save_4:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '3.jpg', self.cotton_flame_img)
            else:
                self.assignScore(
                    index=3,
                    img=self.cotton_flame_img.copy(),
                    object=self.cotton_flame_img_time[0],
                    conf=0.1,
                    time_frame=self.cotton_flame_img_time[1],
                    num_frame=self.cotton_flame_img_time[2],
                    name_save="3.jpg",
                    preds=self.cotton_flame_img_time[3])
            # self.assignScore(3, self.cotton_flame_img, self.cotton_flame_img_time)
            self.save_4 = True
        if len(self.clear_img) > 0 and not self.save_6:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '5.jpg', self.clear_img)
            else:
                self.assignScore(
                    index=5,
                    img=self.clear_img.copy(),
                    object=self.clear_img_time[0],
                    conf=0.1,
                    time_frame=self.clear_img_time[1],
                    num_frame=self.clear_img_time[2],
                    name_save="5.jpg",
                    preds=self.clear_img_time[3])
            # self.assignScore(5, self.clear_img, self.clear_img_time)
            self.save_6 = True

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        # 判断是否倒置溶液
        if 'pour_liquid' in result_key and 'thin_bottle' in result_key and 'beaker' in result_key:
            self.pour_liquid(img0s.copy(), det, result_key)
        # #倒置液体备份：1、细口瓶烧杯相交，2、细口瓶的中心点高于烧杯，3、手拿烧杯或者手拿细口瓶或者都拿
        if 'thin_bottle' in result_key and 'beaker' in result_key and 'hand' in result_key:
            self.pour_liquid_bak(img0s.copy(), det, result_key)
        # 判断是否点燃酒精灯
        if not self.burner_stop and 'burner' in result_key and 'flame' in result_key:
            self.burner_stop = True
        if self.burner_stop and 'burner' in result_key and 'burner_cap' in result_key and 'flame' not in result_key:
            self.slake_burner(img0s.copy(), det, result_key)
        # 未燃烧情况
        if 'cotton' in result_key and 'flame' in result_key and 'clip' in result_key and 'burner' in result_key:
            self.cotton_flame(img0s.copy(), det, result_key)
        # 清洁桌面
        if self.burner_stop and 'clear' in result_key:
            self.clear(img0s.copy(), det, result_key)
        self.save_score_fun(img0s, preds, objects, time, num_frame)

    def process_dict(self, d):
        for key in d.keys():
            if len(d[
                       key]) > 1 and 'beaker' != key and 'hand' != key and 'cotton' != key and 'flame' != key and 'thin_bottle' != key:
                d[key].sort(key=self.sortlist, reverse=True)
                d[key] = [d[key][0]]
            if 'beaker' == key or 'hand' == key or 'cotton' == key or 'flame' == key or 'thin_bottle' == key:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    d[key] = [d[key][0], [0, 0, 0, 0, 0]]
                else:
                    d[key] = d[key][:2]
        return d

    def process_(self, pred, objects=''):
        self.results = pred  # 氧气实验独有
        dict_ = {}
        if objects != '':
            for i in range(len(objects)):
                key = objects[i]['cls']
                value_box = objects[i]['pos']
                value_conf = objects[i]['conf']
                value_ = []
                for j in range(len(value_box)):
                    value_box[j].append(value_conf[j])
                    value_.append(value_box[j])
                dict_[key] = value_
        else:
            names_label = ['hand', 'burner', 'burner_cap', 'clear', 'beaker', 'thin_bottle', 'pour_liquid', 'clip',
                           'cotton', 'matches', 'flame', 'lighter']
            for i in range(len(pred)):
                if pred[i].shape[0] != 0:
                    key = names_label[int(pred[i][0][-1].item())]
                    val = []
                    for j in range(pred[i].shape[0]):
                        val.append(pred[i][j][:5].cpu().detach().numpy().tolist())
                    dict_[key] = val
        dict_ = self.process_dict(dict_)
        return dict_

    def sortlist(self, elem):
        return elem[-1]

    def run_one_result_process(self, frame_top, frame_front, frame_side,
                               pred_top, pred_front, pred_side,
                               time_top, time_front, time_side,
                               num_frame_top,
                               num_frame_front,
                               num_frame_side,
                               path_save,
                               names_label):

        front_preds = None
        top_preds = None
        side_preds = None
        if pred_front is not None and pred_front.shape[0]:
            front_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            dict_ = self.process_(top_preds, objects_front)
            self.num_frame_ = num_frame_front
            self.preds_ = front_preds
            self.objects_ = objects_front
            self.time_ = time_front
            self.predict(frame_front, dict_, list(dict_.keys()), front_preds, objects_front, time_front,
                         num_frame_front)
            # self.plot(front_preds, frame_front)
            # cv2.imshow('1', frame_front)
            # cv2.waitKey(1)

        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=top_preds, front_preds=front_preds, side_preds=side_preds)
