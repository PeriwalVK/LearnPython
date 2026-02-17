"""
Kahn's Algorithm (Topological Sorting using BFS)

------------------------------------------------
What is Topological Sorting?
------------------------------------------------
A topological sort of a Directed Acyclic Graph (DAG)
is a linear ordering of vertices such that:

    For every directed edge (u → v),
    u appears before v in the ordering.

NOTE:
- Works ONLY for Directed Acyclic Graphs (DAG).
- If graph has a cycle, topological ordering is NOT possible.

------------------------------------------------
How Kahn’s Algorithm Works
------------------------------------------------
1. Compute in-degree of every vertex.
2. Push all vertices with in-degree = 0 into a queue.
3. While queue is not empty:
      - Remove a vertex
      - Add it to result
      - Reduce in-degree of its neighbors
      - If any neighbor becomes 0, push it to queue
4. If result size != number of vertices → cycle exists.

------------------------------------------------
Time Complexity
------------------------------------------------
Let:
    V = number of vertices
    E = number of edges

- Calculating in-degree:   O(E)
- Each vertex processed once: O(V)
- Each edge processed once: O(E)

Total Time Complexity: O(V + E)

Space Complexity:
- Adjacency list: O(V + E)
- In-degree array: O(V)
- Queue: O(V)

Total Space: O(V + E)
"""

from collections import deque


def kahn_topological_sort(n, edges):
    """
    n     -> number of vertices (0 to n-1)
    edges -> list of (u, v) meaning u → v
    """

    # Step 1: Build adjacency list
    adj = [[] for _ in range(n)]
    in_degree = [0] * n

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    # Step 2: Add all vertices with in-degree 0 to queue
    queue = deque()

    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    topo_order = []

    # Step 3: Process the queue
    while queue:
        node = queue.popleft()
        topo_order.append(node)

        for neighbor in adj[node]:
            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 4: Check for cycle
    if len(topo_order) != n:
        print("Cycle detected! Topological sort not possible.")
        return []

    return topo_order


if __name__ == "__main__":
    # Example DAG
    # 5 --→ 2 --→ 3 ---> 1
    # |                  ^
    # v                  |
    # 0 <--------------- 4

    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]

    n = 6

    result = kahn_topological_sort(n, edges)
    print("Topological Order:", result)
