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

engine.say("Bắt đầu train data")
engine.runAndWait()

recognizer = cv2.face_LBPHFaceRecognizer.create()

path = 'dataSet'

# lấy dữ liệu từ SQL theo ID
def getImageWithId(path):
    
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)
    
    faces=[]
    IDs=[]
    
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        
        faceNp = np.array(faceImg, 'uint8')
        print(faceNp)
        
        Id = int(imagePath.split('.')[1])
        
        faces.append(faceNp)
        IDs.append(Id)
        
        cv2.imshow('trainning',faceNp)
        cv2.waitKey(10)
        
    return faces,IDs

faces ,Ids=getImageWithId(path)

recognizer.train(faces ,np.array(Ids))

if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainningData.yml')

cv2.destroyAllWindows()