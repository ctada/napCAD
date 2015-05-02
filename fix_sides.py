#This function fixes the sides to be all the right lengths
import scipy
import numpy


def fix_sides(maincontour, foldlines):
	edges=[]
	for point in maincontour:
		
		if point == maincontour[-1]:

