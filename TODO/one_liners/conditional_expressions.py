# cond1 = True
cond1 = False

cond2 = True
# cond2 = False

print("First" if cond1 else "Second" if cond2 else "Third")
"""
Same as below
>>> if cond1:
>>>     print("First")
>>> elif cond2:
>>>     print("Second")
>>> else:
>>>     print("Third")
"""
