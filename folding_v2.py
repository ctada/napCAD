"""Shivali Chandra
Restructured code that takes coordinates of sides and axes of rotation, and rotates the sides 
until they meet, forming a closed 3D shape.
"""

import numpy as np
import math
import collections

def find_intersection_distances(p1,y1,x1,y2,x2):
	if y2-y1 == 0:
		dist = math.fabs(p1[1]-y1)
	elif x2-x1 == 0:
		dist = math.fabs(p1[0]-x1)
	else:
		axis_line_slope = (y2-y1)/(x2-x1)
		perp_slope = -1/(axis_line_slope)
		c1 = axis_line_slope * x1 - y1
		c2 = perp_slope * p1[0] - p1[1]
		x_intersect = (c2 - c1)/(perp_slope - axis_line_slope)
		y_intersect = perp_slope * x_intersect + c2
		dist = math.sqrt((x_intersect-p1[0])**2+(y_intersect-p1[1])**2)
	hypotenuse = math.sqrt((x2-p1[0])**2+(y2-p1[1])**2)
	if hypotenuse == 0:
		angle = 0.0
	else:
		angle = math.asin(dist/hypotenuse)
	return dist,angle

def move_to_actual_coord(old_side,side_dict,side_num,theta):
	"""Change the xy coordinates of the sides to the correct values from the original image
		Input: side coordinates, sides dictionary
		Output: new side coordinates in the sides dictionary	
	"""
	final_side = list()
	y1 = old_side[0][1]
	x1 = old_side[0][0]
	y2 = old_side[len(old_side)-1][1]
	x2 = old_side[len(old_side)-1][0]
	new_xaxis = side_dict[side_num][1][len(old_side)-1][0]
	new_xaxis1 = side_dict[side_num][1][0][0]
	new_yaxis = side_dict[side_num][1][len(old_side)-1][1]
	new_yaxis1 = side_dict[side_num][1][0][1]

	for i,j in enumerate(old_side):
		x = side_dict[side_num][1][i][0]
		y = side_dict[side_num][1][i][1]
		intersections = find_intersection_distances((j[0],j[1]),y1,x1,y2,x2)
		dist = intersections[0]
		coordinates = {1:(x,(dist+new_yaxis)),2:(x,(new_yaxis-dist)),3:((new_xaxis-dist),y),4:((new_xaxis+dist),y)}
		intersections = find_intersection_distances((j[0],j[1]),y1,x1,y2,x2)
		if (new_xaxis>new_xaxis1) and (new_yaxis-new_yaxis1==0):
			[fin_x,fin_y] = coordinates[1]
		elif (new_xaxis<new_xaxis1) and (new_yaxis-new_yaxis1==0):
			[fin_x,fin_y] = coordinates[2]
		elif (new_yaxis>new_yaxis1) and (new_xaxis-new_xaxis1==0):
			[fin_x,fin_y] = coordinates[3]
		else:
			[fin_x,fin_y] = coordinates[4]
		"""else:	
			hyp = intersections[0]/math.sin(intersections[1])"""
		
		z = j[2]

		final_coord = fin_x/1.0,fin_y/1.0,z
		final_coord = list(final_coord)
		final_side.append(final_coord)
	side_dict[side_num] = list(side_dict[side_num])
	side_dict[side_num].append(final_side)
	return side_dict

def transform_side(side,theta,side_dict,side_num):
	"""Transform the coordinates of the side onto the perpendicular plane using Euler-Rodrigues formula
		Input: side coordinates, plane
		Output: new coordinates
	"""
	new_side = list()
	#calculating axis of rotation
	axis = side[len(side)-1][0]-side[0][0],0.0,0.0
	#converting theta to radians
	rad = math.radians(theta)
	for i in side: 
		#calculating vector for each point in side
		side_vector = i[0],i[1],0.0
		#Euler-Rodrigues formula to rotate vectors
		axis = np.asarray(axis)
		theta = np.asarray(rad)
		axis = axis/math.sqrt(np.dot(axis, axis))
		a = math.cos(theta/2.0)
		b, c, d = -axis*math.sin(theta/2.0)
		aa, bb, cc, dd = a*a, b*b, c*c, d*d
		bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
		multiplier = np.array([[aa+bb-cc-dd, 2.0*(bc+ad), 2.0*(bd-ac)],
					[2.0*(bc-ad), aa+cc-bb-dd, 2.0*(cd+ab)],
					[2.0*(bd+ac), 2.0*(cd-ab), aa+dd-bb-cc]])
		transform_vector = (np.dot(multiplier, side_vector))
		#round points to nearest whole number, add to list of transformed side coordinates
		folded_vector = round(transform_vector[0]),round(transform_vector[1]),round(transform_vector[2])
		new_side.append(folded_vector)

	moved_side = move_to_actual_coord(new_side,side_dict,side_num,theta)
	return moved_side

def check_sides(run,theta):
	vector_sides = {}
	data = []
	for i in run: 
		position = run[i][2]
		for j in range(1,len(position)):
			if (position[j][0]>position[j-1][0]) or (position[j][1]>position[j-1][1]) or (position[j][2]>position[j-1][2]):
				key = str(position[j])+str(position[j-1])
			else:
				key = str(position[j-1])+str(position[j])
			if key in vector_sides:
				vector_sides[key].append(i)
			else: 
				vector_sides[key] = [i]
	for k in vector_sides:
		if len(vector_sides[k])>1:
			data.append(vector_sides[k][0])
			data.append(vector_sides[k][1])
	print list(set(run.keys())-set(data))
	#return vector_sides


def make_dictionaries(sides,xy_coord):
	#create dictionary of sides as keys, both sets of xy coordinates as values
	theta = 90
	sides_old_coordinates = {}
	for i in range(0,len(sides)):
		val1 = sides[i]
		val2 = xy_coord[i]
		if i not in sides_old_coordinates:
			sides_old_coordinates[i] = val1,val2
	run_fxn = main(sides_old_coordinates,theta)
	return check_sides(run_fxn,theta)
	

def main(sides,theta):
	"""call things"""
	length = len(sides)
	for i in sides:
		side = sides[i][0]
		transformed_side = transform_side(side,theta,sides,i)
	return transformed_side

side_coordinates = (([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]))
actual_coordinates = (([6,6],[0,6],[0,12],[6,12]),([6,12],[6,18],[12,18],[12,12]),([12,12],[18,12],[18,6],[12,6]),([12,6],[12,0],[6,0],[6,6]))

print make_dictionaries(side_coordinates,actual_coordinates)