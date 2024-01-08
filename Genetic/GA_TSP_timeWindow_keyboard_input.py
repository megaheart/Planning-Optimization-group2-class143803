import random
import matplotlib.pyplot as plt

def fitness(route, e, l, d, t):
    time = 0
    k = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i+1]
        travel_time = t[a][b]
        time = max(time + travel_time + d.get(b, 0), e.get(b, 0) )
        if (time > l.get(b,0)):
            k += 1
    s = sum([t[0][i] for i in range(len(route)-1)])
    return k*s + time 

# def fitness(route, e, l, d, t):
#     time = 0
#     k = 0
#     for i in range(len(route) - 1):
#         a, b = route[i], route[i+1]
#         travel_time = t[a][b]
#         time += t[a][b]
#     return time

def check(route, e, l, d, t):
    time = 0
    total_time = 0
    k = 0
    q = 0
    check_time = 0
    for i in range(len(route) - 1):
        a, b = route[i], route[i+1]
        # print (f"check location {a} and {b}")
        travel_time = t[a][b]
        check_time += t[a][b]
        time = max(time + travel_time + d.get(b, 0), e.get(b, 0))
        # print(f"time to go to {b}: {time}")
        if (time > l.get(b,0)):
            k += 1
            if k == 1:
                q = i+1
        total_time += time - e.get(b, 0) + d.get(b, 0)
        # print(f"total time: {total_time}")
    return time, check_time, k-1, q

def stuck(route, e, l, d, t):
    time = 0
    k = 0
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

def crossover(parent1, parent2):
    cut = random.randint(1, len(parent1) - 1)
    end_cut = random.randint(cut,len(parent1)-1)
    if random.random() < 0.3:
        cut1 = stuck([0]+parent1+[0],e,l,d,t) - 1
        cut2 = stuck([0]+parent2+[0],e,l,d,t) - 1
        if cut1 == len(parent1):
            cut1 = cut
        if cut2 == len(parent2):
            cut2 = cut
        end_cut = random.randint(max(cut1,cut2), len(parent1)-1)
        # child1 = parent1[:cut1] + [x for x in parent2 if x not in parent1[:cut1]]
        # child2 = parent2[:cut2] + [x for x in parent1 if x not in parent2[:cut2]]
        child1 = parent1[:cut1] + [x for x in parent2 if x in parent1[cut1:end_cut]] + parent1[end_cut:]
        child2 = parent2[:cut2] + [x for x in parent1 if x in parent2[cut2:end_cut]] + parent2[end_cut:]
    else:
        # child1 = parent1[:cut] + [x for x in parent2 if x not in parent1[:cut]]
        # child2 = parent2[:cut] + [x for x in parent1 if x not in parent2[:cut]]
        child1 = parent1[:cut] + [x for x in parent2 if x in parent1[cut:end_cut]] + parent1[end_cut:]
        child2 = parent2[:cut] + [x for x in parent1 if x in parent2[cut:end_cut]] + parent2[end_cut:]
    return child1, child2

# def crossover(parent1, parent2):
#     cut = random.randint(1, len(parent1) - 1)
#     cut = stuck(parent1,e,l,d,t)
#     child1 = parent1[:cut] + [x for x in parent2 if x not in parent1[:cut]]
#     child2 = parent2[:cut] + [x for x in parent1 if x not in parent2[:cut]]
#     return child1, child2


# def mutate(route):
#     i, j = random.sample(range(len(route)), 2)
#     route[i], route[j] = route[j], route[i]

def mutate(route):
    i, j = sorted(random.sample(range(len(route)), 2))
    route[i:j+1] = reversed(route[i:j+1])


N = int(input())
e, l, d = {}, {}, {}
t = []

e[0] = l[0] = d[0] = 0

for i in range(1, N+1):
    e[i], l[i], d[i] = map(int, input().split())

for _ in range(N+1):
    t.append(list(map(int, input().split())))


# e, l, d = {}, {}, {}
# t = []
# with open('testcase/input/N500.txt', 'r') as file:
#     N = int(file.readline().strip())

#     for i in range(1, N + 1):
#         e[i], l[i], d[i] = map(int, file.readline().strip().split())

#     for _ in range(N + 1):
#         t.append(list(map(int, file.readline().strip().split())))


def is_in_population(individual, population):
    return individual in population

def ga():
    population = [random.sample(range(1, N + 1), N) for _ in range(1000)]
    # elements = list(range(1,N+1))
    # sorted_elements = sorted(elements, key=lambda x: l.get(x,0))
    # population.append(sorted_elements)
    best_fitness_each_generation = []
    best_res = 999999999
    slide = min(int(N/2), 30)
    end = min (N,60)
    for generation in range(2000):
        population.sort(key=lambda route: fitness([0] + route + [0], e, l, d, t))
        best_fitness_each_generation.append(fitness([0] + population[0] + [0], e, l, d, t))
        if best_fitness_each_generation[generation]<best_res:
            best_res = best_fitness_each_generation[generation]
            sol = population[0]
        new_population = population[:end]
        if generation> 25:
            if best_res-best_fitness_each_generation[generation-25] > -1:
                return sol
        while len(new_population) < 2*end:
            parent1 = random.choices(population[:slide], k=1)[0]
            parent2 = random.choices(population[slide:end], k=1)[0]
            # parents = random.choices(population[:N],k=4)
            # sorted_parents = parents.sort(key=lambda route: fitness([0] + route + [0], e, l, d, t))
            # parent1 = sorted_parents[0]
            # parent2 = sorted_parents[1]
            child1, child2 = crossover(parent1, parent2)
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
    # best_route = population[0]
    return sol

best_route = ga()
print(N)
print(" ".join(map(str, best_route)))
print(check([0] + best_route + [0],e,l,d,t))

# print(check([0] + real_route + [0],e,l,d,t))
