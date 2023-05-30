import time
import random
import numpy as np 
from ortools.algorithms import pywrapknapsack_solver

def optimize_shipment_or_tools(capacity, values, volumes, num_items):
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER,
        'Knapsack'
    )

    # Initialize solver
    solver.Init(values, [volumes], [capacity])

    # Solve the problem
    computed_value = solver.Solve()

    # Get the results
    selected_items = []
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            selected_items.append(i)

    return computed_value, selected_items

def optimize_shipment(capacity, values, volumes, n):
    # Base case
    if n == 0 or capacity == 0:
        return 0, []

    # If the volume of the current item exceeds the capacity don't include it
    if volumes[n-1] > capacity:
        return optimize_shipment(capacity, values, volumes, n-1)

    # Recursive case: Consider both cases and return max
    included_value, included_items = optimize_shipment(capacity - volumes[n - 1], values, volumes, n-1)
    included_value += values[n-1]
    included_items = included_items + [n-1]

    excluded_value, excluded_items = optimize_shipment(capacity, values, volumes, n - 1)

    if included_value > excluded_value:
        return included_value, included_items
    else:
        return excluded_value, excluded_items

def optimize_shipment_dp(capacity, values, volumes, n, memo):
    # Check if the result is already memoized (computation already done)
    if memo[n][capacity] != -1:
        return memo[n][capacity]

    # Base case
    if n == 0 or capacity == 0:
        memo[n][capacity] = 0, []
        return 0, []

    # If the volume of the current item exceeds the capacity don't include it
    if volumes[n-1] > capacity:
        memo[n][capacity] = optimize_shipment_dp(capacity, values, volumes, n-1, memo)
        return memo[n][capacity]

    # Recursive case: Consider both cases and return max
    included_value, included_items = optimize_shipment_dp(capacity - volumes[n-1], values, volumes, n - 1, memo)
    included_value += values[n-1]
    included_items = included_items + [n-1]

    excluded_value, excluded_items = optimize_shipment_dp(capacity, values, volumes, n-1, memo)

    # Update memo array to avoid redundant computations in the future
    # And return the higher case
    if included_value > excluded_value:
        memo[n][capacity] = included_value, included_items
        return included_value, included_items
    else:
        memo[n][capacity] = excluded_value, excluded_items
        return excluded_value, excluded_items

def optimize_shipment_greedy(capacity, values, volumes):
   # Calculate value to volume ratio for each item
    value_per_volume = np.array(values) / np.array(volumes)

    # Sort the items based on their value to volume ratio then inverse (result in decreasing order)
    sorted_items = np.argsort(value_per_volume)[::-1]

    total_value = 0
    selected_items = []

    for item in sorted_items:
        if volumes[item] <= capacity:
            # Include the item if it can fit in the truck
            total_value += values[item]
            selected_items.append(item)
            capacity -= volumes[item]

    return total_value, selected_items


# Original problem
#values =  [7, 9, 5, 12, 14, 6, 12]
#volumes = [3, 4, 2, 6, 7, 3, 5]
#num_items = len(volumes)
capacity = 15

# Enlarged problem (to compare methods)
num_items = 50


values = [random.randint(1, 20) for _ in range(num_items)]
volumes = [random.randint(1, 10) for _ in range(num_items)]

# Recursion method (O(2^n))
start_time = time.time()
max_value, items = optimize_shipment(capacity, values, volumes, num_items)
elapsed_time = time.time()-start_time
print("### Recursion method ###")
print("Maximum total value: ", max_value, ", Execution time (s): ", elapsed_time)
print("Items to include:", items, "\n")
# Memoization method (O(n))
memo = [[-1] * (capacity + 1) for _ in range(num_items + 1)]
start_time = time.time()
max_value, items = optimize_shipment_dp(capacity, values, volumes, num_items, memo)
elapsed_time = time.time()-start_time
print("### Memoization method ###")
print("Maximum total value: ", max_value, ", Execution time (s):", elapsed_time)
print("Items to include:", items, "\n")
# OR Tools
start_time = time.time()
max_value, items = optimize_shipment_or_tools(capacity, values, volumes, num_items)
elapsed_time = time.time()-start_time
print("### OR-Tools ###")
print("Maximum total value: ", max_value, ", Execution time (s):", elapsed_time)
print("Items to include:", items, "\n")
# Greedy
start_time = time.time()
max_value, items = optimize_shipment_greedy(capacity, values, volumes)
elapsed_time = time.time()-start_time
print("### Greedy method ###")
print("Maximum total value: ", max_value, ", Execution time (s):", elapsed_time)
print("Items to include:", np.sort(items).tolist(), "\n")

