import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import csv
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import os

def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

def getListOfGroundTruthForImage(imageName):
    gtList = []
    with open('455_labels.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['filename'] == imageName:
                gtList.append(row)
    return gtList



def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df
    

# define the model options and run
def main():
    xml_dir = os.path.join(os.getcwd(), 'train/Annotations')
    xml_df = xml_to_csv(xml_dir)
    xml_df.to_csv('455_labels.csv', index=None)

    options = {"model": "cfg/455.cfg", "load": 18375, "threshold": 0.4}

    tfnet = TFNet(options)

    img = cv2.imread('/home/dan/darkflow/train/Images/dolphin_batch600027.jpg', cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # use YOLO to predict the image
    result = tfnet.return_predict(img)

    img.shape

    if os.path.exists("yolo.csv"):
        os.remove("yolo.csv")
    with open('yolo.csv', 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([ 'id','label', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax'])
    
    # Get the ground truth results in a list for the given image
    gtList = getListOfGroundTruthForImage('dolphin_batch600027.jpg')
    # Get the IOU value for each detection

    gtList.reverse()
    id = 0
    for i in range(0, len(result) - 1):
        tl = (result[i]['topleft']['x'], result[i]['topleft']['y'])
        br = (result[i]['bottomright']['x'], result[i]['bottomright']['y'])

        label = result[i]['label']
        boxA = {'x1':int(result[i]['topleft']['x']), 'y1':int(result[i]['topleft']['y']) , 'x2':int(result[i]['bottomright']['x']), 'y2':int(result[i]['bottomright']['y'])}
        
        boxB = {'x1':int(gtList[i]['xmin']), 'y1':int(gtList[i]['ymin']) , 'x2':int(gtList[i]['xmax']),'y2':int(gtList[i]['ymax']) }
        print( " get iou = " + str(get_iou(boxA, boxB)))
        box_1 = [[int(result[i]['topleft']['x']), int(result[i]['topleft']['y'])], [int(result[i]['bottomright']['x']), int(result[i]['topleft']['y'])], [int(result[i]['bottomright']['x']), int(result[i]['bottomright']['y'])], [int(result[i]['topleft']['x']), int(result[i]['bottomright']['y'])]]
        box_2 = [[int(gtList[i]['xmin']), int(gtList[i]['ymin'])], [int(gtList[i]['xmax']), int(gtList[i]['ymin'])], [int(gtList[i]['xmax']), int(gtList[i]['ymax']) ], [int(gtList[i]['xmin']), int(gtList[i]['ymax']) ]]
        iou = calculate_iou(box_1, box_2)
        print(str(iou))

        tl2 = (int(gtList[i]['xmin']), int(gtList[i]['ymin']))
        br2 = (int(gtList[i]['xmax']), int(gtList[i]['ymax']))
        id = id + 1
        img = cv2.rectangle(img, tl, br, (0, 255, 0), 7) # draw a ractangle onto an image
        img = cv2.rectangle(img, tl2, br2, (0, 100, 0), 7)
        img = cv2.putText(img, "IOU {0:.2f}".format(iou) + " " + label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2) # add laebl name
    writeFile.close()
    plt.imshow(img)
    plt.show()
     
if __name__ == "__main__" :
    main()
 
