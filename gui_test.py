"""
OpenCV portions copied from http://kieleth.blogspot.com/2014/05/webcam-with-opencv-and-tkinter.html
"""

import Tkinter as tk
import tkFileDialog, Tkconstants
import cv2
import numpy as np
from PIL import Image, ImageTk  # sudo pip install Pillow, sudo apt-get install python-imaging-tk
import stl_test
 
width, height = 800, 600
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

if not cap.isOpened(): 
	cap.open()

root = tk.Tk()

#root.bind('<escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

curFrame = None


def callback():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    curFrame = frame
    cv2.imwrite("napSketch.jpg",curFrame)
    print "Photo Taken"
    #get calculated point things
    x = [0,0,0.5,1,1]
    y = [0,1,0.5,0,1]
    z = [0,0,1,0,0]
    #triangulate
    stl = stl_test.triangulation(x,y,z)
    #stl_test.tri_vis(x,y,z)
    save_as(stl) #save STL instead of text

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    curFrame = cv2image
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def save_as(content):
   #contents = self.textbox.get(1.0,"end-1c")  # given root frame, stores the contents of the text widget in a str, CHANGE TO STL OUTPUT FROM PROGRAM
    f = tkFileDialog.asksaveasfilename(   #this will make the file path a string
        parent= root,
        defaultextension=".stl",                 #so it's easier to check if it exists
        filetypes = (("napCAD STL", "*.stl"),("testText", ".txt")), 
        title="Save STL as...")    #in the save function
    stl_test.stl_write(f,content)

#button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
b = tk.Button(root, text ="Convert to STL", command = callback).pack()

show_frame()
root.mainloop()
