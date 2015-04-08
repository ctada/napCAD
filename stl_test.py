import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import stlwriter # found at http://code.activestate.com/recipes/578246-stl-writer/

def triangulation(x, y, z):
	"""
	Delaunay triangulation and plotting
	"""
	points = np.array([x, y]).T
	tri = Delaunay(points, qhull_options='QJ')
	# p= points[tri.vertices] or #p= points[tri.convex_hull] to access points, note: tri.simplices = tri.vertices
	print points[tri.simplices]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection='3d')
	ax.plot_trisurf(x, y, z, triangles=tri.simplices, cmap=plt.cm.Spectral) #tri.simplices references the faces of the triangles

	# FOR VISUALIZATION PURPOSES
	#for j, p in enumerate(points):
	#	    ax.text(p[0]-0.03, p[1]+0.03, z[j], j, ha='right') # label the points
	#for j, s in enumerate(tri.simplices):
	#	    p = points[s].mean(axis=0)
	#	    ax.text(p[0], p[1], z[j],'#%d' % j, ha='center') # label triangles

	plt.show()

	return points[tri.simplices]

def stl_write(cube_vertices): 
    with open('cubeTest.stl', 'wb') as fp:
        writer = stlwriter.Binary_STL_Writer(fp)
        writer.add_faces(cube_vertices)
        writer.close()

if __name__ == "__main__":
	# example coordinates
	x = [5,5,-5,-5,5,5,-5,-5]
	y = [5,5,5,5,-5,-5,-5,-5]
	z = [5,-5,5,-5,5,-5,5,-5]

	vert = triangulation(x,y,z)
	stl_write(vert)