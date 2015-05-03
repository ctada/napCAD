from face_finder import face_finder
from folding_v2 import main


def napCAD_main():
	testshapeSquare=[(1,0),(2,0),(2,1),(3,1),(3,2),(2,2),(2,3),(1,3),(1,2),(0,2),(0,1),(1,1)]
	foldlinesSquare=[[(1,1),(2,1)],[(2,1),(2,2)],[(2,2),(1,2)],[(1,2),(1,1)]]

	testshapeRect= [(2,0),(3,0),(3,2),(5,2),(5,3),(3,3),(3,5),(2,5),(2,3),(0,3),(0,2),(2,2)]
	foldlinesRect=[[(2,2),(3,2)],[(3,2),(3,3)],[(3,3),(2,3)],[(2,3),(2,2)]]

	# testshapePyramid=

	#faces=face_finder(testshapeRect,foldlinesRect)
	faces=face_finder(testshapeSquare, foldlinesSquare)
	shape3D=main(faces[0],faces[1])
	print 'napCAD_main just ran!'
	return shape3D
