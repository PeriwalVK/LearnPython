import bisect

"""
PYTHON BISECT MODULE TUTORIAL
-----------------------------
The 'bisect' module provides support for maintaining a list in sorted order 
without having to sort the list after each insertion. 

It uses the bisection algorithm (Binary Search).

Key Concepts:
1. bisect_left(a, x): Finds the index to insert 'x' in 'a' to maintain order. 
   If 'x' is already present, the insertion point is BEFORE (to the left of) any existing entries.
   
2. bisect_right(a, x): Similar to bisect_left, but if 'x' is present, 
   the insertion point is AFTER (to the right of) any existing entries.
   
3. insort_left(a, x): Actually inserts 'x' into 'a' at the position found by bisect_left.

4. insort_right(a, x): Actually inserts 'x' into 'a' at the position found by bisect_right.

KEY TAKEAWAYS FOR INTERVIEWS
    1. Input list MUST be sorted.
    2. bisect_left is equivalent to C++ std::lower_bound.
    3. bisect_right is equivalent to C++ std::upper_bound.
    4. Used for finding ranges:
    - Items less than x:  data[:bisect_left(data, x)]
    - Items greater than x: data[bisect_right(data, x):]
    - Count of 'x': bisect_right(data, x) - bisect_left(data, x)

Complexity: 
- Search (bisect): O(log n)
- Insertion (insort): O(n) because inserting into a list requires shifting elements.
"""


def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#' * hash_len} {msg} {'#' * hash_len}")
    print("=" * l)


def announce(msg: str):
    """
    A decorator to announce a message before calling a function.
    """

    def _deco(func):
        def wrapper2(*args, **kwargs):
            separator(msg)
            func(*args, **kwargs)

        return wrapper2

    return _deco


# ---------------------------------------------------------
# 1. BASICS: bisect_left vs bisect_right
# ---------------------------------------------------------
@announce("1. BASICS: bisect_left vs bisect_right")
def _1_bisect_left_vs_bisect_right():
    # Pre-requisite: The list MUST be sorted.
    data = [1, 3, 3, 3, 7, 9]
    print(f"Original Sorted List: {data}")

    target = 3

    # bisect_left: Returns index of the FIRST occurrence of target
    idx_left = bisect.bisect_left(data, target)
    print(f"bisect_left({target}): Index {idx_left}")
    # Visualization: [1, *HERE*, 3, 3, 3, 7, 9]

    # bisect_right: Returns index AFTER the LAST occurrence of target
    # Note: bisect.bisect() is an alias for bisect_right
    idx_right = bisect.bisect_right(data, target)
    print(f"bisect_right({target}): Index {idx_right}")
    # Visualization: [1, 3, 3, 3, *HERE*, 7, 9]


# ---------------------------------------------------------
# 2. INSERTION: insort_left vs insort_right
# ---------------------------------------------------------
@announce("2. INSERTION: insort_left vs insort_right")
def _2_insert_left_vs_insert_right():
    grades = [60, 70, 80, 90]
    print(f"Current Grades: {grades}")

    # We want to add a score of 70.
    # insort_left will put it BEFORE the existing 70.
    # Order becomes: 60, (New 70), (Old 70), 80, 90
    bisect.insort_left(grades, 70)
    print(f"After insort_left(70):  {grades}")

    # We want to add a score of 85.
    # insort_right behaves normally for unique values.
    bisect.insort_right(grades, 85)
    print(f"After insort_right(85): {grades}")


# ---------------------------------------------------------
# 3. PRACTICAL USE CASE: Numeric Grading System
# ---------------------------------------------------------
@announce("3. PRACTICAL USE CASE: Numeric Grading System")
def _3_practical_usecase__numeric_grading_system():
    def get_grade(score):
        # Breakpoints must be sorted!
        breakpoints = [60, 70, 80, 90]
        grades = ["F", "D", "C", "B", "A"]

        # bisect_right returns the index where the score fits.
        # Score < 60  -> index 0 -> 'F'
        # 60 <= Score < 70 -> index 1 -> 'D'
        # ...
        # Score >= 90 -> index 4 -> 'A'

        i = bisect.bisect_right(breakpoints, score)
        return grades[i]

    students = [33, 99, 77, 70, 89, 90, 100]
    print(f"Grading Scale: 60(D), 70(C), 80(B), 90(A)")
    for s in students:
        print(f"Score: {s:<3} -> Grade: {get_grade(s)}")


# ---------------------------------------------------------
# 4. PRACTICAL USE CASE: Searching Ranges (Prefix Sum / Weighted Random Choice)
# ---------------------------------------------------------
@announce(
    "4. PRACTICAL USE CASE: Searching Ranges (Prefix Sum / Weighted Random Choice)"
)
def _4_practical_usecase__prefix_sum__weighted_random_choice():
    import random

    # Scenario: We have items with different probabilities (weights)
    items = ["Common", "Uncommon", "Rare", "Legendary"]
    weights = [50, 30, 15, 5]  # 50% chance, 30% chance, etc.

    # Calculate cumulative weights (Prefix Sum)
    # cum_weights = [50, 80, 95, 100]
    import itertools

    cum_weights = list(itertools.accumulate(weights))

    print(f"Items: {items}")
    print(f"Weights: {weights}")
    print(f"Cumulative Weights: {cum_weights}")

    # Simulate 5 random drops
    print("\nSimulating 5 Drops:")
    for _ in range(5):
        # Pick a random number between 1 and 100
        r = random.randint(1, 100)

        # Find where 'r' fits in the cumulative weights
        # If r=40, index=0 (Common)
        # If r=60, index=1 (Uncommon)
        idx = bisect.bisect_left(cum_weights, r)

        print(f"Rolled: {r:<3} -> Found at idx {idx} -> Item: {items[idx]}")


# ---------------------------------------------------------
# 5. KEY TAKEAWAYS FOR INTERVIEWS
# ---------------------------------------------------------
@announce("5. KEY TAKEAWAYS FOR INTERVIEWS")
def _5_key_takeaways_for_interviews():
    print("""
    1. Input list MUST be sorted.
    2. bisect_left is equivalent to C++ std::lower_bound.
    3. bisect_right is equivalent to C++ std::upper_bound.
    4. Used for finding ranges:
    - Items less than x:  data[:bisect_left(data, x)]
    - Items greater than x: data[bisect_right(data, x):]
    - Count of 'x': bisect_right(data, x) - bisect_left(data, x)
    """)


if __name__ == "__main__":
    _1_bisect_left_vs_bisect_right()
    _2_insert_left_vs_insert_right()
    _3_practical_usecase__numeric_grading_system()
    _4_practical_usecase__prefix_sum__weighted_random_choice()
    _5_key_takeaways_for_interviews()

    # print("test")
    print({bisect.bisect_left([1, 3, 3, 3, 7, 9], 10)})
