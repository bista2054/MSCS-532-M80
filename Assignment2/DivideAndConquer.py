import random
import time
import tracemalloc
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10 ** 6)


# -------------------------------
# Quick Sort Implementation (In-place)
# -------------------------------
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

    return arr


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# -------------------------------
# Merge Sort Implementation
# -------------------------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# -------------------------------
# Benchmarking Function
# -------------------------------
def benchmark(algorithm, data):
    data_copy = data.copy()
    tracemalloc.start()
    start_time = time.time()

    if algorithm == "Quick Sort":
        result = quick_sort(data_copy)
    else:
        result = merge_sort(data_copy)

    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, peak_mem / 1024  # KB


# -------------------------------
# Dataset Generation
# -------------------------------
def generate_dataset(size, dataset_type='random'):
    if dataset_type == 'sorted':
        return list(range(size))
    elif dataset_type == 'reverse_sorted':
        return list(range(size, 0, -1))
    elif dataset_type == 'random':
        return random.sample(range(size * 10), size)
    else:
        raise ValueError("Invalid dataset type")


# -------------------------------
# Performance Visualization
# -------------------------------
def plot_performance(results, sizes, metric='time'):
    algorithms = list(results.keys())
    dataset_types = list(results[algorithms[0]].keys())

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f'Sorting Algorithm Performance ({metric.capitalize()})', fontsize=16)

    for i, dtype in enumerate(dataset_types):
        for algo in algorithms:
            axes[i].plot(sizes, results[algo][dtype], marker='o', label=algo)
        axes[i].set_title(f'{dtype.capitalize()} Data')
        axes[i].set_xlabel('Input Size')
        axes[i].set_ylabel('Time (s)' if metric == 'time' else 'Memory (KB)')
        axes[i].grid(True, linestyle='--', alpha=0.7)
        axes[i].legend()

    plt.tight_layout()
    plt.show()


# -------------------------------
# Main Comparison
# -------------------------------
if __name__ == "__main__":
    sizes = [100, 500, 1000, 2000, 5000]
    dataset_types = ['random', 'sorted', 'reverse_sorted']
    algorithms = ['Quick Sort', 'Merge Sort']

    time_results = {algo: {dtype: [] for dtype in dataset_types} for algo in algorithms}
    memory_results = {algo: {dtype: [] for dtype in dataset_types} for algo in algorithms}

    print("Starting performance comparison...\n" + "=" * 60)

    for size in sizes:
        print(f"\nArray size: {size}\n" + "-" * 30)
        for dtype in dataset_types:
            dataset = generate_dataset(size, dtype)
            print(f"{dtype.capitalize():15s}", end=" ")

            for algo in algorithms:
                try:
                    time_taken, memory_used = benchmark(algo, dataset)
                except RecursionError:
                    time_taken, memory_used = float('inf'), float('inf')
                    print(f"{algo}: RecursionError!", end=" | ")
                    continue

                time_results[algo][dtype].append(time_taken)
                memory_results[algo][dtype].append(memory_used)
                print(f"{algo}: {time_taken:.6f}s/{memory_used:.2f}KB", end=" | ")
            print()

    # Plotting
    plot_performance(time_results, sizes, 'time')
    plot_performance(memory_results, sizes, 'memory')

    # Summary Table
    print("\nPerformance Summary (Size: 10000)")
    print("=" * 60)
    print(f"{'Algorithm':<12} | {'Dataset':<15} | {'Time (s)':<10} | {'Memory (KB)':<12}")
    print("-" * 60)
    for dtype in dataset_types:
        for algo in algorithms:
            time_val = time_results[algo][dtype][-1]
            mem_val = memory_results[algo][dtype][-1]
            print(f"{algo:<12} | {dtype:<15} | {time_val:<10.6f} | {mem_val:<12.2f}")
