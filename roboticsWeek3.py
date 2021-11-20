
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from itertools import product, combinations
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

E = 10 #rounding constant
I = np.array([ [1,0,0],
			   [0,1,0],
			   [0,0,1]  ])


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
def getMatrices():
    R0_1 = np.array([       [np.cos(T1), -np.sin(T1), 0],
                            [np.sin(T1), np.cos(T1), 0],
                            [0, 0, 1]]) 
    # Define the second rotation matrix.
    R1_2 = np.array([       [np.cos(T2), -np.sin(T2), 0],
                            [np.sin(T2), np.cos(T2), 0],
                            [0, 0, 1]]) 
    R0_2 = np.dot(R0_1, R1_2)
    R0_2 = np.ndarray.round(R0_2, E)
    print('R0_2 =\n', R0_2)
    print()
    
    
    #Calculate HTMs
    
    # Row vector for HTM
    extra_row = np.array([[0, 0, 0, 1]])
    
    # Displacement vector from frame 0 to frame 1. 
    D0_1 = np.array(         [[a2 * np.cos(T1)],
                             [a2 * np.sin(T1)],
                             [a1]])
    D0_1 = np.array(D0_1)
    D0_1 = D0_1.reshape(3,1)
    D0_1 = np.ndarray.round(D0_1, E)
    print('D0_1 =\n', D0_1)
    print()
    
    # Displacement vector from frame 1 to frame 2. 
    D1_2 = np.array(        [[a4 * np.cos(T1)],
                             [a4 * np.sin(T1)],
                             [a3]])
    D1_2 = np.array(D1_2)
    D1_2 = D1_2.reshape(3,1)
    D1_2 = np.ndarray.round(D1_2, E)
    print('D1_2 =\n', D1_2)
    print()
    
    #HTM frame 0 to frame 1
    H0_1 = np.concatenate((R0_1, D0_1), axis=1)
    H0_1 = H0_1.reshape(3,4)
    H0_1 = np.concatenate((H0_1, extra_row), 0)
    H0_1 = np.ndarray.round(H0_1, E)
    print("H0_1 =\n", H0_1)
    
    #HTM from frame 1 to frame 2
    H1_2 = np.concatenate((R1_2, D1_2), axis=1)
    H1_2 = np.concatenate((H1_2, extra_row), 0)
    H1_2 = np.ndarray.round(H1_2, E)
    print('H1_2 =\n', H1_2)
    print()
    
    #HTM from frame 0 to frame 2
    H0_2 = np.dot(H0_1, H1_2)
    H0_2 = np.ndarray.round(H0_2, E)
    print("Homogeneous Transformation Matrix\n Frame Frame 0 --> Frame 2")
    print('H0_2 =\n', H0_2)
    print()
    return D0_1, D1_2, H0_1, H0_2, H1_2, R0_1, R0_2, R1_2, extra_row

D0_1, D1_2, H0_1, H0_2, H1_2, R0_1, R0_2, R1_2, extra_row = getMatrices()

#Points
def getPoints():
    p2 = [1,0,0]
    p2 = np.array(p2)
    p2 = p2.reshape(3,1)
    p2 = np.concatenate((p2, [[1]]), 0)
    print('p2 = ')
    print(p2)
    print()
    # p1
    p1 = np.dot(H1_2,p2)
    p1 = np.ndarray.round(p1, E)
    print('p1 = ')
    print(p1)
    print()
    # p0
    p0 = np.dot( H0_2,p2)
    p0 = np.ndarray.round(p0, E)
    print("p0 = ")
    print(p0)
    print()
    
    w = p0[3][0]
    c = [p0[i][0]/w for i in [0, 1, 2]]
    print("Cartesian Coordinates for p0: \n", c)
    return p0, p1, p2, w

p0, p1, p2, w = getPoints()

#Visualize Data
def data_visualization():
    fig = plt.figure("3D Rotation Chart", figsize=(12,9))
    ax = fig.add_subplot(projection = '3d')
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
    
    #Before rotation
    V1 = D0_1
    V2 = D1_2
    V3 = (D1_2 * D0_1)
    #After rotation
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
    return Arrow3D, V1, V1_2, V2, V2_2, V3, V3_2, a, arrows1, arrows2, ax, b, c, d, e, f, fig, i, verts

#Arrow3D, V1, V1_2, V2, V2_2, V3, V3_2, a, arrows1, arrows2, ax, b, c, d, e, f, fig, i, verts = data_visualization()
