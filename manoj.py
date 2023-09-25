from pprint import pprint
from numpy import array, zeros, diag, diagflat, dot
import numpy as np

def jacobi(A, b, N=100, guess=None):
    print("Jacobi")
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed
    count=0
    if guess is None:
        guess = zeros(len(A[0]))
        print("guess",guess)
    D = diag(A)
    # print(D)
    R = A - diagflat(D)
    # print(R)

    # Create a vector of the diagonal elements of A
    # # Initialize the solution vector
    x = guess.copy()
    # print(x)

    # Iterate for N times
    for i in range(N):
        x = (b - dot(R, x)) / D

    return x
    # for _ in range(N):
    #     x_new = (b - np.dot(A, x) + np.multiply(D, x)) / D
    #     x = x_new
    #     count+=1
    # print("x[",count,"]=",x)
    #
    # return x

def gauss_seidel(A, b, tolerance=0.01, N=100, guess=None):
    print("Gauss Seidel")
    """Solves the equation Ax=b via the Gauss-Seidel iterative method."""
    # Create an initial guess if needed
    if guess is None:
        guess = np.zeros(len(A[0]), dtype=np.double)

    # Initialize the solution vector
    x = guess.copy()
    print(x)
    n = len(A)

    # Iterate
    count = 0
    for k in range(N):

        x_old = x.copy()

        # Loop over rows

        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i + 1:], x_old[i + 1:])
            x[i] = (b[i] - s1 - s2) / A[i, i]
            count=count+1


        # Stop condition
        if np.linalg.norm(x - x_old, ord=np.inf) / np.linalg.norm(x, ord=np.inf) < tolerance:
            return x
        print( count)

    return x
#
#
def sor(A,b,N=100,tolerance=0.01,guess=None,w=1.1):
    print("SOR")
    if guess is None:
        guess = np.zeros(len(A[0]), dtype=np.double)

    # Initialize the solution vector
    x = guess.copy()
    print(x)
    n = len(A)

    # Iterate
    count = 0
    for iteration in range(N):
        for i in range(n):
            sum1 = np.dot(A[i, :i], x[:i])
            sum2 = np.dot(A[i, (i + 1):], x[(i + 1):])
            x[i] = (1 - w) * x[i] + (w / A[i, i]) * (b[i] - sum1 - sum2)
            count = count + 1


        if np.linalg.norm(np.dot(A, x) - b) < tolerance:
            return x
        print( count)

    return x













A=array([[3,-1,0,0,0,1/2],[-1,3,-1,0,1/2,0],[0,-1,3,-1,0,0],[0,0,-1,3,-1,0],[0,1/2,0,-1,3,-1],[1/2,0,0,0,-1,3]])
b=array([5/2,3/2,1,1,3/2,5/2])
guess = array([0,0,0,0,0,0])
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
print("A:")
# pprint(A)

print("b:")
# pprint(b)


jacobi = jacobi(A, b, N=7, guess=guess)
print(jacobi)
sol = gauss_seidel(A, b, N=50,guess=guess)
seidal=gauss_seidel(A, b, tolerance=0.01, N=100, guess=None)
print("x:")
print(seidal)
sor=sor(A,b,N=5,tolerance=0.01,guess=None,w=1.1)
print(sor)
