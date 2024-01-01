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

if __name__ == "__main__":
    #input from keyboard

    N = int(input())
    customers = []
    e = [0] * (N + 1) 
    l = [0] * (N + 1) 
    d = [0] * (N + 1) 
    t = [[0] * (N + 1) for _ in range(N + 1)] 
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(1, N+1):
        e[i], l[i], d[i]  = map(int, input().split())
        customers.append([e, l, d])

    for i in range(N + 1):
            t[i] = list(map(int, input().split()))
            for j in range(N + 1):
                C[i][j] = d[i] + t[i][j]
              
    ans = greedy(N, e, l, d, t, C)
    print(N)
    print(" ".join(map(str, ans[1:])), '\n')
