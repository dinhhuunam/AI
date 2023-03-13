import cv2
import numpy as np
import sqlite3
import os
from gtts import gTTS
from playsound import playsound
import pyttsx3


# Sử dụng giọng nói
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)

engine.say("Chào bạn!!!Rất vui sử dụng phần mềm của chúng tôi!!!")
engine.runAndWait()
def insertOrUpdate(id,name,age,lop):
    conn = sqlite3.connect('C:\\Users\\Admin\\Project\\data1.db')

    # viết 1 câu lệnh kiểm tra xem id đã tồn tại chưa
    # query = "SELECT * FROM people WHERE ID=" + str(id)
    
    query = "Select * from people where ID=" + str(id)
    
    cusror = conn.execute(query)

    isRecordExist = 0

    for row in cusror:
        isRecordExist = 1

    if (isRecordExist == 0):
        query = "Insert into People(id,name,age,lop) values("+str(id)+",'"+str(name) +"','" +str(age)+"','"+str(lop)+"')"
    else:
        query = "Update People SET Name = '"+str(name)+"', Age= '"+str(age)+"',Lop= '"+str(lop)+"' where ID= " + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()


# load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.XML')
cap = cv2.VideoCapture(0)

# insertOrUpdate(1,"Nam","nam")


# insert to db
engine.say("Mời bạn nhập ID")
engine.runAndWait()
id = input("Enter your ID: ")
engine.say("Mời bạn nhập tên:")
engine.runAndWait()
name = input("Enter your Name: ")
engine.say("Mời bạn nhập tuổi:")
engine.runAndWait()
age = input("Enter your Age: ")
engine.say("Mời bạn nhập lớp:")
engine.runAndWait()
lop = input("Enter your lop: ")
insertOrUpdate(id,name,age,lop);


# 
engine.say("Yêu cầu không che mặt và nhìn thẳng vào camera")
engine.runAndWait()

sampleNum=0
while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Chuyển từ ảnh RGB sang màu sáng

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0),2)
        
        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        # số ảnh lấy tăng dần
        sampleNum +=1
        
        # lưu ảnh đã chụp khuôn mặt vào file dữ liệu
        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y: y+h,x: x+w])
        
    cv2.imshow('frame',frame)
    
    cv2.waitKey(1)
    
    # Thoát ra nếu số lượng ảnh nhiều hơn 100
    if sampleNum > 300:
        break
    
cap.release()
cv2.destroyAllWindows()