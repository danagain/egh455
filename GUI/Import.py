import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import csv
import os
project_root = os.getcwd() + "/GUI/"

class Import(object):
    def __init__(self, canvas, dataStructure, VideoAnalyzer, statusMessage):
        #inport button icons
        self.loadVideoIcon = PhotoImage(file = project_root + "/iconsBlue/importVideo.png")
        self.loadCSVIcon = PhotoImage(file = project_root + "/iconsBlue/importCSV.png")
        self.dataStructure = dataStructure
        self.canvas = canvas

        windowColour = "white"
        #create buttons
        self.loadVideoB    = tkinter.Button(canvas, text ="Load Video",   image = self.loadVideoIcon,  bg = windowColour, bd = 0, highlightthickness = 0, command = self.importVideo)
        self.loadCSVB      = tkinter.Button(canvas, text ="Load CSV",     image = self.loadCSVIcon,    bg = windowColour, bd = 0, highlightthickness = 0, command = self.importCSV)
        self.loadVideoB.bind("<Enter>", statusMessage.enterLoadVideo)
        self.loadVideoB.bind("<Leave>", statusMessage.leave)
        self.loadCSVB.bind("<Enter>", statusMessage.enterLoadCSV)
        self.loadCSVB.bind("<Leave>", statusMessage.leave)

        self.loadVideoB.place(x = 30, y = 25)
        self.loadCSVB.place(x = 80, y = 25)






    def importCSV(self, _event=0):
        videoIndex = self.dataStructure.getSelection()
        if videoIndex < 0:
            tkinter.messagebox.showinfo("Surf Safe Detection", "Please select a video to link a CSV with.")
            return

        if not self.dataStructure.getisProcessed(videoIndex):
            tkinter.messagebox.showinfo("Surf Safe Detection", "The video you selected is not processed.\n\nYou can only link CSV with a video which has been processed.")
            return

        if self.dataStructure.gethasCSV(videoIndex):
            result = tkinter.messagebox.askquestion("Delete", "This video is already linked to a CSV. \n\nDo you wish to link it with a different CSV?", icon='warning')
            print(result)
            if result == 'no':
                return

        videoPath = self.dataStructure.getSelectedVideoPath()
        videoName = videoPath.split("/")[-1]

        CSVPath = tkinter.filedialog.askopenfilename(
            parent=self.canvas, initialdir='C:/Tutorial',
            title='Import a CSV to link with '+videoName,
            filetypes=[('CSV files', '.csv')]
            )

        if not CSVPath:
            return

        with open(CSVPath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            list = []

            check = True
            for row in readCSV:
                if check:
                    if row[0] != 'FrameNumber' or row[1] != 'PredictionString':
                        tkinter.messagebox.showinfo("Surf Safe Detection", "The selected CSV column headings are incorrect")
                    check = False

                if len(row) > 2:
                    tkinter.messagebox.showinfo("Surf Safe Detection", "The selected CSV has to many rows")
                    return
                list.append(row[1])

            self.dataStructure.setHasCSV(videoIndex, list)





    def importVideo(self, _event=0):
        videoPath = tkinter.filedialog.askopenfilename(
            parent=self.canvas, initialdir='C:/Tutorial',
            title='Import a Video',
            filetypes=[('mp4 video', '.mp4'),
                        ('avi video', '.avi'),
                        ('All video', '*.*'),
                       ('png images', '.png')])
        if not videoPath:
            return
        result = tkinter.messagebox.askyesno("Surf Safe Detection", "Has the video being processed?")


        if not self.dataStructure.addVideo(videoPath, result, False):
            tkinter.messagebox.showinfo("Surf Safe Detection", "The selected file has already been imported")
