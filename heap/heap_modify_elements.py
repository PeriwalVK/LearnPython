from __future__ import annotations
import heapq

class Element:
    def __init__(self, e):
        self.e = e
    
    def __lt__(self, b: Element):
        return self.e < b.e
    
    def __repr__(self):
        return str(self.e)
    
    # def __str__(self):
    #     return f"str:{self.e}"

order = [10, 5, 9, 4, 8, 3, 7, 2, 6, 1]
h = []
mp = dict()
for each in order:
    elt = Element(each)
    print(elt)
    h.append(elt)
    mp[each] = elt
# h = [
#     Element(10),
#     Element(5),
#     Element(9),
#     Element(4),
#     Element(8),
#     Element(3),
#     Element(7),
#     Element(2),
#     Element(6),
#     Element(1),
# ]


heapq.heapify(h)
print(h) # [1, 2, 3, 4, 5, 9, 7, 10, 6, 8]

################## Modifying and heapifying #################

mp[1].e = 100
heapq.heapify(h)
print(h) # [2, 4, 3, 6, 5, 9, 7, 10, 100, 8]