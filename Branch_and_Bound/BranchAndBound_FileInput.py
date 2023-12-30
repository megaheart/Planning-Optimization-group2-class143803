import time

inputFolder = "testcase/input"
outputFolder = "testcase/output"
timeFile = "CP/time.txt"
allFile = ["N5.txt", "N10.txt", "N100.txt", "N200.txt", "N300.txt", "N500.txt", "N600.txt", "N700.txt", "N900.txt",
           "N1000.txt"]

best_time = 1000000000
best_path = []
min_time = 1000000000


def branch_and_bound(num_nodes, e, l, d, w, time_matrix, x, k, current_time):
    global best_time
    global best_path

    if k == 1:
        best_time = 1000000000

    # print(best_time)
    for i in range(1, num_nodes + 1):
        if (i not in x) and current_time + time_matrix[x[k - 1], i] <= l[i]:
            x[k] = i
            current_time += time_matrix[x[k - 1], i]
            w[k] = max(e[i] - current_time, 0)
            current_time += w[k]
            current_time += d[i]

            if k == num_nodes:
                current_time += time_matrix[i, 0]
                if current_time < best_time:
                    best_time = current_time
                    best_path = x.copy()
            else:
                if current_time + min_time * (num_nodes - k) < best_time:
                    branch_and_bound(num_nodes, e, l, d, w, time_matrix, x, k + 1, current_time)

            current_time -= d[i]
            current_time -= w[k]
            w[k] = 0
            current_time -= time_matrix[x[k - 1], i]
            x[k] = 0


def solve(num_nodes, e, l, d, time_matrix):
    w = [0 for i in range(num_nodes + 1)]  # w[i] = thoi gian cho tai thanh pho i
    x = [0 for i in range(num_nodes + 1)]  # x[i] - thanh pho duoc giao hang thu i

    e[0] = 0
    l[0] = 1000000000
    d[0] = 0

    branch_and_bound(num_nodes, e, l, d, w, time_matrix, x, 1, 0)

    res = 0
    for i in range(num_nodes):
        res += time_matrix[best_path[i], best_path[i + 1]]

    res += time_matrix[best_path[num_nodes], best_path[0]]

    return res


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
                    min_time = min(min_time, time_matrix[i, j])

        # Run TSP for each file
        startTime = time.time()
        result = solve(num_nodes, e, l, d, time_matrix)
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

            if result == timeOutput:
                print(f"{file} is correct")
            else:
                print(f"{file} is wrong")
