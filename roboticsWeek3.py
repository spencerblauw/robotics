
import numpy as np
import sys

E = 10 #rounding constant

# frame lengths
a1 = 1 
a2 = 1 
a3 = 1 
a4 = 1 
# Angles in degrees
T1 = 90 # Angle 1
T2 = 90 # Angle 2
T3 = 90 # Angle 3

T1 = (T1/180)*np.pi
T2 = (T2/180)*np.pi
T3 = (T3/180)*np.pi

    # Define the First rotation matrix. ***ROATES AROUND Z Axis***
def getMatrices():
    R0_1 = np.array([       [np.cos(T1), -np.sin(T1), 0],
                            [np.sin(T1), np.cos(T1), 0],
                            [0, 0, 1]]) 
    R0_1 = np.ndarray.round(R0_1, E)
    print('R0_1 =\n', R0_1)
    print()
    # Define the Second rotation matrix. ***ROATES AROUND X Axis***
    R1_2 = np.array([       [1, 0, 0],
                            [0, np.cos(T2), -np.sin(T2)],
                            [-np.sin(T2), 0, np.cos(T2)]]) 
    R0_2 = np.dot(R0_1, R1_2)
    R0_2 = np.ndarray.round(R0_2, E)
    print('R0_2 =\n', R0_2)
    print()

     # Define the Third rotation matrix. ***ROATES AROUND Z Axis***
    R3_2 =   ([[np.cos(T3), -np.sin(T3), 0],
              [np.sin(T3), np.cos(T3), 0],
              [0, 0, 1]])
    R0_3 = np.dot(R0_2, R3_2)
    R0_3 = np.ndarray.round(R0_3, E)
    print('R0_3\n', R0_3)
    print()
# Frame can only be mainpulated in the Z direction in this SCARA model.  End Effector length can range from (0,1).
    

    
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
    
    #Frame 2 to fram 3
    D2_3 = D1_2

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

    #HTM from frame 2 to frame 3
    H2_3 = np.concatenate((R3_2, D2_3), axis=1)
    H2_3 = np.concatenate((H2_3, extra_row), 0)
    H2_3 = np.ndarray.round(H2_3, E)
    print('H2_3 =\n', H2_3)
    print()

    #Frame 3 to 1
    H1_3 = np.dot(H1_2, H2_3)
    H1_3 = np.ndarray.round(H1_3, E)
    
    #HTM from frame 0 to frame 3
    H0_3 = np.dot(H0_2, H2_3)
    H0_3 = np.ndarray.round(H0_3, E)
    print("Homogeneous Transformation Matrix\n Frame Frame 0 --> Frame 3")
    print('H0_3 =\n', H0_3)
    print()

    return D0_1, D1_2, D2_3, H0_1, H0_2, H1_2, H1_3, H2_3, H0_3, R0_1, R0_2, R1_2, extra_row

D0_1, D1_2, D2_3, H0_1, H0_2, H1_2, H1_3, H2_3, H0_3, R0_1, R0_2, R1_2, extra_row = getMatrices()

#Points
def getPoints():
    # End Point
    c = [1,0,0]
    p3 = c
    p3 = np.array(p3)
    p3 = p3.reshape(3,1)
    p3 = np.concatenate((p3, [[1]]), 0)
    print('p3 = ')
    print(p3)
    print()
    # p2
    p2 = H2_3.dot(p3)
    p2 = np.ndarray.round(p2, E)
    print('p2 = ')
    print(p2)
    print()
    # p1
    p1  = H1_3.dot(p3)
    p1  = np.ndarray.round(p1, E)
    print('p1 = ')
    print(p1)
    print()
    # p0
    p0 = H0_3.dot(p3)
    p0 = np.ndarray.round(p0, E)
    print('p0 = ')
    print(p0)
    print()
    
    w = p0[3][0]
    c = [p0[i][0]/w for i in [0, 1, 2]]
    print("Cartesian Coordinates for p0: \n", c)
    return p0, p1, p2, p3, w

p0, p1, p2, p3, w = getPoints()
