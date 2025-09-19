import random
import time
import sys

sys.setrecursionlimit(10 ** 6) 


# -------------------------------
# Quick Sort Implementation
# -------------------------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  # Choose middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


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
# Test and Compare Performance
# -------------------------------
if __name__ == "__main__":
    sizes = [1000, 5000, 10000]
    for n in sizes:
        print(f"\nArray size: {n}")

        # Random data
        arr = random.sample(range(n * 10), n)

        for algo in ["Quick Sort", "Merge Sort"]:
            data = arr.copy()
            start = time.time()
            if algo == "Quick Sort":
                sorted_arr = quick_sort(data)
            else:
                sorted_arr = merge_sort(data)
            end = time.time()
            print(f"{algo} took {end - start:.6f} seconds")
            
