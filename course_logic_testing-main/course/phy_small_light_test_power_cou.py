from .comm import *
from .comm.course_base import ConfigModel
from aideModel.classModel.class_predict import ClassMobilenetv3
from PIL import Image


class PHY_small_light_test_power(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_small_light_test_power, self).__init__()

        self.re_init()
        self.label_class = ['light_non', 'metal_box_down', 'metal_box_up', 'light_dim', 'switch_on', 'light_bright',
                            'metal_box_upright', 'switch_off']
        self.classmodel = ClassMobilenetv3(
            'aideModel/classModel/class_model_weights/class_model_8_v1.0.pt',
            self.label_class)

    def re_init(self):
        # 电池
        self.b_neg = False
        self.b_pos = False
        self.power_con_img = []
        self.power_con_box = []
        self.power_stop = False
        # 电压表
        self.am_neg = False
        self.am_pos = False
        self.am_con_img = []
        self.am_con_box = []
        self.am_stop = False
        # 电压表
        self.vo_neg = False
        self.vo_pos = False
        self.vo_con_img = []
        self.vo_con_box = []
        self.vo_stop = False
        # 开关
        self.sw_neg = False
        self.sw_pos = False
        self.sw_con_img = []
        self.sw_con_box = []
        self.sw_stop = False
        # 灯座
        self.li_neg = False
        self.li_pos = False
        self.li_con_img = []
        self.li_con_box = []
        self.li_stop = False
        # 滑动变阻器
        self.rh_neg = False
        self.rh_pos = False
        self.rh_con_img = []
        self.rh_con_box = []
        self.rh_stop = False
        # 并联
        self.two_stop = False
        self.two_con_img = []
        self.two_con_img_2 = []
        # 亮灯：
        self.light_img = []
        self.lights_start = False
        # 正极进入，负极流出
        self.am_pos_in_neg_out_img = []
        self.vo_pos_in_neg_out_img = []
        self.am_big_or_small_img = []
        self.vo_big_or_small_img = []
        self.am_pos_in_neg_out_img_box = []
        self.vo_pos_in_neg_out_img_box = []
        self.am_big_or_small_img_box = []
        self.vo_big_or_small_img_box = []
        self.big_or_small_img_bak = []
        self.pos_in_neg_out_img_bak = []
        # 量程的选择
        self.big_or_small_img = []
        # 开关连线时断开
        self.sw_off_con_img = []
        self.sw_off_con_img_2 = []
        # 开关闭合
        self.switch_status_img = []
        # 清洁桌面
        self.clear_img = []

        # 滑块移动
        self.gleithretter_dis_img = []
        self.gleithretter_dis_img_bak = []
        self.dis_stop = False
        # 指针偏转
        self.pointer_ammeter_img = []
        self.pointer_voltmeter_img = []
        self.pointer_img_bak = []

        self.pointer_ammeter_img_box = []
        self.pointer_voltmeter_img_box = []
        # 得分点
        self.save_1 = False
        self.save_2 = False
        self.save_3 = False
        self.save_4 = False
        self.save_4_bak = False
        self.save_5 = False
        self.save_5_bak = False
        self.save_6 = False
        self.save_6_bak = False
        self.save_7 = False
        self.save_7_bak = False
        self.save_8 = False
        self.save_9 = False
        self.save_10 = False
        self.save_11 = False
        self.save_12 = False
        self.all_stop = False

        self.switch_sta_bool = False

        self.single_p = False
        self.single_s = False

        self.single_l = False
        self.single_r = False

        self.single_a = False
        self.single_v = False

        self.two_con_img_2_bool = False
        self.l_smi_img = []
        self.tmp = False
        self.light_start_bool = False
        # 不画图
        self.not_draw_img = False
        self.clear_start = False
        self.ll_th = 0.8
        self.light_threshold_box = []

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
                          (int(box[2]), int(box[3])), (0, 255, 255), 2)
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

    # 连接状态
    def power_con(self, img, det, result_key):
        power_box = det['power_source']
        power_red_box = det['wire_connection_red']
        power_black_box = det['wire_connection_black']
        draw_img = img.copy()
        B, bbox = self.fun(power_box, power_red_box, power_black_box, 0.1, 'power_source')
        if B:
            self.power_con_img = self.draw_box(draw_img, bbox, ['power'])
            self.power_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            return True
        return False

    def am_con(self, img, det, result_key):
        am_box = det['ammeter']
        power_red_box = det['wire_connection_red']
        power_black_box = det['wire_connection_black']
        draw_img = img.copy()
        B, bbox = self.fun(am_box, power_red_box, power_black_box, 0.5, '')
        if B:
            self.am_con_img = self.draw_box(draw_img, bbox, ['voltmeter'])
            self.am_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            return True
        else:
            return False

    def vo_con(self, img, det, result_key):
        vo_box = det['voltmeter']
        power_red_box = det['wire_connection_red']
        power_black_box = det['wire_connection_black']
        draw_img = img.copy()
        B, bbox = self.fun(vo_box, power_red_box, power_black_box, 0.5, '')
        if B:
            self.vo_con_img = self.draw_box(draw_img, bbox, ['voltmeter'])
            self.vo_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.two_stop = True
            return True
        else:
            return False

    def rheostat_con(self, img, det, result_key):
        rheostat_box = det['slide_rheostat']
        above_box = det['connect_above']
        following_box = det['connect_following']
        draw_img = img.copy()
        B, bbox = self.fun(rheostat_box, above_box, following_box, 0.5, '')
        if B:
            self.rh_con_img = self.draw_box(draw_img, bbox, ['rheostat'])
            self.rh_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def switch_con(self, img, det, result_key):
        if 'l' in result_key: return False
        if 'switch_on' in result_key:
            switch_box = det['switch_on']
        else:
            switch_box = det['switch_off']
        power_red_box = det['wire_connection_red']
        power_black_box = det['wire_connection_black']
        draw_img = img.copy()
        B, bbox = self.fun(switch_box, power_red_box, power_black_box, 0.5, '')
        if B:
            self.sw_con_img = self.draw_box(draw_img, bbox, ['switch'])
            self.sw_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.sw_off_con_img_2 = self.draw_box(img.copy(), switch_box, ['switch_off'])
            self.sw_off_con_img_2_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        if B and ('switch_off' in result_key or switch_box[0][-1] < 0.3):
            self.sw_off_con_img = self.draw_box(img.copy(), switch_box, ['switch_off'])
            self.sw_off_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        if B:
            return True
        else:
            return False

    def light_con(self, img, det, result_key):
        if 'light_non' in result_key:
            light_box = det['light_non']
        elif 'light_dim' in result_key:
            light_box = det['light_dim']
        elif 'fixed_resistor' in result_key:
            light_box = det['fixed_resistor']
        else:
            light_box = det['light_bright']
        power_red_box = det['wire_connection_red']
        power_black_box = det['wire_connection_black']
        draw_img = img.copy()
        if self.single_p and light_box[0][-1] > 0.85:
            self.light_start_bool = True
        B, bbox = self.fun(light_box, power_red_box, power_black_box, 0.5, '')
        if B:
            if len(self.l_smi_img) == 0 and not self.light_start_bool:
                x_c = int((light_box[0][0] + light_box[0][2]) / 2)
                y_c = int((light_box[0][1] + light_box[0][3]) / 2)
                self.l_smi_img = img[(y_c - 20):(y_c + 20), (x_c - 20):(x_c + 20)]
            self.li_con_img = self.draw_box(draw_img, bbox, ['light'])
            self.li_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            return True
        else:
            return False

    # 判断开关状态
    def switch_status(self, img, det, result_key):
        if 'switch_on' in result_key:
            switch_box = det['switch_on'][0]
        else:
            switch_box = det['switch_off'][0]
        draw_img = img.copy()
        self.switch_status_img = self.draw(draw_img, [switch_box], ['switch_on'])
        self.switch_status_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        self.switch_sta_bool = True
        return True

    # 正极流进负极流出，同时指针有偏转
    def am_pos_in_neg_out(self, img, det, result_key):
        am_box = det['ammeter']
        if 'min' in result_key:
            m_box = det['min']
        elif 'max' in result_key:
            m_box = det['max']
        else:
            m_box = []
        am_stop = False
        if len(m_box) != 0:
            for i in range(len(am_box)):
                for j in range(len(m_box)):
                    vo_pos_neg = len(self.vo_pos_in_neg_out_img_box) == 0 or (
                            len(self.vo_pos_in_neg_out_img_box) != 0 and self.iou(
                        self.vo_pos_in_neg_out_img_box[:4], am_box[i][:4]) < 0.5)
                    vo_rang = len(self.vo_big_or_small_img_box) == 0 or (
                            len(self.vo_big_or_small_img_box) != 0 and self.iou(self.vo_big_or_small_img_box[:4],
                                                                                m_box[j][:4]) < 0.5)
                    if vo_pos_neg and vo_rang:
                        if self.iou(am_box[i][:4], m_box[j][:4]) > 0:
                            self.am_pos_in_neg_out_img = self.draw(img.copy(), [am_box[i]], ['ammeter'])
                            self.am_pos_in_neg_out_img_box = am_box[i]
                            self.am_pos_in_neg_out_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                            self.am_big_or_small_img = self.draw(img.copy(), [m_box[j]], ['range'])
                            self.am_big_or_small_img_box = m_box[j]
                            self.am_big_or_small_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                            am_stop = True
                            break
                if am_stop:
                    break

    def vo_pos_in_neg_out(self, img, det, result_key):
        vo_box = det['voltmeter']
        if 'min' in result_key:
            m_box = det['min']
        elif 'max' in result_key:
            m_box = det['max']
        else:
            m_box = []
        vo_stop = False
        if len(m_box) != 0:
            for h in range(len(vo_box)):
                for k in range(len(m_box)):
                    vo_pos_neg = len(self.am_pos_in_neg_out_img_box) == 0 or (
                            len(self.am_pos_in_neg_out_img_box) != 0 and self.iou(
                        self.am_pos_in_neg_out_img_box[:4], vo_box[h][:4]) < 0.5)
                    vo_rang = len(self.am_big_or_small_img_box) == 0 or (
                            len(self.am_big_or_small_img_box) != 0 and self.iou(self.am_big_or_small_img_box[:4],
                                                                                m_box[h][:4]) < 0.5)
                    if vo_pos_neg and vo_rang:
                        if self.iou(vo_box[h][:4], m_box[k][:4]) > 0:
                            self.vo_pos_in_neg_out_img = self.draw(img.copy(), [vo_box[h]], ['voltmeter'])
                            self.vo_pos_in_neg_out_img_box = vo_box[h]
                            self.vo_pos_in_neg_out_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                            self.vo_big_or_small_img = self.draw(img.copy(), [m_box[k]], ['range'])
                            self.vo_big_or_small_img_box = m_box[k]
                            self.vo_big_or_small_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                            vo_stop = True
                            break
                if vo_stop:
                    break

    def pos_in_neg_out_bak(self, img, det, result_key):
        # cv2.imshow('a', img)
        box = det['ammeter'][0]
        self.big_or_small_img_bak = self.draw(img.copy(), [box], [''])
        self.big_or_small_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        # cv2.imshow('b', self.big_or_small_img_bak)
        # cv2.waitKey(0)
        self.pos_in_neg_out_img_bak = self.draw(img.copy(), [box], [''])
        self.pos_in_neg_out_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def am_pointer_move(self, img, det, result_key):
        if 'pointer_offset' in result_key:
            pointer_box = det['pointer_offset']
        elif 'pointer_zero' in result_key:
            pointer_box = det['pointer_zero']
        else:
            pointer_box = []
        ammeter_box = det['ammeter']
        if len(pointer_box) != 0:
            for i in range(len(pointer_box)):
                for j in range(len(ammeter_box)):
                    if len(self.pointer_voltmeter_img_box) == 0 or (
                            len(self.pointer_voltmeter_img_box) != 0 and self.iou(self.pointer_voltmeter_img_box[:4],
                                                                                  pointer_box[i][:4]) < 0.5):
                        if self.iou(ammeter_box[j][:4], pointer_box[i][:4]) > 0:
                            self.pointer_ammeter_img = self.draw(img.copy(), [pointer_box[i]], ['pointer'])
                            self.pointer_ammeter_img_box = pointer_box[i]
                            self.pointer_ammeter_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def vo_pointer_move(self, img, det, result_key):
        if 'pointer_offset' in result_key:
            pointer_box = det['pointer_offset']
        elif 'pointer_zero' in result_key:
            pointer_box = det['pointer_zero']
        else:
            pointer_box = []
        voltmeter_box = det['voltmeter']
        if len(pointer_box) != 0:
            for i in range(len(pointer_box)):
                for j in range(len(voltmeter_box)):
                    if len(self.pointer_ammeter_img_box) == 0 or (
                            len(self.pointer_ammeter_img_box) != 0 and self.iou(self.pointer_ammeter_img_box[:4],
                                                                                pointer_box[i][:4]) < 0.5):
                        if self.box_include(voltmeter_box[j][:4], pointer_box[i][:4]) > 0:
                            self.pointer_voltmeter_img = self.draw(img.copy(), [pointer_box[i]], ['pointer'])
                            self.pointer_voltmeter_img_box = pointer_box[i]
                            self.pointer_voltmeter_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def pointer_move_bak(self, img, det, result_key):
        box = det['ammeter'][0]
        self.pointer_img_bak = self.draw(img.copy(), [box], [''])
        self.pointer_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    # 判断是不是并联
    def two_con(self, img, det, result_key):
        if 'light_non' in result_key:
            light_box = det['light_non']
        elif 'light_dim' in result_key:
            light_box = det['light_dim']
        elif 'fixed_resistor' in result_key:
            light_box = det['fixed_resistor']
        else:
            light_box = det['light_bright']

        con_box = det['wire_connection']
        vo_box = det['voltmeter']
        box = []
        for i in range(len(light_box)):
            for j in range(len(vo_box)):
                for k in range(len(con_box)):
                    l_c_v_iou = self.iou(light_box[i][:4], con_box[k][:4]) > 0 and self.iou(vo_box[j][:4],
                                                                                            con_box[k][:4]) > 0
                    if l_c_v_iou:
                        if len(box) == 0:
                            box = con_box[k]
                        else:
                            if self.iou(box[:4], con_box[k][:4]) < 0.5:
                                self.two_con_img = self.draw(img.copy(), [light_box[i][:4]], ['light'])
                                self.two_con_img = self.draw(self.two_con_img, [vo_box[j][:4]], ['voltmeter'])
                                self.two_stop = True
                                self.two_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                                break
                if self.two_stop:
                    break
            if self.two_stop:
                break

    def two_con_2(self, img, det, result_key):
        if 'light_non' in result_key:
            light_box = det['light_non']
        elif 'light_dim' in result_key:
            light_box = det['light_dim']
        elif 'fixed_resistor' in result_key:
            light_box = det['fixed_resistor']
        else:
            light_box = det['light_bright']
        w_red_box = det['wire_connection_red']
        w_black_box = det['wire_connection_black']
        con_box = det['wire_connection']
        vo_box = det['voltmeter']
        B, bbox = self.fun(vo_box, w_red_box, w_black_box, 0.5, '')
        if not B: return
        box = []
        for i in range(len(light_box)):
            for j in range(len(vo_box)):
                for k in range(len(con_box)):
                    l_c_v_iou = self.iou(light_box[i][:4], con_box[k][:4]) > 0 and self.iou(vo_box[j][:4],
                                                                                            con_box[k][:4]) > 0
                    l_c_v_iou_2 = self.iou(vo_box[j][:4], con_box[k][:4]) > 0
                    if l_c_v_iou:
                        if len(box) == 0:
                            box = con_box[k]
                        else:
                            if self.iou(box[:4], con_box[k][:4]) < 0.5:
                                self.two_con_img = self.draw(img.copy(), [light_box[i][:4]], ['light'])
                                self.two_con_img = self.draw(self.two_con_img, [vo_box[j][:4]], ['voltmeter'])
                                self.two_stop = True
                                self.two_con_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                                break
                    if l_c_v_iou_2:
                        self.two_con_img_2 = self.draw(img.copy(), [light_box[i][:4]], ['light'])
                        self.two_con_img_2 = self.draw(self.two_con_img_2, [vo_box[j][:4]], ['voltmeter'])
                        self.two_con_img_2_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                        self.two_stop = True
            #     if self.two_stop:
            #         break
            # if self.two_stop:
            #     break

    # 判断灯泡是否亮灯
    def light(self, img, det, result_key):
        l_box = det['l'][0]
        draw_img = img.copy()
        if 'light_non' in result_key:
            box = det['light_non'][0]
        elif 'light_dim' in result_key:
            box = det['light_dim'][0]
        else:
            box = det['light_bright'][0]
        tem_img = img[int(l_box[1]):int(l_box[3]), int(l_box[0]):int(l_box[2])]
        if self.box_include(box[:4], l_box[:4]) and self.sim_fun(tem_img):
            self.lights_start = True
            self.light_img = self.draw(draw_img, [l_box], ['l'])

        # 计算直方图

    def hist_similar(self, lh, rh):
        assert len(lh) == len(rh)
        hist = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)
        return hist

        # 计算相似度

    def calc_similar(self, li, ri):
        calc_sim = self.hist_similar(li.histogram(), ri.histogram())
        # print('calc_sim:', calc_sim)
        return calc_sim

    def sim_fun(self, img1, img2):
        img1 = Image.fromarray(cv2.cvtColor(cv2.resize(img1, (64, 64)), cv2.COLOR_BGR2RGB))
        img2 = Image.fromarray(cv2.cvtColor(cv2.resize(img2, (64, 64)), cv2.COLOR_BGR2RGB))
        # from glob import glob
        # imgs = glob('/home/xd/mnt5/wqg/vm_share/给出去的标注数据/物理/电学/小灯泡测功率/原视频/img_mp4/ii/light_tmp/*.jpg')
        # for file in imgs:
        #     img = cv2.imread(file)
        #     img1 = Image.fromarray(cv2.cvtColor(cv2.resize(img, (64, 64)), cv2.COLOR_BGR2RGB))
        smi_value = self.calc_similar(img1, img2)
        if smi_value > 0.45:
            return False
        return True

    def light_2(self, img, det, result_key):
        l_box = det['l'][0]
        if l_box[-1] < 0.5:
            x_c = int((l_box[0] + l_box[2]) / 2)
            y_c = int((l_box[1] + l_box[3]) / 2)
            self.l_smi_img = img[(y_c - 20):(y_c + 20), (x_c - 20):(x_c + 20)]
            return False
        if 'light_non' in result_key:
            box = det['light_non'][0]
        elif 'light_dim' in result_key:
            box = det['light_dim'][0]
        else:
            box = det['light_bright'][0]
        x_c = int((box[0] + box[2]) / 2)
        y_c = int((box[1] + box[3]) / 2)
        tem_img = img[(y_c - 20):(y_c + 20), (x_c - 20):(x_c + 20)]
        if len(self.l_smi_img) != 0:
            T = self.sim_fun(self.l_smi_img, tem_img)
        else:
            T = False
            self.l_smi_img = tem_img
        # cv2.imshow('a',self.l_smi_img)
        # cv2.imshow('b', tem_img)
        # cv2.waitKey(1)
        if T and self.box_include(box[:4], l_box[:4]) and l_box[-1] > self.ll_th:
            self.lights_start = True
            self.light_img = self.draw(img.copy(), [l_box], ['l'])
            return True
        else:
            self.lights_start = False
            return False

    def light_3(self, img, det, result_key):
        l_box = det['l'][0]
        box = det['light_bright'][0]
        if (self.box_include(box[:4], l_box[:4]) and l_box[-1] > 0.6) or l_box[-1] > self.ll_th:
            self.lights_start = True
            self.light_img = self.draw(img.copy(), [l_box], ['l'])
            return True
        else:
            return False

    def light_threshold(self, img, det, result_key):
        if 'light_non' in result_key:
            box = det['light_non'][0]
        elif 'light_dim' in result_key:
            box = det['light_dim'][0]
        else:
            box = det['light_bright'][0]
        x1, y1, x2, y2 = np.array(box[:4]).astype(int)
        img_ = img[y1:y2, x1:x2]
        resluts = []
        area_max = 0
        img__ = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(img__, 220, 255, cv2.THRESH_BINARY)
        kernel_1 = np.ones((7, 7), np.uint8)
        kernel_2 = np.ones((11, 11), np.uint8)
        ## c.图像的腐蚀，默认迭代次数
        erosion = cv2.erode(thresh1, kernel_1)
        ## 图像的膨胀
        dst = cv2.dilate(erosion, kernel_2)
        contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > area_max:  # 取面积最大
                area_max = area
                x, y, w, h = cv2.boundingRect(contours[i])
                x1_, y1_, x2_, y2_ = int(x), int(y), int(x + w), int(y + h)
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                resluts = [x1 + x1_, y1 + y1_, x1 + x2_, y1 + y2_]  # 还原到原图上
                self.light_threshold_box = resluts
        if len(resluts) > 0:
            # cv2.rectangle(img, (resluts[0], resluts[1]), (resluts[2], resluts[3]), (0, 0, 255), 2)
            # cv2.imshow('ll', img)
            # cv2.waitKey(0)
            self.lights_start = True
            self.light_img = self.draw(img.copy(), [resluts], ['l'])
            return True
        else:
            return False

    def light_class(self, img, det, result_key):
        if self.class_label_init['light_bright'] > 0.95:
            self.lights_start = True
            self.light_img = img
            # cv2.imshow('class_img',img)
            # cv2.waitKey(1)
            return True

    # 判断是不是在整理桌面
    def clear(self, img, det, result_key):
        clean_box = det['clean_desk'][0]
        draw_img = img.copy()
        self.clear_img = self.draw(draw_img, [clean_box], ['clean'])
        self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def clear_2(self, img, det, result_key):
        self.clear_img = img.copy()
        self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    # 判断是不是链接导线正确的公共函数
    def fun(self, box1, box2, box3, th, box1_name):
        pos_bool = False
        neg_bool = False
        re_box = []
        zj_box = []
        if not pos_bool:
            for i in range(len(box1)):
                for j in range(len(box2)):
                    vo_r_iou = self.iou(box1[i][:4], box2[j][:4]) > 0
                    if vo_r_iou:
                        if len(zj_box) == 0:
                            zj_box.append(box2[j])
                            if 'power_source' == box1_name:
                                re_box.append(box1[i])
                            pos_bool = True
                        else:
                            if self.iou(zj_box[0][:4], box2[j][:4]) < th:
                                pos_bool = True
                                if len(re_box) == 0 and 'power_source' != box1_name:
                                    re_box.append(box1[i])
                                elif 'power_source' == box1_name and len(re_box) < 4:
                                    re_box.append(box1[i])
                                re_box.append(zj_box[0])
                                re_box.append(box2[j])
                                break
                if pos_bool:
                    break
        if not neg_bool:
            for h in range(len(box1)):
                for k in range(len(box3)):
                    vo_b_iou = self.iou(box1[h][:4], box3[k][:4]) > 0
                    if vo_b_iou:
                        if len(zj_box) == 0:
                            zj_box.append(box3[k])
                            if 'power_source' == box1_name:
                                re_box.append(box1[i])
                            neg_bool = True
                        else:
                            if self.iou(zj_box[0][:4], box3[k][:4]) < th:
                                neg_bool = True
                                if len(re_box) == 0 and 'power_source' != box1_name:
                                    re_box.append(box1[h])
                                elif 'power_source' == box1_name and len(re_box) < 4:
                                    re_box.append(box1[h])
                                re_box.append(zj_box[0])
                                re_box.append(box3[k])
                                break
                if neg_bool:
                    break
        if pos_bool and neg_bool:
            return True, re_box
        else:
            return False, []

    # 多张图片拼接在一起
    def con_img(self, imgs, save_img):
        index = np.where(save_img)[0]
        if 0 < len(index) <= 6:
            if len(index) == 2:
                res = np.hstack([imgs[index[0]], imgs[index[1]]])
                res = cv2.resize(res, (self.ww, self.hh))
                if len(imgs) == 2:
                    return res, True
                else:
                    return res, False
            elif len(index) == 3:
                res1 = np.hstack([imgs[index[0]], imgs[index[1]]])
                res1 = cv2.resize(res1, (self.ww, self.hh))
                res = np.vstack([res1, imgs[index[2]]])
                res = cv2.resize(res, (self.ww, self.hh))
                if len(imgs) == 3:
                    return res, True
                else:
                    return res, False
            elif len(index) == 4:
                res_h_1 = np.hstack([imgs[index[0]], imgs[index[1]]])
                res_h_2 = np.hstack([imgs[index[2]], imgs[index[3]]])
                res = np.vstack([res_h_1, res_h_2])
                res = cv2.resize(res, (self.ww, self.hh))
                if len(imgs) == 4:
                    return res, True
                else:
                    return res, False
            elif len(index) == 5:
                res1 = np.hstack([imgs[index[0]], imgs[index[1]], imgs[index[2]]])
                res1 = cv2.resize(res1, (self.ww, self.hh))
                res2 = np.hstack([imgs[index[3]], imgs[index[4]]])
                res2 = cv2.resize(res2, (self.ww, self.hh))
                res3 = np.vstack([res1, res2])
                res = cv2.resize(res3, (self.ww, self.hh))
                if len(imgs) == 5:
                    return res, True
                else:
                    return res, False
            elif len(index) == 6:
                res1 = np.hstack([imgs[index[0]], imgs[index[1]], imgs[index[2]]])
                res1 = cv2.resize(res1, (self.ww, self.hh))
                res2 = np.hstack([imgs[index[3]], imgs[index[4]], imgs[index[5]]])
                res2 = cv2.resize(res2, (self.ww, self.hh))
                res3 = np.vstack([res1, res2])
                res = cv2.resize(res3, (self.ww, self.hh))
                if len(imgs) == 6:
                    return res, True
                else:
                    return res, False
            else:
                res = imgs[index[0]]
                return res, False
        else:
            return [], False

    # 判断滑块是否有移动
    def gleithretter_dis(self, img, det, result_key):
        if not self.dis_stop:
            rheostat_box = det['slide_rheostat']
            # gleithretter_box = det['gleithretter']
            # b_bool = False
            # for h in range(len(rheostat_box)):
            #     for k in range(len(gleithretter_box)):
            #         if self.iou(rheostat_box[h][:4], gleithretter_box[k][:4]) > 0:
            #             self.gleithretter_dis_img = self.draw_box(img.copy(), [gleithretter_box[k]], ['gleithretter'])
            # if b_bool:
            if 'connect_above' in result_key and 'connect_following' not in result_key:
                box_bool = len(det['connect_above']) == 2
                box = det['connect_above']
            elif 'connect_above' not in result_key and 'connect_following' in result_key:
                box_bool = len(det['connect_following']) == 2
                box = det['connect_following']
            else:
                box_bool = False
                box = []
            if box_bool:
                w = abs(box[0][0] - box[0][2])
                if self.iou(box[0][:4], box[1][:4]) == 0 and self.dis_point(box[0], box[1]) > 2 * w and self.iou(
                        rheostat_box[0][:4], box[0][:4]) > 0 and self.iou(rheostat_box[0][:4], box[1][:4]) > 0:
                    self.gleithretter_dis_img = self.draw_1(img.copy(), [box[0], box[1]], ['', ''])
                    self.gleithretter_dis_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.dis_stop = True
                    return

    def gleithretter_dis_bak(self, img, det, result_key):
        if 'slide_rheostat' in result_key:
            box = det['slide_rheostat']
        else:
            box = det['gleithretter']
        self.gleithretter_dis_img_bak = self.draw_box(img.copy(), [box[0]], ['gleithretter'])
        self.gleithretter_dis_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        return

    def draw_box(self, draw_img, box, lab):
        # assert len(box)==len(lab)
        if not self.not_draw_img:
            self.plot(self.results, draw_img)
            return draw_img
        for i in range(len(box)):
            draw_img = self.draw(draw_img, [box[i]], [lab[0]])
        return draw_img

    def save_score_fun(self):
        # 保存整理桌面
        if len(self.clear_img) != 0 and not self.save_8:
            self.assignScore(
                index=8,
                img=self.clear_img.copy(),
                object=self.clear_img_list[0],
                conf=0.1,
                time_frame=self.clear_img_list[1],
                num_frame=self.clear_img_list[2],
                name_save="8.jpg",
                preds=self.clear_img_list[3])
            self.save_8 = True
        if not self.all_stop:
            # 得分点1#电路串联
            imgs_1 = [self.power_con_img, self.am_con_img, self.vo_con_img, self.sw_con_img, self.li_con_img,
                      self.rh_con_img]
            save_img_1 = [len(self.power_con_img) != 0, len(self.am_con_img) != 0, len(self.vo_con_img) != 0,
                          len(self.sw_con_img) != 0, len(self.li_con_img) != 0, len(self.rh_con_img) != 0]
            saveimg_1, saveimg_stop_1 = self.con_img(imgs_1, save_img_1)
            if len(saveimg_1) > 0 and not self.save_1:
                if len(self.power_con_img) != 0:
                    self.assignScore(
                        index=1,
                        img=self.power_con_img.copy(),
                        object=self.power_con_img_list[0],
                        conf=0.1,
                        time_frame=self.power_con_img_list[1],
                        num_frame=self.power_con_img_list[2],
                        name_save="1.jpg",
                        preds=self.power_con_img_list[3])
                elif len(self.am_con_img) != 0:
                    self.assignScore(
                        index=1,
                        img=self.am_con_img.copy(),
                        object=self.am_con_img_list[0],
                        conf=0.1,
                        time_frame=self.am_con_img_list[1],
                        num_frame=self.am_con_img_list[2],
                        name_save="1.jpg",
                        preds=self.am_con_img_list[3])
                elif len(self.sw_con_img) != 0:
                    self.assignScore(
                        index=1,
                        img=self.sw_con_img.copy(),
                        object=self.sw_con_img_list[0],
                        conf=0.1,
                        time_frame=self.sw_con_img_list[1],
                        num_frame=self.sw_con_img_list[2],
                        name_save="1.jpg",
                        preds=self.sw_con_img_list[3])
                else:
                    self.assignScore(
                        index=1,
                        img=saveimg_1.copy(),
                        object=None,
                        conf=0.1,
                        time_frame=self.time_,
                        num_frame=self.num_frame_,
                        name_save="1.jpg",
                        preds=None)
                if saveimg_stop_1:
                    self.save_1 = True
            # 得分点2：电压表并联
            if not self.save_2:
                if len(self.two_con_img) != 0:
                    self.assignScore(
                        index=2,
                        img=self.two_con_img.copy(),
                        object=self.two_con_img_list[0],
                        conf=0.1,
                        time_frame=self.two_con_img_list[1],
                        num_frame=self.two_con_img_list[2],
                        name_save="2.jpg",
                        preds=self.two_con_img_list[3])
                    self.save_2 = True
                elif len(self.two_con_img_2) != 0 and not self.lights_start:
                    self.assignScore(
                        index=2,
                        img=self.two_con_img_2.copy(),
                        object=self.two_con_img_2_list[0],
                        conf=0.1,
                        time_frame=self.two_con_img_2_list[1],
                        num_frame=self.two_con_img_2_list[2],
                        name_save="2.jpg",
                        preds=self.two_con_img_2_list[3])
            # 得分点3：链接电路市，开关属于断开状态
            if len(self.sw_off_con_img) != 0 and not self.save_3:
                self.assignScore(
                    index=3,
                    img=self.sw_off_con_img.copy(),
                    object=self.sw_off_con_img_list[0],
                    conf=0.1,
                    time_frame=self.sw_off_con_img_list[1],
                    num_frame=self.sw_off_con_img_list[2],
                    name_save="3.jpg",
                    preds=self.sw_off_con_img_list[3])
                self.save_3 = True
            elif len(self.sw_off_con_img_2) != 0 and len(self.sw_off_con_img) == 0:
                self.assignScore(
                    index=3,
                    img=self.sw_off_con_img_2.copy(),
                    object=self.sw_off_con_img_2_list[0],
                    conf=0.1,
                    time_frame=self.sw_off_con_img_2_list[1],
                    num_frame=self.sw_off_con_img_2_list[2],
                    name_save="3.jpg",
                    preds=self.sw_off_con_img_2_list[3])
            # 得分点4：电流表正极流入，负极流出，电压表同理
            imgs_4 = [self.am_pos_in_neg_out_img, self.vo_pos_in_neg_out_img]
            save_img_4 = [len(self.am_pos_in_neg_out_img) != 0, len(self.vo_pos_in_neg_out_img) != 0]
            # saveimg_4, saveimg_stop_4 = [],False
            saveimg_4, saveimg_stop_4 = self.con_img(imgs_4, save_img_4)
            if len(saveimg_4) > 0 and not self.save_4:
                if len(self.am_pos_in_neg_out_img) != 0:
                    self.assignScore(
                        index=4,
                        img=self.am_pos_in_neg_out_img.copy(),
                        object=self.am_pos_in_neg_out_img_list[0],
                        conf=0.1,
                        time_frame=self.am_pos_in_neg_out_img_list[1],
                        num_frame=self.am_pos_in_neg_out_img_list[2],
                        name_save="4.jpg",
                        preds=self.am_pos_in_neg_out_img_list[3])
                elif len(self.vo_pos_in_neg_out_img) != 0:
                    self.assignScore(
                        index=4,
                        img=self.vo_pos_in_neg_out_img.copy(),
                        object=self.vo_pos_in_neg_out_img_list[0],
                        conf=0.1,
                        time_frame=self.vo_pos_in_neg_out_img_list[1],
                        num_frame=self.vo_pos_in_neg_out_img_list[2],
                        name_save="4.jpg",
                        preds=self.vo_pos_in_neg_out_img_list[3])
                else:
                    self.assignScore(
                        index=4,
                        img=saveimg_4.copy(),
                        object=None,
                        conf=0.1,
                        time_frame=self.time_,
                        num_frame=self.num_frame_,
                        name_save="4.jpg",
                        preds=None)
                if saveimg_stop_4:
                    self.save_4 = True
            # 得分点4备份
            if len(self.pos_in_neg_out_img_bak) != 0 and len(
                    saveimg_4) == 0 and not self.save_4 and not self.save_4_bak:  # todo
                self.assignScore(
                    index=4,
                    img=self.pos_in_neg_out_img_bak.copy(),
                    object=self.pos_in_neg_out_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.pos_in_neg_out_img_bak_list[1],
                    num_frame=self.pos_in_neg_out_img_bak_list[2],
                    name_save="4.jpg",
                    preds=self.pos_in_neg_out_img_bak_list[3])
                self.save_4_bak = True
            # 得分点5：变阻器链接一上一下，滑块最大一端，电阻最大
            if len(self.gleithretter_dis_img) != 0 and not self.save_5:
                self.assignScore(
                    index=5,
                    img=self.gleithretter_dis_img.copy(),
                    object=self.gleithretter_dis_img_list[0],
                    conf=0.1,
                    time_frame=self.gleithretter_dis_img_list[1],
                    num_frame=self.gleithretter_dis_img_list[2],
                    name_save="5.jpg",
                    preds=self.gleithretter_dis_img_list[3])
                if self.dis_stop:
                    self.save_5 = True
            if len(self.gleithretter_dis_img_bak) != 0 and not self.save_5 and not self.save_5_bak:
                self.assignScore(
                    index=5,
                    img=self.gleithretter_dis_img_bak.copy(),
                    object=self.gleithretter_dis_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.gleithretter_dis_img_bak_list[1],
                    num_frame=self.gleithretter_dis_img_bak_list[2],
                    name_save="5.jpg",
                    preds=self.gleithretter_dis_img_bak_list[3])
                self.save_5_bak = True
            # 得分点6：开关闭合，电流表，电压表发生偏转
            imgs_6 = [self.pointer_ammeter_img, self.pointer_voltmeter_img]
            save_img_6 = [len(self.pointer_ammeter_img) != 0, len(self.pointer_voltmeter_img) != 0]
            # saveimg_6, saveimg_stop_6 = [], False
            saveimg_6, saveimg_stop_6 = self.con_img(imgs_6, save_img_6)
            if len(saveimg_6) > 0 and not self.save_6:
                if len(self.pointer_ammeter_img) != 0:
                    self.assignScore(
                        index=6,
                        img=self.pointer_ammeter_img.copy(),
                        object=self.pointer_ammeter_img_list[0],
                        conf=0.1,
                        time_frame=self.pointer_ammeter_img_list[1],
                        num_frame=self.pointer_ammeter_img_list[2],
                        name_save="6.jpg",
                        preds=self.pointer_ammeter_img_list[3])
                elif len(self.pointer_voltmeter_img) != 0:
                    self.assignScore(
                        index=6,
                        img=self.pointer_voltmeter_img.copy(),
                        object=self.pointer_voltmeter_img_list[0],
                        conf=0.1,
                        time_frame=self.pointer_voltmeter_img_list[1],
                        num_frame=self.pointer_voltmeter_img_list[2],
                        name_save="6.jpg",
                        preds=self.pointer_voltmeter_img_list[3])
                else:
                    self.assignScore(
                        index=6,
                        img=saveimg_6.copy(),
                        object=None,
                        conf=0.1,
                        time_frame=self.time_,
                        num_frame=self.num_frame_,
                        name_save="6.jpg",
                        preds=None)
                if saveimg_stop_6:
                    self.save_6 = True
            if len(self.pointer_img_bak) != 0 and len(
                    saveimg_6) == 0 and not self.save_6 and not self.save_6_bak:  # todo
                self.assignScore(
                    index=6,
                    img=self.pointer_img_bak.copy(),
                    object=self.pointer_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.pointer_img_bak_list[1],
                    num_frame=self.pointer_img_bak_list[2],
                    name_save="6.jpg",
                    preds=self.pointer_img_bak_list[3])
                self.save_6_bak = True
            # 得分点7：电流表电压表选择合适的量程
            imgs_7 = [self.am_big_or_small_img, self.vo_big_or_small_img]
            save_img_7 = [len(self.am_big_or_small_img) != 0, len(self.vo_big_or_small_img) != 0]
            # saveimg_7, saveimg_stop_7 = [],False
            saveimg_7, saveimg_stop_7 = self.con_img(imgs_7, save_img_7)
            if len(saveimg_7) > 0 and not self.save_7:
                if len(self.am_big_or_small_img) != 0:
                    self.assignScore(
                        index=7,
                        img=self.am_big_or_small_img.copy(),
                        object=self.am_big_or_small_img_list[0],
                        conf=0.1,
                        time_frame=self.am_big_or_small_img_list[1],
                        num_frame=self.am_big_or_small_img_list[2],
                        name_save="7.jpg",
                        preds=self.am_big_or_small_img_list[3])
                elif len(self.vo_big_or_small_img) != 0:
                    self.assignScore(
                        index=7,
                        img=self.vo_big_or_small_img.copy(),
                        object=self.vo_big_or_small_img_list[0],
                        conf=0.1,
                        time_frame=self.vo_big_or_small_img_list[1],
                        num_frame=self.vo_big_or_small_img_list[2],
                        name_save="7.jpg",
                        preds=self.vo_big_or_small_img_list[3])
                else:
                    self.assignScore(
                        index=7,
                        img=saveimg_7.copy(),
                        object=None,
                        conf=0.1,
                        time_frame=self.time_,
                        num_frame=self.num_frame_,
                        name_save="7.jpg",
                        preds=None)
                if saveimg_stop_7:
                    self.save_7 = True
            # 得分点7备份
            if len(self.big_or_small_img_bak) != 0 and len(
                    saveimg_7) == 0 and not self.save_7 and not self.save_7_bak:  # todo
                self.assignScore(
                    index=7,
                    img=self.big_or_small_img_bak.copy(),
                    object=self.big_or_small_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.big_or_small_img_bak_list[1],
                    num_frame=self.big_or_small_img_bak_list[2],
                    name_save="7.jpg",
                    preds=self.big_or_small_img_bak_list[3])
                self.save_7_bak = True

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        # if len(self.l_smi_img)!=0:
        #     cv2.imshow('a_1',self.l_smi_img)
        #     cv2.waitKey(1)
        ##################################################################################################
        # 判断每个器件是否接线正常，共六个器件
        self.class_model_(img0s, det, result_key)
        if 'wire_connection_red' in result_key and 'wire_connection_black' in result_key:
            if 'power_source' in result_key:
                self.single_p = self.power_con(img0s.copy(), det, result_key)
            if 'ammeter' in result_key:
                self.single_a = self.am_con(img0s.copy(), det, result_key)
            if 'voltmeter' in result_key:
                self.single_v = self.vo_con(img0s.copy(), det, result_key)
            if 'switch_on' in result_key or 'switch_off' in result_key:
                self.single_s = self.switch_con(img0s.copy(), det, result_key)
            if 'fixed_resistor' in result_key or 'light_non' in result_key or 'light_dim' in result_key or 'light_bright' in result_key:
                self.single_l = self.light_con(img0s.copy(), det, result_key)
                ##################################################################################################
                # 判断是不是并联
                if self.single_l and self.single_v and 'voltmeter' in result_key and 'wire_connection' in result_key:
                    self.two_con(img0s.copy(), det, result_key)
                    self.two_con_2(img0s.copy(), det, result_key)
        else:
            self.single_p = False
            self.single_a = False
            self.single_v = False
            self.single_s = False
            self.single_p = False
            self.single_l = False
        if 'slide_rheostat' in result_key and 'connect_above' in result_key and 'connect_following' in result_key:
            self.single_r = self.rheostat_con(img0s.copy(), det, result_key)
        ##################################################################################################
        if self.two_stop:
            # 判断开关是否闭合的同时，判断小灯泡是否被点亮
            light_2_bool = False
            if 'light_non' in result_key or 'light_dim' in result_key or 'light_bright' in result_key:
                light_2_bool = self.light_class(img0s.copy(), det, result_key)
            if not light_2_bool and 'light_non' in result_key or 'light_dim' in result_key or 'light_bright' in result_key:
                light_2_bool = self.light_threshold(img0s.copy(), det, result_key)
            # if not light_2_bool and 'l' in result_key and 'light_bright' in result_key:
            #     light_2_bool = self.light_3(img0s.copy(), det, result_key)
            # if not light_2_bool and 'l' in result_key and (
            #         'light_non' in result_key or 'light_dim' in result_key or 'light_bright' in result_key):
            #     light_2_bool = self.light_2(img0s.copy(), det, result_key)
            if light_2_bool and ((
                                         self.single_p and self.single_a and self.single_v and self.single_l and self.single_s) or self.lights_start):
                self.clear_start = True
                if 'switch_on' in result_key:
                    self.switch_status(img0s.copy(), det, result_key)
                    # if 'l' in result_key and (
                    #         'light_non' in result_key or 'light_dim' in result_key or 'light_bright' in result_key):
                    #     self.light(img0s.copy(), det, result_key)
                ##################################################################################################
                # 在亮灯情况下的一些：
                if self.lights_start and self.switch_sta_bool:
                    ##################################################################################################
                    # 移动滑块
                    if 'slide_rheostat' in result_key and 'gleithretter' in result_key and (
                            'connect_above' in result_key or 'connect_following' in result_key):
                        self.gleithretter_dis(img0s.copy(), det, result_key)
                    if 'slide_rheostat' in result_key or 'gleithretter' in result_key:
                        self.gleithretter_dis_bak(img0s.copy(), det, result_key)
                    ##################################################################################################
                    # 判断正负极流入流出、指针偏转
                    if ('pointer_offset' in result_key or 'pointer_zero' in result_key):
                        if 'ammeter' in result_key and len(self.pointer_ammeter_img) == 0 and self.single_a:
                            self.am_pointer_move(img0s.copy(), det, result_key)
                        if 'voltmeter' in result_key and len(self.pointer_voltmeter_img) == 0 and self.single_v:
                            self.vo_pointer_move(img0s.copy(), det, result_key)
                        if 'ammeter' in result_key and 'voltmeter' in result_key:
                            self.pointer_move_bak(img0s.copy(), det, result_key)

                    if 'ammeter' in result_key and self.single_v:
                        self.am_pos_in_neg_out(img0s.copy(), det, result_key)
                    if 'voltmeter' in result_key and self.single_v:
                        self.vo_pos_in_neg_out(img0s.copy(), det, result_key)
                    if 'ammeter' in result_key and 'voltmeter' in result_key:
                        self.pos_in_neg_out_bak(img0s.copy(), det, result_key)
            ##################################################################################################
            # 判断正负极流入流出、指针偏转
            if not self.single_p and (not self.single_a or not self.single_l or not self.single_s) and ((
                                                                                                                self.save_4 or self.save_5 or self.save_6 or self.save_7) or self.clear_start):
                if 'l' not in result_key and len(self.clear_img) == 0 and 'clean_desk' in result_key:
                    self.clear(img0s.copy(), det, result_key)
                    if self.save_4 or self.save_5 or self.save_6 or self.save_7:
                        self.all_stop = True
                if 'l' not in result_key and len(self.clear_img) == 0 and (
                        'wire_connection_red' not in result_key and 'wire_connection_black' in result_key):
                    self.clear_2(img0s.copy(), det, result_key)
                    if self.save_4 or self.save_5 or self.save_6 or self.save_7:
                        self.all_stop = True
        self.save_score_fun()

    def class_model_(self, img0s, det, result_key):
        imgs_list = []
        self.class_label_init = {}
        for key in self.label_class:
            self.class_label_init[key] = 0
            if key in result_key:
                box = det[key][0]
                imgs_list.append(img0s[int(box[1]):int(box[3]), int(box[0]):int(box[2])])
        if len(imgs_list) > 0:
            pre = self.classmodel(imgs_list)
            for i in range(pre.shape[0]):
                ind = int(pre[i][1])
                self.class_label_init[self.label_class[ind]] = pre[i][0]

    def process_dict(self, d):
        for key in d.keys():
            if len(d[key]) > 1 and key in ['slide_rheostat', 'switch_on', 'switch_off', 'ammeter', 'light_non',
                                           'voltmeter', 'light_dim', 'l', 'light_bright']:
                d[key].sort(key=self.sortlist, reverse=True)
                d[key] = [d[key][0]]
            if 'power_source' == key:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    bbox = d[key][:1]
                    bbox.append([0, 0, 0, 0, 0])
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
                elif len(d[key]) == 2:
                    bbox = d[key][:2]
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
                else:
                    d[key] = d[key][:3]
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
            self.names_label = ['power_source',
                                'ammeter',
                                'slide_rheostat',
                                'gleithretter',
                                'wire_connection_red',
                                'wire_connection_black',
                                'connect_above',
                                'connect_following',
                                'wire_connection',
                                'min',
                                'pointer_offset',
                                'max',
                                'pointer_zero',
                                'switch_off',
                                'switch_on',
                                'clean_desk',
                                'wire_connection_binding_post',
                                'light_non',
                                'voltmeter',
                                'light_dim',
                                'l',
                                'light_bright']
            for i in range(len(pred)):
                if pred[i].shape[0] != 0:
                    key = self.names_label[int(pred[i][0][-1].item())]
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
            self.ww, self.hh = frame_top.shape[1], frame_top.shape[0]
            top_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
            dict_ = self.process_(top_preds, objects_top)
            self.num_frame_ = num_frame_top
            self.preds_ = top_preds
            self.objects_ = objects_top
            self.time_ = time_top
            self.predict(frame_top, dict_, list(dict_.keys()), top_preds, objects_top, time_front, num_frame_front)
            # self.plot(top_preds, frame_top)
            # cv2.imshow('a', frame_top)
            # cv2.waitKey(1)
        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=top_preds, front_preds=top_preds, side_preds=side_preds)
