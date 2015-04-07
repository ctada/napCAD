from stl import mesh
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Triangulation of Cube
"""
x = [5,5,-5,-5,5,5,-5,-5]
y = [5,5,5,5,-5,-5,-5,-5]
z = [5,-5,5,-5,5,-5,5,-5]
points = np.array([[x[i], y[i]] for i in range(len(x))])
tri = Delaunay(points, qhull_options='QJ')
# p= points[tri.vertices] or #p= points[tri.convex_hull] to access points, note: tri.simplices = tri.vertices

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.plot_trisurf(x, y, z, triangles=tri.vertices, cmap=plt.cm.Spectral)
plt.show()
 
#print 'vertices', points[tri.vertices]

# Using an existing stl file:
mesh = mesh.Mesh.from_file('testcube_10mm.stl')
"""
VERTICE_COUNT = 12
data = np.array([[-5., -5., -5.,  5., -5., -5.,  5., -5.,  5.],
 [-5., -5., -5.,  5., -5.,  5., -5., -5.,  5.],
 [-5.,  5., -5.,  5.,  5., -5.,  5., -5., -5.],
 [-5.,  5., -5.,  5., -5., -5., -5., -5., -5.],
 [ 5.,  5., -5.,  5.,  5.,  5.,  5., -5.,  5.],
 [ 5.,  5., -5.,  5., -5.,  5.,  5., -5., -5.],
 [ 5.,  5.,  5., -5.,  5.,  5., -5., -5.,  5.],
 [ 5.,  5.,  5., -5., -5.,  5.,  5., -5.,  5.],
 [-5.,  5.,  5., -5.,  5., -5., -5., -5., -5.],
 [-5.,  5.,  5., -5., -5., -5., -5., -5.,  5.],
 [-5.,  5., -5., -5.,  5.,  5.,  5.,  5.,  5.],
 [-5.,  5., -5.,  5.,  5.,  5.,  5.,  5., -5.]], dtype=mesh.Mesh.dtype)
mesh = mesh.Mesh(data, remove_empty_areas=False)
"""

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
