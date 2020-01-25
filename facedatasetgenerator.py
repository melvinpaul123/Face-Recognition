import cv2
import sqlite3
import os
import sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(0)
i=0

def info(Id,Name,Age,Gen):
    conn=sqlite3.connect(path+r'\facebase1.db')
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE people SET NAME=' "+str(Name)+" ' WHERE ID="+str(Id)
        cmd2="UPDATE people SET AGE=' "+str(Age)+" 'WHERE ID="+str(Id)
        cmd3="UPDATE people SET GENDER=' "+str(Gen)+" ' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO People(ID,NAME,AGE,GENDER) Values("+str(Id)+",'"+str(Name)+"','"+str(Age)+"','"+str(Gen)+"')"
        cmd2=""
        cmd3=""
    conn.execute(cmd)
    conn.execute(cmd2)
    conn.execute(cmd3)
    conn.commit()
    conn.close()
        
id=input('enter the Id= ')
name=input('enter the Name= ')
age=input('enter the Age= ')
gender=input('enter the Gender(M/F/Other)= ')
info(id,name,age,gender)

while 1:
    ret, img = cap.read()
    cv2.resizeWindow('img', 600,500)
    #cv2.line(img,(600,250),(0,250),(0,255,0),1)
    #cv2.line(img,(300,0),(300,500),(0,255,0),1)
    #cv2.circle(img, (300, 250), 5, (255, 255, 255), -1)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)

    for (x,y,w,h) in faces:
        i=i+1
        print(i)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
        roi_gray  = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        cv2.imwrite("dataSet/face-"+str(id)+'.'+ str(i) + ".jpg", roi_gray)

    cv2.imshow('img',img)
   
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    if i>=30:
        cap.release()
        cv2.destroyAllWindows()
        break
