import cv2
import pickle
import cvzone
import numpy as np


# video feed
cap = cv2.VideoCapture('carPark.mp4')
with open('CarParkPos','rb') as f:
    posList = pickle.load(f)
width , height = 107,48
def check_parking_space(imgPro):
  spaceCounter = 0
  for pos in posList:
    x,y = pos
    

    img_crop = imgPro[y:y+height,x:x+width]
    #cv2.imshow(str(x*y),img_crop)
    count = cv2.countNonZero(img_crop)
    
    if count < 900:
      color = (0,255,0)
      thickness = 5
      spaceCounter += 1
    else:
      color = (0,0,255)
      thickness = 2
    cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)
    cvzone.putTextRect(img,str(count),(x,y+height-3),scale = 1.5,thickness=2,
                       offset=0,colorR=color)
  cvzone.putTextRect(img,str(f'Free:{spaceCounter}/{len(posList)}'),(100,50),scale = 3,thickness=5,
                       offset=3,colorR=(0,250,0))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc(*'mp4v'),40,(frame_width,frame_height))
while True :
  if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    ## first one is current frame and second one is total frames if they are equal we are resetting frame to zero
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
  ret,img = cap.read()
  imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
  imgThresh = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV,25,16)
  imgMedian = cv2.medianBlur(imgThresh,5)
  kernel = np.ones((3,3),np.uint8)
  imgDialte = cv2.dilate(imgMedian,kernel,iterations=1)
  check_parking_space(imgDialte)
  cv2.imshow("Image",img)
  out.write(img)
  
  #cv2.imshow("ImageBlur",imgBlur)
  #cv2.imshow("ImageThresh",imgThresh)
  #cv2.imshow('medianBlur',imgMedian)
  #cv2.imshow('dialted',imgDialte)
  k =cv2.waitKey(10) & 0xFF
  if k == 27:
    break
cap.release()
out.release()
cv2.destroyAllWindows()
  



