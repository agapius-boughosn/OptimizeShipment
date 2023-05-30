# Optimize Shipments
This code aims to optimize a shipment problem using different methods: recursion, memoization, and the OR Tools library. Given a set of items with values and volumes, the script aims to select a subset of items that maximizes the total value while not exceeding a given capacity.

## Methods
The main script `main.py` includes the different methods for solving the problem. The included methods are:
* `optimize_shipment(capacity, values, volumes, n)`: Solves the problem using a recursive approach. This method has an exponential time complexity of O(2^n) and is not efficient for large problem sizes.
* `optimize_shipment_dp(capacity, values, volumes, n, memo)`: Solves the problem using a memoized recursive approach. This method has a time complexity of O(n) and provides significant performance improvements over the simple recursive method.
* `optimize_shipment_or_tools(capacity, values, volumes, num_items)`: Solves the problem using the OR Tools library.
* `optimize_shipment_greedy(capacity, values, volumes)`: Solves the problem using a greedy approach with a time perfomance comparable to the OR tools library.

## Functioning
The implemented code follows the below steps:

1. Imports the required libraries:
```
import time
import random
import numpy as np 
from ortools.algorithms import pywrapknapsack_solver
```

2. Defines the problem inputs:
* `capacity`: The maximum capacity.
* `values`: A list of item values.
* `volumes`: A list of item volumes.

3. Calls the desired method:
* Recursive method:
```
max_value, items = optimize_shipment(capacity, values, volumes, num_items)
```

* Memoization method:
```
memo = [[-1] * (capacity + 1) for _ in range(num_items + 1)]
max_value, items = optimize_shipment_dp(capacity, values, volumes, num_items, memo)
```

* OR Tools method:
```
max_value, items = optimize_shipment_or_tools(capacity, values, volumes, num_items)
```

* Greedy method:
```
max_value, items = optimize_shipment_greedy(capacity, values, volumes)
```

4. Prints the results:
```
print("Maximum total value:", max_value)
print("Items to include:", items)
```

## Usage
The script provides an example usage with a small problem size and a larger problem size for comparison. You can uncomment the original problem values and run the script to see the results.

## Dependencies
The project has the following dependencies:
* Python 3.x
* OR Tools library (install using `pip install ortools`)