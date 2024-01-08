import sys
import os
import time

curDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curDir)

# region Greedy Initialization
def GreedyTimeClose(N, l):
    closeTime = sorted(l)
    iterSort = [0]
    visited = [False] * (N + 1)
    for time in closeTime[1:]:
        for j in range(1, N + 1):
            if time == l[j] and not visited[j]:
                iterSort.append(j)
                visited[j] = True
                break
    return iterSort

def oneOptChange(i, j, route):
    temp = route[i]
    newRoute = route[:j] + [temp] + route[j:i] + route[i+1:]
    return newRoute

def greedy(N, e, l, d, t, C):
    iterSort = GreedyTimeClose(N, l)
    orderTime = [0] * (N + 1)
    newRoute = [0]
    visited = [False] * (N + 1)
    timeVisit = [0]
    for i in range(1, N + 1):
        orderTime[iterSort[i]] = i
    for i in range(1, N + 1):
        nextCity = iterSort[i]
        minCostOneStep = l[nextCity]
        selectCity = nextCity
        selectTime = max(e[nextCity], timeVisit[-1] + C[newRoute[-1]][nextCity])
        for j in range(1, N + 1):
            if not visited[j] and j != nextCity:
                timeCome = max(e[j], timeVisit[-1] + C[newRoute[-1]][j])
                if timeCome < minCostOneStep - C[j][nextCity]:
                    minCostOneStep = timeCome + C[j][nextCity]
                    selectCity = j
                    selectTime = timeCome
        if selectCity != nextCity:
            jChange = orderTime[selectCity]
            iterSort = oneOptChange(jChange, i, iterSort)
            for i in range(1, N + 1):
                orderTime[iterSort[i]] = i
        newRoute.append(selectCity)
        visited[selectCity] = True
        timeVisit.append(selectTime)
    return newRoute
# endregion

def calculate_M(x, N, e, l, C):
    M = [0] * (N + 1)
    for i in range(1, N + 1):
        M[x[i]] = max(e[x[i]], M[x[i - 1]] + C[x[i - 1]][x[i]])
        if M[x[i]] > l[x[i]]:
            return M, False
    return M, True

def calulate_cost(N, e, l, d, t_matrix, C, x):
    M, is_valid = calculate_M(x, N, e, l, C)
    if not is_valid:
        return -1, False
    return M[x[-1]] + C[x[-1]][0], True

def TSP_init_start_element(N,e,l,d,C,t_matrix):
    newL = l.copy()
    newL[0] = 0
    x = greedy(N, e, newL, d, t_matrix, C)
    _cost, is_valid = calulate_cost(N, e, l, d, t_matrix, C, x)
    return x, _cost

def TSP_generate_neighbor(N, x):
    newX = x.copy()
    for i in range(1, N):
        for j in range(i + 1, N + 1):
            tmp = newX[i]
            newX[i] = newX[j]
            newX[j] = tmp
            yield newX
            tmp = newX[i]
            newX[i] = newX[j]
            newX[j] = tmp
    
def TSP_best_neighbor(N, e, l, d, t_matrix, C, x, current_cost):
    best_cost = current_cost
    best_route = x
    for newRoute in TSP_generate_neighbor(N, x):
        # Check constraint and calculate cost
        new_cost, is_valid = calulate_cost(N, e, l, d, t_matrix, C, newRoute)
        # Update best cost and route
        if is_valid and new_cost < best_cost:
            best_cost = new_cost
            best_route = newRoute.copy()
    return best_route, best_cost

def TSP_local_search(N, eld, t_matrix):
    # Init variables and constraints
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
        C_i = []
        for j in range(num_nodes):
            C_i.append(d[i] + t_matrix[i][j])
        C.append(C_i)

    x, current_cost = TSP_init_start_element(N,e,l,d,C,t_matrix)

    # Local search
    while True:
        newX, newCost = TSP_best_neighbor(N, e, l, d, t_matrix, C, x, current_cost)
        if newCost < current_cost:
            x = newX
            current_cost = newCost
        else:
            print(N)
            s = ''
            for i in range(1, N + 1):
                s += str(x[i]) + ' '
            print(s)
            return current_cost

    return 0

def compare_ans_and_compute_time():
    base_path_input = './testcase/input'
    input_file = ["N5.txt", "N10.txt", "N100.txt", "N200.txt", "N300.txt", "N500.txt", "N600.txt", "N700.txt", "N900.txt", "N1000.txt"]
    base_path_output = './testcase/output'
    output_file = ["N5.txt", "N10.txt", "N100.txt", "N200.txt", "N300.txt", "N500.txt", "N600.txt", "N700.txt", "N900.txt", "N1000.txt"]
    write_time_to = './testcase/actual_output/time.txt'
    with open(write_time_to, 'w') as f:
        for i in range(len(input_file)):
            print("\nStart test case [\"" + input_file[i] + "\"]\n")
            eld = []
            t = []
            with open(os.path.join(base_path_input, input_file[i]), 'r') as file:
                # Read the input
                N = int(file.readline())

                for _ in range(N):
                    e, l, d = map(int, file.readline().split())
                    eld.append([e, l, d])

                for _ in range(N+1):
                    row = list(map(int, file.readline().split()))
                    t.append(row)

            start_time = time.time()
            ans = TSP_local_search(N, eld, t)
            end_time = time.time()
            f.write(input_file[i] + ": " + str(end_time - start_time) + ' (s)\n')

            with open(base_path_output + '/' + output_file[i], 'r') as file:
                num_nodes = int(file.readline())
                list_nodes = list(map(int, file.readline().split()))
                time_visit = {}
                time_visit[0] = 0
                # list_nodes = [0] + list_nodes
                d = [0] + [eld[i][2] for i in range(len(eld))]
                e = [0] + [eld[i][0] for i in range(len(eld))]
                for k in range(1, len(list_nodes)):
                    time_visit[list_nodes[k]] = max(time_visit[list_nodes[k-1]] + t[list_nodes[k-1]][list_nodes[k]] + d[list_nodes[k-1]], e[list_nodes[k]])
                testcaseAns = time_visit[list_nodes[num_nodes]] + t[list_nodes[num_nodes]][0] + d[list_nodes[num_nodes]]

            if ans == testcaseAns:
                print('\n Same, ', "testcaseAns = ", testcaseAns, "ans = ", ans)
            elif ans < testcaseAns:
                print('\n Better, ', "testcaseAns = ", testcaseAns, "ans = ", ans)    
            else:
                print('\n Worse, ', "testcaseAns = ", testcaseAns, "ans = ", ans)

if __name__ == '__main__':
    
    # compare ans and compute time
    compare_ans_and_compute_time()