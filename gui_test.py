"""
OpenCV portions copied from http://kieleth.blogspot.com/2014/05/webcam-with-opencv-and-tkinter.html
"""

import Tkinter as tk
import tkFileDialog, Tkconstants, tkMessageBox
import cv2
import numpy as np
from PIL import Image, ImageTk  # sudo pip install Pillow, sudo apt-get install python-imaging-tk
import stl_test
from basic_cube import MVP_image_to_3D as mvp
import matplotlib, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

width, height = 800, 600
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

if not cap.isOpened(): 
	cap.open()

root = tk.Tk()
root.title('napCAD')
def handler():
    if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
        root.quit()
root.protocol("WM_DELETE_WINDOW", handler)
root.bind('<Escape>', lambda e: root.quit())

lmain = tk.Label(root)
lmain.pack()

curFrame = None

def processImg():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    curFrame = frame
    cv2.imwrite("napSketch.jpg",curFrame)

    sides = mvp.find_rectangles("basic_cube/cube.jpg")
    side_lists = mvp.normalize_sides(sides)
    perfect_side=[[0,0],[side_lists[0][1][0],0],[side_lists[0][1][0],side_lists[0][1][0]],[0,side_lists[0][1][0]]]

    #convert coordinates
    x,y,z= mvp.output_xyz(perfect_side,perfect_side,perfect_side,perfect_side,perfect_side,perfect_side)
    #triangulate
    stl, fig = stl_test.triangulation(x,y,z)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg( canvas, root )
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect('key_press_event', on_key_event)

    
    #s = tk.Button(master=root, text='Save As', command=save_as(stl)).pack(side=tk.TOP)
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
    #root.quit()
def _quit():
    cap.release()
    cv2.destroyAllWindows()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def handler():
    if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
        root.quit()

def on_key_event(event):
    print('you pressed %s'%event.key)
    key_press_handler(event, canvas, toolbar)

#button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
b = tk.Button(root, text ="Preview 3D Model", command = processImg).pack()
q = tk.Button(master=root, text='Quit', command=_quit).pack(side=tk.BOTTOM)

show_frame()
root.mainloop()

