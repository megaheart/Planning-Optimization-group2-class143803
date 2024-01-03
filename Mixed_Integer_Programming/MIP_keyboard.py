# MIXED-INTEGER PROGRAMMING MODEL FOR THE TIME WINDOWED TRAVELING SALESMAN PROBLEM

from ortools.linear_solver import pywraplp
import sys
import os
import time

curDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curDir)

def TSP_mixed_integer_programming(N, eld, t_matrix):
    model = pywraplp.Solver.CreateSolver('SCIP')

    num_nodes = N + 1 # include i = 0
    e = []  # earliest time to visit city i
    l = []  # latest time to visit city i
    d = []  # duration time to visit city i
    x_matrix = []  # x[i,j] = 1 if i -> j else 0
    M = []  # M[i] = time to visit city i
    C = []  # C[i][j] = d[i] + t_matrix[i][j]
    d.append(0)
    e.append(0)
    l.append(100000000)
    for i in range(N):
        e.append(eld[i][0])
        l.append(eld[i][1])
        d.append(eld[i][2])

    for i in range(num_nodes):
        x_i = []
        C_i = []
        for j in range(num_nodes):
            x_i.append(model.IntVar(0, 1, f'x[{i},{j}]'))
            C_i.append(d[i] + t_matrix[i][j])
        x_matrix.append(x_i)
        C.append(C_i)

    # Constraint 6
    M.append(model.IntVar(0, 0, 'M[0]'))
    model.Add(M[0] == 0)
    for i in range(1, num_nodes):
        # Constraint 3
        M.append(model.IntVar(e[i], l[i], f'M[{i}]'))


    # time waiting at city i
    w = []
    # Constraint 7
    w.append(model.IntVar(0, 0, 'w[0]'))
    model.Add(w[0] == 0)
    for i in range(1, num_nodes):
        # Constraint 8
        w.append(model.IntVar(0, model.infinity(), f'w[{i}]'))

    # define constraints
    # each city is visited exactly once (Constraint 5)
    for i in range(num_nodes):
        constraint = model.Constraint(1, 1)
        for j in range(num_nodes):
            if i != j:
                constraint.SetCoefficient(x_matrix[i][j], 1)

    # each city is left exactly once (Constraint 4)
    for i in range(num_nodes):
        constraint = model.Constraint(1, 1)
        for j in range(num_nodes):
            if i != j:
                constraint.SetCoefficient(x_matrix[j][i], 1)
    
    # time window constraints
    for i in range(num_nodes):
        for j in range(1, num_nodes):
            if i != j:
                # Constraint 1
                model.Add(M[j] >= M[i] + C[i][j] + w[j] + (x_matrix[i][j] - 1) * 100000000)
                # Constraint 2
                model.Add(M[j] <= M[i] + C[i][j] + w[j] + (1 - x_matrix[i][j]) * 100000000)

    # define objective function
    objective = model.Objective()
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                objective.SetCoefficient(x_matrix[i][j], C[i][j])
    for i in range(1, num_nodes):
        objective.SetCoefficient(w[i], 1)
    objective.SetMinimization()

    status = model.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(num_nodes- 1)
        solution = {}
        solution[0] = 0
        for i in range(1, num_nodes):
            solution[i] = M[i].solution_value()
        solution = sorted(solution.items(), key=lambda x: x[1])
        for i in range(1,num_nodes):
            print(solution[i][0], end=' ')
    else:
        print('The problem does not have an optimal solution.')

    return model.Objective().Value()

if __name__ == '__main__':
    
    N = int(input())
    customers = []
    t = []
    for i in range(1, N+1):
        e, l, d = map(int, input().split())
        customers.append([e, l, d])

    for _ in range(N+1):
        row = list(map(int, input().split()))
        t.append(row)

    ans = TSP_mixed_integer_programming(N, customers, t)

