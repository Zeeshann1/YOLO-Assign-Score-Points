from .comm import *
from .comm.course_base import ConfigModel
from torchvision import transforms
from aideModel import ClassMobilenetv3
from PIL import Image

class PHY_explore_buoyancy_factors(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_explore_buoyancy_factors, self).__init__()
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

    def re_init(self):
        # 鸡蛋放入烧杯中并加水
        self.egg_in_beaker_img = []
        # 开始加盐搅拌
        self.add_salt_stir_start = False
        # 鸡蛋漂浮
        self.egg_float_img = []
        self.beaker_bbox = []
        self.stone_water_start = False
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
        self.save_3 = False
        self.save_3_bak = False
        self.save_4 = False
        self.save_4_bak = False
        self.save_5 = False
        self.save_5_bak = False
        self.save_6 = False
        self.save_6_bak = False

        self.stone_water_box = []
        self.desk_th = 0.2
        self.stone_water_th = 0.2

        self.not_draw_img = True
        self.egg_down = False

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

        # 在烧杯中加入适量的水，并将鸡蛋放入水中

    def egg_in_beaker(self, img, det, result_key):
        beaker_box = det['beaker']
        beaker_water_box = det['beaker_water']
        egg_box = det['egg'][0]
        for i in range(len(beaker_box)):
            for j in range(len(beaker_water_box)):
                bool_1 = self.iou(beaker_box[i][:4], beaker_water_box[j][:4]) > 0
                bool_2 = self.iou(beaker_box[i][:4], egg_box[:4]) > 0
                bool_3 = self.iou(beaker_water_box[j][:4], egg_box[:4]) == 0
                bool_4 = beaker_water_box[j][3] < egg_box[1]
                if bool_1 and bool_2 and bool_3 and bool_4:
                    self.egg_in_beaker_img = self.draw(img.copy(), [beaker_water_box[j], egg_box],
                                                       ['beaker_water', 'egg'])
                    self.egg_in_beaker_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.beaker_bbox = beaker_box[i]
                    self.egg_down = True

        # 加盐搅拌

    def add_salt_stir(self, img, det, result_key):
        spoon_box = det['spoon'][0]
        salt_box = det['salt'][0]
        mouth_bottle_box = det['mouth_bottle'][0]
        bool_1 = self.iou(spoon_box[:4], mouth_bottle_box[:4]) > 0 and self.iou(salt_box[:4],
                                                                                mouth_bottle_box[:4]) > 0
        if bool_1:
            self.add_salt_stir_start = True

    def add_salt_stir_(self, img, det, result_key):
        beaker_water_box = det['beaker_water']
        beaker_box = det['beaker']
        glass_rod_box = det['glass_rod'][0]
        for i in range(len(beaker_water_box)):
            for j in range(len(beaker_box)):
                bool_1 = self.iou(beaker_water_box[i][:4], beaker_box[j][:4]) > 0
                bool_2 = self.iou(glass_rod_box[:4], beaker_box[j][:4]) > 0
                if bool_1 and bool_2 and glass_rod_box[-1] > 0.7:
                    self.add_salt_stir_start = True

        # 鸡蛋漂浮

    def egg_float(self, img, det, result_key):
        water_box = det['water']
        beaker_water_box = det['beaker_water']
        egg_box = det['egg'][0]
        if 'hand' in result_key:
            hand_box = det['hand']
            if self.iou(hand_box[0][:4], egg_box[:4]) > 0 or self.iou(hand_box[1][:4], egg_box[:4]) > 0: return
        for i in range(len(water_box)):
            for j in range(len(beaker_water_box)):
                if 'glass_rod' in result_key:
                    glass_rod_box = det['glass_rod'][0]
                    if self.iou(water_box[i][:4], glass_rod_box[:4]) > 0: return
                bool_1 = self.iou(water_box[i][:4], beaker_water_box[j][:4]) > 0
                bool_2 = self.iou(beaker_water_box[j][:4], egg_box[:4]) > 0 and (egg_box[1] + egg_box[3]) / 2 > \
                         beaker_water_box[j][3]  # 鸡蛋顶要超过水面中心，且鸡蛋中心位置要在水面下方
                bool_3 = self.iou(beaker_water_box[j][:4], egg_box[:4]) > 0
                if bool_1 and bool_2 and bool_3 and self.egg_down:
                    self.egg_float_img = self.draw(img.copy(), [water_box[i], egg_box],
                                                   ['water', 'egg'])
                    self.egg_float_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

        # 调零

    def zero(self, img, det, result_key):
        hand_box = det['hand']
        eye_box = det['eye'][0]
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h < 3 * spring_box_w: return  # 计算弹簧测力计长宽比
        bottle_box = det['beaker'][0]
        spring_box_y_c = (spring_box[1] + spring_box[3]) / 2
        # bottle_box_y_c = (bottle_box[1] + bottle_box[3]) / 2
        bool_1 = self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4], spring_box[
                                                                                             :4]) > 0 and spring_box_y_c < \
                 bottle_box[1]
        bool_2 = spring_box[1] < eye_box[3] < spring_box[3]  # 眼睛和滑动变阻器保持一样高度
        if bool_1 and len(self.zero_img) == 0 and bool_2:
            self.zero_img = self.draw(img.copy(), [spring_box],
                                      ['spring_dynamometer'])
            self.zero_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def zero_bak(self, img, det, result_key):
        hand_box = det['hand']
        beaker_box = det['beaker'][0]
        spring_box = det['spring_dynamometer'][0]
        spring_box_w = spring_box[2] - spring_box[0]
        spring_box_h = spring_box[3] - spring_box[1]
        if spring_box_h < 3 * spring_box_w: return
        spring_box_y_c = (spring_box[1] + spring_box[3]) / 2
        bool_1 = (self.iou(hand_box[0][:4], spring_box[:4]) > 0 and self.iou(hand_box[1][:4],
                                                                             spring_box[
                                                                             :4]) > 0) and spring_box_y_c < \
                 beaker_box[1]
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
        if len(self.beaker_bbox) != 0 and spring_box[3] > self.beaker_bbox[1]: return
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
            self.measurement_stone_img_list= [self.objects_, self.time_, self.num_frame_, self.preds_]

    def measurement_stone_bak(self, img, det, result_key):
        if 'spring_dynamometer' in result_key:
            spring_box = det['spring_dynamometer'][0]
            spring_box_w = spring_box[2] - spring_box[0]
            spring_box_h = spring_box[3] - spring_box[1]
            if spring_box_h < 2 * spring_box_w: return
            if len(self.beaker_bbox) != 0 and spring_box[3] > self.beaker_bbox[1]: return
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
        water_box = det['water'][0]
        stone_box = det['stone'][0]
        beaker_water_box = det['beaker_water'][0]
        bool_1 = self.iou(beaker_water_box[:4], stone_box[:4]) > 0
        if bool_1 and not self.stone_water_start:
            self.stone_water_start = True
            return
        stone_box_x_c = (stone_box[2] + stone_box[0]) / 2
        bool_2 = self.iou(water_box[:4], stone_box[:4]) > 0 and self.iou(beaker_water_box[:4],
                                                                         stone_box[:4]) == 0 and \
                 water_box[0] < stone_box_x_c < water_box[2]
        if bool_2 and self.stone_water_start and stone_box[-1] > self.stone_water_th:
            self.stone_water_th = stone_box[-1]
            self.stone_water_img = self.draw(img.copy(), [stone_box, water_box],
                                             ['stone_box', 'water_box'])
            self.stone_water_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        if bool_2 and stone_box[-1] > self.stone_water_th:
            self.stone_water_th = stone_box[-1]
            self.stone_water_img_bak = self.draw(img.copy(), [stone_box, water_box],
                                                 ['stone_box', 'water_box'])
            self.stone_water_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

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
                self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def clear_2(self, img, det, result_key):
        if len(self.beaker_bbox) != 0:
            h, w = img.shape[0], img.shape[1]
            clear_xmin, clear_xmax = min(w / 4, self.beaker_bbox[0]), max(self.beaker_bbox[2], w / 4 * 3)
            box = [clear_xmin, 0, clear_xmax, h]
        else:
            box = []
        if 'beaker' in result_key:
            if len(box) == 0: return
            beaker_box = det['beaker']
            for i in range(len(beaker_box)):
                bool_1 = self.iou(beaker_box[i][:4], box) == 0
                bool_2 = self.iou(beaker_box[i][:4], self.beaker_bbox[:4]) == 0
                if bool_1 and bool_2:
                    self.clear_img_bak = self.draw(img.copy(), [box], ['clear'])
                    self.clear_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        else:
            if len(self.stone_water_box) != 0:
                self.clear_img_bak = self.draw(img.copy(), [box], ['clear'])
                self.clear_img_bak_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def save_score_fun(self):
        if len(self.egg_in_beaker_img) != 0 and not self.save_1:
            self.assignScore(
                index=1,
                img=self.egg_in_beaker_img.copy(),
                object=self.egg_in_beaker_img_list[0],
                conf=0.1,
                time_frame=self.egg_in_beaker_img_list[1],
                num_frame=self.egg_in_beaker_img_list[2],
                name_save="1.jpg",
                preds=self.egg_in_beaker_img_list[3])
            # self.assignScore(1, self.egg_in_beaker_img, time.time())
            self.save_1 = True
        if len(self.egg_float_img) != 0 and not self.save_2:
            self.assignScore(
                index=2,
                img=self.egg_float_img.copy(),
                object=self.egg_float_img_list[0],
                conf=0.1,
                time_frame=self.egg_float_img_list[1],
                num_frame=self.egg_float_img_list[2],
                name_save="2.jpg",
                preds=self.egg_float_img_list[3])
            # self.assignScore(2, self.egg_float_img, time.time())
            self.save_2 = True
        if len(self.zero_img) != 0 and not self.save_3:
            self.assignScore(
                index=3,
                img=self.zero_img.copy(),
                object=self.zero_img_list[0],
                conf=0.1,
                time_frame=self.zero_img_list[1],
                num_frame=self.zero_img_list[2],
                name_save="3.jpg",
                preds=self.zero_img_list[3])
            # self.assignScore(3, self.zero_img, time.time())
            self.save_3 = True
        if len(self.zero_img_bak) != 0 and not self.save_3 and not self.save_3_bak:
            self.assignScore(
                index=3,
                img=self.zero_img_bak.copy(),
                object=self.zero_img_bak_list[0],
                conf=0.1,
                time_frame=self.zero_img_bak_list[1],
                num_frame=self.zero_img_bak_list[2],
                name_save="3.jpg",
                preds=self.zero_img_bak_list[3])
            self.assignScore(3, self.zero_img_bak, time.time())
            self.save_3_bak = True

        if len(self.measurement_stone_img) != 0:
            self.assignScore(
                index=4,
                img=self.measurement_stone_img.copy(),
                object=self.measurement_stone_img_list[0],
                conf=0.1,
                time_frame=self.measurement_stone_img_list[1],
                num_frame=self.measurement_stone_img_list[2],
                name_save="4.jpg",
                preds=self.measurement_stone_img_list[3])
            # self.assignScore(4, self.measurement_stone_img, time.time())
        if len(self.measurement_stone_img_bak) != 0:
            self.assignScore(
                index=4,
                img=self.measurement_stone_img_bak.copy(),
                object=self.measurement_stone_img_bak_list[0],
                conf=0.1,
                time_frame=self.measurement_stone_img_bak_list[1],
                num_frame=self.measurement_stone_img_bak_list[2],
                name_save="4.jpg",
                preds=self.measurement_stone_img_bak_list[3])
            # self.assignScore(4, self.measurement_stone_img_bak, time.time())
            # self.save_3_bak = True

        if len(self.stone_water_img) != 0:
            self.assignScore(
                index=5,
                img=self.stone_water_img.copy(),
                object=self.stone_water_img_list[0],
                conf=0.1,
                time_frame=self.stone_water_img_list[1],
                num_frame=self.stone_water_img_list[2],
                name_save="5.jpg",
                preds=self.stone_water_img_list[3])
            # self.assignScore(5, self.stone_water_img, time.time())
            # self.save_4 = True
        if len(self.stone_water_img_bak) != 0:
            self.assignScore(
                index=5,
                img=self.stone_water_img_bak.copy(),
                object=self.stone_water_img_bak_list[0],
                conf=0.1,
                time_frame=self.stone_water_img_bak_list[1],
                num_frame=self.stone_water_img_bak_list[2],
                name_save="5.jpg",
                preds=self.stone_water_img_bak_list[3])
            # self.assignScore(5, self.stone_water_img_bak, time.time())
            # self.save_4_bak = True
        # 保存整理桌面
        if len(self.measurement_stone_img) != 0 or len(self.measurement_stone_img_bak) != 0 or len(
                self.stone_water_img) != 0 or len(self.stone_water_img_bak) != 0:
            if len(self.clear_img) != 0 and not self.save_6 and not self.save_6_bak:
                self.assignScore(
                    index=6,
                    img=self.clear_img.copy(),
                    object=self.clear_img_list[0],
                    conf=0.1,
                    time_frame=self.clear_img_list[1],
                    num_frame=self.clear_img_list[2],
                    name_save="6.jpg",
                    preds=self.clear_img_list[3])
                # self.assignScore(6, self.clear_img, time.time())
                self.save_6 = True
            if len(self.clear_img_bak) != 0 and not self.save_6_bak:
                self.assignScore(
                    index=6,
                    img=self.clear_img_bak.copy(),
                    object=self.clear_img_bak_list[0],
                    conf=0.1,
                    time_frame=self.clear_img_bak_list[1],
                    num_frame=self.clear_img_bak_list[2],
                    name_save="6.jpg",
                    preds=self.clear_img_bak_list[3])
                # self.assignScore(6, self.clear_img_bak, time.time())
                self.save_6_bak = True

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        # 1、在烧杯中加入适量的水，并将鸡蛋放入水中
        # 2、并加盐搅拌，观察鸡蛋是否漂浮
        # 3、弹簧测力计调零
        # 4、弹簧测力计测金属块，保持静止并记录示数
        # 5、弹簧测力计挂上金属块，并放入水中
        # 6、整理器材
        ##################################################################################################
        # 1、在烧杯中加入适量的水，并将鸡蛋放入水中
        if 'beaker' in result_key and 'egg' in result_key and 'beaker_water' in result_key:
            self.egg_in_beaker(img0s.copy(), det, result_key)
        ##################################################################################################
        # 2、并加盐搅拌，观察鸡蛋是否漂浮
        # 2.1、并加盐搅拌
        if 'spoon' in result_key and 'salt' in result_key and 'mouth_bottle' in result_key:
            self.add_salt_stir(img0s.copy(), det, result_key)
        # if 'beaker_water' in result_key and 'glass_rod' in result_key and 'egg' in result_key:
        #     self.add_salt_stir(img0s[0].copy(), det, result_key)
        # 2.1、观察鸡蛋是否漂浮
        if self.add_salt_stir_start and 'water' in result_key and 'egg' in result_key and 'beaker_water' in result_key:
            self.egg_float(img0s.copy(), det, result_key)
        ##################################################################################################
        # 3、弹簧测力计调零
        if 'hand' in result_key and 'spring_dynamometer' in result_key and 'beaker' in result_key and 'eye' in result_key:
            self.zero(img0s.copy(), det, result_key)
        if 'hand' in result_key and 'spring_dynamometer' in result_key and 'bottle_water' in result_key:
            self.zero_bak(img0s.copy(), det, result_key)
        ##################################################################################################
        # 4、弹簧测力计测金属块，保持静止并记录示数
        if 'spring_dynamometer' in result_key and 'stone' in result_key and 'stone_desktop' in result_key and 'hand' in result_key:
            self.measurement_stone(img0s.copy(), det, result_key)
        if 'stone' in result_key and 'stone_desktop' in result_key:
            self.measurement_stone_bak(img0s.copy(), det, result_key)
        ##################################################################################################
        # 5、弹簧测力计挂上金属块，并放入水中
        if 'beaker_water' in result_key and 'stone' in result_key and 'water' in result_key:
            self.stone_water(img0s.copy(), det, result_key)
        ##################################################################################################
        # 6、整理器材
        if len(self.measurement_stone_img) != 0 or len(self.measurement_stone_img_bak) != 0 or len(
                self.stone_water_img) != 0 or len(self.stone_water_img_bak) != 0:
            if 'clear' in result_key:
                self.clear(img0s.copy(), det, result_key)
            self.clear_2(img0s.copy(), det, result_key)
        self.save_score_fun()

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
            names_label = ['beaker_water',
             'water',
             'spring_dynamometer',
             'hand',
             'beaker',
             'eye',
             'stone',
             'stone_desktop',
             'egg',
             'glass_rod',
             'salt',
             'mouth_bottle',
             'spoon',
             'clear',
             'pen',
             'zero']
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

