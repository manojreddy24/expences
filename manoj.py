from pprint import pprint
import numpy as np

def jacobi(A, b, N=100, guess=None):
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed
    if guess is None:
        guess = np.zeros(len(A[0]))

    # Create a vector of the diagonal elements of A
    D = np.diag(A)
    print(D)
    if np.all(D > np.abs(A).sum(axis=1) - D):

        print("Matrix A is diagonally dominant")
    else:
        print("Matrix A is NOT diagonally dominant so we are exchanging rows")

        for i in range(len(A)):
            if np.abs(A[i,i])<np.abs(A[0, :]).sum():
                print("Row exchange")
                A[[i, np.argmax(np.abs(A[i:, i]))]] = A[[np.argmax(np.abs(A[i:, i])), i]]
                b[[i, np.argmax(np.abs(A[i:, i]))]] = b[[np.argmax(np.abs(A[i:, i])), i]]
                print(A)
                print(b)
                print("Row exchange done")
                break





    # # Initialize the solution vector
    x = guess.copy()

    # # Iterate for N times
    for _ in range(N):
        x_new = (b - np.dot(A, x) + np.multiply(D, x)) / D
        x = x_new

    return x

A = np.array([[1.0, 3.0], [2.0, 1.0]])
b = np.array([5.0,5.0])
guess = np.array([1.0, 1.0])

sol = jacobi(A, b, N=100, guess=guess)

print("A:")
pprint(A)

print("b:")
pprint(b)

print("x:")
pprint(sol)
