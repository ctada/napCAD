import cv2
import numpy as np
import pprint
import plotly.plotly as py
from plotly.graph_objs import *
from normalizer import normalize

# Get image
def find_rectangles(file_path):
	"""
	Description: Finds the 6 main views of a cube in a given image
	Input:
		- file_path - Path to jpeg of drawing
	Returns:
		- sides - List of vertex sets corresponding to the views of the image
	"""
	# Get the image
	image = cv2.imread(file_path)
	image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)

	# Convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Convert the grayscale image to binary
	binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

	# Detect edges with Canny
	edged = cv2.Canny(binary, 30, 200)

	# Find the 10 contours within the edged image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)#[:10]
	rectCnt = None
	count = 0
	vertices = []

	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if contour has four points, classify as rectangle
		if len(approx) == 4:
			rectCnt = approx
			vertices.append(rectCnt)
			cv2.drawContours(image, [rectCnt], -1, (0, 255, 0), 1)
			count += 1

	# Draw the rectangles over the image
	cv2.imshow("Rectangles", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# Find the min/max x and y values
	x = []
	y = []
	for rect in vertices:
		for vert in rect:
			x.append(vert[0][0])
			y.append(vert[0][1])

	minx = min(x)
	miny = min(y)
	maxx = max(x)
	maxy = max(y)
	centery = (maxx + minx)/2
	bottomy = (centery + miny)/2

	# Find the cube sides views using coordinate limits
	cube_right = []
	cube_left = []
	cube_top = []
	cube_back = []
	cube_front = []
	cube_bottom = []

	# Use find_side for extreme sides (right, left, top, back)
	def find_side(direction, xory):
		side = []
		for l in vertices:
			for v in l:
				if v[0][xory] == direction:
					side = l
					break
			else:
				continue
			break
		return side

	# Use find closest for middle sides (front, bottom)
	def find_closest(direction, xory):
		closest = maxy
		sides = []
		for l in vertices:
			for v in l:
				if v[0][xory] < closest:
					closest = v[0][xory]
		side = find_side(closest, 1)
		return side

		closest = myList[0]
		for i in range(1, len(myList)):
			if abs(i - myNumber) < closest:
				closest = i
		return closest	

	cube_right = find_side(maxx, 0)
	cube_left = find_side(minx, 0)
	cube_top = find_side(maxy, 1)
	cube_back = find_side(miny, 1)
	cube_front = find_closest(centery, 1) 
	cube_bottom = find_closest(bottomy, 1)

	return cube_right, cube_left, cube_top, cube_back, cube_front, cube_bottom

	
def normalize_sides(sides):
	"""
	Description: Squares the sides of the rectangles and averages the points
				 so that they fit together
	Input:
		- sides - Six vertex sets representing the sides of a drawing
	Returns:
		- norm_sides - Squared and fit sides list
	"""
	sides_list = []

	# Average side vertices and make perfect rectangles
	def square_sides(sides):
		# Find the min/max x and y values
		x = []
		y = []
		for vert in sides:
			x.append(vert[0][0])
			y.append(vert[0][1])

		minx = 0
		miny = 0
		maxx = max(x)-min(x)
		maxy = max(y)-min(y)

		# Construct new squared vertex set with format |1 2|
		#											   |3 4|
		squared_side = [[minx,miny],[maxx,miny],[maxx,maxy],[minx,maxy]]
		#squared_side = [[minx, maxy], [maxx, maxy], [minx, miny], [maxx, miny]]
		return squared_side

	squared_right = square_sides(sides[0])
	squared_left = square_sides(sides[1])
	squared_top = square_sides(sides[2])
	squared_back = square_sides(sides[3])
	squared_front = square_sides(sides[4])
	squared_bottom = square_sides(sides[5])

	return squared_front,squared_left,squared_back,squared_right,squared_top,squared_bottom

def front_plane(front):
	new_front = [None]*len(front)
	#iterate through list of tuples, add z-dimension
	for i,(x,y) in enumerate(front):
		new_front[i] = (x,y,0)
	return new_front

def left_plane(left_side,start_x):
	left = [None]*len(left_side)
	#iterate through list of tuples, add z-dimension and change x-coordinates
	for i,(x,y) in enumerate(left_side):
		left[i] = (start_x,y,x)
	left_list = [list(k) for k in left]		#list of tuples to list of lists
	#switch coordinates to flip the face
	left_list[0][2],left_list[1][2],left_list[2][2],left_list[3][2] = left_list[1][2],left_list[0][2],left_list[3][2],left_list[2][2]
	new_left = [tuple(j) for j in left_list]	#list of lists to list of tuples
	return new_left

def right_plane(right_side,width):
	new_right = [None]*len(right_side)
	#iterate through list of tuples, add z-dimension and change x-coordinates
	for i,(x,y) in enumerate(right_side):
		new_right[i] = (width,y,x)
	return new_right

def back_plane(back,length):
	back_side = [None]*len(back)
	#iterate through list of tuples, add z-dimension
	for i,(x,y) in enumerate(back):
		back_side[i] = (x,y,length)
	back_list = [list(k) for k in back_side]	#list of tuples to list of lists
	#switch coordinates to flip the face
	back_list[0][0],back_list[1][0],back_list[2][0],back_list[3][0] = back_list[1][0],back_list[0][0],back_list[3][0],back_list[2][0]
	new_back = [tuple(j) for j in back_list]	#list of lists to list of tuples
	return new_back

def top_plane(top,height):
	new_top = [None]*len(top)
	#iterate through list of tuples, add z-dimension and change y-coordinates
	for i,(x,y) in enumerate(top):
		new_top[i] = (x,height,y)
	return new_top

def bottom_plane(bottom,start_y):
	bottom_side = [None]*len(bottom)
	#iterate through list of tuples, add z-dimension and change y-coordinates
	for i,(x,y) in enumerate(bottom):
		bottom_side[i] = (x,start_y,y)
	bottom_list = [list(k) for k in bottom_side]	#list of tuples to list of lists
	#switch coordinates to flip the face
	bottom_list[0][2],bottom_list[2][2],bottom_list[1][2],bottom_list[3][2] = bottom_list[2][2],bottom_list[0][2],bottom_list[3][2],bottom_list[1][2]
	new_bottom = [tuple(j) for j in bottom_list]	#list of lists to list of tuples
	return new_bottom

def make_shape(front,left_side,back,right_side,top,bottom):
	"""This function takes the 2D-coordinates as inputs, 
	calls each respective face function to get the 3D-coordinates, 
	and plots them to ensure that they are correct"""

	front_3D = front_plane(front)
	left_side_3D = left_plane(left_side,front_3D[0][0])
	right_side_3D = right_plane(right_side,front_3D[1][0])
	back_3D = back_plane(back,left_side_3D[0][2])
	top_3D = top_plane(top,front_3D[2][1])
	bottom_3D = bottom_plane(bottom,front_3D[0][1])

	trace1 = Scatter3d(
	    x=[int(i[0]) for i in front_3D],
	    y=[int(j[1]) for j in front_3D],
	    z=[int(k[2]) for k in front_3D],
	    mode='lines+markers',
	)
	trace2 = Scatter3d(
	    x=[int(i[0]) for i in left_side_3D],
	    y=[int(j[1]) for j in left_side_3D],
	    z=[int(k[2]) for k in left_side_3D],
	    mode='lines+markers',
	)
	trace3 = Scatter3d(
	    x=[int(i[0]) for i in right_side_3D],
	    y=[int(j[1]) for j in right_side_3D],
	    z=[int(k[2]) for k in right_side_3D],
	    mode='lines+markers',
	)
	trace4 = Scatter3d(
	    x=[int(i[0]) for i in back_3D],
	    y=[int(j[1]) for j in back_3D],
	    z=[int(k[2]) for k in back_3D],
	    mode='lines+markers',
	)
	trace5 = Scatter3d(
	    x=[int(i[0]) for i in top_3D],
	    y=[int(j[1]) for j in top_3D],
	    z=[int(k[2]) for k in top_3D],
	    mode='lines+markers',
	)
	trace6 = Scatter3d(
	    x=[int(i[0]) for i in bottom_3D],
	    y=[int(j[1]) for j in bottom_3D],
	    z=[int(k[2]) for k in bottom_3D],
	    mode='lines+markers',
	)
	data = Data([trace1,trace2,trace3,trace4,trace5,trace6])
	layout = Layout(
	    margin=Margin(
	        l=0,
	        r=0,
	        b=0,
	        t=0
	    )
	)
	fig = Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='simple-3d-scatter')

	return "front:",front_3D,"left:",left_side_3D,"back:",back_3D,"right:",right_side_3D,"top:",top_3D,"bottom:",bottom_3D

#define each face for testing purposes
sides = find_rectangles("cube.jpg")
# side_lists = normalize_sides(sides)
side_lists = normalize(sides)



front_2D = side_lists[0]
left_side_2D = side_lists[1]
back_2D = side_lists[2]
right_side_2D = side_lists[3]
top_2D = side_lists[4]
bottom_2D = side_lists[5]

#convert coordinates
print make_shape(front_2D,left_side_2D,back_2D,right_side_2D,top_2D,bottom_2D)