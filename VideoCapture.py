import cv2
import numpy as np

VID_SCALE_FACTOR=60/100 #percentage

COLORS_NUM=4 #crvena,zelena,plava,zuta
POVRSINA=1500 #sve manje od toga nije trazeni objekt, nego sum
lower_red = np.array([156, 70, 50])
high_red = np.array([180, 255, 255])
lower_green = np.array([40, 70, 50])
high_green = np.array([100, 255, 255])
lower_blue = np.array([100, 100, 50])
high_blue = np.array([130, 255, 255])
lower_yellow = np.array([7, 100, 100])
high_yellow = np.array([35, 255, 255])
colors=[(lower_red,high_red),
        (lower_green,high_green),
        (lower_blue,high_blue),
        (lower_yellow,high_yellow)]
mask=[np.zeros((640,480))] * COLORS_NUM
median=[np.zeros((640,480))] * COLORS_NUM
# brojac za piramidu, kocku i kuglu
# podatci se salju na uart tek kada je rpi siguran za neki objekt
# odnosno kada detektira najmanje 30 puta neki objekt, za to sluze ovi brojaci
crveni_br=[0,0,0]
zeleni_br=[0,0,0]
plavi_br=[0,0,0]
zuti_br=[0,0,0]

def clear_color_counters():
    for i in range(0,3):
        crveni_br[i]=0
        zeleni_br[i]=0
        plavi_br[i]=0
        zuti_br[i]=0

class VideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.video = cv2.VideoCapture(video_source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH) * VID_SCALE_FACTOR
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) * VID_SCALE_FACTOR
        self.ret = 0

    def get_frame(self):
        if self.video.isOpened():
            _, self.frame = self.video.read()
            self.frame = cv2.resize(self.frame, (int(self.width), int(self.height)), interpolation=cv2.INTER_AREA)
            self.frame = cv2.flip(self.frame, 1)
            return (cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.video.isOpened():
            self.video.release()