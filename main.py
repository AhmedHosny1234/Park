import cv2
import cvzone
import pickle
import numpy as np

width,height =41,24

with open('CarParkPos','rb') as f:
        poslist=pickle.load(f)

def checkparkingSpace(imgproc):
 SpaceCounter=0
 for pos in poslist:
        x,y=pos
        imgcrop=imgproc[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgcrop)
        count=cv2.countNonZero(imgcrop)
        cvzone.putTextRect(img,str(count),(x,y+height-2),scale=.7,thickness=1,offset=0)
        if count <200:
             color=(0,255,0)
             SpaceCounter+=1
        else:
             color=(0,0,255)
           
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,1)           
 cvzone.putTextRect(img,f'free {SpaceCounter} / {len(poslist)} ',(50,100),scale=3,thickness=5,offset=20)

cap=cv2.VideoCapture('Untitled video - Made with Clipchamp.mp4')
while True:
    #reloade a video agin 
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    succes,img=cap.read()
    imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #to GrayLevel
    imgblur=cv2.GaussianBlur(imggray,(3,3),1)    #add blur to GrayLevel
    imgbinary=cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C
                                    ,cv2.THRESH_BINARY_INV,25,16)
    imgmedian=cv2.medianBlur(imgbinary,7)
    ker=np.ones((3,3),np.uint8)
    imgd=cv2.dilate(imgmedian,ker,iterations=1)
    checkparkingSpace(imgd)
    
    cv2.imshow("imagesss",imgd)
   
    cv2.imshow("imgbinary111 ",img)
    cv2.waitKey(1)