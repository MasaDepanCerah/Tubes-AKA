import time

from coinChange import (
    coin_change_iterative,
    coin_change_recursive,
    coin_change_iterative_early,
    coin_change_recursive_optimized
)


def measure(func, k, n):
    start = time.perf_counter()
    result = func(k, n)
    end = time.perf_counter()
    return result, end - start


def run_single(k, n, mode):
    start = time.perf_counter()

    if mode == "iterative":
        result = coin_change_iterative(k, n)

    if mode == "recursive":
        result = coin_change_recursive(k, n)

    if mode == "iterative_opt":
        result = coin_change_iterative_early(k, n)

    if mode == "recursive_opt":
        result = coin_change_recursive_optimized(k, n)
    
    end = time.perf_counter()
    exec_time = (end - start) * 1000  # ms

    return result, exec_time


def run_graph(k, max_n, flags):
    step = max_n // 10
    if step == 0:
        step = 1

    data = {}

    algorithms = {
        "Iterative": coin_change_iterative,
        "Recursive": coin_change_recursive,
        #"Iterative (Optimized)": coin_change_iterative_early,
        #"Recursive (Optimized)": coin_change_recursive_optimized
    }

    for name in algorithms:
        if not flags[name]:
            continue

        n_values = []
        t_values = []

        for n in range(step, max_n + 1, step):
            _, t = measure(algorithms[name], k, n)
            n_values.append(n)
            t_values.append(t)

        data[name] = {
            "n": n_values,
            "time": t_values
        }

    return data
