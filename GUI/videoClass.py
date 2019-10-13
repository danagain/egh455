import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import os






class VideoPlayer:
    def __init__(self, rootcanvas, dataStructure, updateStatistics, statusMessage, VideoAnalyzer, videoSource=0):
        self.videoSource = videoSource
        self.rootcanvas=rootcanvas
        self.dataStructure = dataStructure
        self.updateStatistics = updateStatistics
        self.playImg = tkinter.PhotoImage(file = "./GUI/iconsBlue/play.png")
        self.pauseImg = tkinter.PhotoImage(file = "./GUI/iconsBlue/pause.png")

        self.play = False
        self.frameNumber = 0
        self.videoIndex = -1
        self.hasCSV = False

        # open video source
        self.video = CurrentVideo(self.videoSource)
        self.vidLength = self.video.getNumFrames()

        # Create video canvas
        self.imageCanvas = tkinter.Canvas(self.rootcanvas, width = 576, height = 400, bg="white", highlightthickness=1, highlightbackground="white")
        self.imageCanvas.pack()

        # Create playback functionalty canvas
        self.sliderCanvas = tkinter.Canvas(self.rootcanvas, width = 576, height = 80, bg="lightgrey", highlightthickness=1, highlightbackground="white")
        self.sliderCanvas.pack()
        self.frameSlider = FrameSlider(self.sliderCanvas, self.vidLength, self)

        # The play/pause Button
        self.btnPlayPause=tkinter.Button(self.sliderCanvas, command=self.playPause, image = self.playImg, bg = "lightgrey", bd = 0, highlightthickness = 0)
        self.btnPlayPause.bind("<Enter>", statusMessage.enterPlayPause)
        self.btnPlayPause.bind("<Leave>", statusMessage.leave)
        self.btnPlayPause.place(x = 1, y = 1)

        #Display frist frame
        self.updateFrame()
        #start loop
        self.loop()


    def addVideo(self, videoSource, videoIndex):
        self.video.__del__()
        self.videoIndex = videoIndex
        self.frameNumber = 0
        self.videoSource = videoSource
        self.video = CurrentVideo(videoSource)
        self.hasCSV = self.dataStructure.gethasCSV(videoIndex)
        if self.hasCSV:
            if self.video.getNumFrames() != self.dataStructure.getCSVLength(videoIndex)-1:
                self.hasCSV = False
                tkinter.messagebox.showinfo("Surf Safe Detection", "The number of frames in the video does not match \nthe number of statistics. \n\nThe video will be played without statistics")
        self.vidLength = self.video.getNumFrames()
        self.frameSlider.setLength(self.vidLength)
        self.dataStructure.setUpdate(False)

        #display frist frame
        self.updateFrame()
        self.play = True
        self.playPause()


    def playPause(self, _event=0):
        if self.play:
            self.play = False
            self.btnPlayPause.configure(image = self.playImg)
        else:
            self.play = True
            self.btnPlayPause.configure(image = self.pauseImg)


    def changeFrameTo(self, frame):
        if frame != self.frameNumber:
            self.video.setFrame(frame)
            self.frameNumber = frame
            self.updateFrame()

    def nextFrame(self, _event=0):
        if self.frameNumber != self.vidLength:
            self.changeFrameTo(self.frameNumber + 1)

    def lastFrame(self, _event=0):
        if self.frameNumber > 0:
            self.changeFrameTo(self.frameNumber - 2)

    def loop(self):
        if  self.dataStructure.getUpdate():
            videoSelection = self.dataStructure.getCurrentVideo()
            self.addVideo(self.dataStructure.getVideoPath(videoSelection), videoSelection)
        if self.play:
            self.updateFrame()
        self.imageCanvas.after(15, self.loop)


    def updateFrame(self):
        ret, frame = self.video.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.imageCanvas.create_image(289, 201, image = self.photo)
            self.frameNumber = self.frameNumber + 1
            self.frameSlider.setFrameScroll(self.frameNumber)
            if self.hasCSV:
                self.updateStatistics.updateStatistics(self.frameNumber, self.videoIndex)
            else:
                self.updateStatistics.delete()




class CurrentVideo:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            tkinter.messagebox.showerror("Surf Safe Detection", "Unable to open video at "+ video_source)
            return

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def getNumFrames(self):
        length = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        return length


    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                frameR = cv2.resize(frame,(580,403))
                return (ret, cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def setFrame(self, frameNumber):
        self.vid.set(1,frameNumber);

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()



class FrameSlider():
    def __init__(self, canvas, NumFrames, videoClass):
        self.vidLength = NumFrames
        self.videoClass = videoClass

        #The slider
        self.frameScroll = tkinter.Scale(canvas, from_=1, to=self.vidLength, orient=tkinter.HORIZONTAL,length = 480, showvalue=False, command =self.updateVideo)
        self.frameScroll.place(x=90, y = 32)

    def setFrameScroll(self, frameNumber):
        self.frameScroll.set(frameNumber)

    def setLength(self, vidLength):
        self.frameScroll.configure(to=vidLength)

    def updateVideo(self, args):
        val = self.frameScroll.get()
        self.videoClass.changeFrameTo(val)
