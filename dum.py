# References
#https://copyprogramming.com/howto/diagonal-matrix-in-python
# https://math.sci.ccny.cuny.edu/document/328Code
# https://docs.python.org/3/library/string.html#format-specification-mini-language
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

        if e < error_tolerance:
            print(f'Converged after {iteration + 1} iterations with error {e:.6f}')
            return u1, u2, u3, u4, u5, u6,iteration+1


        x = np.array([u1, u2, u3, u4, u5, u6])

    print(f'Failed to converge after {iteration + 1} iterations')


#Gauss Seidel method
def gauss_seidel(A, b, init_guess, error_tolerance, N=100):
    x=init_guess.copy()
    for iteration in range(N):
        u1=(b[0]-(A[0,1]*x[1]+A[0,2]*x[2]+A[0,3]*x[3]+A[0,4]*x[4]+A[0,5]*x[5]))/A[0,0]
        u2=(b[1]-(A[1,0]*u1+A[1,2]*x[2]+A[1,3]*x[3]+A[1,4]*x[4]+A[1,5]*x[5]))/A[1,1]
        u3=(b[2]-(A[2,0]*u1+A[2,1]*u2+A[2,3]*x[3]+A[2,4]*x[4]+A[2,5]*x[5]))/A[2,2]
        u4=(b[3]-(A[3,0]*u1+A[3,1]*u2+A[3,2]*u3+A[3,4]*x[4]+A[3,5]*x[5]))/A[3,3]
        u5=(b[4]-(A[4,0]*u1+A[4,1]*u2+A[4,2]*u3+A[4,3]*u4+A[4,5]*x[5]))/A[4,4]
        u6=(b[5]-(A[5,0]*u1+A[5,1]*u2+A[5,2]*u3+A[5,3]*u4+A[5,4]*u5))/A[5,5]
        print(f'Iteration {iteration + 1}: u1={u1}, u2={u2}, u3={u3}, u4={u4}, u5={u5}, u6={u6}')

        e= np.max(np.abs(x - np.array([u1, u2, u3, u4, u5, u6])))
        # print(f'Error: {e:.6f}')

        if e < error_tolerance:
            print(f'Converged after {iteration + 1} iterations with error {e:.6f}')
            return u1, u2, u3, u4, u5, u6,iteration+1
        x=np.array([u1, u2, u3, u4, u5, u6])
    print(f'Did not converge after {iteration + 1} iterations')



#SOR method
def sor(A, b, init_guess, omega, error_tolerance, N=100):
    x = init_guess.copy()
    for iteration in range(N):
        u1 = (b[0] - (A[0, 1] * x[1] + A[0, 2] * x[2] + A[0, 3] * x[3] + A[0, 4] * x[4] + A[0, 5] * x[5])) / A[0, 0]
        u2 = (b[1] - (A[1, 0] * u1 + A[1, 2] * x[2] + A[1, 3] * x[3] + A[1, 4] * x[4] + A[1, 5] * x[5])) / A[1, 1]
        u3 = (b[2] - (A[2, 0] * u1 + A[2, 1] * u2 + A[2, 3] * x[3] + A[2, 4] * x[4] + A[2, 5] * x[5])) / A[2, 2]
        u4 = (b[3] - (A[3, 0] * u1 + A[3, 1] * u2 + A[3, 2] * u3 + A[3, 4] * x[4] + A[3, 5] * x[5])) / A[3, 3]
        u5 = (b[4] - (A[4, 0] * u1 + A[4, 1] * u2 + A[4, 2] * u3 + A[4, 3] * u4 + A[4, 5] * x[5])) / A[4, 4]
        u6 = (b[5] - (A[5, 0] * u1 + A[5, 1] * u2 + A[5, 2] * u3 + A[5, 3] * u4 + A[5, 4] * u5)) / A[5, 5]

        new_x = omega * np.array([u1, u2, u3, u4, u5, u6]) + (1 - omega) * x
        # print(new_x)

        print(f'Iteration {iteration + 1}: u1={u1}, u2={u2}, u3={u3}, u4={u4}, u5={u5}, u6={u6}')

        e = np.max(np.abs(new_x - x))
        # ett=np.abs(new_x - x)
        # print(f'Error: {ett}')
        # print(f'Error: {e:.6f}')

        if (e < error_tolerance):
            print(f'Converged after {iteration + 1} iterations with error {e:.6f}')
            return u1, u2, u3, u4, u5, u6, iteration+1
        x = new_x.copy()
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
omega=1.1
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

print("jacobi method")
# Call the Jacobi function to find u1, u2, u3, u4, u5, u6
u1, u2, u3, u4, u5, u6,iteration_jacobi = jacobi(A, b, init_guess, error_tolerance, N=100)

print("gauss seidel method")
g1,g2,g3,g4,g5,g6,iteration_guass = gauss_seidel(A, b, init_guess, error_tolerance, N=100)

print("sor method")
s1,s2,s3,s4,s5,s6,iteration_sor = sor(A, b, init_guess, omega, error_tolerance, N=100)



table = f"""
Solution:
{'-'*26}
{'Variable':<10}{'Jacobi':<25}{'Gauss-Seidel':<25}{'SOR':<15}
{'-'*26}
{'u1':<10}{u1:<25}{g1:<25}{s1:<15}
{'u2':<10}{u2:<25}{g2:<25}{s2:<15}
{'u3':<10}{u3:<25}{g3:<25}{s3:<15}
{'u4':<10}{u4:<25}{g4:<25}{s4:<15}
{'u5':<10}{u5:<25}{g5:<25}{s5:<15}
{'u6':<10}{u6:<25}{g6:<25}{s6:<15}
{'-'*26}
"""

# Print the formatted table
print(table)



print("number of iteration required to find the solution")
print("jacobi method iteration",iteration_jacobi)
print("gauss seidel method iteration",iteration_guass)
print("sor method iteration",iteration_sor)
print("amoung all the method jacobi method taking more iteration to find the solution because it neither taking updated values in that current iteration nor it dosn't have weights as sor ")
print("When w= near to 1 we can call it as gauss seidel method eventhough both guassseidal and sor taking same iterations to find the solution but sor is more efficient because it has better convergence rate than gauss seidel method")
print("SOR<GAUSS_SEIDEL<JACOBI")
