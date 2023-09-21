from pprint import pprint
from numpy import array, zeros, diag, diagflat, dot
import numpy as np

def jacobi(A, b, N=100, guess=None):
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed
    if guess is None:
        guess = zeros(len(A[0]))
    D = diag(A)
    R = A - diagflat(D)

    # Create a vector of the diagonal elements of A
    # # Initialize the solution vector
    x = guess.copy()

    # # Iterate for N times
    for i in range(N):
        x = (b - dot(R, x)) / D

    return x

A = array([[3,-1,0,0,0,1/2],[-1,3,-1,0,1/2,0],[0,-1,3,-1,0,0],[0,0,-1,3,-1,0],[0,1/2,0,-1,3,-1],[1/2,0,0,0,-1,3]])
b = array([5/2,3/2,1,1,3/2,5/2])
guess = array([1,1,1,1,1,1])
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
            print(A)
            print(b)
            print("Row exchange done")
            break
print("A:")
pprint(A)

print("b:")
pprint(b)


sol = jacobi(A, b, N=100, guess=guess)


print("x:")
pprint(sol)




