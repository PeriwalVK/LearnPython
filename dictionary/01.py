"""
Q1.
Given 3 dictionaries
d1 = {'a':20, 'b': 3, 'e': 22}
d2 = {'b': 22, 'a': 45, 'c': 10, 'd':103}
d3 = {'b': 22, 'a': 2, 'c': 30, 'e':21}

Create a final dictionary that has all elements with sum of counts in ascending order.
You can use any libs. Try to complete the solution in minimum lines of code.
Solution should be extensible such that in future we can use any number of dictionaries
"""

from collections import Counter
from functools import reduce

d1 = {"a": 20, "b": 3, "e": 22}
d2 = {"b": 22, "a": 45, "c": 10, "d": 103}
d3 = {"b": 22, "a": 2, "c": 30, "e": 21}

all_dicts = [d1, d2, d3]


# The built-in sum function, however, takes an iterable as its first argument and an optional start value as its second.
# Hence getting TypeError
# combined_counter = reduce(sum, map(Counter, all_dicts), Counter())
# use lambda a,b:a+b instead

combined_counter = sum(map(Counter, all_dicts), Counter())
final_dict = dict(sorted(combined_counter.items(), key=lambda item: item[1]))

# Print the final dictionary
print(final_dict)
