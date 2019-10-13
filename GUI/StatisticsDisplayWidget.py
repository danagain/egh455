from tkinter import ttk


class ListSelection(object):
    def __init__(self, columnHeader, columnWidths, videoStatFrame, height):
        self.tree = None
        self._setup_widgets(columnHeader, videoStatFrame, height)
        self._build_tree(columnHeader, columnWidths)

    def _setup_widgets(self, columnHeader, videoStatFrame, height):
        self.tree = ttk.Treeview(columns=columnHeader, show="headings", height=height)
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=videoStatFrame)
        vsb.grid(column=1, row=0, sticky='ns', in_=videoStatFrame)

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
    def addItems(self, items):
        # for item in items:
        self.tree.insert('', 'end', values=items)

# Deleats the current items in the treeview and adds the items passed to the
# function to the tree
# items must be a matrix of strings
    def deleteItems(self):
        self.tree.delete(*self.tree.get_children())



    def getSelection(self):
        try:
            item = self.tree.selection()[0]
            item = item.split('I')
            item = int(item[1], 16)
            item = item - 1
            return item
        except:
            return -1


    def OnSelection(self, event):
        return self.getSelection()
