import cv2
import numpy as np



widthImg=360
heightImg=640

frameWidth=640
frameHeight=480
cap= cv2.VideoCapture(0)
cap.set(3,frameHeight)
cap.set(4,frameWidth)
cap.set(150,150)

def preProcessing(img):
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny=cv2.Canny(imgBlur,200,200)
    kernel=np.ones((5,5))
    imgDial= cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres=cv2.erode(imgDial,kernel,iterations=1)

    return imgThres
def getContours(img):
    biggest=np.array([])
    maxArea=0
    contours, hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area=cv2.contourArea(cnt)
        #print(area)
        #draw
        if area>5000:
         #cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
         #claculate the curve lenght that hlpes us to approximate the corners of our shape
         peri=cv2.arcLength(cnt,True)
         #print(peri)
         approx=cv2.approxPolyDP(cnt,0.02*peri,True)
         if area>maxArea and len(approx)==4:
             biggest=approx
             maxArea=area
    cv2.drawContours(imgContour,biggest, -1, (255, 0, 0), 15)
    return biggest

def reorder(myPoints):
      myPoints=myPoints.reshape((4,2))
      myPointsNew=np.zeros((4,1,2),np.int32)
      add= myPoints.sum(1)
      print("add",add)

      myPointsNew[0]=myPoints[np.argmin(add)]
      print("add argmin", myPointsNew[0])

      myPointsNew[3]=myPoints[np.argmax(add)]
      print("addargmax", myPointsNew[3])

      diff=np.diff(myPoints,axis=1)
      myPointsNew[1]=myPoints[np.argmin(diff)]
      print("add hight", myPointsNew[1])
      myPointsNew[2] = myPoints[np.argmax(diff)]
      print("add width", myPointsNew[2])
      #print("New points",myPointsNew)
      return myPointsNew



def getWarp(img,biggest):
    biggest1=reorder(biggest)

    #print(biggest.shape)
   # pts1=np.float32([ [231,103],[437,103],[231,449],[437,449] ]) #manually detection
    pts1=np.float32(biggest1)
    pts2 = np.float32([ [0,0], [widthImg,0], [0,heightImg], [widthImg,heightImg] ])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput= cv2.warpPerspective(img,matrix,(widthImg,heightImg))

    #cropped image
    #imgCropped=imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    #imgCroppedResize=cv2.resize(imgCropped,(widthImg,heightImg))
    return imgOutput




while True:
    #success, img=cap.read()
    img=cv2.imread("Resources/paper3.jpg")
    imgContour = img.copy()
    imgThres=preProcessing(img)
    biggest=getContours(imgThres)
    #print(biggest)
    imgWrapped= getWarp(img,biggest)
    cv2.imshow("Result",imgWrapped)
    cv2.imshow("Original",img)
    if cv2.waitKey(1) &0xFF== ord('q'):
        break