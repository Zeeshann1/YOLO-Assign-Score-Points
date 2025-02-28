from .comm import *
from .comm.course_base import ConfigModel
from torchvision import transforms
from aideModel import ClassMobilenetv3,ClassOpenvinoDetect
from PIL import Image
from configg.global_config import GLOBAL_is_user_all_model_type, GLOBAL_all_model_type_name, OPENVINO_VERSION
import os
class PHY_water_pressure_public(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_water_pressure_public, self).__init__()
        self.show_error = False
        self.show_img = False
        self.dis_all = -1
        self.start_dis = -2
        self.re_init_pure()
        self.re_init_salt()
        self.error_init()
        self.clear_img = []
        pt_path_ = 'aideModel/classModel/class_model_weights/class_model_3_v1.0.pt'
        if GLOBAL_is_user_all_model_type and GLOBAL_all_model_type_name == 'openvino':
            if OPENVINO_VERSION >= 2022:
                pt_path_ = pt_path_.replace('.pt', '_2022.xml')
            assert os.path.exists(pt_path_)
            self.classmodel = ClassOpenvinoDetect(
                str(Path(__file__).parent.parent / pt_path_),
                ['metal_box_down', 'metal_box_up', 'metal_box_vertical'])
        else:
            self.classmodel = ClassMobilenetv3(
                str(Path(__file__).parent.parent / pt_path_),
                ['metal_box_down', 'metal_box_up', 'metal_box_vertical'])
        self.save_score_1 = False
        self.save_score_2 = False
        self.save_score_3 = False
        self.save_score_4 = False
        self.save_score_5 = False
        self.save_score_6 = False
        self.save_score_7 = False
        self.save_score_8 = False
        self.save_score_9 = False
        self.save_score_10 = False
        self.save_score_11 = False
        self.save_score_12 = False
        self.save_score_13 = False

    def error_init(self):
        self.bl_2 = False
        self.j_1 = False
        self.j_time = None
        self.color_bucket = False
        self.nocolor_bucket = False
        self.error_count = 0
        self.error_save_score_1 = False
        self.error_water_select_img = []

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

    def re_init_pure(self):
        self.start_depth = False
        self.start_dir = False
        # 深度
        self.img_depth_1 = []
        self.img_depth_1_dis = 0.0
        self.img_depth_2 = []
        self.img_depth_2_dis = 0.0
        self.img_depth_3 = []
        self.img_depth_3_dis = 0.0
        # 方向
        self.img_down = []
        self.img_down_dis = 0.0
        self.img_vertical = []
        self.img_vertical_dis = 0.0
        self.img_up = []
        self.img_up_dis = 0.0
        self.save_pureimg_stop = False

        self.pure_2_dis = 40
        self.pure_3_dis = 40

    def re_init_salt(self):
        self.lab_start_depth = False
        self.lab_start_dir = False
        # 深度
        self.lab_img_depth_1 = []
        self.lab_img_depth_1_dis = 0.0
        self.lab_img_depth_2 = []
        self.lab_img_depth_2_dis = 0.0
        self.lab_img_depth_3 = []
        self.lab_img_depth_3_dis = 0.0
        # 方向
        self.lab_img_down = []
        self.lab_img_down_dis = 0.0
        self.lab_img_vertical = []
        self.lab_img_vertical_dis = 0.0
        self.lab_img_up = []
        self.lab_img_up_dis = 0.0
        self.save_saltimg_stop = False

        self.salt_2_dis = 40
        self.salt_3_dis = 40

    def fun_u_surfacew_dis(self, img, det, result_key):
        if len(det['u_water_surfacew']) < 2: return
        box_1 = det['u_water_surfacew'][0]
        box_2 = det['u_water_surfacew'][1]
        if box_1[0] == 0 or box_2[0] == 0:
            self.dis_all = -1
            return
        w_1, h_1, c_x_1, c_y_1 = box_1[2] - box_1[0], box_1[3] - box_1[1], (box_1[2] + box_1[0]) / 2, (
                box_1[3] + box_1[1]) / 2
        w_2, h_2, c_x_2, c_y_2 = box_2[2] - box_2[0], box_2[3] - box_2[1], (box_2[2] + box_2[0]) / 2, (
                box_2[3] + box_2[1]) / 2
        dis = abs(c_y_1 - c_y_2)
        self.dis_all = dis
        if self.start_dis == -2:
            self.start_dis = dis
        return

    def pure_water_depth(self, img, det, result_key):
        '''
        1、金属盒在水面下方且在水中
        2、金属盒小于水面时开始，间隔30取一个图保存
        '''
        metal_box = det['metal_box'][0]
        bucket_box = det['bucket'][0]
        bucket_face_box = det['bucket_water_surfacews'][0]
        bool_1 = self.box_include(metal_box, bucket_box)  # 金属盒在桶里面(全包含)
        bool_2 = bucket_face_box[3] < metal_box[1]
        bool_3 = self.iou(bucket_face_box[:4], metal_box[:4]) > 0 or bucket_face_box[3] > metal_box[1]
        if bool_3:
            self.start_depth = True
        if bool_1 and bool_2 and self.start_depth and len(self.img_depth_1) == 0:
            self.img_depth_1 = img
            self.img_depth_1_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.img_depth_1_dis = self.dis_all
            # cv2.imwrite(self.pp + 'img_depth_1.jpg', self.img_depth_1)
            # cv2.imshow(f'img_1 {str(self.dis_all)}',self.img_depth_1)
        if len(self.img_depth_1) != 0 and (self.dis_all - self.img_depth_1_dis) > self.pure_2_dis and len(self.img_depth_2) == 0:
            self.pure_2_dis = self.dis_all - self.img_depth_1_dis
            self.img_depth_2 = img
            self.img_depth_2_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.img_depth_2_dis = self.dis_all
            # cv2.imwrite(self.pp + 'img_depth_2.jpg', self.img_depth_2)
            # cv2.imshow(f'img_2 {str(self.dis_all)}', self.img_depth_2)
        if len(self.img_depth_2) != 0 and (self.dis_all - self.img_depth_2_dis) >  self.pure_3_dis and len(self.img_depth_3) == 0:
            self.pure_3_dis = self.dis_all - self.img_depth_2_dis
            self.img_depth_3 = img
            self.img_depth_3_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.img_depth_3_dis = self.dis_all
            # cv2.imwrite(self.pp + 'img_depth_3.jpg', self.img_depth_3)
            # cv2.imshow(f'img_3 {str(self.dis_all)}', self.img_depth_3)

    def pure_water_dis(self, img, det, result_key):
        '''
        1、金属盒在水面下方且在水中
        2、选择一个高度，默认保留5帧
        3、方向准换之后，高度差在30以内
        '''
        if not self.save_pureimg_stop:
            metal_box = det['metal_box'][0]
            bucket_box = det['bucket'][0]
            bucket_face_box = det['bucket_water_surfacews'][0]
            bool_1 = self.box_include(metal_box, bucket_box)  # 金属盒在桶里面(全包含)
            bool_2 = bucket_face_box[3] < metal_box[1]
            bool_3 = self.iou(bucket_face_box[:4], metal_box[:4]) > 0 or bucket_face_box[3] > metal_box[1]
            if bool_3:
                self.start_dir = True
            if bool_1 and bool_2 and self.start_dir:
                draw = img.copy()
                class_img = img[int(metal_box[1]):int(metal_box[3]), int(metal_box[0]):int(metal_box[2])]
                class_result = self.classmodel([class_img])
                lab = self.classmodel.label[int(class_result[0][-1])]
                # v = class_result[0][0]
                # if v < 0.9: return
                # cv2.imshow(lab, class_img)
                if 'metal_box_down' == lab:
                    self.img_down = img
                    self.img_down_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.img_down_dis = self.dis_all
                elif 'metal_box_vertical' == lab:
                    self.img_vertical = img
                    self.img_vertical_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.img_vertical_dis = self.dis_all
                elif 'metal_box_up' == lab:
                    self.img_up = img
                    self.img_up_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.img_up_dis = self.dis_all
                bool_4 = self.img_down_dis > 1 and self.img_vertical_dis > 1 and self.img_up_dis > 1
                bool_5 = abs(self.img_down_dis - self.img_vertical_dis) < 30 and abs(
                    self.img_down_dis - self.img_up_dis) < 30 and abs(self.img_vertical_dis - self.img_up_dis) < 30
                if bool_4 and bool_5:# and self.sim_fun(self.img_down, self.img_vertical, self.img_up):
                    self.save_pureimg_stop = True
                    # cv2.imwrite(self.pp + 'down.jpg', self.img_down)
                    # cv2.imwrite(self.pp + 'vertical.jpg', self.img_vertical)
                    # cv2.imwrite(self.pp + 'up.jpg', self.img_up)
                    # cv2.imshow('down',self.img_down)
                    # cv2.imshow('vertical', self.img_vertical)
                    # cv2.imshow('up', self.img_up)

    def salt_water_depth(self, img, det, result_key):
        '''
        1、金属盒在水面下方且在水中
        2、金属盒小于水面时开始，间隔30取一个图保存
        '''
        metal_box = det['metal_box'][0]
        bucket_box = det['bucket'][0]
        bucket_face_box = det['bucket_water_surfacews'][0]
        bool_1 = self.box_include(metal_box, bucket_box)  # 金属盒在桶里面(全包含)
        bool_2 = bucket_face_box[3] < metal_box[1]
        bool_3 = self.iou(bucket_face_box[:4], metal_box[:4]) > 0 or bucket_face_box[3] > metal_box[1]
        if bool_3:
            self.lab_start_depth = True
        if bool_1 and bool_2 and self.lab_start_depth and len(self.lab_img_depth_1) == 0:
            self.lab_img_depth_1 = img
            self.lab_img_depth_1_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.lab_img_depth_1_dis = self.dis_all
            # cv2.imwrite(self.pp + 'lab_img_depth_1.jpg', self.lab_img_depth_1)
            # cv2.imshow(f'img_1_lab {str(self.dis_all)}',self.lab_img_depth_1)
        if len(self.lab_img_depth_1) != 0 and (self.dis_all - self.lab_img_depth_1_dis) > self.salt_2_dis and len(
                self.lab_img_depth_2) == 0:
            self.salt_2_dis = self.dis_all - self.lab_img_depth_1_dis
            self.lab_img_depth_2 = img
            self.lab_img_depth_2_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.lab_img_depth_2_dis = self.dis_all
            # cv2.imwrite(self.pp + 'lab_img_depth_2.jpg', self.lab_img_depth_2)
            # cv2.imshow(f'img_2_lab {str(self.dis_all)}', self.lab_img_depth_2)
        if len(self.lab_img_depth_2) != 0 and (self.dis_all - self.lab_img_depth_2_dis) > self.salt_3_dis and len(
                self.lab_img_depth_3) == 0:
            self.salt_3_dis = self.dis_all - self.lab_img_depth_2_dis
            self.lab_img_depth_3 = img
            self.lab_img_depth_3_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            self.lab_img_depth_3_dis = self.dis_all
            # cv2.imwrite(self.pp + 'lab_img_depth_3.jpg', self.lab_img_depth_3)
            # cv2.imshow(f'img_3_lab {str(self.dis_all)}', self.lab_img_depth_3)

    def hist_similar(self, lh, rh):
        assert len(lh) == len(rh)
        hist = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)
        return hist

        # 计算相似度

    def calc_similar(self, li, ri):
        calc_sim = self.hist_similar(li.histogram(), ri.histogram())
        # print('calc_sim:', calc_sim)
        return calc_sim

    def sim_fun(self, img1, img2, img3):
        smi_num = 0.8
        if len(img1) != 0 and len(img2) != 0 and len(img3) != 0:
            img1 = Image.fromarray(cv2.cvtColor(cv2.resize(img1, (64, 64)), cv2.COLOR_BGR2RGB))
            img2 = Image.fromarray(cv2.cvtColor(cv2.resize(img2, (64, 64)), cv2.COLOR_BGR2RGB))
            img3 = Image.fromarray(cv2.cvtColor(cv2.resize(img3, (64, 64)), cv2.COLOR_BGR2RGB))
            smi_12 = self.calc_similar(img1, img2)
            smi_23 = self.calc_similar(img2, img3)
            smi_13 = self.calc_similar(img1, img3)
            if smi_12 < smi_num and smi_23 < smi_num and smi_13 < smi_num:
                return True
            return False
        elif len(img1) != 0 and len(img2) != 0 and len(img3) == 0:
            img1 = Image.fromarray(cv2.cvtColor(cv2.resize(img1, (64, 64)), cv2.COLOR_BGR2RGB))
            img2 = Image.fromarray(cv2.cvtColor(cv2.resize(img2, (64, 64)), cv2.COLOR_BGR2RGB))
            smi_12 = self.calc_similar(img1, img2)
            if smi_12 < smi_num:
                return True
            return False
        elif len(img1) != 0 and len(img2) == 0 and len(img3) != 0:
            img1 = Image.fromarray(cv2.cvtColor(cv2.resize(img1, (64, 64)), cv2.COLOR_BGR2RGB))
            img3 = Image.fromarray(cv2.cvtColor(cv2.resize(img3, (64, 64)), cv2.COLOR_BGR2RGB))
            smi_13 = self.calc_similar(img1, img3)
            if smi_13 < smi_num:
                return True
            return False
        elif len(img1) == 0 and len(img2) != 0 and len(img3) != 0:
            img2 = Image.fromarray(cv2.cvtColor(cv2.resize(img2, (64, 64)), cv2.COLOR_BGR2RGB))
            img3 = Image.fromarray(cv2.cvtColor(cv2.resize(img3, (64, 64)), cv2.COLOR_BGR2RGB))
            smi_23 = self.calc_similar(img2, img3)
            if smi_23 < smi_num:
                return True
            return False
        else:
            return False

    def salt_water_dis(self, img, det, result_key):
        '''
        1、金属盒在水面下方且在水中
        2、选择一个高度，默认保留5帧
        3、方向准换之后，高度差在30以内
        '''
        if not self.save_saltimg_stop:
            metal_box = det['metal_box'][0]
            bucket_box = det['bucket'][0]
            bucket_face_box = det['bucket_water_surfacews'][0]
            bool_1 = self.box_include(metal_box, bucket_box)  # 金属盒在桶里面(全包含)
            bool_2 = bucket_face_box[3] < metal_box[1]
            bool_3 = self.iou(bucket_face_box[:4], metal_box[:4]) > 0 or bucket_face_box[3] > metal_box[1]
            if bool_3:
                self.lab_start_dir = True
            if bool_1 and bool_2 and self.lab_start_dir:
                draw = img.copy()
                class_img = img[int(metal_box[1]):int(metal_box[3]), int(metal_box[0]):int(metal_box[2])]
                class_result = self.classmodel([class_img])
                lab = self.classmodel.label[int(class_result[0][-1])]
                # v = class_result[0][0]
                # if v < 0.9: return
                # cv2.imshow(lab, class_img)
                if 'metal_box_down' == lab:
                    self.lab_img_down = img
                    self.lab_img_down_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.lab_img_down_dis = self.dis_all
                elif 'metal_box_vertical' == lab:
                    self.lab_img_vertical = img
                    self.lab_img_vertical_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.lab_img_vertical_dis = self.dis_all
                elif 'metal_box_up' == lab:
                    self.lab_img_up = img
                    self.lab_img_up_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.lab_img_up_dis = self.dis_all
                bool_4 = self.lab_img_down_dis > 1 and self.lab_img_vertical_dis > 1 and self.lab_img_up_dis > 1
                bool_5 = abs(self.lab_img_down_dis - self.lab_img_vertical_dis) < 30 and abs(
                    self.lab_img_down_dis - self.lab_img_up_dis) < 30 and abs(
                    self.lab_img_vertical_dis - self.lab_img_up_dis) < 30
                if bool_4 and bool_5:# and self.sim_fun(self.lab_img_down, self.lab_img_vertical, self.lab_img_up):
                    self.save_saltimg_stop = True
                    # cv2.imwrite(self.pp + 'down_lab.jpg', self.lab_img_down)
                    # cv2.imwrite(self.pp + 'vertical_lab.jpg', self.lab_img_vertical)
                    # cv2.imwrite(self.pp + 'up_lab.jpg', self.lab_img_up)
                    # cv2.imshow('down_lab',self.lab_img_down)
                    # cv2.imshow('vertical_lab', self.lab_img_vertical)
                    # cv2.imshow('up_lab', self.lab_img_up)

    def fun_clear(self, img, det, result_key):
        if len(self.img_depth_1) != 0 and len(self.lab_img_depth_1) != 0:
            w_dis = img.shape[1] / 4
            bool_1 = 'bucket_water_column' not in result_key and 'bucket_water_surfacew' not in result_key
            if bool_1:
                self.clear_img = img.copy()
                self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                return
            if 'bucket' in result_key:
                box = det['bucket'][0]
            elif 'bucket_water_column' in result_key:
                box = det['bucket_water_column'][0]
            elif 'bucket_water_column' in result_key:
                box = det['bucket_water_column'][0]
            else:
                box = []
            if len(box) > 0:
                w = (box[0] + box[2]) / 2
                if w > w_dis * 3 or w < w_dis:
                    self.clear_img = img.copy()
                    self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    return

    def error_water_select(self,img, det, result_key):
        if 'bucket' in result_key and 'metal_box' in result_key and 'bucket_water_column' in result_key:
            bucket_box = det['bucket'][0]
            metal_box_box = det['metal_box'][0]
            bucket_water_box = det['bucket_water_column'][0]
            bool_1 = self.box_include(bucket_box[:4],metal_box_box[:4]) and self.box_include(bucket_water_box[:4],metal_box_box[:4])
            if bool_1 and not self.j_1:
                self.j_1 = True
                self.j_time = time.time()
                if 'color_label' in result_key:
                    self.color_bucket = True
                else:
                    self.nocolor_bucket = True
            if self.j_time is not None and not self.bl_2:
                if self.j_1 and (time.time()-self.j_time)>2:#相交10s之后，在判断金属盒是否离开水桶：
                    self.bl_2 = self.iou(bucket_box[:4], metal_box_box[:4])==0 or self.iou(
                        bucket_water_box[:4], metal_box_box[:4])==0
            if self.bl_2 and bool_1:
                if ('color_label' in result_key and self.color_bucket) or ('color_label' not in result_key and self.nocolor_bucket):
                    self.error_water_select_img = img
                    self.error_water_select_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]



        #     else:
        #         return
        # if self.save_pureimg_stop and not self.save_saltimg_stop:
        #     if 'color_label' not in result_key and 'bucket' in result_key:
        #         self.error_count+=1
        #     if self.error_count>100:
        #         self.error_water_select_img = img
        #         self.error_water_select_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        # elif not self.save_pureimg_stop and self.save_saltimg_stop:
        #     if 'color_label' in result_key and 'bucket' in result_key:
        #         self.error_count+=1
        #     if self.error_count>100:
        #         self.error_water_select_img = img
        #         self.error_water_select_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        # elif not self.save_pureimg_stop and not self.save_saltimg_stop:
        #     pass
        # else:
        #     pass

    def error_save_score_fun(self):
        if len(self.error_water_select_img) != 0 and not self.error_save_score_1:
            self.assignScore(
                index=1,
                img=self.error_water_select_img.copy(),
                object=self.error_water_select_img_list[0],
                conf=0.1,
                time_frame=self.error_water_select_img_list[1],
                num_frame=self.error_water_select_img_list[2],
                name_save="1_error.jpg",
                preds=self.error_water_select_img_list[3])
            self.error_save_score_1 = True


    def save_score_fun(self, frame_front, preds, objects, time, num_frame, type='win'):
        # print(preds)
        # print(objects)
        if len(self.img_depth_1) != 0 and not self.save_score_1:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '1.jpg', self.img_depth_1)
            else:
                self.assignScore(
                    index=1,
                    img=self.img_depth_1.copy(),
                    object=self.img_depth_1_list[0],
                    conf=0.1,
                    time_frame=self.img_depth_1_list[1],
                    num_frame=self.img_depth_1_list[2],
                    name_save="1.jpg",
                    preds=self.img_depth_1_list[3])
            self.save_score_1 = True
        if len(self.img_depth_2) != 0 and not self.save_score_2:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '2.jpg', self.img_depth_2)
            else:
                self.assignScore(
                    index=2,
                    img=self.img_depth_2.copy(),
                    object=self.img_depth_2_list[0],
                    conf=0.1,
                    time_frame=self.img_depth_2_list[1],
                    num_frame=self.img_depth_2_list[2],
                    name_save="2.jpg",
                    preds=self.img_depth_2_list[3])
            self.save_score_2 = True
        if len(self.img_depth_3) != 0 and not self.save_score_3:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '3.jpg', self.img_depth_3)
            else:
                self.assignScore(
                    index=3,
                    img=self.img_depth_3.copy(),
                    object=self.img_depth_3_list[0],
                    conf=0.1,
                    time_frame=self.img_depth_3_list[1],
                    num_frame=self.img_depth_3_list[2],
                    name_save="3.jpg",
                    preds=self.img_depth_3_list[3])
            self.save_score_3 = True
        if self.save_pureimg_stop:
            if len(self.img_down) != 0 and not self.save_score_4:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '4.jpg', self.img_down)
                else:
                    self.assignScore(
                        index=4,
                        img=self.img_down.copy(),
                        object=self.img_down_list[0],
                        conf=0.1,
                        time_frame=self.img_down_list[1],
                        num_frame=self.img_down_list[2],
                        name_save="4.jpg",
                        preds=self.img_down_list[3])
                self.save_score_4 = True
            if len(self.img_vertical) != 0 and not self.save_score_5:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '5.jpg', self.img_vertical)
                else:
                    self.assignScore(
                        index=5,
                        img=self.img_vertical.copy(),
                        object=self.img_vertical_list[0],
                        conf=0.1,
                        time_frame=self.img_vertical_list[1],
                        num_frame=self.img_vertical_list[2],
                        name_save="5.jpg",
                        preds=self.img_vertical_list[3])
                self.save_score_5 = True
            if len(self.img_up) != 0 and not self.save_score_6:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '6.jpg', self.img_up)
                else:
                    self.assignScore(
                        index=6,
                        img=self.img_up.copy(),
                        object=self.img_up_list[0],
                        conf=0.1,
                        time_frame=self.img_up_list[1],
                        num_frame=self.img_up_list[2],
                        name_save="6.jpg",
                        preds=self.img_up_list[3])
                self.save_score_6 = True
        if len(self.lab_img_depth_1) != 0 and not self.save_score_7:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '7.jpg', self.lab_img_depth_1)
            else:
                self.assignScore(
                    index=7,
                    img=self.lab_img_depth_1.copy(),
                    object=self.lab_img_depth_1_list[0],
                    conf=0.1,
                    time_frame=self.lab_img_depth_1_list[1],
                    num_frame=self.lab_img_depth_1_list[2],
                    name_save="7.jpg",
                    preds=self.lab_img_depth_1_list[3])
            self.save_score_7 = True
        if len(self.lab_img_depth_2) != 0 and not self.save_score_8:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '8.jpg', self.lab_img_depth_2)
            else:
                self.assignScore(
                    index=8,
                    img=self.lab_img_depth_2.copy(),
                    object=self.lab_img_depth_2_list[0],
                    conf=0.1,
                    time_frame=self.lab_img_depth_2_list[1],
                    num_frame=self.lab_img_depth_2_list[2],
                    name_save="8.jpg",
                    preds=self.lab_img_depth_2_list[3])
            self.save_score_8 = True
        if len(self.lab_img_depth_3) != 0 and not self.save_score_9:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '9.jpg', self.lab_img_depth_3)
            else:
                self.assignScore(
                    index=9,
                    img=self.lab_img_depth_3.copy(),
                    object=self.lab_img_depth_3_list[0],
                    conf=0.1,
                    time_frame=self.lab_img_depth_3_list[1],
                    num_frame=self.lab_img_depth_3_list[2],
                    name_save="9.jpg",
                    preds=self.lab_img_depth_3_list[3])
            self.save_score_9 = True
        if self.save_saltimg_stop:
            if len(self.lab_img_down) != 0 and not self.save_score_10:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '10.jpg', self.lab_img_down)
                else:
                    self.assignScore(
                        index=10,
                        img=self.lab_img_down.copy(),
                        object=self.lab_img_down_list[0],
                        conf=0.1,
                        time_frame=self.lab_img_down_list[1],
                        num_frame=self.lab_img_down_list[2],
                        name_save="10.jpg",
                        preds=self.lab_img_down_list[3])
                self.save_score_10 = True
            if len(self.lab_img_vertical) != 0 and not self.save_score_11:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '11.jpg', self.lab_img_vertical)
                else:
                    self.assignScore(
                        index=11,
                        img=self.lab_img_vertical.copy(),
                        object=self.lab_img_vertical_list[0],
                        conf=0.1,
                        time_frame=self.lab_img_vertical_list[1],
                        num_frame=self.lab_img_vertical_list[2],
                        name_save="11.jpg",
                        preds=self.lab_img_vertical_list[3])
                self.save_score_11 = True
            if len(self.lab_img_up) != 0 and not self.save_score_12:
                if time is None and type != 'win':
                    cv2.imwrite(self.save_path + '12.jpg', self.lab_img_up)
                else:
                    self.assignScore(
                        index=12,
                        img=self.lab_img_up.copy(),
                        object=self.lab_img_up_list[0],
                        conf=0.1,
                        time_frame=self.lab_img_up_list[1],
                        num_frame=self.lab_img_up_list[2],
                        name_save="12.jpg",
                        preds=self.lab_img_up_list[3])
                self.save_score_12 = True
        if len(self.clear_img) != 0 and not self.save_score_13:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '13.jpg', self.clear_img)
            else:
                self.assignScore(
                    index=13,
                    img=self.clear_img.copy(),
                    object=self.clear_img_list[0],
                    conf=0.1,
                    time_frame=self.clear_img_list[1],
                    num_frame=self.clear_img_list[2],
                    name_save="13.jpg",
                    preds=self.clear_img_list[3])
            self.save_score_13 = True

    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        bool_all_1 = 'u_water_surfacew' in result_key
        if bool_all_1:
            self.fun_u_surfacew_dis(img0s.copy(), det, result_key)
            if 'bucket' in result_key and 'metal_box' in result_key and 'bucket_water_surfacews' in result_key and 'bucket_water_column' in result_key:
                bucket_box = det['bucket'][0]
                metal_box = det['metal_box'][0]
                bool_1 = self.iou(bucket_box[:4], metal_box[:4]) > 0
                if bool_1 and 'color_label' in result_key and 'bucket' in result_key:
                    color_box = det['color_label'][0]
                    bucket_box = det['bucket'][0]
                    if self.iou(color_box[:4], bucket_box[:4]) > 0:
                        # 盐水
                        self.salt_water_depth(img0s.copy(), det, result_key)
                        self.salt_water_dis(img0s.copy(), det, result_key)
                    else:
                        # 清水
                        self.pure_water_depth(img0s.copy(), det, result_key)
                        self.pure_water_dis(img0s.copy(), det, result_key)
                elif bool_1 and 'color_label' not in result_key and 'bucket' in result_key:
                    # 清水
                    self.pure_water_depth(img0s.copy(), det, result_key)
                    self.pure_water_dis(img0s.copy(), det, result_key)
                else:
                    pass
        else:
            self.dis_all = -1
        if len(self.img_depth_1) != 0 and len(self.img_depth_1) != 0:
            self.fun_clear(img0s.copy(), det, result_key)
        if self.show_error:
            self.error_water_select(img0s.copy(), det, result_key)
            self.error_save_score_fun()
        self.save_score_fun(img0s, preds, objects, time, num_frame)

    def process_dict(self, d):
        for key in list(d.keys()):
            if len(d[key]) > 1 and 'hand' != key and 'u_water_surfacew' != key:
                d[key].sort(key=self.sortlist, reverse=True)
                d[key] = [d[key][0]]
            if 'hand' == key or 'u_water_surfacew' == key:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    bbox = d[key][:1]
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
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
            names_label = ['towel',
                     'bucket',
                     'hand',
                     'bucket_water_surfacews',
                     'bucket_water_column',
                     'u_water_surfacew',
                     'u',
                     'u_interface',
                     'metal_box',
                     'clip',
                     'knob',
                     'color_label',
                     'clear']
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
            if self.show_img:
                self.plot(front_preds, frame_front)
                frame_front = cv2.resize(frame_front, (640, 384))
                cv2.imshow('1', frame_front)
                cv2.waitKey(1)

        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=top_preds, front_preds=front_preds, side_preds=side_preds)
