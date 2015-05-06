"""
OpenCV portions based off of http://kieleth.blogspot.com/2014/05/webcam-with-opencv-and-tkinter.html
"""

import Tkinter as tk
import tkFileDialog, Tkconstants, tkMessageBox
import cv2
import numpy as np
from PIL import Image, ImageTk  # sudo pip install Pillow, sudo apt-get install python-imaging-tk
#from basic_cube import MVP_image_to_3D as mvp
import read_box_image as rImg
import stl
import folding_v3 as fold
import face_finder as ff
import matplotlib, sys
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def processImg():
    """
    Captures image of sketch and processes paths, folds shape, and creates STL. Renders interactive 3D plot of figure and adds button option to save the STL file. 
    """
    width, height = 300, 200 #sets new dimensions of video feed to make room for 3D render on screen
    cap.set(3, width) #3 references cv2.CV_CAP_PROP_FRAME_WIDTH, from http://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
    cap.set(4, height) #4 references cv2.CV_CAP_PROP_FRAME_HEIGHT

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    curFrame = frame
    cv2.imwrite("napSketch.jpg",curFrame) #captures sketch in frame

    d= VertexDialog(root) #asks for number of vertices in final form
    root.wait_window(d.top)
    vertNum = d.getNum() 
    sides = rImg.find_folds("napSketch.jpg", int(vertNum))
    #sides= rImg.find_folds("fold_box.jpg",12)

    # faces=ff.face_finder([(1,0),(2,0),(2,1),(3,1),(3,2),(2,2),(2,3),(1,3),(1,2),(0,2),(0,1),(1,1)],[[(1,1),(2,1)],[(2,1),(2,2)],[(2,2),(1,2)],[(1,2),(1,1)]])
    faces=ff.face_finder(sides[0], sides[1])
    # faces=ff.face_finder([(364, 278), (200, 305), (205, 467), (47, 488), (40, 665), (205, 645),(209, 793), (382, 791), (381, 633), (555, 616), (557, 439), (378, 451)],[[(205, 467), (205, 645)], [(205, 645), (381, 633)], [(381, 633), (378,451)], [(378, 451), (205, 467)]])
    x, y, z=fold.main(faces[0],faces[1])
    to_stl, triangles = stl.triangulation(x,y,z) #triangulates 3D points

    fig = plt.figure() #creates figure 
    #based off of http://matplotlib.org/examples/user_interfaces/embedding_in_tk.html
    canvas = FigureCanvasTkAgg(fig, master=root) #creates canvas with figure
    ax = fig.add_subplot(1, 1, 1, projection='3d') # sets plot to be 3D
    ax.plot_trisurf(x, y, z, triangles=triangles, cmap=plt.cm.Spectral) #plots triangulated points in 3D, tri.simplices references the faces of the triangles
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect('key_press_event', key_press_handler) #event handling for plot
    toolbar = NavigationToolbar2TkAgg( canvas, root ) #creates toolbar for navigating plot
    toolbar.update()
    canvas.show() 
    
    saveButton = tk.Button(master=root, text='Save As', command=lambda:save_as(to_stl)).pack(side=tk.TOP, expand=1) #when clicked, open save dialog for STL file
    
def show_frame():
    """
    Shows video feed with pathfinding feedback so that user knows when to capture image of sketch for processing
    """
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
    binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1] # Convert the grayscale image to binary
    edged = cv2.Canny(binary, 30, 200) # Detect edges with Canny

    # Find the 10 contours within the edged image
    #__,cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (cnts,_) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)#[:10]
    rectCnt = None
    count = 0
    vertices = []
    drawn = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if contour has four points, draw on the contour
        if len(approx) == 4:
            rectCnt = approx
            vertices.append(rectCnt)
            cv2.drawContours(frame, [rectCnt], -1, (0, 255, 0), 1)
            count += 1

    img = Image.fromarray(frame)     #get new Image, now with contours drawn on
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def save_as(content):
    """
    Writes triangulated faces of object to STL file
    input: numpy array of triangulated faces
    output: None (writes to file)
    """
    f = tkFileDialog.asksaveasfilename(   #this will make the file path a string
        parent= root,
        defaultextension=".stl",                
        filetypes = (("napCAD STL", "*.stl"),("testText", ".txt")), 
        title="Save STL as...")    #in the save function
    stl.stl_write(f,content)

def _quit():
    """
    Safely exits program, closing webcam and GUI. 
    """
    cap.release()
    cv2.destroyAllWindows()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def handler():
    """
    Confirms quit when user closes out of window
    """
    if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
        root.quit()


class VertexDialog:
    """
    Custom dialog box to ask for number of vertices in drawn sketch (geometric net)
    Based off of http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    """
    def __init__(self, parent):
        """
        Creates and opens new dialog window, asking for number of expected vertices in the sketch
        """
        self.inputVertNum = 0
        top = self.top = tk.Toplevel(parent)
        tk.Label(top, text="Photo Taken! \n Please enter the number of vertices in the sketch.").pack()
        self.e = tk.Entry(top)
        self.e.pack(padx=5)

        b = tk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        """
        Reads in input to window, closes window
        """
        self.inputVertNum= self.e.get()
        self.top.destroy()

    def getNum(self):
        """
        Returns expected number of vertices in sketch, as entered into the dialog window
        """
        return self.inputVertNum

cap = cv2.VideoCapture(0) #starts recording 

if not cap.isOpened(): 
    cap.open() #turns on camera

root = tk.Tk()
root.title('napCAD')

root.protocol("WM_DELETE_WINDOW", handler) #if window is closed or the Esc key is pressed, confirm quit and exit program
root.bind('<Escape>', lambda e: root.quit())

lmain = tk.Label(root)
lmain.pack()

curFrame = None

b = tk.Button(root, text ="Preview 3D Model", command = processImg).pack() #triggers processing of sketch
q = tk.Button(master=root, text='Quit', command=_quit).pack(side=tk.BOTTOM) #exits program if pressed 

show_frame()
root.mainloop()


