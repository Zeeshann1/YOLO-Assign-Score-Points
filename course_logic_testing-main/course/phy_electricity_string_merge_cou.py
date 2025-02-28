from .comm import *
from .comm.course_base import ConfigModel
from torchvision import transforms
from aideModel import ClassMobilenetv3
from PIL import Image

class PHY_electricity_string_merge(ConfigModel):
    def __init__(self):
        super(PHY_electricity_string_merge, self).__init__()
        self.re_init()

    def re_init(self):
        self.switchstatu_1 = False
        self.switchstatu_2 = False
        self.switchstatu_3 = False

        # 接线
        self.battery_conn_s_c_sta = False

        # 图片
        self.battery_img = []
        self.battery_img_time = []

        self.switch_img = []
        self.switch_img_time = []

        self.light_base_conn_img = []
        self.light_base_conn_img_time = []

        self.light_on_off_img = []
        self.light_on_off_img_time = []

        self.clear_img = []
        self.clear_img_time = []

        self.c_conn = False
        self.b_conn = False

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

    def switch_status(self, img, det, savefile, result_key):
        for i in range(len(det['switch'])):
            s_box = det['switch'][i][:4]
            s_point1 = det['switch'][i][5]
            s_point2 = det['switch'][i][6]
            s_point3 = det['switch'][i][7]
            if (s_point1[0] < s_point2[0] and s_point2[0] < s_point3[0]) or (
                    s_point1[0] > s_point2[0] and s_point2[0] > s_point3[0]):
                # img = self.draw(img, [s_box], ['switch_status'])
                img = self.plot(self.preds_draw, img.copy())
                if i == 0:
                    self.switchstatu_1 = True
                elif i == 1:
                    self.switchstatu_2 = True
                elif i == 2:
                    self.switchstatu_3 = True

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

    # 链接
    def is_two_pos_con(self, det, result_key, box, ba=False):
        '''
        判断是不是并联

        '''
        if 'two_connect_line_pos' in result_key:
            for j in range(len(det['two_connect_line_pos'])):
                t_c_box = det['two_connect_line_pos'][j][:4]
                if self.iou(box, t_c_box) > 0:
                    if ba:
                        return True, t_c_box
                    return True
        if ba:
            return False, []
        else:
            return False

    def is_two_neg_con(self, det, result_key, box, ba=False):
        '''
        判断是不是并联

        '''
        if 'two_connect_line_neg' in result_key:
            for j in range(len(det['two_connect_line_neg'])):
                t_c_box = det['two_connect_line_neg'][j][:4]
                if self.iou(box, t_c_box) > 0:
                    if ba:
                        return True, t_c_box
                    return True
        if ba:
            return False, []
        else:
            return False

    def is_single_pos_con(self, det, result_key, box, ba=False):
        '''
        两个接线柱同时满足：单个接线柱链接是否完成
        '''
        if 'wired_pos' in result_key:
            for i in range(len(det['wired_pos'])):
                c_box = det['wired_pos'][i][:4]
                if self.iou(box, c_box) > 0:
                    if ba:
                        return True, c_box
                    return True
        if ba:
            return False, []
        else:
            return False

    def is_single_neg_con(self, det, result_key, box, ba=False):
        '''
        两个接线柱同时满足：单个接线柱链接是否完成
        '''
        if 'wired_neg' in result_key:
            for i in range(len(det['wired_neg'])):
                c_box = det['wired_neg'][i][:4]
                if self.iou(box, c_box) > 0:
                    if ba:
                        return True, c_box
                    return True
        if ba:
            return False, []
        else:
            return False

    def switch_conn(self, img, det, result_key):
        self.switch_img = []
        for i in range(len(det['switch'])):
            s_box = det['switch'][i][:4]
            s_score = det['switch'][i][4]
            s_pos = self.is_single_pos_con(det, result_key, s_box)
            s_neg = self.is_single_neg_con(det, result_key, s_box)
            w_pos = self.is_two_pos_con(det, result_key, s_box)
            w_neg = self.is_two_neg_con(det, result_key, s_box)
            bo = np.array([s_pos, s_neg, w_pos, w_neg])
            if len(bo[bo == True]) == 2 and s_score > 0.65:
                # self.switch_img.append(self.draw(img.copy(), [s_box], ['switch_' + str(i)]))
                self.switch_img.append(self.plot(self.preds_draw, img.copy()))
                self.switch_img_time.append( [self.objects_, self.time_, self.num_frame_, self.preds_])

    def light_base_conn(self, img, det, result_key):
        self.light_base_conn_img = []
        img1 = img.copy()
        for i in range(len(det['light_base'])):
            l_b_box = det['light_base'][i][:4]
            l_b_score = det['light_base'][i][4]
            s_pos = self.is_single_pos_con(det, result_key, l_b_box)
            s_neg = self.is_single_neg_con(det, result_key, l_b_box)
            w_pos = self.is_two_pos_con(det, result_key, l_b_box)
            w_neg = self.is_two_neg_con(det, result_key, l_b_box)
            bo = np.array([s_pos, s_neg, w_pos, w_neg])
            if len(bo[bo == True]) == 2 and l_b_score > 0.65:
                # self.light_base_conn_img.append(self.draw(img.copy(), [l_b_box], ['light_base_' + str(i)]))
                self.light_base_conn_img.append(self.plot(self.preds_draw, img.copy()))
                self.light_base_conn_img_time.append([self.objects_, self.time_, self.num_frame_, self.preds_])

    def battery_conn(self, img, det, result_key):
        ba_count = 0
        ba_count_2 = 0
        if len(det['battery']) == 2:
            box = []
            for i in range(len(det['battery'])):
                ll = []
                ba_box = det['battery'][i][:4]
                ba_score = det['battery'][i][4]
                s_pos, s_pos_box = self.is_single_pos_con(det, result_key, ba_box, True)
                s_neg, s_neg_box = self.is_single_neg_con(det, result_key, ba_box, True)
                w_pos, w_pos_box = self.is_two_pos_con(det, result_key, ba_box, True)
                w_neg, w_neg_box = self.is_two_neg_con(det, result_key, ba_box, True)
                ll.append(s_pos_box)
                ll.append(s_neg_box)
                ll.append(w_pos_box)
                ll.append(w_neg_box)
                bo = np.array([s_pos, s_neg, w_pos, w_neg])
                if len(bo[bo == True]) == 1:
                    index = np.where(bo == True)[0][0]
                    box_1 = ll[index]
                    if len(box) == 0:
                        box = box_1
                        ba_count += 1
                        # img = self.draw(img, [ba_box], ['battery'])
                        # img = self.plot(self.preds_draw, img.copy())
                    elif len(box) > 0 and self.iou(box_1, box) == 0:
                        ba_count += 1
                        # img = self.draw(img, [ba_box], ['battery'])
                        # img = self.plot(self.preds_draw, img.copy())
                    else:
                        ba_count = ba_count
                elif len(bo[bo == True]) == 2:
                    ba_count_2 += 1
                    # img = self.draw(img, [ba_box], ['battery'])
                    # img = self.plot(self.preds_draw, img.copy())
                if ba_count == 2:
                    self.battery_conn_s_c_sta = True
                elif ba_count_2 == 2:
                    self.battery_conn_s_c_sta = True
                if self.battery_conn_s_c_sta and ba_score > 0.65:
                    self.battery_img = self.plot(self.preds_draw, img.copy())
                    self.battery_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def light_on_off(self, img, det, result_key):
        self.light_on_off_img = []
        for i in range(len(det['light_base'])):
            l_b_box = det['light_base'][i][:4]
            for j in range(len(det['light_open'])):
                l_o_box = det['light_open'][j][:4]
                l_o_score = det['light_open'][j][4]
                if self.iou(l_b_box, l_o_box) > 0:
                    s_pos = self.is_single_pos_con(det, result_key, l_b_box)
                    s_neg = self.is_single_neg_con(det, result_key, l_b_box)
                    w_pos = self.is_two_pos_con(det, result_key, l_b_box)
                    w_neg = self.is_two_neg_con(det, result_key, l_b_box)
                    bo = np.array([s_pos, s_neg, w_pos, w_neg])
                    if len(bo[bo == True]) > 1 and l_o_score > 0.1:
                        # self.light_on_off_img.append(self.draw(img.copy(), [l_o_box], ['light_open']))
                        self.light_on_off_img.append(self.plot(self.preds_draw, img.copy()))
                        self.light_on_off_img_time.append([self.objects_, self.time_, self.num_frame_, self.preds_])

    def clear(self, img, det, result_key):
        for i in range(len(det['clear'])):
            clear_box = det['clear'][i][:4]
            # self.clear_img = self.draw(img.copy(), [clear_box], ['clear_box'])
            self.clear_img = self.plot(self.preds_draw, img.copy())
            self.clear_img_time =  [self.objects_, self.time_, self.num_frame_, self.preds_]

    def draw(self, img, boxs, label):
        '''
        功能：画图，box是列表，对应的label也是一个列表
        '''
        # if not self.not_draw_img:
        #     self.plot(self.results, img)
        #     return img
        assert len(boxs) == len(label)
        for i in range(len(boxs)):
            box = boxs[i]
            if box[0] == 0: continue
            cv2.rectangle(img, (int(box[0]), int(box[1])), \
                          (int(box[2]), int(box[3])), (0, 255, 255), 2)
            lab = f"{label[i]}: {box[-1]:.2f}"
            cv2.putText(img,
                        lab, (int(box[0]), int(box[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 123), 2)
        return img

    def save_score_fun(self):
        # 第一次灯亮时，判断开关个数
        if not self.c_conn and len(self.light_base_conn_img) != 0:
            light_on_off_base = [3, 4]
            for i in range(len(self.light_base_conn_img)):
                self.assignScore(
                    index=light_on_off_base[i],
                    img=self.light_base_conn_img[i].copy(),
                    object=self.light_base_conn_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_base_conn_img_time[i][1],
                    num_frame=self.light_base_conn_img_time[i][2],
                    name_save=str(light_on_off_base[i])+".jpg",
                    preds=self.light_base_conn_img_time[i][3])
        elif not self.b_conn and self.c_conn and len(self.light_base_conn_img) != 0:
            light_on_off_base = [13, 14]
            for i in range(len(self.light_on_off_img)):
                self.assignScore(
                    index=light_on_off_base[i],
                    img=self.light_on_off_img[i].copy(),
                    object=self.light_on_off_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_on_off_img_time[i][1],
                    num_frame=self.light_on_off_img_time[i][2],
                    name_save=str(light_on_off_base[i])+".jpg",
                    preds=self.light_on_off_img_time[i][3])

        if not self.c_conn and len(self.light_on_off_img) != 0:
            light_base = [5, 6]
            for i in range(len(self.light_on_off_img)):
                self.assignScore(
                    index=light_base[i],
                    img=self.light_on_off_img[i].copy(),
                    object=self.light_on_off_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_on_off_img_time[i][1],
                    num_frame=self.light_on_off_img_time[i][2],
                    name_save=str(light_base[i])+".jpg",
                    preds=self.light_on_off_img_time[i][3])
        elif not self.b_conn and self.c_conn and len(self.light_base_conn_img) != 0:
            light_base = [11, 12]
            for i in range(len(self.light_base_conn_img)):
                self.assignScore(
                    index=light_base[i],
                    img=self.light_base_conn_img[i].copy(),
                    object=self.light_base_conn_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_base_conn_img_time[i][1],
                    num_frame=self.light_base_conn_img_time[i][2],
                    name_save=str(light_base[i]) + ".jpg",
                    preds=self.light_base_conn_img_time[i][3])
        if not self.c_conn and len(self.switch_img) != 0 and len(self.switch_img) == 1:
            switch_base = [2]
            for i in range(len(self.switch_img)):
                self.assignScore(
                    index=switch_base[i],
                    img=self.switch_img[i].copy(),
                    object=self.switch_img_time[i][0],
                    conf=0.1,
                    time_frame=self.switch_img_time[i][1],
                    num_frame=self.switch_img_time[i][2],
                    name_save=str(switch_base[i]) + ".jpg",
                    preds=self.switch_img_time[i][3])
        elif not self.b_conn and self.c_conn and len(self.light_base_conn_img) != 0:
            switch_base = [8, 9, 10]
            for i in range(len(self.switch_img)):
                self.assignScore(
                    index=switch_base[i],
                    img=self.switch_img[i].copy(),
                    object=self.switch_img_time[i][0],
                    conf=0.1,
                    time_frame=self.switch_img_time[i][1],
                    num_frame=self.switch_img_time[i][2],
                    name_save=str(switch_base[i]) + ".jpg",
                    preds=self.switch_img_time[i][3])

        if not self.b_conn and len(self.battery_img) != 0:
            self.assignScore(
                index=1,
                img=self.battery_img.copy(),
                object=self.battery_img_time[0],
                conf=0.1,
                time_frame=self.battery_img_time[1],
                num_frame=self.battery_img_time[2],
                name_save="1.jpg",
                preds=self.battery_img_time[3])
        elif not self.b_conn and self.c_conn and len(self.battery_img) != 0:
            self.assignScore(
                index=7,
                img=self.battery_img.copy(),
                object=self.battery_img_time[0],
                conf=0.1,
                time_frame=self.battery_img_time[1],
                num_frame=self.battery_img_time[2],
                name_save="7.jpg",
                preds=self.battery_img_time[3])


        if not self.c_conn and len(self.light_base_conn_img) >= 1 and len(self.light_on_off_img) > 0 and len(
                self.switch_img) == 1 and len(self.battery_img) != 0:
            self.assignScore(
                index=1,
                img=self.battery_img.copy(),
                object=self.battery_img_time[0],
                conf=0.1,
                time_frame=self.battery_img_time[1],
                num_frame=self.battery_img_time[2],
                name_save="1.jpg",
                preds=self.battery_img_time[3])

            switch_base = [2]
            for i in range(len(self.switch_img)):
                self.assignScore(
                    index=switch_base[i],
                    img=self.switch_img[i].copy(),
                    object=self.switch_img_time[i][0],
                    conf=0.1,
                    time_frame=self.switch_img_time[i][1],
                    num_frame=self.switch_img_time[i][2],
                    name_save=str(switch_base[i]) + ".jpg",
                    preds=self.switch_img_time[i][3])

            light_base = [3, 4]
            for i in range(len(self.light_base_conn_img)):
                self.assignScore(
                    index=light_base[i],
                    img=self.light_base_conn_img[i].copy(),
                    object=self.light_base_conn_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_base_conn_img_time[i][1],
                    num_frame=self.light_base_conn_img_time[i][2],
                    name_save=str(light_base[i]) + ".jpg",
                    preds=self.light_base_conn_img_time[i][3])

            light_on_off_base = [5, 6]
            for i in range(len(self.light_on_off_img)):
                self.assignScore(
                    index=light_on_off_base[i],
                    img=self.light_on_off_img[i].copy(),
                    object=self.light_on_off_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_on_off_img_time[i][1],
                    num_frame=self.light_on_off_img_time[i][2],
                    name_save=str(light_on_off_base[i]) + ".jpg",
                    preds=self.light_on_off_img_time[i][3])

            self.re_init()
            self.c_conn = True
        if not self.b_conn and len(self.light_base_conn_img) > 0 and len(self.light_on_off_img) > 0 and len(
                self.switch_img) == 3:
            self.assignScore(
                index=7,
                img=self.battery_img.copy(),
                object=self.battery_img_time[0],
                conf=0.1,
                time_frame=self.battery_img_time[1],
                num_frame=self.battery_img_time[2],
                name_save="7.jpg",
                preds=self.battery_img_time[3])


            switch_base = [8, 9, 10]
            for i in range(len(self.switch_img)):
                self.assignScore(
                    index=switch_base[i],
                    img=self.switch_img[i].copy(),
                    object=self.switch_img_time[i][0],
                    conf=0.1,
                    time_frame=self.switch_img_time[i][1],
                    num_frame=self.switch_img_time[i][2],
                    name_save=str(switch_base[i]) + ".jpg",
                    preds=self.switch_img_time[i][3])


            light_base = [11, 12]
            for i in range(len(self.light_base_conn_img)):
                self.assignScore(
                    index=light_base[i],
                    img=self.light_base_conn_img[i].copy(),
                    object=self.light_base_conn_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_base_conn_img_time[i][1],
                    num_frame=self.light_base_conn_img_time[i][2],
                    name_save=str(light_base[i]) + ".jpg",
                    preds=self.light_base_conn_img_time[i][3])


            light_on_off_base = [13, 14]
            for i in range(len(self.light_on_off_img)):
                self.assignScore(
                    index=light_on_off_base[i],
                    img=self.light_on_off_img[i].copy(),
                    object=self.light_on_off_img_time[i][0],
                    conf=0.1,
                    time_frame=self.light_on_off_img_time[i][1],
                    num_frame=self.light_on_off_img_time[i][2],
                    name_save=str(light_on_off_base[i]) + ".jpg",
                    preds=self.light_on_off_img_time[i][3])


            if len(self.clear_img) != 0:
                self.assignScore(
                    index=15,
                    img=self.clear_img.copy(),
                    object=self.clear_img_time[0],
                    conf=0.1,
                    time_frame=self.clear_img_time[1],
                    num_frame=self.clear_img_time[2],
                    name_save="15.jpg",
                    preds=self.clear_img_time[3])

            self.re_init()
            self.b_conn = True

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        # 第一次灯亮时，判断开关个数
        if 'light_base' in result_key and (('wired_neg' in result_key and 'wired_pos' in result_key) or (
                'two_connect_line_pos' in result_key and 'two_connect_line_neg' in result_key)):
            self.light_base_conn(img0s.copy(), det, result_key)
        if 'light_base' in result_key and 'light_open' in result_key:
            self.light_on_off(img0s.copy(), det, result_key)
        if 'switch' in result_key and (('wired_neg' in result_key and 'wired_pos' in result_key) or (
                'two_connect_line_pos' in result_key and 'two_connect_line_neg' in result_key)):
            self.switch_conn(img0s.copy(), det, result_key)
        if 'clear' in result_key:
            self.clear(img0s.copy(), det, result_key)
        # 电池
        if 'battery' in result_key and 'wired_neg' in result_key and 'wired_pos' in result_key:
            self.battery_conn(img0s.copy(), det, result_key)
        self.save_score_fun()

    def process_dict(self, d):
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
            names_label = ['ammeter', 'ammeter_needle', 'battery', 'light_base', 'light_off', 'no_range', 'not_wired_neg', 'not_wired_pos', 'switch', 'small_range', 'wired_neg', 'wired_pos', 'two_connect_line_neg', 'light_open', 'clear']
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
        top_preds = None
        side_preds = None
        if pred_top is not None and pred_top.shape[0]:
            top_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
            dict_ = self.process_(top_preds, objects_top)
            self.num_frame_ = num_frame_top
            self.preds_ = None
            self.preds_draw =top_preds
            self.objects_ = objects_top
            self.time_ = time_top
            self.predict(frame_top, dict_, list(dict_.keys()), top_preds, objects_top, time_front, num_frame_front)
            # self.plot(top_preds, frame_top)
            # cv2.imshow('a', frame_top)
            # cv2.waitKey(1)
        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=top_preds, front_preds=top_preds, side_preds=side_preds)



