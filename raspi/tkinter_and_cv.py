#!/usr/bin/python3
'''
created by Branimir Mihelcic, 2019
pip 10.0.1
setuptools 39.1.0
numpy 1.17.3
opencv-python 4.1.1.26
Pillow 6.2.1
'''
from tkinter import Tk,messagebox,Text,Scrollbar,Canvas,Frame,Button,Label
from tkinter.constants import *
from PIL import Image,ImageTk
from Spremnik import Spremnik
from VideoCapture import VideoCapture
import cv2
import numpy as np
import RPi.GPIO as GPIO
import serial

DASH_COUNT=25
# koliko puta mora neki objekt biti prepoznat prije slanja informacije...povecanje pouzdanosti
MIN_DETECT = 20

COLORS_NUM=4 #crvena,zelena,plava,zuta
POVRSINA=1500 #sve manje od toga nije trazeni objekt, nego shum
lower_red = np.array([156, 70, 50])
high_red = np.array([180, 255, 255])
lower_green = np.array([40, 100, 165])
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
# odnosno kada detektira najmanje MIN_DETECT puta neki objekt, za to sluze ovi brojaci
crveni_br=[0,0,0]
zeleni_br=[0,0,0]
plavi_br=[0,0,0]
zuti_br=[0,0,0]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)

UART=serial.Serial()
UART.baudrate=115200
UART.port='/dev/serial0'
UART.open()


''' main class, the whole application '''
class App(Frame):
    def __init__(self, parent, **kwargs):
        Frame.__init__(self,parent,**kwargs)
        self.message_list=['A',0,0,0,0,0,0,0,0,0,'B',0,0,0,0,0,0,0,0,0,'C',0,0,0,0,0,0,0,0,0,0,'#']
        ''' making some frames '''
        self.top_frame = Frame(parent)
        self.bottom_frame = Frame(parent)
        self.sub_frame_A = Frame(self.top_frame)
        self.sub_frame_B = Frame(self.top_frame)
        self.sub_frame_C = Frame(self.top_frame)
        self.sub_frame_D = Frame(self.bottom_frame)
        self.sub_frame_E = Frame(self.bottom_frame)
        self.sub_frame_F = Frame(self.bottom_frame)

        self.predmet_num=1
        self.flag = 0

        # open video source
        self.Video = VideoCapture(0)

        self.label_A = Label(self.top_frame, text=DASH_COUNT * "-" + " Spremnik A " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=0)
        self.label_B = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik B " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=1)
        self.label_C = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik C " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=2)
        self.spremnik_A = Spremnik(self,self.sub_frame_A)
        self.spremnik_B = Spremnik(self,self.sub_frame_B)
        self.spremnik_C = Spremnik(self,self.sub_frame_C)
        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(self.sub_frame_F, width=self.Video.width, height=self.Video.height)
        self.terminal = Text(self.sub_frame_D, height=20, width=40)
        self.terminal_scrollbar = Scrollbar(self.sub_frame_D, command=self.terminal.yview)
        self.terminal.config(yscrollcommand=self.terminal_scrollbar.set)
        self.analyze_sort_btn = Button(self.sub_frame_E, height=3, text="SORT", command=self.Analyze_Sort, width=8)
        self.start_stop_btn = Button(self.sub_frame_E, height=3, text="START",bg = "light green", command=self.Start_Stop, width=8)

        ''' gridding and packing '''
        self.sub_frame_A.grid(row=1, column=0)
        self.sub_frame_B.grid(row=1, column=1)
        self.sub_frame_C.grid(row=1, column=2)
        self.sub_frame_D.grid(row=0, column=0)
        self.sub_frame_E.grid(row=0, column=1,padx=60)
        self.sub_frame_F.grid(row=0, column=2)
        self.terminal.grid(row=0, column=0)
        self.terminal_scrollbar.grid(row=0, column=1, sticky='ns')
        self.analyze_sort_btn.grid(row=0,column=0,pady=35)
        self.start_stop_btn.grid(row=1, column=0)
        self.canvas.grid(row=0, column=0)
        self.top_frame.pack()
        Label(parent, text=270 * '-').pack()
        self.bottom_frame.pack()

        self.delay = 4
        self.update()

    def update(self):
        self.frame = self.Video.Get_Frame()
        if GPIO.input(17) == GPIO.HIGH:
            self.flag=True
        print(self.flag)
        if self.flag == True:
            self._Detection()
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.after(self.delay, self.update)

    def Start_Stop(self):
        if self.start_stop_btn['text'] == "START":
            self.start_stop_btn['text'] = "STOP"
            self.start_stop_btn['bg'] = 'red'
        elif self.start_stop_btn['text'] == "STOP":
            self.start_stop_btn['text'] = "START"
            self.start_stop_btn['bg'] = 'light green'
        try:
            self.Prepare_Message()
            self.message = ''.join(str(e) for e in self.message_list)
            self.terminal.insert(END, self.message + '\n')
            self.terminal.see('end')
            UART.write(self.message.encode())
            # print(message)
        except ValueError:
            messagebox.showwarning("Warning!", "Molim ispravan unos mase (0-1000 grama)")

    def Analyze_Sort(self):
        if self.analyze_sort_btn['text'] == "ANALYZE":
            self.analyze_sort_btn['text'] = "SORT"
        elif self.analyze_sort_btn['text'] == "SORT":
            self.analyze_sort_btn['text'] = "ANALYZE"

    def Prepare_Message(self):
        self.spremnici = [self.spremnik_A,self.spremnik_B,self.spremnik_C]
        for spremnik in self.spremnici:
            if spremnik.boja.get() == 0 and spremnik.oblik.get() == 0 and spremnik.toggle_btn_masa['text'] == 'OFF':
                for i in range(1+10*self.spremnici.index(spremnik), 10+10*self.spremnici.index(spremnik)):
                    self.message_list[i] = 0
            else:
                self.message_list[1+10*self.spremnici.index(spremnik)] = spremnik.oblik.get()
                self.message_list[2+10*self.spremnici.index(spremnik)] = spremnik.boja.get()
                if spremnik.toggle_btn_masa['text'] == 'ON':
                    if len(spremnik.entry_masa_min.get()) == 0 or len(spremnik.entry_masa_max.get()) == 0:
                        raise ValueError
                    if spremnik.masa_max.get() < spremnik.masa_min.get() or spremnik.masa_max.get() > 1000 or spremnik.masa_min.get() < 0:
                        raise ValueError
        ''' min masa '''
        temp = [0, 0, 0]
        list_min = [self.spremnik_A.masa_min.get(), self.spremnik_B.masa_min.get(), self.spremnik_C.masa_min.get()]
        for c in range(0, 3):
            choice = list_min[c]
            for i in range(0, 3):
                ostatak = choice % 10
                temp[2 - i] = ostatak
                choice = int(choice / 10)
            self.message_list[3 + c * 10] = temp[0]
            self.message_list[4 + c * 10] = temp[1]
            self.message_list[5 + c * 10] = temp[2]
        ''' max masa '''
        temp = [0, 0, 0, 0]
        list_max = [self.spremnik_A.masa_max.get(), self.spremnik_B.masa_max.get(), self.spremnik_C.masa_max.get()]
        for c in range(0, 3):
            choice = list_max[c]
            for i in range(0, 4):
                ostatak = choice % 10
                temp[3 - i] = ostatak
                choice = int(choice / 10)
            self.message_list[6 + c * 10] = temp[0]
            self.message_list[7 + c * 10] = temp[1]
            self.message_list[8 + c * 10] = temp[2]
            self.message_list[9 + c * 10] = temp[3]
        if self.start_stop_btn['text'] == "START":
            self.message_list[30] = 0
        elif self.analyze_sort_btn['text'] == "ANALYZE":
            self.message_list[30] = 2
        elif self.analyze_sort_btn['text'] == "SORT":
            self.message_list[30] = 1

    def _Detection(self):
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)
        n = 0
        for i, j in colors:
            mask[n] = cv2.inRange(self.hsv, i, j)
            median[n] = cv2.medianBlur(mask[n], 9)
            n += 1
        for n in range(0, COLORS_NUM):
            _,contours, _ = cv2.findContours(median[n], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # print('area='+str(area))
                approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
                x = approx.ravel()[0]
                y = approx.ravel()[1]

                # crvenu boju
                if n == 0:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (255, 0, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Crvena piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                            crveni_br[0] += 1
                            if crveni_br[0] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'23#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Crvena piramida\n')
                                self.terminal.see('end')
                                self.predmet_num+=1
                                self.flag = False
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Crvena kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                            crveni_br[1] += 1
                            if crveni_br[1] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'22#')
                                self.terminal.insert(END,str(self.predmet_num)+'. predmet: Crvena kocka\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag = False
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Crvena kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                            crveni_br[2] += 1
                            if crveni_br[2] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'21#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Crvena kugla\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag = False
                # zelena boja
                elif n==1:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (0, 255, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Zelena piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[0]+=1
                            if zeleni_br[0] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'13#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Zelena piramida\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Zelena kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[1]+=1
                            if zeleni_br[1] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'12#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Zelena kocka\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Zelena kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0))
                            zeleni_br[2]+=1
                            if zeleni_br[2] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'11#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Zelena kugla\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                # plava boja
                elif n==2:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (0, 0, 255), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Plava piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                            plavi_br[0]+=1
                            if plavi_br[0] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'33#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Plava piramida\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                        elif len(approx) == 4:
                            cv2.putText(self.frame, str(self.predmet_num)+'. predmet: Plava kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                            plavi_br[1]+=1
                            if plavi_br[1] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'32#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Plava kocka\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Plava kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
                            plavi_br[2]+=1
                            if plavi_br[2] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'31#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Plava kugla\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                # zuta boja
                elif n==3:
                    if area > POVRSINA:
                        cv2.drawContours(self.frame, [approx], -1, (255, 255, 0), 3)
                        if len(approx) == 3:
                            cv2.putText(self.frame, 'Zuta piramida', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[0]+=1
                            if zuti_br[0] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'43#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Zuta piramida\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                        elif len(approx) == 4:
                            cv2.putText(self.frame, 'Zuta kocka', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[1]+=1
                            if zuti_br[1] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'42#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Zuta kocka\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False
                        elif len(approx) >= 7:
                            cv2.putText(self.frame, 'Zuta kugla', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
                            zuti_br[2]+=1
                            if zuti_br[2] >= MIN_DETECT:
                                Clear_Color_Counters()
                                UART.write(b'41#')
                                self.terminal.insert(END, str(self.predmet_num)+'. predmet: Zuta kugla\n')
                                self.terminal.see('end')
                                self.predmet_num += 1
                                self.flag=False


def Clear_Color_Counters():
    for i in range(0, 3):
        crveni_br[i] = 0
        zeleni_br[i] = 0
        plavi_br[i] = 0
        zuti_br[i] = 0

if __name__ == '__main__':
    root = Tk()
    root.geometry("1024x600")
    app = App(root)
    app.pack()
    root.mainloop()
