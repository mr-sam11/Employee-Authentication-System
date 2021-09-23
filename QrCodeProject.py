import cv2
import numpy as np
from pyzbar.pyzbar import decode
# decode is the function used here for finding Qr code and getting msg out of it and to find the location as well
from playsound import playsound

# cap is object for VideoCapture source inorder to turn on webcam
cap = cv2.VideoCapture(0)  # we have to define id in this case we are putting 0
cap.set(3,640)  # width id is 3
cap.set(4,480)  # height id is 4

with open('myDataFile.text') as f:      # opening myDataFile; file that contains authenticated person's ids
    myDataList = f.read().splitlines()  # it will read all the data and based on the lines it will add 1 item to the list, so every line is a new item
print(myDataList)

while True:
    success, img = cap.read()   # in order to read image
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')   # to convert in string
        print(myData)   # printing data
        if myData in myDataList:    # checking if the data is present in myDataList
            myOutput = 'Authorized' # if true: print authorized
            myColor = (0,255,0)     # output color: green
        else:
            myOutput = 'Un-Authorized'  # if false: print un-authorized
            myColor = (0, 0, 255)       #output color: red
            playsound('unauthenticated.mp3')    # play sound for un-authorized

        # since we dnt want to use rect for bounding box intead we want to use pokygon,
        # because rect will show us the approximated bounding box whereas even if we rotate img polygon will
        # actual bounding area
        # so for polygons we have to convert it into an array and we have to reshape that array
        # and send it to our polygonLines func
        pts = np.array([barcode.polygon],np.int32)  # we are going to put our polygon values inside pts
        pts = pts.reshape((-1,1,2)) # reshape
        cv2.polylines(img,[pts],True,myColor,5) # function for our polygons, True=closedPolygon, thickness=5
        pts2 = barcode.rect
        # here we are extracting the top point of rect because if we use polyLines, the problem with that is,
        # if we have an angle on our img then the text will rotate as well but we dnt wnt rotated text,
        # that stays const so that its easier to read and for that we are using the top points of our rect

        cv2.putText(img,myOutput,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,myColor,2)  # scale=0.9, thickness=2
    cv2.imshow('result', img)
    cv2.waitKey(1)  # waiting for time 1 milisec