#!/usr/bin/python3
import cv2
import numpy as np
from math import sqrt
import RPi.GPIO as GPIO
import serial
from izbornik import Izbornik


COLORS_NUM=4 #crvena,zelena,plava,zuta
POVRSINA=1500 #sve manje od toga nije trazeni objekt, nego sum
CAMERA_PORT=0 #na koji USB ulaz je prikljucena kamera


#lower_x su donje HSV granice
#high_x su gornje HSV granice

#Hue 0-180
#Saturation 0-255
#Value 0-255


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

video=cv2.VideoCapture(CAMERA_PORT)
video.set(cv2.CAP_PROP_FRAME_WIDTH,400)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,400)
#video.set(cv2.CAP_PROP_BRIGHTNESS,1)
#video.set(cv2.CAP_PROP_CONTRAST,2)
#video.set(cv2.CAP_PROP_FPS,10)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)

UART=serial.Serial()
UART.baudrate=115200
UART.port='/dev/serial0'
UART.open()

message=Izbornik()
print("\r\nSaljem '"+message+"' na UART")
UART.write(message.encode())

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

flag=0
while True:
    #flag=1
    if GPIO.input(17)==GPIO.HIGH:
        flag=1
    if flag==1:
        _,frame=video.read()
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        n=0
        for i,j in colors:
            mask[n]=cv2.inRange(hsv,i,j)
            median[n]=cv2.medianBlur(mask[n],9)
            n+=1
        for n in range(0,COLORS_NUM):
            _,contours,_=cv2.findContours(median[n],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area=cv2.contourArea(cnt)
                #print('area='+str(area))
                approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
                x=approx.ravel()[0]
                y=approx.ravel()[1]

                # crvenu boju
                if n == 0:
                    if area > POVRSINA:
                        cv2.drawContours(frame, [approx], -1, (0, 0, 255), 3)
                        if len(approx) == 3:
                            cv2.putText(frame, 'Crvena piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                            crveni_br[0]+=1
                            if crveni_br[0] >=20:
                                clear_color_counters()
                                UART.write(b'23#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(frame, 'Crvena kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                            crveni_br[1]+=1
                            if crveni_br[1] >=20:
                                clear_color_counters()
                                UART.write(b'22#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(frame, 'Crvena kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                            crveni_br[2]+=1
                            if crveni_br[2] >= 20:
                                    clear_color_counters()
                                    UART.write(b'21#')
                                    flag=0

                # zelena boja
                elif n==1:
                    if area > POVRSINA:
                        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(frame, 'Zelena piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[0]+=1
                            if zeleni_br[0] >=20:
                                clear_color_counters()
                                UART.write(b'13#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(frame, 'Zelena kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[1]+=1
                            if zeleni_br[1] >=20:
                                clear_color_counters()
                                UART.write(b'12#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(frame, 'Zelena kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[2]+=1
                            if zeleni_br[2] >= 20:
                                clear_color_counters()
                                UART.write(b'11#')
                                flag=0

                # plava boja
                elif n==2:
                    if area > POVRSINA:
                        cv2.drawContours(frame, [approx], -1, (255, 0, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(frame, 'Plava piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
                            plavi_br[0]+=1
                            if plavi_br[0] >=20:
                                clear_color_counters()
                                UART.write(b'33#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(frame, 'Plava kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
                            plavi_br[1]+=1
                            if plavi_br[1] >=20:
                                clear_color_counters()
                                UART.write(b'32#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(frame, 'Plava kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0))
                            plavi_br[2]+=1
                            if plavi_br[2] >= 20:
                                clear_color_counters()
                                UART.write(b'31#')
                                flag=0

                # zuta boja
                elif n==3:
                    if area > POVRSINA:
                        cv2.drawContours(frame, [approx], -1, (255, 255, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(frame, 'Zuta piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[0]+=1
                            if zuti_br[0] >=20:
                                clear_color_counters()
                                UART.write(b'43#')
                                flag=0
                        elif len(approx) == 4:
                            cv2.putText(frame, 'Zuta kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[1]+=1
                            if zuti_br[1] >=20:
                                clear_color_counters()
                                UART.write(b'42#')
                                flag=0
                        elif len(approx) >= 7:
                            cv2.putText(frame, 'Zuta kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[2]+=1
                            if zuti_br[2] >= 20:
                                clear_color_counters()
                                UART.write(b'41#')
                                flag=0


        #cv2.imshow("mask red",mask[0])
        #cv2.imshow("mask green", mask[1])
        #cv2.imshow("mask blue", mask[2])
        #cv2.imshow("median red",median[0])
        #cv2.imshow("median green", median[1])
        #cv2.imshow("median blue", median[2])
        cv2.imshow("frame", frame)
        #cv2.imwrite('/home/pi/Desktop/image6.jpg',frame)

        key=cv2.waitKey(2)
        if key == 27:
            break


video.release()
GPIO.cleanup()
cv2.destroyAllWindows()