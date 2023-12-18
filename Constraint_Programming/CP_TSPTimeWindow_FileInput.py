from ortools.sat.python import cp_model
import time

# Bien: X: x[i][j] = 1 neu di tu thanh pho i den thanh pho j, 0 neu nguoc lai
#       M: M[i] = thoi gian den thanh pho i
#       w: w[i] = thoi gian cho tai thanh pho i
# Rang buoc:
#       - Moi thanh pho chi duoc di qua 1 lan
#       - Thoi gian den thanh pho i phai nam trong khoang [e[i], l[i]]
#       - Thoi gian den thanh pho j = tg den thanh pho i + tg giao hang tai i + tg di tu i den j + tg cho tai j
# Muc tieu: Minimize tong thoi gian di chuyen giua cac thanh pho
# -----------------------------------------------

# NOTE: Chu trinh con duoc loai bo: thoi gian den thanh pho i = thoi gian den thanh pho j + thoi gian di tu j den i

inputFolder = "testcase/input"
outputFolder = "testcase/output"
timeFile = "CP/time.txt"
allFile = ["N5.txt", "N10.txt", "N100.txt", "N200.txt", "N300.txt", "N500.txt", "N600.txt", "N700.txt", "N900.txt",
           "N1000.txt"]


def CP_TSP_TimeWindow(num_nodes, e, l, d, time_matrix):
    x = {}  # x[i,j] = 1 if i -> j else 0
    M = {}  # M[i] = thoi gian giao hang tai thanh pho i
    w = {}  # w[i] = thoi gian cho tai thanh pho i

    # Model
    model = cp_model.CpModel()

    for i in range(num_nodes + 1):
        for j in range(num_nodes + 1):
            x[i, j] = model.NewIntVar(0, 1, 'x[%i, %i]' % (i, j))

    # Thoi gian den thanh pho i phai nam trong khoang [e[i], l[i]]
    for i in range(num_nodes + 1):
        M[i] = model.NewIntVar(e[i], l[i], 'M[%i]' % i)
        w[i] = model.NewIntVar(0, 1000000, 'w[%i]' % i)

    # Khoi tao gia tri cho M[0] va w[0]
    model.Add(M[0] == 0)
    model.Add(w[0] == 0)

    # Moi thanh pho chi duoc di qua 1 lan
    for i in range(num_nodes + 1):
        model.Add(sum(x[i, j] for j in range(num_nodes + 1) if j != i) == 1)
        model.Add(sum(x[j, i] for j in range(num_nodes + 1) if j != i) == 1)

    # Thoi gian den thanh pho j = tg den thanh pho i + tg giao hang tai i + tg di tu i den j + tg cho tai j
    for i in range(num_nodes + 1):
        for j in range(num_nodes + 1):
            if i != j and j != 0:
                model.Add(M[j] >= M[i] + d[i] + time_matrix[i, j] + w[j] + (x[i, j] - 1) * 1000000000)
                model.Add(M[j] <= M[i] + d[i] + time_matrix[i, j] + w[j] + (1 - x[i, j]) * 1000000000)

    # Muc tieu: Minimize tong thoi gian di het cac thanh pho
    model.Minimize(sum(time_matrix[i, j] * x[i, j] for i in range(num_nodes) for j in range(num_nodes) if j != i))

    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Result
    if status == cp_model.OPTIMAL:

        # solution = {}
        # solution[0] = 0

        # for i in range(1, num_nodes + 1):
        #     solution[i] = solver.Value(M[i])
        # solution = sorted(solution.items(), key=lambda x: x[1])

        # for i in range(1, num_nodes + 1):
        #     print(solution[i][0], end=' ')
        # print("\n")

        return solver.ObjectiveValue()
    else:
        print("No solution found.")
        return 0


if __name__ == '__main__':
    for file in allFile:
        print(file)

        e = {}
        l = {}
        d = {}
        time_matrix = {}

        # Read input
        with open(f"{inputFolder}/{file}", "r") as f:
            num_nodes = int(f.readline())

            e[0] = 0
            l[0] = 1000000000
            d[0] = 0

            for i in range(1, num_nodes + 1):
                data = f.readline().split(" ")

                e[i] = int(data[0])
                l[i] = int(data[1])
                d[i] = int(data[2])

            for i in range(num_nodes + 1):
                data = f.readline().split(" ")
                for j in range(num_nodes + 1):
                    time_matrix[i, j] = int(data[j])

        # Run TSP for each file
        startTime = time.time()
        result = CP_TSP_TimeWindow(num_nodes, e, l, d, time_matrix)
        endTime = time.time()

        # Write time to file
        with open(timeFile, "a") as fTime:
            fTime.write(f"{file}: {endTime - startTime}\n")

        # Compare result
        with open(f"{outputFolder}/{file}", "r") as fOutput:
            num_nodes = int(fOutput.readline())
            list_cities = list(map(int, fOutput.readline().split()))

            timeOutput = time_matrix[0, list_cities[0]]
            for i in range(num_nodes):
                if i < num_nodes - 1:
                    timeOutput += time_matrix[list_cities[i], list_cities[i + 1]]
                else:
                    timeOutput += time_matrix[list_cities[i], 0]

            if result <= timeOutput:
                print(f"{file} is correct")
            else:
                print(f"{file} is wrong")
