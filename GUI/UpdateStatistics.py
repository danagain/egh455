import StatisticsDisplayWidget
import AnimalTotals


class UpdateStatistics:
    def __init__(self, animalTotalFrame, videoStatFrame, dataStructure):
        columnHeader = ("ID", "Object", "C.I", "Xmin", "Ymin", "Xmax", "Ymax")
        columnWidths = (25, 60, 40, 40, 40, 40, 40)
        self.videoStatisticTable = StatisticsDisplayWidget.ListSelection(columnHeader, columnWidths, videoStatFrame, height = 10)
        self.animalTotals = AnimalTotals.AnimalTotals(animalTotalFrame)
        self.dataStructure = dataStructure




    def updateStatistics(self, frameNumber, video):
        self.videoStatisticTable.deleteItems()
        statistics = self.dataStructure.getCSV(frameNumber, video)
        statistics = statistics.split()

        dolphinTotal = 0
        sharkTotal = 0
        surferTotal = 0
        objectNo = 1
        count = 0
        string = ['1']
        for x in range(len(statistics)):
            if count < 6:
                string.append(statistics[x])
                count = count + 1
            else:
                #update data viewer
                self.videoStatisticTable.addItems(string)

                # count animal totals
                if string[1].casefold() == 'dolphin':
                    dolphinTotal = dolphinTotal + 1
                elif string[1].casefold() == 'shark':
                    sharkTotal = sharkTotal + 1
                elif string[1].casefold() == 'surfer':
                    surferTotal = surferTotal + 1

                # clear string and update object number and count
                string.clear()
                objectNo = objectNo + 1
                string.append(objectNo)
                count = 0
                string.append(statistics[x])
                count = count + 1
        #Update Animal totals
        self.animalTotals.setTotals(sharkTotal, dolphinTotal, surferTotal)

    # deletes all the items in the video frame statistic table
    def delete(self):
        self.videoStatisticTable.deleteItems()
