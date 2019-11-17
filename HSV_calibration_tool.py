#kalibracija hsv vrijednosti za neku masku
import cv2
import numpy as np

lh=0
ls=0
lv=0
uh=180
us=255
uv=255
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])

brightness=100
contrast=150
saturation=210
#hue=0

calibrator="HSV calibrator"

def nothing(x):
    print("Trackbar value: " + str(x))
    pass

video=cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,450)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,425)
#cv2.namedWindow("HSV")
#cv2.setMouseCallback("HSV", mouse_pos, 0)

cv2.namedWindow(calibrator)
cv2.createTrackbar("lower hue", calibrator, 0, 180, nothing)
cv2.setTrackbarPos("lower hue",calibrator,lh)
cv2.createTrackbar("lower saturation", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("lower saturation",calibrator,ls)
cv2.createTrackbar("lower value", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("lower value",calibrator,lv)
cv2.createTrackbar("upper hue", calibrator, 0, 180, nothing)
cv2.setTrackbarPos("upper hue",calibrator,uh)
cv2.createTrackbar("upper saturation", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("upper saturation",calibrator,us)
cv2.createTrackbar("upper value", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("upper value",calibrator,uv)

cv2.createTrackbar("Brightness", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("Brightness",calibrator,brightness)
cv2.createTrackbar("Contrast", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("Contrast",calibrator,contrast)
cv2.createTrackbar("Saturation", calibrator, 0, 255, nothing)
cv2.setTrackbarPos("Saturation",calibrator,saturation)
#cv2.createTrackbar("Hue", calibrator, 0, 255, nothing)
#cv2.setTrackbarPos("Hue",calibrator,hue)

while True:
    video.set(cv2.CAP_PROP_CONTRAST, contrast)
    video.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    video.set(cv2.CAP_PROP_SATURATION, saturation)
    #video.set(cv2.CAP_PROP_HUE, hue)
    _,frame=video.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_hsv,upper_hsv)
    cv2.imshow("slika",frame)
    #cv2.imshow("HSV", hsv)
    cv2.imshow(calibrator, mask)

    key=cv2.waitKey(3)
    if key == 27:
        break

    lh = cv2.getTrackbarPos("lower hue",calibrator)
    ls = cv2.getTrackbarPos("lower saturation",calibrator)
    lv = cv2.getTrackbarPos("lower value",calibrator)
    uh = cv2.getTrackbarPos("upper hue",calibrator)
    us = cv2.getTrackbarPos("upper saturation",calibrator)
    uv = cv2.getTrackbarPos("upper value",calibrator)
    brightness = cv2.getTrackbarPos("Brightness", calibrator)
    contrast = cv2.getTrackbarPos("Contrast", calibrator)
    saturation = cv2.getTrackbarPos("Saturation", calibrator)
    #hue = cv2.getTrackbarPos("Hue", calibrator)

    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])


video.release()
cv2.destroyAllWindows()