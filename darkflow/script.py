import cv2
import matplotlib.pyplot as plt
import csv
import glob
import pandas as pd
import os
import sys
import time
import json
# sys.path.append("./darkflow/")


sys.path.append("./darkflow/")
from darkflow.darkflow.net.build import TFNet
# define the model options and run
def predict(videoPath):


    if os.path.exists("yolo.csv"):
        os.remove("yolo.csv")
    with open('yolo.csv', 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([ 'FrameNumber', 'PredictionString'])
        writeFile.close()

    options = {"model": "cfg/455.cfg", "load": 35250, "threshold": 0.4}
    frameNum = 0
    tfnet = TFNet(options)

    skip = False
    fileDir = os.listdir(os.getcwd() + "/frames")
    for filename in fileDir:
        
        img = cv2.imread(os.getcwd() + "/frames/" + filename, cv2.IMREAD_COLOR)
        #print(os.getcwd() + "/frames/" + filename)
        while img is None:
            print("image is none")
            img = cv2.imread(os.getcwd() + "/frames/" + filename, cv2.IMREAD_COLOR)
            time.sleep(2)
            if img is None:
                skip = True
                os.remove(os.getcwd() + "/frames/" + filename)
                break
        saved_img = img
        if not skip:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            print("not skipping")
            # use YOLO to predict the image
            result = tfnet.return_predict(img)

            #print("result equals " + str(result))
            img.shape

            id = 0
            csvString = ""
            for i in range(0, len(result)):
                tl = (result[i]['topleft']['x'], result[i]['topleft']['y'])
                br = (result[i]['bottomright']['x'], result[i]['bottomright']['y'])
                label = result[i]['label']
                #print(result[i])

                id = id + 1
                csvString += result[i]['label'] + " " + str(result[i]['confidence']) + " " + str(result[i]['bottomright']['x']) + " " \
                    + str(result[i]['bottomright']['x']) + " " + str(result[i]['topleft']['y']) + " " + str(result[i]['bottomright']['y']) + " "
                saved_img = cv2.rectangle(saved_img, tl, br, (0, 255, 0), 7) 
                saved_img = cv2.putText(saved_img, str(id) + " " + label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

            cv2.imwrite(os.getcwd() + "/output-images/" + filename, saved_img)
            with open('yolo.csv', 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([frameNum, csvString])
                frameNum = frameNum + 1
                csvString = ""
                writeFile.close()
            
            print("Finished processing image " + str(frameNum) + "/" + str(len(fileDir)))
    

        skip = False
    print("Making video")
    img_array = []
    for index in range(0, len(os.listdir(os.getcwd() + "/output-images/"))):
        print("sorted file name : " + str(img))
        img = cv2.imread(os.getcwd() + "/output-images/" + str(index) + ".jpg", cv2.IMREAD_COLOR)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    print(len(img_array))
    out = cv2.VideoWriter(os.getcwd() + "/" +  videoPath.split("/")[-1].split(".")[0]  +  "-yolo.avi" ,cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()
    return json.dumps({'csvpath': os.getcwd() + "/yolo.csv", 'videopath': os.getcwd() + "/" +  videoPath.split("/")[-1].split(".")[0] +  "-yolo.avi"})


    # plt.imshow(img)
    # plt.show()
     
#if __name__ == "__main__" :
   # predict()
 
