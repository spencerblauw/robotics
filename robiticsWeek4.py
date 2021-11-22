import numpy as np

""" This program will calculate the angles of a 2DOF Spherical Manipulator using inverse kinematics"""

#Enter Side Lengths
#a1, a2, a3 = 1, 1, 1
a1, a2, a3 = 1, 1, 1
print("Frame Lengths a1, a2, a3 = ", a1, a2, a3)
E = 3 #decimals

#Calculate Angles
def getAngles(x,y,z,a1,a2,a3):
    T2 = np.arcsin((z-1)/a3)
    #print("Theta 2 = ", T2)
    T1 = np.arccos(x/(a2+a3*np.cos(T2)))
    #print("Theta 1 = ", T1)
    #T1 = np.arcsin(y/(a2+a3*np.cos(T2)))
    #print("Theta 1 still = ", T1)
    return T1, T2


""" GET ANGLES FROM XYZ INPUT"""
#User Input X,Y,Z to get angles
def anglesFromInput():
    X = 0
    Y = 0
    Z = 0
    X = float(input("Enter Desired X-Coordinate : "))
    Y = float(input("Enter Desired Y-Coordinate : "))
    Z = float(input("Enter Desired Z-Coordinate : "))
    X = round(X, E)
    Y = round(Y, E)
    Z = round(Z, E)
    T1, T2 = getAngles(X,Y,Z, a1,a2,a3)
    T1 = round(T1, E)
    T2 = round(T2, E)
    print("For Coordinates X, Y and Z, = {", X , ", ",Y,", ",Z,"}:\n " +
          "The Angles for Theta1 and Theta 2 are: \n T1: ", T1, "\nT2: ", T2)
    return T1, T2, X, Y, Z

"""*************************************For Later Use******************************************"""
#Create Workspace and Spatial reference points for pre-processed mapping of output data
def createWorkspace(granularity, E, a1, a2, a3):
    #granularity = 10#Number of points in linespace
    #E = 5 #decimals
    #a1, a2, a3 = 1,1,1
    x_space = np.linspace(0,(a1+a2+a3),granularity)
    y_space = np.linspace(0,(a1+a2+a3),granularity)
    z_space = np.linspace(0,(a1+a2+a3),granularity)
    x_space = np.round(x_space, decimals=E)
    y_space = np.round(y_space, decimals=E)
    z_space = np.round(z_space, decimals=E)
    
    
    workspace = [] #Accessible Points
    voidSpace = [] #Inaccesible points
    anglespace = [] #Set of cooresponding angles
    numpoints = 0
    
    for i in x_space:
        for j in y_space:
            for k in z_space:
               T1, T2 = getAngles(i,j,k,a1,a2,a3)
               if np.isnan([T1,T2]).any() == False:
                   workspace.append([i,j,k])
                   Tset = np.round([T1, T2], decimals=E)
                   anglespace.append(Tset)
                   numpoints +=1
               else:
                   voidSpace.append([i,j,k])
   
    #create dict
    movement = {}
    i=0
    while i < numpoints:
        movement[str(workspace[i])] = tuple(anglespace[i]) #Movement points and angles 
        i+=1
    #This is the total point/angle pair dict
    cnt = 0
    for i in movement:
        print(i, np.round(np.rad2deg(movement[i]), decimals=E))
        cnt +=1
    print("Number of total points in space is: ", cnt)
    
    
    """We now have completed tables of workspace, voidspace, and anglespace. these can now
       be mapped to one another for faster  processing and verification of possible movement"""
    return

if __name__=='__main__':
    anglesFromInput()
    usrputs = input("Enter 1 if you wish to create a workspace: ")
    if usrputs == '1':
        granularity = int(input("how many total points per axis would you like to create in this world?:"))
        E = int(input("How many decimal points for rounding?"))
        a1 = float(input("Enter a1: "))
        a2 = float(input("Enter a2: "))
        a3 = float(input("Enter a3: "))
    createWorkspace(granularity, E, a1,a2,a3)


