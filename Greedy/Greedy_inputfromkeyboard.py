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
    for i in range(1, len(route)):  
        if route[i] < N + 1 and route[i - 1] < N + 1:
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

    for i in range(1, N + 1):
        orderTime[iterSort[i]] = i

    for i in range(1, N + 1):
        nextCity = iterSort[i]
        if visited[nextCity]:
            continue

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
              
    route = greedy(N, e, l, d, t, C)
    print(N)
    if route is not None:
        print(" ".join(map(str, route[1:])))
