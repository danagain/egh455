import tkinter
from tkinter import *
import shutil
import csv
import os
project_root = os.getcwd() + "/GUI/"
class Export(object):
    def __init__(self, canvas, dataStructure, VideoAnalyzer, statusMessage):
        #export button icons
        self.exportVideoIcon = PhotoImage(file = project_root + "/iconsBlue/exportVideo.png")
        self.exportCSVIcon = PhotoImage(file = project_root + "/iconsBlue/exportCSV.png")
        self.dataStructure = dataStructure
        self.canvas = canvas
        self.statusMessage = statusMessage

        self.exportCSVB    = tkinter.Button(canvas, text ="Export CSV",   image = self.exportCSVIcon,  bg = "white", bd = 0, highlightthickness = 0, command = self.exportCSV)
        self.exportVideoB  = tkinter.Button(canvas, text ="Export Video", image = self.exportVideoIcon, bg = "white", bd = 0, highlightthickness = 0, command = self.exportVideo)
        self.exportCSVB.bind("<Enter>", statusMessage.enterExportCSV)
        self.exportCSVB.bind("<Leave>", statusMessage.leave)
        self.exportVideoB.bind("<Enter>", statusMessage.enterExportVideo)
        self.exportVideoB.bind("<Leave>", statusMessage.leave)

        self.exportVideoB.place(x = 200, y = 25)
        self.exportCSVB.place(x = 250, y = 25)


    def exportVideo(self, _event=0):
        videoPath = self.dataStructure.getSelectedVideoPath()
        if not videoPath:
            tkinter.messagebox.showinfo("Surf Safe Detection", "Please select a video to export.")
            return
        self.saveFileTo(videoPath)


    def saveFileTo(self, path):
        videoName = path.split("/")[-1]
        self.canvas.filename = tkinter.filedialog.asksaveasfilename(
            parent=self.canvas, initialdir='C:/Tutorial',
            title="Select a location for "+videoName,
            filetypes=[('media', '.mp4'),
                       ("all files","*.*")],
            initialfile = videoName
            )

        if not self.canvas.filename:
            return
        try:
            newPath = shutil.copy(path, self.canvas.filename)
        except:
            tkinter.messagebox.showinfo("Surf Safe Detection", "There has been an unexped error exporting the video")
            return

        tkinter.messagebox.showinfo("Surf Safe Detection", "Video successfully exported")


    def exportCSV(self, _event=0):
        videoPath = self.dataStructure.getSelectedVideoPath()
        selection = self.dataStructure.getSelection()
        if not videoPath:
            tkinter.messagebox.showinfo("Surf Safe Detection", "Please select a videos statistics to export.")
            return

        if not self.dataStructure.gethasCSV(selection):
            tkinter.messagebox.showinfo("Surf Safe Detection", "There is no CSV linked with this video.\n\nPlease select a videos statistics to export.")
            return

        videoName = videoPath.split("/")[-1]
        CSVName = str(videoName.split(".")[0])+" statistics.CSV"
        self.canvas.filename = tkinter.filedialog.asksaveasfilename(
            parent=self.canvas, initialdir='C:/Tutorial',
            title="Select a location for "+videoName + " statictics",
            filetypes=[('media', '.CSV')],
            initialfile = CSVName
            )

        if not self.canvas.filename:
            return

        try:
            with open(self.canvas.filename, mode='w') as csv_file:
                fieldnames = ['FrameNumber', 'PredictionString']
                writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(fieldnames)

                for i in range(self.dataStructure.getCSVLength(selection)-1):
                    string = [i , self.dataStructure.getCSV(i+1, selection)]
                    print(string)
                    writer.writerow(string)
        except:
            tkinter.messagebox.showinfo("Surf Safe Detection", "There has been an unexped error exporting the CSV")
            return

        tkinter.messagebox.showinfo("Surf Safe Detection", "succesfully exported "+videoName.split(".")[0]+ " to CSV")





















# stop
