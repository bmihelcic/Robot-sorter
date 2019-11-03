from tkinter import *
import cv2
from PIL import Image,ImageTk

DASH_COUNT=14
RB_WIDTH=6
RB_HEIGHT=1
RB_FONT_SIZE=15

TOG_WIDTH=8

TERMINAL_X=40
TERMINAL_Y=20

class App:
    def __init__(self, root, window_title):
        self.root = root
        self.root.title(window_title)
        self.root.geometry('1024x600')
        self.top_frame = Frame(root)
        self.frame_A = Frame(self.top_frame)
        self.frame_B = Frame(self.top_frame)
        self.frame_C = Frame(self.top_frame)
        self.bottom_frame = Frame(root)

        self.video_source = 2

        # open video source
        self.vid = VideoCapture(self.video_source)

        self.label_A = Label(self.top_frame, text=DASH_COUNT * "-" + " Spremnik A " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=0)
        self.label_B = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik B " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=1)
        self.label_C = Label(self.top_frame, text=DASH_COUNT * '-' + " Spremnik C " + DASH_COUNT * "-", bd=2, relief="solid", fg='white', bg='grey').grid(row=0,column=2)
        self.spremnik_A = Spremnik(self.frame_A)
        self.spremnik_B = Spremnik(self.frame_B)
        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(self.bottom_frame, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(row=0,column=2)

        self.frame_A.grid(row=1, column=0)
        self.frame_B.grid(row=1, column=1)
        self.top_frame.pack()
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

class VideoCapture:
     def __init__(self, video_source):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

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

class Spremnik:
    oblik=0
    boja=0
    def __init__(self,frame):
        Label(frame, text="OBLICI").grid(row=0, column=0)
        Label(frame, text="BOJA").grid(row=0, column=1)
        Label(frame, text="MASA").grid(row=0, column=2)
        self.toggle_btn_oblikA = Button(frame, text="OFF", bg='red', command=self.ToggleOblik, width=TOG_WIDTH)
        self.toggle_btn_oblikA.grid(row=1, column=0)
        self.toggle_btn_bojaA = Button(frame, text="OFF", bg='red', command=self.ToggleOblik, width=TOG_WIDTH)
        self.toggle_btn_bojaA.grid(row=1, column=1)
        self.toggle_btn_masaA = Button(frame, text="OFF", bg='red', command=self.ToggleOblik, width=TOG_WIDTH)
        self.toggle_btn_masaA.grid(row=1, column=2)
        self.radio_btn_kuglaA = Radiobutton(frame, variable=self.oblik, value=1, text='kugla', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_kuglaA.grid(row=2, column=0)
        self.radio_btn_kockaA = Radiobutton(frame, variable=self.oblik, value=2, text='kocka', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_kockaA.grid(row=3, column=0)
        self.radio_btn_piramidaA = Radiobutton(frame, variable=self.oblik, value=3, text='piramida', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_piramidaA.grid(row=4, column=0)
        self.radio_btn_zelenaA = Radiobutton(frame, variable=self.boja, value=1, text='zelena', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_zelenaA.grid(row=2, column=1)
        self.radio_btn_crvenaA = Radiobutton(frame, variable=self.boja, value=2, text='crvena', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_crvenaA.grid(row=3, column=1)
        self.radio_btn_plavaA = Radiobutton(frame, variable=self.boja, value=3, text='plava', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_plavaA.grid(row=4, column=1)
        self.radio_btn_zutaA = Radiobutton(frame, variable=self.boja, value=4, text='zuta', state=DISABLED, width=RB_WIDTH, height=RB_HEIGHT, anchor=W, font=(None, RB_FONT_SIZE))
        self.radio_btn_zutaA.grid(row=5, column=1)
        self.label_masaA_min = Label(frame, text="  MIN", fg="grey")
        self.label_masaA_min.grid(row=2, column=2, sticky=W)
        self.entry_masaA_min = Entry(frame, width=5, state=DISABLED)
        self.entry_masaA_min.grid(row=2, column=2, columnspan=2, sticky=E)
        self.label_masaA_max = Label(frame, text="  MAX", fg="grey")
        self.label_masaA_max.grid(row=3, column=2, sticky=W)
        self.entry_masaA_max = Entry(frame, width=5, state=DISABLED)
        self.entry_masaA_max.grid(row=3, column=2, sticky=E)
    def ToggleOblik(self):
        self.oblik=not self.oblik
        print("ToggleOblik"+str(self.oblik))


 # Create a window and pass it to the Application object
App(Tk(), "Tkinter and OpenCV")