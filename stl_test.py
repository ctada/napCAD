from stl import mesh
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import stlwriter

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
	 
	#print 'vertices', points[tri.vertices]
def np_stl(): 
	"""
	Save to STL, based off of numpy-stl library
	"""
	# Using an existing stl file:
	mesh = mesh.Mesh.from_file('testcube_10mm.stl')

	# Or creating a new mesh:
	#VERTICE_COUNT = 10
	#data = np.zeros(VERTICE_COUNT, dtype=mesh.Mesh.dtype)
	#mesh = mesh.Mesh(data, remove_empty_areas=False)

	# The mesh normals (calculated automatically)
	mesh.normals
	# The mesh vectors
	mesh.v0, mesh.v1, mesh.v2

	#for i in range(len(mesh.v0)):
		# multiple v0, v1, and v2 for scaling and avoiding pyramids
	#	mesh.v0[i] *= 2#*numpy.random.randint(-i,i+1)
	#	mesh.v1[i] *= 2 #*numpy.random.randint(-i, i+1)
	#	mesh.v2[i] *= 3


	# Accessing individual points (concatenation of v0, v1 and v2 in triplets)
	mesh.points[0] == mesh.v0[0]
	mesh.points[1] == mesh.v1[0]
	mesh.points[2] == mesh.v2[0]
	mesh.points[3] == mesh.v0[1]
	#mesh.update_normals()

	mesh.save('new_stl.stl')

	print 'points', mesh.points
	print 'data', mesh.data
	#print 'v0', mesh.v0

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