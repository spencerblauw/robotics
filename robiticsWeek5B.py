import numpy as np
E = 3
#2DOF Serial Manipulator
a1, a2, a3 = 1,1,1
T1 = 2.1 #radians
d1 = .5

j1 = [T1, 0, a2, a1]
j2 = [0,0,0,(a3+d1)]

def getHomogeneousMatrix(j):
    T1  = j[0]
    aa1 = j[1]
    r1  = j[2]
    d1  = j[3]

    H = np.array([[np.cos(T1), -np.sin(T1), np.sin(T1), r1*np.cos(T1)],
                  [np.sin(T1), np.cos(T1)*np.cos(aa1), -np.cos(T1)*np.sin(aa1), r1*np.sin(T1)],
                  [0, np.sin(aa1), np.cos(aa1), d1],
                  [0,0,0,1]])
    H = np.ndarray.round(H, E)
    return H

#Homogeneous Matrix Transformation
H0_1 = getHomogeneousMatrix(j1)
H1_2 = getHomogeneousMatrix(j2)
H0_2 = np.dot(H0_1, H1_2)
H0_2 = np.ndarray.round(H0_2, E)

print("H0_1: \n", H0_1, "\n H1_2: \n" , H1_2, "\n H0_2 = np.dot(H0_1, H1_2), therefore: \n H0_2: \n", H0_2)
x = H0_2[0][3]
y = H0_2[1][3]
z = H0_2[2][3]
print("End Point with respect to Origin when: \nd = ", d1, "\nTheta = ", T1, "\n(",x,",",y,",",z,')')
