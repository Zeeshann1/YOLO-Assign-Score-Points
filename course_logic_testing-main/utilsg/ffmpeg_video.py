# _*_ coding:utf-8 _*_

'''

python3

opencv

ffmpeg

rtmp 推流视频直播pipe:: Invalid argumentb

'''
import time

import cv2

import subprocess
import platform
import shlex

SYSTEM_NOW = platform.system()

# ffmpeg 推流

class FfmpegRtmp(object):
    def __init__(self, rtmpurl, appname,rtmpfile, width = 1920,height=1080):
        # self.rtmpUrl = "rtmp://127.0.0.1:1935/" + rtmpfile
        self.rtmpUrl = rtmpurl + appname+ "/" + rtmpfile

        self.width = width
        self.height = height
        self.sizeStr = "{}x{}".format(width, height)
        self.FPS = 25.0
        self.stat = True
        if width == 1920 and height == 1080:
            self.videoType = "yuv1080p"
        else:
            self.videoType = "yuv720p"

        if SYSTEM_NOW == "Linux":
            self.command = [
                '/home/xiding/workspace/ffmpeg-4.4.1-amd64-static/ffmpeg',
                '-y', '-an',
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', self.sizeStr,
                '-r', str(self.FPS),
                '-i', '-',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'ultrafast',
                '-f', 'flv',
                self.rtmpUrl
            ]
        else:
            self.command = [
                'D:\\soft\\ffmpeg-2021-12-20-git-631e31773b-essentials_build\\ffmpeg-2021-12-20-git-631e31773b-essentials_build\\bin\\ffmpeg',
                '-y', '-an',
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', self.sizeStr,
                '-r', str(self.FPS),
                '-i', '-',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'ultrafast',
                '-f', 'flv',
                self.rtmpUrl
            ]

        self.pipe = subprocess.Popen(self.command,shell=False,stdin=subprocess.PIPE)

    def write_img_ffmpeg(self,image):
        self.pipe.stdin.write(image.tobytes())

    def release_pipe_ffmpeg(self):
        self.pipe.terminate()

def main_decode_gpu(gpuid, rtspurl):
    cv2.setDevice(gpuid)
    # img_Mat =

if __name__ == "__main__":
    #rtmp://192.168.1.194/${app_name}/${stream_name}
    #ffmpeg -rtsp_transport tcp -i rtsp://admin:a1234567@192.168.5.211/video1 -vcodec copy -acodec copy -f flv -y rtmp://192.168.1.194/live/stream

    url_rtmp = "rtmp://192.168.1.194/"
    file_video = "EXPID_STDID"
    rtmpfile = "top"
    # fr = FfmpegRtmp(rtmpurl=url_rtmp,
    #                 appname=file_video,
    #                 rtmpfile=rtmpfile,
    #                 width=1920,
    #                 height=1080)


    # file_openvideo = "rtsp://admin:a1234567@192.168.12.221/h264/ch1/main/av_stream"
    file_openvideo = "rtsp://admin:a1234567@192.168.12.83/h264/ch1/main/av_stream"
    cap = cv2.VideoCapture(file_openvideo)
    time.sleep(6)
    while cap.isOpened():
        t = time.time()
        success, frame = cap.read()
        # print(frame.shape)
        if success:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # fr.write_img_ffmpeg(frame)
            print("{}\n".format(time.time()-t))
        # time.sleep(0.04)
    cap.release()
    # fr.release_pipe_ffmpeg()
