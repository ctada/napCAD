"""Code to take coordinates of each side and fold line and determine the 
plane of the fold line perpendicular to the base. Each side's coordinates are 
transformed onto this plane, and then the program checks for intersecting sides 
to determine whether or not to fold/unfold the sides."""

import numpy as np
import mathfc
import collections

def transform_side(side,theta,actual_fold_lines):
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
	return new_side

def further_transform_check(sides,actual_folds,theta,connections):
	"""Check if sides intersect, and output whether the angles of the side planes need to be changed or not
		Input: all side coordinates, plane equation 
		Output: side coordinates if proper, or neg/pos (for more or less angle) and side coordinates
	"""
	all_sides = {}
	count = 0
	#make list of vectors in each side
	for i in sides:
		#add to dictionary with side as key and vectors as values


		for j in range(1,len(i)):
			new_vector = (i[j][0]-i[j-1][0],i[j][1]-i[j-1][1],i[j][2]-i[j-1][2])
			#vectors.append(new_vector)



	"""for x, left in enumerate(vectors):
		print left
		for y, right in enumerate(vectors):
			common = len(set(left) & set(right))
	        #print left
	print count"""

def main(sides):
	"""call things"""
	theta = 90
	folded_sides = list()
	length = len(sides)
	for i in sides:
		folded_sides.append(transform_side(i,theta,actual_fold_lines))
	#return folded_sides
	return further_transform_check(folded_sides,actual_fold_lines,theta,length)

side_coordinates = (([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[3,0]),([0,0],[0,6],[6,6],[4,0]))
actual_fold_lines = ([0,12],[0,18],[0,18],[6,18],[6,18],[6,12],[6,12],[6,6],[0,6])

print main(side_coordinates)