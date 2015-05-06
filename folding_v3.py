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

"""def find_coordinates(p1,p2,x1,y1,axis_x1,axis_y1,axis_x2,axis_y2,theta):
	Change the xy coordinates of the sides to the correct values from the original image
		Input: new point coordinates, old point coordinates, axes points, theta
		Output: translated xy coordinates
	
	#conditional statements to check if folding lines are horizontal or vertical (special cases)
	if (axis_x2>axis_x1) and (axis_y2-axis_y1==0):
		#check to see which direction to move coordinates, inwards or outwards
		if math.degrees(theta) <= 90:
			#set new x,y coordinates based upon conditional statement
			x,y = p2[0],axis_y2+math.fabs(p1[1]-y1)
		else:
			x,y = p2[0],axis_y2-math.fabs(p1[1]-y1)
	elif (axis_x2<axis_x1) and (axis_y2-axis_y1==0):
		if math.degrees(theta) <= 90:
			x,y = p2[0],axis_y2-math.fabs(p1[1]-y1)
		else:
			x,y = p2[0],axis_y2+math.fabs(p1[1]-y1)
	elif (axis_y2>axis_y1) and (axis_x2-axis_x1==0):
		if math.degrees(theta) <= 90:
			x,y = axis_x2-math.fabs(p1[0]-x1),p2[1]
		else:
			x,y = axis_x2+math.fabs(p1[0]-x1),p2[1]
	elif (axis_y2<axis_y1) and (axis_x2-axis_x1==0):
		if math.degrees(theta) <= 90:
			x,y = axis_x2+math.fabs(p1[0]-x1),p2[1]
		else:
			x,y = axis_x2-math.fabs(p1[0]-x1),p2[1]
	#in this case, the folding line is diagonal
	else:
		#slope of actual folding line
		axis_slope = (axis_y2-axis_y1)/(axis_x2-axis_x1)
		#slope of final coordinate
		point_slope = -1/axis_slope
		#intersection point of not-translated coordinate, base folding line
		int_x,int_y = p1[0],0
		#distance between intersection point and right axis coordinate (not-translated)
		axis_dist = x1-int_x
		point_dist = p1[1]-y1
		#calculating intersection point on actual folding line
		intersect_x = axis_x2 - (axis_dist*(1/math.sqrt(1+(point_slope**2))))
		intersect_y = axis_y2 - (axis_dist*(point_slope/math.sqrt(1+(point_slope**2))))
		#find final translated x,y coordinates, check if move points inwards or outwards
		if math.degrees(theta) <= 90:
			x = axis_x2 - (point_dist*(1/math.sqrt(1+(point_slope**2))))
			y = axis_y2 - (point_dist*(point_slope/math.sqrt(1+(point_slope**2))))
		else:
			x = axis_x2 + (point_dist*(1/math.sqrt(1+(point_slope**2))))
			y = axis_y2 + (point_dist*(point_slope/math.sqrt(1+(point_slope**2))))
	return x,y"""

"""def move_to_actual_coord(old_side,side_dict,side_num,theta):
	Move the side and store the new coordinates in the dictionary
		Input: side coordinates, sides dictionary, theta
		Output: new side coordinates in the sides dictionary
	
	final_side = list()
	#x and y coordinates of right point of folding axis for side normalized to 0,0's
	x2 = old_side[len(old_side)-1][0]
	y2 = old_side[len(old_side)-1][1]
	#x and y coordinates of the two points defining the actual side's folding axis
	xaxis1 = side_dict[side_num][1][0][0]
	yaxis1 = side_dict[side_num][1][0][1]
	xaxis2 = side_dict[side_num][1][len(old_side)-1][0]
	yaxis2 = side_dict[side_num][1][len(old_side)-1][1]
	
	#iterate through each point in the folded side (non-translated)
	for i,j in enumerate(old_side):
		#current x,y,z (z will remain the same)
		x = j[0]
		y = j[1]
		z = j[2]

		#actual x and y coordinates of the point before rotation (not normalized)
		real_x = side_dict[side_num][1][i][0]
		real_y = side_dict[side_num][1][i][1]

		#call function to translate x,y coordinates
		x,y = find_coordinates((x,y),(real_x,real_y),x2,y2,xaxis1,yaxis1,xaxis2,yaxis2,theta)
		
		#add to final_side list
		final_coord = x/1.0,y/1.0,z
		final_coord = list(final_coord)
		final_side.append(final_coord)

	#add final_side to sides dictionary, return dictionary
	side_dict[side_num] = list(side_dict[side_num])
	side_dict[side_num].append(final_side)
	return side_dict"""

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
	return theta,x,y,z

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
			lr1x = position[j-1][0]*.8
			ur1x = position[j-1][0]*1.2
			lr1y = position[j-1][1]*.8
			ur1y = position[j-1][1]*1.2
			lr1z = position[j-1][2]*.8
			ur1z = position[j-1][2]*1.2
			lr2x = position[j][0]*.8
			ur2x = position[j][0]*1.2
			lr2y = position[j][1]*.8
			ur2y = position[j][1]*1.2
			lr2z = position[j][2]*.8
			ur2z = position[j][2]*1.2
			if ((lr1x==lr2x) or (lr1y==lr2y)) and (lr2z>lr1z):
				key = (lr2x,ur2x,lr2y,ur2y,lr2z,ur2z,lr1x,ur1x,lr1y,ur1y,lr1z,ur1z)
			elif ((lr2x>lr1x) or (lr2y>lr1y)): 
				key = (lr2x,ur2x,lr2y,ur2y,lr2z,ur2z,lr1x,ur1x,lr1y,ur1y,lr1z,ur1z)
			else:
				key = (lr1x,ur1x,lr1y,ur1y,lr1z,ur1z,lr2x,ur2x,lr2y,ur2y,lr2z,ur2z)
			"""if ((position[j][0]==position[j-1][0]) or (position[j][1]==position[j-1][1])) and (position[j][2]>position[j-1][2]):
				key = str(position[j])+str(position[j-1])
			elif ((position[j][0]>position[j-1][0]) or (position[j][1]>position[j-1][1])):
				key = str(position[j])+str(position[j-1])
			else:
				key = str(position[j-1])+str(position[j])
			#add keys, side numbers as values to a dictionary"""	
			if key in vector_sides:
				j = vector_sides[key]
				if i in j:
					pass
				else:
					vector_sides[key].append(i)
			else: 
				vector_sides[key] = [i]
		print theta,vector_sides
	for i in run:
		position = run[i][2]
		for j in range(1,len(position)):
			for k,v in vector_sides.iteritems():
				if (position[j][0]>=k[0]) and (position[j][0]<=k[1]) and (position[j][1]>=k[2]) and (position[j][1]<=k[3]) and (position[j][2]>=k[4]) and (position[j][2]<=k[5]) and (position[j-1][0]>=k[6]) and (position[j-1][0]<=k[7]) and (position[j-1][1]>=k[8]) and (position[j-1][1]<=k[9]) and (position[j-1][2]>=k[10]) and (position[j-1][2]<=k[11]):
					if i in v:
						pass
					else:
						vector_sides[k].append(i)
				elif (position[j][0]>=k[0]) and (position[j][0]<=k[1]) and (position[j][1]>=k[2]) and (position[j][1]<=k[3]) and (position[j][2]>=k[4]) and (position[j][2]<=k[5]) and (position[j-1][0]>=k[6]) and (position[j-1][0]<=k[7]) and (position[j-1][1]>=k[8]) and (position[j-1][1]<=k[9]) and (position[j-1][2]>=k[10]) and (position[j-1][2]<=k[11]):
					if i in v:
						pass
					else:
						vector_sides[k].append(i)
				else:
					pass
	print vector_sides
	for k in vector_sides:
		#if a key has more than one value, two sides have folded to meet up
		if len(vector_sides[k])>1:
			print 'YESSSSSSS'
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
		return check_sides(redone,new_run,new_t,final)

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
	return output(final_sides[0],final_sides[1])
	
if __name__ == "__main__":

	#following hard-coded shapes are for testing purposes
	"""CUBE (WORKS)"""
	#side_coordinates = (([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]),([0,0],[0,6],[6,6],[6,0]))
	#actual_coordinates = (([6,6],[0,6],[0,12],[6,12]),([6,12],[6,18],[12,18],[12,12]),([12,12],[18,12],[18,6],[12,6]),([12,6],[12,0],[6,0],[6,6]))

	side_coordinates = (([0.0, 0.0], [29.872513615975315, -170.97553313343803],
[190.68908980679365, -128.98709636493328], [170.7913480783877,
31.86401452370699]), ([0.0, 0.0], [29.872513615975315,
-170.97553313343803], [190.68908980679365, -128.98709636493328],
[170.7913480783877, 31.86401452370699]), ([0.0, 0.0],
[21.00000000000001, 158.0], [198.0, 165.0], [178.0, 0.0]), ([0.0, 0.0],
[-6.076800673605707, 147.9292820694174], [166.65852593657547,
157.70204733182067], [176.40861656959956, 0.0]), ([0.0, 0.0],
[14.129948664096155, 174.25654808571758], [191.0729449989362,
179.1734625703078], [182.02472359545007, 0.0]))
	actual_coordinates = (([205, 467], [200,
305], [364, 278], [378, 451]), ([381, 633], [205, 645], [205, 467],
[378, 451]), ([205, 467], [47, 488], [40, 665], [205, 645]), ([205,
645], [209, 793], [382, 791], [381, 633]), ([381, 633], [555, 616],
[557, 439], [378, 451]))
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