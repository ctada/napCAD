"""
Author: Kathryn Hite
Updated: 3/30/15
Description: Input a drawing and find and classify the rectangles within it.
"""

import cv2
import numpy as np
import pprint

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
	_,cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

	return "front:",squared_front,"left:",squared_left,"back:",squared_back,"right:",squared_right,"top:",squared_top,"bottom:",squared_bottom

	#return squared_right, squared_left, squared_top, squared_back, squared_front, squared_bottom

sides = find_rectangles("cube.jpg")
print normalize_sides(sides)