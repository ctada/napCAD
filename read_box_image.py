import cv2
import numpy as np
import pprint

# Get image
def find_folds(file_path, outside_points):
	"""
	Description: Finds the 6 main views of a cube in a given image
	Input:
		- file_path - Path to jpeg of drawing
		- outside_points - Number of vertices on the outside contour of the image (passed in form GUI input)
	Returns:
		- outside_contour - outside contour of the drawing
		- fold_lines - fold lines of the drawing
	"""
	# Get the input image
	image = cv2.imread(file_path)
	image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
	newImage = image

	# Convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Convert the grayscale image to binary
	binary = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

	# Detect edges with Canny
	edged = cv2.Canny(binary, 30, 200, apertureSize=3)

	# Find the contours within the edged image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)#[:10]
	rectCnt = None
	vertices = []

	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# Get the largest contour
		if len(approx) == outside_points:
			rectCnt = approx
			vertices.append(rectCnt)
			cv2.drawContours(image, [rectCnt], -1, (0, 255, 0), 1)
			break

	outside = rectCnt

	#Find the inner fold lines
	count = 0
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if contour has four points, classify as rectangle
		if len(approx) == 4:
			rectCnt = approx
			vertices.append(rectCnt)
			cv2.drawContours(image, [rectCnt], -1, (0, 255, 0), 1)
			count += 1

	# Iterate through outside contour to reorganize the data as a list of tuples  (to fit with folding code)
	outside_contour = []
	for item in outside:
		outside_contour.append(tuple(item[0])) 

	print len(outside_contour)
	# Find only the inside points of the contour - this defines fold line points for folding an open topped box
	outside_points = list(outside_contour) # Preventing the original list from being changed

	x = []
	y = []
	for point in outside_points:
		x.append(point[0])
		y.append(point[1])

	# Remove max x values
	maxx1 = max(x)
	x.remove(maxx1)
	maxx2 = max(x)

	# Remove min x values
	minx1 = min(x)
	x.remove(minx1)
	minx2 = min(x)

	# Remove max y values
	maxy1 = max(y)
	y.remove(maxy1)
	maxy2 = max(y)

	# Remove min y values
	miny1 = min(y)
	y.remove(miny1)
	miny2 = min(y)

	def remove_points(minmax, xory):
		side = []
		for point in outside_points:
			if point[xory] == minmax:
				outside_points.remove(point)
				print len(outside_contour)

	remove_points(maxx1, 0)
	remove_points(maxx2, 0)
	remove_points(minx1, 0)
	remove_points(minx2, 0)
	remove_points(maxy1, 1)
	remove_points(maxy2, 1)
	remove_points(miny1, 1)
	remove_points(miny2, 1)

	# Set fold lines
	fold_lines = [[outside_points[0], outside_points[1]],
					[outside_points[1], outside_points[2]],
					[outside_points[2], outside_points[3]],
					[outside_points[3], outside_points[0]]]

	print outside_contour
	print len(outside_contour)
	return outside_contour, fold_lines