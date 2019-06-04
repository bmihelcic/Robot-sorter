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

calibrator="HSV calibrator"
"""
x_koo=0
y_koo=0

def mouse_pos(event,x,y,flags,params):
    global x_koo,y_koo
    if event==cv2.EVENT_MOUSEMOVE:
        x_koo=x
        y_koo=y
"""
def nothing(x):
    print("Trackbar value: " + str(x))
    pass

video=cv2.VideoCapture(2)
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

while True:
    _,frame=video.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_hsv,upper_hsv)
    #cv2.putText(hsv,str(hsv[y_koo,x_koo]),(x_koo+20,y_koo),cv2.FONT_HERSHEY_COMPLEX,1,(0),2)
    #cv2.imshow("Frame", frame)
    cv2.imshow("HSV", hsv)
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
    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])


video.release()
cv2.destroyAllWindows()