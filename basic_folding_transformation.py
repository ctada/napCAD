"""Code to take coordinates of each side and fold line and determine the 
plane of the fold line perpendicular to the base. Each side's coordinates are 
transformed onto this plane, and then the program checks for intersecting sides 
to determine whether or not to fold/unfold the sides."""

import numpy as np
import math
import collections

def convert_coordinates(side,fold):
	"""Converts coordinates read through OpenCV into standardized coordinates so that 
		the axis is a vector protruding from the origin"""

def transform_side(side,fold,theta):
	"""Transform the coordinates of the side onto the perpendicular plane using Euler-Rodrigues formula
		Input: side coordinates, plane
		Output: new coordinates
	"""
	new_side = list()
	for i in side: 
		side_vector = i[0]-0,i[1]-0,0
		axis = fold[1][0]- 0,fold[1][1]-0,0
		axis_array = np.asarray(axis)
		theta = np.asarray(math.radians(theta))
		fin_axis = axis_array/math.sqrt(np.dot(axis, axis))
		a = math.cos(theta/2)
		b,c,d = -fin_axis*math.sin(theta/2)
		aa,bb,cc,dd = a*a, b*b, c*c, d*d
		bc,ad,ac,ab,bd,cd = b*c, a*d, a*c, a*b, b*d, c*d
		multiplier = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
						[2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
						[2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
		transform_vector = (np.dot(multiplier, side_vector))
		folded_vector = round(transform_vector[0]),round(transform_vector[1]),round(transform_vector[2])
		new_side.append(folded_vector)
	return new_side

def further_transform_check(sides,axes,theta):
	"""Check if sides intersect, and output whether the angles of the side planes need to be changed or not
		Input: all side coordinates, plane equation 
		Output: side coordinates if proper, or neg/pos (for more or less angle) and side coordinates
	"""
	temp_sides = list()
	for i in range(1,len(sides)):
		if sides[i] == sides[i-1]:
			print 'y'
			temp_sides.append(i)
			temp_sides.append(i-1)
			#sides = transform_side(temp_sides,axes,theta-1)
		else:
			temp_sides.append(i)
			temp_sides.append(i-1)
			#sides = transform_side(temp_sides,axes,theta-1)


def main(sides,fold_lines):
	"""call things"""
	theta = 90
	folded_sides = list()
	for i in sides:
		folded_sides.append(transform_side(i,fold_lines,theta))
	return further_transform_check(folded_sides,fold_lines,theta)

fold_lines = ([0,0],[6,0])
all_sides = (([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]))

print main(all_sides,fold_lines)