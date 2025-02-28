from .comm import *
from .comm.course_base import ConfigModel


class CHEM_O2_drug(ConfigModel):

    def __init__(
            self
    ):
        super(CHEM_O2_drug, self).__init__()
        self.re_init()

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

    def draw_1(self, img, boxs, label):
        '''
        功能：画图，box是列表，对应的label也是一个列表
        '''
        assert len(boxs) == len(label)
        for i in range(len(boxs)):
            box = boxs[i]
            if box[0] == 0: continue
            cv2.rectangle(img, (int(box[0]), int(box[1])), \
                          (int(box[2]), int(box[3])), (0, 0, 255), 3)
            lab = f"{label[i]}: {box[-1]:.2f}"
            cv2.putText(img,
                        lab, (int(box[0]), int(box[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255), 2)
        return img

    def re_init(self):
        # 手握试管部分
        self.score_1 = False
        self.hand_tube_th = 0.1
        self.hand_tube_img = []
        self.hand_tube_img_time = ''
        # 气泡
        self.score_2 = False
        # 搭建装置
        self.score_3_1 = False
        self.device_start_stop_1 = False
        self.device_start_stop_th_1 = 0.6
        self.device_start_stop_1_img = []
        self.device_start_stop_1_img_time = ''

        self.score_3_2 = False
        self.device_start_stop_2 = False
        self.device_start_stop_th_2 = 0.6
        self.device_start_stop_2_img = []
        self.device_start_stop_2_img_time = ''

        self.score_3_3 = False
        self.device_start_stop_3 = False
        self.device_start_stop_th_3 = 0.6
        self.device_start_stop_3_img = []
        self.device_start_stop_3_img_time = ''
        # 三分之一处、试管口倾斜向下
        self.score_4_1 = False
        self.score_4_2 = False
        self.device_start_stop_4 = False
        self.device_start_stop_th_4 = 0.6
        self.device_start_stop_4_1_img = []
        self.device_start_stop_4_1_img_time = ''
        self.device_start_stop_4_2_img = []
        self.device_start_stop_4_2_img_time = ''
        # 装置整体搭建完毕
        self.score_3_4 = False
        self.device_start_stop_5 = False
        self.device_start_count_1 = 0
        self.device_start_img_1 = []
        self.device_start_stop_5_img = []
        self.device_start_stop_5_img_time = ''
        # 水槽部分
        self.score_6_1 = False
        self.sink_th_1 = 0.7  # 容器
        self.sink_stop_1 = False
        self.sink_stop_1_img = []
        self.sink_stop_1_img_time = ''

        self.score_6_2 = False
        self.sink_th_2 = 0.4  # 盖片
        self.sink_stop_2 = False
        self.sink_stop_2_img = []
        self.sink_stop_2_img_time = ''

        self.score_7 = False
        self.sink_th_3 = 0.7  # 倒扣
        self.sink_stop_3 = False
        self.sink_stop_3_img = []
        self.sink_stop_4_img_time = ''
        # 清理桌面
        self.score_8 = False
        self.clear_th = 0.6
        self.clear_stop = False
        self.clear_stop_img = []
        self.clear_stop_img_time = ''
        # sava
        self.save_1 = True
        self.save_2 = True
        self.save_3 = True
        self.save_4 = True
        self.save_5 = True
        self.save_6 = True
        self.save_7 = True
        self.save_8 = True

        self.start_6_7 = False

        self.device_start_stop_6_img = []
        self.device_start_stop_6_img_time = ''
        self.score_3_6 = False
        self.score_3_6_th = 0.6

        self.results = None
        self.hand_tube_bubble_img = []
        self.hand_tube_img_bubble_time = []
        # 增加得分点
        self.add_drug_img = []
        self.save_9 = True

        self.drug_send_tube_img = []
        self.save_10 = True

        self.flame_add_burner_img = []
        self.save_11 = True
        self.save_11_stop = True

        self.flame_close_img = []
        self.save_12 = True
        self.save_12_stop = True

        self.add_drug_img_2 = []
        self.save_9_2 = True

        self.drug_send_tube_img_2 = []
        self.save_10_2 = True

        self.save_11_2 = False
        self.lighter_and_flame_img = []
        self.flame_add_burner_img_2 = []
        self.add_flame_th = 0.5
        self.not_draw_img = True

    def dis_point(self, p1, p2):
        p1 = [(p1[:4][0] + p1[:4][2]) / 2, (p1[:4][1] + p1[:4][3]) / 2]
        p2 = [(p2[:4][0] + p2[:4][2]) / 2, (p2[:4][1] + p2[:4][3]) / 2]
        x_d = p1[0] - p2[0]
        y_d = p1[1] - p2[1]
        # 用math.sqrt（）求平方根
        return math.sqrt((x_d ** 2) + (y_d ** 2))

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

        ##############################手握试管######################################################

    def fun_hold(self, img, det, result_key):
        '''
        功能：判断手握试管这个标签是否与手、橡胶管相交
        '''
        sink_box = det['s_hand_tube_water_sink'][0]
        sink = det['l_sink'][0]
        rubber_tube = det['l_rubber_tube'][0]
        hand = det['l_hand']
        bool_swsg_1 = not self.score_1 and sink_box[-1] >= self.hand_tube_th
        bool_swsg_2 = self.box_include(sink_box[:4], rubber_tube[:4]) > 0 and self.iou(sink[:4], rubber_tube[:4]) > 0
        bool_swsg_3 = self.iou(hand[0][:4], rubber_tube[:4]) == 0 or self.iou(hand[1][:4], rubber_tube[:4]) == 0
        if bool_swsg_1 and bool_swsg_2 and bool_swsg_3:
            self.hand_tube_th = sink_box[-1]
            draw = img
            self.hand_tube_img = self.draw(draw.copy(), [sink_box], ['s_hand_tube_water_sink'])
            self.hand_tube_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.hand_tube_bubble_img = self.draw(draw.copy(), [sink], ['sink'])
            self.hand_tube_bubble_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

        ##############################装置摆放######################################################

    def fun_device_zjdz(self, img, det, result_key):
        burner_holder_tube = det['s_burner_holder_tube'][0]
        holder_bottom = det['l_holder_bottom'][0]
        # 1 支架底座
        bool_1 = not self.device_start_stop_1 and burner_holder_tube[-1] > 0.5 and holder_bottom[
            -1] > self.device_start_stop_th_1
        bool_2 = self.iou(burner_holder_tube[:4], holder_bottom[:4]) > 0.1
        if bool_1 and bool_2:
            self.device_start_stop_th_1 = holder_bottom[-1]
            draw = img.copy()
            self.device_start_stop_1_img = self.draw(draw, [holder_bottom], ['l_holder_bottom'])
            self.device_start_stop_1_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_3_1 = True
            if holder_bottom[-1] > 0.7:
                self.device_start_stop_1 = True
                return True
        return False

    def fun_device_jjd(self, img, det, result_key):
        burner_holder_tube = det['s_burner_holder_tube'][0]
        burner = det['l_burner'][0]
        # 2 酒精灯
        bool_1 = not self.device_start_stop_2 and burner_holder_tube[-1] > 0.5 and burner[
            -1] > self.device_start_stop_th_2
        bool_2 = self.iou(burner_holder_tube[:4], burner[:4]) > 0.1
        if bool_1 and bool_1:
            self.device_start_stop_th_2 = burner[-1]
            draw = img
            self.device_start_stop_2_img = self.draw(draw, [burner], ['l_burner'])
            self.device_start_stop_2_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_3_2 = True
            if burner[-1] > 0.65:
                self.device_start_stop_2 = True
                return True
        return False

    def fun_device_zjxn(self, img, det, result_key):
        hand = det['l_hand']
        holder_bottom = det['l_holder_bottom'][0]
        holder_bottom_knob = det['l_holder_bottom_knob'][0]
        # 3 支架旋钮
        bool_1 = not self.device_start_stop_3 and (self.device_start_stop_1 or self.device_start_stop_2)
        bool_2 = self.iou(holder_bottom[:4], hand[0][:4]) > 0.05
        bool_3 = self.iou(holder_bottom_knob[:4], hand[0][:4]) > 0.05 or self.iou(holder_bottom_knob[:4],
                                                                                  hand[1][:4]) > 0.05
        bool_4 = holder_bottom_knob[-1] > 0.6
        if bool_1 and bool_2 and bool_3 and bool_4:
            self.device_start_stop_th_3 = holder_bottom_knob[-1]
            draw = img
            self.device_start_stop_3_img = self.draw(draw, [holder_bottom_knob], ['l_holder_bottom_knob'])
            self.device_start_stop_3_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_3_3 = True
            if holder_bottom_knob[-1] > 0.6:
                self.device_start_stop_3 = True
                return True
        return False

    def fun_device_sg_jz(self, img, det, result_key):
        hand = det['l_hand']
        tube = det['l_tube'][0]
        holder_clip = det['l_holder_clip'][0]
        tube_head = det['l_tube_head'][0]
        # 4 试管和支架夹子
        bool_1 = not self.device_start_stop_4 and (self.device_start_stop_3 or self.device_start_stop_1)
        bool_2 = self.iou(hand[0][:4], tube[:4]) == 0 or self.iou(hand[1][:4], tube[:4]) == 0
        bool_3 = self.iou(hand[0][:4], holder_clip[:4]) == 0 or self.iou(hand[1][:4], holder_clip[:4]) == 0
        bool_4 = self.iou(tube_head[:4], tube[:4]) > 0
        bool_5 = self.iou(tube[:4], holder_clip[:4]) > 0 and tube[-1] > 0.6 and holder_clip[-1] > 0.6
        if bool_1 and bool_2 and bool_3 and bool_4 and bool_5:
            draw_1 = img.copy()
            self.device_start_stop_4_1_img = self.draw(draw_1, [tube, holder_clip],
                                                       ['tube', 'l_holder_clip'])
            self.device_start_stop_4_1_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_4_1 = True
            draw_2 = img.copy()
            self.device_start_stop_4_2_img = self.draw(draw_2, [tube], ['tube'])
            self.device_start_stop_4_2_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_4_2 = True
            self.device_start_stop_4 = True
            return True
        return False

    def fun_device_final_1(self, img, det, result_key):
        burner_holder_tube_sink_hand = det['s_burner_holder_tube_sink_hand'][0]
        rubber_tube = det['l_rubber_tube'][0]
        sink = det['l_sink'][0]
        bool_1 = not self.device_start_stop_5 and self.device_start_stop_4
        bool_2 = burner_holder_tube_sink_hand[-1] > self.device_start_stop_th_4 and self.iou(rubber_tube[:4],
                                                                                             sink[:4]) > 0
        bool_3 = 'l_holder_bottom' in result_key or 'l_burner' in result_key
        if bool_1 and bool_2 and bool_3:
            self.device_start_stop_th_4 = burner_holder_tube_sink_hand[-1]
            self.device_start_img_1 = self.draw(img, [burner_holder_tube_sink_hand], ['burner_holder_tube_sink_hand'])
            return True
        return False

    def fun_device_final_2(self, img, det, result_key):
        sink = det['l_sink'][0]
        rubber_tube = det['l_rubber_tube'][0]
        bool_1 = len(self.device_start_img_1) > 0 and not self.device_start_stop_5
        bool_2 = self.iou(sink[:4], rubber_tube[:4]) > 0
        if bool_1 and bool_2:
            self.device_start_stop_5_img = self.device_start_img_1
            self.device_start_stop_5_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_3_4 = True
            self.device_start_stop_5 = True
            return True
        return False

    def fun_device_final_3(self, img, det, result_key):
        # 4 整体装置都安装完毕
        burner_holder_tube = det['s_burner_holder_tube'][0]
        if burner_holder_tube[4] > self.score_3_6_th:
            self.score_3_6_th = burner_holder_tube[4]
            draw = img
            self.device_start_stop_6_img = self.draw(draw, [burner_holder_tube], ['burner_holder_tube'])
            self.device_start_stop_6_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_3_6 = True
            return True
        return False

        ##############################集气瓶收集气体######################################################

    def fun_sink_1(self, img, det, result_key):
        hand_0 = det['l_hand'][0]
        hand_1 = det['l_hand'][1]
        container = det['l_container'][0]
        sink = det['l_sink'][0]
        bool_1 = self.device_start_stop_1 or self.device_start_stop_2 or self.device_start_stop_3 or self.device_start_stop_4 or self.device_start_stop_5
        # 容器
        bool_2 = not self.sink_stop_1 and container[-1] > self.sink_th_1 and self.box_include(container[:4], sink[:4])
        if bool_1 and bool_2:
            self.sink_th_1 = container[-1]
            draw = img
            self.sink_stop_1_img = self.draw(draw, [container], ['l_container'])
            self.sink_stop_1_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_6_1 = True
            self.sink_stop_1 = True
        # 倒扣:水槽包含容器、两只手与水槽有iou,容器与任意一只手有交集
        bool_3 = not self.sink_stop_3 and container[-1] > self.sink_th_3
        bool_4 = self.box_include(container[:4], sink[:4])
        bool_5 = self.iou(sink[:4], hand_0[:4]) > 0.1 and self.iou(sink[:4], hand_0[:4]) > 0.1
        bool_6 = self.iou(container[:4], hand_0[:4]) > 0.1 and self.iou(container[:4], hand_1[:4]) > 0.1
        if bool_1 and bool_3 and bool_4 and bool_5 and bool_6:
            self.sink_th_3 = container[-1]
            draw = img
            self.sink_stop_3_img = self.draw(draw, [container, hand_0, hand_1],
                                             ['l_container', 'l_hand', 'l_hand'])
            self.sink_stop_3_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_7 = True
            self.sink_stop_3 = True

    def fun_sink_2(self, img, det, result_key):

        hand_0 = det['l_hand'][0]
        hand_1 = det['l_hand'][1]
        sink = det['l_sink'][0]
        coverglass = det['l_coverglass'][0]
        # 盖片
        bool_1 = not self.sink_stop_2 and coverglass[-1] > self.sink_th_2
        bool_2 = self.box_include(coverglass[:4], sink[:4])
        if bool_1 and bool_2:
            self.sink_th_2 = coverglass[-1]
            draw = img
            self.sink_stop_2_img = self.draw(draw, [coverglass], ['l_coverglass'])
            self.sink_stop_2_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_6_2 = True
            self.sink_stop_2 = True
        # 倒扣:盖片和水槽是包含关系 切水槽与两只手有iou、任意一只手与盖片有iou
        bool_3 = not self.sink_stop_3 and coverglass[-1] > self.sink_th_3
        bool_4 = self.box_include(coverglass[:4], sink[:4])
        bool_5 = self.iou(sink[:4], hand_0[:4]) > 0.1 and self.iou(sink[:4], hand_0[:4]) > 0.1
        bool_6 = self.iou(coverglass[:4], hand_0[:4]) > 0.15 or self.iou(coverglass[:4], hand_1[:4]) > 0.15
        if bool_3 and bool_4 and bool_5 and bool_6:
            self.sink_th_3 = coverglass[-1]
            draw = img
            self.sink_stop_3_img = self.draw(draw, [coverglass, hand_0, hand_1],
                                             ['l_container', 'l_hand', 'l_hand'])
            self.sink_stop_3_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_7 = True
            self.sink_stop_3 = True

    def fun_sink_3(self, img, det, result_key):

        hand_0 = det['l_hand'][0]
        hand_1 = det['l_hand'][1]
        container = det['l_container'][0]
        coverglass = det['l_coverglass'][0]
        sink = det['l_sink'][0]
        # 容器
        bool_1 = not self.sink_stop_1 and container[-1] > self.sink_th_1
        bool_2 = self.box_include(container[:4], sink[:4])
        if bool_1 and bool_2:
            self.sink_th_1 = container[-1]
            draw = img
            self.sink_stop_1_img = self.draw(draw, [container], ['l_container'])
            self.sink_stop_1_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_6_1 = True
            self.sink_stop_1 = True
        # 盖片
        bool_3 = not self.sink_stop_2 and coverglass[-1] > self.sink_th_2
        bool_4 = self.box_include(coverglass[:4], sink[:4])
        if bool_3 and bool_4:
            self.sink_th_2 = coverglass[-1]
            draw = img
            self.sink_stop_2_img = self.draw(draw, [coverglass], ['l_coverglass'])
            self.sink_stop_2_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_6_2 = True
            self.sink_stop_2 = True
        # 倒扣：盖片、容器有交集，两只手和水槽有iou 手和盖片或者容器有iou
        bool_5 = self.iou(container[:4], coverglass[:4]) > 0 and self.iou(sink[:4], hand_0[:4]) > 0.1 and self.iou(
            sink[:4], hand_1[:4]) > 0.1
        bool_6 = self.iou(container[:4], hand_0[:4]) > 0 or self.iou(coverglass[:4], hand_0[:4]) > 0
        bool_7 = self.iou(container[:4], hand_1[:4]) > 0 or self.iou(coverglass[:4], hand_1[:4]) > 0
        bool_8 = self.iou(coverglass[:4], hand_0[:4]) > 0.1 or self.iou(coverglass[:4], hand_1[:4]) > 0.1
        if bool_5 and (bool_6 or bool_7) and bool_8 and container[-1] > self.sink_th_3:
            self.sink_th_3 = container[-1]
            draw = img
            self.sink_stop_3_img = self.draw(draw, [container, coverglass, hand_0, hand_1],
                                             ['l_container', 'l_coverglass', 'l_hand', 'l_hand'])
            self.sink_stop_3_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_7 = True
            self.sink_stop_3 = True

        ##############################整理桌面######################################################

    def fun_clear(self, img, det, result_key):
        if 'l_clear' in det.keys():
            clear = det['l_clear'][0]
            inlist = []
            if not self.clear_stop and clear[-1] > self.clear_th:
                for key in result_key:
                    if key in ['l_clear', 'l_hand']:
                        continue
                    item = det[key][0]
                    center_x, center_y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                    if clear[0] < center_x < clear[2] and clear[1] < center_y < clear[3]:
                        inlist.append(item)
                        if len(inlist) > 0:
                            break
                if len(inlist) == 0:
                    self.clear_th = clear[-1]
                    self.clear_stop_img = self.draw(img, [clear], ['l_clear'])
                    self.clear_stop_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.score_8 = True
                    if self.clear_th > 0.8:
                        self.clear_stop = True

    def fun_clear_hand(self, img, det, result_key):
        if 'l_hand' in result_key and 'l_towel' in result_key:
            hand = det['l_hand']
            towel = det['l_towel'][0]
            if 'l_holder_clip' in result_key and 'l_tube' in result_key:
                holder_clip = det['l_holder_clip'][0]
                tube = det['l_tube'][0]
                bool_t_c_4_1 = self.iou(holder_clip[:4], tube[:4]) > 0
                if bool_t_c_4_1:
                    return
            bool_c_8_1 = self.iou(hand[0][:4], towel[:4]) > 0 or self.iou(hand[1][:4], towel[:4]) > 0
            if bool_c_8_1:
                self.clear_stop_img = img
                self.clear_stop_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
                self.score_8 = True

    def fun_clear_2(self, img, det, result_key):
        tube = det['l_tube'][0]
        tube_head = det['l_tube_head'][0]
        bool_1 = self.iou(tube_head[:4], tube[:4]) == 0
        if bool_1:
            self.clear_stop_img = img
            self.clear_stop_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.score_8 = True

    def fun_clear_(self, img, det, result_key):
        if 'l_clear' in det.keys():
            clear = det['l_clear'][0]
            inlist = []
            if not self.clear_stop and clear[-1] > self.clear_th:
                for key in result_key:
                    if key in ['l_clear', 'l_hand']:
                        continue
                    item = det[key][0]
                    center_x, center_y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                    if clear[0] < center_x < clear[2] and clear[1] < center_y < clear[3]:
                        inlist.append(item)
                        if len(inlist) > 0:
                            break
                if len(inlist) == 0:
                    self.clear_th = clear[-1]
                    self.clear_stop_img = self.draw(img, [clear], ['l_clear'])
                    self.clear_stop_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.score_8 = True
                    if self.clear_th > 0.8:
                        self.clear_stop = True

        ##############################增加得分点:取氯酸钾和二氧化锰（两者3：1比例）混合均匀######################################################

    def fun2_clear(self, img, det, result_key):
        w_dis = img.shape[1] / 4
        bool_1 = 'l_holder_clip' not in result_key and 'l_holder_bottom_knob' not in result_key
        if bool_1:
            self.clear_stop_img = img.copy()
            self.clear_stop_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            return
        if 'l_holder_clip' in result_key:
            box = det['l_holder_clip'][0]
        elif 'l_holder_bottom_knob' in result_key:
            box = det['l_holder_bottom_knob'][0]
        elif 'l_lamp_cap' in result_key:
            box = det['l_lamp_cap'][0]
        else:
            box = []
        if len(box) > 0:
            w = (box[0] + box[2]) / 2
            if w > w_dis * 3 or w < w_dis:
                self.clear_stop_img = img.copy()
                self.clear_stop_img_time = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]
                return

    def fun_add_drug(self, img, det, result_key):
        draw = img.copy()
        spoon = det['l_spoon'][0]
        tube = det['l_tube'][0]
        w, h = spoon[2] - spoon[0], spoon[3] - spoon[1]
        hand = det['l_hand']
        if 'l_potassium_permanganate' in result_key:
            box = det['l_potassium_permanganate'][0]
        elif 'l_sodium_chloride' in result_key:
            box = det['l_sodium_chloride'][0]
        else:
            box = []
        if len(box) > 1:
            bool_1 = self.iou(spoon[:4], box[:4]) > 0
        else:
            bool_1 = False
        # 手和勺子有交集
        bool_2 = self.iou(hand[0][:4], spoon[:4]) > 0 or self.iou(hand[1][:4], spoon[:4]) > 0
        bool_3 = w > h * 1.5
        # 手和试管有交集
        bool_4 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        if bool_1 and bool_2 and bool_3 and bool_4:
            self.add_drug_img = self.draw(draw, [spoon, box], ['flame', 'drug'])
            self.add_drug_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def fun_add_drug_2(self, img, det, result_key):
        draw = img.copy()
        spoon = det['l_spoon'][0]
        # tube = det['l_tube'][0]
        w, h = spoon[2] - spoon[0], spoon[3] - spoon[1]
        hand = det['l_hand']
        if 'l_spoon_permanganate' in result_key:
            box = det['l_spoon_permanganate'][0]
        elif 'l_spoon_chloride' in result_key:
            box = det['l_spoon_chloride'][0]
        else:
            box = []
        if len(box) > 1:
            bool_1 = self.iou(spoon[:4], box[:4]) > 0
        else:
            bool_1 = False
        # 手和勺子有交集
        bool_2 = self.iou(hand[0][:4], spoon[:4]) > 0 or self.iou(hand[1][:4], spoon[:4]) > 0
        bool_3 = w > h * 1.5
        # 手和试管有交集
        # bool_4 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        if bool_1 and bool_2 and bool_3:
            self.add_drug_img_2 = self.draw(draw, [spoon, box], ['flame', 'drug'])
            self.add_drug_img_2_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def fun2_add_drug(self, img, det, result_key):
        draw = img.copy()
        spoon = det['l_spoon'][0]
        spoon_c_y = (spoon[1] + spoon[3]) / 2
        tube = det['l_tube'][0]
        w, h = spoon[2] - spoon[0], spoon[3] - spoon[1]
        hand = det['l_hand']
        if 'l_potassium_permanganate' in result_key:
            box = det['l_potassium_permanganate'][0]
        elif 'l_sodium_chloride' in result_key:
            box = det['l_sodium_chloride'][0]
        else:
            box = []
        if len(box) > 1:
            box_c_y = (box[1] + box[3]) / 2
            bool_1 = self.iou(spoon[:4], box[:4]) > 0 and box_c_y > spoon_c_y
        else:
            bool_1 = False
        # 手和勺子有交集
        bool_2 = self.iou(hand[0][:4], spoon[:4]) > 0 or self.iou(hand[1][:4], spoon[:4]) > 0
        # bool_3 = w>h*1.5
        # 手和试管有交集
        bool_3 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        if bool_1 and bool_2 and bool_3:
            self.add_drug_img = self.draw(draw, [spoon, box], ['flame', 'drug'])
            self.add_drug_img_time = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]

    def fun2_add_drug_2(self, img, det, result_key):
        draw = img.copy()
        spoon = det['l_spoon'][0]
        w, h = spoon[2] - spoon[0], spoon[3] - spoon[1]
        hand = det['l_hand']
        if 'l_spoon_permanganate' in result_key:
            box = det['l_spoon_permanganate'][0]
        elif 'l_spoon_chloride' in result_key:
            box = det['l_spoon_chloride'][0]
        else:
            box = []
        if len(box) > 1:
            bool_1 = self.iou(spoon[:4], box[:4]) > 0
        else:
            bool_1 = False
        # 手和勺子有交集
        bool_2 = self.iou(hand[0][:4], spoon[:4]) > 0 or self.iou(hand[1][:4], spoon[:4]) > 0
        bool_3 = w > h
        if bool_1 and bool_2 and bool_3:
            self.add_drug_img_2 = self.draw(draw, [spoon, box], ['flame', 'drug'])
            self.add_drug_img_2_time = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]
        ##############################用药匙或纸槽将药品送入到试管底部######################################################

    def fun_drug_send_tube(self, img, det, result_key):
        draw = img.copy()
        tube = det['l_tube'][0]
        t_w, t_h = tube[2] - tube[0], tube[3] - tube[1]
        hand = det['l_hand']
        if 'l_spoon' in result_key:
            box = det['l_spoon'][0]
        elif 'l_paper_slot' in result_key:
            box = det['l_paper_slot'][0]
        else:
            box = []
        # 手与试管相交
        bool_1 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        # 试管与勺子或者纸槽相交
        if len(box) > 1:
            w, h = box[2] - box[0], box[3] - box[1]
            bool_2 = self.iou(tube[:4], box[:4]) > 0 and (len(self.add_drug_img) > 0 or len(self.add_drug_img_2) > 0)
            # 手与勺子或者纸槽相交
            bool_3 = self.iou(hand[0][:4], box[:4]) > 0 or self.iou(hand[1][:4], box[:4]) > 0
            # 勺子或者纸槽宽是高的1.5倍以上
            bool_4 = w > 1.5 * h  # and t_w>t_h*1.5
        else:
            bool_2 = False
            bool_3 = False
            bool_4 = False
        if bool_1 and bool_2 and bool_3 and bool_4:
            self.drug_send_tube_img = self.draw(draw, [tube, box], ['tube', 'drug'])
            self.drug_send_tube_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def fun_drug_send_tube_2(self, img, det, result_key):
        draw = img.copy()
        tube = det['l_tube'][0]
        t_w, t_h = tube[2] - tube[0], tube[3] - tube[1]
        hand = det['l_hand']
        if 'l_spoon' in result_key:
            box = det['l_spoon'][0]
        elif 'l_paper_slot' in result_key:
            box = det['l_paper_slot'][0]
        else:
            box = []
        # 判断试管底部是否有反应物
        if 'l_tube_bottom' in result_key:
            box_ = det['l_tube_bottom'][0]
        else:
            box_ = []
        # 试管底部反应物与试管有交集
        if len(box_) > 0:
            bool_1 = self.iou(hand[0][:4], tube[:4]) > 0
        else:
            bool_1 = False
        # 手与试管相交
        bool_2 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        # 试管与勺子或者纸槽相交
        if len(box) > 1:
            w, h = box[2] - box[0], box[3] - box[1]
            bool_3 = len(self.add_drug_img_2) > 0 or len(self.add_drug_img) > 0
            # 手与勺子或者纸槽相交
            bool_4 = self.iou(hand[0][:4], box[:4]) > 0 or self.iou(hand[1][:4], box[:4]) > 0
            # 勺子或者纸槽宽是高的1.5倍以上
            bool_5 = w > 1.5 * h  # and t_w>t_h*1.5
        else:
            bool_3 = False
            bool_4 = False
            bool_5 = False
        if bool_1 and bool_2 and bool_3 and bool_4 and bool_5:
            self.drug_send_tube_img_2 = self.draw(draw, [tube, box], ['tube', 'drug'])
            self.drug_send_tube_img_2_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def fun2_drug_send_tube(self, img, det, result_key):
        draw = img.copy()
        tube = det['l_tube'][0]
        t_w, t_h = tube[2] - tube[0], tube[3] - tube[1]
        hand = det['l_hand']
        if 'l_spoon' in result_key:
            box = det['l_spoon'][0]
        elif 'l_paper_slot' in result_key:
            box = det['l_paper_slot'][0]
        else:
            box = []
        # 手与试管相交
        bool_1 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        # 试管与勺子或者纸槽相交
        if len(box) > 1:
            w, h = box[2] - box[0], box[3] - box[1]
            bool_2 = self.iou(tube[:4], box[:4]) > 0 and (len(self.add_drug_img) > 0 or len(self.add_drug_img_2) > 0)
            # 手与勺子或者纸槽相交
            bool_3 = self.iou(hand[0][:4], box[:4]) > 0 or self.iou(hand[1][:4], box[:4]) > 0
            # 勺子或者纸槽宽是高的1倍以上
            bool_4 = w > h  # and t_w>t_h*1.5
        else:
            bool_2 = False
            bool_3 = False
            bool_4 = False
        if bool_1 and bool_2 and bool_3 and bool_4:
            self.drug_send_tube_img = self.draw(draw, [tube, box], ['tube', 'drug'])
            self.drug_send_tube_img_time = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]

    def fun2_drug_send_tube_2(self, img, det, result_key):
        draw = img.copy()
        tube = det['l_tube'][0]
        t_w, t_h = tube[2] - tube[0], tube[3] - tube[1]
        hand = det['l_hand']
        if 'l_spoon' in result_key:
            box = det['l_spoon'][0]
        elif 'l_paper_slot' in result_key:
            box = det['l_paper_slot'][0]
        else:
            box = []
        # 判断试管底部是否有反应物
        if 'l_tube_bottom' in result_key:
            box_ = det['l_tube_bottom'][0]
        else:
            box_ = []
        # 试管底部反应物与试管有交集
        if len(box_) > 0:
            bool_1 = self.iou(hand[0][:4], tube[:4]) > 0
        else:
            bool_1 = False
        # 手与试管相交
        bool_2 = self.iou(hand[0][:4], tube[:4]) > 0 or self.iou(hand[1][:4], tube[:4]) > 0
        # 试管与勺子或者纸槽相交
        if len(box) > 1:
            w, h = box[2] - box[0], box[3] - box[1]
            bool_3 = len(self.add_drug_img_2) > 0 or len(self.add_drug_img) > 0
            # 手与勺子或者纸槽相交
            bool_4 = self.iou(hand[0][:4], box[:4]) > 0 or self.iou(hand[1][:4], box[:4]) > 0
            # 勺子或者纸槽宽是高的1.5倍以上
            bool_5 = w > 1.5 * h  # and t_w>t_h*1.5
        else:
            bool_3 = False
            bool_4 = False
            bool_5 = False
        if bool_1 and bool_2 and bool_3 and bool_4 and bool_5:
            self.drug_send_tube_img_2 = self.draw(draw, [tube, box], ['tube', 'drug'])
            self.drug_send_tube_img_2_time = [self.objects_front, self.time_front, self.num_frame_front,
                                              self.preds_front]
        ##############################点燃酒精灯加热######################################################

    def fun_lighter_and_flame(self, img, det, result_key):
        hand = det['l_hand']
        lighter = det['l_lighter'][0]
        burner = det['l_burner'][0]
        draw = img.copy()
        if 'l_lamp_cap' in result_key:
            box = det['l_lamp_cap'][0]
            bool_1 = self.iou(burner[:4], box[:4]) == 0
        else:
            bool_1 = False
        bool_2 = self.iou(hand[0][:4], lighter[:4]) > 0 or self.iou(hand[1][:4], lighter[:4]) > 0
        bool_3 = self.iou(lighter[:4], burner[:4]) > 0
        if bool_1 and bool_2 and bool_3:
            self.lighter_and_flame_img = self.draw(draw, [lighter, burner], ['lighter', 'burner'])
            self.lighter_and_flame_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def fun_flame_add_burner(self, img, det, result_key):
        flame = det['l_flame'][0]
        tube_bottom = det['l_tube_bottom'][0]
        draw = img.copy()
        bool_1 = self.iou(flame[:4], tube_bottom[:4]) > 0
        if bool_1 and flame[-1] > self.add_flame_th:
            self.add_flame_th = flame[-1]
            self.flame_add_burner_img = self.draw(draw, [flame, tube_bottom], ['flame', 'l_tube_bottom'])
            self.flame_add_burner_img_time = [self.objects_front, self.time_front, self.num_frame_front,
                                              self.preds_front]

    def fun2_flame_add_burner(self, img, det, result_key):
        flame = det['l_flame'][0]
        tube_bottom = det['l_tube_bottom'][0]
        draw = img.copy()
        bool_1 = self.iou(flame[:4], tube_bottom[:4]) > 0
        if bool_1 and flame[-1] > self.add_flame_th:
            self.add_flame_th = flame[-1]
            self.flame_add_burner_img = self.draw(draw, [flame, tube_bottom], ['flame', 'l_tube_bottom'])
            self.flame_add_burner_img_time = [self.objects_front, self.time_front, self.num_frame_front,
                                              self.preds_front]

    def fun_flame_add_burner_2(self, img, det, result_key):
        if 's_burner_holder_tube' in result_key:
            box = det['s_burner_holder_tube'][0]
        elif 's_burner_holder_tube_sink' in result_key:
            box = det['s_burner_holder_tube_sink'][0]
        else:
            box = det['s_burner_holder_tube_sink_hand'][0]
        burner = det['l_burner'][0]
        tube_bottom = det['l_tube_bottom'][0]
        draw = img.copy()
        bool_1 = self.iou(burner[:4], tube_bottom[:4]) > 0
        bool_2 = self.iou(box[:4], tube_bottom[:4]) > 0
        bool_3 = self.iou(burner[:4], box[:4]) > 0
        if bool_1 and bool_2 and bool_3:
            self.flame_add_burner_img_2 = self.draw(draw, [burner, tube_bottom], ['flame', 'l_tube_bottom'])
            self.flame_add_burner_img_2_time = [self.objects_, self.time_, self.num_frame_, self.preds_]

        ##############################熄灭酒精灯######################################################

    def fun_flame_close(self, img, det, result_key):
        burner = det['l_burner'][0]
        lamp_cap = det['l_lamp_cap'][0]
        draw = img.copy()
        if 'l_flame' in result_key:
            flame = det['l_flame'][0]
            bool_1 = self.iou(flame[:4], lamp_cap[:4]) > 0
            if bool_1 and len(self.flame_close_img) == 0:
                self.flame_close_img = self.draw(draw, [flame, lamp_cap], ['flame', 'lamp_cap'])
                self.flame_close_img_time = [self.objects_, self.time_, self.num_frame_,
                                             self.preds_]
                # cv2.imshow('a', img)
                # cv2.waitKey(0)
                return
        bool_2 = self.iou(burner[:4], lamp_cap[:4]) > 0
        if bool_2 and len(self.flame_close_img) == 0:
            self.flame_close_img = self.draw(draw, [burner, lamp_cap], ['burner', 'lamp_cap'])
            self.flame_close_img_time = [self.objects_, self.time_, self.num_frame_, self.preds_]
            # cv2.imshow('a', img)
            # cv2.waitKey(0)

    def fun2_flame_close(self, img, det, result_key):
        burner = det['l_burner'][0]
        lamp_cap = det['l_lamp_cap'][0]
        draw = img.copy()
        if 'l_flame' in result_key:
            flame = det['l_flame'][0]
            bool_1 = self.iou(flame[:4], lamp_cap[:4]) > 0
            if bool_1 and len(self.flame_close_img) == 0:
                self.flame_close_img = self.draw(draw, [flame, lamp_cap], ['flame', 'lamp_cap'])
                self.flame_close_img_time = [self.objects_front, self.time_front, self.num_frame_front,
                                             self.preds_front]
                # cv2.imshow('a', img)
                # cv2.waitKey(0)
                return
        bool_2 = self.iou(burner[:4], lamp_cap[:4]) > 0
        if bool_2 and len(self.flame_close_img) == 0:
            self.flame_close_img = self.draw(draw, [burner, lamp_cap], ['burner', 'lamp_cap'])
            self.flame_close_img_time = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]
            # cv2.imshow('a', img)
            # cv2.waitKey(0)

    def save_score_fun(self):
        if self.save_6 and self.save_7:
            bool_1 = self.device_start_stop_1 or self.device_start_stop_2 or self.device_start_stop_3 or self.device_start_stop_4 or self.device_start_stop_5
            # 得分点1：将导管伸入水中，用手捂试管或微热试管
            if len(self.hand_tube_img) > 0 and bool_1 and self.save_1:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '1.jpg', self.hand_tube_img)
                else:
                    self.assignScore(
                        index=1,
                        img=self.hand_tube_img.copy(),
                        object=self.hand_tube_img_time[0],
                        conf=0.1,
                        time_frame=self.hand_tube_img_time[1],
                        num_frame=self.hand_tube_img_time[2],
                        name_save="1.jpg",
                        preds=self.hand_tube_img_time[3])
                self.save_1 = False
            # 得分点2：导管口有气泡（暂时不做）
            if len(self.hand_tube_bubble_img) > 0 and bool_1 and self.save_2:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '2.jpg', self.hand_tube_bubble_img)
                else:
                    self.assignScore(
                        index=2,
                        img=self.hand_tube_bubble_img.copy(),
                        object=self.hand_tube_bubble_img_time[0],
                        conf=0.1,
                        time_frame=self.hand_tube_bubble_img_time[1],
                        num_frame=self.hand_tube_bubble_img_time[2],
                        name_save="2.jpg",
                        preds=self.hand_tube_bubble_img_time[3])
                self.save_2 = False

            # 得分点9：取氯酸钾和二氧化锰（两者3：1比例）混合均匀
            if len(self.add_drug_img_2) > 0 and self.save_9_2:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '9.jpg', self.add_drug_img_2)
                else:
                    self.assignScore(
                        index=9,
                        img=self.add_drug_img_2.copy(),
                        object=self.add_drug_img_2_time[0],
                        conf=0.1,
                        time_frame=self.add_drug_img_2_time[1],
                        num_frame=self.add_drug_img_2_time[2],
                        name_save="9.jpg",
                        preds=self.add_drug_img_2_time[3])
                # self.assignScore(9, self.add_drug_img_2, time.time())
                self.save_9_2 = False
                self.save_9 = False

            if len(self.add_drug_img) > 0 and self.save_9:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '9.jpg', self.add_drug_img)
                else:
                    self.assignScore(
                        index=9,
                        img=self.add_drug_img.copy(),
                        object=self.add_drug_img_time[0],
                        conf=0.1,
                        time_frame=self.add_drug_img_time[1],
                        num_frame=self.add_drug_img_time[2],
                        name_save="9.jpg",
                        preds=self.add_drug_img_time[3])
                # self.save_9 = False
            # 得分点10：用药匙或纸槽将药品送入到试管底部
            if len(self.drug_send_tube_img) > 0 and self.save_10:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '10.jpg', self.drug_send_tube_img)
                else:
                    self.assignScore(
                        index=10,
                        img=self.drug_send_tube_img.copy(),
                        object=self.drug_send_tube_img_time[0],
                        conf=0.1,
                        time_frame=self.drug_send_tube_img_time[1],
                        num_frame=self.drug_send_tube_img_time[2],
                        name_save="10.jpg",
                        preds=self.drug_send_tube_img_time[3])
                # self.assignScore(10, self.drug_send_tube_img, time.time())
                self.save_10 = False
                self.save_10_2 = False
            if len(self.drug_send_tube_img_2) > 0 and self.save_10_2:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '10.jpg', self.drug_send_tube_img_2)
                else:
                    self.assignScore(
                        index=2,
                        img=self.drug_send_tube_img_2.copy(),
                        object=self.drug_send_tube_img_2_time[0],
                        conf=0.1,
                        time_frame=self.drug_send_tube_img_2_time[1],
                        num_frame=self.drug_send_tube_img_2_time[2],
                        name_save="10.jpg",
                        preds=self.drug_send_tube_img_2_time[3])
                # self.assignScore(10, self.drug_send_tube_img_2, time.time())
                # self.save_10 = False
            # 得分点3：按由下往上、从左到右的顺序搭建装置
            if self.score_3_4 and self.save_3:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '3.jpg', self.device_start_stop_5_img)
                else:
                    self.assignScore(
                        index=3,
                        img=self.device_start_stop_5_img.copy(),
                        object=self.device_start_stop_5_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_5_img_time[1],
                        num_frame=self.device_start_stop_5_img_time[2],
                        name_save="3.jpg",
                        preds=self.device_start_stop_5_img_time[3])
                # self.assignScore(3, self.device_start_stop_5_img, self.device_start_stop_5_img_time)
                self.save_3 = False
                self.start_6_7 = True
            elif self.score_3_6 and self.save_3:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '3.jpg', self.device_start_stop_6_img)
                else:
                    self.assignScore(
                        index=3,
                        img=self.device_start_stop_6_img.copy(),
                        object=self.device_start_stop_6_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_6_img_time[1],
                        num_frame=self.device_start_stop_6_img_time[2],
                        name_save="3.jpg",
                        preds=self.device_start_stop_6_img_time[3])
                # self.assignScore(3, self.device_start_stop_6_img, self.device_start_stop_6_img_time)
            elif self.score_3_3 and self.device_start_stop_3 and self.save_3:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '3.jpg', self.device_start_stop_3_img)
                else:
                    self.assignScore(
                        index=3,
                        img=self.device_start_stop_3_img.copy(),
                        object=self.device_start_stop_3_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_3_img_time[1],
                        num_frame=self.device_start_stop_3_img_time[2],
                        name_save="3.jpg",
                        preds=self.device_start_stop_3_img_time[3])
                # self.assignScore(3, self.device_start_stop_3_img, self.device_start_stop_3_img_time)
            elif self.score_3_2 and self.device_start_stop_2 and self.save_3:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '3.jpg', self.device_start_stop_2_img)
                else:
                    self.assignScore(
                        index=3,
                        img=self.device_start_stop_2_img.copy(),
                        object=self.device_start_stop_2_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_2_img_time[1],
                        num_frame=self.device_start_stop_2_img_time[2],
                        name_save="3.jpg",
                        preds=self.device_start_stop_2_img_time[3])
                # self.assignScore(3, self.device_start_stop_2_img, self.device_start_stop_2_img_time)
            elif self.score_3_1 and self.device_start_stop_1 and self.save_3:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '3.jpg', self.device_start_stop_1_img)
                else:
                    self.assignScore(
                        index=3,
                        img=self.device_start_stop_1_img.copy(),
                        object=self.device_start_stop_1_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_1_img_time[1],
                        num_frame=self.device_start_stop_1_img_time[2],
                        name_save="3.jpg",
                        preds=self.device_start_stop_1_img_time[3])
                # self.assignScore(3, self.device_start_stop_1_img, self.device_start_stop_1_img_time)
            # 得分点4：铁夹夹在距试管口三分之一处
            if self.score_4_1 and self.save_4:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '4.jpg', self.device_start_stop_4_1_img)
                else:
                    self.assignScore(
                        index=4,
                        img=self.device_start_stop_4_1_img.copy(),
                        object=self.device_start_stop_4_1_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_4_1_img_time[1],
                        num_frame=self.device_start_stop_4_1_img_time[2],
                        name_save="4.jpg",
                        preds=self.device_start_stop_4_1_img_time[3])
                # self.assignScore(4, self.device_start_stop_4_1_img, self.device_start_stop_4_1_img_time)
                self.save_4 = False
                self.start_6_7 = True
            elif self.score_3_4 and self.save_4:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '4.jpg', self.device_start_stop_5_img)
                else:
                    self.assignScore(
                        index=4,
                        img=self.device_start_stop_5_img.copy(),
                        object=self.device_start_stop_5_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_5_img_time[1],
                        num_frame=self.device_start_stop_5_img_time[2],
                        name_save="4.jpg",
                        preds=self.device_start_stop_5_img_time[3])
                # self.assignScore(4, self.device_start_stop_5_img, self.device_start_stop_5_img_time)
            # 得分点5：试管口略向下倾斜
            if self.score_4_2 and self.save_5:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '5.jpg', self.device_start_stop_4_2_img)
                else:
                    self.assignScore(
                        index=5,
                        img=self.device_start_stop_4_2_img.copy(),
                        object=self.device_start_stop_4_2_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_4_2_img_time[1],
                        num_frame=self.device_start_stop_4_2_img_time[2],
                        name_save="5.jpg",
                        preds=self.device_start_stop_4_2_img_time[3])
                # self.assignScore(5, self.device_start_stop_4_2_img, self.device_start_stop_4_2_img_time)
                self.save_5 = False
                self.start_6_7 = True
            elif self.score_3_4 and self.save_5:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '5.jpg', self.device_start_stop_5_img)
                else:
                    self.assignScore(
                        index=5,
                        img=self.device_start_stop_5_img.copy(),
                        object=self.device_start_stop_5_img_time[0],
                        conf=0.1,
                        time_frame=self.device_start_stop_5_img_time[1],
                        num_frame=self.device_start_stop_5_img_time[2],
                        name_save="5.jpg",
                        preds=self.device_start_stop_5_img_time[3])
                # self.assignScore(5, self.device_start_stop_5_img, self.device_start_stop_5_img_time)
        # 得分点11：点燃酒精灯、先预热在集中加热试管
        if len(self.flame_add_burner_img) > 0:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '11.jpg', self.flame_add_burner_img)
            else:
                self.assignScore(
                    index=11,
                    img=self.flame_add_burner_img.copy(),
                    object=self.flame_add_burner_img_time[0],
                    conf=0.1,
                    time_frame=self.flame_add_burner_img_time[1],
                    num_frame=self.flame_add_burner_img_time[2],
                    name_save="11.jpg",
                    preds=self.flame_add_burner_img_time[3])
            # self.assignScore(11, self.flame_add_burner_img, time.time())
            # self.save_11 = False
            self.save_11_stop = False
            self.save_11_2 = False
        if len(self.lighter_and_flame_img) > 0 and self.save_11_2:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '11.jpg', self.lighter_and_flame_img)
            else:
                self.assignScore(
                    index=11,
                    img=self.lighter_and_flame_img.copy(),
                    object=self.lighter_and_flame_img_time[0],
                    conf=0.1,
                    time_frame=self.lighter_and_flame_img_time[1],
                    num_frame=self.lighter_and_flame_img_time[2],
                    name_save="11.jpg",
                    preds=self.lighter_and_flame_img_time[3])
            # self.assignScore(11, self.lighter_and_flame_img, time.time())
        elif len(self.flame_add_burner_img_2) > 0 and self.save_11_2:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '11.jpg', self.flame_add_burner_img_2)
            else:
                self.assignScore(
                    index=11,
                    img=self.flame_add_burner_img_2.copy(),
                    object=self.flame_add_burner_img_2_time[0],
                    conf=0.1,
                    time_frame=self.flame_add_burner_img_2_time[1],
                    num_frame=self.flame_add_burner_img_2_time[2],
                    name_save="11.jpg",
                    preds=self.flame_add_burner_img_2_time[3])
            # self.assignScore(11, self.flame_add_burner_img_2, time.time())
        if self.start_6_7:
            # 得分点6：集气瓶盛满水，盖上毛玻片（暂时默认）
            if self.score_6_2 and self.save_6:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '6.jpg', self.sink_stop_2_img)
                else:
                    self.assignScore(
                        index=6,
                        img=self.sink_stop_2_img.copy(),
                        object=self.sink_stop_2_img_time[0],
                        conf=0.1,
                        time_frame=self.sink_stop_2_img_time[1],
                        num_frame=self.sink_stop_2_img_time[2],
                        name_save="6.jpg",
                        preds=self.sink_stop_2_img_time[3])
                # self.assignScore(6, self.sink_stop_2_img, self.sink_stop_2_img_time)
                self.save_6 = False
            elif self.score_6_1 and self.save_6:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '6.jpg', self.sink_stop_1_img)
                else:
                    self.assignScore(
                        index=6,
                        img=self.sink_stop_1_img.copy(),
                        object=self.sink_stop_1_img_time[0],
                        conf=0.1,
                        time_frame=self.sink_stop_1_img_time[1],
                        num_frame=self.sink_stop_1_img_time[2],
                        name_save="6.jpg",
                        preds=self.sink_stop_1_img_time[3])
                # self.assignScore(6, self.sink_stop_1_img, self.sink_stop_1_img_time)
            elif self.score_7 and self.save_6:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '6.jpg', self.sink_stop_3_img)
                else:
                    self.assignScore(
                        index=6,
                        img=self.sink_stop_3_img.copy(),
                        object=self.sink_stop_3_img_time[0],
                        conf=0.1,
                        time_frame=self.sink_stop_3_img_time[1],
                        num_frame=self.sink_stop_3_img_time[2],
                        name_save="6.jpg",
                        preds=self.sink_stop_3_img_time[3])
                # self.assignScore(6, self.sink_stop_3_img, self.sink_stop_3_img_time)
            # 得分点7：将集气瓶倒置在水槽中（暂时默认）
            if self.score_7 and self.save_7:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '7.jpg', self.sink_stop_3_img)
                else:
                    self.assignScore(
                        index=7,
                        img=self.sink_stop_3_img.copy(),
                        object=self.sink_stop_3_img_time[0],
                        conf=0.1,
                        time_frame=self.sink_stop_3_img_time[1],
                        num_frame=self.sink_stop_3_img_time[2],
                        name_save="7.jpg",
                        preds=self.sink_stop_3_img_time[3])
                # self.assignScore(7, self.sink_stop_3_img, self.sink_stop_3_img_time)
                self.save_7 = False
            elif self.score_6_2 and self.save_7:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '7.jpg', self.sink_stop_2_img)
                else:
                    self.assignScore(
                        index=7,
                        img=self.sink_stop_2_img.copy(),
                        object=self.sink_stop_2_img_time[0],
                        conf=0.1,
                        time_frame=self.sink_stop_2_img_time[1],
                        num_frame=self.sink_stop_2_img_time[2],
                        name_save="7.jpg",
                        preds=self.sink_stop_2_img_time[3])
                # self.assignScore(7, self.sink_stop_2_img, self.sink_stop_2_img_time)
            elif self.score_6_1 and self.save_7:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '7.jpg', self.sink_stop_1_img)
                else:
                    self.assignScore(
                        index=7,
                        img=self.sink_stop_1_img.copy(),
                        object=self.sink_stop_1_img_time[0],
                        conf=0.1,
                        time_frame=self.sink_stop_1_img_time[1],
                        num_frame=self.sink_stop_1_img_time[2],
                        name_save="7.jpg",
                        preds=self.sink_stop_1_img_time[3])
                # self.assignScore(7, self.sink_stop_1_img, self.sink_stop_1_img_time)
            # 得分点12：将导管从水槽中取出，熄灭酒精灯
            if len(self.flame_close_img) > 0 and self.save_12:  # and not self.save_11_stop:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '12.jpg', self.flame_close_img)
                else:
                    self.assignScore(
                        index=12,
                        img=self.flame_close_img.copy(),
                        object=self.flame_close_img_time[0],
                        conf=0.1,
                        time_frame=self.flame_close_img_time[1],
                        num_frame=self.flame_close_img_time[2],
                        name_save="12.jpg",
                        preds=self.flame_close_img_time[3])
                # self.assignScore(12, self.flame_close_img, time.time())
                self.save_12 = False
                self.save_12_stop = False
            # 得分点8：拆卸装置，整理桌面
            if self.score_8:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '8.jpg', self.clear_stop_img)
                else:
                    self.assignScore(
                        index=8,
                        img=self.clear_stop_img.copy(),
                        object=self.clear_stop_img_time[0],
                        conf=0.1,
                        time_frame=self.clear_stop_img_time[1],
                        num_frame=self.clear_stop_img_time[2],
                        name_save="8.jpg",
                        preds=self.clear_stop_img_time[3])
                # self.assignScore(8, self.clear_stop_img, self.clear_stop_img_time)
                # self.save_8 = False
        if len(self.clear_stop_img) != 0:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '8.jpg', self.clear_stop_img)
            else:
                self.assignScore(
                    index=8,
                    img=self.clear_stop_img.copy(),
                    object=self.clear_stop_img_time[0],
                    conf=0.1,
                    time_frame=self.clear_stop_img_time[1],
                    num_frame=self.clear_stop_img_time[2],
                    name_save="8.jpg",
                    preds=self.clear_stop_img_time[3])
            # self.assignScore(8, self.clear_stop_img, self.clear_stop_img_time)

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        '''
        无药品版本：
            1、将导管伸入水中，用手捂试管或微热试管
            2、导管口有气泡（暂时不做）
            3、按由下往上、从左到右的顺序搭建装置
            4、铁夹夹在距试管口三分之一处
            5、试管口略向下倾斜
            6、集气瓶盛满水，盖上毛玻片（暂时默认）
            7、将集气瓶倒置在水槽中（暂时默认）
            8、拆卸装置，整理桌面
        有药品版本：
           1、将导管伸入水中，用手捂试管或微热试管
           2、取氯酸钾和二氧化锰（两者3：1比例）混合均匀
           3、用药匙或纸槽将药品送入到试管底部
           4、有下往上，从左至右组装仪器
           5、集气瓶盛满水倒放在水槽中
           6、点燃酒精灯、先预热在集中加热试管
           7、当导管口有连续气泡时，开始收集氧气（暂时不做）
           8、当集气瓶口有气泡逸出时。取出集气瓶，用毛玻璃片改好集气瓶，取出正放在桌面上
           9、将导管从水槽中取出，熄灭酒精灯
           10、整理桌面
        有药品和无药品两版本得分点融合：
            1、将导管伸入水中，用手捂试管或微热试管
            2、导管口有气泡（暂时不做）
            3、按由下往上、从左到右的顺序搭建装置
            4、铁夹夹在距试管口三分之一处
            5、试管口略向下倾斜
            6、集气瓶盛满水，盖上毛玻片（暂时默认）
            7、将集气瓶倒置在水槽中（暂时默认）
            8、拆卸装置，整理桌面

            9、取氯酸钾和二氧化锰（两者3：1比例）混合均匀
            10、用药匙或纸槽将药品送入到试管底部
            11、点燃酒精灯、先预热在集中加热试管
            12、将导管从水槽中取出，熄灭酒精灯
        '''
        top_img = img0s[0]
        top_det = det[0]
        top_key = result_key[0]
        front_img = img0s[1]
        front_det = det[1]
        front_key = result_key[1]
        # top_key,top_det,top_img,front_key,front_det,front_img,side_key,side_det,side_img = self.fun_get_img(img0s, det, re_key)
        if 's_hand_tube_water_sink' in top_key and 'l_rubber_tube' in top_key and 'l_hand' in top_key and 'l_sink' in top_key:
            self.fun_hold(top_img, top_det, top_key)
        ##################################################
        # 取氯酸钾和二氧化锰（两者3：1比例）混合均匀
        # 用药匙或纸槽将药品送入到试管底部
        # front
        if 'l_spoon' in front_key and 'l_tube' in front_key and 'l_hand' in front_key:
            self.fun2_add_drug(front_img, front_det, front_key)
            self.fun2_add_drug_2(front_img, front_det, front_key)
            self.fun2_drug_send_tube(front_img, front_det, front_key)
            self.fun2_drug_send_tube_2(front_img, front_det, front_key)
        # top
        if 'l_spoon' in top_key and 'l_tube' in top_key and 'l_hand' in top_key:
            if len(self.add_drug_img) == 0:
                self.fun_add_drug(top_img, top_det, top_key)
            if len(self.add_drug_img_2) == 0:
                self.fun_add_drug_2(top_img, top_det, top_key)
            if len(self.add_drug_img) == 0:
                self.fun_drug_send_tube(top_img, top_det, top_key)
            if len(self.add_drug_img_2) == 0:
                self.fun_drug_send_tube_2(top_img, top_det, top_key)

        ##################################################
        # 装置搭建
        bool_x = False
        if 's_burner_holder_tube' in top_key and 'l_hand' in top_key and (
                'l_burner_bottom' in top_key or 'l_burner' in top_key):
            if not bool_x and 'l_holder_bottom' in top_key:  # 支架底座
                bool_x = self.fun_device_zjdz(top_img, top_det, top_key)
            if not bool_x and 'l_burner' in top_key:  # 酒精灯
                bool_x = self.fun_device_jjd(top_img, top_det, top_key)
            if not bool_x and 'l_holder_bottom_knob' in top_key and 'l_holder_bottom' in top_key:  # 支架旋钮
                bool_x = self.fun_device_zjxn(top_img, top_det, top_key)
            if not bool_x and 'l_tube' in top_key and 'l_holder_clip' in top_key and 'l_tube_head' in top_key:
                bool_x = self.fun_device_sg_jz(top_img, top_det, top_key)
        # 整体装置都安装完毕
        if not bool_x and 'l_rubber_tube' in top_key and 'l_sink' in top_key:
            if not bool_x and 's_burner_holder_tube_sink_hand' in top_key:
                bool_x = self.fun_device_final_1(top_img, top_det, top_key)
            if not bool_x:
                bool_x = self.fun_device_final_2(top_img, top_det, top_key)
            if not bool_x and 's_burner_holder_tube' in top_key and 'l_holder_bottom' in top_key and 'l_hand' in top_key:
                bool_x = self.fun_device_final_3(top_img, top_det, top_key)
        ###################################################################
        # 打火器点火
        bool_flame = 's_burner_holder_tube' in top_key or 's_burner_holder_tube_sink' in top_key or 's_burner_holder_tube_sink_hand' in top_key
        if bool_flame and 'l_lighter' in top_key and 'l_hand' in top_key and 'l_burner' in top_key:
            self.fun_lighter_and_flame(top_img, top_det, top_key)
        # 试管在酒精灯上加热
        if 'l_flame' in front_key and 'l_tube_bottom' in front_key:
            self.fun2_flame_add_burner(front_img, front_det, front_key)
        if bool_flame and 'l_burner' in top_key and 'l_tube_bottom' in top_key:
            self.fun_flame_add_burner_2(top_img, top_det, top_key)
        ###################################################################
        # 集气瓶
        if self.start_6_7:
            if 'l_container' in top_key and 'l_coverglass' not in top_key and 'l_sink' in top_key and 'l_hand' in top_key:
                self.fun_sink_1(top_img, top_det, top_key)
            elif 'l_coverglass' in top_key and 'l_container' not in top_key and 'l_sink' in top_key and 'l_hand' in top_key:
                self.fun_sink_2(top_img, top_det, top_key)
            elif 'l_coverglass' in top_key and 'l_container' in top_key and 'l_sink' in top_key and 'l_hand' in top_key:
                self.fun_sink_3(top_img, top_det, top_key)

            ###################################################################
            # 熄灭酒精灯
            if 'l_burner' in front_key and 'l_lamp_cap' in front_key:
                self.fun2_flame_close(front_img, front_det, front_key)
            if 'l_burner' in top_key and 'l_lamp_cap' in top_key:
                self.fun_flame_close(top_img, top_det, top_key)
        ###################################################################
        # 整理桌面
        bool_8x = self.device_start_stop_1 or self.device_start_stop_2 or self.device_start_stop_3 or self.device_start_stop_4 or self.device_start_stop_5
        if self.save_6 and self.save_7 and bool_8x:
            if 'l_clear' in top_key:
                self.fun_clear(top_img, top_det, top_key)
            # if 'l_hand' in top_key and 'l_towel' in top_key:
            #     self.fun_clear_hand(top_img, top_det, top_key)
            # if 'l_tube' in top_key and 'l_tube_head' in top_key:
            #     self.fun_clear_2(top_img, top_det, top_key)
        if not self.save_11:
            self.fun2_clear(front_img, front_det, front_key)
        self.save_score_fun()

    def process_dict(self, d):
        sink_box = []
        for key in list(d.keys()):
            if len(d[key]) > 1 and 'l_hand' != key and 'l_container' != key:
                d[key].sort(key=self.sortlist, reverse=True)
                d[key] = [d[key][0]]
            if 'l_hand' == key:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    bbox = d[key][:1]
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
                else:
                    d[key] = d[key][:2]
            if 'l_sink' == key:
                sink_box = d[key][0][:4]
        if len(sink_box) > 0:
            c_x, c_y = (sink_box[0] + sink_box[2]) / 2, (sink_box[1] + sink_box[3]) / 2
            for key in d.keys():
                if 'l_container' == key:
                    dis_list = []
                    import math
                    for item in d[key]:
                        ci_x, ci_y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                        dis_list.append(math.sqrt(((ci_x - c_x) ** 2) + ((ci_y - c_y) ** 2)))
                    index = dis_list.index(min(dis_list, key=abs))
                    d[key] = [d[key][index]]
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
            names_label = ['l_tube_head',
                           'l_rubber_tube',
                           'l_hand',
                           'l_sink',
                           'l_burner',
                           'l_lamp_cap',
                           'l_container',
                           'l_coverglass',
                           'l_holder_bottom',
                           'l_holder_bottom_knob',
                           'l_holder_clip',
                           'l_tube',
                           'l_towel',
                           'l_save_tube',
                           'l_spoon',
                           'l_potassium_permanganate',
                           'l_sodium_chloride',
                           'l_matchbox',
                           'l_paper_slot',
                           'l_lighter',
                           'l_burner_bottom',
                           's_hand_tube_water_sink',
                           'l_tube_bottom',
                           's_burner_holder_tube',
                           'l_flame',
                           's_burner_holder_tube_sink',
                           's_burner_holder_tube_sink_hand',
                           'l_clear',
                           'l_burner_bottom_knob',
                           'l_spoon_chloride',
                           'l_spoon_permanganate',
                           'l_matches']
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
        '''
        该实验赋分逻辑里面，不画图，画图在逻辑里面画图
        '''
        num_frame = num_frame_top
        top_true = False
        result_preds = None
        time_process_start = time.time()
        if pred_top is not None and pred_top.shape[0]:
            top_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
            dict_ = self.process_(top_preds, objects_top)
            self.num_frame_ = num_frame_top
            self.preds_ = top_preds
            self.objects_ = objects_top
            self.time_ = time_top
            top_key = list(dict_.keys())
            front_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            dict_front = self.process_(front_preds, objects_front)
            self.num_frame_front = num_frame_front
            self.preds_front = front_preds
            self.objects_front = None
            self.time_front = time_front
            front_key = list(dict_front.keys())
            self.predict([frame_top, frame_front], [dict_, dict_front], [top_key, front_key])
            # self.plot(top_preds, frame_top)
            # self.plot(front_preds, frame_front)
            # frame_top = cv2.resize(frame_top, (640, 384))
            # frame_front = cv2.resize(frame_front, (640, 384))
            # cv2.imshow('11', frame_top)
            # cv2.imshow('22', frame_front)
            # cv2.waitKey(1)
        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=result_preds, front_preds=None, side_preds=None)