
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from itertools import product, combinations
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

E = 10 #rounding constant

# Angles in degrees
T1 = 90 # Angle 1
T2 = 90 # Angle 2
T1 = np.deg2rad(T1)
T2 = np.deg2rad(T1)
 
# frame lengths
a1 = 1 
a2 = 1 
a3 = 1 
a4 = 1 

# Define the first rotation matrix.
R0_1 = np.array([       [np.cos(T1), -np.sin(T1), 0],
                        [np.sin(T1), np.cos(T1), 0],
                        [0, 0, 1]]) 
 
# Define the second rotation matrix.
R1_2 = np.array([       [np.cos(T2), -np.sin(T2), 0],
                        [np.sin(T2), np.cos(T2), 0],
                        [0, 0, 1]]) 
 
R0_2 = R0_1 @ R1_2

# Displacement vector from frame 0 to frame 1. 
D0_1 = np.array(         [[a2 * np.cos(T1)],
                         [a2 * np.sin(T1)],
                         [a1]]) 

# Displacement vector from frame 1 to frame 2. 
D1_2 = np.array(        [[a4 * np.cos(T1)],
                         [a4 * np.sin(T1)],
                         [a3]])

# Row vector for HTM
extra_row = np.array([[0, 0, 0, 1]])

#HTM frame 0 to frame 1
H0_1 = np.concatenate((R0_1, D0_1), axis=1)
H0_1 = np.concatenate((H0_1, extra_row), axis=0) 

#HTM from frame 1 to frame 2
H1_2 = np.concatenate((R1_2, D1_2), axis=1)
H1_2 = np.concatenate((H1_2, extra_row), axis=0)

#HTM from frame 0 to frame 2
H0_2 = H0_1 * H1_2

# Display HTM
print("Homogeneous Transformation Matrix ________________ Frame Frame 0 --> Frame 2")
print(H0_2)

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

V1 = D0_1
V2 = D1_2
V3 = (D1_2 * D0_1)
V1_2 = D0_1
V2_2 = D1_2
V3_2 = (D1_2 * D0_1)

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
