from .comm import *
from .comm.course_base import ConfigModel
from utilsg.litF import ts2ft




class PHY_light_reflex(ConfigModel):
    def __init__(self):
        super(PHY_light_reflex, self).__init__()
        self.initScore()

    def initScore(self):
        self.frame_id = 0
        self.exp_ok = [-1] * 6
        self.clean_frame_id = -1
        self.labels = [
            "draw_angle", "draw_dotted_line", "draw_reflection_marks",
            "draw_solid_line", "grubbing_sth", "hands_up", "leave",
            "mark_reflection_point", "measure_angle", "open_laser",
            "prepare_or_clean", "putting_sth", "talking", "watching"
        ]
        self.grid_width = 4
        self.grid_height = 4

    def patchFrames(self, frames):
        imgh, imgw = frames[0].shape[:2]
        img = np.zeros(shape=(imgh * 4, imgw * 4, 3), dtype=np.uint8)
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                idx = i * 4 + j
                img[i * imgh:(i + 1) * imgh, j * imgw:(j + 1) *
                    imgw, :] = frames[idx]
        return img

    def preProcess(self, preds):
        res = []
        preds = torch.sigmoid(preds)
        self.confs = preds
        for i, label in enumerate(self.labels):  ## 对每个类进行最大抑制

            if preds[i] > 0.8:
                res.append(label)
        return res

    def run_one_result_process(
            self, frame_top, frame_front, frame_side, pred_top, pred_front,
            pred_side, time_top, time_front, time_side, num_frame_top,
            num_frame_front, num_frame_side, path_save, names_label):

        #logger.info("Processing Reflex")
        self.time_top = time_top
        self.time_front = time_front
        self.time_side = time_side
        self.num_frame_top = num_frame_top
        self.num_frame_front = num_frame_front
        self.num_frame_side = num_frame_side
        self.num_frame = num_frame_front
        self.frame_top = frame_top
        self.frame_front = frame_front
        self.frame_side = frame_side
        # logger.info(frame_front[0].shape)
        front_true = False
        if pred_front != None and pred_front.shape[0]:
            front_true = True
        if front_true:
            #### TODO 这里没有执行rtmp_push_fun ####
            self.frame_id += 1
            if frame_front is None or pred_front is None:
                return
            preds = self.preProcess(pred_front)

            if -1 == self.exp_ok[0] and "open_laser" in preds:

                # assignScore
                patch_frame = self.patchFrames(frame_front)
                self.assignScore(1, patch_frame, time_front, None)
                self.exp_ok[0] = self.frame_id
                return

            if -1 == self.exp_ok[1]:
                f1 = "open_laser" in preds
                f2 = "mark_reflection_point" in preds
                if f1 and f2:
                    patch_frame = self.patchFrames(frame_front)
                    self.assignScore(2, patch_frame, time_front, None)
                    self.exp_ok[1] = self.frame_id
                    return

            if -1 == self.exp_ok[2] and -1 != self.exp_ok[1]:
                f1 = "grubbing_sth" in preds
                f2 = "putting_sth" in preds
                f3 = "draw_solid_line" in preds
                if f1 and f2 and f3:
                    patch_frame = self.patchFrames(frame_front)
                    self.assignScore(3, patch_frame, time_front, None)
                    self.exp_ok[2] = self.frame_id
                    return

            if -1 == self.exp_ok[3]:
                f1 = "grubbing_sth" in preds
                f2 = "putting_sth" in preds
                f3 = "draw_dotted_line" in preds
                if f1 and f2 and f3:
                    patch_frame = self.patchFrames(frame_front)
                    self.assignScore(4, patch_frame, time_front, None)
                    self.exp_ok[3] = self.frame_id
                    return

            if -1 == self.exp_ok[4]:
                f1 = "putting_sth" in preds
                f2 = "measure_angle" in preds
                if f1 and f2:
                    patch_frame = self.patchFrames(frame_front)
                    self.assignScore(5, patch_frame, time_front, None)
                    self.exp_ok[4] = self.frame_id
                    return

            if -1 == self.exp_ok[5]:
                if "prepare_or_clean" in preds:
                    self.clean_frame_id = self.frame_id
                else:
                    f1 = "leave" in preds
                    f2 = "talking" in preds
                    f3 = "hands_up" in preds
                    if f1 or f2 or f3:
                        if self.clean_frame_id != -1 and self.frame_id - self.clean_frame_id > 2:
                            patch_frame = self.patchFrames(frame_front)
                            self.assignScore(6, patch_frame, time_front, None)
                            self.exp_ok[5] = self.frame_id
                            return
