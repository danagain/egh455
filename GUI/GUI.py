import tkinter
from tkinter import *

import videoClass
import SSDdataStructure
import Process
import Import
import Export
import Status
import UpdateStatistics
import HelpMenu
import sys
import os

project_root = os.getcwd() + "/GUI/"

class SurfSafeDetection(object):
    def __init__(self, master):
        master.title("Surf Safe Detection")
        master.geometry('901x531')
        master.resizable(0, 0) #Don't allow resizing in the x or y direction
        self.master = master

        # TODO: surfer, dolphin and animal totals
        # restart video when it comes to the end

        ################################## GUI Frames ##################################
        windowColour        = "white"
        animalTotalFrame    = tkinter.Frame(self.master, bg=windowColour, width=580, height=200,  highlightthickness=1, highlightbackground="black")
        leftFrame           = tkinter.Frame(self.master, bg=windowColour, width=320, height=550, highlightthickness=1, highlightbackground="black")
        videoFrame          = tkinter.Frame(self.master, bg=windowColour, width=579, height=550, highlightthickness=1, highlightbackground="black")
        statusFrame         = tkinter.Frame(self.master, bg=windowColour, width=899, height=20,  highlightthickness=1, highlightbackground="black")
        videoSelectionFrame = tkinter.Frame(self.master, bg=windowColour, width=200, height=100,  highlightthickness=1, highlightbackground="white")
        videoStatFrame      = tkinter.Frame(leftFrame,     bg=windowColour, width=350, height=300, pady=3)

        animalTotalFrame.place(x = 320, y = 485)
        videoStatFrame.place(x =10, y = 280)
        videoSelectionFrame.place(y = 90, x = 10)
        statusFrame.place(x = 1, y = 510)
        leftFrame.place(x = 1, y = 1)
        videoFrame.place(x = 320, y = 1)


        ############################### Object Creation #####################################
        statusMessage = Status.StatusMessage(statusFrame)
        dataStructure = SSDdataStructure.DataStructure(videoSelectionFrame)
        videoStatistics = UpdateStatistics.UpdateStatistics(animalTotalFrame, videoStatFrame, dataStructure)
        VideoPlayer = videoClass.VideoPlayer(videoFrame, dataStructure, videoStatistics, statusMessage, self.master, project_root + "/455SSDWelcomeMessage.jpg" )
        processVideo = Process.Process(leftFrame, dataStructure, self.master, statusMessage)
        importVideoCSV = Import.Import(leftFrame, dataStructure, self.master, statusMessage)
        exportVideoCSV = Export.Export(leftFrame, dataStructure, self.master, statusMessage)


        ########################## Window Top Menu #########################################
        # a root menu to insert all the sub menus
        root_menu = tkinter.Menu(self.master)
        self.master.config(menu = root_menu)

        # file sub menu
        file_menu = tkinter.Menu(root_menu)
        root_menu.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label = "Import Video", command = importVideoCSV.importVideo)
        file_menu.add_command(label = "Import Image", command = importVideoCSV.importVideo)
        file_menu.add_command(label = "Import CSV", command = importVideoCSV.importCSV)
        file_menu.add_separator()
        file_menu.add_command(label = "Export CSV", command = exportVideoCSV.exportCSV)
        file_menu.add_command(label = "Save Video", command = exportVideoCSV.exportVideo)
        file_menu.add_command(label = "Save Image", command = exportVideoCSV.exportVideo)
        file_menu.add_separator()
        file_menu.add_command(label = "Quit", command = self.quit)

        # help sub menu
        help_menu = tkinter.Menu(root_menu)
        root_menu.add_cascade(label = "Help", menu = help_menu)
        help_menu.add_command(label = "Help", command = self.helpMenu)


        #shortcut functionalty
        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<h>", self.helpMenu)
        self.master.bind("<p>", processVideo.processVideo)
        self.master.bind('n', importVideoCSV.importVideo)
        self.master.bind("<Control-n>", importVideoCSV.importCSV)
        self.master.bind('s', exportVideoCSV.exportVideo)
        self.master.bind("<Control-s>", exportVideoCSV.exportCSV)
        self.master.bind("<space>", VideoPlayer.playPause)
        self.master.bind("<Left>", VideoPlayer.lastFrame)
        self.master.bind("<Right>", VideoPlayer.nextFrame)

    ########################## Help Menu #########################################
    def helpMenu(self, _event=0):
        Helpwindow = HelpMenu.helpMenu()

    ########################## Quit ##############################################
    def quit(self, _event=0):
        self.master.quit()


def main():
    root = tkinter.Tk()
    my_gui = SurfSafeDetection(root)
    root.mainloop()




if __name__ == "__main__":
    main()
