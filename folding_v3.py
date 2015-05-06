"""Shivali Chandra
Restructured code that takes coordinates of sides and axes of rotation, and rotates the sides 
until they meet, forming a closed 3D shape. As of 5/3/15 can fold cubes, square pyramids, and 
other prisms with square bases.
"""

import numpy as np
import math
import collections

def find_intersection_distances(p1,y1,x1,y2,x2):
	#checks if axis is horizontal or vertical
	if y2-y1 == 0:
		dist = math.fabs(p1[1]-y1)
	elif x2-x1 == 0:
		dist = math.fabs(p1[0]-x1)
	else:
		#not used as of now, calculating new distance based off of diagonal axis
		axis_line_slope = (y2-y1)/(x2-x1)
		perp_slope = -1/(axis_line_slope)
		c1 = axis_line_slope * x1 - y1
		c2 = perp_slope * p1[0] - p1[1]
		x_intersect = (c2 - c1)/(perp_slope - axis_line_slope)
		y_intersect = perp_slope * x_intersect + c2
		dist = math.sqrt((x_intersect-p1[0])**2+(y_intersect-p1[1])**2)
	hypotenuse = math.sqrt((x2-p1[0])**2+(y2-p1[1])**2)
	return dist

def move_to_actual_coord(old_side,side_dict,side_num,theta):
	"""Change the xy coordinates of the sides to the correct values from the original image
		Input: side coordinates, sides dictionary
		Output: new side coordinates in the sides dictionary	
	"""
	final_side = list()
	#y1,x1,y2,x2 are coordinates of axis normalized to zero
	y1 = old_side[0][1]
	x1 = old_side[0][0]
	y2 = old_side[len(old_side)-1][1]
	x2 = old_side[len(old_side)-1][0]

	#variables are coordinates of actual axis
	new_xaxis = side_dict[side_num][1][len(old_side)-1][0]
	new_xaxis1 = side_dict[side_num][1][0][0]
	new_yaxis = side_dict[side_num][1][len(old_side)-1][1]
	new_yaxis1 = side_dict[side_num][1][0][1]

	#iterate through each point of a side
	for i,j in enumerate(old_side):
		x = side_dict[side_num][1][i][0]
		y = side_dict[side_num][1][i][1]
		intersections = find_intersection_distances((j[0],j[1]),y1,x1,y2,x2)
		dist = intersections
		coordinates = {1:(x,(dist+new_yaxis)),2:(x,(new_yaxis-dist)),3:((new_xaxis-dist),y),4:((new_xaxis+dist),y)}
		intersections = find_intersection_distances((j[0],j[1]),y1,x1,y2,x2)
		#check which direction the fold needs to be (inwards or outwards) depending on axis orientation
		if (new_xaxis>new_xaxis1) and (new_yaxis-new_yaxis1==0):
			if (math.degrees(theta) <= 90):
				if (new_yaxis<0):
					[fin_x,fin_y] = coordinates[1]
				else: 
					[fin_x,fin_y] = coordinates[2]
			else:
				if (new_yaxis<0):
					[fin_x,fin_y] = coordinates[2]
				else: 
					[fin_x,fin_y] = coordinates[1]
		elif (new_xaxis<new_xaxis1) and (new_yaxis-new_yaxis1==0):
			if math.degrees(theta) <= 90: 
				if (new_yaxis<0):
					[fin_x,fin_y] = coordinates[2]
				else: 
					[fin_x,fin_y] = coordinates[1]
			else:
				if (new_yaxis<0):
					[fin_x,fin_y] = coordinates[1]
				else: 
					[fin_x,fin_y] = coordinates[2]
		elif (new_yaxis>new_yaxis1) and (new_xaxis-new_xaxis1==0):
			if math.degrees(theta) <= 90:
				if (new_xaxis<0):
					[fin_x,fin_y] = coordinates[3]
				else: 
					[fin_x,fin_y] = coordinates[4]
			else:
				if (new_xaxis<0):
					[fin_x,fin_y] = coordinates[4]
				else: 
					[fin_x,fin_y] = coordinates[3]
		else:
			if math.degrees(theta) <=90:
				if (new_xaxis<0):
					[fin_x,fin_y] = coordinates[4]
				else: 
					[fin_x,fin_y] = coordinates[3]
			else:
				if (new_xaxis<0):
					[fin_x,fin_y] = coordinates[3]
				else: 
					[fin_x,fin_y] = coordinates[4]

		z = j[2]

		#add coordinates to final_side
		final_coord = fin_x/1.0,fin_y/1.0,z
		final_coord = list(final_coord)
		final_side.append(final_coord)

	#add final_side to dictionary of sides
	side_dict[side_num] = list(side_dict[side_num])
	side_dict[side_num].append(final_side)
	return side_dict

def transform_side(side_num,side_dict,theta):
	"""Transform the coordinates of the side onto the perpendicular plane using Euler-Rodrigues formula
		Input: side coordinates, sides dictionary, theta
		Output: new coordinates
	"""
	side = side_dict[side_num][0]
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
	#call function to translate the x,y coordinates with relation to the actual side coordinates
	moved_side = move_to_actual_coord(new_side,side_dict,side_num,theta)
	return moved_side

def output(theta,final_list):
	"""Function takes each point and returns the x,y,z coordinates in three lists.
		Input: theta (for testing), final sides dictionary
		Output: three lists of x,y,z
	"""
	#create 3 empty lists for the x,y,z coordinate values
	x = list()
	y = list()
	z = list()
	final_coordinates = []

	#iterate through dictionary to add the side coordinates to a list
	for i in final_list:
		final_coordinates.append(final_list[i][2]) 

	#iterate through coordinate list to create three lists of x,y, and z respectively
	for i in final_coordinates:
		for j in i: 
			x.append(j[0])
			y.append(j[1])
			z.append(j[2])
	return x,y,z

def check_sides(run,temp,theta,fin):
	"""Recursive function takes in each side and continuously checks for sides to meet up
		Input: sides that are being folded, temporary dict with sides to check against, theta, 
		full list of sides_old_coordinates
		Output: final theta, dictionary of final sides
	"""
	#create list and dictionaries for storing points
	vector_sides = temp
	data = []
	redo_sides = {}
	new_run = {}

	#iterate through dictionary of the sides still being folded
	for i in run: 
		position = run[i][2]
		#create keys of the sets of two points that define each line in a side
		for j in range(1,len(position)):
			if ((position[j][0]==position[j-1][0]) or (position[j][1]==position[j-1][1])):
				key = str(position[j][0])+str(position[j][1])+str(position[j-1][0])+str(position[j-1][1])
			elif ((position[j][0]>position[j-1][0]) or (position[j][1]>position[j-1][1])):
				key = str(position[j][0])+str(position[j][1])+str(position[j-1][0])+str(position[j-1][1])
			else:
				key = str(position[j-1][0])+str(position[j-1][1])+str(position[j][0])+str(position[j][1])
			#add keys, side numbers as values to a dictionary
			if key in vector_sides:
				vector_sides[key].append(i)
			else: 
				vector_sides[key] = [i]	
	for k in vector_sides:
		#if a key has more than one value, two sides have folded to meet up
		if len(vector_sides[k])>1:
			data.append(vector_sides[k][0])
			data.append(vector_sides[k][1])
	#check to see if all the sides have met another side, new_side_list returns those that have not
	new_side_list = list(set(run.keys())-set(data))
	#if there are no sides left to fold, return the final list of coordinates
	if not new_side_list:
		return theta,run
	else:
		#if there are, add to theta to have the side fold again
		new_t = theta+1

		#create a new dictionary with only the sides that need to be folded
		for i in run.keys():
			if i in new_side_list:
				redo_sides[i] = [run[i][0]]
				redo_sides[i].append(run[i][1])
			else:
				#create a temp dictionary of sides that don't need to be folded (to compare coordinates with)
				new_run[i] = run[i]
			#call function to fold sides again
			redone = transform_side(i,redo_sides,new_t)
		
		#add the completed and the newly folded sides to a new list
		final = redone.copy()
		final.update(new_run)
		#call this function again to check if all sides have met another side
		if theta < 360:
			return check_sides(redone,new_run,new_t,final)
		else:
			return -1

def make_sides(sides,theta):
	"""Function iterates through the sides and folds each one, returning new coordinates
		Input: sides dictionary, theta
		Output: the transformed sides
	"""
	length = len(sides)
	
	#iterate through sides to fold each side individually
	for i in sides:
		side = sides[i][0]
		transformed_side = transform_side(i,sides,theta)
	return transformed_side

def main(sides,xy_coord):
	"""Main function that creates a dictionary with the two lists and calls other functions
		Input: list of sides normalized to 0,0, and list of actual side coordinates
		Output: the list of x,y,z coordinates of the final folded shape
	"""
	theta = 20
	sides_old_coordinates = {}

	#iterate through the sides to create a dictionary with side number as key, 
	#val 1 as the side normalized to 0, and val 2 as the actual side coordinates
	for i in range(0,len(sides)):
		val1 = sides[i] 
		val2 = xy_coord[i]
		if i not in sides_old_coordinates:
			sides_old_coordinates[i] = val1,val2
	
	#call function to iterate through sides and fold each one
	run_fxn = make_sides(sides_old_coordinates,theta)
	#call function to check that sides have met up (prism has been folded)
	final_sides = check_sides(run_fxn,{},theta,{})
	#call function to output the final lists of x,y,z coordinates
	if final_sides == -1:
		return "Sorry, these sides never meet up!Here is what I am trying to fold:",xy_coord
	else:
		return output(final_sides[0],final_sides[1])
	
if __name__ == "__main__":

	#following hard-coded shapes are for testing purposes
	"""CUBE (WORKS)"""
	#side_coordinates = (([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]))
	#actual_coordinates = (([6,6],[0,6],[0,12],[6,12]),([6,12],[6,18],[12,18],[12,12]),([12,12],[18,12],[18,6],[12,6]),([12,6],[12,0],[6,0],[6,6]))

	"""side_coordinates = (([0.0, 0.0], [0.0, 194.0], [176.00000000000003, 193.99999999999997], [176.0, 0.0]), ([0.0, 0.0], [0.0, 176.0], [173.0, 176.0], [173.0, 0.0]), ([0.0, 0.0], [0.0, 194.0], [165.00000000000003, 193.99999999999997], [165.0, 0.0]), ([0.0, 0.0], [0.0, 176.0], [147.99999999999997, 176.00000000000003], [148.0, 0.0]))
	actual_coordinates = (([381, 451], [381, 645], [557, 645], [557, 451]), ([205, 451], [381, 451], [381, 278], [205, 278]), ([205, 645], [205, 451], [40, 451], [40, 645]), ([381, 645], [205, 645], [205, 793], [381, 793]))
	print main(side_coordinates,actual_coordinates)"""

	"""side_coordinates = (([0,0],[0,110],[100,100],[100,0]),([0,0],[0,110],[100,100],[100,0]),([0,0],[0,115],[100,100],[100,0]),([0,0],[0,110],[100,100],[100,0]))
	actual_coordinates = (([100,200],[100,310],[200,300],[200,200]),([200,200],[310,200],[300,100],[200,100]),([200,100],[200,-15],[100,0],[100,100]),([100,100],[-10,100],[0,200],[100,200]))
	print main(side_coordinates,actual_coordinates)"""

	side_coordinates = (([0.0, 0.0], [0.0, 173.0], [176.00000000000003, 172.99999999999997], [176.0, 0.0]), ([0.0, 0.0], [0.0, 165.0], [194.0, 165.0], [194.0, 0.0]), ([0.0, 0.0], [0.0, 148.0], [176.0, 148.0], [176.0, 0.0]), ([0.0, 0.0], [0.0, 176.0], [194.0, 176.0], [194.0, 0.0]))
	actual_coordinates = (([381, 451], [381, 278], [205, 278], [205, 451]), ([205, 451], [40, 451], [40, 645], [205, 645]), ([205, 645], [205, 793], [381, 793], [381, 645]), ([381, 645], [557, 645], [557, 451], [381, 451]))
	print main(side_coordinates,actual_coordinates)

	"""RECTANGULAR PRISM
	side_coordinates = (([0.0, 0.4], [0.0, 2.0], [1.5, 2.0], [1.0, 0.0]), ([0.0, 0.0], [0.0, 2.0], [1.0, 2.0], [1.0, 0.0]), ([0.0, 0.0], [0.0, 2.0], [0.9999999999999998, 2.0], [1.0, 0.0]), ([0.0, 0.0], [0.0, 2.0], [0.9999999999999999, 2.0], [1.0, 0.0]))
	actual_coordinates = (([3, 2.2], [3, 0], [2, 0], [2, 2]), ([3, 3], [5, 3], [5, 2], [3, 2]), ([2, 3], [2, 5], [3, 5], [3, 3]), ([2, 2], [0, 2], [0, 3], [2, 3]))

	print main(side_coordinates,actual_coordinates)"""

	"""SQUARE PYRAMID (WORKS)
	side_coordinates = (([0,0],[3,6],[6,0]),([0,0],[3,6],[6,0]),([0,0],[3,6],[6,0]),([0,0],[3,6],[6,0]))
	actual_coordinates = (([6,6],[0,9],[6,12]),([6,12],[9,18],[12,12]),([12,12],[18,9],[12,6]),([12,6],[9,0],[6,6]))
	
	print main(side_coordinates,actual_coordinates)"""

	"""TRIANGULAR PRISM (WIP)
	side_coordinates = (([0,0],[0,6],[6,6],[6,0]),([0,0],[3,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[3,6],[6,0]))
	actual_coordinates = (([6,6],[0,6],[0,12],[6,12]),([6,12],[9,18],[12,12]),([12,12],[18,12],[18,6],[12,6]),([12,6],[9,0],[6,6]))

	print main(side_coordinates,actual_coordinates)"""
	
	"""PYRAMID (DOESN'T WORK)
	side_coordinates = (([0,0],[3,6],[6,0]),([0,0],[3,6],[6,0]),([0,0],[3,6],[6,0]))
	actual_coordinates = (([6,0],[0,0],[3,6]),([3,6],[6,12],[9,6]),([9,6],[12,0],[6,0]))

	print main(side_coordinates,actual_coordinates)"""