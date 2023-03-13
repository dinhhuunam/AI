import cv2
import numpy as np
import sqlite3
import os
from PIL import Image
from gtts import gTTS
from playsound import playsound
import pyttsx3

# Sử dụng giọng nói
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)
engine.say("Nhìn thẳng vào camera và giữ cố định!!!")
engine.runAndWait()

# trainning hinh anh nhanh dien va thu vien nhan dien khuon mat
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.XML')
recognizer = cv2.face_LBPHFaceRecognizer.create()

recognizer.read('/Users/Admin/Project/recognizer/trainningData.yml')

# get profile by id from database
def getProfile(id):

    conn = sqlite3.connect("data1.db")

    query = "SELECT * FROM people WHERE ID=" + str(id)
    cusror = conn.execute(query)
    profile = None
    for row in cusror:
        profile = row

    conn.close()
    return profile

cap = cv2.VideoCapture(0)

fontFace = cv2.FONT_HERSHEY_SIMPLEX

i=0; j=0
while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Chuyển từ ảnh RGB sang màu sáng

    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]

        id, confidence = recognizer.predict(roi_gray)

        if confidence < 40:
            profile = getProfile(id)

            if (profile != None):
                cv2.putText(frame, "Name: "+str(profile[1]), (x+10, y+h+30), fontFace,1, (0, 255, 0), 2)
                cv2.putText(frame, "Age : "+str(profile[2]), (x+10, y+h+60), fontFace,1, (0, 255, 0), 2)
                cv2.putText(frame, "Class : "+str(profile[3]), (x+10, y+h+90), fontFace,1, (0, 255, 0), 2)
                while(i<1):
                    # engine.say("Thông tin sinh viên: ")
                    engine.say("Bạn là sinh viên học viện bưu chính viễn thông ")
                    engine.say(" Lớp: "+ profile[3])
                    engine.say("Thông tin sinh viên hợp lệ!!! Mời bạn vào lớp!!!")
                    engine.runAndWait()
                    i=i+1
                    break
            else:
                cv2.putText(frame, "Unknown", (x+10, y+h+30),fontFace,1, (0, 0, 255), 2)
                while(j<1):
                        engine.say("Chưa nhận dạng được khuôn mặt!!! Bạn chưa được vào lớp!!!")
                        engine.runAndWait()
                        j=j+1
                        break
            
    cv2.imshow('image', frame)
    if (cv2.waitKey(1) == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()