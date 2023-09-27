import numpy as np
from numpy import array, zeros, diag, diagflat, dot

def jacobi(A, b, init_guess, error_tolerance, N=100):

    # Create an initial guess if needed
    x = init_guess.copy()

    for iteration in range(N):
        u1=(b[0]-(A[0,1]*x[1]+A[0,2]*x[2]+A[0,3]*x[3]+A[0,4]*x[4]+A[0,5]*x[5]))/A[0,0]
        u2=(b[1]-(A[1,0]*x[0]+A[1,2]*x[2]+A[1,3]*x[3]+A[1,4]*x[4]+A[1,5]*x[5]))/A[1,1]
        u3=(b[2]-(A[2,0]*x[0]+A[2,1]*x[1]+A[2,3]*x[3]+A[2,4]*x[4]+A[2,5]*x[5]))/A[2,2]
        u4=(b[3]-(A[3,0]*x[0]+A[3,1]*x[1]+A[3,2]*x[2]+A[3,4]*x[4]+A[3,5]*x[5]))/A[3,3]
        u5=(b[4]-(A[4,0]*x[0]+A[4,1]*x[1]+A[4,2]*x[2]+A[4,3]*x[3]+A[4,5]*x[5]))/A[4,4]
        u6=(b[5]-(A[5,0]*x[0]+A[5,1]*x[1]+A[5,2]*x[2]+A[5,3]*x[3]+A[5,4]*x[4]))/A[5,5]


        print(f'Iteration {iteration + 1}: u1={u1:6f}, u2={u2:6f}, u3={u3:6f}, u4={u4:6f}, u5={u5:6f}, u6={u6:6f}')

        e = np.max(np.abs(x - np.array([u1, u2, u3, u4, u5, u6])))
        ett=np.abs(x - np.array([u1, u2, u3, u4, u5, u6]))
        print("Error:",ett)

        if e < error_tolerance:
            print(f'Converged after {iteration + 1} iterations with error {e:.6f}')
            return u1, u2, u3, u4, u5, u6

        x = np.array([u1, u2, u3, u4, u5, u6])

    print(f'Failed to converge after {iteration + 1} iterations')


# Define the matrix A, vector b, initial guess, and error tolerance
A = np.array([[3, -1, 0, 0, 0, 1 / 2],
              [-1, 3, -1, 0, 1 / 2, 0],
              [0, -1, 3, -1, 0, 0],
              [0, 0, -1, 3, -1, 0],
              [0, 1 / 2, 0, -1, 3, -1],
              [1 / 2, 0, 0, 0, -1, 3]])

b = np.array([5 / 2, 3 / 2, 1, 1, 3 / 2, 5 / 2])

init_guess = np.array([0, 0, 0, 0, 0, 0])

error_tolerance = 0.01
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

# Call the Jacobi function to find u1, u2, u3, u4, u5, u6
u1, u2, u3, u4, u5, u6 = jacobi(A, b, init_guess, error_tolerance, N=100)

print(f'Solution for jacobi:')
print(f'u1={u1:6f}')
print(f'u2={u2:6f}')
print(f'u3={u3:6f}')
print(f'u4={u4:6f}')
print(f'u5={u5:6f}')
print(f'u6={u6:6f}')



