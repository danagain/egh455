import tkinter


class StatusMessage(object):
    def __init__(self, canvas):
        self.windowStatus = tkinter.Label(canvas, text = "Status:", bg = "white")
        self.windowStatus.place(y = 2, x = 4)


    def setStatus(self, message):
        self.windowStatus.config(text="Status: "+ str(message))


    def enterProcess(self, _event=0):
        self.setStatus("Process Video button")

    def leave(self, _event=0):
        self.setStatus(" ")

    def enterExportCSV(self, _event=0):
        self.setStatus("Export video statistics to a CSV button")

    def enterExportVideo(self, _event=0):
        self.setStatus("Export video button")

    def enterLoadVideo(self, _event=0):
        self.setStatus("Load video button")

    def enterLoadCSV(self, _event=0):
        self.setStatus("Load video statistics from a CSV button")

    def enterPlayPause(self, _event=0):
        self.setStatus("Play/Pause video button")
