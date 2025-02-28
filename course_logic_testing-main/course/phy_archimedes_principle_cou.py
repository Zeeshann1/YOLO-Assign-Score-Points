# from configg.sort_1 import Sort_
# Sort_ = lambda x:x
from .comm import *
from .comm.course_base import ConfigModel
from torchvision import transforms
from aideModel import ClassMobilenetv3
from PIL import Image


class PHY_archimedes_principle(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_archimedes_principle, self).__init__()
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

    ####################################################################################################################################
    def re_init(self):
        self.pour_water_img = []
        self.zero_img = []
        self.zero_img_bak = []
        self.measurement_stone_img = []
        self.measurement_stone_img_bak = []
        self.stone_water_img = []
        self.stone_water_img_bak = []
        # 清理桌面
        self.clear_bool = False
        self.clear_img = []
        self.clear_img_bak = []
        # 保存得分点
        self.save_1 = False
        self.save_2 = False
        self.save_2_bak = False
        self.save_3 = False
        self.save_3_bak = False
        self.save_4 = False
        self.save_4_bak = False
        self.save_5 = False
        self.save_5_bak = False
        self.save_6 = False

        self.stone_water_start = False
        self.stone_water_box = []
        self.desk_th = 0.2
        self.stone_water_th = 0.2

        self.not_draw_img = True
        self.water_bbox = []

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

    # 倒水
    def pour_water(self, img, det, result_key):
        surface_box = det['bottle_water_surface'][0]
        water_box = det['bottle_water'][0]
        surface_box_w = surface_box[2] - surface_box[0]
        water_box_h = water_box[3] - water_box[1]
        bool_1 = self.iou(surface_box[:4], water_box[:4]) > 0 and water_box_h > surface_box_w * 2
        if bool_1 and len(self.pour_water_img) == 0:
            self.water_bbox = water_box
            self.pour_water_img = self.draw(img.copy(), [surface_box, water_box],
                                            ['bottle_water_surface', 'bottle_water'])
            self.pour_water_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            # cv2.imshow('1',self.pour_water_img)
            # cv2.waitKey(0)

    # 调零
    def zero(self, img, det, result_key):
        hand_box = det['hand']
        eye_box = det['eye'][0]
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h < 3 * spring_box_w: return
        bottle_box = det['measuring_bottle'][0]
        spring_box_y_c = (spring_box[1] + spring_box[3]) / 2
        bottle_box_y_c = (bottle_box[1] + bottle_box[3]) / 2
        bool_1 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4], spring_box[
                                                                                             :4]) > 0 and spring_box_y_c < bottle_box_y_c
        bool_2 = spring_box[1] < eye_box[3] < spring_box[3]  # 眼睛和滑动变阻器保持一样高度
        if bool_1 and len(self.zero_img) == 0 and bool_2:
            self.zero_img = self.draw(img.copy(), [spring_box],
                                      ['spring_dynamometer'])
            self.zero_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            # cv2.imshow('2', self.zero_img)
            # cv2.waitKey(0)

    def zero_bak(self, img, det, result_key):
        hand_box = det['hand']
        water_box = det['bottle_water'][0]
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h < 3 * spring_box_w: return
        spring_box_y_c = (spring_box[1] + spring_box[3]) / 2
        bool_1 = (self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4],
                                                                             spring_box[
                                                                             :4]) > 0) and spring_box_y_c < \
                 water_box[1]
        if bool_1 and len(self.zero_img_bak) == 0:
            self.zero_img_bak = self.draw(img.copy(), [spring_box],
                                          ['spring_dynamometer'])
            self.zero_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    # 竖直挂物体之后观看示数
    def measurement_stone(self, img, det, result_key):
        hand_box = det['hand']
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h < 2 * spring_box_w: return
        if len(self.water_bbox) != 0 and spring_box[3] > self.water_bbox[1]: return
        stone_box = det['stone'][0]
        stone_desktop_box = det['stone_desktop'][0]
        desktop_box_w = stone_desktop_box[2] - stone_desktop_box[0]
        desktop_box_h = stone_desktop_box[3] - stone_desktop_box[1]
        bool_1 = self.iou(stone_box[:4], stone_desktop_box[:4]) > 0 and desktop_box_h > desktop_box_w
        bool_2 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 or self.iou(hand_box[1][:4],
                                                                           spring_box[:4]) > 0  # 至少有一只手和弹簧测力计有交集
        if bool_1 and bool_2 and stone_desktop_box[-1] > self.desk_th:
            self.desk_th = stone_desktop_box[-1]
            self.measurement_stone_img = self.draw(img.copy(), [stone_box, stone_desktop_box],
                                                   ['stone', 'stone_desktop'])
            self.measurement_stone_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            # cv2.imshow('3', self.measurement_stone_img)
            # cv2.waitKey(0)
        # spring_box = det['spring_dynamometer'][0]
        # stone_x_c,stone_x_y = (stone_box[0] + stone_box[2]) / 2,(stone_box[1] + stone_box[3]) / 2
        # bool_1 = stone_box[0]>spring_box[2] and spring_box[0] < stone_x_c < spring_box[2]
        # if bool_1 and len(self.measurement_stone_img)==0:
        #     self.measurement_stone_img = self.draw(img.copy(), [spring_box,stone_box],
        #                                    ['spring_dynamometer','stone'])
        # cv2.imshow('3', self.measurement_stone_img)
        # cv2.waitKey(0)

    def measurement_stone_bak(self, img, det, result_key):
        if 'spring_dynamometer' in result_key:
            spring_box = det['spring_dynamometer'][0]
            spring_box_w = spring_box[2] - spring_box[0]
            spring_box_h = spring_box[3] - spring_box[1]
            if spring_box_h < 2 * spring_box_w: return
            if len(self.water_bbox) != 0 and spring_box[3] > self.water_bbox[1]: return
        stone_box = det['stone'][0]
        stone_desktop_box = det['stone_desktop'][0]
        desktop_box_w = stone_desktop_box[2] - stone_desktop_box[0]
        desktop_box_h = stone_desktop_box[3] - stone_desktop_box[1]
        bool_1 = desktop_box_h > desktop_box_w
        if bool_1 and stone_desktop_box[-1] > self.desk_th and self.iou(stone_box[:4], stone_desktop_box[:4]) > 0:
            self.desk_th = stone_desktop_box[-1]
            self.measurement_stone_img_bak = self.draw(img.copy(), [stone_box, stone_desktop_box],
                                                       ['stone', 'stone_desktop'])
            self.measurement_stone_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    # 物块在水中
    def stone_water(self, img, det, result_key):
        water_box = det['bottle_water'][0]
        stone_box = det['stone'][0]
        surface_box = det['bottle_water_surface'][0]
        measuring_box = det['measuring_bottle'][0]
        bool_1 = self.iou(surface_box[:4], stone_box[:4]) > 0
        if bool_1 and not self.stone_water_start:
            self.stone_water_start = True
            return
        stone_box_x_c = (stone_box[2] + stone_box[0]) / 2
        bool_2 = self.iou(water_box[:4], stone_box[:4]) > 0 and self.iou(surface_box[:4], stone_box[:4]) == 0 and \
                 water_box[0] < stone_box_x_c < water_box[2]
        if bool_2 and self.stone_water_start and stone_box[-1] > self.stone_water_th:
            self.stone_water_th = stone_box[-1]
            self.stone_water_img = self.draw(img.copy(), [stone_box, water_box],
                                             ['stone_box', 'water_box'])
            self.stone_water_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.stone_water_box = measuring_box
        if bool_2 and stone_box[-1] > self.stone_water_th:
            self.stone_water_th = stone_box[-1]
            self.stone_water_img_bak = self.draw(img.copy(), [stone_box, water_box],
                                                 ['stone_box', 'water_box'])
            self.stone_water_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.stone_water_box = measuring_box
            # cv2.imshow('4',self.stone_water_img)
            # cv2.waitKey(0)

    # 整理桌面
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
                    if self.iou(clear_box[:4], box) > 0:
                        self.clear_bool = True
                        break
            if not self.clear_bool and len(self.clear_img) == 0:
                self.clear_img = self.draw(img.copy(), [clear_box], ['clear'])
                self.clear_img_time = time.time()
                self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def clear_2(self, img, det, result_key):
        if len(self.stone_water_box) != 0:
            h, w = img.shape[0], img.shape[1]
            clear_xmin, clear_xmax = min(w / 4, self.stone_water_box[0]), max(self.stone_water_box[2], w / 4 * 3)
            box = [clear_xmin, 0, clear_xmax, h]
        else:
            box = []
        if 'measuring_bottle' in result_key:
            measuring_box = det['measuring_bottle'][0]
            if len(box) != 0 and (
                    self.iou(measuring_box[:4], self.stone_water_box[:4]) == 0 or self.iou(measuring_box[:4],
                                                                                           box) == 0):
                self.clear_img_bak = self.draw(img.copy(), [box], ['clear'])
                self.clear_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        else:
            if len(self.stone_water_box) != 0:
                self.clear_img_bak = self.draw(img.copy(), [box], ['clear'])
                self.clear_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def save_score_fun(self, frame_front, preds, objects, time, num_frame, type='win'):
        if len(self.pour_water_img) != 0 and not self.save_1:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '1.jpg', self.pour_water_img)
            else:
                self.assignScore(
                    index=1,
                    img=self.pour_water_img.copy(),
                    object=self.pour_water_img_list[0],
                    conf=0.1,
                    time_frame=self.pour_water_img_list[1],
                    num_frame=self.pour_water_img_list[2],
                    name_save="1.jpg",
                    preds=self.pour_water_img_list[3])
            self.save_1 = True

        if len(self.zero_img) != 0 and not self.save_2:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '2.jpg', self.zero_img)
            else:
                self.assignScore(
                    index=2,
                    img=self.zero_img.copy(),
                    object=self.zero_img_list[0],
                    conf=0.1,
                    time_frame=self.zero_img_list[1],
                    num_frame=self.zero_img_list[2],
                    name_save="2.jpg",
                    preds=self.zero_img_list[3])
            self.save_2 = True
        if len(self.zero_img_bak) != 0 and not self.save_2 and not self.save_2_bak:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '2.jpg', self.zero_img_bak)
            else:
                self.assignScore(
                    index=2,
                    img=self.zero_img_bak.copy(),
                    object=self.zero_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.zero_img_bak_list[1],
                    num_frame=self.zero_img_bak_list[2],
                    name_save="2.jpg",
                    preds=self.zero_img_bak_list[3])
            self.save_2_bak = True

        if len(self.measurement_stone_img) != 0:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '3.jpg', self.measurement_stone_img)
            else:
                self.assignScore(
                    index=3,
                    img=self.measurement_stone_img.copy(),
                    object=self.measurement_stone_img_list[0],
                    conf=0.1,
                    time_frame=self.measurement_stone_img_list[1],
                    num_frame=self.measurement_stone_img_list[2],
                    name_save="3.jpg",
                    preds=self.measurement_stone_img_list[3])

        if len(self.measurement_stone_img_bak) != 0:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '3.jpg', self.measurement_stone_img_bak)
            else:
                self.assignScore(
                    index=3,
                    img=self.measurement_stone_img_bak.copy(),
                    object=self.measurement_stone_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.measurement_stone_img_bak_list[1],
                    num_frame=self.measurement_stone_img_bak_list[2],
                    name_save="3.jpg",
                    preds=self.measurement_stone_img_bak_list[3])

        if len(self.stone_water_img) != 0:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '4.jpg', self.stone_water_img)
            else:
                self.assignScore(
                    index=4,
                    img=self.stone_water_img.copy(),
                    object=self.stone_water_img_list[0],
                    conf=0.1,
                    time_frame=self.stone_water_img_list[1],
                    num_frame=self.stone_water_img_list[2],
                    name_save="4.jpg",
                    preds=self.stone_water_img_list[3])

        if len(self.stone_water_img_bak) != 0:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '4.jpg', self.stone_water_img_bak)
            else:
                self.assignScore(
                    index=4,
                    img=self.stone_water_img_bak.copy(),
                    object=self.stone_water_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.stone_water_img_bak_list[1],
                    num_frame=self.stone_water_img_bak_list[2],
                    name_save="4.jpg",
                    preds=self.stone_water_img_bak_list[3])

        # 保存整理桌面
        if len(self.measurement_stone_img) != 0 or len(self.measurement_stone_img_bak) != 0 or len(
                self.stone_water_img) != 0 or len(self.stone_water_img_bak) != 0:
            if len(self.clear_img) != 0 and not self.save_5 and not self.save_5_bak:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '5.jpg', self.clear_img)
                else:
                    self.assignScore(
                        index=5,
                        img=self.clear_img.copy(),
                        object=self.clear_img_list[0],
                        conf=0.1,
                        time_frame=self.clear_img_list[1],
                        num_frame=self.clear_img_list[2],
                        name_save="5.jpg",
                        preds=self.clear_img_list[3])
                self.save_5 = True
            if len(self.clear_img_bak) != 0 and not self.save_5_bak:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '5.jpg', self.clear_img_bak)
                else:
                    self.assignScore(
                        index=5,
                        img=self.clear_img_bak.copy(),
                        object=self.clear_img_bak_list[0],
                        conf=0.1,
                        time_frame=self.clear_img_bak_list[1],
                        num_frame=self.clear_img_bak_list[2],
                        name_save="5.jpg",
                        preds=self.clear_img_bak_list[3])
                self.save_5_bak = True

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        # 1、在量筒中倒入适量水，观察并记录量筒中水面的对应示数
        # 2、完成弹簧测力计调零
        # 3、弹簧测力计测金属块，保持静止并记录示数
        # 4、弹簧测力计挂上金属块，并放入水中
        # 5、整理器材
        ##################################################################################################
        # 1、在量筒中倒入适量水，观察并记录量筒中水面的对应示数
        img0s = [img0s]
        if 'bottle_water_surface' in result_key and 'bottle_water' in result_key:
            self.pour_water(img0s[0].copy(), det, result_key)
        ##################################################################################################
        # 2、完成弹簧测力计调零
        if 'hand' in result_key and 'spring_dynamometer' in result_key and 'measuring_bottle' in result_key and 'eye' in result_key:
            self.zero(img0s[0].copy(), det, result_key)
        if 'hand' in result_key and 'spring_dynamometer' in result_key and 'bottle_water' in result_key:
            self.zero_bak(img0s[0].copy(), det, result_key)
        ##################################################################################################
        # 3、弹簧测力计测金属块，保持静止并记录示数
        if 'spring_dynamometer' in result_key and 'stone' in result_key and 'stone_desktop' in result_key and 'hand' in result_key:
            self.measurement_stone(img0s[0].copy(), det, result_key)
        if 'stone' in result_key and 'stone_desktop' in result_key:
            self.measurement_stone_bak(img0s[0].copy(), det, result_key)
        ##################################################################################################
        # 4、弹簧测力计挂上金属块，并放入水中
        if 'bottle_water' in result_key and 'stone' in result_key and 'bottle_water_surface' in result_key and 'measuring_bottle' in result_key:
            self.stone_water(img0s[0].copy(), det, result_key)
        ##################################################################################################
        # 5、整理器材
        if len(self.measurement_stone_img) != 0 or len(self.measurement_stone_img_bak) != 0 or len(
                self.stone_water_img) != 0 or len(self.stone_water_img_bak) != 0:
            if 'clear' in result_key:
                self.clear(img0s[0].copy(), det, result_key)
            self.clear_2(img0s[0].copy(), det, result_key)
        self.save_score_fun(img0s, preds, objects, time, num_frame)

    def process_dict(self, d):
        for key in d.keys():
            if len(d[key]) > 1 and key not in ['hand', 'eye']:
                d[key].sort(key=self.sortlist, reverse=True)
                d[key] = [d[key][0]]
            if key in ['hand', 'eye']:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    bbox = d[key][:1]
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
                else:
                    bbox = d[key][:2]
                    d[key] = bbox
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
            names_label = ['spring_dynamometer',
                           'pen',
                           'paper',
                           'stone',
                           'eye',
                           'hand',
                           'zero',
                           'stone_desktop',
                           'bottle_water_surface',
                           'bottle_water',
                           'measuring_bottle',
                           'beaker',
                           'beaker_water',
                           'clear',
                           'beaker_water_surface']
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


class PHY_archimedes_rub(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_archimedes_rub, self).__init__()
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
                          (int(box[2]), int(box[3])), (0, 255, 255), 2)
            lab = f"{label[i]}: {box[-1]:.2f}"
            cv2.putText(img,
                        lab, (int(box[0]), int(box[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 123), 2)
        return img

    ####################################################################################################################################
    def re_init(self):
        self.show_img = False
        self.zero_topdis = 500
        # self.deepsort = Sort_()
        self.select_stone_img_top = []
        self.select_stone_img_front = []
        self.select_stone_img_front_2 = []
        self.pour_water_img_front = []
        self.pour_water_img_top = []
        self.zero_img_front = []
        self.zero_img_front_2 = []
        self.zero_img_side = []
        self.zero_img_top = []
        self.measurement_stone_img_front = []
        self.measurement_stone_img_front_2 = []
        self.measurement_stone_img_side = []
        self.stone_water_img_front = []
        self.stone_water_img_front_2 = []
        self.stone_water_img_side = []
        self.pull_car_img_top = []
        self.pull_car_img_top_2 = []
        self.pull_car_img_top_dis = []
        self.pull_car_img_side = []
        # 清理桌面
        self.clear_bool = False
        self.clear_img_front = []
        self.clear_img_top = []
        # 保存得分点
        self.save_1 = False
        self.save_2 = False
        self.save_3 = False
        self.save_4 = False
        self.save_5 = False
        self.save_6 = False
        self.save_7 = False
        self.save_8 = False
        self.save_9 = False
        self.save_10 = False
        self.save_11 = False
        self.stone_water_box = []
        self.conn_box_w = 0
        self.stone_water_bool = False
        self.top_car_boxdis = []
        self.side_car_boxdis = []
        self.top_cardis = False
        self.side_cardis = False
        self.measurement_stone_bool = False
        self.top_car_spring_dis = []  # 保存车和测力计距离数组
        self.top_car_boxdis_dis = []  # 保存车的坐标信息

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

    # 石头
    def front_select_stone(self, img, det, result_key):
        ''''
        1、先识别出空烧杯
        2、然后在判断空烧杯中有水即满足
        '''
        stone_box = det['stone']
        hand_box = det['hand']
        hand_w = hand_box[0][2] - hand_box[0][0]
        h, w = img.shape[0], img.shape[1]
        box = [w * 0.25, 0, w * 0.75, h * 0.8]
        if 'spring_dynamometer' in result_key:
            spring_box = det['spring_dynamometer'][0]
        else:
            spring_box = []
        if stone_box[1][1] > 1:
            bool_1 = self.dis_point(stone_box[0], stone_box[1]) > 1.5 * hand_w
        else:
            bool_1 = True
        for i in range(len(stone_box)):
            if self.box_include(box, stone_box[i]):
                ll = []
                for j in range(len(hand_box)):
                    if self.iou(hand_box[j][:4], stone_box[i][:4]) > 0:
                        hand_w_,hand_h_ = hand_box[j][2]-hand_box[j][0],hand_box[j][3]-hand_box[j][1]
                        stone_w_, stone_h_ = stone_box[i][2] - stone_box[i][0], stone_box[i][3] - stone_box[j][1]
                        if hand_w_*hand_h_*0.7>stone_w_*stone_h_:
                            ll.append(True)
                if len(ll) > 0:
                    bool_2 = True
                else:
                    bool_2 = False
                    # bool_3 = self.iou(hand_box[0][:4], hand_box[1][:4]) > 0
                bool_3 = (len(spring_box) != 0 and self.iou(spring_box[:4], stone_box[i][:4]) == 0) or len(
                    spring_box) == 0
                if bool_1 and bool_2 and bool_3 and len(self.select_stone_img_front) == 0 and stone_box[i][-1] > 0.8:
                    self.select_stone_img_front = img.copy()
                    self.select_stone_img_front_list = [self.objects_front, self.time_front, self.num_frame_front,
                                                        self.preds_front]

    def front_select_stone_2(self, img, det, result_key):
        ''''
        1、先识别出空烧杯
        2、然后在判断空烧杯中有水即满足
        '''
        stone_box = det['stone']
        spring_stone_box = det['spring_stone'][0]
        h, w = img.shape[0], img.shape[1]
        box = [w * 0.25, 0, w * 0.75, h * 0.8]
        for i in range(len(stone_box)):
            if self.box_include(box, stone_box[i]) and self.iou(spring_stone_box[:4], stone_box[i][:4]) > 0:
                if len(self.select_stone_img_front_2) == 0:
                    self.select_stone_img_front_2 = img.copy()
                    self.select_stone_img_front_2_list = [self.objects_front, self.time_front, self.num_frame_front,
                                                          self.preds_front]

    def top_select_stone(self, img, det, result_key):
        ''''
        1、先识别出空烧杯
        2、然后在判断空烧杯中有水即满足
        '''
        stone_box = det['stone']
        hand_box = det['hand']
        hand_w = hand_box[0][2] - hand_box[0][0]
        h, w = img.shape[0], img.shape[1]
        box = [w * 0.2, h * 0.3, w * 0.8, h]
        if 'spring_dynamometer' in result_key:
            spring_box = det['spring_dynamometer'][0]
        else:
            spring_box = []
        if stone_box[1][1] > 1:
            bool_1 = self.dis_point(stone_box[0], stone_box[1]) > 1.5 * hand_w
        else:
            bool_1 = True
        # bool_1 = stone_box[1][1] > 1 and self.dis_point(stone_box[0], stone_box[1]) > 1.5 * hand_w
        for i in range(len(stone_box)):
            if self.box_include(box, stone_box[i]):
                ll = []
                for j in range(len(hand_box)):
                    if self.iou(hand_box[j][:4], stone_box[i][:4]) > 0:
                        ll.append(True)
                if len(ll) > 0:
                    bool_2 = True
                else:
                    bool_2 = False
                # bool_2 = self.iou(hand_box[0][:4], stone_box[i][:4]) > 0 or self.iou(hand_box[1][:4],
                #                                                                      stone_box[i][:4]) > 0
                # bool_3 = self.iou(hand_box[0][:4], hand_box[1][:4]) > 0
                bool_3 = (len(spring_box) != 0 and self.iou(spring_box[:4], stone_box[i][:4]) == 0) or len(
                    spring_box) == 0
                if bool_1 and bool_2 and bool_3 and len(self.select_stone_img_top) == 0:
                    self.select_stone_img_top = img.copy()
                    self.select_stone_img_top_list = [self.objects_top, self.time_top, self.num_frame_top,
                                                      self.preds_top]

    # 调零
    def front_zero(self, img, det, result_key):
        ''''
        1、判断测力计一定是竖直方向放置（正视角）
        2、
        '''
        h, w = img.shape[0], img.shape[1]
        hand_box = det['hand']
        if hand_box[1][0] != 0 and hand_box[1][1] != 0:
            hand_box.sort(key=self.sort_y, reverse=False)
        hand_cx_1, hand_cy_1 = (hand_box[0][0] + hand_box[0][2]) / 2, (hand_box[0][1] + hand_box[0][3]) / 2
        hand_cx_2, hand_cy_2 = (hand_box[1][0] + hand_box[1][2]) / 2, (hand_box[1][1] + hand_box[1][3]) / 2
        # eye_box = det['eye'][0]
        spring_box = det['spring_dynamometer'][0]
        spring_box_w, spring_box_cx = spring_box[2] - spring_box[0], (spring_box[2] + spring_box[0]) / 2
        spring_box_h, spring_box_cy = spring_box[3] - spring_box[1], (spring_box[3] + spring_box[1]) / 2
        if spring_box_h < 3 * spring_box_w or spring_box[3]>h*0.8: return
        spring_box_y_c = (spring_box[1] + spring_box[3]) / 2
        # 最上面的一只手和测力计有交集、且手的中心在测力计中心上方
        bool_1 = hand_box[0][0] > 1 and self.iou(hand_box[0][:4],
                                                 spring_box[:4]) > 0 and hand_cy_1 - spring_box_w < spring_box_cy
        # 两手和测力计有交集
        bool_2 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4], spring_box[:4]) > 0
        # 如果检测到头，需要判断测力计是否和头有交集,手有经过排序
        if 'head' in result_key:
            head_box = det['head'][0]
            bool_3 = self.iou(head_box[:4], spring_box[:4]) > 0
        else:
            bool_3 = False
            head_box = []
        # 单手调零,手和测力计都和头有交集
        if len(head_box) != 0:
            bool_3_1 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[0][:4],
                                                                                  head_box[:4]) > 0 and self.iou(
                spring_box[:4], head_box[:4]) > 0
        else:
            bool_3_1 = False

        # 判断测力计是否在两手之间
        bb = np.array(hand_box)
        hand_min_x, hand_max_x = bb[:, 0].min(), bb[:, 2].max()
        bool_4 = hand_min_x > 1 and hand_max_x > 1 and hand_min_x < spring_box[0] and spring_box[2] < hand_max_x
        # 如果烧杯在，测力计中心小于烧杯中心
        if 'beaker_water' in result_key:
            beaker_water_box = det['beaker_water']
            li = []
            for j in range(len(beaker_water_box)):
                beaker_box_y_c = (beaker_water_box[j][1] + beaker_water_box[j][3]) / 2
                if spring_box_y_c < beaker_box_y_c:
                    li.append(True)
            if len(li) == len(beaker_water_box):
                bool_5 = True
            else:
                bool_5 = False
        else:
            bool_5 = True
        # 如果石头在，石头要和测力计保持一定的距离
        if 'stone' in result_key:
            stone_box = det['stone']
            stone_w1 = stone_box[0][2] - stone_box[0][0]
            stone_w2 = stone_box[1][2] - stone_box[1][0]
            bool_6 = self.iou(stone_box[0][:4], spring_box[:4]) == 0 and self.iou(stone_box[1][:4], spring_box[:4]) == 0
            # bool_6 = stone_box[0][1] - stone_w1 > spring_box[3] or stone_box[1][1] - stone_w2 > spring_box[3]
        else:
            bool_6 = True
        if 'line' in result_key:
            line_box = det['line'][0]
            bool_7 = self.iou(line_box[:4], hand_box[0][:4]) == 0 and self.iou(line_box[:4], hand_box[1][:4]) == 0
        else:
            bool_7 = True
        bool_8 = spring_box[2]<w-50
        if len(self.zero_img_front) == 0 and (
                bool_1 or bool_2 or bool_3 or bool_3_1) and bool_4 and bool_5 and bool_6 and bool_7 and bool_8 and (
                not self.save_4 or not self.save_6):
            self.zero_img_front = img.copy()
            self.zero_img_front_list = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]
        # 调零
    def front_zero_2(self, img, det, result_key):
        ''''
        1、测力计过在头的区间，且没有组合标签的出现
        2、
        '''
        h, w = img.shape[0], img.shape[1]
        box = [w * 0.4, 0, w * 0.6, h*0.5]
        box_2 = [0, 0, w, h * 0.6]
        spring_box = det['spring_dynamometer'][0]
        spring_box_w, spring_box_cx = spring_box[2] - spring_box[0], (spring_box[2] + spring_box[0]) / 2
        spring_box_h, spring_box_cy = spring_box[3] - spring_box[1], (spring_box[3] + spring_box[1]) / 2
        if spring_box_h < spring_box_w or spring_box[3]>h*0.8: return
        sping_w = (spring_box[3]-spring_box[1])*0.7
        if 'head' in result_key:
            head_box = det['head'][0]
            bool_1 = spring_box[1]<head_box[3] and self.dis_point(head_box,spring_box)<sping_w
        else:
            bool_1 = True
        if 'eye' in result_key:
            eye_box = det['eye']
            bool_2 = spring_box[1]<eye_box[0][3]<spring_box[3] or spring_box[1]<eye_box[1][3]<spring_box[3]
            bool_2 = bool_2 and (self.dis_point(eye_box[0],spring_box)<sping_w or self.dis_point(eye_box[1],spring_box)<sping_w)
        else:
            bool_2 = True
        bool_3 = self.iou(box,spring_box[:4])>0 and spring_box[1]<100
        bool_4 = self.iou(box_2,spring_box[:4])>0
        if 'stone' in result_key:
            ll = []
            stone_box = det['stone']
            for j in range(len(stone_box)):
                stone_ = stone_box[j]
                if stone_[3]<h*0.6:
                    ll.append(True)
            if len(ll)==0 and self.iou(stone_box[0][:4],stone_box[1][:4])==0:
                bool_5 = True
            else:
                bool_5 = False
        else:
            bool_5 = True
        bool_8 = spring_box[2] < w - 50
        if len(self.zero_img_front_2) == 0 and bool_4 and bool_5 and bool_8 and (bool_1 or bool_2 or bool_3) and spring_box[1]<=self.zero_topdis and (not self.save_4 or not self.save_6):
            self.zero_topdis = spring_box[1]
            self.zero_img_front_2 = img.copy()
            self.zero_img_front_2_list = [self.objects_front, self.time_front, self.num_frame_front, self.preds_front]


    # def side_zero(self, img, det, result_key):
    #     ''''
    #     1、判断测力计一定是竖直方向放置（正视角）
    #     2、
    #     '''
    #     hand_box = det['hand']
    #     # eye_box = det['eye'][0]
    #     spring_box = det['spring_dynamometer'][0]
    #     spring_box_w = spring_box[2] - spring_box[0]
    #     spring_box_h = spring_box[3] - spring_box[1]
    #     if spring_box_h < 3 * spring_box_w: return
    #     bool_1 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4], spring_box[
    #                                                                                          :4]) > 0
    #
    #     # bool_2 = spring_box[1] + 30 < eye_box[3] < spring_box[3]  # 眼睛和滑动变阻器保持一样高度
    #     bool_2 = True
    #     # 判断测力计是否在两手之间
    #     bb = np.array(hand_box)
    #     hand_min_x, hand_max_x = bb[:, 0].min(), bb[:, 2].max()
    #     bool_3 = hand_min_x > 1 and hand_max_x > 1 and hand_min_x < spring_box[0] and spring_box[2] < hand_max_x
    #     if bool_1 and len(self.zero_img_side) == 0 and bool_2 and bool_3 and (not self.save_4 or  not self.save_6):
    #         self.zero_img_side = img.copy()
    #         self.zero_img_side_list = [self.objects_side, self.time_side, self.num_frame_side,
    #                                                     self.preds_side]
    #     # 调零
    def top_zero(self, img, det, result_key):
        ''''
        1、判断测力计一定是竖直方向放置（正视角）
        2、
        '''
        h, w = img.shape[0], img.shape[1]
        box = [w * 0.3, h * 0.5, w * 0.7, h]
        hand_box = det['hand']
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h < 2 * spring_box_w: return
        # 两手同时和测力计有交集
        bool_1 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4], spring_box[:4]) > 0
        # 区域内有交集
        bool_2 = self.iou(box, spring_box[:4]) > 0
        # 判断测力计是否在两手之间
        bb = np.array(hand_box)
        hand_min_x, hand_max_x = bb[:, 0].min(), bb[:, 2].max()
        bool_3 = hand_min_x > 1 and hand_max_x > 1 and hand_min_x < spring_box[0] and spring_box[2] < hand_max_x
        if bool_1 and len(self.zero_img_top) == 0 and bool_2 and bool_3 and (not self.save_4 or not self.save_6):
            self.zero_img_top = img.copy()
            self.zero_img_top_list = [self.objects_top, self.time_top, self.num_frame_top, self.preds_top]

    # 竖直挂物体之后观看示数
    def front_measurement_stone(self, img, det, result_key):
        ''''
        1、测力计一定是竖直
        2、一定有石头
        3、石头和弹簧测力计分别与测力计——石头这个标签有交集
        4、如果在称量石头,有烧杯在的时候，不能和烧杯有交集
        '''
        stone_boxes = det['stone']
        for i in range(len(stone_boxes)):
            stone_ = stone_boxes[i]
            spring_stone_box = det['spring_stone'][0]
            spring_box = det['spring_dynamometer'][0]
            spring_box_w = spring_stone_box[2] - spring_stone_box[0]
            spring_box_h = spring_stone_box[3] - spring_stone_box[1]
            if spring_box_h < 3 * spring_box_w: return
            # 组合标签分别和测力计、石头有交集
            bool_1 = self.iou(stone_[:4], spring_stone_box[:4]) > 0 and self.iou(spring_box[:4],
                                                                                 spring_stone_box[:4]) > 0

            if 'beaker_water' in result_key:
                beaker_water_box = det['beaker_water']
                li = []
                for j in range(len(beaker_water_box)):
                    if self.iou(stone_[:4], beaker_water_box[j][:4]) == 0:
                        li.append(True)
                if len(li) == len(beaker_water_box):
                    bool_2 = True
                else:
                    bool_2 = False
            else:
                bool_2 = True
            stone_box_cx, stone_box_cy = (stone_[0] + stone_[2]) / 2, (stone_[1] + stone_[3]) / 2
            spring_box_cx, spring_box_cy = (spring_box[0] + spring_box[2]) / 2, (spring_box[1] + spring_box[3]) / 2
            stone_box_w = stone_[2] - stone_[0]
            # 测力计和石的中心点X方向差值不能大于石头的宽的一半
            if 'hand' in result_key:
                hand_box = det['hand']
                hand_w = hand_box[0][2] - hand_box[0][0]
                bool_3 = self.iou(hand_box[0][:4], stone_[:4]) < 0.08 and self.iou(hand_box[1][:4],
                                                                                   stone_[:4]) < 0.08 and \
                         spring_stone_box[1] < hand_w * 2
            else:
                bool_3 = True
            bool_4 = abs(spring_box_cx - stone_box_cx) < stone_box_w * 0.5
            # bool_4 = spring_stone_box[0] <= stone_box_cx <= spring_stone_box[2] and stone_box_cy < spring_stone_box[3]
            if bool_1 and bool_2 and not self.save_6 and bool_3 and bool_4 and len(
                    self.measurement_stone_img_front) == 0:
                self.measurement_stone_bool = True
                self.measurement_stone_img_front = img.copy()
                self.measurement_stone_img_front_list = [self.objects_front, self.time_front, self.num_frame_front,
                                                         self.preds_front]

    def front_measurement_stone_2(self, img, det, result_key):
        ''''
        1、测力计一定是竖直
        2、一定有石头
        3、石头和弹簧测力计分别与测力计——石头这个标签有交集
        4、如果在称量石头,有烧杯在的时候，不能和烧杯有交集
        '''
        stone_boxes = det['stone']
        for i in range(len(stone_boxes)):
            stone_ = stone_boxes[i]
            spring_stone_box = det['spring_stone'][0]
            spring_box_w = spring_stone_box[2] - spring_stone_box[0]
            spring_box_h = spring_stone_box[3] - spring_stone_box[1]
            if spring_box_h < 3 * spring_box_w: return
            # 组合标签分别和测力计、石头有交集
            bool_1 = self.iou(stone_[:4], spring_stone_box[:4]) > 0
            if 'beaker_water' in result_key:
                beaker_water_box = det['beaker_water']
                li = []
                for j in range(len(beaker_water_box)):
                    if self.box_include(stone_[:4], beaker_water_box[j][:4]):
                        li.append(True)
                if len(li) == len(beaker_water_box):
                    bool_2 = True
                else:
                    bool_2 = False
            else:
                bool_2 = True
            if bool_1 and bool_2 and  not self.save_6 and len(self.measurement_stone_img_front_2) == 0:
                self.measurement_stone_img_front_2 = img.copy()
                self.measurement_stone_img_front_2_list = [self.objects_front, self.time_front, self.num_frame_front,
                                                           self.preds_front]

    # 竖直挂物体之后观看示数
    def side_measurement_stone(self, img, det, result_key):
        ''''
        1、测力计一定是竖直
        2、一定有石头
        3、石头和弹簧测力计分别与测力计——石头这个标签有交集
        4、如果在称量石头,有烧杯在的时候，不能和烧杯有交集
        '''
        stone_boxes = det['stone']
        for i in range(len(stone_boxes)):
            stone_ = stone_boxes[i]
            spring_stone_box = det['spring_stone'][0]
            spring_box = det['spring_dynamometer'][0]
            spring_box_w = spring_stone_box[2] - spring_stone_box[0]
            spring_box_h = spring_stone_box[3] - spring_stone_box[1]
            if spring_box_h < 1.5 * spring_box_w: return
            bool_1 = self.iou(stone_[:4], spring_stone_box[:4]) > 0 and self.iou(spring_box[:4],
                                                                                 spring_stone_box[:4]) > 0
            if 'beaker' in result_key:
                beaker_box = det['beaker']
                li = []
                for j in range(len(beaker_box)):
                    if self.iou(stone_[:4], beaker_box[j][:4]) == 0:
                        li.append(True)
                if len(li) == len(beaker_box):
                    bool_2 = True
                else:
                    bool_2 = False
            else:
                bool_2 = True
            if 'hand' in result_key:
                hand_box = det['hand']
                bool_3 = self.iou(hand_box[0][:4], stone_[:4]) == 0 and self.iou(hand_box[1][:4], stone_[:4]) == 0
            else:
                bool_3 = True
            stone_box_cx, stone_box_cy = (stone_[0] + stone_[2]) / 2, (stone_[1] + stone_[3]) / 2
            spring_box_cx, spring_box_cy = (spring_box[0] + spring_box[2]) / 2, (spring_box[1] + spring_box[3]) / 2
            stone_box_w = stone_[2] - stone_[0]
            # 测力计和石的中心点X方向差值不能大于石头的宽的一半
            # bool_4 = abs(spring_box_cx - stone_box_cx) < stone_box_w
            bool_5 = spring_stone_box[1] < 300
            if bool_1 and bool_2 and not self.save_6 and bool_3 and bool_5 and len(self.stone_water_img_front_2)==0 and len(self.measurement_stone_img_side)==0:
                self.measurement_stone_bool = True
                self.measurement_stone_img_side = img.copy()
                self.measurement_stone_img_side_list = [self.objects_side, self.time_side, self.num_frame_side,
                                                        self.preds_side]

    # 物块在水中
    def front_stone_water(self, img, det, result_key):
        ''''
       1、测力计一定是竖直
       2、一定有石头
       3、石头和弹簧测力计分别与测力计——石头这个标签有交集
       4、测力计——石头这个标签与水柱有交集且石头在水面下方
       '''
        stone_boxes = det['stone']
        for i in range(len(stone_boxes)):
            stone_ = stone_boxes[i]
            spring_stone_box = det['spring_stone'][0]
            if 'spring_dynamometer' in result_key:
                spring_box = det['spring_dynamometer'][0]
                spring_box_w = spring_box[2] - spring_box[0]
                spring_box_h = spring_box[3] - spring_box[1]
                if spring_box_h < 3 * spring_box_w: return
                # 测力计和石头这个标签和测力计、石头都要有交集
                bool_1 = self.iou(stone_[:4], spring_stone_box[:4]) > 0 and self.iou(spring_box[:4],
                                                                                     spring_stone_box[:4]) > 0
            else:
                bool_1 = self.iou(stone_[:4], spring_stone_box[:4]) > 0
            # surface_box = det['beaker_water_surface']
            beaker_water_box = det['beaker_water']
            for j in range(len(beaker_water_box)):
                water_box = beaker_water_box[j]
                # 石头、测力计-石头和烧杯要有交集，烧杯可能是多个
                bool_2 = self.iou(stone_[:4], water_box[:4]) > 0 and self.iou(spring_stone_box[:4], water_box[:4]) > 0
                # 石头、测力计-石头要在烧杯内
                bool_3 = (water_box[0] < spring_stone_box[0] and spring_stone_box[2] < water_box[2])
                bool_4 = (water_box[0] < stone_[0] and stone_[2] < water_box[2] and water_box[1] < stone_[3])
                # 石头要在水柱中心点下方
                stone_cy = (stone_[1] + stone_[3]) / 2
                # water_cy_1 = (water_box[1][1] + stone_box[1][3]) / 2
                # bool_6 = water_cy_0<stone_box[3] or water_cy_1< stone_box[3]
                bool_5 = water_box[1] < stone_cy
                if bool_1 and bool_2 and bool_3 and bool_4 and bool_5 and len(self.stone_water_img_front) == 0:
                    self.stone_water_bool = True
                    self.stone_water_img_front = img.copy()
                    self.stone_water_box = water_box
                    self.stone_water_img_front_list = [self.objects_front, self.time_front, self.num_frame_front,
                                                       self.preds_front]

    def front_stone_water_2(self, img, det, result_key):
        ''''
       1、测力计一定是竖直
       2、一定有石头
       3、石头和弹簧测力计分别与测力计——石头这个标签有交集
       4、测力计——石头这个标签与水柱有交集且石头在水面下方
       '''
        spring_stone_box = det['spring_stone'][0]
        if 'spring_dynamometer' in result_key:
            spring_box = det['spring_dynamometer'][0]
            spring_box_w = spring_box[2] - spring_box[0]
            spring_box_h = spring_box[3] - spring_box[1]
            if spring_box_h < 3 * spring_box_w: return
            # 测力计和石头这个标签和测力计、石头都要有交集
            bool_1 = self.iou(spring_box[:4], spring_stone_box[:4]) > 0
        else:
            bool_1 = True
        beaker_box = det['beaker']
        for j in range(len(beaker_box)):
            water_box = beaker_box[j]
            # 组合标签和烧杯有交集
            bool_2 = self.iou(spring_stone_box[:4], water_box[:4]) > 0
            # 组合标签在烧杯内
            bool_3 = (water_box[0] < spring_stone_box[0] and spring_stone_box[2] < water_box[2])
            #烧杯中间
            water_cy_1 = (water_box[1] + water_box[3]) / 2
            #组合标签下端在烧杯中心一下
            bool_4 = spring_stone_box[3] > water_cy_1
            if bool_1 and bool_2 and bool_3 and bool_4 and len(self.stone_water_img_front_2) == 0:
                self.stone_water_bool = True
                self.stone_water_img_front_2 = img.copy()
                self.stone_water_img_front_2_list = [self.objects_front, self.time_front, self.num_frame_front,
                                                     self.preds_front]

    def side_stone_water(self, img, det, result_key):
        ''''
       1、测力计一定是竖直
       2、一定有石头
       3、石头和弹簧测力计分别与测力计——石头这个标签有交集
       4、测力计——石头这个标签与水柱有交集且石头在水面下方
       '''
        stone_boxes = det['stone']
        for i in range(len(stone_boxes)):
            stone_ = stone_boxes[i]
            spring_stone_box = det['spring_stone'][0]
            spring_stone_box_cx = (spring_stone_box[0] + spring_stone_box[2]) / 2
            spring_box = det['spring_dynamometer'][0]
            beaker_box_ = det['beaker']
            spring_box_w = spring_box[2] - spring_box[0]
            spring_box_h = spring_box[3] - spring_box[1]
            if spring_box_h < 1.5 * spring_box_w: return
            bool_1 = self.iou(stone_[:4], spring_stone_box[:4]) > 0 or self.iou(spring_box[:4],
                                                                                 spring_stone_box[:4]) > 0
            for j in range(len(beaker_box_)):
                beaker_box = beaker_box_[j]
                bool_2 = self.iou(stone_[:4], beaker_box[:4]) > 0 or self.iou(spring_stone_box[:4], beaker_box[:4]) > 0
                #bool_3 = beaker_box[0] < spring_stone_box_cx < beaker_box[2] and stone_[3] < beaker_box[3]
                bool_4 = beaker_box[0] < spring_stone_box_cx < beaker_box[2] and beaker_box[1] < stone_[1]
                bool_5 = self.iou(beaker_box[:4], spring_stone_box[:4]) > 0 and spring_stone_box[3] < beaker_box[3] - 10
                # bool_6 = len(self.measurement_stone_img_front) != 0 or len(self.measurement_stone_img_side) != 0
                beaker_box_cy = (beaker_box[1] + beaker_box[3]) / 2
                # 石头最下方要低过烧杯中心
                bool_7 = beaker_box_cy < stone_[3] and self.iou(beaker_box[:4],stone_[:4])>0
                if bool_1 and bool_2 and bool_4 and bool_5 and bool_7 and len(self.stone_water_img_side)==0:
                    self.stone_water_bool = True
                    self.stone_water_img_side = img.copy()
                    self.stone_water_img_side_list = [self.objects_side, self.time_side, self.num_frame_side,
                                                      self.preds_side]
                    break

    def top_pull_car(self, img, det, result_key):
        ''''
        1、测力计和车这个标签要和测力计、车有交集
        2、手和车无交集
        3、手和测力计有交集
        4、连接处和车和测力计都有交集
        '''
        hand_box = det['hand']
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h * 1.5 > spring_box_w: return
        car_box = det['car'][0]
        car_box_w = car_box[2] - car_box[0]
        conn_box = det['conn'][0]
        spring_car_box = det['spring_car'][0]
        if 'stone' in result_key:
            stone_box = det['stone']
            stone_box_1_w,stone_box_1_h = stone_box[0][2]-stone_box[0][0],stone_box[0][3]-stone_box[0][1]
            stone_box_2_w, stone_box_2_h = stone_box[1][2] - stone_box[1][0], stone_box[1][3] - stone_box[1][1]
            if stone_box_1_w*stone_box_1_h>stone_box_2_w*stone_box_2_h:
                if spring_car_box[1]<stone_box[0][3]:return
            else:
                if spring_car_box[1] < stone_box[1][3]: return
                # 组合标签要和每个元素都有交集
        bool_1 = self.iou(spring_car_box[:4], spring_box[:4]) > 0 or self.iou(spring_car_box[:4], car_box[:4]) > 0
        # 手不能和车有交集
        bool_2 = self.iou(hand_box[0][:4], car_box[:4]) == 0 and self.iou(hand_box[1][:4], car_box[:4]) == 0
        # 手和测力计要有交集
        bool_3 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 or self.iou(hand_box[1][:4], spring_box[:4]) > 0
        # 连接处要和车或测力计有交集
        bool_4 = self.iou(conn_box[:4], spring_box[:4]) > 0 or self.iou(conn_box[:4], car_box[:4]) > 0
        conn_box_w = conn_box[2] - conn_box[0]
        # 移动位置位置超过车长位置时截止
        if bool_1 and bool_3 and bool_4 and conn_box_w > self.conn_box_w and not self.top_cardis:
            self.conn_box_w = conn_box_w
            self.pull_car_img_top = img.copy()
            self.pull_car_img_top_list = [self.objects_top, self.time_top, self.num_frame_top, self.preds_top]
            if len(self.top_car_boxdis) == 0:
                self.top_car_boxdis = car_box
            else:
                bool_dis = car_box_w < self.dis_point(self.top_car_boxdis, car_box)
                if bool_dis:
                    self.top_cardis = True
            # cv2.imwrite(self.save_path + '/5.jpg', img)

    def top_pull_car_2(self, img, det, result_key):
        ''''
        1、测力计和车这个标签要和测力计、车有交集
        2、手和车无交集
        3、手和测力计有交集
        4、连接处和车和测力计都有交集
        '''
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h  > spring_box_w: return
        car_box = det['car'][0]
        spring_car_box = det['spring_car'][0]
        if 'stone' in result_key:
            stone_box = det['stone']
            stone_box_1_w,stone_box_1_h = stone_box[0][2]-stone_box[0][0],stone_box[0][3]-stone_box[0][1]
            stone_box_2_w, stone_box_2_h = stone_box[1][2] - stone_box[1][0], stone_box[1][3] - stone_box[1][1]
            area_1,area_2 = stone_box_1_w*stone_box_1_h,stone_box_2_w*stone_box_2_h
            if area_1>area_2 and area_2>0 and area_1>0:
                if spring_car_box[1]<stone_box[0][3]:return
            else:
                if spring_car_box[1] < stone_box[1][3]: return
        # 组合标签要和每个元素都有交集
        bool_1 = self.iou(spring_car_box[:4], spring_box[:4]) > 0 or self.iou(spring_car_box[:4], car_box[:4]) > 0
        # 移动位置位置超过车长位置时截止
        if bool_1 and not self.top_cardis and len(self.pull_car_img_top_2) == 0:
            self.pull_car_img_top_2 = img.copy()
            self.pull_car_img_top_2_list = [self.objects_top, self.time_top, self.num_frame_top, self.preds_top]

    def top_pull_car_dis(self, img, det, result_key):
        ''''
        1、测力计和车这个标签要和测力计、车有交集
        2、手和车无交集
        3、手和测力计有交集
        4、连接处和车和测力计都有交集
        '''
        hand_box = det['hand']
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h * 1.5 > spring_box_w: return
        car_box = det['car'][0]
        car_box_w = car_box[2] - car_box[0]
        h, w = img.shape[0], img.shape[1]
        box_1 = [w * 0.2, h * 0.4, w * 0.8, h]
        # 车和测力计在限定区域内
        if self.box_include(box_1, car_box) and self.box_include(box_1, spring_box):
            # 手不能和车有交集
            bool_1 = self.iou(hand_box[0][:4], car_box[:4]) == 0 or self.iou(hand_box[1][:4], car_box[:4]) == 0
            # 手和测力计要有交集
            bool_2 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 or self.iou(hand_box[1][:4], spring_box[:4]) > 0
            #测力计和小车需要在一条直线上
            if spring_box[0]>car_box[2]:#车在左边
                if car_box[1]>spring_box[3] or car_box[3]<spring_box[1]:return
            if spring_box[2]<car_box[0]:#车在右边
                if spring_box[1]>car_box[3] or spring_box[3]<car_box[1]:return
            if bool_2:
                # 保存车和测力计之间的而距离
                self.top_car_spring_dis.append(abs(spring_box[0] - car_box[2]))
                if len(self.top_car_spring_dis) >= 5:
                    # 5帧的均值小于车长的一半
                    bool_3 = abs(
                        self.top_car_spring_dis[0] - np.array(self.top_car_spring_dis).mean()) < car_box_w * 0.5
                    del self.top_car_spring_dis[0]
                    if bool_3 and len(self.top_car_boxdis_dis) == 0:
                        self.top_car_boxdis_dis = car_box
                    if len(self.top_car_boxdis_dis) != 0:
                        bool_dis = car_box_w < self.dis_point(self.top_car_boxdis_dis, car_box)
                        if bool_dis and len(self.pull_car_img_top_dis)==0:
                            self.pull_car_img_top_dis = img.copy()
                            self.pull_car_img_top_dis_list = [self.objects_top, self.time_top, self.num_frame_top,
                                                              self.preds_top]
                            # self.top_cardis = True
                        # self.top_car_boxdis_dis = car_box

    def side_pull_car(self, img, det, result_key):
        ''''
        1、测力计和车这个标签要和测力计、车有交集
        2、手和车无交集
        3、手和测力计有交集
        4、连接处和车和测力计都有交集
        '''
        hand_box = det['hand']
        spring_box = det['spring_dynamometer'][0]
        car_box = det['car'][0]
        car_box_w = car_box[2] - car_box[0]
        spring_car_box = det['spring_car'][0]
        bool_1 = self.iou(spring_car_box[:4], spring_box[:4]) > 0 or self.iou(spring_car_box[:4], car_box[:4]) > 0
        #bool_2 = self.iou(hand_box[0][:4], car_box[:4]) == 0 and self.iou(hand_box[1][:4], car_box[:4]) == 0
        bool_3 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 or self.iou(hand_box[1][:4], spring_box[:4]) > 0
        if bool_1 and bool_3 and not self.side_cardis:
            self.pull_car_img_side = img.copy()
            self.pull_car_img_side_list = [self.objects_side, self.time_side, self.num_frame_side,self.preds_side]
            # cv2.imwrite(self.save_path + '/5.jpg', img)
            if len(self.side_car_boxdis) == 0:
                self.side_car_boxdis = car_box
            else:
                bool_dis = car_box_w < self.dis_point(self.side_car_boxdis, car_box)
                if bool_dis:
                    self.side_cardis = True

    # 整理桌面
    def front_clear(self, img, det, result_key):
        h, w = img.shape[0], img.shape[1]
        clear_xmin, clear_xmax = w * 0.15, w * 0.85
        box = [clear_xmin, 0, clear_xmax, h]
        list_ = ['beaker', 'beaker_water_surface', 'beaker_water', 'car', 'stone', 'spring_dynamometer']
        for key in result_key:
            if key not in list_: continue
            beaker_box = det[key]
            for j in range(len(beaker_box)):
                if self.iou(beaker_box[j][:4], box) > 0:
                    return
        self.clear_img_front = img.copy()
        self.clear_img_front_list = [self.objects_front, self.time_front, self.num_frame_front,
                                     self.preds_front]

    def top_clear(self, img, det, result_key):
        h, w = img.shape[0], img.shape[1]
        box_1 = [w * 0.2, h * 0.5, w * 0.8, h]
        box_2 = [0, h * 0.5, w, h]
        bool_1_list = []
        for i in range(len(result_key)):
            if result_key[i] in ['hand', 'eye', 'head', 'towel','stone']: continue
            _box = det[result_key[i]]
            for j in range(len(_box)):
                bool_1 = self.iou(_box[j][:4], box_1) > 0 or self.iou(_box[j][:4], box_2) > 0
                if bool_1:
                    bool_1_list.append(bool_1)
        if len(bool_1_list) == 0:
            self.clear_img_top = img.copy()
            self.clear_img_top_list = [self.objects_top, self.time_top, self.num_frame_top, self.preds_top]

    def save_score_fun(self):
        # 得分点1
        if len(self.select_stone_img_top) != 0 and not self.save_1 and not self.save_8:
            self.assignScore(
                index=1,
                img=self.select_stone_img_top.copy(),
                object=self.select_stone_img_top_list[0],
                conf=0.1,
                time_frame=self.select_stone_img_top_list[1],
                num_frame=self.select_stone_img_top_list[2],
                name_save="1.jpg",
                preds=self.select_stone_img_top_list[3])
            self.save_1 = True
        if len(self.select_stone_img_front) != 0 and not self.save_1 and not self.save_8:
            self.assignScore(
                index=1,
                img=self.select_stone_img_front.copy(),
                object=self.select_stone_img_front_list[0],
                conf=0.1,
                time_frame=self.select_stone_img_front_list[1],
                num_frame=self.select_stone_img_front_list[2],
                name_save="1.jpg",
                preds=self.select_stone_img_front_list[3])
            # self.save_1 = True
        if len(self.select_stone_img_front_2) != 0 and not self.save_1 and not self.save_8:
            self.assignScore(
                index=1,
                img=self.select_stone_img_front_2.copy(),
                object=self.select_stone_img_front_2_list[0],
                conf=0.1,
                time_frame=self.select_stone_img_front_2_list[1],
                num_frame=self.select_stone_img_front_2_list[2],
                name_save="1.jpg",
                preds=self.select_stone_img_front_2_list[3])
            # self.save_1 = True
        # 得分点3
        if len(self.zero_img_front) != 0 and not self.save_3:
            self.assignScore(
                index=3,
                img=self.zero_img_front.copy(),
                object=self.zero_img_front_list[0],
                conf=0.1,
                time_frame=self.zero_img_front_list[1],
                num_frame=self.zero_img_front_list[2],
                name_save="3.jpg",
                preds=self.zero_img_front_list[3])
            self.save_3 = True
        if len(self.zero_img_front_2) != 0 and not self.save_3:
            self.assignScore(
                index=3,
                img=self.zero_img_front_2.copy(),
                object=self.zero_img_front_2_list[0],
                conf=0.1,
                time_frame=self.zero_img_front_2_list[1],
                num_frame=self.zero_img_front_2_list[2],
                name_save="3.jpg",
                preds=self.zero_img_front_2_list[3])
        if len(self.zero_img_front) == 0 and self.measurement_stone_bool:
            if len(self.zero_img_top) != 0 and not self.save_3:
                self.assignScore(
                    index=3,
                    img=self.zero_img_top.copy(),
                    object=self.zero_img_top_list[0],
                    conf=0.1,
                    time_frame=self.zero_img_top_list[1],
                    num_frame=self.zero_img_top_list[2],
                    name_save="3.jpg",
                    preds=self.zero_img_top_list[3])
                self.save_3 = True
        # 得分点4
        if len(self.measurement_stone_img_front) != 0 and not self.save_4:
            self.assignScore(
                index=4,
                img=self.measurement_stone_img_front.copy(),
                object=self.measurement_stone_img_front_list[0],
                conf=0.1,
                time_frame=self.measurement_stone_img_front_list[1],
                num_frame=self.measurement_stone_img_front_list[2],
                name_save="4.jpg",
                preds=self.measurement_stone_img_front_list[3])
            self.save_4 = True
        if len(self.measurement_stone_img_front_2) != 0 and not self.save_4:
            self.assignScore(
                index=4,
                img=self.measurement_stone_img_front_2.copy(),
                object=self.measurement_stone_img_front_2_list[0],
                conf=0.1,
                time_frame=self.measurement_stone_img_front_2_list[1],
                num_frame=self.measurement_stone_img_front_2_list[2],
                name_save="4.jpg",
                preds=self.measurement_stone_img_front_2_list[3])
        # 正视角没找到的情况看看侧视角，在下一个得分点得到之前保存
        if not self.save_4 and len(self.measurement_stone_img_side) != 0:
            self.assignScore(
                index=4,
                img=self.measurement_stone_img_side.copy(),
                object=self.measurement_stone_img_side_list[0],
                conf=0.1,
                time_frame=self.measurement_stone_img_side_list[1],
                num_frame=self.measurement_stone_img_side_list[2],
                name_save="4.jpg",
                preds=self.measurement_stone_img_side_list[3])
            # self.save_4 = True
        # 得分点6
        if len(self.stone_water_img_front) != 0 and not self.save_6:
            self.assignScore(
                index=6,
                img=self.stone_water_img_front.copy(),
                object=self.stone_water_img_front_list[0],
                conf=0.1,
                time_frame=self.stone_water_img_front_list[1],
                num_frame=self.stone_water_img_front_list[2],
                name_save="6.jpg",
                preds=self.stone_water_img_front_list[3])
            self.save_6 = True
        if len(self.stone_water_img_front_2) != 0 and not self.save_6:
            self.assignScore(
                index=6,
                img=self.stone_water_img_front_2.copy(),
                object=self.stone_water_img_front_2_list[0],
                conf=0.1,
                time_frame=self.stone_water_img_front_2_list[1],
                num_frame=self.stone_water_img_front_2_list[2],
                name_save="6.jpg",
                preds=self.stone_water_img_front_2_list[3])
            # self.save_6 = True
        if len(self.stone_water_img_side) != 0 and not self.save_6:
            self.assignScore(
                index=6,
                img=self.stone_water_img_side.copy(),
                object=self.stone_water_img_side_list[0],
                conf=0.1,
                time_frame=self.stone_water_img_side_list[1],
                num_frame=self.stone_water_img_side_list[2],
                name_save="6.jpg",
                preds=self.stone_water_img_side_list[3])
            # self.save_6 = True
        # 得分点8
        if len(self.pull_car_img_top) != 0 and not self.save_8:
            self.assignScore(
                index=8,
                img=self.pull_car_img_top.copy(),
                object=self.pull_car_img_top_list[0],
                conf=0.1,
                time_frame=self.pull_car_img_top_list[1],
                num_frame=self.pull_car_img_top_list[2],
                name_save="8.jpg",
                preds=self.pull_car_img_top_list[3])
            # self.pull_car_img = []
            if self.top_cardis:
                self.save_8 = True
        if len(self.pull_car_img_top_2) != 0 and len(self.pull_car_img_top) == 0 and  not self.save_8:
            self.assignScore(
                index=8,
                img=self.pull_car_img_top_2.copy(),
                object=self.pull_car_img_top_2_list[0],
                conf=0.1,
                time_frame=self.pull_car_img_top_2_list[1],
                num_frame=self.pull_car_img_top_2_list[2],
                name_save="8.jpg",
                preds=self.pull_car_img_top_2_list[3])
        if len(self.pull_car_img_top_dis) != 0 and len(self.pull_car_img_top) == 0 and len(self.pull_car_img_top_2) == 0 and not self.save_8:
            self.assignScore(
                index=8,
                img=self.pull_car_img_top_dis.copy(),
                object=self.pull_car_img_top_dis_list[0],
                conf=0.1,
                time_frame=self.pull_car_img_top_dis_list[1],
                num_frame=self.pull_car_img_top_dis_list[2],
                name_save="8.jpg",
                preds=self.pull_car_img_top_dis_list[3])
        if len(self.pull_car_img_side) != 0 and len(self.pull_car_img_top) == 0 and not self.save_8:
            self.assignScore(
                index=8,
                img=self.pull_car_img_side.copy(),
                object=self.pull_car_img_side_list[0],
                conf=0.1,
                time_frame=self.pull_car_img_side_list[1],
                num_frame=self.pull_car_img_side_list[2],
                name_save="8.jpg",
                preds=self.pull_car_img_side_list[3])
            # self.pull_car_img_bak_list = []
            if self.side_cardis:
                self.save_8 = True
        # 得分点10
        # if self.stone_water_bool:
        if len(self.clear_img_front) != 0  and not self.save_10:
            self.assignScore(
                index=10,
                img=self.clear_img_front.copy(),
                object=self.clear_img_front_list[0],
                conf=0.1,
                time_frame=self.clear_img_front_list[1],
                num_frame=self.clear_img_front_list[2],
                name_save="10.jpg",
                preds=self.clear_img_front_list[3])
            self.clear_img_front = []
        if len(self.clear_img_top) != 0 and not self.save_10:
            self.assignScore(
                index=10,
                img=self.clear_img_top.copy(),
                object=self.clear_img_top_list[0],
                conf=0.1,
                time_frame=self.clear_img_top_list[1],
                num_frame=self.clear_img_top_list[2],
                name_save="10.jpg",
                preds=self.clear_img_top_list[3])
            self.clear_img_top = []
            if self.save_8:
                self.save_10 = True

    def predict(self, img0s, dets, result_keys):
        # 1、选择较小的石块进行测量
        # 2、对弹簧测力计进行调零
        # 3、将小石块用细线系好，并竖直挂在弹簧测力计挂钩上
        # 4、将小石块缓慢浸入水中
        # 5、拉着木块在实验台上匀速直线滑动
        # 6、实验结束后能及时整理仪器
        ##################################################################################################
        # 2、对弹簧测力计进行调零
        top_img, top_det, top_key = img0s[0], dets[0], result_keys[0]
        front_img, front_det, front_key = img0s[1], dets[1], result_keys[1]
        side_img, side_det, side_key = img0s[2], dets[2], result_keys[2]
        if 'stone' in front_key and 'hand' in front_key:
            # 跟踪
            # bb_ = np.array([front_det['hand'][0][:4]])
            # tra = self.deepsort.update(bb_)
            # if len(tra)==0:
            #     pass
            # else:
            #     for object in tra:
            #         xmin,ymin,xmax,ymax,index = object[0],object[1],object[2],object[3],object[4]
            #         cv2.rectangle(front_img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,0,255),3)
            #         cv2.putText(front_img,str(index),(int(xmin),int(ymin)),cv2.FONT_HERSHEY_PLAIN,2,[0,0,255],2)
            # cv2.imshow('a',front_img)
            # cv2.waitKey(1)
            self.front_select_stone(front_img, front_det, front_key)
        if 'stone' in front_key and 'spring_stone' in front_key:
            self.front_select_stone_2(front_img, front_det, front_key)
        if 'stone' in top_key and 'hand' in top_key:
            self.top_select_stone(top_img, top_det, top_key)
        if 'line' not in front_key and 'spring_stone' not in front_key and 'hand' in front_key and 'spring_dynamometer' in front_key:
            self.front_zero(front_img, front_det, front_key)
        if 'line' not in front_key and 'spring_stone' not in front_key and 'spring_dynamometer' in front_key:
            self.front_zero_2(front_img, front_det, front_key)
        # if 'spring_stone' not in side_key and 'hand' in side_key and 'spring_dynamometer' in side_key and  'spring_stone' not in side_key:
        #     self.side_zero(side_img, side_det, side_key)
        if 'spring_stone' not in top_key and 'hand' in top_key and 'spring_dynamometer' in top_key and 'spring_stone' not in top_key:
            self.top_zero(top_img, top_det, top_key)
        ##################################################################################################
        # 3、将小石块用细线系好，并竖直挂在弹簧测力计挂钩上
        if 'spring_dynamometer' in front_key and 'stone' in front_key and 'spring_stone' in front_key:
            self.front_measurement_stone(front_img, front_det, front_key)
        if 'stone' in front_key and 'spring_stone' in front_key:
            self.front_measurement_stone_2(front_img, front_det, front_key)
        if 'spring_dynamometer' in side_key and 'stone' in side_key and 'spring_stone' in side_key:
            self.side_measurement_stone(side_img, side_det, side_key)
        ##################################################################################################
        # 4、将小石块缓慢浸入水中
        if 'stone' in front_key and 'spring_stone' in front_key and 'beaker_water' in front_key:
            self.front_stone_water(front_img, front_det, front_key)
        if 'spring_stone' in front_key and 'beaker' in front_key:
            self.front_stone_water_2(front_img, front_det, front_key)
        if 'spring_dynamometer' in side_key and 'stone' in side_key and 'spring_stone' in side_key and 'beaker' in side_key:
            self.side_stone_water(side_img, side_det, side_key)
        ##################################################################################################
        # 5、拉着木块在实验台上匀速直线滑动
        if 'hand' in top_key and 'spring_dynamometer' in top_key and 'car' in top_key:
            if 'spring_car' in top_key and 'conn' in top_key:
                self.top_pull_car(top_img, top_det, top_key)
            else:
                self.top_pull_car_dis(top_img, top_det, top_key)
        if 'spring_car' in top_key and 'spring_dynamometer' in top_key and 'car' in top_key:
            self.top_pull_car_2(top_img, top_det, top_key)
        if 'spring_car' in side_key and 'hand' in side_key and 'spring_dynamometer' in side_key and 'car' in side_key:
            self.side_pull_car(side_img, side_det, side_key)
        ##################################################################################################
        # 6、实验结束后能及时整理仪器
        if len(self.measurement_stone_img_front) != 0 or len(self.stone_water_img_front) != 0 or len(
                self.measurement_stone_img_side) != 0 or len(self.stone_water_img_side) != 0 or len(self.measurement_stone_img_front_2)!=0\
                 or len(self.stone_water_img_front_2)!=0 or len(self.pull_car_img_top_2)!=0:
            if 'spring_car' not in front_key and 'spring_stone' not in front_key:
                self.front_clear(front_img, front_det, front_key)
            if 'beaker' in top_key and ('car' in top_key or 'spring_dynamometer' in top_key) and  'spring_car' not in top_key and 'spring_stone' not in top_key:
                self.top_clear(top_img, top_det, top_key)
        self.save_score_fun()

    def process_dict(self, d):
        for key in d.keys():
            if len(d[key]) > 1 and key not in ['hand', 'eye', 'stone']:
                d[key].sort(key=self.sortlist, reverse=True)
                d[key] = [d[key][0]]
            if key in ['hand', 'eye', 'stone', 'beaker_water_surface', 'beaker_water', 'beaker']:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    bbox = d[key][:1]
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
                else:
                    bbox = d[key][:2]
                    d[key] = bbox
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
            names_label = ['potato', 'car', 'spring_dynamometer', 'beaker_water_surface', 'beaker_water', 'beaker',
                           'eye', 'hand', 'line', 'stone', 'conn', 'spring_car', 'spring_stone']
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

    def sort_y(self, elem):
        return elem[1]

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
        # if pred_front is not None and pred_front.shape[0])and pred_side is not None and pred_side.shape[
        #     0] and pred_top is not None and pred_top.shape[0]:
        # top
        if pred_top is not None and pred_top.shape[0]:
            top_preds, objects_top = self.assign_labels(frame_top, pred_top, names_label)
            dict_top = self.process_(top_preds, objects_top)
            self.num_frame_top = num_frame_top
            self.preds_top = top_preds
            self.objects_top = None  # objects_top
            self.time_top = time_top
            top_key = list(dict_top.keys())
        else:
            dict_top,top_key = [],[]
        # # front
        if pred_front is not None and pred_front.shape[0]:
            front_preds, objects_front = self.assign_labels(frame_front, pred_front, names_label)
            dict_front = self.process_(front_preds, objects_front)
            self.num_frame_front = num_frame_front
            self.preds_front = front_preds
            self.objects_front = None
            self.time_front = time_front
            front_key = list(dict_front.keys())
        else:
            dict_front,front_key = [],[]
        # # side
        if pred_side is not None and pred_side.shape[0]:
            side_preds, objects_side = self.assign_labels(frame_side, pred_side, names_label)
            dict_side = self.process_(side_preds, objects_side)
            self.num_frame_side = num_frame_side
            self.preds_side = side_preds
            self.objects_side = None
            self.time_side = time_side
            side_key = list(dict_side.keys())
        else:
            dict_side, side_key = [], []
        self.predict([frame_top, frame_front, frame_side], [dict_top, dict_front, dict_side],
                     [top_key, front_key, side_key])
        if self.show_img:
            if front_preds is not None and top_preds is not None  and side_preds is not None :
                self.plot(front_preds, frame_front)
                self.plot(top_preds, frame_top)
                self.plot(side_preds, frame_side)
            frame_front = cv2.resize(frame_front, (940, 684))
            frame_top = cv2.resize(frame_top, (940, 684))
            frame_side = cv2.resize(frame_side, (940, 684))
            cv2.imshow('front', frame_front)
            cv2.imshow('top', frame_top)
            cv2.imshow('side', frame_side)
            cv2.waitKey(1)
        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=top_preds, front_preds=front_preds, side_preds=side_preds)
