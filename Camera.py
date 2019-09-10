# -*- coding: utf-8 -*-
"""
Created on Thur Dec 13 21:50:16 2018

@author: rushad
"""

import tkinter as tk
import os
import cv2
from PIL import Image, ImageTk
import numpy
import random

name_elements = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
num_elements = [1,2,3,4,5,6,7,8,9]
OptionList = ["Normal", "Black & White", "Sketchbook"]

if(os.path.isdir('webcam_images') == False):
    os.mkdir('webcam_images')
    os.chdir('webcam_images')
    
else:
    os.chdir('webcam_images')
    
path = os.getcwd()

if (os.path.exists(str(path) + "\\img_data.txt")):
    image_data = open("img_data.txt","r")

    if("--- Image Names ---\n" not in image_data.read()):
        image_data.write("--- Image Names ---\n")
        image_data.close()
else:
    image_data = open("img_data.txt","a")
    image_data.write("--- Image Names ---\n")
    image_data.close()

cancel = False

cap = cv2.VideoCapture(0)

def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    button1 = tk.Button(mainWindow, text="Save Image!", command=saveAndExit)
    button2 = tk.Button(mainWindow, text="Take new image", command=resume)
    button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button1.focus()

def saveAndExit(event = 0):
    global prevImg, img_name
    img_no = 1

    image_data = open("img_data.txt","r")
    img_name = str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(img_no) + ".png"

    if(img_name in image_data.read()):
        img_name = str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(random.choice(name_elements)) + str(img_no + random.choice(num_elements)) + ".png"
        image_data.close()
        
    image_data = open("img_data.txt","a")
    image_data.write(img_name + "\n")
    image_data.close()
    
    prevImg.save(img_name)
    
    img_no = img_no + 1
    callback()
    mainWindow.quit()


def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    lmain.after(10, show_frame)

mainWindow = tk.Tk(screenName="Camera")
mainWindow.resizable(width=True, height=True)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button = tk.Button(mainWindow, text="Capture", command=prompt_ok)
variable = tk.StringVar(mainWindow)
variable.set(OptionList[0])
w = tk.OptionMenu(mainWindow, variable, *OptionList)
w.pack()

labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
labelTest.pack(side="top")

def callback(*args):
    global cv2_image, img_name
    _,frame = cap.read()
    
    if variable.get() == "Black & White":
        temp_img = cv2.imread(img_name)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(img_name, temp_img)

    elif variable.get() == "Sketchbook":
        temp_img = cv2.imread(img_name)
        img_gray = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        img_gray_blur = cv2.bilateralFilter(img_gray,9,75,75)
        canny_edges = cv2.Canny(img_gray_blur, 0, 15)
        _, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
        
        cv2.imwrite(img_name, mask)
        
    elif variable.get() == "Normal":
        pass
    
lmain.pack()
button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
button.focus()

def show_frame():
    global cancel, prevImg, button, cv2_image

    _,frame = cap.read()
    frame = cv2.flip(frame,1)
    
    if variable.get() == "Normal":
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
    elif variable.get() == "Black & White":
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    elif variable.get() == "Sketchbook":
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_gray_blur = cv2.bilateralFilter(img_gray,9,75,75)
        canny_edges = cv2.Canny(img_gray_blur, 0, 15)
        _, cv2_image = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)

    prevImg = Image.fromarray(cv2_image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()
