import numpy as np
E = 10

A0 = [0,0,0]
A1 = [4,3,0]
p1_1 = [1,2,0]
p1_0 = A1 + p1_1
v_p1_0 = [1,-1,0]

px = p1_0[0]
py = p1_0[1]
pz = p1_0[2]

D = np.array([[0, -3, 0, 1],
              [3, 0, 0, -1],
              [0,0,0,0],
              [0,0,0,0]])
D = np.ndarray.round(D.reshape(4,4), E)

T = np.array([[1,0,0,4],
              [0,1,0,3],
              [0,0,1,0],
              [0,0,0,1]])
T = np.ndarray.round(T.reshape(4,4), E)

DT = np.dot(D, T)
DT = np.ndarray.round(DT, E)

w = np.array([1,2,0,1])
w = w.reshape(4,1)

Tw = np.dot(T, w)
DTw = np.dot(D, Tw)
DTw = np.ndarray.round(DTw, E)
print("DTw: ", DTw)
