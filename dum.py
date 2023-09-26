#jacobi
u1, u2, u3, u4, u5, u6 = [0] * 6
TOL = 0.001
n = 100
for i in range(n):
    eq1 = (5 - u6 + 2 * u2) / 6
    eq2 = (3 + 2 * u1 + 2 * u3 - u5) / 6
    eq3 = (1 + u2 + u4) / 3
    eq4 = (1 + u3 + u5) / 3
    eq5 = (3 - u2 + 2 * u4 + 2 * u6) / 6
    eq6 = (5 - u1 + 2 * u5) / 6

    print(f'\t{eq1:.4f}\t{eq2:.4f}\t{eq3:.4f}\t{eq4:.4f}\t{eq5:.4f}\t{eq6:.4f}\n')

    u_values = [u1, u2, u3, u4, u5, u6]
    eq_values = [eq1, eq2, eq3, eq4, eq5, eq6]

    tolerances = [abs(u - eq) for u, eq in zip(u_values, eq_values)]

    TOL1, TOL2, TOL3, TOL4, TOL5, TOL6 = tolerances
    u1, u2, u3, u4, u5, u6 = eq_values

    if all(tol > TOL for tol in tolerances):
        continue
    else:

        break
print(f'\nSolution: u1={eq1:0.2f}, u2={eq2:0.2f}, u3={eq3:0.2f}, u4={eq4:0.2f}, u5={eq5:0.2f}, u6={eq6:0.2f}\n')




print("GAUSS SEIDAL")





u1, u2, u3, u4, u5, u6 = [0] * 6

n = 100
for i in range(n):
    eq1 = (5 - u6 + 2 * u2) / 6
    eq2 = (3 + 2 * eq1 + 2 * u3 - u5) / 6
    eq3 = (1 + eq2 + u4) / 3
    eq4 = (1 + eq3 + u5) / 3
    eq5 = (3 - eq2 + 2 * eq4 + 2 * u6) / 6
    eq6 = (5 - eq1 + 2 * eq5) / 6

    print(f'\t{eq1:.4f}\t{eq2:.4f}\t{eq3:.4f}\t{eq4:.4f}\t{eq5:.4f}\t{eq6:.4f}\n')

    u_values = [u1, u2, u3, u4, u5, u6]
    eq_values = [eq1, eq2, eq3, eq4, eq5, eq6]

    tolerances = [abs(u - eq) for u, eq in zip(u_values, eq_values)]

    TOL1, TOL2, TOL3, TOL4, TOL5, TOL6 = tolerances
    u1, u2, u3, u4, u5, u6 = eq_values

    if all(tol > TOL for tol in tolerances):
        continue
    else:

        break
print(f'\nSolution: u1={eq1:0.2f}, u2={eq2:0.2f}, u3={eq3:0.2f}, u4={eq4:0.2f}, u5={eq5:0.2f}, u6={eq6:0.2f}\n')



print("SOR")




u1, u2, u3, u4, u5, u6 = [0] * 6

n = 100
w=1.1
for i in range(n):
    eq1 = (5 - u6 + 2 * u2) / 6
    eq2 = (3 + 2 * eq1 + 2 * u3 - u5) / 6
    eq3 = (1 + eq2 + u4) / 3
    eq4 = (1 + eq3 + u5) / 3
    eq5 = (3 - eq2 + 2 * eq4 + 2 * u6) / 6
    eq6 = (5 - eq1 + 2 * eq5) / 6

    print(f'\t{eq1:.4f}\t{eq2:.4f}\t{eq3:.4f}\t{eq4:.4f}\t{eq5:.4f}\t{eq6:.4f}\n')

    u_values = [u1, u2, u3, u4, u5, u6]
    eq_values = [eq1, eq2, eq3, eq4, eq5, eq6]
    weigt = [(1 - w) * u + w * eq for u, eq in zip(u_values, eq_values)]
    tolerances = [abs(u - eq) for u, eq in zip(u_values, weigt)]
    TOL1, TOL2, TOL3, TOL4, TOL5, TOL6 = tolerances
    u1, u2, u3, u4, u5, u6 = weigt
    if all(tol > TOL for tol in tolerances):
        continue
    else:

        break
print(f'\nSolution: u1={eq1:0.2f}, u2={eq2:0.2f}, u3={eq3:0.2f}, u4={eq4:0.2f}, u5={eq5:0.2f}, u6={eq6:0.2f}\n')



