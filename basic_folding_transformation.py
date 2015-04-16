"""Code to take coordinates of each side and fold line and determine the 
plane of the fold line perpendicular to the base. Each side's coordinates are 
transformed onto this plane, and then the program checks for intersecting sides 
to determine whether or not to fold/unfold the sides."""

import numpy as np
import math

def find_perp_plane(fold_coordinates):
	"""find the plane the fold line is in that is perpendicular to the base side
		Input: side coordinates, fold line equation, base plane
		Output: plane equation? 
	"""
	#return 0,fold_coordinates[1][0]-fold_coordinates[0][0],0
	return fold_coordinates[1][0]- 0,fold_coordinates[1][1]-0,0

def transform_side(side,fold,theta):
	"""Transform the coordinates of the side onto the perpendicular plane using Euler-Rodrigues formula
		Input: side coordinates, plane
		Output: new coordinates
	"""
	new_side = list()
	for i in side: 
		side_vector = i[0]-0,i[1]-0,0
		axis = np.asarray(find_perp_plane(fold))
		theta = np.asarray(theta)
		axis = axis/math.sqrt(np.dot(axis, axis))
		a = math.cos(theta/2)
		b,c,d = -axis*math.sin(theta/2)
		aa,bb,cc,dd = a*a, b*b, c*c, d*d
		bc,ad,ac,ab,bd,cd = b*c, a*d, a*c, a*b, b*d, c*d
		multiplier = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
						[2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
						[2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
		transform_vector = (np.dot(multiplier, side_vector))
		folded_vector = round(transform_vector[0]),round(transform_vector[1]),round(transform_vector[2])
		new_side.append(folded_vector)
	return new_side

def further_transform_check():
	"""Check if sides intersect, and output whether the angles of the side planes need to be changed or not
		Input: all side coordinates, plane equation 
		Output: side coordinates if proper, or neg/pos (for more or less angle) and side coordinates
	"""

def main():
	"""call things"""

fold_lines = ([0,0],[6,0])
theta = math.radians(90)
side = ([0,0],[0,6],[6,6],[6,0])

print transform_side(side,fold_lines,theta)