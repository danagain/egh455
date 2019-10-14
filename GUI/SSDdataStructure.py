
import dataDisplayWidget

class DataStructure:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DataStructure.__instance == None:
            DataStructure()
            return DataStructure.__instance


    def __init__(self, canvas):
        """ Virtually private constructor. """
        if DataStructure.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DataStructure.__instance = self
            self.videoPath = []
            self.isProcessed = []
            self.hasCSV = []
            self.videoSelection = dataDisplayWidget.ListSelection(self, canvas)
            self.CurrentVideo = -1
            self.update = False

    # adds a video to the dataStructure
    def addVideo(self, path, isProcessed, hasCSV):
        if self.exists(path):
            return False
        #add items to data structure
        self.videoPath.append(path)
        self.isProcessed.append(isProcessed)
        self.hasCSV.append(hasCSV)
        #display added items
        self.updateDataDisplay()
        return True

    # updates the data display
    def updateDataDisplay(self):
        self.videoSelection.addItems(self.videoPath, self.isProcessed, self.hasCSV)
        self.update = True

    # sets the CSV list and the specified index
    def setHasCSV(self, index, list):
        self.hasCSV[index] = list.copy()
        self.updateDataDisplay()

    # checks if the path variable (given as an parameter) already exists in the data structure
    def exists(self, path):
        x = self.videoPath.count(path)
        if(x > 0):
            return True
        return False

    # returns the boolean variable update which indicates whether the
    # user has updated there video selection
    def getUpdate(self):
        return self.update

    # returns the video path at the selected index in the video path list
    def getVideoPath(self, index):
         return self.videoPath[index]

    # returns a boolean variable determining if the video stored at index has been
    # processed
    def getisProcessed(self, index):
          return self.isProcessed[index]

    # returns a boolean variable determining if the video stored at index is linked
    # a statistics data structure
    def gethasCSV(self, videoIndex):
        if self.hasCSV[videoIndex]:
            return True
        else:
            return False

    # returns the frame statistics located at the  parameters video index and frameNumber
    def getCSV(self, frameNumber, video):
        return self.hasCSV[video][frameNumber]

    # returns the number of rows in the CSV located at the parameter videoIndex
    def getCSVLength(self, videoIndex):
            return len(self.hasCSV[videoIndex])


    # def getProcessedVideo(self):
    #     processedVids = []
    #     for indx, val in enumerate(self.isProcessed):
    #         if val and not self.hasCSV[indx]:
    #             processedVids.append(self.videoPath[indx])
    #     return processedVids

    # returns the index of the video the user has selected.
    def getSelection(self):
        return self.videoSelection.getSelection()

    # returns the video path of the selected video
    # if no video is selected it returns false
    def getSelectedVideoPath(self):
        selectionIndex = self.getSelection()
        if (selectionIndex < 0):
            return False
        return self.getVideoPath(selectionIndex)

    # sets the boolean variable update which indicates whether the
    # user has updated there video selection
    def setUpdate(self, boolean):
        self.update = boolean

    
    def getIndex(self, path):
        return self.videoPath.index(path)
        
    def playVideo(self, selection):
        self.CurrentVideo = selection
        self.update = True


    def getCurrentVideo(self):
        return self.CurrentVideo



        
























        #stop moving
