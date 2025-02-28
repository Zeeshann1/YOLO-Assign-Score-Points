import torchvision.transforms as transforms
from PIL import Image
from logger import logger
from .comm import *
from .comm.course_base import ConfigModel

# from config.phy_convex_lens_imaging import PTJTTJCX01
# from utilsg.litF import uploaded_images, encode_image_jpg, upload_redis_or_save_json_local, ts2ft
# from configg.global_config import SCORE_ROOT_PATH
# from concurrent.futures import ThreadPoolExecutor
import copy
from deeplearn.yolov5s.models.hrnet_lite import get_model

DEBUG_ = True

## TODO ##
## !!!发现不等高进行得分撤回!!!


class Regresser():
    def __init__(self):
        self.model = get_model(1)
        weight_path = str(
            Path(__file__).parent /
            "../deeplearn/yolov5s/weights/phy_convex_lens_imaging/heatmap_lite.pth"
        )
        torch.cuda.empty_cache()
        checkpoint = torch.load(weight_path, map_location="cpu")
        self.model.load_state_dict(checkpoint)
        self.model.train(False)
        self.model.eval()
        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((96 * 2, 96)),
            transforms.ToTensor(),
        ])

    def __call__(self, pred_box, img):
        coarse_box = [
            int(0.5 * pred_box[0] + 0.5 * pred_box[2]),
            int(0.5 * pred_box[1] + 0.5 * pred_box[3]),
            pred_box[2] - pred_box[0], pred_box[3] - pred_box[1]
        ]
        x, y, w, h = coarse_box
        xmin, ymin, xmax, ymax = int(x - 0.5 * w), int(y - 0.5 * h), int(
            x + 0.5 * w), int(y + 0.5 * h)
        r = 0.7
        crop_xmin = int(x - r * w)
        crop_ymin = int(y - r * h)
        crop_xmax = int(x + r * w)
        crop_ymax = int(y + r * h)
        crop_xmin = max(crop_xmin, 0)
        crop_ymin = max(crop_ymin, 0)
        crop_xmax = min(crop_xmax, 1920)
        crop_ymax = min(crop_ymax, 1080)
        roi = img[crop_ymin:crop_ymax, crop_xmin:crop_xmax]
        img_ = roi
        img_ = Image.fromarray(img_)
        img_ = self.transform(img_).unsqueeze(0)
        with torch.no_grad():
            img_ = img_.to(self.device)
            preds = self.model(img_)
            preds = preds.cpu()
            pred = (preds[0, 0].numpy() * 255).astype(np.uint8)
            pred = cv2.resize(pred,
                              (crop_xmax - crop_xmin, crop_ymax - crop_ymin))
            ret, mask = cv2.threshold(pred, 75, 255, cv2.THRESH_BINARY)
            ret, pts = self.get_kps_by_mask(mask)
            if ret:
                pts = np.array(pts, dtype=np.float).reshape((-1, 2))
                pts[:, 0] += crop_xmin
                pts[:, 1] += crop_ymin
            return ret, pts

    def get_kps_by_mask(self, mask_binary):
        def sort_res(res):
            final_res = []
            res_sort = sorted(res, key=lambda x: x[1])
            if res_sort[0][0] < res_sort[1][0]:
                final_res.append([res_sort[0][0], res_sort[0][1]])
                final_res.append([res_sort[1][0], res_sort[1][1]])
            else:
                final_res.append([res_sort[1][0], res_sort[1][1]])
                final_res.append([res_sort[0][0], res_sort[0][1]])
            if res_sort[2][0] < res_sort[3][0]:
                final_res.append([res_sort[3][0], res_sort[3][1]])
                final_res.append([res_sort[2][0], res_sort[2][1]])
            else:
                final_res.append([res_sort[2][0], res_sort[2][1]])
                final_res.append([res_sort[3][0], res_sort[3][1]])
            return final_res

        h, w = mask_binary.shape[:2]
        contours, _ = cv2.findContours(mask_binary, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        res = []
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                #print(radius)
                res.append((x, y, radius))
        if len(res) == 4:
            return True, sort_res(res)
        elif len(res) < 4:
            return False, None
        else:
            res_sort = sorted(res, key=lambda x: x[1])
            res_tops = [t for t in res_sort if t[1] < h / 2]
            res_bottoms = [t for t in res_sort if t[1] > h / 2]
            res_tops = sorted(res_tops, key=lambda x: -x[-1])
            if len(res_tops) < 2:
                return False, None
            res_tops = res_tops[:2]
            res_bottoms = sorted(res_bottoms, key=lambda x: -x[-1])
            if len(res_bottoms) < 2:
                return False, None
            res_bottoms = res_bottoms[:2]
            return True, sort_res(res_tops + res_bottoms)


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





class PHY_convex_lens_2(ConfigModel):
    def __init__(self):
        super(PHY_convex_lens_2, self).__init__()
        self.initScore()

    def initScore(self):
        self.exp_ok = [-1] * 18
        self.h_optical_source = 0
        self.smallest_frame = None
        self.largest_frame = None
        self.clearest_frame = None
        self.frame_id = 0
        self.frame_width = 0

        # 凸透镜是否放在光具座中心的阈值
        self.thre1 = 0.1
        # 是否是一代视频, 一代视频偏模糊
        self.is_first = True
        # 判断光屏是否移动了
        self.buffer_front = []
        self.buffer_top = []
        self.height, self.width = 0, 0
        ##this is used for counting time of giving point,the point is that one point shall be given when relative object stands still.The points should not be given when objects are moving --huoheng
        self.exp_ok_hold=[None]*18 

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
        self.exp_ok[index - 1] = -2

    def get_clear_score(self, box):
        xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(
            box[3])
        roi = self.frame_front[ymin:ymax, xmin:xmax]
        roi_lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)[:, :, 1]
        laplacian = cv2.Laplacian(roi_lab, cv2.CV_64F).var()
        laplacian = min(laplacian, 150)
        clear_score = laplacian / 150.
        return clear_score

    def exp_filter(self, d_front, d_top):
        d = {"front": {}, "top": {}}
        if "光具座_前视" in d_front.keys():
            bench = sorted(
                d_front["光具座_前视"],
                key=lambda x: -(x[2] - x[0]) * (x[3] - x[1]))[0]
            xmin = bench[0]
            xmax = bench[2]
            for key, vals in d_front.items():
                if key == "光具座_前视":
                    d["front"][key] = vals
                else:
                    vals_new = []
                    for val in vals:
                        x = 0.5 * (val[0] + val[2])
                        if xmin <= x <= xmax:
                            vals_new.append(val)
                    if len(vals_new):
                        d["front"][key] = vals_new
        else:
            d["front"] = d_front
        if "光具座_顶视" in d_top.keys():
            bench = sorted(
                d_top["光具座_顶视"],
                key=lambda x: -(x[2] - x[0]) * (x[3] - x[1]))[0]
            xmin = bench[0]
            xmax = bench[2]
            for key, vals in d_top.items():
                if key == "光具座_顶视":
                    d["top"][key] = vals
                else:
                    vals_new = []
                    for val in vals:
                        x = 0.5 * (val[0] + val[2])
                        if xmin <= x <= xmax:
                            vals_new.append(val)
                    if len(vals_new):
                        d["top"][key] = vals_new
        else:
            d["top"] = d_top
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

        def assign_error_fun(index, view):
            if view == "front":
                self.assignError(
                    index=index,
                    img=self.frame_front,
                    time_frame=self.time_front,
                    object=self.objects_front,
                    preds=self.preds_front,
                    num_frame=self.num_frame_front)
            elif view == "top":
                self.assignError(
                    index=index,
                    img=self.frame_top,
                    time_frame=self.time_top,
                    object=self.objects_top,
                    preds=self.preds_top,
                    num_frame=self.num_frame_top)

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
        #print('asign done')

        if top_true and front_true:
            self.rtmp_push_fun(
                top_img=frame_top,
                front_img=frame_front,
                side_img=frame_side,
                top_preds=self.preds_top,
                front_preds=self.preds_front,
                side_preds=None)
            

            if self.frame_width == 0:
                self.frame_width = self.frame_top.shape[1]
                self.height, self.width = self.frame_top.shape[
                    0], self.frame_top.shape[1]
            d_front = dict()
            d_top = dict()
            
            for label, boxes in zip(self.labels, self.preds_front):
                if boxes.size(0) > 0:
                    if "头" == label:
                        d_front[label] = boxes.cpu().numpy()
                    elif "前视" in label:
                        d_front[label] = boxes.cpu().numpy()
            for label, boxes in zip(self.labels, self.preds_top):
                if boxes.size(0) > 0:
                    if "头" == label:
                        d_top[label] = boxes.cpu().numpy()
                    elif "顶视" in label:
                        d_top[label] = boxes.cpu().numpy()
            self.d = self.exp_filter(d_front, d_top)
            self.judge_first()

            if DEBUG_:
                show_front = copy.copy(self.frame_front)
                show_top = copy.copy(self.frame_top)
                self.plot(self.preds_front, show_front)
                self.plot(self.preds_top, show_top)

                cv2.imshow("front_img0", show_front)
                cv2.imshow("top_img0", show_top)
                cv2.waitKey(1)
            self.frame_id += 1
            #print("start logic")
            ## 1. 观察并记录凸透镜的焦距
            if -1 == self.exp_ok[0]:
                ###hold for 0.5s
                if self.j1():
                    ##hold some time then give points --huboheng
                    if not self.exp_ok_hold[0]:
                        self.exp_ok_hold[0] = time_front
                        if DEBUG_:
                            print("start timeing for 1")
                    elif time_top-self.exp_ok_hold[0]>500:
                        ##hold for 1000ms,that is one second --huboheng
                        self.exp_ok[0] = self.frame_id
                        assign_score_fun(1, "front")
                        if DEBUG_:
                            print("exp ok 1")                        
                        return
                    else:
                        pass                        
                else:
                    ##if not j1(), reset the time --huboheng
                    self.exp_ok_hold[0]=None

            ## 2. 在光具座中央固定好凸透镜（一般放置在整数的刻度处，如50厘米处）
            if -1 == self.exp_ok[1]:
                ###hold for 0.5s
                if self.j2():
                    ##hold some time then give points --huboheng
                    if not self.exp_ok_hold[1]:
                        self.exp_ok_hold[1] = time_top
                        if DEBUG_:
                            print("start timeing for 2")
                    elif time_top-self.exp_ok_hold[1]>500:
                        ##hold for 1000ms,that is one second --huboheng
                        self.exp_ok[1] = self.frame_id
                        assign_score_fun(2, "top")
                        if DEBUG_:
                            print("exp ok 2")                        
                        return
                    else:
                        pass                        
                else:
                    ##if not j1(), reset the time --huboheng
                    self.exp_ok_hold[1]=None
            # ## e1: 凸透镜位置错误放置，光源、光屏不在凸透镜两侧
            # ret, view = self.e1()
            # if ret:
            #     assign_error_fun(1, view)
            # ## e2: 光源、凸透镜、光屏中心不等高
            # ret, view = self.e2()
            # if ret:
            #     assign_error_fun(2, view)
            ## 3. 将LED光源和光屏放置在凸透镜两侧
            if -1 == self.exp_ok[2] and (-1!=self.exp_ok[1]):
                ret, view = self.j3()
                if ret:
                    if DEBUG_:
                        print("exp ok 3")
                    if view == "front":
                        self.exp_ok[2] = self.frame_id
                        assign_score_fun(3, "front")
                    else:
                        self.exp_ok[2] = self.frame_id
                        assign_score_fun(3, "top")
                    return
            ## 4. 调节凸透镜、光源和光屏三者的高度,使光源中心、凸透镜中心和光屏中心在同一高度上
            if -1 == self.exp_ok[3]:
                if self.j4():
                    self.exp_ok[3] = self.frame_id
                    assign_score_fun(4, "front")
                    if DEBUG_:
                        print("exp ok 4")
                    return
            ## 5. 移动光源到某个位置，使光源离开凸透镜的距离大于两倍焦距
            ## sometimes exp_ok[3] is not given,yet the exp shall be continued --huboheng
            if (-1 != self.exp_ok[2]) and (-1 == self.exp_ok[4]):
                if self.j5():
                    ##hold some time then give points --huboheng
                    if not self.exp_ok_hold[4]:
                        self.exp_ok_hold[4] = time_top
                        if DEBUG_:
                            print("start timeing for 5")
                    elif time_top-self.exp_ok_hold[4]>1000:
                        ##hold for 1000ms,that is one second --huboheng
                        self.exp_ok[4] = self.frame_id
                        assign_score_fun(5, "top")
                        if DEBUG_:
                            print("exp ok 5")                        
                        return
                    else:
                        pass                        
                else:
                    ##if not j5(), reset the time --huboheng
                    self.exp_ok_hold[4]=None

            ## 6. 移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止
            ## 7. 观察成像特点，并记录物距和像距
            ## score 7 is given automaticly
            if -1 != self.exp_ok[4] and -1 == self.exp_ok[5] and -1 == self.exp_ok[6]:
                ret, view = self.j6()
                if ret and self.j5(): ###need to be at the situation of j11:
                    ##hold some time then give points.top hold top time and front hold front time --huboheng
                    time_now = time_top if view == "top" else time_front
                    if not self.exp_ok_hold[5]:
                        self.exp_ok_hold[5] = {'top':None,'front':None}
                        self.exp_ok_hold[5][view] = time_now
                        if DEBUG_:
                            print("start timeing for 6 7 ",view)
                        
                    elif not self.exp_ok_hold[5][view]:
                        self.exp_ok_hold[5][view] = time_now
                        if DEBUG_:
                            print("start timeing for 6 7 ",view)
                        
                    elif time_now-self.exp_ok_hold[5][view]>1000:                        
                        self.exp_ok[5] = self.frame_id
                        self.exp_ok[6] = self.frame_id
                        if view == "top":
                            assign_score_fun(6, "top")
                            assign_score_fun(7, "top")
                            if DEBUG_:
                                print("exp ok 6 top")
                                print("exp ok 7 top")
                            return
                        else:
                            assign_score_fun(6, "front")
                            assign_score_fun(7, "front")
                            if DEBUG_:
                                print("exp ok 6 front")
                                print("exp ok 7 front")
                            return
                    else:
                        pass
                else:
                    ##if not ret, reset the time --huboheng
                    self.exp_ok_hold[5]=None

            ## 8. 移动光源到某个位置，使光源离开凸透镜的距离等于两倍焦距
            if (-1 != self.exp_ok[2]) and (-1 == self.exp_ok[7]):
                if self.j8():
                    ##hold some time then give points --huboheng
                    if not self.exp_ok_hold[7]:
                        self.exp_ok_hold[7] = time_top
                        if DEBUG_:
                            print("start timeing for 8")                        
                    elif time_top-self.exp_ok_hold[7]>1000:
                        ##hold for 1000ms,that is one second --huboheng
                        self.exp_ok[7] = self.frame_id
                        assign_score_fun(8, "top")
                        if DEBUG_:
                            print("exp ok 8")                        
                        return
                    else:
                        #print(time_top-self.exp_ok_hold[7])
                        pass                        
                else:
                    ##if not j8(), reset the time --huboheng
                    self.exp_ok_hold[7]=None                    
                
            ## 9. 移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止
            ## 10. 观察成像特点，并记录物距和像距
            ## score 10 is given automaticly
            if (-1 != self.exp_ok[7]) and -1 == self.exp_ok[8] and -1 == self.exp_ok[9]:
                ret, view = self.j9()
                if ret and self.j8(): ###need to be at the situation of j8:
                   ##hold some time then give points.top hold top time and front hold front time --huboheng
                    time_now = time_top if view == "top" else time_front
                    if not self.exp_ok_hold[8]:
                        self.exp_ok_hold[8] = {'top':None,'front':None}
                        self.exp_ok_hold[8][view] = time_now
                        if DEBUG_:
                            print("start timeing for 9 10 ",view)
                        
                    elif not self.exp_ok_hold[8][view]:
                        self.exp_ok_hold[8][view] = time_now
                        if DEBUG_:
                            print("start timeing for 9 10 ",view)
                        
                    elif time_now-self.exp_ok_hold[8][view]>1000:                        
                        self.exp_ok[8] = self.frame_id
                        self.exp_ok[9] = self.frame_id
                        if view == "top":
                            assign_score_fun(9, "top")
                            assign_score_fun(10, "top")
                            if DEBUG_:
                                print("exp ok 9 top")
                                print("exp ok 10 top")
                            return
                        else:
                            assign_score_fun(9, "front")
                            assign_score_fun(10, "front")
                            if DEBUG_:
                                print("exp ok 9 front")
                                print("exp ok 10 front")
                            return
                    else:
                        pass
                else:
                    ##if not ret, reset the time --huboheng
                    if self.exp_ok_hold[8]:
                        self.exp_ok_hold[8]=None
                    
            ## 11. 移动光源到某个位置，使光源离开凸透镜的距离大于一倍焦距小于两倍焦距
            if (-1 != self.exp_ok[2]) and (-1 == self.exp_ok[10]):
                if self.j11():
                    ##hold some time then give points --huboheng
                    if not self.exp_ok_hold[10]:
                        self.exp_ok_hold[10] = time_top 
                        if DEBUG_:
                            print("start timeing for 11")                        
                    elif time_top-self.exp_ok_hold[10]>1000:
                        ##hold for 1000ms,that is one second --huboheng
                        self.exp_ok[10] = self.frame_id
                        assign_score_fun(11, "top")
                        if DEBUG_:
                            print("exp ok 11")                        
                        return
                    else:
                        pass                        
                else:
                    ##if not j11(), reset the time --huboheng
                    self.exp_ok_hold[10]=None                    
                    
            ## 12. 移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止
            ## 13. 观察成像特点，并记录物距和像距
            ## score 13 is given automaticly
            if -1 != self.exp_ok[10] and -1 == self.exp_ok[11] and -1 == self.exp_ok[12]:
                ret, view = self.j12()
                if ret and self.j11(): ###need to be at the situation of j11
                   ##hold some time then give points.top hold top time and front hold front time --huboheng
                    time_now = time_top if view == "top" else time_front
                    if not self.exp_ok_hold[11]:
                        self.exp_ok_hold[11] = {'top':None,'front':None}
                        self.exp_ok_hold[11][view] = time_now
                        if DEBUG_:
                            print("start timeing for 12 13 ",view)
                        
                        
                    elif not self.exp_ok_hold[11][view]:
                        self.exp_ok_hold[11][view] = time_now
                        if DEBUG_:
                            print("start timeing for 12 13 ",view)
                        
                    elif time_now-self.exp_ok_hold[11][view]>1000:                        
                        self.exp_ok[11] = self.frame_id
                        self.exp_ok[12] = self.frame_id
                        if view == "top":
                            assign_score_fun(12, "top")
                            assign_score_fun(13, "top")
                            if DEBUG_:
                                print("exp ok 12 top")
                                print("exp ok 13 top")
                            return
                        else:
                            assign_score_fun(12, "front")
                            assign_score_fun(13, "front")
                            if DEBUG_:
                                print("exp ok 12 front")
                                print("exp ok 13 front")
                            return
                    else:
                        pass
                else:
                    ##if not ret, reset the time --huboheng
                    self.exp_ok_hold[11]=None

            ## 14. 移动光源到某个位置，使光源离开凸透镜的距离小于一倍焦距
            if (-1 != self.exp_ok[2]) and (-1 == self.exp_ok[13]):
                if self.j14():
                    ##hold some time then give points --huboheng
                    if not self.exp_ok_hold[13]:
                        self.exp_ok_hold[13] = time_top 
                        if DEBUG_:
                            print("start timeing for 14")                        
                    elif time_top-self.exp_ok_hold[13]>1000:
                        ##hold for 1000ms,that is one second --huboheng
                        self.exp_ok[13] = self.frame_id
                        assign_score_fun(14, "top")
                        if DEBUG_:
                            print("exp ok 14")                        
                        return
                    else:
                        pass                        
                else:
                    ##if not j14(), reset the time --huboheng
                    self.exp_ok_hold[13]=None
                    
            ## 15. 移动光屏找像，观察光屏上是否有像
            if (-1 != self.exp_ok[13]) and (self.exp_ok[14] == -1):
                ret, view = self.j15()
                if ret:
                    if view == "front":
                        self.exp_ok[14] = self.frame_id
                        assign_score_fun(15, "front")
                        if DEBUG_:
                            print("exp ok 15")
                    else:
                        self.exp_ok[14] = self.frame_id
                        assign_score_fun(15, "top")
                        if DEBUG_:
                            print("exp ok 15")                        
                    return
            ## 16. 移去光屏，从光屏一侧透过凸透镜用眼睛观察像
            ## 17. 观察并记录成像情况
            if (-1 != self.exp_ok[13]) and (-1 == self.exp_ok[15]):
                ret, view = self.j16()
                if ret:
                    if view == "front":
                        self.exp_ok[15] = self.frame_id
                        assign_score_fun(16, "front")

                        self.exp_ok[16] = self.frame_id
                        assign_score_fun(17, "front")
                        if DEBUG_:
                            print("exp ok 16")                           
                            print("exp ok 17")
                    else:
                        self.exp_ok[15] = self.frame_id
                        assign_score_fun(16, "top")
                        self.exp_ok[16] = self.frame_id
                        assign_score_fun(17, "top")
                        if DEBUG_:
                            print("exp ok 16")                           
                            print("exp ok 17")                        
                    return
            ## 18. 完成实验并整理仪器
            if (-1 != self.exp_ok[3]) and (-1 == self.exp_ok[17]):
                ret, view = self.j18()
                if ret:
                    if view == "front":
                        self.exp_ok[17] = self.frame_id
                        assign_score_fun(18, "front")

                        return
                    else:
                        self.exp_ok[17] = self.frame_id
                        assign_score_fun(18, "top")
                        return
        # logger.info('赋分进程结束')

    # DONE
    def judge_first(self):
        if "光具座_顶视" in self.d["top"].keys():
            bench = self.d["top"]["光具座_顶视"][0]
            width = bench[2] - bench[0]
            if width > self.frame_width * 0.7:
                self.is_first = False

    # DONE
    def e1(self):
        ## 凸透镜位置错误放置，光源、光屏不在凸透镜两侧
        ### 前视判断
        def j_front():
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if not ("光源板_前视" in self.d["front"].keys()):
                return False
            if not ("光屏_前视" in self.d["front"].keys()):
                return False
            convex = self.d["front"]["凸透镜_前视"][0]
            board = self.d["front"]["光源板_前视"][0]
            screen = self.d["front"]["光屏_前视"][0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_board = 0.5 * (board[0] + board[2])
            x_screen = 0.5 * (screen[0] + screen[2])
            if (x_convex - x_board) * (x_screen - x_convex) < 0:
                return True
            return False

        ### 顶视判断
        def j_top():
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            if not ("光源板_顶视" in self.d["top"].keys()):
                return False
            if not ("光屏_顶视" in self.d["top"].keys()):
                return False
            convex = self.d["top"]["凸透镜_顶视"][0]
            board = self.d["top"]["光源板_顶视"][0]
            screen = self.d["top"]["光屏_顶视"][0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_board = 0.5 * (board[0] + board[2])
            x_screen = 0.5 * (screen[0] + screen[2])
            if (x_convex - x_board) * (x_screen - x_convex) < 0:
                return True
            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    def e2(self):
        ## 光源、凸透镜、光屏中心不等高
        if not ("凸透镜_前视" in self.d["front"].keys()):
            return False
        if self.is_first:
            if not ("光具座_前视" in self.d["front"].keys()):
                return False
        if not ("光屏_前视" in self.d["front"].keys()):
            return False
        if not ("凸透镜_镜身_前视" in self.d["front"].keys()):
            return False
        if not ("光屏_屏身_前视" in self.d["front"].keys()):
            return False
        if not ("光源板_前视" in self.d["front"].keys()):
            return False
        convex = self.d["front"]["凸透镜_镜身_前视"][0]
        screen = self.d["front"]["光屏_屏身_前视"][0]
        board = self.d["front"]["光源板_前视"][0]
        # 有像
        if ("像_前视" in self.d["front"].keys()):
            # 有光源
            if ("光源_前视" in self.d["front"].keys()):
                image = self.d["front"]["像_前视"][0]
                source = self.d["front"]["光源_前视"][0]
                # 高度不对等
                if abs(
                        0.5 * (image[1] + image[3]) - 0.5 *
                    (source[1] + source[3])) > 0.1 * (source[3] - source[1]):
                    return True
                # 成像偏心
                cy_min = screen[1] + 0.2 * (screen[3] - screen[1])
                cy_max = screen[1] + 0.8 * (screen[3] - screen[1])
                cy = 0.5 * (image[1] + image[3])
                if cy < cy_min or cy > cy_max:
                    return True
                return False
        return False

    # DONE
    def j1(self):
        ## 观察并记录凸透镜的焦距

        if ("凸透镜_前视" in self.d["front"].keys()) and (
                "光具座_前视" in self.d["front"].keys()):
            return True
        if ("凸透镜_顶视" in self.d["top"].keys()) and (
                "光具座_顶视" in self.d["top"].keys()):
            return True
        return False

    # DONE
    def j2(self):
        ### 顶视角判断
        def j_top():
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            convex_top = self.d["top"]["凸透镜_顶视"][0]
            bench_top = self.d["top"]["光具座_顶视"][0]
            len_bench_top = bench_top[2] - bench_top[0]
            cx_convex_top = 0.5 * (convex_top[0] + convex_top[2])
            cx_bench_top = 0.5 * (bench_top[0] + bench_top[2])
            if (cx_convex_top - cx_bench_top) / len_bench_top < self.thre1:
                return True

            return False
        
        def j_front():
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if not ("光具座_前视" in self.d["front"].keys()):
                return False
            convex_front = self.d["front"]["凸透镜_前视"][0]
            bench_front = self.d["front"]["光具座_前视"][0]
            len_bench_front = bench_front[2] - bench_front[0]
            cx_convex_front = 0.5 * (convex_front[0] + convex_front[2])
            cx_bench_front = 0.5 * (bench_front[0] + bench_front[2])
            if (cx_convex_front - cx_bench_front) / len_bench_front < self.thre1:
                return True

            return False

        
        return j_top()

    # DONE
    def j3(self):
        ## 将LED光源和光屏放置在凸透镜两侧
        ### 前视判断
        def j_front():
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if not ("光源板_前视" in self.d["front"].keys()):
                return False
            if not ("光屏_前视" in self.d["front"].keys()):
                return False
            convex = self.d["front"]["凸透镜_前视"][0]
            board = self.d["front"]["光源板_前视"][0]
            screen = self.d["front"]["光屏_前视"][0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_board = 0.5 * (board[0] + board[2])
            x_screen = 0.5 * (screen[0] + screen[2])
            if (x_convex - x_board) * (x_screen - x_convex) > 0:
                return True
            return False

        ### 顶视判断
        def j_top():
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            if not ("光源板_顶视" in self.d["top"].keys()):
                return False
            if not ("光屏_顶视" in self.d["top"].keys()):
                return False
            convex = self.d["top"]["凸透镜_顶视"][0]
            board = self.d["top"]["光源板_顶视"][0]
            screen = self.d["top"]["光屏_顶视"][0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_board = 0.5 * (board[0] + board[2])
            x_screen = 0.5 * (screen[0] + screen[2])
            if (x_convex - x_board) * (x_screen - x_convex) > 0:
                return True
            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    # DONE
    def j4(self):
        ## 调节凸透镜、光源和光屏三者的高度, 使光源中心、凸透镜中心和光屏中心在同一高度上
        if not ("凸透镜_前视" in self.d["front"].keys()):
            return False
        if self.is_first:
            if not ("光具座_前视" in self.d["front"].keys()):
                return False
        if not ("光屏_前视" in self.d["front"].keys()):
            return False
        if not ("凸透镜_镜身_前视" in self.d["front"].keys()):
            return False
        if not ("光屏_屏身_前视" in self.d["front"].keys()):
            return False
        if not ("光源板_前视" in self.d["front"].keys()):
            return False
        convex = self.d["front"]["凸透镜_镜身_前视"][0]
        screen = self.d["front"]["光屏_屏身_前视"][0]
        board = self.d["front"]["光源板_前视"][0]
        # 有像
        if ("像_前视" in self.d["front"].keys()):
            # 有光源
            if ("光源_前视" in self.d["front"].keys()):
                image = self.d["front"]["像_前视"][0]
                source = self.d["front"]["光源_前视"][0]
                # 高度不对等
                if abs(
                        0.5 * (image[1] + image[3]) - 0.5 *
                    (source[1] + source[3])) > 0.1 * (source[3] - source[1]):
                    return False
                # 成像偏心
                cy_min = screen[1] + 0.2 * (screen[3] - screen[1])
                cy_max = screen[1] + 0.8 * (screen[3] - screen[1])
                cy = 0.5 * (image[1] + image[3])
                if cy < cy_min or cy > cy_max:
                    return False
                return True
        # 没有像，最初调试阶段
        ### 一代相机
        if self.is_first:
            #### 没开灯
            if not ("光源_前视" in self.d["front"].keys()):
                # 利用畸变特性
                if abs(convex[1] - board[1]) > 0.1 * (convex[3] - convex[1]):
                    return False
                # 中心一致性
                if abs(
                        0.5 * (convex[1] + convex[3]) - 0.5 *
                    (screen[1] + screen[3])) > 0.1 * (convex[3] - convex[1]):
                    return False
            #### 开灯了
            else:
                source = self.d["front"]["光源_前视"][0]
                box_source = [0, source[1], 1, source[3]]
                box_convex = [0, convex[1], 1, convex[3]]
                box_screen = [
                    0, screen[1] + 0.2 * (screen[3] - screen[1]), 1,
                    screen[1] + 0.8 * (screen[3] - screen[1])
                ]
                # print(
                #     iou(box_source, box_convex), iou(box_source, box_screen),
                #     iou(box_screen, box_convex))
                if iou(box_source, box_convex) < 0.6:
                    return False
                if iou(box_source, box_screen) < 0.25:
                    return False
                if iou(box_screen, box_convex) < 0.5:
                    return False

        ## 二代相机
        else:
            # 开灯了
            if ("光源_前视" in self.d["front"].keys()):
                source = self.d["front"]["光源_前视"][0]
                y_convex = 0.5 * (convex[1] + convex[3])
                y_source = 0.5 * (source[1] + source[3])
                y_screen = 0.5 * (screen[1] + screen[3])
                if abs(y_convex - y_source) > 0.1 * (convex[3] - convex[1]):
                    return False
                if abs(y_convex - y_screen) > 0.1 * (convex[3] - convex[1]):
                    return False
                if abs(y_source - y_screen) > 0.1 * (convex[3] - convex[1]):
                    return False
            # 没开灯
            else:

                # 中心一致性
                if abs(
                        0.5 * (convex[1] + convex[3]) - 0.5 *
                    (screen[1] + screen[3])) > 0.1 * (convex[3] - convex[1]):
                    return False
                # y1 + 1/3(y2-y1)
                if abs(0.5 * (convex[1] + convex[3]) -
                       (0.666 * board[1] + 0.333 * screen[3])) > 0.1 * (
                           convex[3] - convex[1]):
                    return False
        return True

    # DONE
    def j5(self):
        ## 移动光源到某个位置，使光源离开凸透镜的距离大于两倍焦距
        ### 顶视必须包含
        if not ("凸透镜_顶视" in self.d["top"].keys()):
            return False
        if not ("光具座_顶视" in self.d["top"].keys()):
            return False
        if not ("光源板_顶视" in self.d["top"].keys()):
            return False
        if not ("光屏_顶视" in self.d["top"].keys()):
            return False
        ### 判断灯是否亮,灯没亮直接不看
        if not (("光源_顶视" in self.d["top"].keys()) or
                ("光源_前视" in self.d["front"].keys())):
            return False

        ### 判断距离关系
        source = self.d["top"]["光源板_顶视"][0]
        convex = self.d["top"]["凸透镜_顶视"][0]
        image = self.d["top"]["光屏_顶视"][0]
        bench = self.d["top"]["光具座_顶视"][0]
        if source[0] < convex[0] < image[0]:
            x_source = source[2]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[0]
        elif image[0] < convex[0] < source[0]:
            x_source = source[0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[2]
        else:
            return False
        # 一代相机，成像有畸变
        #'''
        if self.is_first:
            f_ratio = 0.10902896081771721
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])

            if dis_obj - dis_cov * 2 > 0.02 * (bench[2] - bench[0]):
                return True
        # 二代相机，无畸变
        else:
            f_ratio = 0.0884118190212373
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])

            if dis_obj - dis_cov * 2 > 0.02 * (bench[2] - bench[0]):
                return True
        #'''
        '''
        dis_obj = abs(x_source - x_convex)
        dis_img = abs(x_image - x_convex)
        ratio = dis_obj/dis_img
        if ratio>1.1:
            return True
        '''
        return False

    def j6(self):
        ## 移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止
        ### 没有像
        if not ("像_前视" in self.d["front"].keys()):
            return False, None

        def j_front():

            ### 前视必须包含
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if not ("光源板_前视" in self.d["front"].keys()):
                return False
            if not ("光屏_前视" in self.d["front"].keys()):
                return False
            ### 判断灯是否亮, 灯没亮直接不看
            if not ("光源_前视" in self.d["front"].keys()):
                return False
            image = self.d["front"]["像_前视"][0]
            source = self.d["front"]["光源_前视"][0]
            image_h = image[3] - image[1]
            source_h = source[3] - source[1]
            clear_score = self.get_clear_score(image)
            state = {
                "clear": clear_score,
                "size": image_h,
            }

            if source_h / image_h > 1.1:
                self.update_image("small", state)
            self.update_image("clear", state)
            return True

        def j_top():
            ### 顶视必须包含
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            if not ("光源板_顶视" in self.d["top"].keys()):
                return False
            if not ("光屏_顶视" in self.d["top"].keys()):
                return False

            ### 判断距离关系
            source = self.d["top"]["光源板_顶视"][0]
            convex = self.d["top"]["凸透镜_顶视"][0]
            bench = self.d["top"]["光具座_顶视"][0]
            image = self.d["top"]["光屏_顶视"][0]
            if source[0] < convex[0] < image[0]:
                x_source = source[2]
                x_convex = 0.5 * (convex[0] + convex[2])
                x_image = image[0]
            elif image[0] < convex[0] < source[0]:
                x_source = source[0]
                x_convex = 0.5 * (convex[0] + convex[2])
                x_image = image[2]
            else:
                return False
            # 一代相机，成像有畸变
            if self.is_first:
                f_ratio = 0.10902896081771721
                dis_obj = abs(x_source - x_convex)
                dis_cov = f_ratio * (bench[2] - bench[0])
                dis_img = abs(x_image - x_convex)

                if dis_obj - dis_cov * 2 < 0.01 * (bench[2] - bench[0]):
                    return False
                if dis_cov * 2 - dis_img < 0.01 * (bench[2] - bench[0]):
                    return False
                if dis_img - dis_cov < 0.01 * (bench[2] - bench[0]):
                    return False
                return True
            # 二代相机，无畸变
            else:
                f_ratio = 0.0884118190212373
                dis_obj = abs(x_source - x_convex)
                dis_cov = f_ratio * (bench[2] - bench[0])
                dis_img = abs(x_image - x_convex)

                if dis_obj - dis_cov * 2 < 0.01 * (bench[2] - bench[0]):
                    return False
                if dis_cov * 2 - dis_img < 0.01 * (bench[2] - bench[0]):
                    return False
                if dis_img - dis_cov < 0.01 * (bench[2] - bench[0]):
                    return False
                return True
            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    # DONE
    def j8(self):
        ## 移动光源到某个位置，使光源离开凸透镜的距离等于两倍焦距
        ### 顶视必须包含
        if not ("凸透镜_顶视" in self.d["top"].keys()):
            return False
        if not ("光具座_顶视" in self.d["top"].keys()):
            return False
        if not ("光源板_顶视" in self.d["top"].keys()):
            return False
        if not ("光屏_顶视" in self.d["top"].keys()):
            return False
        ### 判断灯是否亮,灯没亮直接不看
        if not (("光源_顶视" in self.d["top"].keys()) or
                ("光源_前视" in self.d["front"].keys())):
            return False
        ### 判断距离关系
        source = self.d["top"]["光源板_顶视"][0]
        convex = self.d["top"]["凸透镜_顶视"][0]
        bench = self.d["top"]["光具座_顶视"][0]
        image = self.d["top"]["光屏_顶视"][0]
        if source[0] < convex[0] < image[0]:
            x_source = source[2]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[0]
        elif image[0] < convex[0] < source[0]:
            x_source = source[0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[2]
        else:
            return False
        #'''
        # 一代相机，成像有畸变
        if self.is_first:
            f_ratio = 0.10902896081771721
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])
            if abs(dis_obj - dis_cov * 2) < 0.025 * (bench[2] - bench[0]):
                return True
        # 二代相机，无畸变
        else:
            f_ratio = 0.0884118190212373
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])
            if abs(dis_obj - dis_cov * 2) < 0.025 * (bench[2] - bench[0]):
                return True
        #'''
        '''
        dis_obj = abs(x_source - x_convex)
        dis_img = abs(x_image - x_convex)
        ratio = dis_obj/dis_img
        if ratio<=1.1 and ratio>=0.9:
            return True 
        '''

        return False

    def j9(self):
        ### 没有像
        if not ("像_前视" in self.d["front"].keys()):
            return False, None

        ## 移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止
        def j_front():

            ### 前视必须包含
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if not ("光源板_前视" in self.d["front"].keys()):
                return False
            if not ("光屏_前视" in self.d["front"].keys()):
                return False
            ### 判断灯是否亮, 灯没亮直接不看
            if not ("光源_前视" in self.d["front"].keys()):
                return False
            image = self.d["front"]["像_前视"][0]
            source = self.d["front"]["光源_前视"][0]
            image_h = image[3] - image[1]
            source_h = source[3] - source[1]
            clear_score = self.get_clear_score(image)
            state = {
                "clear": clear_score,
                "size": image_h,
            }
            if 0.9 < image_h / source_h < 1.1:
                self.update_image("middle", state)
                return True
            return False

        def j_top():
            ### 顶视必须包含
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            if not ("光源板_顶视" in self.d["top"].keys()):
                return False
            if not ("光屏_顶视" in self.d["top"].keys()):
                return False

            ### 判断距离关系
            source = self.d["top"]["光源板_顶视"][0]
            convex = self.d["top"]["凸透镜_顶视"][0]
            bench = self.d["top"]["光具座_顶视"][0]
            image = self.d["top"]["光屏_顶视"][0]
            if source[0] < convex[0] < image[0]:
                x_source = source[2]
                x_convex = 0.5 * (convex[0] + convex[2])
                x_image = image[0]
            elif image[0] < convex[0] < source[0]:
                x_source = source[0]
                x_convex = 0.5 * (convex[0] + convex[2])
                x_image = image[2]
            else:
                return False
            # 一代相机，成像有畸变
            if self.is_first:
                f_ratio = 0.10902896081771721
                dis_obj = abs(x_source - x_convex)
                dis_cov = f_ratio * (bench[2] - bench[0])
                dis_img = abs(x_image - x_convex)

                if abs(dis_obj - dis_cov * 2) > 0.025 * (bench[2] - bench[0]):
                    return False
                if abs(dis_img - dis_cov * 2) > 0.025 * (bench[2] - bench[0]):
                    return False
                return True
            # 二代相机，无畸变
            else:
                f_ratio = 0.0884118190212373
                dis_obj = abs(x_source - x_convex)
                dis_cov = f_ratio * (bench[2] - bench[0])
                dis_img = abs(x_image - x_convex)

                if abs(dis_obj - dis_cov * 2) > 0.025 * (bench[2] - bench[0]):
                    return False
                if abs(dis_img - dis_cov * 2) > 0.025 * (bench[2] - bench[0]):
                    return False
                return True
            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    def j11(self):
        ## 移动光源到某个位置，使光源离开凸透镜的距离大于一倍焦距小于两倍焦距
        ### 顶视必须包含
        if not ("凸透镜_顶视" in self.d["top"].keys()):
            return False
        if not ("光具座_顶视" in self.d["top"].keys()):
            return False
        if not ("光源板_顶视" in self.d["top"].keys()):
            return False
        if not ("光屏_顶视" in self.d["top"].keys()):
            return False
        ### 判断灯是否亮,灯没亮直接不看
        if not (("光源_顶视" in self.d["top"].keys()) or
                ("光源_前视" in self.d["front"].keys())):
            return False
        ### 判断距离关系
        source = self.d["top"]["光源板_顶视"][0]
        convex = self.d["top"]["凸透镜_顶视"][0]
        bench = self.d["top"]["光具座_顶视"][0]
        image = self.d["top"]["光屏_顶视"][0]
        if source[0] < convex[0] < image[0]:
            x_source = source[2]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[0]
        elif image[0] < convex[0] < source[0]:
            x_source = source[0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[2]
        else:
            return False
        # 一代相机，成像有畸变
        if self.is_first:
            f_ratio = 0.10902896081771721
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])
            dis_img = abs(x_image - x_convex)
            if dis_obj < dis_cov + 0.015 * (bench[2] - bench[0]):
                return False
            if dis_obj > 2 * dis_cov - 0.015 * (bench[2] - bench[0]):
                return False

            return True
        # 二代相机，无畸变
        else:
            f_ratio = 0.0884118190212373
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])
            dis_img = abs(x_image - x_convex)
            if dis_obj < dis_cov + 0.00 * (bench[2] - bench[0]):
                return False
            if dis_obj > 2 * dis_cov - 0.00 * (bench[2] - bench[0]):
                return False

            return True

        return False

    def j12(self):
        ### 没有像
        if not ("像_前视" in self.d["front"].keys()):
            return False, None
        ## 移动光屏找像，当光屏上出现像后，将光屏左右微调，直到像清晰为止
        def j_front():

            ### 前视必须包含
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if not ("光源板_前视" in self.d["front"].keys()):
                return False
            if not ("光屏_前视" in self.d["front"].keys()):
                return False
            ### 判断灯是否亮, 灯没亮直接不看
            if not ("光源_前视" in self.d["front"].keys()):
                return False
            image = self.d["front"]["像_前视"][0]
            source = self.d["front"]["光源_前视"][0]
            image_h = image[3] - image[1]
            source_h = source[3] - source[1]
            clear_score = self.get_clear_score(image)
            state = {
                "clear": clear_score,
                "size": image_h,
            }
            if image_h / source_h > 1.2:
                self.update_image("large", state)
                return True
            return False

        def j_top():
            ### 顶视必须包含
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            if not ("光源板_顶视" in self.d["top"].keys()):
                return False
            if not ("光屏_顶视" in self.d["top"].keys()):
                return False

            ### 判断距离关系
            source = self.d["top"]["光源板_顶视"][0]
            convex = self.d["top"]["凸透镜_顶视"][0]
            bench = self.d["top"]["光具座_顶视"][0]
            image = self.d["top"]["光屏_顶视"][0]
            if source[0] < convex[0] < image[0]:
                x_source = source[2]
                x_convex = 0.5 * (convex[0] + convex[2])
                x_image = image[0]
            elif image[0] < convex[0] < source[0]:
                x_source = source[0]
                x_convex = 0.5 * (convex[0] + convex[2])
                x_image = image[2]
            else:
                return False
            # 一代相机，成像有畸变
            if self.is_first:
                f_ratio = 0.10902896081771721
                dis_obj = abs(x_source - x_convex)
                dis_cov = f_ratio * (bench[2] - bench[0])
                dis_img = abs(x_image - x_convex)
                if dis_obj < dis_cov:
                    return False
                if dis_obj > 2 * dis_cov:
                    return False
                if dis_img - dis_cov * 2 < 0:
                    return False

                return True
            # 二代相机，无畸变
            else:
                f_ratio = 0.0884118190212373
                dis_obj = abs(x_source - x_convex)
                dis_cov = f_ratio * (bench[2] - bench[0])
                dis_img = abs(x_image - x_convex)
                if dis_obj < dis_cov:
                    return False
                if dis_obj > 2 * dis_cov:
                    return False
                if dis_img - dis_cov * 2 < 0:
                    return False

                return True
            return False

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    # DONE
    def j14(self):
        ## 移动光源到某个位置，使光源离开凸透镜的距离小于一倍焦距
        ### 顶视必须包含
        if not ("凸透镜_顶视" in self.d["top"].keys()):
            return False
        if not ("光具座_顶视" in self.d["top"].keys()):
            return False
        if not ("光源板_顶视" in self.d["top"].keys()):
            return False
        if not ("光屏_顶视" in self.d["top"].keys()):
            return False
        ### 判断灯是否亮,灯没亮直接不看
        if not (("光源_顶视" in self.d["top"].keys()) or
                ("光源_前视" in self.d["front"].keys())):
            return False
        ### 判断距离关系
        source = self.d["top"]["光源板_顶视"][0]
        convex = self.d["top"]["凸透镜_顶视"][0]
        bench = self.d["top"]["光具座_顶视"][0]
        image = self.d["top"]["光屏_顶视"][0]
        if source[0] < convex[0] < image[0]:
            x_source = source[2]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[0]
        elif image[0] < convex[0] < source[0]:
            x_source = source[0]
            x_convex = 0.5 * (convex[0] + convex[2])
            x_image = image[2]
        else:
            return False
        # 一代相机，成像有畸变
        if self.is_first:
            f_ratio = 0.10902896081771721
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])

            if dis_cov - dis_obj > 0:
                return True
        # 二代相机，无畸变
        else:
            f_ratio = 0.0884118190212373
            dis_obj = abs(x_source - x_convex)
            dis_cov = f_ratio * (bench[2] - bench[0])

            if dis_cov - dis_obj > 0:
                return True

        return False

    # DONE
    def j15(self):
        ## 移动光屏找像，观察光屏上是否有像
        ### 通过判断光屏移动的幅度来判断，间隔5帧的幅度变化
        if "光屏_前视" in self.d["front"].keys():
            if self.is_first:
                if not ("光具座_前视" in self.d["front"].keys()):
                    return False, None

                bench = self.d["front"]["光具座_前视"][0]
                bw = bench[2] - bench[0]
            else:
                bw = 1920
            screen = self.d["front"]["光屏_前视"][0]
            x = 0.5 * (screen[0] + screen[2])
            self.buffer_front.append(x)

            if len(self.buffer_front) == 3:
                self.buffer_front = self.buffer_front[1:]
                self.buffer_front = sorted(self.buffer_front)

                if self.buffer_front[-1] - self.buffer_front[0] > 0.01 * bw:
                    return True, "front"
                return False, None

        elif "光屏_顶视" in self.d["top"].keys():
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False, None

            bench = self.d["top"]["光具座_顶视"][0]
            bw = bench[2] - bench[0]
            screen = self.d["top"]["光屏_顶视"][0]
            x = 0.5 * (screen[0] + screen[2])
            self.buffer_top.append(x)

            if len(self.buffer_top) == 3:
                self.buffer_top = self.buffer_top[1:]
                self.buffer_front = sorted(self.buffer_top)
                if self.buffer_top[-1] - self.buffer_top[0] > 0.01 * bw:
                    return True, "top"
                return False, None

        return False, None

    # DONE
    def j16(self):
        ## 移去光屏，从光屏一侧透过凸透镜用眼睛观察像
        ### 前视判断法
        def j_front():
            if not ("凸透镜_前视" in self.d["front"].keys()):
                return False
            if self.is_first:
                if not ("光具座_前视" in self.d["front"].keys()):
                    return False
            if not ("光源板_前视" in self.d["front"].keys()):
                return False
            if not ("头" in self.d["front"].keys()):
                return False
            head = sorted(
                self.d["front"]["头"],
                key=lambda x: -(x[2] - x[0]) * (x[3] - x[1]))[0]
            optical_board = self.d["front"]["光源板_前视"][0]
            if self.is_first:
                optical_bench = self.d["front"]["光具座_前视"][0]
            else:
                optical_bench = [
                    0, optical_board[3] - 60, 1920, optical_board[3] + 110
                ]
            convex_glass = self.d["front"]["凸透镜_前视"][0]
            x_head = 0.5 * (head[0] + head[2])
            x_optical_board = 0.5 * (optical_board[0] + optical_board[2])
            x_convex_glass = 0.5 * (convex_glass[0] + convex_glass[2])
            w_bench = optical_bench[2] - optical_bench[0]
            x_bench = 0.5 * (optical_bench[2] + optical_bench[0])
            # 同侧
            if (x_convex_glass - x_head) * (
                    x_optical_board - x_convex_glass) < 0:
                if DEBUG_:
                    #print("same side")
                    pass
                return False
            # 头要稍微有点距离
            if not (abs(x_head - x_bench) > 0.15 * w_bench
                    and abs(x_head - x_convex_glass) >
                    abs(x_convex_glass - x_optical_board)):
                if DEBUG_:
                    #print("near head")
                    pass
                return False
            # 头离得太远，没在看
            if optical_bench[1] - head[3] > 50:
                if DEBUG_:
                    #print("too far head")
                    pass
                return False
            ## 一代相机
            if self.is_first:
                if abs(x_convex_glass - x_optical_board) > 0.2 * w_bench:
                    if DEBUG_:
                        print("dis err")
                    return False
            ## 二代相机
                if abs(x_convex_glass - x_optical_board) > 0.3 * w_bench:
                    return False

                
            return True

        # 顶视判断法
        def j_top():
            if not ("凸透镜_顶视" in self.d["top"].keys()):
                return False
            if not ("光具座_顶视" in self.d["top"].keys()):
                return False
            if not ("光源板_顶视" in self.d["top"].keys()):
                return False
            if not ("头" in self.d["top"].keys()):
                return False
            head = sorted(
                self.d["top"]["头"],
                key=lambda x: -(x[2] - x[0]) * (x[3] - x[1]))[0]
            optical_board = self.d["top"]["光源板_顶视"][0]
            optical_bench = self.d["top"]["光具座_顶视"][0]
            convex_glass = self.d["top"]["凸透镜_顶视"][0]
            x_head = 0.5 * (head[0] + head[2])
            x_optical_board = 0.5 * (optical_board[0] + optical_board[2])
            x_convex_glass = 0.5 * (convex_glass[0] + convex_glass[2])
            w_bench = optical_bench[2] - optical_bench[0]
            x_bench = 0.5 * (optical_bench[2] + optical_bench[0])
            # 同侧
            if (x_convex_glass - x_head) * (
                    x_optical_board - x_convex_glass) < 0:
                if DEBUG_:
                    #print("top same side")
                    pass
                return False
            # 头要稍微有点距离
            if not (abs(x_head - x_bench) > 0.15 * w_bench
                    and abs(x_head - x_convex_glass) >
                    abs(x_convex_glass - x_optical_board)):
                if DEBUG_:
                    #print("top near head")
                    pass
                return False
            # 头离得太远，没在看
            if optical_bench[1] - head[3] > 50:
                if DEBUG_:
                    #print("top too near head")
                    pass
                return False
            ## 一代相机
            if self.is_first:
                if abs(x_convex_glass - x_optical_board) > 0.15 * w_bench:
                    return False
            ## 二代相机
                if abs(x_convex_glass - x_optical_board) > 0.2 * w_bench:
                    return False
            return True

        if j_front():
            return True, "front"
        elif j_top():
            return True, "top"
        return False, None

    # DONE
    def j18(self):
        ## 完成实验并整理仪器

        if "桌面整洁_前视" in self.d["front"].keys():
            return True, "front"
        elif "桌面整洁_顶视" in self.d["top"].keys():
            return True, "top"
        else:
            if not self.is_first:
                area = [
                    0.25 * self.width, 0.5 * self.height, 0.75 * self.width,
                    self.height
                ]
                for key, vals in self.d["top"].items():
                    val = vals[0]
                    if iou(area, val) > 0:
                        return False, None
                return True, "top"
            else:
                area = [0, 0.6 * self.height, self.width, self.height]
                for key, vals in self.d["top"].items():
                    val = vals[0]

                    if iou(area, val) > 0:
                        return False, None
                return True, "top"
        return False, None

    # DONE
    def update_image(self, mode, des):
        def assignScore(idx, frame):
            self.assignScore(
                index=idx,
                img=frame[0],
                object=frame[1],
                conf=0.1,
                time_frame=frame[2],
                num_frame=frame[3],
                name_save=f"{idx}.jpg",
                preds=frame[4])

        if mode == "small":
            if self.smallest_frame is None:
                self.smallest_frame = (copy.copy(
                    self.frame_front), self.objects_front, self.time_front,
                                       self.num_frame_front, self.preds_front,
                                       des["size"], des["clear"])

                assignScore(6, self.smallest_frame)
                assignScore(7, self.smallest_frame)
            else:
                if des["size"] < self.smallest_frame[-2]:
                    self.smallest_frame = (copy.copy(
                        self.frame_front), self.objects_front, self.time_front,
                                           self.num_frame_front,
                                           self.preds_front, des["size"],
                                           des["clear"])
                    assignScore(6, self.smallest_frame)
                    assignScore(7, self.smallest_frame)
        elif mode == "middle":
            if self.clearest_frame is None:
                self.clearest_frame = (copy.copy(
                    self.frame_front), self.objects_front, self.time_front,
                                       self.num_frame_front, self.preds_front,
                                       des["size"], des["clear"])
                assignScore(9, self.clearest_frame)
                assignScore(10, self.clearest_frame)
            else:
                if des["clear"] > self.clearest_frame[-1]:
                    self.clearest_frame = (copy.copy(
                        self.frame_front), self.objects_front, self.time_front,
                                           self.num_frame_front,
                                           self.preds_front, des["size"],
                                           des["clear"])
                    assignScore(9, self.clearest_frame)
                    assignScore(10, self.clearest_frame)
        elif mode == "large":
            if self.largest_frame is None:
                self.largest_frame = (copy.copy(
                    self.frame_front), self.objects_front, self.time_front,
                                      self.num_frame_front, self.preds_front,
                                      des["size"], des["clear"])
                assignScore(12, self.largest_frame)
                assignScore(13, self.largest_frame)

            else:
                if des["size"] > self.largest_frame[-2]:
                    self.largest_frame = (copy.copy(
                        self.frame_front), self.objects_front, self.time_front,
                                          self.num_frame_front,
                                          self.preds_front, des["size"],
                                          des["clear"])
                    assignScore(12, self.largest_frame)
                    assignScore(13, self.largest_frame)


