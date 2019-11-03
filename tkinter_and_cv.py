import tkinter
import cv2
from PIL import Image,ImageTk

DASH_COUNT=14

class App:
    def __init__(self, root, window_title):
        self.root = root
        self.root.title(window_title)
        self.top_frame = tkinter.Frame(root)
        self.bottom_frame = tkinter.Frame(root)
        self.frame_A = tkinter.Frame(self.top_frame)
        self.frame_B = tkinter.Frame(self.top_frame)
        self.frame_C = tkinter.Frame(self.top_frame)
        self.video_source = 2

        # open video source
        self.vid = VideoCapture(self.video_source)

        self.label_A = tkinter.Label(self.top_frame, text=DASH_COUNT * "-" + " Spremnik A " + DASH_COUNT * "-", bd=2, relief="solid",
                        fg='white', bg='grey').grid(row=0,column=0)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.bottom_frame, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(row=0,column=2)

        self.top_frame.pack()
        self.bottom_frame.pack()

        self.delay = 15
        self.update()

        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
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


 # Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")