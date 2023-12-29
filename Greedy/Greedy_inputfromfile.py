import time

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

def M_calculate(route, N, e, C):
    M = [0] * (N + 1)
    for i in range(1, N + 1):
        M[route[i]] = max(e[route[i]], M[route[i - 1]] + C[route[i - 1]][route[i]])
    return M

def cost(route, N, C):
    return sum(C[route[i - 1]][route[i]] for i in range(1, N + 1)) + C[route[N]][0]

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

# Existing imports and functions...
def calculate_total_time(route, t):
    total_time = 0
    for i in range(1, len(route)):
        total_time += t[route[i - 1]][route[i]]
    total_time += t[route[-1]][0]  # Add time to return to the starting point, if needed
    return total_time

def compare_ans_and_compute_time():
    inputFolder = 'testcase/input'
    outputFolder = 'testcase/output'
    timeFile = 'time.txt'
    allFiles = ["N5.txt", "N10.txt", "N100.txt", "N200.txt", "N300.txt", "N500.txt", "N600.txt", "N700.txt", "N900.txt", "N1000.txt"]
    # allFiles=["N5.txt"]
    with open(timeFile, 'w') as f:
        for file_name in allFiles:
            input_file = f"{inputFolder}/{file_name}"
            output_file = f"{outputFolder}/{file_name.replace('.txt', '_output.txt')}"
            customers = []
            t = []
            with open(input_file, 'r') as file:
                N = int(file.readline())
                e = [0]
                l = [0]
                d = [0]
                for k in range(1, N + 1):
                    ek, lk, dk = map(int, file.readline().split())
                    e.append(ek)
                    l.append(lk)
                    d.append(dk)
                    customers.append([ek, lk, dk])

                for _ in range(N + 1):
                    row = list(map(int, file.readline().split()))
                    t.append(row)

            C = [[0] * (N + 1) for _ in range(N + 1)]
            for i in range(N + 1):
                for j in range(N + 1):
                    C[i][j] = d[i] + t[i][j]

            start_time = time.time()
            ans = greedy(N, e, l, d, t, C)
            end_time = time.time()
            f.write(f"{file_name}: {end_time - start_time}\n")
            timeAns = calculate_total_time(ans, t)
            with open(output_file, 'r') as file:
                num_nodes = int(file.readline())
                list_nodes = list(map(int, file.readline().split()))
                time_visit = {}
                time_visit[0] = 0
                myAns=calculate_total_time(list_nodes, t)
            # print(f'\nGreedy Algorithm Route for {file_name}: {ans}')
            # print(f'Expected Output Route for {file_name}: {list_nodes}')            
            print(f'\nGreedy Algorithm Time for {file_name}: {timeAns}')
            print(f'Expected Output Time for {file_name}: {myAns}')           
            if timeAns <= myAns:                                
                print(f'{file_name}: Correct')
            else:
                print(f'{file_name}: Wrong')

# Main execution block
if __name__ == "__main__":
    compare_ans_and_compute_time()