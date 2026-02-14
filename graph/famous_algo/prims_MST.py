"""
Prim's Algorithm (Minimum Spanning Tree)
# NOTE:
# This implementation assumes the graph is connected.
# If graph is disconnected, it will return MST of only
# the component containing the start node.

We assume vertices are numbered from 0 to n-1.
Graph is represented using an adjacency list.

------------------------------------------------
Time Complexity Discussion (Accurate Version)
------------------------------------------------

We use:
    - Adjacency List
    - Binary Min Heap (priority queue)

There are two main operations:

1) Extract-min (pop from heap)
   - Happens once per vertex
   - Total: V times
   - Each takes O(log V)
   - Cost: V log V

2) Push edges into heap
   - Each edge can be pushed once
   - Total: E times
   - Each push takes O(log V)
   - Cost: E log V

Total complexity:

    V log V + E log V
    = (V + E) log V

-----------------------------------------------
Why do some books write O(E log V)?
-----------------------------------------------

Because in a connected graph:

    E >= V - 1

So asymptotically:
    E dominates V

Thus:
    (V + E) log V ≈ E log V

Both forms are correct.
    - O((V + E) log V) → More precise
    - O(E log V)       → Simplified form

-----------------------------------------------
Final Complexity:
    O((V + E) log V)
-----------------------------------------------

suitable for: Dense graphs
"""

import heapq
from typing import List, Tuple


def to_adj(edges: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int]]]:
    n = 1 + max(
        max(edge[0], edge[1]) for edge in edges
    )  # vertices: 0, 1, 2, 3, .... n-1

    graph: List[List[Tuple[int, int]]] = [[] for _ in range(n)]

    for u, v, weight in edges:
        graph[u].append((weight, v))
        graph[v].append((weight, u))

    return graph

    # graph: List[List[Tuple[int, int]]] = [
    #     [(weight, neighbour)]
    # ]


def prim(n, graph) -> List[Tuple[int, int, int]]:
    """
    n     → number of vertices (0 to n-1)
    graph → adjacency list
            graph[u] = [(weight, v), ...]
    """

    visited = [False] * n
    min_heap = []

    mst: List[Tuple[int, int, int]] = []  # (u, v, weight)

    # Start from any vertex -> here we chose 0
    start_node = 0
    visited[start_node] = True

    for edge_weight, neighbor in graph[start_node]:
        heapq.heappush(min_heap, (edge_weight, neighbor, start_node))

    while min_heap:
        weight, node, parent = heapq.heappop(min_heap)
        if visited[node]:
            continue

        mst.append((parent, node, weight))
        visited[node] = True

        if len(mst) == n - 1:
            break

        # Push all adjacent edges
        for edge_weight, neighbor in graph[node]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (edge_weight, neighbor, node))

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

graph = to_adj(edges)
# graph: List[List[Tuple[int, int]]] = [
#     [(weight, neighbour)]
# ]

n = len(graph)

print(graph)

mst = prim(n, graph)

print("[Prims]: MST edges:", mst)
print("[Prims]: Total weight:", sum(e[2] for e in mst))
