"""
============================================================
                SORTING ALGORITHMS - COMPLETE SCRIPT
============================================================

Algorithms Included:
1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Merge Sort
5. Quick Sort
6. Heap Sort
7. Counting Sort
8. Radix Sort
9. Bucket Sort
10. Python Built-in Sort (Timsort)

------------------------------------------------------------
COMPLEXITY LEGEND:
n = number of elements
k = range of elements
d = number of digits (for radix sort)
------------------------------------------------------------
"""

# TODO: add proper comments to get a visual feel of what this algo does

import heapq


# ============================================================
# 1. BUBBLE SORT
# Time Complexity:
#   Best: O(n)
#   Avg:  O(n^2)
#   Worst:O(n^2)
# Space: O(1)
# Stable: Yes
# ============================================================
def bubble_sort(arr):
    arr = arr.copy()
    """
    visualise density difference
    wherever you find max element just before min, just swap them,
    max elements will come up like a bubble
    """
    n = len(arr)

    for end in range(n - 1, 0, -1):
        swapped = False
        for j in range(1, end + 1):
            if arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                swapped = True

        if not swapped:  # already sorted, no need to continue
            break

    return arr


# ============================================================
# 2. SELECTION SORT
# Time Complexity:
#   Best/Avg/Worst: O(n^2)
# Space: O(1)
# Stable: No
# ============================================================
def selection_sort(arr):
    """
    "Select the correct element for this seat"

        leftmost seat is selected for next min,
        now search for next min in remaining array,
        in the end, swap that min with target seat
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):  # target seat for next min element
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


# ============================================================
# 3. INSERTION SORT
# Time Complexity:
#   Best: O(n)
#   Avg/Worst: O(n^2)
# Space: O(1)
# Stable: Yes
# ============================================================
def insertion_sort(arr):
    """
    “Maintain a sorted region and grow it.”
    "Keep things sorted as you go."
    "Just like you sort playing cards in your hands, you INSERT the card to its right place"

        Keep Left side is always sorted
        Insert next element into correct position
        faster if already partially sorted.

    """
    arr = arr.copy()

    for nxt in range(1, len(arr)):
        key = arr[nxt]
        j = nxt - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


# ============================================================
# 4. MERGE SORT
# Time Complexity:
#   Best/Avg/Worst: O(n log n)
# Space: O(n)
# Stable: Yes
# ============================================================
def merge_sort(arr):
    # arr = arr.copy() # not required
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    m = len(left)
    n = len(right)
    i = j = 0

    while i < m and j < n:
        if left[i] <= right[j]:  # equal condition makes it stable
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < m:
        result.append(left[i])
        i += 1

    while j < n:
        result.append(right[j])
        j += 1

    return result


# ============================================================
# 5. QUICK SORT
# Time Complexity:
#   Best/Avg: O(n log n)
#   Worst: O(n^2)
# Space:
#   Best: O(log n) if balanced recursion tree
#   Worst: O(n) if scewed recursion tree
# Stable: No
# ============================================================


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


# partition function
def partition(arr, low, high):

    # chose last element as pivot,
    # finally ye jaha jayega, that will be partition point
    pivot = arr[high]

    # jb bhi pivot se smaller element mile,
    # i+=1 krke seat banao and udhar bitha do, yaani swap krdo
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:  # found smaller
            i += 1  # made seat
            swap(arr, i, j)  # swap krke bitha diya

    # ab last me pivot ko bhi bitha diya seat banake,
    # and seat number return krdi
    swap(arr, i + 1, high)
    return i + 1


def QS(arr, low, high):

    if low < high:
        # pi is the partition return index of pivot
        # did something with this array such that elemebnts on the left of pivot are smaller
        # and elements on the right are greater or equal
        pi = partition(arr, low, high)

        QS(arr, low, pi - 1)
        QS(arr, pi + 1, high)
        # pivot was on its right place
        # array is sorted now


def quick_sort(arr):
    """
    kuchh game krke array ko partition kro and ek pivot nikalo
    such that left me saare chhote elt ho and right me saare bade


        Pick last element and assume it pivot
        now keep swaping all lesser elements to the left
        in the end swap pivot to next seat
        now everything smaller on left, larger on right,
        so return pivot's current position

        Now pivot to apni shi position pr hai -> so Recursively sort left and right parts


    It reduces problem size dramatically after partition.
    “If I place one element correctly, the rest becomes easier.”
    It wins because partitioning is powerful.
    """

    arr = arr.copy()

    if len(arr) <= 1:
        return arr

    QS(arr, 0, len(arr) - 1)

    return arr


# ============================================================
# 6. HEAP SORT
# Time Complexity:
#   Best/Avg/Worst: O(n log n)
# Space: O(1) extra (in-place heapify)
# Stable: No
# ============================================================


# def heap_sort(arr):
#     arr = arr.copy()
#     heapq.heapify(arr)  # O(n)
#     return [heapq.heappop(arr) for _ in range(len(arr))]


# To heapify a subtree rooted with node i and having n elements
# assuming its child sub-trees are already heapified
def heapify(arr, n, i):

    # Initialize largest as root
    largest = i

    # left index = 2*i + 1
    l = 2 * i + 1

    # right index = 2*i + 2
    r = 2 * i + 2

    # If left child is larger than root
    if l < n and arr[l] > arr[largest]:
        largest = l

    # If right child is larger than largest so far
    if r < n and arr[r] > arr[largest]:
        largest = r

    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        # Recursively heapify the affected sub-tree
        heapify(arr, n, largest)


# Main function to do heap sort
def heap_sort(arr):
    arr = arr.copy()
    n = len(arr)

    # Heapifying full array.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract an element from heap
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]

        # Call max heapify on the reduced heap
        heapify(arr, i, 0)

    return arr


# ============================================================
# 7. COUNTING SORT (for non-negative integers)
#
# Time Complexity: O(n + k)
# Space: O(k)
#     where k is the max element present in array
#
# Stable: Yes (if implemented carefully)
# ============================================================
def counting_sort(arr):
    """
    "Count instead of compare.”
    max element nikalo and 0 to max tk ka count record krlo
    fir 0 to max tk loop krke count times i ko append krte rho result me

    “If values are limited, sorting is just counting.”

    This is why it's O(n + k).

    agar max element bada ho gya to unoptiml because bada loop lgega
    """
    arr = arr.copy()  # not required

    if not arr:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    result = []
    for i, freq in enumerate(count):
        for _ in range(freq):
            result.append(i)
        # result.extend([i] * freq)

    return result


# ============================================================
# 8. RADIX SORT (for non-negative integers)
# TODO: FIX
# Time Complexity: O(d(n + k))
# Space: O(n + k)
# Stable: Yes
# ============================================================
def counting_sort_by_digit(arr, exp):
    """
    Put elements into buckets based on range, then sort each bucket.

    Core Idea

    Divide range into buckets

    Sort buckets individually

    Merge

    Deep insight
    It works best when data is uniformly distributed.

    It believes:

    “If I reduce problem density, sorting becomes easy.”

    """
    arr = arr.copy()

    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    arr = arr.copy()
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr


# ============================================================
# 9. BUCKET SORT (for floats in range [0,1))
# Time Complexity:
#   Avg: O(n + k)
#   Worst: O(n^2)
# Space: O(n)
# ============================================================
def bucket_sort(arr):
    """
    Divide range into n buckets
    Sort buckets individually
    then Merge

    works best when data is uniformly distributed.
    """
    # arr = arr.copy() # not required

    n = len(arr)

    min_ = min(arr)
    max_ = max(arr)

    if min_ == max_:
        return arr

    max_ += 1  # just to avoid index = n case

    # create n empty buckets: Each bucket represents a small interval
    buckets = [[] for _ in range(n)]

    for num in arr:
        index = int(n * (num - min_) / (max_ - min_))
        buckets[index].append(num)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))  # using Timsort

    return sorted_arr


# ============================================================
# 10. PYTHON BUILT-IN SORT (TIMSORT)
# Time Complexity:
#   Worst: O(n log n)
# Space: O(n)
# Stable: Yes
# ============================================================
def python_sort(arr):
    """
    Real-world data is rarely random.
    Detect natural sorted runs
    Use insertion sort on small runs
    Merge them efficiently

    That's why it's used in Python and Java.
    """
    return sorted(arr)


# ============================================================
# TESTING ALL SORTS
# ============================================================
if __name__ == "__main__":
    sample = [5, 2, 9, 1, 5, 6]
    # sample = [3, 4, 2, 5, 7, 1, 2, 3, 9, 2]

    print("Original:", sample)
    print("Bubble:", bubble_sort(sample))
    print("Selection:", selection_sort(sample))
    print("Insertion:", insertion_sort(sample))
    print("Merge:", merge_sort(sample))
    print("Quick:", quick_sort(sample))
    print("Heap:", heap_sort(sample))
    print("Counting:", counting_sort(sample))
    print("Radix:", radix_sort(sample))
    print("Bucket:", bucket_sort(sample))
    print("Built-in:", python_sort(sample))
