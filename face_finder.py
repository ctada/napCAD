#This fuction finds faces



#From http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
import math
import numpy

def dotproduct(v1, v2):
	return sum((a*b) for a, b in zip(v1, v2))

def length(v):
	return math.sqrt(dotproduct(v, v))

def calc_angle(v1, v2):
	return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


#From http://stackoverflow.com/questions/20023209/python-function-for-rotating-2d-objects
def rotatePolygon(polygon,theta):
    """Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = math.radians(theta)
    rotatedPolygon = []
    for corner in polygon :
        rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
    return rotatedPolygon



def face_finder(maincontour, foldlines):
	#takes in a list of points of the main contour, and a list of point pairs giving fold lines

	#dictionary of links, both contour and folded
	connectionDict={}
	for point in enumerate(maincontour):
		index=point[0]
		connections=[tuple(maincontour[index-1]),tuple(maincontour[(index+1)%(len(maincontour))])]
		for line in foldlines:
			if point[1] in line:
				connections.insert(0,tuple(line[line.index(point[1])-1]))
		connectionDict[point[1]]=connections

	#collect a list of all faces (with duplicates)
	faceLists=[]
	for point in maincontour:
		face=(breadth_first(point, connectionDict)[:-1]) #for some reason breadth first seach includes the startpoint twice. Easiest fix!
		faceLists.append(face)


	#uses set notation to drop extras
	culledFaceLists=[]
	faceSets=[]
	for face in faceLists:
		if set(face) not in faceSets:
			faceSets.append(set(face))
			culledFaceLists.append(face)

	rotatedFaceLists=[]  #the normalized and translated faces
	regularFaceLists=[]  #the original lists, but flipped if needed2


	#count fold lines to see if it's a base or not
	for face in culledFaceLists:
		faceindex=culledFaceLists.index(face)
		totalfoldlines=0
		for point in enumerate(face):
			point2=point[1]
			index=point[0]
			point1=face[index-1]
			if [point1,point2] in foldlines:
				totalfoldlines+=1

		#If it's a base, FOR NOW just remove it

		if totalfoldlines>=2:
			culledFaceLists.pop(faceindex)


		#If it's a regular side
		if totalfoldlines == 1:
			for point in enumerate(face):
				point2=point[1]
				index=point[0]
				point1=face[index-1]

				xfactor=point1[0]
				yfactor=point1[1]
				newpoint2=[point2[0]-xfactor,point2[1]-yfactor]
				angle=math.degrees(calc_angle(newpoint2,[1,0]))
				newface=[]
				for point in face:
					newpoint=[point[0]-xfactor,point[1]-yfactor]
					newface.append(newpoint)
				rotatedFace=rotatePolygon(newface,angle)

		uprightFace=[]

		upsideDown=False
		backwards=False
		for point in rotatedFace:
			if point[1]<0:
				upsideDown=True
		if rotatedFace[rotatedFace.index((0.0,0.0))+1][0] < 0:
			backwards=True

		for point in rotatedFace:
			if backwards:
				newx=point[0]*-1
			else:
				newx = point[0]
			if upsideDown:
				newy=point[1]*-1
			else:
				newy=point[1]
			newpoint=[newx,newy]
			for coord in enumerate(newpoint):
				if coord[1] < 1e-5 and coord > -1e-5:
					newpoint[coord[0]]=0


			uprightFace.append(newpoint)
		rotatedFaceLists.append(uprightFace)

		#Set 0,0 and the corresponding point at the correct spot
		# faceindex=culledFaceLists.index(face)  #define this earlier
		zeroindex=uprightFace.index([0,0])
		shifter=(-zeroindex)

		rotatedFaceLists[faceindex]=numpy.array(numpy.roll(rotatedFaceLists[faceindex],shifter,axis=0)).tolist()

		culledFaceLists[faceindex]=numpy.array(numpy.roll(culledFaceLists[faceindex],shifter,axis=0)).tolist()

		rotatedFaceLists[faceindex]=[rotatedFaceLists[faceindex][0]]+rotatedFaceLists[faceindex][1:][::-1]

		if (upsideDown and backwards) or (not upsideDown and not backwards): #Two opposite direction flips or none
			culledFaceLists[faceindex]=numpy.array([culledFaceLists[faceindex][0]]+culledFaceLists[faceindex][1:][::-1]).tolist()




	# print culledFaceLists[1]
	# print rotatedFaceLists[1]




	#Format lists as tuples of tuples of lists
	a=[]
	for face in rotatedFaceLists:
		a.append(tuple(face))
	FormattedNormalizedSides=tuple(a)

	b=[]
	for face in culledFaceLists:
		newlist=[]
		for point in face:
			newpoint=list(point)
			newlist.append(newpoint)
		b.append(tuple(newlist))
	FormattedOriginalSides=tuple(b)

	return [FormattedNormalizedSides,FormattedOriginalSides]






def breadth_first(startPoint, connectionDict): #Modified from http://stackoverflow.com/questions/8922060/breadth-first-search-trace-path

    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([startPoint])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == startPoint and len(path)>3:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in connectionDict.get(node, []):
        	if adjacent not in path[1:]:
	            new_path = list(path)
	            new_path.append(adjacent)
	            queue.append(new_path)



if __name__ == '__main__':

	testshape=[(1,0),(2,0),(2,1),(3,1),(3,2),(2,2),(2,3),(1,3),(1,2),(0,2),(0,1),(1,1)]
	foldlines=[[(1,1),(2,1)],[(2,1),(2,2)],[(2,2),(1,2)],[(1,2),(1,1)]]


	# print face_finder(testshape,foldlines)
	a=face_finder(testshape,foldlines)
	print a[0]
	print a[1]