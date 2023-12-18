from ortools.sat.python import cp_model

# Bien: X: x[i][j] = 1 neu di tu thanh pho i den thanh pho j, 0 neu nguoc lai
#       M: M[i] = thoi gian den thanh pho i
#       w: w[i] = thoi gian cho tai thanh pho i
# Rang buoc:
#       - Moi thanh pho chi duoc di qua 1 lan
#       - Thoi gian den thanh pho i phai nam trong khoang [e[i], l[i]]
#       - Thoi gian den thanh pho i = tg den thanh pho j + tg giao hang tai j + tg di tu j den i + tg cho tai j
# Muc tieu: Minimize tong thoi gian di chuyen giua cac thanh pho
# -----------------------------------------------

# NOTE: Chu trinh con duoc loai bo: thoi gian den thanh pho i = thoi gian den thanh pho j + thoi gian di tu j den i

e = {}  # thoi gian som nhat de den thanh pho i
l = {}  # thoi gian tre nhat de den thanh pho i
d = {}  # thoi gian mat de giao hang tai thanh pho i
x = {}  # x[i,j] = 1 if i -> j else 0
M = {}  # M[i] = thoi gian giao hang tai thanh pho i
w = {}  # w[i] = thoi gian cho tai thanh pho i
time_matrix = {}  # time_matrix[i][j] = thoi gian di tu thanh pho i den thanh pho j

# Input
num_nodes = int(input())

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

# Thoi gian den thanh pho i = thoi gian den thanh pho j + thoi gian di tu j den i
for i in range(num_nodes + 1):
    for j in range(num_nodes + 1):
        if i != j and j != 0:
            model.Add(M[j] >= M[i] + d[i] + time_matrix[i, j] + w[j] + (x[i, j] - 1) * 1000000000)
            model.Add(M[j] <= M[i] + d[i] + time_matrix[i, j] + w[j] + (1 - x[i, j]) * 1000000000)

# Muc tieu: Minimize tong thoi gian di het cac thanh pho
model.Minimize(M[num_nodes] + d[num_nodes] + time_matrix[num_nodes, 0])

# Solve model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# In ket qua
print(num_nodes)

if status == cp_model.OPTIMAL:
    # In gia tri toi uu
    # print(solver.ObjectiveValue())

    # In hanh trinh toi uu
    current_city = 0
    while 1:
        for i in range(num_nodes + 1):
            if solver.Value(x[current_city, i]) == 1:
                if i != 0:
                    print(i, end=' ')
                current_city = i
                break
        if current_city == 0:
            break
else:
    print("No solution found.")