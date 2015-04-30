# napCAD
NapCAD is an openCV-based image to CAD program that translates JPEG images to STL files.
See more at ctada.github.io/napCAD

//GETTING STARTED
To clone the repo and run the program:

$ cd your_repo_root
$ git clone https://github.com/ctada/napCAD.git
$ cd napCad
$ python gui_test.py

At this point, the GUI should pop up. Hold up your drawn geometric net to your webcam, and click "Preview 3D Model". The green lines on screen represent the edges that the program "sees" in your drawing. Note that the scale of the 3D render/ preview may be skewed; the coordinate values on the axes should still be accurate, however. After previewing, you can save the 3D render and STL file, or try a new sketch.

