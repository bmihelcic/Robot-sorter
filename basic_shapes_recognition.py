import cv2
import numpy as np
from math import sqrt

def pitagora(tocka1,tocka2):
    a=abs(tocka2[0]-tocka1[0])
    b=abs(tocka2[1]-tocka1[1])
    return sqrt(pow(a,2)+pow(b,2))

def jednake_stranice(str1,str2):
    #print(abs(str1-str2))
    if abs(str1-str2) > 15:
        return 0
    else:
        return 1

COLORS_NUM=5

lower_red = np.array([160, 80, 50])
high_red = np.array([180, 255, 255])
lower_green = np.array([50, 50, 100])
high_green = np.array([90, 255, 255])
lower_blue = np.array([100, 80, 50])
high_blue = np.array([150, 255, 255])
lower_yellow = np.array([50, 80, 50])
high_yellow = np.array([70, 255, 255])
lower_white = np.array([0, 0, 230])
high_white = np.array([180, 60, 255])

colors=[(lower_red,high_red),
        (lower_green,high_green),
        (lower_blue,high_blue),
        (lower_yellow,high_yellow),
        (lower_white,high_white)]
mask=[np.zeros((640,480))] * COLORS_NUM
median=[np.zeros((640,480))] * COLORS_NUM

video=cv2.VideoCapture(2)
#fourcc=cv2.VideoWriter_fourcc(*'XVID')
#out=cv2.VideoWriter('/media/branimir/5bef6032-0370-4f59-935d-82210e02d20c/output.avi',fourcc,20.0,(640,480))
while True:
    _,frame=video.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    n=0
    for i,j in colors:
        mask[n]=cv2.inRange(hsv,i,j)
        median[n]=cv2.medianBlur(mask[n],9)
        n+=1
    for n in range(0,COLORS_NUM):
        contours,_=cv2.findContours(median[n],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area=cv2.contourArea(cnt)
            #print('area='+str(area))
            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
            x=approx.ravel()[0]
            y=approx.ravel()[1]
            if n == 0:
                if area > 5000:
                    cv2.drawContours(frame, [approx], -1, (0, 0, 255), 3)
                    if len(approx) == 4:
                        if jednake_stranice(pitagora(approx[0, 0], approx[3, 0]),
                                            pitagora(approx[0, 0], approx[1, 0])):
                            cv2.putText(frame, 'Crveni kvadrat', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                        else:
                            cv2.putText(frame, 'Crveni pravokutnik', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                    elif len(approx) > 7:
                        cv2.putText(frame, 'Crveni krug', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
            elif n==1:
                if area>5000:
                    cv2.drawContours(frame,[approx],-1,(0,255,0),3)
                    if len(approx) == 4:
                        if jednake_stranice(pitagora(approx[0,0],approx[3,0]),
                                            pitagora(approx[0,0],approx[1,0])):
                            cv2.putText(frame, 'Zeleni kvadrat', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                        else:
                            cv2.putText(frame, 'Zeleni pravokutnik', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                    elif len(approx) > 7:
                        cv2.putText(frame, 'Zeleni krug', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
            elif n==2:
                if area > 5000:
                    cv2.drawContours(frame, [approx], -1, (255, 0, 0), 3)
                    if len(approx) == 4:
                        if jednake_stranice(pitagora(approx[0, 0], approx[3, 0]),
                                            pitagora(approx[0, 0], approx[1, 0])):
                            cv2.putText(frame, 'Plavi kvadrat', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                        else:
                            cv2.putText(frame, 'Plavi pravokutnik', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                    elif len(approx) > 7:
                        cv2.putText(frame, 'Plavi krug', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
            elif n==3:
                if area > 5000:
                    cv2.drawContours(frame, [approx], -1, (255, 0, 0), 3)
                    if len(approx) == 4:
                        if jednake_stranice(pitagora(approx[0, 0], approx[3, 0]),
                                            pitagora(approx[0, 0], approx[1, 0])):
                            cv2.putText(frame, 'Žuti kvadrat', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                        else:
                            cv2.putText(frame, 'Žuti pravokutnik', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                    elif len(approx) > 7:
                        cv2.putText(frame, 'Žuti krug', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
            elif n == 4:
                if area > 5000:
                    cv2.drawContours(frame, [approx], -1, (255, 255, 255), 3)
                    if len(approx) == 4:
                        if jednake_stranice(pitagora(approx[0, 0], approx[3, 0]),
                                            pitagora(approx[0, 0], approx[1, 0])):
                            cv2.putText(frame, 'Bijeli kvadrat', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
                        else:
                            cv2.putText(frame, 'Bijeli pravokutnik', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
                    elif len(approx) > 7:
                        cv2.putText(frame, 'Bijeli krug', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

    #out.write(frame)
    #cv2.imshow("mask red",mask[0])
    #cv2.imshow("mask green", mask[1])
    #cv2.imshow("mask blue", mask[2])

    #cv2.imshow("median red",median[0])
    #cv2.imshow("median green", median[1])
    #cv2.imshow("median blue", median[2])
    cv2.imshow("median white", median[4])
    cv2.imshow("frame", frame)

    key=cv2.waitKey(2)
    if key == 27:
        break

video.release()
out.release()
cv2.destroyAllWindows()
