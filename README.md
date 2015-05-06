# napCAD
NapCAD is an openCV-based image to CAD program that translates JPEG images to STL files.
See more at ctada.github.io/napCAD


//GETTING STARTED

First, ensure the following libraries are installed. 

Auto-installed with Python: 
Tkinter
Numpy
Math
Collections
Stlwriter (comes with repo)

Will need to be installed:
OpenCV
Scipy
Pillow
Matplotlib

To install these libraries, enter the following into command line. NOTE: This assumes a Debian/ Ubuntu operating system.


$ sudo apt-get install python-numpy python-scipy python-matplotlib 
$ sudo pip install Pillow
$ sudo apt-get install python-imaging-tk


A couple things in case you run into issues:

1. If you need to install dependencies for the above libraries (in this example, python-matplotlib), try sudo apt-get build-dep python-matplotlib
2. The following error may show up when running code that contains OpenCV:
$ ValueError: too many values to unpack
If this happens, change the beginning of line 74 in napCAD.py and line 30 in read_box_image.py from “(cnts,_) ” to “_,cnts, _” and the code will run. We believe this is an issue with OpenCV versions, but we're still working on confirming that hypothesis.

Once all the dependencies are installed, clone the repo and run the program:

$ cd your_repo_root
$ git clone https://github.com/ctada/napCAD.git
$ cd napCad
$ python gui_test.py

At this point, the GUI should pop up. Hold up your drawn geometric net to your webcam, and click "Preview 3D Model". The green lines on screen represent the edges that the program "sees" in your drawing. Note that the scale of the 3D render/ preview may be skewed; the coordinate values on the axes should still be accurate, however. After previewing, you can save the 3D render and STL file, or try a new sketch.

