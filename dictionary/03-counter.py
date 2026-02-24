from collections import Counter


c1 = Counter({"a": 5, "b": 3, "c": 2, "e": 5})
c2 = Counter({"a": 2, "b": 4, "d": 1, "e": 5})
c1.subtract(c2)
# Allows zero and negative counts
# original c1 modified
print(c1)  # Counter({'a': 3, 'c': 2, 'e': 0, 'b': -1, 'd': -1})


c1 = Counter({"a": 5, "b": 3, "c": 2, "e": 5})
c2 = Counter({"a": 2, "b": 4, "d": 1, "e": 5})
result = c1 - c2
# Removes zero and negative counts
# original c1 not modified
print(result)  # Counter({'a': 3, 'c': 2})
