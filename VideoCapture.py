import cv2
import numpy as np

VID_SCALE_FACTOR=60/100 #percentage

# koliko puta mora neki objekt biti prepoznat prije slanja informacije...povecanje pouzdanosti
MIN_DETECT = 20

COLORS_NUM=4 #crvena,zelena,plava,zuta
POVRSINA=1500 #sve manje od toga nije trazeni objekt, nego shum
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
            self.detection()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            return self.frame
        else:
            return None

    def detection(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        n = 0
        for i, j in colors:
            mask[n] = cv2.inRange(hsv, i, j)
            median[n] = cv2.medianBlur(mask[n], 9)
            n += 1
        for n in range(0, COLORS_NUM):
            contours, _ = cv2.findContours(median[n], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # print('area='+str(area))
                approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
                x = approx.ravel()[0]
                y = approx.ravel()[1]

                # crvenu boju
                if n == 0:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (0, 0, 255), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Crvena piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                            crveni_br[0] += 1
                            if crveni_br[0] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'23#')
                                flag = 0
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Crvena kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                            crveni_br[1] += 1
                            if crveni_br[1] >= MIN_DETECT:
                                clear_color_counters()
                               # UART.write(b'22#')
                                flag = 0
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Crvena kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                            crveni_br[2] += 1
                            if crveni_br[2] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'21#')
                                flag = 0
                # zelena boja
                elif n==1:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (0, 255, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Zelena piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[0]+=1
                            if zeleni_br[0] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'13#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Zelena kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[1]+=1
                            if zeleni_br[1] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'12#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Zelena kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[2]+=1
                            if zeleni_br[2] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'11#')
                                flag=0
                # plava boja
                elif n==2:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (255, 0, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Plava piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
                            plavi_br[0]+=1
                            if plavi_br[0] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'33#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Plava kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
                            plavi_br[1]+=1
                            if plavi_br[1] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'32#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Plava kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
                            plavi_br[2]+=1
                            if plavi_br[2] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'31#')
                                flag=0
                # zuta boja
                elif n==3:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (255, 255, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Zuta piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[0]+=1
                            if zuti_br[0] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'43#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Zuta kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[1]+=1
                            if zuti_br[1] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'42#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Zuta kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[2]+=1
                            if zuti_br[2] >= MIN_DETECT:
                                clear_color_counters()
                                #UART.write(b'41#')
                                flag=0

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.video.isOpened():
            self.video.release()