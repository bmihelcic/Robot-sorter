'''
created by Branimir Mihelcic, 2019
pip 10.0.1
setuptools 39.1.0
numpy 1.17.3
opencv-python 4.1.1.26
Pillow 6.2.1
'''
from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image,ImageTk

DASH_COUNT=25
RB_WIDTH=6
RB_HEIGHT=1
RB_FONT_SIZE=15

TOG_WIDTH=8

TERMINAL_X=40
TERMINAL_Y=20

VID_SCALE_FACTOR=60/100 #percentage


''' main class, the whole application '''
class App:
    def __init__(self, root, window_title):
        self.message_list=['A',0,0,0,0,0,0,0,0,0,'B',0,0,0,0,0,0,0,0,0,'C',0,0,0,0,0,0,0,0,0,'#']
        ''' making some frames '''
        self.root = root
        self.root.title(window_title)
        self.root.geometry('1024x600')
        self.top_frame = Frame(root)
        self.sub_frame_A = Frame(self.top_frame)
        self.sub_frame_B = Frame(self.top_frame)
        self.sub_frame_C = Frame(self.top_frame)
        self.bottom_frame = Frame(root)

        self.video_source = 0
        # open video source
        self.vid = VideoCapture(self.video_source)

        self.label_A = Label(self.top_frame, text=DASH_COUNT * "-" + " Spremnik A " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=0)
        self.label_B = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik B " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=1)
        self.label_C = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik C " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=2)
        self.spremnik_A = Spremnik(self.sub_frame_A)
        self.spremnik_B = Spremnik(self.sub_frame_B)
        self.spremnik_C = Spremnik(self.sub_frame_C)
        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(self.bottom_frame, width=self.vid.width, height=self.vid.height)
        self.terminal = Text(self.bottom_frame, height=TERMINAL_Y, width=TERMINAL_X)
        self.terminal_scrollbar = Scrollbar(self.bottom_frame, command=self.terminal.yview)
        self.terminal.config(yscrollcommand=self.terminal_scrollbar.set)
        self.send_btn = Button(self.bottom_frame, text="SEND", command=self.Send, width=8)

        ''' gridding and packing '''
        self.sub_frame_A.grid(row=1, column=0)
        self.sub_frame_B.grid(row=1, column=1)
        self.sub_frame_C.grid(row=1, column=2)
        self.terminal.grid(row=0, column=0)
        self.terminal_scrollbar.grid(row=0, column=1, sticky='ns')
        self.send_btn.grid(row=0, column=2, padx=50)
        self.canvas.grid(row=0, column=3)
        self.top_frame.pack()
        Label(self.root, text=270 * '-').pack()
        self.bottom_frame.pack()

        self.delay = 15
        self.update()
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.root.after(self.delay, self.update)

    def Send(self):
        try:
            self.Prepare_Message()
            self.message = ''.join(str(e) for e in self.message_list)
            self.terminal.insert(END, self.message + '\n')
            self.terminal.see('end')
            # print(message)
        except ValueError:
            messagebox.showwarning("Warning!", "Molim ispravan unos mase (0-1000 grama)")

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
                    spremnik.masa_min.set(int(spremnik.entry_masa_min.get()))
                    spremnik.masa_max.set(int(spremnik.entry_masa_max.get()))
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


class VideoCapture:
     def __init__(self, video_source):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)*VID_SCALE_FACTOR
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)*VID_SCALE_FACTOR

     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)

''' klasa za spremnike, toggle buttons, radio buttons, etc. '''
class Spremnik:
    def __init__(self,frame):
        self.oblik = IntVar()
        self.boja = IntVar()
        self.masa_min = IntVar()
        self.masa_max = IntVar()
        Label(frame, text="OBLICI").grid(row=0, column=0)
        Label(frame, text="BOJA").grid(row=0, column=1)
        Label(frame, text="MASA").grid(row=0, column=2)
        self.toggle_btn_oblik = Button(frame, text="OFF", bg='red', command=self.ToggleOblik, width=TOG_WIDTH)
        self.toggle_btn_oblik.grid(row=1, column=0)
        self.toggle_btn_boja = Button(frame, text="OFF", bg='red', command=self.ToggleBoja, width=TOG_WIDTH)
        self.toggle_btn_boja.grid(row=1, column=1)
        self.toggle_btn_masa = Button(frame, text="OFF", bg='red', command=self.ToggleMasa, width=TOG_WIDTH)
        self.toggle_btn_masa.grid(row=1, column=2)
        self.radio_btn_kugla = Radiobutton(frame, variable=self.oblik, value=1, text='kugla', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_kugla.grid(row=2, column=0)
        self.radio_btn_kocka = Radiobutton(frame, variable=self.oblik, value=2, text='kocka', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_kocka.grid(row=3, column=0)
        self.radio_btn_piramida = Radiobutton(frame, variable=self.oblik, value=3, text='piramida', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_piramida.grid(row=4, column=0)
        self.radio_btn_zelena = Radiobutton(frame, variable=self.boja, value=1, text='zelena', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_zelena.grid(row=2, column=1)
        self.radio_btn_crvena = Radiobutton(frame, variable=self.boja, value=2, text='crvena', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_crvena.grid(row=3, column=1)
        self.radio_btn_plava = Radiobutton(frame, variable=self.boja, value=3, text='plava', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_plava.grid(row=4, column=1)
        self.radio_btn_zuta = Radiobutton(frame, variable=self.boja, value=4, text='zuta', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_zuta.grid(row=5, column=1)
        self.label_masa_min = Label(frame, text="  MIN", fg="grey")
        self.label_masa_min.grid(row=2, column=2, sticky=W)
        self.entry_masa_min = Entry(frame, width=5, state=DISABLED)
        self.entry_masa_min.grid(row=2, column=2, columnspan=2, sticky=E)
        self.label_masa_max = Label(frame, text="  MAX", fg="grey")
        self.label_masa_max.grid(row=3, column=2, sticky=W)
        self.entry_masa_max = Entry(frame, width=5, state=DISABLED)
        self.entry_masa_max.grid(row=3, column=2, sticky=E)
        self._oblikState=False
        self._bojaState=False
        self._masaState=False

    def ToggleOblik(self):
        self._oblikState = not self._oblikState
        #print(self._oblikState)
        if self._oblikState == True:
            self.toggle_btn_oblik.config(bg='light green')
            self.toggle_btn_oblik.config(text='ON')
            self.radio_btn_kugla.config(state=NORMAL)
            self.radio_btn_kocka.config(state=NORMAL)
            self.radio_btn_piramida.config(state=NORMAL)
            self.radio_btn_kugla.select()
        elif self._oblikState == False:
            self.toggle_btn_oblik.config(bg='red')
            self.toggle_btn_oblik.config(text='OFF')
            self.radio_btn_kugla.config(state=DISABLED)
            self.radio_btn_kocka.config(state=DISABLED)
            self.radio_btn_piramida.config(state=DISABLED)
            self.oblik.set(0)

    def ToggleBoja(self):
        self._bojaState = not self._bojaState
        if self._bojaState == True:
            self.toggle_btn_boja.config(bg='light green')
            self.toggle_btn_boja.config(text='ON')
            self.radio_btn_crvena.config(state=NORMAL)
            self.radio_btn_plava.config(state=NORMAL)
            self.radio_btn_zelena.config(state=NORMAL)
            self.radio_btn_zuta.config(state=NORMAL)
            self.radio_btn_zelena.select()
        elif self._bojaState == False:
            self.toggle_btn_boja.config(bg='red')
            self.toggle_btn_boja.config(text='OFF')
            self.radio_btn_crvena.config(state=DISABLED)
            self.radio_btn_plava.config(state=DISABLED)
            self.radio_btn_zuta.config(state=DISABLED)
            self.radio_btn_zelena.config(state=DISABLED)
            self.boja.set(0)

    def ToggleMasa(self):
        self._masaState = not self._masaState
        if self._masaState == True:
            self.toggle_btn_masa.config(bg='light green')
            self.toggle_btn_masa.config(text='ON')
            self.entry_masa_max.config(state=NORMAL)
            self.entry_masa_min.config(state=NORMAL)
            self.label_masa_min.config(fg='black')
            self.label_masa_max.config(fg='black')
            self.masa_min.set(0)
            self.masa_max.set(1000)
            self.entry_masa_min.insert(0, 0)
            self.entry_masa_max.insert(0, 1000)
        elif self._masaState == False:
            self.toggle_btn_masa.config(bg='red')
            self.toggle_btn_masa.config(text='OFF')
            self.entry_masa_min.delete(0, END)
            self.entry_masa_max.delete(0, END)
            self.entry_masa_max.config(state=DISABLED)
            self.entry_masa_min.config(state=DISABLED)
            self.label_masa_min.config(fg='grey')
            self.label_masa_max.config(fg='grey')
            self.masa_min.set(0)
            self.masa_max.set(0)
            #self.min_masa_digits()
            #self.max_masa_digits()


 # Create a window and pass it to the Application object
App(Tk(), "SORTER IZBORNIK")