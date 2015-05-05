import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
def v1(): 
	# pyramid
	# u, v are parameterisation variables
	#u = np.array([0,0,0.5,1,1]) 
	#v = np.array([0,1,0.5,0,1]) 

	#x = u
	#y = v
	#z = np.array([0,0,1,0,0])

	# cube-- sort of
	# u, v are parameterisation variables
	u = np.array([0,0,1,1,0,0,1,1,.5,0]) 
	v = np.array([0,1,0,1,0,1,0,1,.5,.5]) 

	x = u
	y = v
	z = np.array([0,0,0,0,1,1,1,1,1,.5])

	# Triangulate parameter space to determine the triangles
	#tri = mtri.Triangulation(u, v)
	tri = Delaunay(np.array([u,v]).T)

	print 'polyhedron(faces = ['
	#for vert in tri.triangles:
	for vert in tri.simplices:
	    print '[%d,%d,%d],' % (vert[0],vert[1],vert[2]),
	print '], points = ['
	for i in range(x.shape[0]):
	    print '[%f,%f,%f],' % (x[i], y[i], z[i]),
	print ']);'

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection='3d')

	# The triangles in parameter space determine which x, y, z points are
	# connected by an edge
	#ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap=plt.cm.Spectral)
	ax.plot_trisurf(x, y, z, triangles=tri.simplices, cmap=plt.cm.Spectral)


	plt.show()

def v2():
	points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
	tri = Delaunay(points)

	plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
	#plt.plot(points[:,0], points[:,1], 'o')
	
	for j, p in enumerate(points):
	    plt.text(p[0]-0.03, p[1]+0.03, j, ha='right') # label the points
	for j, s in enumerate(tri.simplices):
	    p = points[s].mean(axis=0)
	    plt.text(p[0], p[1], '#%d' % j, ha='center') # label triangles
	plt.xlim(-0.5, 1.5); plt.ylim(-0.5, 1.5)
	plt.show()


if __name__ == "__main__":
	v1()