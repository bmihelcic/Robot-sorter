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

DASH_COUNT=25

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

        # open video source
        self.Video = VideoCapture(0)

        self.label_A = Label(self.top_frame, text=DASH_COUNT * "-" + " Spremnik A " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=0)
        self.label_B = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik B " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=1)
        self.label_C = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik C " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=2)
        self.spremnik_A = Spremnik(self.sub_frame_A)
        self.spremnik_B = Spremnik(self.sub_frame_B)
        self.spremnik_C = Spremnik(self.sub_frame_C)
        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(self.bottom_frame, width=self.Video.width, height=self.Video.height)
        self.terminal = Text(self.bottom_frame, height=20, width=40)
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

        self.delay = 4
        self.update()
        self.root.mainloop()

    def update(self):
        self.frame = self.Video.get_frame()
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
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

 # Create a window and pass it to the Application object
App(Tk(), "SORTER IZBORNIK")