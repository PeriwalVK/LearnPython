"""
Kruskal's Algorithm (Minimum Spanning Tree)

We assume vertices are numbered from 0 to n-1.

-----------------------------------------------
Time Complexity Discussion (Beginner Friendly)
-----------------------------------------------

1) Sorting edges:
    O(E log E)

2) Union-Find operations (with path compression + union by rank):
    Each operation is O(alpha(V))

    alpha(V) = Inverse Ackermann function.
    It grows extremely slowly.

Theoretical complexity:
    O(E log E + E * alpha(V))

Practical reality:
    In any real-world system, alpha(V) <= 4.
    So E * alpha(V) behaves like O(E).

So practically:
    Kruskal runs in O(E log E)
    (Sorting dominates the time)

-----------------------------------------------
Conclusion:
    Practically → Almost linear for union part
    Formally → O(E alpha(V))
-----------------------------------------------

suitable for: Sparse graphs

"""

from typing import List, Tuple


class DisjointSet:
    def __init__(self, n):
        # Parent array: initially each node is its own parent
        self.parent = list(range(n))

        # Rank array: used to keep tree shallow
        self.rank = [0] * n

    def find(self, node):
        # Path Compression:
        # Make every node on path point directly to root
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        # If both vertices have same root → already in same set
        if root_u == root_v:
            return

        # Union by Rank: Attach smaller height tree under larger one
        if self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        elif self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1

        # print(f"merged {u} and {v}")


def kruskal(n, edges: List[Tuple[int, int, int]]):
    """
    n     → number of vertices (0 to n-1)
    edges → list of (u, v, weight)
    """

    # Step 1: Sort edges by weight
    edges.sort(key=lambda e: e[2])
    print(edges)

    ds = DisjointSet(n)

    mst = []

    # Step 2: Process edges in increasing weight order
    for e in edges:
        # Add edge if it doesn't form a cycle
        u, v, weight = e

        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append(e)

    return mst


# -------------------------------
# Example
# -------------------------------


edges = [
    # (u, v, weight)
    (1, 0, 3),
    (3, 0, 1),
    (3, 1, 3),
    (2, 1, 1),
    (3, 2, 1),
    (3, 4, 6),
    (2, 4, 5),
    (2, 5, 4),
    (4, 5, 2),
]

n = 1 + max(max(edge[0], edge[1]) for edge in edges)  # vertices: 0, 1, 2, 3, .... n-1
mst = kruskal(n, edges)

print("[Kruskal]: MST edges:", mst)
print("[Kruskal]: Total weight:", sum(e[2] for e in mst))
