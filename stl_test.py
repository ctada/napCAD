import numpy as np
from scipy.spatial import Delaunay, ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import stlwriter # found at http://code.activestate.com/recipes/578246-stl-writer/

def triangulation(x, y, z):
	"""
	Triangulation with ConvexHull and plotting

	"""
	points = np.array([x, y, z]).T
	tri = ConvexHull(points, qhull_options='QJ Pp')
	# p= points[tri.vertices] or #p= points[tri.convex_hull] to access points, note: tri.simplices = tri.vertices

	# FOR VISUALIZATION PURPOSES
	# to plot 3D representation, take out the z in the np array above
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection='3d')
	ax.plot_trisurf(x, y, z, triangles=tri.simplices, cmap=plt.cm.Spectral) #tri.simplices references the faces of the triangles
	
	#for j, p in enumerate(points):
	#	    ax.text(p[0]-0.03, p[1]+0.03, z[j], j, ha='right') # label the points
	#for j, s in enumerate(tri.simplices):
	#	    p = points[s].mean(axis=0)
	#	    ax.text(p[0], p[1], z[j],'#%d' % j, ha='center') # label triangles

	#plt.show()

	return points[tri.simplices], tri.simplices

def stl_write(file_name, cube_vertices): 
    with open(file_name, 'wb') as fp:
        writer = stlwriter.Binary_STL_Writer(fp)
        writer.add_faces(cube_vertices)
        writer.close()

if __name__ == "__main__":
	# example coordinates
	shape = 2
	if shape == 1: 
		filename = 'cubeTest.stl'
		x = [5,5,-5,-5,5,5,-5,-5]
		y = [5,5,5,5,-5,-5,-5,-5]
		z = [5,-5,5,-5,5,-5,5,-5]
	elif shape == 2: 
		filename = 'pyramidTest.stl'
		x = [0,0,0.5,1,1]
		y = [0,1,0.5,0,1]
		z = [0,0,1,0,0]

	vert = triangulation(x,y,z)
	#stl_write(filename, vert[0])