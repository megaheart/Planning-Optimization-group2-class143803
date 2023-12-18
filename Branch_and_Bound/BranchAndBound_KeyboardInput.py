best_time = 1000000000
best_path = []


def branch_and_bound(num_nodes, e, l, d, w, time_matrix, x, k, current_time):
    global best_time
    global best_path

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
                if current_time < best_time:
                    branch_and_bound(num_nodes, e, l, d, w, time_matrix, x, k + 1, current_time)

            current_time -= d[i]
            current_time -= w[k]
            w[k] = 0
            current_time -= time_matrix[x[k - 1], i]
            x[k] = 0


if __name__ == '__main__':
    num_nodes = int(input())

    e = {}  # thoi gian som nhat de den thanh pho i
    l = {}  # thoi gian tre nhat de den thanh pho i
    d = {}  # thoi gian mat de giao hang tai thanh pho i
    w = [0 for i in range(num_nodes + 1)]  # w[i] = thoi gian cho tai thanh pho i
    x = [0 for i in range(num_nodes + 1)]  # x[i] - thanh pho duoc giao hang thu i
    time_matrix = {}  # time_matrix[i][j] = thoi gian di tu thanh pho i den thanh pho j

    e[0] = 0
    l[0] = 1000000000
    d[0] = 0

    for i in range(1, num_nodes + 1):
        data = input().split(" ")

        e[i] = int(data[0])
        l[i] = int(data[1])
        d[i] = int(data[2])

    for i in range(num_nodes + 1):
        data = input().split(" ")
        for j in range(num_nodes + 1):
            time_matrix[i, j] = int(data[j])

    branch_and_bound(num_nodes, e, l, d, w, time_matrix, x, 1, 0)

    print(num_nodes)
    for i in range(1, num_nodes + 1):
        print(best_path[i], end=" ")
    print(best_time)