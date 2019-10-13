import tkinter
from tkinter import *
from tkinter import ttk

class Loading(object):
    def __init__(self):
        #create a loading  window to dislay loading graphic
        self.videoProcessing = tkinter.Toplevel(bg="white")
        self.videoProcessing.title('Surf Safe Detection')
        self.videoProcessing.geometry("300x80")
        self.videoProcessing.resizable(0, 0) #Don't allow resizing in the x or y direction

        self.frame = tkinter.Frame(self.videoProcessing, bg="white", width=420, height=300)
        self.frame.pack()
        self.message = tkinter.Label(self.frame, text = "Processing Video", bg = "white")
        self.message.place(x = 75, y = 30)
        self.count = 1
        self.loop()

    # Continuous loop which updates the loading graphic.
    def loop(self):
        if self.count == 1:
            self.message.config(text="Processing Video.")
        elif self.count == 2:
            self.message.config(text="Processing Video..")
        elif self.count == 3:
            self.message.config(text="Processing Video...")
        else:
            self.message.config(text="Processing Video")
            self.count = 0
        self.count=self.count+1
        self.frame.after(1000, self.loop)
