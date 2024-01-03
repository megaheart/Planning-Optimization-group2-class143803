from itertools import permutations
import time

def calculate_travel_time(sequence, e, l, d, t):
    current_time = 0
    last_location = 0
    for customer in sequence:
        travel_time = t[last_location][customer]
        current_time += travel_time
        if current_time < e[customer - 1]:
            current_time = e[customer - 1]
        if current_time > l[customer - 1]:
            return float('inf')
        current_time += d[customer - 1]
        last_location = customer
    current_time += t[last_location][0]
    return current_time

def find_optimal_delivery_sequence(N, e, l, d, t):
    shortest_time = float('inf')
    optimal_sequence = None
    for sequence in permutations(range(1, N + 1)):
        travel_time = calculate_travel_time(sequence, e, l, d, t)
        if travel_time < shortest_time:
            shortest_time = travel_time
            optimal_sequence = sequence
    return optimal_sequence, shortest_time

N = int(input())
e, l, d = [], [], []
for _ in range(N):
    ei, li, di = map(int, input().split())
    e.append(ei)
    l.append(li)
    d.append(di)
t = []
for _ in range(N + 1):
    t.append(list(map(int, input().split())))

start_time = time.time()
optimal_sequence, shortest_time = find_optimal_delivery_sequence(N, e, l, d, t)
end_time = time.time()

if optimal_sequence:
    print(N)
    print(' '.join(map(str, optimal_sequence)))
else:
    print("No valid delivery sequence found within the given time windows.")
print(f"Execution time: {end_time - start_time:.3f} seconds")
