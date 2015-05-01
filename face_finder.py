#This fuction finds faces



#From http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
import math

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

	# startpoint=0 #this gives the most recent point before jumping across a fold line

	# faces=[]

	# while startpoint+1 < len(maincontour): #if the index of the next point to check is giving the original start point, stop
	# 	face=[maincontour[startpoint]

	# 	nextpoint=startpoint+1 #initialize next point to check
	# 	while maincontour[nextpoint] is not maincontour[startpoint]: #stop when a full loop is made
	# 		face.append(maincontour[nextpoint])

	# 		#If this point is on a fold line, skip ahead to the other side of the fold line
	# 		onFoldline=False
	# 		for line in enumerate(foldlines):
	# 			if maincontour[nextpoint] in line[1] and line[1][line[1].index(maincontour[nextpoint])-1] < nextpoint
	# 				onFoldline=line[0]

	# 		if onFoldline==False:
	# 			nextpoint=nextpoint+1

	# 		else:
	# 			line=foldlines[onFoldLine]
	# 			jumpPoint=line[line.index(maincontour[nextpoint])-1] #jump across a foldline, but only to a smaller index
	# 			nextStartPoint=nextpoint+1
	# 			if jumpPoint==maincontour[starpoint]:
	# 				nextpoint=startpoint 							#so that we don't accidentally skip over the startpoint
	# 			else nextpoint=maincontour.index(jumpPoint)+1		#so that we don't jump back and forth over and over
	# 			face.append(jumpPoint)


	connectionDict={}
	for point in enumerate(maincontour):
		index=point[0]
		connections=[tuple(maincontour[index-1]),tuple(maincontour[(index+1)%(len(maincontour))])]
		for line in foldlines:
			if point[1] in line:
				connections.insert(0,tuple(line[line.index(point[1])-1]))
		connectionDict[point[1]]=connections

	faceLists=[]
	for point in maincontour:
		face=(breadth_first(point, connectionDict)[:-1])
		faceLists.append(face)



	culledFaceLists=[]
	faceSets=[]
	for face in faceLists:
		if set(face) not in faceSets:
			faceSets.append(set(face))
			culledFaceLists.append(face)

	rotatedFaceLists=[]

	for face in culledFaceLists:
		totalfoldlines=0
		for point in enumerate(face):
			point2=point[1]
			index=point[0]
			point1=face[index-1]
			if [point1,point2] in foldlines:
				totalfoldlines+=1
				
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
			uprightFace.append([newpoint])
		rotatedFaceLists.append(uprightFace)
	return rotatedFaceLists


	# 		for value in enumerate(newpoint):
	# 			if value[1] < 1e-5:
	# 				newpoint[value[0]]=0
	# 		flippedFace.append(newpoint)
	# 	rotatedFaceLists.append(flippedFace)
	# return rotatedFaceLists





# def depth_first(pointlist,connectionDict):
# 	lastpoint=pointlist[-1]
# 	loops=[]
# 	for connection in connectionDict[tuple(lastpoint)]:

# 		if connection == pointlist[0] and len(pointlist) != 2:
# 			loops.append(pointlist)
			
# 		if connection not in pointlist:
# 			loops.append(depth_first(pointlist+[connection],connectionDict))
# 	lengths=[None]
# 	print 'loops'
# 	print loops
# 	for loop in enumerate(loops):
# 		lengths.append(len(loops[loop[0]]))
# 	if lengths != []:
# 		return loops[lengths.index(min(lengths))]
# 	if lengths == []:
# 		return []

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
	print face_finder(testshape,foldlines)