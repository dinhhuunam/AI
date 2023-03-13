import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import sqlite3
import os
from PIL import Image
from gtts import gTTS
from playsound import playsound
import pyttsx3

# Sử dụng giọng nói. trợ lý ảo
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)

# hàm nhận diện khuôn mặt
def RecognitionData():
    engine.say("Nhìn thẳng vào camera và giữ cố định!!!")
    engine.runAndWait()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.XML')
    #recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read("trainningData.yml")

    def getProfile(id):
        conn = sqlite3.connect("data1.db")
        query = "SELECT * FROM people WHERE ID=" + str(id)
        cusror = conn.execute(query)
        profile = None
        for row in cusror:
            profile = row
        conn.close()
        return profile
    # Khởi tạo camera của máy tính
    cap = cv2.VideoCapture(0)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    i=0; j=0
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Chuyển từ ảnh RGB sang màu sáng
        faces = face_cascade.detectMultiScale(gray)
        # Cần vẽ được hình vuông bao quanh khuôn mặt
        for (x, y, w, h) in faces:
            # hàm rectangle để vẽ hình vuông
            # Điểm (x,y) là toạ độ điểm ban đầu
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225,0), 2)
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
                    cv2.putText(frame, "Unknown", (x+10, y+h+30),fontFace,1, (0, 255, 0), 2)
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


# hàm train để train dữ liệu ảnh
def TrainData():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    path = 'dataSet'
    def getImagesWithID(path):
        imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
        faces=[]
        IDs=[]
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            Id = int(imagePath.split('.')[1])
            faces.append(faceNp)
            IDs.append(Id)
            cv2.imshow('training', faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    # Ta sẽ có 1 hàm train. Ta truyền vào hai tham số faces và Ids
    recognizer.train(faces ,np.array(Ids))

    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')
    # Sau khi train xong sẽ tạo ra 1 file đuôi yml để lưu dữ liệu sau khi đã train
    recognizer.save('recognizer/trainningData.yml')
    cv2.destroyAllWindows()


# lấy dữ liệu ảnh từ webcam và thêm thông tin vào database
def getData2():
    engine.say("Chào bạn!!!Rất vui sử dụng phần mềm của chúng tôi!!!")
    engine.runAndWait()
    def insertOrUpdate(id,name,age,lop):   
        # truy cập đến đường dẫn trong sqlite3
        conn = sqlite3.connect('C:\\Users\\Admin\\Project\\data1.db')
        # viết 1 câu lệnh kiểm tra xem id đã tồn tại chưa
        query = "Select * from people where ID=" + str(id)
        # truy cập vào các query
        cusror = conn.execute(query)
    # biến isRecordExist để kiểm tra xem id đã tồn tại chưa
    # chưa tồn tại sẽ gán bằng 0
    # tồn tại rồi gán bằng 1
        isRecordExist = 0
    # duyệt từng hàng trên bản ghi
        for row in cusror: 
            isRecordExist = 1
        if (isRecordExist == 0):
            query = "Insert into People(id,name,age,lop) values("+str(id)+",'"+str(name) +"','" +str(age)+"','"+str(lop)+"')"
        else:
            query = "Update People SET Name = '"+str(name)+"', Age= '"+str(age)+"',Lop= '"+str(lop)+"' where ID= " + str(id)
        conn.execute(query)
        conn.commit()
        conn.close()
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.XML')
    # hàm trong opencv để truy cập vào webcam máy tính
    cap = cv2.VideoCapture(0) 
    # Người dùng nhập dữ liệu từ bàn phím 
    id = int1.get()
    name ="'"+str1.get()+"'"
    age ="'"+str2.get()+"'"
    lop ="'"+str3.get()+"'"
    # truyền vào 4 tham số lưu vào database
    insertOrUpdate(id,name,age,lop)
    engine.say("Yêu cầu không che mặt và nhìn thẳng vào camera")
    engine.runAndWait()
    sampleNum=0
    # nhận diện khuôn mặt từ webcam và lưu vào database
    while True:
        ret, frame= cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            sampleNum += 1

            if not os.path.exists('dataSet'):
                os.makedirs('dataSet')
                
            cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y: y+h,x: x+w])            
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('frame',frame)
        cv2.waitKey(1)
        
        if(sampleNum>300):
            cap.release()
            cv2.destroyAllWindows()
            break
        
    edit_id.delete(0,"end")
    edit_name.delete(0,"end")
    edit_age.delete(0,"end")
    edit_lop.delete(0,"end")
    
    
# Giao diện
win = tk.Tk()
win.title("He thong nhan dien khuon mat")
win.geometry('500x400')
win.configure(bg='#263D42')

label = ttk.Label(win,text="Hệ Thống Nhận Diện Khuôn Mặt",background="grey",foreground="white",font=20)
label.grid(column =1, row =0)
label.place(x=100)

label1 = ttk.Label(win,text="Id:",background="#263D42",foreground="white")  
label1.grid(column =0, row =2)
label1.place(y=80)

label2 = ttk.Label(win,text="Name:",background="#263D42",foreground="white")
label2.grid(column =0, row =3)
label2.place(y=120)

label3 = ttk.Label(win,text="Age:",background="#263D42",foreground="white")
label3.grid(column =0, row =4)
label3.place(y=160)

label4 = ttk.Label(win,text="Lop:",background="#263D42",foreground="white")
label4.grid(column =0, row =5)
label4.place(y=200)

int1 =tk.IntVar()
edit_id=ttk.Entry(win,textvariable=int1, width=50)
edit_id.grid(column =1, row =2)
edit_id.focus()
edit_id.place(x=90,y=80)

str1 =tk.StringVar()
edit_name=ttk.Entry(win,textvariable=str1,width=50)
edit_name.grid(column =1, row =3)
edit_name.place(x=90,y=120)

str2 =tk.StringVar()
edit_age=ttk.Entry(win,textvariable=str2,width=50)
edit_age.grid(column =1, row =4)
edit_age.place(x=90,y=160)

str3 =tk.StringVar()
edit_lop=ttk.Entry(win,textvariable=str3,width=50)
edit_lop.grid(column =1, row =5)
edit_lop.place(x=90,y=200)


btlaydulieu= ttk.Button(win, text ="Lấy Dữ Liệu", command=getData2)
btlaydulieu.grid(column =0, row =8)
#btlaydulieu.place()
bttrain= ttk.Button(win, text ="Training", command=TrainData)
bttrain.grid(column =1, row =8)
btnhandien= ttk.Button(win, text ="Nhận Diện", command=RecognitionData)
btnhandien.grid(column =2, row =8)  
bttrain.place(x=200,y=250)
btnhandien.place(x=350,y=250)
btlaydulieu.place(x=50,y=250)

win.mainloop()