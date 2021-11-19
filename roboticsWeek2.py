
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from itertools import product, combinations
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

E = 10
I = np.array([ [1,0,0],
			   [0,1,0],
			   [0,0,1]  ])

#Angles
T1, T2, T3 = 15, 30, 45
T1 = (T1/180)*np.pi 
T2 = (T2/180)*np.pi
T3 = (T3/180)*np.pi
#Vectors	
V1 = [0,1,0]
V2 = [1,0,0]
V3 = [0,0,1]
v4 = [0,-1,0]

#Rotation Matrices
R0_1 = np.array([
	[np.cos(T1), -np.sin(T1), 0],
	[np.sin(T1), np.cos(T1), 0],
	[0,          0,           1]
	])
R1_2 = np.array([
	[np.cos(T2), -np.sin(T2), 0],
	[np.sin(T2), np.cos(T2), 0],
	[0,          0,           1]
	])
R2_3 = np.array([
	[np.cos(T3), -np.sin(T3), 0],
	[np.sin(T3), np.cos(T3), 0],
	[0,          0,           1]
	])
R0_2 = np.dot(R0_1, R1_2)
R0_3 = np.dot(R0_2, R2_3)

#New Vectors					
V1_2 = np.dot(V1, R0_1)
V1_2 = np.ndarray.round(V1_2, E)
V2_2 = np.dot(V2, R0_2)
V2_2 = np.ndarray.round(V2_2, E)
V3_2 = np.dot(V3, R0_3)
V3_2 = np.ndarray.round(V3_2, E)

#Show work
vectors = [V1, V2, V3]
angles = [np.round(T1, decimals = 10), np.round(T2, decimals = 10), np.round(T3, decimals = 10)]
newVectors = [V1_2,	V2_2, V3_2]
i = 0
for V in vectors:
	print("Vector: \n", V, "\n rotated ", angles[i], " radians to form new Vector: \n", newVectors[i])
	i+= 1

#Visualize Data
fig = plt.figure("3D Rotation Chart", figsize=(12,9))
ax = fig.gca(projection='3d')
ax.set_aspect("auto")
plt.title("3D Rotation Chart");

ax.scatter([0], [0], [0], color="g", s=100)
ax.scatter([1], [0], [0], color="k", s=0)
ax.scatter([-1], [0], [0], color="k", s=0)
ax.scatter([0], [1], [0], color="k", s=0)
ax.scatter([0], [-1], [0], color="k", s=0)
ax.scatter([0], [0], [1], color="k", s=0)
ax.scatter([0], [0], [-1], color="k", s=0)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

class Arrow3D(FancyArrowPatch):
	def __init__(self, xs, ys, zs, *args, **kwargs):
		FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
		self._verts3d = xs, ys, zs
	def draw(self, renderer):
		xs3d, ys3d, zs3d = self._verts3d
		xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
		self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
		FancyArrowPatch.draw(self, renderer)
#verts
a = Arrow3D([0,1],[0,0],[0,0])
b = Arrow3D([0,-1],[0,0],[0,0])
c = Arrow3D([0,0],[0,1],[0,0])
d = Arrow3D([0,0],[0,-1],[0,0])
e = Arrow3D([0,0],[0,0],[0,1])
f = Arrow3D([0,0],[0,0],[0,-1])
verts = [a,b,c,d,e,f]
for a in verts:
	ax.add_artist(a)

#frames
arrows1 = []
arrows2 = []
i=1
#Before
ax.text(V1[0]+.05,V1[1]+.05,V1[2]+.05, '%s' % "V1: "+str(V1), size=12, zorder=1, color='b')
arrows1.append(Arrow3D([0,V1[0]], [0,V1[1]], [0,V1[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color = "b"))
ax.text(V2[0]+.05,V2[1]+.05,V2[2]+.05, '%s' % "V2: "+str(V2), size=12, zorder=1, color='b')
arrows1.append(Arrow3D([V1[0],V2[0]], [V1[1],V2[1]], [V1[2],V2[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color = "b"))
ax.text(V3[0]+.05,V3[1]+.05,V3[2]+.05, '%s' % "V3: "+str(V3), size=12, zorder=1, color='b')
arrows1.append(Arrow3D([V2[0],V3[0]], [V2[1],V3[1]], [V2[2],V3[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color = "b"))
#after
ax.text(V1_2[0]+.05,V1_2[1]+.05,V1_2[2]+.05, '%s' % "V1: "+str(V1), size=12, zorder=1, color='r')
arrows1.append(Arrow3D([0,V1_2[0]], [0,V1_2[1]], [0,V1_2[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color = "r"))
ax.text(V2_2[0]+.05,V2_2[1]+.05,V2_2[2]+.05, '%s' % "V2: "+str(V2), size=12, zorder=1, color='r')
arrows1.append(Arrow3D([V1_2[0],V2_2[0]], [V1_2[1],V2_2[1]], [V1_2[2],V2_2[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color = "r"))
ax.text(V3_2[0]+.05,V3_2[1]+.05,V3_2[2]+.05, '%s' % "V3: "+str(V3), size=12, zorder=1, color='r')
arrows1.append(Arrow3D([V2_2[0],V3_2[0]], [V2_2[1],V3_2[1]], [V2_2[2],V3_2[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color = "r"))

for a in arrows1:
	ax.add_artist(a)
plt.show()

#for V in vectors:
#	ax.text(V[0]+.05,V[1]+.05,V[2]+.05, '%s' % i+":"+str(V), size=12, zorder=1, color='b')
#	arrows2.append(Arrow3D([0, V[0]], [0, V[1]], [0,V[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color="b"))
#	ax.add_artist(arrows2[i-1])
#	i += 1
#for V in newVectors:
#	ax.text(V[0]+.05,V[1]+.05,V[2]+.05, '%s' % i+":"+str(V), size=12, zorder=1, color='r')
#	arrows2.append(Arrow3D([0, V[0]], [0, V[1]], [0,V[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color="r"))
#	ax.add_artist(arrows2[i-1])
#	i += 1 

