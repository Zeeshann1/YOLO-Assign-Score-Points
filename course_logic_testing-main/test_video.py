#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

import numpy as np 
import cv2
import onnxruntime as rt
import torch
###import the experiment you want
from course.phy_convex_lens_cou import PHY_convex_lens_2

# In[2]:


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# In[3]:


def nms_boxes(boxes, scores,nms_thres):
    """Suppress non-maximal boxes.

    # Arguments
        boxes: ndarray, boxes of objects.
        scores: ndarray, scores of objects.

    # Returns
        keep: ndarray, index of effective boxes.
    """
    x = boxes[:, 0]
    y = boxes[:, 1]
    w = boxes[:, 2] - boxes[:, 0]
    h = boxes[:, 3] - boxes[:, 1]

    areas = w * h
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x[i], x[order[1:]])
        yy1 = np.maximum(y[i], y[order[1:]])
        xx2 = np.minimum(x[i] + w[i], x[order[1:]] + w[order[1:]])
        yy2 = np.minimum(y[i] + h[i], y[order[1:]] + h[order[1:]])

        w1 = np.maximum(0.0, xx2 - xx1 + 0.00001)
        h1 = np.maximum(0.0, yy2 - yy1 + 0.00001)
        inter = w1 * h1

        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= nms_thres)[0]
        order = order[inds + 1]
    keep = np.array(keep)
    return keep




def detect(img0,sess,draw=1,nc=17,con_thres = 0.4,nms_thres = 0.6,inshape = (640,384),
           anchors = [10, 13, 16, 30, 33, 23, 30, 61, 62, 45, 59, 119, 116, 90, 156, 198, 373, 326]):
    ###nc: number of class  in this experimnet
    img = cv2.resize(img0, inshape)
    img = img / 255.
    img = img[:, :, ::-1].transpose((2, 0, 1))  # HWC转CHW
    data = np.expand_dims(img, axis=0)  # 扩展维度至[1,3,384,640]

    scaleW = inshape[0]/img0.shape[1]
    scaleH = inshape[1]/img0.shape[0]
    input_name = sess.get_inputs()[0].name
    out0 = sess.run(['output0','output1','output2'], {input_name: data.astype(np.float32)})[0] 
    out1 = sess.run(['output0','output1','output2'], {input_name: data.astype(np.float32)})[1] 
    out2 = sess.run(['output0','output1','output2'], {input_name: data.astype(np.float32)})[2] 
    
    dict_res = {}
    for i in range(nc):
        dict_res[i] = {'boxes':[],'scores':[]}
    outs = [out0,out1,out2]
    
    for o in range(3):
        i = 0
        grid_w = outs[o].shape[3]
        grid_h = outs[o].shape[2]
        for a in range(3):
            for y in range(grid_h):
                for x in range(grid_w):
                    thispred = outs[o][0][a][y][x]
                    pred_x = sigmoid(thispred[0])
                    pred_y = sigmoid(thispred[1])
                    pred_w = sigmoid(thispred[2])
                    pred_h = sigmoid(thispred[3])
                    pred_conf = sigmoid(thispred[4])
                    if not pred_conf>con_thres:
                        continue
                    ##get the class
                    classpreds = thispred[5:]                
                    max_class_pred=np.max(classpreds)
                    max_class_conf= sigmoid(max_class_pred)
                    class_idx = np.where(classpreds==max_class_pred)[0][0]                
                    ##get xywh pred
                    c_x = 1.0 * (pred_x * 2 - 0.5 + x) * inshape[0] / grid_w;
                    c_y = 1.0 * (pred_y * 2 - 0.5 + y) * inshape[0] / grid_w;
                    c_w = 4.0 * pred_w * pred_w * anchors[o * 3 * 2 + a * 2];
                    c_h = 4.0 * pred_h * pred_h * anchors[o * 3 * 2 + a * 2 + 1]
                    ##
                    xmin = (c_x - 0.5 * c_w ) / scaleW;
                    ymin = (c_y - 0.5 * c_h ) / scaleH;
                    xmax = (c_x + 0.5 * c_w) / scaleW;
                    ymax = (c_y + 0.5 * c_h) / scaleH;
                    dict_res[class_idx]['boxes'].append([xmin,ymin,xmax,ymax])
                    dict_res[class_idx]['scores'].append(max_class_conf*pred_conf)   
    
    boxes, scores, classes = [],[],[]
    for i in range(nc):
        if len(dict_res[i]['boxes'])>0:
            keep = nms_boxes(np.array(dict_res[i]['boxes']),np.array(dict_res[i]['scores']),nms_thres)
            for j in range(len(keep)):
                classes.append(i)
                scores.append(dict_res[i]['scores'][keep[j]]) 
                boxes.append(dict_res[i]['boxes'][keep[j]]) 
    if draw and boxes is not None:
            draw(img0, boxes, scores, classes)
    pred = [boxes[i]+[scores[i]] 
              + [classes[i]] for i in range(len(boxes))]
    pred_tensor = torch.from_numpy(np.array(pred))
    return img0,pred_tensor


# In[5]:


def draw(image, boxes, scores, classes):
    """Draw the boxes on the image.

    # Argument:
        image: original image.
        boxes: ndarray, boxes of objects.
        classes: ndarray, classes of objects.
        scores: ndarray, scores of objects.
        all_classes: all classes name.
    """
    for box, score, cl in zip(boxes, scores, classes):
        top, left, right, bottom = box
        #print('class: {}, score: {}'.format(str(cl), score))
        #print('box coordinate left,top,right,down: [{}, {}, {}, {}]'.format(top, left, right, bottom))
        top = int(top)
        left = int(left)
        right = int(right)
        bottom = int(bottom)

        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(str(cl), score),
                    (top, left - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (0, 0, 255), 1)




###the video path
front_path = 'videos/front1.mp4'
top_path = 'videos/top1.mp4'

vc_front = cv2.VideoCapture(front_path)  # import video files
vc_top = cv2.VideoCapture(top_path)  # import video files

# determine whether to open normally
if vc_front.isOpened() and vc_top.isOpened():
    ret_front, frame_front = vc_front.read()
    ret_top, frame_top = vc_top.read()
else:
    ret_front,ret_top = False,False
    


count = 0  # count the number of pictures
frame_interval = 5  # video frame count interval frequency
frame_interval_count = 0
sess = rt.InferenceSession('models/phy_convex_lens_imaging_2X.onnx')
##names_label:all the objects in your experiment
names_label=['头',  '光源_前视',  '光屏_前视', '光源板_前视',  '光具座_前视',  '凸透镜_前视', 
 '像_前视',  '桌面整洁_前视', '光源_顶视', '光屏_顶视', '光源板_顶视', '像_顶视', 
 '光具座_顶视', '凸透镜_顶视',  '桌面整洁_顶视',  '凸透镜_镜身_前视', '光屏_屏身_前视']
logic_convex = PHY_convex_lens_2()

## experiment_id_now: the experiment id of your experiment
## exper_score_ids: all ids of scores,start from '1' 
## call_back_url: where to save score and error pics
logic_convex.setDefaultInfo(student_flag='test',
                       experiment_id_now='PTJTTJCX02',
                       exper_score_ids=['1','2','3','4','5','6','7','8','9','10'
                                        ,'11','12','13','14','15','16','17','18'],
                       call_back_url='result/')

path_save = 'result/'



# loop read video frame
while ret_front:
    ret_front, frame_front = vc_front.read()
    ret_top, frame_top = vc_top.read()
    time_front=vc_front.get(0)
    time_top=vc_top.get(0)
    # store operation every time f frame
    if frame_interval_count % frame_interval == 0:
        #save_image(count, frame)
        num = frame_interval_count / frame_interval
        frame_front,pred_front=detect(frame_front,sess,draw=0)
        frame_top,pred_top=detect(frame_top,sess,draw=0)
        frame_side,pred_side,time_side= None,None,None
        #time_top, time_front, time_side=frame_interval,frame_interval,frame_interval
        num_frame_top,num_frame_front, num_frame_side=count,count,count
        
        
        #print(time_front,time_top)
        
        
        logic_convex.run_one_result_process(
            frame_top, frame_front, frame_side, pred_top, pred_front,
            pred_side, time_top, time_front, time_side, num_frame_top,
            num_frame_front, num_frame_side, path_save, names_label)
        
        #cv2.imwrite('raw_pictures/front'+str(count)+'.jpg', frame_front)
        #cv2.imwrite('raw_pictures/top'+str(count)+'.jpg', frame_top)
        #process_detect()
        
        #logging.info("num：" + str(count) + ", frame: " +
        #             str(frame_interval_count))
        count += 1
    frame_interval_count += 1
    cv2.waitKey(1)

vc_front.release()
vc_top.release()







