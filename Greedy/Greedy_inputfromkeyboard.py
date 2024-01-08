import time

def GreedyTimeClose(N, l):
    # Create a sorted list of locations based on their closing times
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
    # Calculate the earliest time to arrive at each location
    M = [0] * (N + 1)
    for i in range(1, len(route)):  
        if route[i] < N + 1 and route[i - 1] < N + 1:
            M[route[i]] = max(e[route[i]], M[route[i - 1]] + C[route[i - 1]][route[i]])
    return M

def oneOptChange(i, j, route):
    # Modify the route by reordering one location
    temp = route[i]
    newRoute = route[:j] + [temp] + route[j:i] + route[i+1:]
    return newRoute

def greedy(N, e, l, C):
    # Greedy algorithm to find an initial feasible route
    iterSort = GreedyTimeClose(N, l)
    newRoute = [0]
    visited = [False] * (N + 1)

    for i in range(1, N + 1):
        nextCity = iterSort[i]
        if visited[nextCity]:
            continue
        minCostOneStep = l[nextCity]
        selectCity = nextCity
        selectTime = max(e[nextCity], M_calculate(newRoute, N, e, C)[-1] + C[newRoute[-1]][nextCity])

        for j in range(1, N + 1):
            if not visited[j] and j != nextCity:
                timeCome = max(e[j], M_calculate(newRoute, N, e, C)[-1] + C[newRoute[-1]][j])
                if timeCome < minCostOneStep - C[j][nextCity]:
                    minCostOneStep = timeCome + C[j][nextCity]
                    selectCity = j
                    selectTime = timeCome
        
        if selectCity != nextCity:
            jChange = iterSort.index(selectCity)
            iterSort = oneOptChange(jChange, i, iterSort)
            nextCity = selectCity

        newRoute.append(nextCity)
        visited[nextCity] = True
        timeVisit = M_calculate(newRoute, N, e, C)
        if any(timeVisit[j] > l[j] for j in newRoute[1:]):
            return None

    return newRoute

if __name__ == "__main__":
    N = int(input())
    e = [0] * (N + 1) 
    l = [0] * (N + 1) 
    d = [0] * (N + 1) 
    t = [[0] * (N + 1) for _ in range(N + 1)] 
    C = [[0] * (N + 1) for _ in range(N + 1)]
    
    for i in range(1, N+1):
        e[i], l[i], d[i] = map(int, input().split())

    for i in range(N + 1):
        t[i] = list(map(int, input().split()))

    for i in range(N + 1):
        for j in range(N + 1):
            C[i][j] = t[i][j] + d[i]
              
    route = greedy(N, e, l, C)
    print(N)
    if route is not None:
        print(" ".join(map(str, route[1:])))
