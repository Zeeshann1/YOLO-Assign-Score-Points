from configg import GLOBAL_is_user_all_model_type,GLOBAL_all_model_type_name,OPENVINO_VERSION
from .comm import *
from .comm.course_base import ConfigModel
from aideModel import ClassMobilenetv3,ClassOpenvinoDetect
from aideModel import HrnentKeyPoint, HRliteOpenvinoDetect
import os

class PHY_small_light_test_power_pubilc(ConfigModel):

    def __init__(
            self
    ):
        super(PHY_small_light_test_power_pubilc, self).__init__()
        self.show_error = False
        self.show_img=False
        self.re_init()
        self.re_init_error()
        classmodel_path = 'aideModel/classModel/class_model_weights/class_model_8_v1.0.pt'
        keymodel_path = 'aideModel/pointModel/weights/switch_keypoint.pt'
        if GLOBAL_is_user_all_model_type and GLOBAL_all_model_type_name == 'openvino':
            if OPENVINO_VERSION > 2021:
                classmodel_path = classmodel_path.replace('.pt', '_2022.xml')
                keymodel_path = keymodel_path.replace('.pt', '_2022.xml')
            else:
                classmodel_path = classmodel_path.replace('.pt', '.xml')
                keymodel_path = keymodel_path.replace('.pt', '.xml')
            assert os.path.exists(classmodel_path) and os.path.exists(keymodel_path)
            self.classmodel = ClassOpenvinoDetect(model_path=classmodel_path,
                                                  lab=['light_non', 'metal_box_down', 'metal_box_up', 'light_dim',
                                                       'switch_on', 'light_bright',
                                                       'metal_box_upright', 'switch_off'])
            self.keypoint_infer = HRliteOpenvinoDetect(
                modelpath=keymodel_path)

        else:
            assert os.path.exists(classmodel_path) and os.path.exists(keymodel_path)
            self.classmodel = ClassMobilenetv3(
                model_path=classmodel_path,
                lab=['light_non', 'metal_box_down', 'metal_box_up', 'light_dim', 'switch_on', 'light_bright',
                     'metal_box_upright', 'switch_off'])
            self.keypoint_infer = HrnentKeyPoint(
                modelpath=keymodel_path)

    def dis_point(self, p1, p2):
        p1 = [(p1[:4][0] + p1[:4][2]) / 2, (p1[:4][1] + p1[:4][3]) / 2]
        p2 = [(p2[:4][0] + p2[:4][2]) / 2, (p2[:4][1] + p2[:4][3]) / 2]
        x_d = p1[0] - p2[0]
        y_d = p1[1] - p2[1]
        # 用math.sqrt（）求平方根
        return math.sqrt((x_d ** 2) + (y_d ** 2))

    def dis_point_(self, p1, p2):
        w1, h1 = p1[2] - p1[0], p1[3] - p1[1]
        w2, h2 = p2[2] - p2[0], p2[3] - p2[1]
        min_dis = min(w1, h1, w2, h2)
        p1 = [p1[:4][2], (p1[:4][1] + p1[:4][3]) / 2]
        p2 = [p2[:4][2], (p2[:4][1] + p2[:4][3]) / 2]
        x_d = p1[0] - p2[0]
        y_d = p1[1] - p2[1]
        return math.sqrt((x_d ** 2) + (y_d ** 2)), min_dis

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

    def re_init(self):
        # self.line_infer = Predict()
        # self.switch_point_infer = LiteHrnetPredict()
        # 每个器件的连接状态
        self.single_p = False
        self.single_a = False
        self.single_v = False
        self.single_s = False
        self.single_l = False
        self.single_l_two = False
        self.single_r = False
        # 串联电路
        self.tandem_img = []
        self.tandem_img_bool = False
        self.parallel_img = []
        self.parallel_img_bool = False
        # 灯泡亮度阈值，去一个最大得分
        self.light_class_th = 0.9
        self.light_img = []
        self.light_bool = False
        # 判断滑动变阻器是不是同上同下
        self.r_up_img = []
        self.r_down_img = []
        self.r_up_down_img = []
        # 开关状态
        self.s_status_lab = ''
        # 滑动变阻器滑片滑到阻值最大
        self.r_max = False
        self.r_max_img = []
        self.r_location = []

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
        self.save_score_14 = False

        self.vo_pos_in_img = []
        self.vo_pointer_img = []
        self.vo_pointer_img_bool = False
        self.am_pos_in_img = []
        self.am_pointer_img = []
        self.am_pointer_img_bool = False
        self.clear_img = []
        self.clear_stop = False
        self.switch_disconnect_img_1 = []
        self.switch_disconnect_img_1_bool = False
        self.switch_closure_img_1 = []
        self.switch_disconnect_img_2 = []
        self.switch_closure_img_2 = []
        self.vo_min_img = []
        self.vo_max_img = []
        self.am_min_img = []
        self.am_max_img = []
        self.vo_min_bool = False
        self.am_min_bool = False
    def re_init_error(self):
        self.error_vo_c_img = []
        self.error_am_two_img =[]
        self.error_r_tong_up_img = []
        self.error_r_tong_down_img = []

        self.error_save_score_1 = False
        self.error_save_score_2 = False
        self.error_save_score_3 = False
        self.error_save_score_4 = False
        self.error_save_score_5 = False
        self.error_save_score_6 = False
        self.error_save_score_7 = False


    def fun_get_img(self, img0s, det, re_key):
        top_key = []
        top_det = []
        top_img = []
        front_key = []
        front_det = []
        front_img = []
        side_key = []
        side_det = []
        side_img = []
        if img0s['top'] is not None:
            top_img = img0s['top'].copy()
        if det['top'] is not None:
            top_det = det['top']
            top_key = re_key['top']
        if img0s['front'] is not None:
            front_img = img0s['front'].copy()
        if det['front'] is not None:
            front_det = det['front']
            front_key = re_key['front']
        if img0s['side'] is not None:
            side_img = img0s['side'].copy()
        if det['side'] is not None:
            side_det = det['side']
            side_key = re_key['side']
        return top_key, top_det, top_img, front_key, front_det, front_img, side_key, side_det, side_img

    # def find_max_region(self,mask_sel):
    #     contours, hierarchy = cv2.findContours(mask_sel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     # 找到最大区域并填充
    #     area = []
    #
    #     for j in range(len(contours)):
    #         area.append(cv2.contourArea(contours[j]))
    #     inds = np.argsort(area)[-2:]
    #     if inds.shape[0] <2:return []
    #     box1 = cv2.minAreaRect(contours[inds[0]])#（x，y），（宽度，高度），旋转角度
    #     x1,y1,x2,y2 = box1[0][0],box1[0][1],box1[0][0]+box1[1][0],box1[0][1]+box1[1][0]
    #     box2 = cv2.minAreaRect(contours[inds[1]])
    #     x3, y3, x4, y4 = box2[0][0],box2[0][1],box2[0][0]+box2[1][0],box2[0][1]+box2[1][0]
    #     return [[x1,y1,x2,y2,(x1+x2)/2,(y1+y2)/2],[x3, y3, x4, y4,(x3+x4)/2,(y3+y4)/2]]
    # def fun_line(self, img, det, result_key):
    #     img_res = self.line_infer(img)
    #     w,h = self.line_infer.resize[0],self.line_infer.resize[1]
    #     max_class = img_res.max()
    #     mask = np.zeros((img_res.shape[0], img_res.shape[1])).astype('uint8')
    #     d = 0
    #     ww,hh = 1920,1080
    #     if 'wire_binding' in result_key:
    #         power_red_box = np.array(det['wire_binding'])
    #         power_red_box[:, [0, 2]] = power_red_box[:, [0, 2]]/ww*w
    #         power_red_box[:, [1, 3]] = power_red_box[:, [1, 3]] / hh * h
    #         for i in range(len(power_red_box)):
    #             x1,y1,x2,y2 = int(power_red_box[i][0]),int(power_red_box[i][1]),int(power_red_box[i][2]),int(power_red_box[i][3])
    #             cv2.rectangle(mask, (x1-d,y1+d), (x2-d,y2+d), (255, 255, 255), thickness=-1)
    #     if 'voltmeter_blue_wire_binding' in result_key:
    #         power_red_box = np.array(det['voltmeter_blue_wire_binding'])
    #         power_red_box[:, [0, 2]] = power_red_box[:, [0, 2]]/ww*w
    #         power_red_box[:, [1, 3]] = power_red_box[:, [1, 3]] / hh * h
    #         for i in range(len(power_red_box)):
    #             x1,y1,x2,y2 = int(power_red_box[i][0]),int(power_red_box[i][1]),int(power_red_box[i][2]),int(power_red_box[i][3])
    #             cv2.rectangle(mask, (x1-d,y1+d), (x2-d,y2+d), (255, 255, 255), thickness=-1)
    #     if 'ammeter_wire_binding' in result_key:
    #         power_red_box = np.array(det['ammeter_wire_binding'])
    #         power_red_box[:, [0, 2]] = power_red_box[:, [0, 2]]/ww*w
    #         power_red_box[:, [1, 3]] = power_red_box[:, [1, 3]] / hh * h
    #         for i in range(len(power_red_box)):
    #             x1,y1,x2,y2 = int(power_red_box[i][0]),int(power_red_box[i][1]),int(power_red_box[i][2]),int(power_red_box[i][3])
    #             cv2.rectangle(mask, (x1-d,y1+d), (x2-d,y2+d), (255, 255, 255), thickness=-1)
    #     if 'wire_binding' in result_key:
    #         power_red_box = np.array(det['wire_binding'])
    #         power_red_box[:, [0, 2]] = power_red_box[:, [0, 2]]/ww*w
    #         power_red_box[:, [1, 3]] = power_red_box[:, [1, 3]] / hh * h
    #         for i in range(len(power_red_box)):
    #             x1,y1,x2,y2 = int(power_red_box[i][0]),int(power_red_box[i][1]),int(power_red_box[i][2]),int(power_red_box[i][3])
    #             cv2.rectangle(mask, (x1-d,y1+d), (x2-d,y2+d), (255, 255, 255), thickness=-1)
    #     if 'rheostat_up' in result_key:
    #         rheostat_blue_box = det['rheostat_up'][0]
    #         x5, y5, x6, y6 = int(rheostat_blue_box[0]), int(rheostat_blue_box[1]), int(rheostat_blue_box[2]), int(
    #             rheostat_blue_box[3])
    #         cv2.rectangle(mask, (x5-d, y5+d), (x6-d, y6+d), (255, 255, 255), thickness=-1)
    #     if 'rheostat_down' in result_key:
    #         rheostat_yellow_box = det['rheostat_down'][0]
    #         x7, y7, x8, y8 = int(rheostat_yellow_box[0]), int(rheostat_yellow_box[1]), int(rheostat_yellow_box[2]), int(
    #             rheostat_yellow_box[3])
    #         cv2.rectangle(mask, (x7-d, y7+d), (x8-d, y8+d), (255, 255, 255), thickness=-1)
    #     rect_1 = []
    #     #######################################角点检测##########################################
    #     # for i in range(1,max_class):
    #     #     mask_ = img_res.copy()
    #     #     mask__ = mask.copy()
    #     #     mask_[mask_ != i] = 0
    #     #     mask_[mask_==i]= 255
    #     #     #角点检测算法
    #     #     corners = cv2.goodFeaturesToTrack(mask_, 2, 0.01, 1)
    #     #     if corners is not None:
    #     #         corners[:, :, 0] = corners[:,:,0]/ w * ww
    #     #         corners[:, :,1] = corners[:, :, 1] / h * hh
    #     #         x1,y1,x2,y2 = corners[0][0][0],corners[0][0][1],corners[1][0][0],corners[1][0][1]
    #     #         rect_1.append([x1,y1,x2,y2,i])
    #     #         img = cv2.circle(img, (int(x1), int(y1)), 3, (0, 0, 255), 1)
    #     #         img = cv2.circle(img, (int(x2), int(y2)), 3, (0, 0, 255),1)
    #     #         img = cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)),
    #     #                        (0, 0, 255), 3)
    #     #         img = cv2.putText(img, str(i), (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1.2,(0, 0, 255), 2)
    #     #         img = cv2.putText(img, str(i), (int(x2), int(y2)), cv2.FONT_HERSHEY_SIMPLEX, 1.2,(255, 255, 255), 2)
    #     ########################################利用接线柱检测区分##########################################
    #     # img_res = cv2.dilate(img_res, np.ones((5,5),np.uint8))
    #     for i in range(1, max_class):
    #         mask_ = img_res.copy()
    #         mask__ = mask.copy()
    #         mask_[mask_ != i] = 0
    #         mask_[mask_ == i] = 255
    #         ii = cv2.bitwise_and(mask_,mask__)
    #         cv2.imshow('1', mask_)
    #         cv2.imshow('2', mask__)
    #         cv2.imshow('3', ii)
    #         rect_1 = self.find_max_region(ii)
    #         if len(rect_1)!=0:
    #             rect_1 = np.array(rect_1)
    #             rect_1[:, [0, 2, 4]] = rect_1[:, [0, 2, 4]] / w * ww
    #             rect_1[:, [1, 3, 5]] = rect_1[:, [1, 3, 5]] / h * hh
    #             img = cv2.circle(img,(int(rect_1[0][4]),int(rect_1[0][5])),3,(0,0,255),1)
    #             img = cv2.circle(img,(int(rect_1[1][4]), int(rect_1[1][5])), 3, (0, 0, 255),1)
    #             img = cv2.line(img,  (int(rect_1[0][4]),int(rect_1[0][5])),(int(rect_1[1][4]), int(rect_1[1][5])), (0, 0, 255), 3)
    #             img = cv2.putText(img, str(i),(int(rect_1[0][4]),int(rect_1[0][5])), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
    #             img = cv2.putText(img, str(i),(int(rect_1[1][4]), int(rect_1[1][5])), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
    #                               (255, 255, 255), 2)
    #     #
    #     cv2.imshow('4', img)
    #     cv2.waitKey(0)
    #     # print(rect_1)
    #     return rect_1
    # def filter_det(self, img, det, result_key):
    #     if 'ammeter' in result_key and 'wire_binding' in result_key:
    #         ammeter_box = det['ammeter'][0]
    #         am_wire_binding_boxs = det['wire_binding']
    #         box_ = []
    #         am_pop_ = []
    #         for i in range(len(am_wire_binding_boxs)):
    #             box = am_wire_binding_boxs[i]
    #             if self.iou(ammeter_box[:4], box[:4]) > 0:
    #                 box_.append(box)
    #                 am_pop_.append(i)
    #             if len(box_) == 2:
    #                 break
    #         for ii in range(len(am_pop_)):
    #             am_wire_binding_boxs.pop(ii)
    #         if len(box_) != 0:
    #             det['ammeter_wire_binding'] = box_
    #         if len(am_wire_binding_boxs) > 0:
    #             det['wire_binding'] = am_wire_binding_boxs
    #         else:
    #             det.pop('wire_binding')
    #     if 'voltmeter_blue' in result_key and 'wire_binding' in result_key:
    #         voltmeter_blue_box = det['voltmeter_blue'][0]
    #         vo_b_wire_binding_boxs = det['wire_binding']
    #         box_ = []
    #         vo_b_pop_ = []
    #         for j in range(len(vo_b_wire_binding_boxs)):
    #             box = vo_b_wire_binding_boxs[j]
    #             if self.iou(voltmeter_blue_box[:4],box[:4])>0:
    #                 box_.append(box)
    #                 vo_b_pop_.append(j)
    #             if len(box_)==2:
    #                 break
    #         for jj in range(len(vo_b_pop_)):
    #             vo_b_wire_binding_boxs.pop(jj)
    #         if len(box_)!=0:
    #             det['voltmeter_blue_wire_binding'] = box_
    #         if len(vo_b_wire_binding_boxs)>0:
    #             det['wire_binding'] = vo_b_wire_binding_boxs
    #         else:
    #             det.pop('wire_binding')
    #     if 'voltmeter' in result_key and 'wire_binding' in result_key:
    #         voltmeter_box = det['voltmeter'][0]
    #         vo_wire_binding_boxs = det['wire_binding']
    #         box_ = []
    #         vo_pop_ = []
    #         for k in range(len(vo_wire_binding_boxs)):
    #             box = vo_wire_binding_boxs[k]
    #             if self.iou(voltmeter_box[:4], box[:4]) > 0:
    #                 box_.append(box)
    #                 vo_pop_.append(k)
    #             if len(box_) == 2:
    #                 break
    #         for kk in range(len(vo_pop_)):
    #             vo_wire_binding_boxs.pop(kk)
    #         if len(box_) != 0:
    #             det['voltmeter_wire_binding'] = box_
    #         if len(vo_wire_binding_boxs) > 0:
    #             det['wire_binding'] = vo_wire_binding_boxs
    #         else:
    #             det.pop('wire_binding')
    #     return det,list(det.keys())
    # def fun_line_filter(self, img, det, result_key):
    #     rect_ = self.fun_line(img, det, result_key)
    #     aa = []
    #     list_1=[]
    #     for i in range(len(rect_)):
    #         x1,y1,x2,y2,c_x,c_y = rect_[i]
    #         list_2 = []
    #         for key in result_key:
    #             if key not in ['power_source','ammeter','slide_rheostat','voltmeter','switch','light_']:continue
    #             box_1 = det[key]
    #             list_3 = []
    #             for j in range(len(box_1)):
    #                 x3,y3,x4,y4,v = box_1[j]
    #                 if x3<=x1<=x4 and y3<=y1<=y4:
    #                     list_3.append([x1,y1,key,x3,y3,x4,y4,v])
    #                 elif x3<=x2<=x4 and y3<=y2<=y4:
    #                     list_3.append([x2,y2,key,x3,y3,x4,y4,v])
    #                 if len(list_3)!=0:
    #                     list_2.append(list_3)
    #                     break
    #             if len(list_2)==2:
    #                 list_1.append(list_2)
    #                 list_2 = []
    #     return list_1
    # def fun_switch_point(self, img, det, result_key):
    #     if 'switch_on' in result_key:
    #         switch_box = det['switch_on'][0]
    #     elif 'switch_off' in result_key:
    #         switch_box = det['switch_off'][0]
    #     else:
    #         switch_box = []
    #     if len(switch_box)!=0:
    #         x1, y1, x2, y2 = int(switch_box[0]), int(switch_box[1]), int(switch_box[2]),int(switch_box[3])
    #         im = img[y1:y2,x1:x2]
    #         self.switch_point_infer(im)
    #         # self.switch_point_infer()
    ########################################################################

    # 连接状态
    def is_conn(self, box1, box2, type=''):
        dict_1 = {}
        count = 0
        for i in range(len(box1)):
            for j in range(len(box2)):
                bool_1 = self.iou(box1[i][:4], box2[j][:4]) > 0
                if bool_1:
                    dict_1[type + str(count)] = [box1[i], box2[j]]
                    count += 1
        key_count = list(dict_1.keys())
        if (type == 'r_up_' or type == 'r_down_') and len(key_count) == 1:
            return True, dict_1
        elif type != 'r_up_' and type != 'r_down_' and len(key_count) > 1:
            return True, dict_1
        else:
            return False, dict_1

    def power_con(self, img, det, result_key):
        power_box = det['power_source']
        con_box = det['wire_binding']
        bool_1, dict_1 = self.is_conn(power_box, con_box, 'power_')
        return bool_1

    def am_con(self, img, det, result_key):
        am_box = det['ammeter']
        con_box = det['wire_binding']
        bool_1, dict_1 = self.is_conn(am_box, con_box, 'am_')
        key = list(dict_1.keys())
        # if bool_1 and len(self.am_min_img) == 0:
        #     self.am_min_img = img.copy()
        #     self.am_min_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        if 'am_0' in key and 'am_1' in key and not self.am_min_bool:
            if self.iou(dict_1['am_0'][-1][:4], dict_1['am_1'][-1][:4]) < 0.1:
                # if self.iou(dict_1['am_0'][-1][:4],dict_1['am_1'][-1][:4])>0.2:return bool_1
                dis, min = self.dis_point_(dict_1['am_0'][-1], dict_1['am_1'][-1])
                multiple = 2
                # if dis<min*multiple:
                #     self.am_min_img = img.copy()
                #     self.am_min_bool = True
                if dis >= min * multiple:
                    self.am_max_img = img.copy()
                    self.am_max_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                else:
                    self.am_min_img = img.copy()
                    self.am_min_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.am_min_bool = True
        return bool_1

    def vo_con(self, img, det, result_key):
        if 'voltmeter' in result_key  and 'v_color_label' in result_key:
            v = det['voltmeter']
            v_c = det['v_color_label']
            if self.iou(v[0][:4],v_c[0][:4])>0:
                vo_box=v
            else:
                return  False
        else:
            vo_box = det['voltmeter_blue']
        con_box = det['wire_binding']
        bool_1, dict_1 = self.is_conn(vo_box, con_box, 'vo_')
        key = list(dict_1.keys())
        # if bool_1 and len(self.vo_min_img) == 0:
        #     self.vo_min_img = img.copy()
        #     self.vo_min_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        if 'vo_0' in key and 'vo_1' in key and not self.vo_min_bool:
            if self.iou(dict_1['vo_0'][-1][:4], dict_1['vo_1'][-1][:4]) < 0.1:
                dis, min = self.dis_point_(dict_1['vo_0'][-1], dict_1['vo_1'][-1])
                multiple = 2
                # if dis<min*multiple:
                #     self.vo_min_img = img.copy()
                #     self.vo_min_bool = True
                if dis >= min * multiple:
                    self.vo_max_img = img.copy()
                    self.vo_max_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                else:
                    self.vo_min_img = img.copy()
                    self.vo_min_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.vo_min_bool = True
        return bool_1

    def rheostat_con(self, img, det, result_key):
        rheostat_box = det['slide_rheostat']
        up_box = det['rheostat_up']
        down_box = det['rheostat_down']
        bool_1, dict_1 = self.is_conn(rheostat_box, up_box, 'r_up_')
        bool_2, dict_2 = self.is_conn(rheostat_box, down_box, 'r_down_')
        return bool_1 and bool_2

    def switch_con(self, img, det, result_key):
        switch_box = det['switch']
        con_box = det['wire_binding']
        bool_1, dict_1 = self.is_conn(switch_box, con_box, 's_')
        if bool_1:
            self.switch_disconnect_img_1 = img.copy()
            self.switch_disconnect_img_1_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        return bool_1

    def switch_con_point(self, img, det, result_key):
        switch_box = det['switch']
        if 'wire_binding' in result_key:
            con_box = det['wire_binding']
            for i in range(len(switch_box)):
                for j in range(len(con_box)):
                    if self.iou(switch_box[i][:4], con_box[j][:4]) > 0:
                        return True
        return False

    def fun_switch_con_point(self, top_img, top_det, top_key):
        if 'switch' in top_key:
            bool_1 = self.switch_con_point(top_img, top_det, top_key)
            # 在灯亮之前
            if bool_1 and not self.switch_disconnect_img_1_bool and len(self.light_img) == 0:
                type, ii = self.switch_status(top_img, top_det, top_key)
                if type == 0:
                    self.switch_disconnect_img_1 = ii
                    self.switch_disconnect_img_1_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                    self.switch_disconnect_img_1_bool = True
                elif type == 1:
                    self.switch_closure_img_1 = ii
                    self.switch_closure_img_1_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                else:
                    pass
            # 在灯亮之后
            if not bool_1 and len(self.light_img) != 0 and self.switch_disconnect_img_1_bool and len(
                    self.switch_disconnect_img_2) == 0:# and not self.clear_stop:
                type, ii = self.switch_status(top_img, top_det, top_key)
                if type == 0:
                    self.switch_disconnect_img_2 = ii
                    self.switch_disconnect_img_2_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                elif type == 1:
                    self.switch_closure_img_2 = ii
                    self.switch_closure_img_2_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                else:
                    pass

    def light_con(self, img, det, result_key):
        light_box = det['light_base']
        con_box = det['wire_binding']
        bool_1, dict_1 = self.is_conn(light_box, con_box, 'l_base_')
        return bool_1

    def light_con_two(self, img, det, result_key):
        light_box = det['light_base']
        con_box = det['two']
        bool_1, dict_1 = self.is_conn(light_box, con_box, 'l_two')
        return bool_1

    def r_max_fun(self, top_img, top_det, top_key):
        '''
            接线时判断是不是滑动变阻器阻值是不是最大：
            1、判断依据：连接电路时，滑动变阻器是否远离下接线柱
        '''
        if 'slide_rheostat' in top_key and 'gleithretter' in top_key and 'rheostat_up' in top_key and 'rheostat_down' in top_key and len(
                self.r_up_down_img) != 0:
            rheostat_box = top_det['slide_rheostat'][0]
            w, h = rheostat_box[2] - rheostat_box[0], rheostat_box[3] - rheostat_box[1]
            gleithretter_box = top_det['gleithretter'][0]
            box_down = top_det['rheostat_down'][0]
            dist = self.dis_point(gleithretter_box, box_down)
            if not self.r_max:
                p1 = (int((gleithretter_box[0] + gleithretter_box[2]) / 2),
                      int((gleithretter_box[1] + gleithretter_box[3]) / 2))
                p2 = (int((box_down[0] + box_down[2]) / 2), int((box_down[1] + box_down[3]) / 2))
                draw_img = top_img.copy()
                draw_img = cv2.line(draw_img, p1, p2, (0, 0, 255), 2)
                self.r_location = cv2.putText(draw_img, str(round(dist, 2)), p1, cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                              (0, 0, 255), 2)
            if dist > 90:
                self.r_max_img = self.r_location
                self.r_max_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                self.r_max = True

    def vo_two(self, top_img, top_det, top_key):
        '''
        判断电压表是不是并联：
        1、并联接线标签（two）要和导线链接有交集，同时要满足和电压表有交集
        2、满足两条线
        '''
        if 'light_base' in top_key and 'wire_con' in top_key and 'two' in top_key and (
                ('voltmeter' in top_key and 'v_color_label' in top_key) or 'voltmeter_blue' in top_key):
            if 'voltmeter' in top_key and 'v_color_label' in top_key:
                v = top_det['voltmeter'][0]
                v_c = top_det['v_color_label'][0]
                if self.iou(v[:4],v_c[:4])>0:
                    vo_box = v
                else:
                    return
            else:
                vo_box = top_det['voltmeter_blue'][0]
            two_box = top_det['two']
            light_base_box = top_det['light_base'][0]
            if len(two_box) < 2: return
            wire_con_box = top_det['wire_con']
            two_1 = []
            wire_con_1 = []
            # 两根并联导线同时满足电压表、灯座相连：
            bool_list = []
            for k in range(len(wire_con_box)):
                bool_1 = self.iou(light_base_box[:4], wire_con_box[k][:4]) > 0 and self.iou(vo_box[:4],
                                                                                            wire_con_box[k][:4]) > 0
                bool_2 = self.iou(two_box[0][:4], wire_con_box[k][:4]) > 0 or self.iou(two_box[1][:4],
                                                                                       wire_con_box[k][:4]) > 0
                bool_list.append(bool_1 and bool_2)
            bool_list = np.array(bool_list)
            if bool_list[bool_list == True].shape[0] > 1:
                self.parallel_img = self.draw(top_img.copy(), [vo_box], ['v'])
                self.parallel_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                return
            # for i in range(len(two_box)):
            #     for j in range(len(wire_con_box)):
            #         bool_1 = self.iou(two_box[i][:4], wire_con_box[j][:4]) > 0 and self.iou(vo_box[:4],
            #                                                                                 wire_con_box[j][:4]) > 0
            #         if bool_1 and len(two_1) == 0:
            #             two_1 = two_box[i]
            #             wire_con_1 = wire_con_box[j]
            #             count = j
            #             break
            #         if bool_1 and len(two_1) != 0:
            #             bool_2 = self.iou(two_box[i][:4], two_1[:4]) < 0.6 and self.iou(wire_con_1[:4],
            #                                                                             wire_con_box[j][:4]) < 0.6
            #             if bool_2:
            #                 self.parallel_img = self.draw(top_img.copy(), [vo_box], ['v'])

    def device_conn_status(self, top_img, top_det, top_key):
        '''
        判断是不是串联：
        1、仅仅看是不是线是否接好
        2、不通过其他条件判断，如串联时需要阻值最大等等
        '''
        s_type = ''
        if 'wire_binding' in top_key:
            if 'power_source' in top_key:
                self.single_p = self.power_con(top_img, top_det, top_key)
            if 'ammeter' in top_key:
                self.single_a = self.am_con(top_img, top_det, top_key)
            if ('voltmeter' in top_key  and 'v_color_label' in top_key) or 'voltmeter_blue' in top_key:
                self.single_v = self.vo_con(top_img, top_det, top_key)
            if 'switch' in top_key:
                self.single_s = self.switch_con(top_img, top_det, top_key)
            if 'light_base' in top_key:
                self.single_l = self.light_con(top_img, top_det, top_key)
        if 'light_base' in top_key and 'two' in top_key:
            self.single_l_two = self.light_con_two(top_img, top_det, top_key)
        if 'slide_rheostat' in top_key and ('rheostat_up' in top_key or 'rheostat_down' in top_key):
            self.single_r = self.r_same_conn(top_img, top_det, top_key)
        bool_1 = self.single_p and self.single_a and self.single_r
        bool_2 = self.single_s and (self.single_l or self.single_l_two)
        if bool_1 and bool_2:
            self.tandem_img_bool = True
            self.tandem_img = top_img
            self.tandem_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def light_base_l(self, img, det, result_key):
        light_base_box = det['light_base'][0]
        light_box = det['light'][0]
        class_img = img[int(light_base_box[1]):int(light_base_box[3]),
                    int(light_base_box[0]):int(light_base_box[2])]
        if class_img is None:return False
        class_result = self.classmodel([class_img])
        lab = self.classmodel.label[int(class_result[0][-1])]
        if class_result[0][0] > self.light_class_th and lab == 'light_bright' and light_box[-1] > 0.2:
            # self.light_class_th = class_result[0][0]
            self.light_img = img
            self.light_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
            # cv2.imshow('l',class_img)
            # cv2.waitKey(1)
            return True
        return False
    def range_am(self, img, det, result_key):
        '''
        判断max or min是否与接线相交，如果没有相交pass
        '''
        am_box = det['ammeter'][0]
        min_box = det['min_max']
        for i in range(len(min_box)):
            bool_1 = self.iou(min_box[i][:4], am_box[:4]) > 0
            if bool_1:
                x1,y1,x2,y2,val = int(min_box[i][0])-20,int(min_box[i][1])-20,int(min_box[i][2])+20,int(min_box[i][3])+20,min_box[i][4]
                class_img = img[y1:y2,x1:x2]
                class_result = self.classmodel([class_img])
                lab = self.classmodel.label[int(class_result[0][-1])]
                # if class_result[0][0] > self.light_class_th and lab == 'min' and val > 0.8:
                #     cv2.imshow('am_min', class_img)
                #     cv2.waitKey(1)
                # if class_result[0][0] > self.light_class_th and lab == 'max' and val > 0.8:
                #     cv2.imshow('am_max', class_img)
                #     cv2.waitKey(1)
        return False
    def range_vo_b(self, img, det, result_key):
        '''
        判断max or min是否与接线相交，如果没有相交pass
        '''
        vo_b_box = det['voltmeter_blue'][0]
        min_box = det['min_max']
        for i in range(len(min_box)):
            bool_1 = self.iou(min_box[i][:4], vo_b_box[:4]) > 0
            if bool_1:
                x1,y1,x2,y2,val = int(min_box[i][0])-10,int(min_box[i][1])-10,int(min_box[i][2])+10,int(min_box[i][3])+10,min_box[i][4]
                class_img = img[y1:y2,x1:x2]
                if class_img is None:return  False
                class_result = self.classmodel([class_img])
                lab = self.classmodel.label[int(class_result[0][-1])]
                # if class_result[0][0] > self.light_class_th and lab == 'min' and val > 0.8:
                #     cv2.imshow('vo_b_min', class_img)
                #     cv2.waitKey(1)
                # if class_result[0][0] > self.light_class_th and lab == 'max' and val > 0.8:
                #     cv2.imshow('vo_b_mmax', class_img)
                #     cv2.waitKey(1)
        return False

    def r_judge_up_down(self, rheostat_box, box, w):
        index_1 = []
        for i in range(len(box)):
            bool_1 = self.iou(rheostat_box[:4], box[i][:4]) > 0
            if bool_1:
                index_1.append(i)
        if len(index_1) > 1:
            len_1 = len(index_1)
            for j in range(len_1 - 1):
                bool_2 = box[j] != box[j + 1] and self.dis_point(box[j], box[j + 1]) > 0.3 * w
                if bool_2:
                    return True
        return False

    def r_same_conn(self, img, det, result_key):
        '''判断滑动变阻器是不是同上同下连接'''
        rheostat_box = det['slide_rheostat'][0]
        w, h = rheostat_box[2] - rheostat_box[0], rheostat_box[3] - rheostat_box[1]
        if 'rheostat_up' in result_key and 'rheostat_down' not in result_key:
            box_up = det['rheostat_up']
            bool_1 = self.r_judge_up_down(rheostat_box, box_up, w)
            if bool_1:
                self.r_up_img = img
        elif 'rheostat_up' not in result_key and 'rheostat_down' in result_key:
            box_down = det['rheostat_down']
            bool_2 = self.r_judge_up_down(rheostat_box, box_down, w)
            if bool_2:
                self.r_down_img = img
        else:
            box_up = det['rheostat_up'][0]
            box_down = det['rheostat_down'][0]
            bool_3 = self.iou(rheostat_box[:4], box_up[:4]) > 0 and self.iou(rheostat_box[:4], box_down[:4]) > 0
            bool_4 = self.iou(box_up[:4], box_down[:4]) < 0.5
            if bool_3 and bool_4:
                self.r_up_down_img = img
                self.r_up_down_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
        if len(self.r_up_img) != 0 or len(self.r_down_img) != 0 or len(self.r_up_down_img) != 0:
            return True
        else:
            return False

    def connection_type(self, s_type):
        bool_1 = self.single_p and self.single_a and self.single_r
        bool_2 = self.single_s and (self.single_l or self.single_l_two)
        bool_3 = self.single_s and (self.single_l or self.single_l_two) and self.single_v
        if bool_1 and bool_2:  # and s_type == 'switch_off':
            self.tandem_img_bool = True  # 串联
        if bool_1 and bool_3:  # and s_type == 'switch_off':
            self.parallel_img_bool = True

    def switch_status(self, img, det, result_key):
        switch_box = det['switch'][0]
        h, w = img.shape[:2]
        class_img = img[max(0, int(switch_box[1] - 10)):min(int(switch_box[3] + 10), h),
                    max(0, int(switch_box[0] - 20)):min(int(switch_box[2] + 20), w)]
        # cv2.imshow('class_img',class_img)
        # cv2.waitKey(1)
        if class_img is None:return -1, []
        point_coor = self.keypoint_infer.infer(class_img)
        if len(point_coor) == 3:
            bool_1 = self.keypoint_infer.k_b(class_img, point_coor)
            if bool_1:
                return 1, img  # 0开始断开，1开始闭合，-1不满足情况
            else:
                return 0, img
        return -1, []

    def default_score(self, img, det, result_key):
        if self.light_bool:
            if 'voltmeter_blue' in result_key or ('voltmeter' in result_key and 'v_color_label' in result_key):
                if 'voltmeter' in result_key and 'v_color_label' in result_key:
                    v = det['voltmeter'][0]
                    v_c = det['v_color_label'][0]
                    if self.iou(v[:4], v_c[:4]) > 0:
                        vo_box = v
                    else:
                        return
                else:
                    vo_box = det['voltmeter_blue'][0]
                self.vo_pos_in_img = self.draw(img.copy(), [vo_box], ['vo_pos_in'])
                self.vo_pos_in_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                self.vo_pointer_img = img.copy()
                self.vo_pointer_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                if 'pointer' in result_key:
                    pointer_box = det['pointer']
                    for i in range(len(pointer_box)):
                        if self.iou(vo_box[:4], pointer_box[i][:4]) > 0:
                            # self.vo_pointer_img = self.draw(img.copy(), [pointer_box[i]], ['vo_pointer'])
                            self.vo_pointer_img = img.copy()
                            self.vo_pointer_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                            self.vo_pointer_img_bool = True
            if 'ammeter' in result_key:
                am_box = det['ammeter'][0]
                self.am_pos_in_img = self.draw(img.copy(), [am_box], ['am_pos_in'])
                self.am_pos_in_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                self.am_pointer_img = img.copy()
                self.am_pointer_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                if 'pointer' in result_key:
                    pointer_box = det['pointer']
                    for j in range(len(pointer_box)):
                        if self.iou(am_box[:4], pointer_box[j][:4]) > 0:
                            # self.am_pointer_img = self.draw(img.copy(), [pointer_box[j]], ['am_pointer'])
                            self.am_pointer_img = img.copy()
                            self.am_pointer_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                            self.am_pointer_img_bool = True
        self.light_bool = False

    def clear_fun(self, img, det, result_key):
        if len(self.parallel_img) != 0:
            if 'clear' in result_key:
                self.clear_img = img.copy()
                self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                self.clear_stop = True
            if 'wire_binding' not in result_key and 'wire_con' not in result_key:
                self.clear_img = img.copy()
                self.clear_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]

    def error_vo_c(self,img, det, result_key):
        if not self.single_v:#判断电压表链接状态
            return
        #如果没有检测到电表、
        if 'voltmeter' in result_key and 'v_color_label' in result_key:
            v = det['voltmeter']
            v_c = det['v_color_label']
            if self.iou(v[0][:4], v_c[0][:4]) > 0:
                vo_box = v
            else:
                return False
        elif 'voltmeter_blue' in result_key:
            vo_box = det['voltmeter_blue']
        else:
            return False
        con_box = det['wire_con']
        con_box_list = []
        for i in range(len(con_box)):
            if self.iou(vo_box[0][:4],con_box[i][:4])>0:
                con_box_list.append(con_box[i])
        V_C = False
        if len(con_box_list)==2:
            for key in result_key:
                if key in ['voltmeter','voltmeter_blue','wire_con']:continue
                for j in range(len(det[key])):
                    box = det[key][j]
                    if self.iou(box[:4],con_box_list[0][:4])>0 and self.iou(box[:4],con_box_list[1][:4])>0:
                        V_C = True
            if not V_C:
                self.error_vo_c_img = img.copy()
                self.error_vo_c_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                return
    def error_am_two(self, img, det, result_key):
        '''
        判断电压表是不是并联：
        1、并联接线标签（two）要和导线链接有交集，同时要满足和电压表有交集
        2、满足两条线
        '''
        if  'wire_binding' in result_key and 'wire_con' in result_key and 'two' in result_key and 'ammeter' in result_key:
            am_box = det['ammeter'][0]
            two_box = det['two']
            if len(two_box) < 2: return
            wire_con_box = det['wire_con']
            wire_box = det['wire_binding']
            #找到电流表内部接线柱
            am_wire_list = []
            for i in range(len(wire_box)):
                if self.iou(am_box[:4],wire_box[i][:4])>0:
                    am_wire_list.append(wire_box[i])
                if len(am_wire_list)==2:
                    break

            # 两根并联导线同时满足电压表、灯座相连：
            bool_list = []
            if len(am_wire_list)==2:
                for k in range(len(wire_con_box)):
                    bool_1 = self.iou(am_box[:4],wire_con_box[k][:4]) > 0
                    bool_2 = self.iou(two_box[0][:4], wire_con_box[k][:4]) > 0 or self.iou(two_box[1][:4],wire_con_box[k][:4]) > 0
                    bool_3 = self.iou(am_wire_list[0][:4], wire_con_box[k][:4]) > 0 or self.iou(am_wire_list[1][:4],
                                                                                           wire_con_box[k][:4]) > 0
                    bool_list.append(bool_1 and bool_2 and bool_3)

        if 'light_base' in result_key and 'wire_con' in result_key and 'two' in result_key and 'ammeter' in result_key:
            am_box = det['ammeter'][0]
            two_box = det['two']
            light_base_box = det['light_base'][0]
            if len(two_box) < 2: return
            wire_con_box = det['wire_con']
            # 两根并联导线同时满足电压表、灯座相连：
            bool_list = []
            for k in range(len(wire_con_box)):
                bool_1 = self.iou(light_base_box[:4], wire_con_box[k][:4]) > 0 and self.iou(am_box[:4],
                                                                                            wire_con_box[k][:4]) > 0
                bool_2 = self.iou(two_box[0][:4], wire_con_box[k][:4]) > 0 or self.iou(two_box[1][:4],
                                                                                       wire_con_box[k][:4]) > 0
                bool_list.append(bool_1 and bool_2)
            bool_list = np.array(bool_list)
            if bool_list[bool_list == True].shape[0] > 1:
                self.error_am_two_img = img.copy()
                self.error_am_two_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                return
    def error_r_tong_up(self, img, det, result_key):
        if 'slide_rheostat' in result_key and 'rheostat_up' in result_key and 'rheostat_down' not in result_key:
            # con_box = det['wire_con']
            r_box = det['slide_rheostat'][0]
            r_up_box = det['rheostat_up']
            bool_1 = self.iou(r_box[:4],r_up_box[0][:4])>0 and self.iou(r_box[:4],r_up_box[1][:4])>0
            bool_2 = len(self.error_r_tong_up_img)==0
            if bool_1 and bool_2:
                self.error_r_tong_up_img = img.copy()
                self.error_r_tong_up_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                return
    def error_r_tong_down(self, img, det, result_key):
        if 'slide_rheostat' in result_key and 'rheostat_down' in result_key and 'rheostat_up' not in result_key:
            r_box = det['slide_rheostat'][0]
            r_down_box = det['rheostat_down']
            bool_1 = self.iou(r_box[:4],r_down_box[0][:4])>0 and self.iou(r_box[:4],r_down_box[1][:4])>0
            bool_2 = len(self.error_r_tong_down_img)==0
            if bool_1 and bool_2:
                self.error_r_tong_down_img = img.copy()
                self.error_r_tong_down_img_list = [self.objects_, self.time_, self.num_frame_, self.preds_]
                return



    def save_score_fun(self, frame_front, preds, objects, time, num_frame, type='win'):
        if len(self.tandem_img) != 0 and not self.save_score_1:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '1.jpg', self.tandem_img)
            else:
                self.assignScore(
                    index=1,
                    img=self.tandem_img.copy(),
                    object=self.tandem_img_list[0],
                    conf=0.1,
                    time_frame=self.tandem_img_list[1],
                    num_frame=self.tandem_img_list[2],
                    name_save="1.jpg",
                    preds=self.tandem_img_list[3])
            self.save_score_1 = True
        if len(self.parallel_img) != 0 and not self.save_score_2:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '2.jpg', self.parallel_img)
            else:
                self.assignScore(
                    index=2,
                    img=self.parallel_img.copy(),
                    object=self.parallel_img_list[0],
                    conf=0.1,
                    time_frame=self.parallel_img_list[1],
                    num_frame=self.parallel_img_list[2],
                    name_save="2.jpg",
                    preds=self.parallel_img_list[3])
            self.save_score_2 = True
        if len(self.r_max_img) != 0 and not self.save_score_3:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '3.jpg', self.r_max_img)
            else:
                self.assignScore(
                    index=3,
                    img=self.r_max_img.copy(),
                    object=self.r_max_img_list[0],
                    conf=0.1,
                    time_frame=self.r_max_img_list[1],
                    num_frame=self.r_max_img_list[2],
                    name_save="3.jpg",
                    preds=self.r_max_img_list[3])
            self.save_score_3 = True
        if len(self.r_up_down_img) != 0 and not self.save_score_4:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '4.jpg', self.r_up_down_img)
            else:
                self.assignScore(
                    index=4,
                    img=self.r_up_down_img.copy(),
                    object=self.r_up_down_img_list[0],
                    conf=0.1,
                    time_frame=self.r_up_down_img_list[1],
                    num_frame=self.r_up_down_img_list[2],
                    name_save="4.jpg",
                    preds=self.r_up_down_img_list[3])
            self.save_score_4 = True
        if len(self.light_img) != 0 and not self.save_score_5:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '5.jpg', self.light_img)
            else:
                self.assignScore(
                    index=5,
                    img=self.light_img.copy(),
                    object=self.light_img_list[0],
                    conf=0.1,
                    time_frame=self.light_img_list[1],
                    num_frame=self.light_img_list[2],
                    name_save="5.jpg",
                    preds=self.light_img_list[3])
            self.save_score_5 = True
        if len(self.switch_disconnect_img_1) != 0 and not self.save_score_6:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '6.jpg', self.switch_disconnect_img_1)
            else:
                self.assignScore(
                    index=6,
                    img=self.switch_disconnect_img_1.copy(),
                    object=self.switch_disconnect_img_1_list[0],
                    conf=0.1,
                    time_frame=self.switch_disconnect_img_1_list[1],
                    num_frame=self.switch_disconnect_img_1_list[2],
                    name_save="6.jpg",
                    preds=self.switch_disconnect_img_1_list[3])
            if self.switch_disconnect_img_1_bool:
                self.save_score_6 = True
        #####################默认得分#############
        if len(self.vo_pos_in_img) != 0 and not self.save_score_7:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '7.jpg', self.vo_pos_in_img)
            else:
                self.assignScore(
                    index=7,
                    img=self.vo_pos_in_img.copy(),
                    object=self.vo_pos_in_img_list[0],
                    conf=0.1,
                    time_frame=self.vo_pos_in_img_list[1],
                    num_frame=self.vo_pos_in_img_list[2],
                    name_save="7.jpg",
                    preds=self.vo_pos_in_img_list[3])
            self.save_score_7 = True
        if len(self.am_pos_in_img) != 0 and not self.save_score_8:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '8.jpg', self.am_pos_in_img)
            else:
                self.assignScore(
                    index=8,
                    img=self.am_pos_in_img.copy(),
                    object=self.am_pos_in_img_list[0],
                    conf=0.1,
                    time_frame=self.am_pos_in_img_list[1],
                    num_frame=self.am_pos_in_img_list[2],
                    name_save="8.jpg",
                    preds=self.am_pos_in_img_list[3])
            self.save_score_8 = True
        if len(self.vo_pointer_img) != 0 and not self.save_score_9:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '9.jpg', self.vo_pointer_img)
            else:
                self.assignScore(
                    index=9,
                    img=self.vo_pointer_img.copy(),
                    object=self.vo_pointer_img_list[0],
                    conf=0.1,
                    time_frame=self.vo_pointer_img_list[1],
                    num_frame=self.vo_pointer_img_list[2],
                    name_save="9.jpg",
                    preds=self.vo_pointer_img_list[3])
            if self.vo_pointer_img_bool:
                self.save_score_9 = True
        if len(self.am_pointer_img) != 0 and not self.save_score_10:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '10.jpg', self.am_pointer_img)
            else:
                self.assignScore(
                    index=10,
                    img=self.am_pointer_img.copy(),
                    object=self.am_pointer_img_list[0],
                    conf=0.1,
                    time_frame=self.am_pointer_img_list[1],
                    num_frame=self.am_pointer_img_list[2],
                    name_save="10.jpg",
                    preds=self.am_pointer_img_list[3])
            if self.am_pointer_img_bool:
                self.save_score_10 = True
        if len(self.switch_disconnect_img_2) != 0 and not self.save_score_11:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '11.jpg', self.switch_disconnect_img_2)
            else:
                self.assignScore(
                    index=11,
                    img=self.switch_disconnect_img_2.copy(),
                    object=self.switch_disconnect_img_2_list[0],
                    conf=0.1,
                    time_frame=self.switch_disconnect_img_2_list[1],
                    num_frame=self.switch_disconnect_img_2_list[2],
                    name_save="11.jpg",
                    preds=self.switch_disconnect_img_2_list[3])
            self.save_score_11 = True
        if len(self.clear_img) != 0 and not self.save_score_12:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '12.jpg', self.clear_img)
            else:
                self.assignScore(
                    index=12,
                    img=self.clear_img.copy(),
                    object=self.clear_img_list[0],
                    conf=0.1,
                    time_frame=self.clear_img_list[1],
                    num_frame=self.clear_img_list[2],
                    name_save="12.jpg",
                    preds=self.clear_img_list[3])
            if self.clear_stop:
                self.save_score_12 = True
        if len(self.vo_min_img) != 0 and not self.save_score_13:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '13.jpg', self.vo_min_img)
            else:
                self.assignScore(
                    index=13,
                    img=self.vo_min_img.copy(),
                    object=self.vo_min_img_list[0],
                    conf=0.1,
                    time_frame=self.vo_min_img_list[1],
                    num_frame=self.vo_min_img_list[2],
                    name_save="13.jpg",
                    preds=self.vo_min_img_list[3])
            if self.vo_min_bool:
                self.save_score_13 = True
        if len(self.am_min_img) != 0 and not self.save_score_14:
            if time is None and type != 'win':
                cv2.imwrite(self.save_path + '14.jpg', self.am_min_img)
            else:
                self.assignScore(
                    index=14,
                    img=self.am_min_img.copy(),
                    object=self.am_min_img_list[0],
                    conf=0.1,
                    time_frame=self.am_min_img_list[1],
                    num_frame=self.am_min_img_list[2],
                    name_save="14.jpg",
                    preds=self.am_min_img_list[3])
            if self.am_min_bool:
                self.save_score_14 = True
    def error_save_score_fun(self):
        if len(self.error_vo_c_img) != 0 and not self.error_save_score_1:
            self.assignError(
                index=1,
                img=self.error_vo_c_img.copy(),
                object=self.error_vo_c_img_list[0],
                conf=0.1,
                time_frame=self.error_vo_c_img_list[1],
                num_frame=self.error_vo_c_img_list[2],
                name_save="1_error.jpg",
                preds=self.error_vo_c_img_list[3])
            self.error_save_score_1 = True
        if len(self.error_am_two_img) != 0 and not self.error_save_score_2:
            self.assignError(
                index=2,
                img=self.error_am_two_img.copy(),
                object=self.error_am_two_img_list[0],
                conf=0.1,
                time_frame=self.error_am_two_img_list[1],
                num_frame=self.error_am_two_img_list[2],
                name_save="2_error.jpg",
                preds=self.error_am_two_img_list[3])
            self.error_save_score_2 = True
        if len(self.error_r_tong_up_img) != 0 and not self.error_save_score_3:
            self.assignError(
                index=3,
                img=self.error_r_tong_up_img.copy(),
                object=self.error_r_tong_up_img_list[0],
                conf=0.1,
                time_frame=self.error_r_tong_up_img_list[1],
                num_frame=self.error_r_tong_up_img_list[2],
                name_save="3_error.jpg",
                preds=self.error_r_tong_up_img_list[3])
            self.error_save_score_3 = True
        if len(self.error_r_tong_down_img) != 0 and not self.error_save_score_4:
            self.assignError(
                index=4,
                img=self.error_r_tong_down_img.copy(),
                object=self.error_r_tong_down_img_list[0],
                conf=0.1,
                time_frame=self.error_r_tong_down_img_list[1],
                num_frame=self.error_r_tong_down_img_list[2],
                name_save="4_error.jpg",
                preds=self.error_r_tong_down_img_list[3])
            self.error_save_score_4 = True
        if len(self.switch_closure_img_1) != 0 and not self.error_save_score_5:
            self.assignError(
                index=5,
                img=self.switch_closure_img_1.copy(),
                object=self.switch_closure_img_1_list[0],
                conf=0.1,
                time_frame=self.switch_closure_img_1_list[1],
                num_frame=self.switch_closure_img_1_list[2],
                name_save="5_error.jpg",
                preds=self.switch_closure_img_1_list[3])
            self.error_save_score_5 = True
        if len(self.switch_closure_img_2) != 0 and not self.error_save_score_6:
            self.assignError(
                index=6,
                img=self.switch_closure_img_2.copy(),
                object=self.switch_closure_img_2_list[0],
                conf=0.1,
                time_frame=self.switch_closure_img_2_list[1],
                num_frame=self.switch_closure_img_2_list[2],
                name_save="6_error.jpg",
                preds=self.switch_closure_img_2_list[3])
            self.error_save_score_6 = True
    def predict(self, img0s, det, result_key, preds=None, objects=None, time=None, num_frame=None):
        '''
        1、计算每个器件的连接状态
            1.1、电池
            1.2、开关
            1.3、电压表
            1.4、电流表
            1.5、灯座（分并联和串联，两者满足一个即可）
            1.6、滑动变阻器（分同上、同下、一上一下，判断状态时满足一个即可）
        2、判断灯泡是否亮
        3、判断开关状态（开关状态可和后期各种判断组合使用）
        4、判断电流表、电压表正进负出（待做）
        5、判断指针偏转（待做）
        6、滑动变阻器移动
            6.1、判断滑动变阻器接线时滑片位置是否原理下接线组
            6.2、判断滑片与下接线柱的距离
        '''
        ##################################################################################################
        # 判断每个器件是否接线正常，共六个器件
        # top_key,top_det,top_img,front_key,front_det,front_img,side_key,side_det,side_img = self.fun_get_img(img0s, det, re_key)
        # top_det, top_key = self.filter_det(top_img, top_det, top_key)
        # self.fun_line_filter(top_img, top_det, top_key)
        # self.fun_switch_point(top_img, top_det, top_key)
        # cv2.imshow('a', img0s)
        # cv2.waitKey(1)
        if False:
            result_key, det, img0s, front_key, front_det, front_img, side_key, side_det, side_img = self.fun_get_img(
                img0s, det, result_key)
        self.device_conn_status(img0s, det, result_key)
        self.r_max_fun(img0s, det, result_key)
        self.vo_two(img0s, det, result_key)
        self.fun_switch_con_point(img0s, det, result_key)
        # if 'switch' in result_key:
        #     self.switch_status(img0s, det, result_key)
        # 判断灯泡是否亮
        if 'light_base' in result_key and 'light' in result_key:
            self.light_bool = self.light_base_l(img0s, det, result_key)
        if not self.light_bool and 'light' in result_key:
            self.light_bool = True
        # 判断灯泡是否亮
        # if 'min_max' in result_key and 'ammeter' in result_key:
        #     self.am_ = self.range_am(img0s, det, result_key)
        # if  'min_max' in result_key and 'voltmeter_blue' in result_key:
        #     self.vo_b = self.range_vo_b(img0s, det, result_key)
        self.default_score(img0s, det, result_key)
        self.clear_fun(img0s, det, result_key)
        #############错误得分点
        if self.show_error:
            if ('voltmeter_blue' in result_key or ('voltmeter' in result_key and 'v_color_label' in result_key)) and 'wire_con' in result_key:
                self.error_vo_c(img0s, det, result_key)
            self.error_am_two(img0s, det, result_key)
            self.error_r_tong_up(img0s, det, result_key)
            self.error_r_tong_down(img0s, det, result_key)
            self.error_save_score_fun()
        #############错误得分点
        self.save_score_fun(img0s, preds, objects, time, num_frame)

    def process_dict(self, d):
        for key in list(d.keys()):
            # if key == 'point' and len(self.region) == 0:
            #     self.region = dict_[key][0]
            if len(d[key]) > 1 and key in ['ammeter',
                                           'voltmeter',
                                           'clear',
                                           'light',
                                           'voltmeter_blue',
                                           'slide_rheostat',
                                           'gleithretter',
                                           'point',
                                           'switch',
                                           'light_base',
                                           'v_color_label']:
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
            if 'min_max' == key:
                d[key].sort(key=self.sortlist, reverse=True)
                if len(d[key]) == 1:
                    bbox = d[key][:1]
                    bbox.append([0, 0, 0, 0, 0])
                    d[key] = bbox
                else:
                    d[key] = d[key][:2]
            if self.show_error:
                if  'rheostat_up' == key or 'rheostat_down' == key:
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
            names_label = ['power_source',
                           'ammeter',
                           'voltmeter',
                           'clear',
                           'light',
                           'voltmeter_blue',
                           'slide_rheostat',
                           'gleithretter',
                           'point',
                           'switch',
                           'light_base',
                           'a_v_label',
                           'pointer',
                           'v_color_label',
                           'wire_binding',
                           'wire_con',
                           'rheostat_up',
                           'rheostat_down',
                           'two', "min_max"]
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
            self.preds_ = top_preds
            self.objects_ = objects_top
            self.time_ = time_top
            self.predict(frame_top, dict_, list(dict_.keys()), top_preds, objects_top, time_front, num_frame_front)
            if self.show_img:
                self.plot(top_preds, frame_top)
                # frame_top =  cv2.resize(frame_top,(640,384))
                cv2.imshow('power', frame_top)
                cv2.waitKey(1)
        self.rtmp_push_fun(top_img=frame_top, front_img=frame_front, side_img=frame_side,
                           top_preds=top_preds, front_preds=top_preds, side_preds=side_preds)

