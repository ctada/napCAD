"""Code to take coordinates of each side and fold line and determine the 
plane of the fold line perpendicular to the base. Each side's coordinates are 
transformed onto this plane, and then the program checks for intersecting sides 
to determine whether or not to fold/unfold the sides."""

import numpy as np
import math
import collections

def transform_side(side,theta,actual_fold_lines,pos):
	"""Transform the coordinates of the side onto the perpendicular plane using Euler-Rodrigues formula
		Input: side coordinates, plane
		Output: new coordinates
	"""
	new_side = list()
	#calculating axis of rotation
	axis = side[3][0]-side[0][0],0,0
	#converting theta to radians
	rad = math.radians(theta)
	for i in side: 
		#calculating vector for each point in side
		side_vector = i[0],i[1],0
		#Euler-Rodrigues formula to rotate vectors
		axis = np.asarray(axis)
		theta = np.asarray(rad)
		axis = axis/math.sqrt(np.dot(axis, axis))
		a = math.cos(theta/2)
		b, c, d = -axis*math.sin(theta/2)
		aa, bb, cc, dd = a*a, b*b, c*c, d*d
		bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
		multiplier = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
					[2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
					[2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
		transform_vector = (np.dot(multiplier, side_vector))
		#round points to nearest whole number, add to list of transformed side coordinates
		folded_vector = round(transform_vector[0]),round(transform_vector[1]),round(transform_vector[2])
		new_side.append(folded_vector)
	#replace local coordinate system with image coordinates
	"""final_side = ()
	for i,j in enumerate(new_side):
		if i%2 == :
			 = actual_fold_lines[pos][0]
			 = actual_fold_lines[pos][1]"""
	return new_side

print transform_side(([0,0],[0,6],[6,6],[6,0]),90,([0,18],[6,18]),1)

def further_transform_check(sides,axes,theta,connections):
	"""Check if sides intersect, and output whether the angles of the side planes need to be changed or not
		Input: all side coordinates, plane equation 
		Output: side coordinates if proper, or neg/pos (for more or less angle) and side coordinates
	"""
	temp_sides = list()
	count = 0

	"""while count != connections:
		for i in range(1,len(sides)):
			if sides[i] == sides[i-1]:
				count+=1
			else:
				print i
				count+=1"""
	print count

def main(sides):
	"""call things"""
	theta = 90
	folded_sides = list()
	length = len(sides)
	for i in sides:
		folded_sides.append(transform_side(i,theta,actual_fold_lines,index[i]))
	#return folded_sides
	#return further_transform_check(folded_sides,fold_lines,theta,length)

#side_coordinates = (([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[3,0]),([0,0],[0,6],[6,6],[4,0]))
#actual_fold_lines = ([0,12],[0,18],[0,18],[6,18],[6,18],[6,12],[6,12],[6,6],[0,6])

#print main(side_coordinates)