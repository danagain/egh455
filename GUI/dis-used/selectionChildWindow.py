import tkinter
from tkinter import *
from tkinter import ttk

class ListboxWindow(object):
    def __init__(self, items, callingObject):
        self.window(items)
        self. callingObject = callingObject


    def window(self, items):
        #create a new window for video selection
        self.videoSelection = tkinter.Toplevel(bg="white")
        self.videoSelection.title('Surf Safe Detection')
        self.videoSelection.geometry("373x191")

        self.message = tkinter.Label(self.videoSelection, text = "Please select a video to link the imported CSV with", bg = "white")
        self.message.place(x = 5, y = 10)
        self.frame = tkinter.Frame(self.videoSelection, bg="white", width=420, height=300)
        self.frame.place(x = 5, y = 30)

        self.listbox = Listbox(self.frame, width=49)
        self.scrollbar = Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.grid(column=0, row=0, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')


        for val in  items:
            self.listbox.insert(END, val)

        self.OkB     = tkinter.Button(self.videoSelection, text ="Ok",     command = self.getPath, width = 10)
        self.cancelB = tkinter.Button(self.videoSelection, text ="Cancel", command = self.__del__, width = 10)
        self.OkB.place(y = 160, x = 60)
        self.cancelB.place(y = 160, x = 215)


    def getPath(self):
        self.pathIndex = self.listbox.get(ACTIVE)
        if not self.pathIndex:
            self.tkinter.messagebox.showinfo("Surf Safe Detection", "No video selected \n\nPlease select a Video to link the CSV with")
            return

        self.videoSelection.destroy()
        self.callingObject.saveFileTo(self.pathIndex)
        self.__del__()

    def __del__(self):
        self.videoSelection.destroy()
