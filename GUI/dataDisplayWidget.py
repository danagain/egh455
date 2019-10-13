from tkinter import ttk

from os.path import relpath


class ListSelection(object):
    def __init__(self, datastructure, videoStatFrame):
        self.tree = None
        self.datastructure = datastructure
        self.deleteCount=1;

        columnHeader = ("Video Name", "Analysed", "CSV")
        columnWidths = (185, 60, 40)
        height = 5
        self._setup_widgets(columnHeader, videoStatFrame, height)
        self._build_tree(columnHeader, columnWidths)

    def _setup_widgets(self, columnHeader, videoStatFrame, height):
        self.tree = ttk.Treeview(columns=columnHeader, show="headings", height=height)
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=videoStatFrame)
        vsb.grid(column=1, row=0, sticky='ns', in_=videoStatFrame)
        self.tree.bind("<Double-1>", self.playVideo)

        videoStatFrame.grid_columnconfigure(0, weight=1)
        videoStatFrame.grid_rowconfigure(0, weight=1)

#Adds headins to the treeview wiget
#Sets the colum iths of the treeview wiget
    def _build_tree(self, columnHeader, columnWidths):
        for col in columnHeader:
            self.tree.heading(col, text=col)
        for indx, val in enumerate(columnWidths):
            self.tree.column(columnHeader[indx], width=val)

# adds the items passed to the
# function to the tree
# items must be a matrix of strings
    def addItems(self, videoPath, processed, CSV):
        #delete all entrys in data display
        self.delete_items()
        videoName = "error"
        isProcessed = "error"
        hasCSV =    "error"
        for loopIndex in range(len(videoPath)):
            # split file name from path
            videoName = videoPath[loopIndex].split("/")[-1]
            # check has CSV covert to yes no
            if CSV[loopIndex]:
                hasCSV = "Yes"
            else:
                hasCSV = "No"
            #check if is processed convert to yes no
            if processed[loopIndex]:
                isProcessed = "Yes"
            else:
                isProcessed = "No"
            # add entry to display
            row = [[videoName], [isProcessed], [hasCSV]]

            self.tree.insert('', 'end', value=row)


# Deleats the current items in the treeview and adds the items passed to the
# function to the tree
# items must be a matrix of strings
    def delete_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            self.deleteCount = self.deleteCount +1;

    def getSelection(self):
        try:
            item = self.tree.selection()[0]
            item = item.split('I')
            item = int(item[1], 16)
            item = item - self.deleteCount
            return item
        except:
            return -1


    def playVideo(self, event):
        self.datastructure.playVideo(self.getSelection())
