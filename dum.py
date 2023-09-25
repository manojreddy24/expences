import numpy as np
from numpy import dot, diag, diagflat, array, zeros

def jacobi(A, b, init_guess,error_tolerance, N=100):
    print("Jacobi")
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed
    count = 0
    print(init_guess)
    condition = True

    while condition:
        u1 = (5 - init_guess[5] + 2 * init_guess[1]) / 6
        u2 = (3 + 2 * init_guess[0] + 2 * init_guess[2] - init_guess[4]) / 6
        u3 =  (1 + init_guess[1] + init_guess[3]) / 3
        u4=(1 + init_guess[2] + init_guess[4]) / 3
        u5=(3 - init_guess[1] + 2 * init_guess[3] + 2 * init_guess[5]) / 6
        u6=(5 - init_guess[0] + 2 * init_guess[4]) / 6



        print('%d\t%0.4f\t%0.4f\t%0.4f\t%0.4f\t%0.4f\t%0.4f\n' % (count, u1,u2, u3,u4,u5,u6))

        e1 = abs(u1 - init_guess[0])
        e2 = abs(u2 - init_guess[1])
        e3 = abs(u3 - init_guess[2])
        e4 = abs(u4 - init_guess[3])
        e5 = abs(u5 - init_guess[4])
        e6 = abs(u6 - init_guess[5])




        count += 1
        init_guess[0] = u1
        init_guess[1] = u2
        init_guess[2] = u3
        init_guess[3] = u4
        init_guess[4] = u5
        init_guess[5] = u6



        condition = e1 > error_tolerance and e2 > error_tolerance and e3 > error_tolerance and e4 > error_tolerance and e5 > error_tolerance and e6 > error_tolerance

    print('\nSolution: 1=%0.3f, 2=%0.3f, 3=%0.3f,4=%0.3f,5=%0.3f, and 6 = %0.3f\n' % (u1, u2, u3,u4,u5,u6))












    return 1



A=array([[3,-1,0,0,0,1/2],[-1,3,-1,0,1/2,0],[0,-1,3,-1,0,0],[0,0,-1,3,-1,0],[0,1/2,0,-1,3,-1],[1/2,0,0,0,-1,3]])
b=array([5/2,3/2,1,1,3/2,5/2])
init_guess = array([0,0,0,0,0,0])
D = diag(A)
# print(D)
if np.all(D > np.abs(A).sum(axis=1) - D):

    print("Matrix A is diagonally dominant")
else:
    print("Matrix A is NOT diagonally dominant so we are exchanging rows")

    for i in range(len(A)):
        if np.abs(A[i, i]) < np.abs(A[0, :]).sum():
            print("Row exchange")
            A[[i, np.argmax(np.abs(A[i:, i]))]] = A[[np.argmax(np.abs(A[i:, i])), i]]
            b[[i, np.argmax(np.abs(A[i:, i]))]] = b[[np.argmax(np.abs(A[i:, i])), i]]
            # print(A)
            # print(b)
            print("Row exchange done")
            break


jacobi = jacobi(A, b, init_guess,error_tolerance=0.01, N=100)
print(jacobi)