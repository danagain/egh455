import tkinter

class helpMenu(object):
    def __init__(self):
        self.help = tkinter.Toplevel(bg="white")
        self.help.title('Surf Safe Detection Help')
        self.help.geometry("650x400")

        scrollbar = tkinter.Scrollbar(self.help)
        scrollbar.pack(side='right', fill='y')

        T = tkinter.Text(self.help, height=10, width=100, yscrollcommand=scrollbar.set)
        T.pack(side='left', fill='both')

        scrollbar.config(command=T.yview)

        ## Style Tags
        T.tag_configure('Title', font=('Arial', 18, 'bold'))
        T.tag_configure('heading', font=('Arial', 15, 'bold'))
        T.tag_configure('text', font=('Arial', 15, 'bold'))

        #text
        str = "Surf Safe Detection Help Menu\n\n"
        T.insert('end',str, 'Title')

        str = "Import a Video\n"
        T.insert('end',str, 'heading')

        str = """Step 1: Press the import video button on the GUI home screen or press the 'n' key\n
Step 2: Select a video from the local operating system\n
Step 3: Select yes in the pop up window if the video has been process\n\n\n"""
        T.insert('end',str)

        str = "Import a CSV\n"
        T.insert('end',str, 'heading')

        str = """Step 1: you must first import video that has been processed\n
Step 2: Select a video that has been processed from the list of videos in the GUI\n
Step 3: Press the import CSV button on the GUI home screen or press the 'ctrl+n' keys\n
Step 4: Select a CSV from the local operating system\n\n\n"""
        T.insert('end',str)


        str = "Export a Video\n"
        T.insert('end',str, 'heading')

        str = """Step 1: Select the video you wish to export from the list of videos in the GUI\n
Step 2: Press the export video button on the GUI home screen or press the 's' key\n
Step 3: Select the location you wish to export the video to\n
Step 4: (optional) Change the file name\n\n\n"""
        T.insert('end',str)


        str = "Export a CSV\n"
        T.insert('end',str, 'heading')

        str = """Step 1: Select the CSV you wish to export from the list of videos in the GUI\n
Step 2: Press the export CSV button on the GUI home screen or press the 'ctrl+s' keys\n
Step 3: Select the location you wish to export the CSV to\n
Step 4: (optional) Change the file name\n\n\n"""
        T.insert('end',str)


        str = "Process a Video\n"
        T.insert('end',str, 'heading')

        str = """Step 1: you must first import video that has not been processed\n
Step 2: Select the video you wish to process from the list of videos in the GUI\n
Step 3: Select the DLM from the drop down menu\n
Step 4: Press the process button on the GUI home screen or press the 'p' key\n\n\n"""
        T.insert('end',str)


        str = "Play a Video\n"
        T.insert('end',str, 'heading')

        str = """Step 1: you must first import video\n
Step 2: Double click on video you wish to play from the list of videos in the GUI\n
Step 3: Press the play button\n
Step 4: (optional) Drag the slider to fast forward and rewind\n
step 5: (optional) Use arrow keys to fast forward and rewind\n\n\n"""
        T.insert('end',str)




















        #end
