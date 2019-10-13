import tkinter


class AnimalTotals(object):
    def __init__(self, canvas):

        self.surferTotal  = tkinter.Label(canvas,    text = "Surfer Total:", bg = "White")
        self.sharkTotal   = tkinter.Label(canvas,    text = "Shark Total:",  bg = "White")
        self.dolfinTotal  = tkinter.Label(canvas,    text = "Dolphin Total:", bg = "White")
        self.surferTotal.place(y = 5, x = 10)
        self.sharkTotal.place(y = 5, x = 210)
        self.dolfinTotal.place(y = 5, x = 400)

    # updates the lables below the GUI
    def setTotals(self, shark, dolphin, surfer):
        self.surferTotal.config(text="Surfer Total: "+ str(surfer))
        self.dolfinTotal.config(text="Dolphin Total: "+ str(dolphin))
        self.sharkTotal.config(text="Shark Total: "+ str(shark))

    def clearTotals(self):
        self.surferTotal.config(text="Surfer Total:")
        self.dolfinTotal.config(text="Dolphin Total:")
        self.sharkTotal.config(text="Shark Total:")
