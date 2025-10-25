from collections import Counter


c1 = Counter({"a": 5, "b": 3, "c": 2})
c2 = Counter({"a": 2, "b": 4, "d": 1})
c1.subtract(c2)
print(c1)
# Output: Counter({'a': 3, 'c': 2, 'b': -1, 'd': -1})


c1 = Counter({"a": 5, "b": 3, "c": 2})
c2 = Counter({"a": 2, "b": 4, "d": 1})
result = c1 - c2
print(result)
# Output: Counter({'a': 3, 'c': 2})
