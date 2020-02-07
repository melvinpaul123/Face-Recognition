import cv2,os
from PIL import Image
import sqlite3
import sys

path = os.path.dirname(os.path.abspath(__file__))
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(path+r'\trainer\trainer.yml')
font =cv2.FONT_HERSHEY_SIMPLEX #Creates a font

def getProfile(nbr_predicted):
    conn=sqlite3.connect(path+r'\facebase1.db')
    cmd="SELECT * FROM People WHERE ID="+str(nbr_predicted)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while 1:
    ret, img = cap.read()
    cv2.resizeWindow('img', 640,480)
    #cv2.line(img,(600,250),(0,250),(0,255,0),1)
    #cv2.line(img,(300,0),(300,500),(0,255,0),1)
    #cv2.circle(img, (300, 250), 5, (255, 255, 255), -1)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)

    for (x,y,w,h) in faces:
        roi_gray  = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        nbr_predicted, conf = recognizer.predict(roi_gray)
        profile=getProfile(nbr_predicted)
        print(conf)
        if(profile!=None):
            if conf <=45:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
                cv2.putText(img,"ID: "+str(profile[0]), (x,y+h+20),font, 1, (255,255,255),2) #Draw the text
                cv2.putText(img,"Name:"+str(profile[1]),(x,y+h+45),font, 1,(255,255,255),2);
                cv2.putText(img,"Age: "+str(profile[2]),(x,y+h+70),font, 1,(255,255,255),2);
                cv2.putText(img,"Gender: "+str(profile[3]),(x,y+h+95),font, 1, (255,255,255),2);
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),5)#(b,g,r)
                cv2.putText(img,"NOT IN THE SYSTEM", (x,y+h+20),font, 1, (255,255,255),2) #Draw the text

            

    cv2.imshow('img',img)
   
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
