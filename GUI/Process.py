import tkinter
from tkinter import *
import requests
import loading
import os
import json
import csv
project_root = os.getcwd() + "/GUI/"

class Process(object):

    def __init__(self, canvas, dataStructure, VideoAnalyzer, statusMessage):
        self.dataStructure = dataStructure;
        self.DLM = ttk.Combobox(canvas, width=34, values=[ "YOLOv3", "Group 1",])
        self.statusMessage = statusMessage
        self.processIcon = PhotoImage(file = project_root + "/iconsBlue/process.png")
        self.processButton = tkinter.Button(canvas, text ="Process Video",  image = self.processIcon, bg = "white", bd = 0, highlightthickness = 0, command = self.processVideo)
        self.processButton.bind("<Enter>", statusMessage.enterProcess)
        self.processButton.bind("<Leave>", statusMessage.leave)


        DLMLable = tkinter.Label(canvas, text = "Select a video and DLM to process", bg = "white", font=("Helvetica", 10,"bold"))
        DLMLable.place(x = 55, y = 222)
        self.DLM.place(x = 55, y = 247)
        self.processButton.place(x = 8, y = 222)




    def processVideo(self, _event=0):
        vidSelection = self.dataStructure.getSelection()
        print(vidSelection)
        DLMselection = self.DLM.current()

        if vidSelection < 0:
            tkinter.messagebox.showinfo("Surf Safe Detection", "No video selected")
            return

        if DLMselection < 0:
            tkinter.messagebox.showinfo("Surf Safe Detection", "No DLM selected")
            return

        if self.dataStructure.getisProcessed(vidSelection):
            tkinter.messagebox.showinfo("Surf Safe Detection", "This video is already processed")
            return

        videoPath = self.dataStructure.getVideoPath(vidSelection)
        print(videoPath)

        self.GetRequest(vidSelection, DLMselection)



    def GetRequest(self, path, DLM):
        # loadingWindow = loading.Loading()

        if DLM == 0:
            DLM = "yolo"
        else:
            DLM = "ssd"

        res = requests.get("http://localhost:5000/" + DLM, headers = {'video-path' : os.getcwd() + '/test-data/testdata.mp4'})
        print("sending data to server")
        res = json.loads(res.content)



        ## TODO: The loading window is causing issues and the dataStructure.exists is throwing errors
        # loadingWindow.destroy()


        # add processed video
        # if self.dataStructure.exists(self, path):
        #     tkinter.messagebox.showinfo("Surf Safe Detection", "The video path already exists")
        #     return

        self.dataStructure.addVideo(res['videopath'], True, False)

        # add processed CSV
        with open(res['csvpath']) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            list = []

            check = True
            for row in readCSV:
        ########## debug #####################
                if check:
                    if row[0] != 'FrameNumber' or row[1] != 'PredictionString':
                        tkinter.messagebox.showinfo("Surf Safe Detection", "The selected CSV column headings are incorrect")
                    check = False

                if len(row) > 2:
                    tkinter.messagebox.showinfo("Surf Safe Detection", "The selected CSV has to many rows")
                    return

        #######################################
                list.append(row[1])

            #self.dataStructure.setHasCSV(videoIndex, list)
