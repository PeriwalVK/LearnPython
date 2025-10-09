"""
Write a Python function that takes the following dictionaries as input
and returns a new dictionary that contains only the elements that are common to each input.

Find sums of the count of the common elements
d1 = {'a':20, 'b': 3, 'e': 22, 'd': 24}
d2 = {'b': 22, 'a': 45, 'c': 10, 'd':3}
d3 = {'b': 22, 'a': 2, 'c': 30, 'e':21}
d4 = {'a': 22, 'k': 2, 'c': 30, 'b':21}
"""

from collections import Counter
from functools import reduce


d1 = {"a": 20, "b": 3, "e": 22, "d": 24}
d2 = {"b": 22, "a": 45, "c": 10, "d": 3}
d3 = {"b": 22, "a": 2, "c": 30, "e": 21}
d4 = {"a": 22, "k": 2, "c": 30, "b": 21}

dict_list = [d1, d2, d3, d4]

common_keys = reduce(lambda x, y: x & y, map(lambda d: set(d.keys()), dict_list))

filter_dict = lambda d: Counter({key: d[key] for key in common_keys})
# filter_dict = lambda d: Counter(dict(map(lambda key: (key, d[key]), common_keys)))

common_dict = sum(map(filter_dict, dict_list), Counter())
sorted_common_dict = dict(sorted(common_dict.items(), key=lambda x: x[1]))


print(sorted_common_dict)
