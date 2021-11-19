import numpy as np


def q1():
    # Find sum, avg, max, min for this list using Numpy
    a = [2, 6, 1, 3, 8, 9, 2]
    b = np.array(a)
    max = np.amax(b)
    avg = np.average(b)
    min = np.amin(b)

    print('a = ',a,'\nmax = ', max, '\nmin = ', min, '\naverage = ', avg)

def q2():
    A = [
        [1, 0, 2],
        [2, 1, 0.5],
        [0, 0, 2]
    ]
    B = [
        [3, 1, 0],
        [0, 2, 0.5],
        [0, 0.2, 1]
    ]
    a = np.array(A)
    b = np.array(B)
    c = 3*a+b

    print('A =\n',a,'\nB = \n',b, '\n3A+B = \n', c)

def q3():
    a = np.random.random((3,3,3))*3
    print(a)

def q4():
    a = np.random.random((2,2))
    x = np.linalg.norm(a)
    print('Norm of \n', a, '\n is', x)

if __name__ == '__main__':
    q1()
    q2()
    q3()
    q4()
