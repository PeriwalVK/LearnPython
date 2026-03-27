# ============================
# Python Frozenset Tutorial
# ============================

print("=== Frozenset Basics ===")

# Creating a frozenset from a list
fs0 = frozenset([1, 2, 3])
fs1 = frozenset([3, 2, 1, 3, 2])
# Both are same
print(f"fs0 == fs1 : {fs0 == fs1}")  # True
print(f"hash(fs0) == hash(fs1): {hash(fs0) == hash(fs1)}")  # True

# Creating a frozenset from a tuple
fs2 = frozenset((3, 4, 5))
print("fs2:", fs2)  # Output: frozenset({3, 4, 5})

# Creating a frozenset from a set
fs3 = frozenset({5, 6, 7})
print("fs3:", fs3)  # Output: frozenset({5, 6, 7})

# ============================
# Frozenset Operations
# ============================

fs_a = frozenset([1, 2, 3])
fs_b = frozenset([3, 4, 5])

# Union
print("Union:", fs_a | fs_b)  # frozenset({1, 2, 3, 4, 5})

# Intersection
print("Intersection:", fs_a & fs_b)  # frozenset({3})

# Difference
print("Difference:", fs_a - fs_b)  # frozenset({1, 2})

# Symmetric Difference
print("Symmetric Difference:", fs_a ^ fs_b)  # frozenset({1, 2, 4, 5})

# ============================
# Membership Testing (O(1))
# ============================
print("Is 2 in fs_a?", 2 in fs_a)  # True
print("Is 5 in fs_a?", 5 in fs_a)  # False

# ============================
# Using frozenset as dictionary keys
# ============================
d = {frozenset([1, 2]): "Pair 1-2", frozenset([3, 4]): "Pair 3-4"}
print("Dictionary with frozenset keys:", d)

# ============================
# Using frozenset inside another set
# ============================
set_of_sets = {frozenset([1, 2]), frozenset([3, 4])}
print("Set of frozensets:", set_of_sets)

# ============================
# Immutability demonstration
# ============================
try:
    fs_a.add(10)  # ❌ AttributeError
except AttributeError as e:
    print("Cannot modify frozenset:", e)
