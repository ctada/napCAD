#Caleb
#normalizes shapes in size and sets the lower left corner to 0
import math

def calc_dist(a,b):
	ax=a[0]
	ay=a[1]
	bx=b[0]
	by=b[1]

	return math.sqrt((ax-bx)**2+(ay-by)**2)


def normalize(shapes):
	right=shapes[0]
	left=shapes[1]
	top=shapse[2]
	back=shapes[3]
	front=shapes[4]
	bottom=shapes[5]

	leftscale=calc_dist(front[0],front[2])/calc_dist(left[1],left[3])
	topscale=calc_dist(front[0],front[1])/calc_dist(top[2],top[3])
	rightscale=calc_dist(front[1],front[3])/calc_dist(right[0],right[3])
	bottomscale=calc_dist(front[2],front[3])/calc_dist(bottom[0],bottom[1])
	backscale=bottomscale*calc_dist(bottom[3],bottom[4])/calc_dist(back[0],back[1])

	scaleFactors=[rightscale,leftscale,topscale,backscale,1,bottomscale]

	#scale everything by a factor determined by adjacent sides
	scaledShapes=[]
	for shape in enumerate(shapes):
		scaledShape=[]
		for point in shape:
			newpoint=tuple([i * scaleFactors[shape[0]] for i in point])
			scaledShape.append(newpoint)
		scaledShapes.append(scaledShape)

	#normalize to 0 (sets the bottom left corner to 0,0)
	shiftedShapes=[]
	for shape in scaledShapes:
		x=shape[3][0]
		y=shape[3][1]
		newShape=[]
		for point in shape:
			newpoint=tuple([point[0]-x,point[1]-y])
			newShape.append(newpoint)
		shiftedShapes.append(newShape)

	return shiftedShapes