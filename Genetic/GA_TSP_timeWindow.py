import random

def fitness(route, e, l, d, t):
    time = 0
    total_time = 0
    k = 0
    real_time = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i+1]
        travel_time = t[a][b]
        time = max(time + travel_time + d.get(b, 0), e.get(b, 0) )
        real_time = real_time + travel_time + d.get(b,0)
        if (time > l.get(b,0)):
            k += 1
        total_time += max(0,time - l.get(b,0))
    s = sum([t[0][i] for i in range(len(route)-1)])/len(route)
    return k*s + total_time + time

def check(route, e, l, d, t):
    time = 0
    total_time = 0
    k = 0
    q = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i+1]
        # print (f"check location {a} and {b}")
        travel_time = t[a][b]
        time = max(time + travel_time + d.get(b, 0), e.get(b, 0))
        # print(f"time to go to {b}: {time}")
        if (time > l.get(b,0)):
            k += 1
            if k == 1:
                q = i+1
        total_time += time - e.get(b, 0) + d.get(b, 0)
        # print(f"total time: {total_time}")
    return total_time, time, k, q

def stuck(route, e, l, d, t):
    time = 0
    total_time = 0
    k = 0
    q = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i+1]
        # print (f"check location {a} and {b}")
        travel_time = t[a][b]
        time = max(time + travel_time + d.get(b, 0), e.get(b, 0))
        # print(f"time to go to {b}: {time}")
        if (time > l.get(b,0)):
            k += 1
            if k == 1:
                return i+1
    return len(route)

def crossover(parent1, parent2,generation):
    cut = random.randint(1, len(parent1) - 1)
    if random.random() < 300/(generation+1):
        cut1 = stuck(parent1,e,l,d,t) - 1
        cut2 = stuck(parent2,e,l,d,t) - 1
        child1 = parent1[:cut1] + [x for x in parent2 if x not in parent1[:cut1]]
        child2 = parent2[:cut2] + [x for x in parent1 if x not in parent2[:cut2]]
    else:
        child1 = parent1[:cut] + [x for x in parent2 if x not in parent1[:cut]]
        child2 = parent2[:cut] + [x for x in parent1 if x not in parent2[:cut]]
    return child1, child2

# def crossover(parent1, parent2):
#     cut = random.randint(1, len(parent1) - 1)
#     cut = stuck(parent1,e,l,d,t)
#     child1 = parent1[:cut] + [x for x in parent2 if x not in parent1[:cut]]
#     child2 = parent2[:cut] + [x for x in parent1 if x not in parent2[:cut]]
#     return child1, child2


def mutate(route):
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]

# N = int(input())
# e, l, d = {}, {}, {}
# t = []

# e[0] = l[0] = d[0] = 0

# for i in range(1, N+1):
#     e[i], l[i], d[i] = map(int, input().split())

# for _ in range(N+1):
#     t.append(list(map(int, input().split())))


e, l, d = {}, {}, {}
t = []
with open('testcase/input/N10.txt', 'r') as file:
    N = int(file.readline().strip())

    for i in range(1, N + 1):
        e[i], l[i], d[i] = map(int, file.readline().strip().split())

    for _ in range(N + 1):
        t.append(list(map(int, file.readline().strip().split())))

def is_in_population(individual, population):
    return individual in population

population = [random.sample(range(1, N+1), N) for _ in range(1000)]
best_fitness_each_generation = []

for generation in range(2000):
    population.sort(key=lambda route: fitness([0] + route + [0], e, l, d, t))
    best_fitness_each_generation.append(fitness([0] + population[0] + [0], e, l, d, t))
    new_population = population[:20]

    while len(new_population) < 50:
        # parent1 = random.choices(population[:50], k=1)[0]
        # parent2 = random.choices(population[51:100], k=1)[0]
        parent1, parent2 = random.choices(population[:20],k=2)
        child1, child2 = crossover(parent1, parent2,generation)
        if random.random() < 0.1:
            mutate(child1)
        if random.random() < 0.1:
            mutate(child2)
        # new_population += [child1, child2]
        if not is_in_population(child1, new_population):
            new_population.append(child1)
        if not is_in_population(child2, new_population):
            new_population.append(child2)
    population = new_population

best_route = population[0]
print(N)
print(" ".join(map(str, best_route)))
print(check([0] + best_route + [0],e,l,d,t))
#
# plt.plot(best_fitness_each_generation)
# plt.xlabel('Generation')
# plt.ylabel('Best Fitness')
# plt.title('Best Fitness over Generations')
# plt.show()

# print(check([0] + real_route + [0],e,l,d,t))
