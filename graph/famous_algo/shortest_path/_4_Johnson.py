"""
Johnson's Algorithm for All-Pairs Shortest Paths
------------------------------------------------

Works for:
- Directed graphs
- Negative edge weights
- No negative cycles

Time Complexity:
O(VE + V E log V)
"""
"""
Johnson’s Algorithm
-------------------

Purpose:
--------
Find shortest distances between ALL pairs of vertices.

Unlike:
    - Dijkstra       → Single Source Shortest Path (no negative edges)
    - Bellman-Ford   → Single Source (handles negative edges)
    - Floyd-Warshall → All pairs, O(V^3)

Johnson:
    - Works for all pairs
    - Works with negative edges
    - Does NOT work if there is a negative cycle
    - More efficient than Floyd-Warshall for sparse graphs

------------------------------------------------------------
Core Idea:
------------------------------------------------------------

If we can somehow remove negative weights,
we can safely run Dijkstra from every vertex.

Steps:

1) Add a new vertex 'q'
2) Connect q → every vertex with weight 0
3) Run Bellman-Ford from q
      → get potential values h[v]
4) Reweight every edge:
      w'(u,v) = w(u,v) + h[u] - h[v]

   This guarantees:
      - All edges become non-negative
      - Shortest path structure is preserved

5) Run Dijkstra from each vertex
6) Convert distances back to original weights

------------------------------------------------------------
Time Complexity:
------------------------------------------------------------
Bellman-Ford :  O(VE)
Dijkstra V times: O(V * (E log V))

Total:
    O(VE + V E log V)

Efficient for sparse graphs.

------------------------------------------------------------
Space Complexity:
------------------------------------------------------------
O(V^2)  → for storing all-pairs result
O(V + E) → graph storage

------------------------------------------------------------
When to Use?
------------------------------------------------------------
- Sparse graphs
- Graph has negative edges
- No negative cycle
- Large V where Floyd-Warshall is too slow

----------------------------------------------------------------------
| Algorithm            | Negative Edges | Dense Graph | Sparse Graph |
| -------------------- | -------------- | ----------- | ------------ |
| Floyd-Warshall       |      ✔         |      ✔✔    |      ❌      |
| Dijkstra (all nodes) |      ❌        |      ✔     |       ✔      |
| Johnson              |      ✔         |      ❌    |      ✔✔      |
----------------------------------------------------------------------

"""
"""
Johnson’s Algorithm
-------------------

Purpose:
--------
Find shortest distances between ALL pairs of vertices.

Unlike:
    - Dijkstra       → Single Source Shortest Path (no negative edges)
    - Bellman-Ford   → Single Source (handles negative edges)
    - Floyd-Warshall → All pairs, O(V^3)

Johnson:
    - Works for all pairs
    - Works with negative edges
    - Does NOT work if there is a negative cycle
    - More efficient than Floyd-Warshall for sparse graphs

------------------------------------------------------------
Core Idea:
------------------------------------------------------------

If we can somehow remove negative weights,
we can safely run Dijkstra from every vertex.

Steps:

1) Add a new vertex 'q'
2) Connect q → every vertex with weight 0
3) Run Bellman-Ford from q
      → get potential values h[v]
4) Reweight every edge:
      w'(u,v) = w(u,v) + h[u] - h[v]

   This guarantees:
      - All edges become non-negative
      - Shortest path structure is preserved

5) Run Dijkstra from each vertex
6) Convert distances back to original weights

------------------------------------------------------------
Time Complexity:
------------------------------------------------------------
Bellman-Ford :  O(VE)
Dijkstra V times: O(V * (E log V))

Total:
    O(VE + V E log V)

Efficient for sparse graphs.

------------------------------------------------------------
Space Complexity:
------------------------------------------------------------
O(V^2)  → for storing all-pairs result
O(V + E) → graph storage

------------------------------------------------------------
When to Use?
------------------------------------------------------------
- Sparse graphs
- Graph has negative edges
- No negative cycle
- Large V where Floyd-Warshall is too slow

----------------------------------------------------------------------
| Algorithm            | Negative Edges | Dense Graph | Sparse Graph |
| -------------------- | -------------- | ----------- | ------------ |
| Floyd-Warshall       |      ✔         |      ✔✔    |      ❌      |
| Dijkstra (all nodes) |      ❌        |      ✔     |       ✔      |
| Johnson              |      ✔         |      ❌    |      ✔✔      |
----------------------------------------------------------------------

"""

import heapq

INF = float("inf")


def bellman_ford(V, edges, source):
    """
    Standard Bellman-Ford
    Returns:
        h[] array if no negative cycle
        None if negative cycle exists
    """

    distance = [INF] * V
    distance[source] = 0

    # Relax edges V-1 times
    for _ in range(V - 1):
        for u, v, w in edges:
            if distance[u] != INF and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    # Detect negative cycle
    for u, v, w in edges:
        if distance[u] != INF and distance[u] + w < distance[v]:
            return None

    return distance


def dijkstra(V, adj, source):
    """
    Standard Dijkstra using Min-Heap
    """

    distance = [INF] * V
    distance[source] = 0

    pq = [(0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist > distance[u]:
            continue

        for v, w in adj[u]:
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                heapq.heappush(pq, (distance[v], v))

    return distance


def johnson(graph):
    """
    graph: adjacency list
           graph[u] = [(v, weight), ...]

    Returns:
        All-pairs shortest distance matrix
    """

    V = len(graph)

    # Convert adjacency list to edge list
    edges = []
    for u in range(V):
        for v, w in graph[u]:
            edges.append((u, v, w))

    # ------------------------------------------------
    # Step 1: Add extra node q
    # ------------------------------------------------
    new_vertex = V
    for v in range(V):
        edges.append((new_vertex, v, 0))

    # ------------------------------------------------
    # Step 2: Run Bellman-Ford from q
    # ------------------------------------------------
    h = bellman_ford(V + 1, edges, new_vertex)

    if h is None:
        print("Graph contains a negative weight cycle")
        return None

    # Remove temporary edges
    edges = edges[:-V]

    # ------------------------------------------------
    # Step 3: Reweight edges
    # ------------------------------------------------
    new_adj = [[] for _ in range(V)]

    for u, v, w in edges:
        new_weight = w + h[u] - h[v]
        new_adj[u].append((v, new_weight))

    # ------------------------------------------------
    # Step 4: Run Dijkstra from each vertex
    # ------------------------------------------------
    all_pairs = []

    for u in range(V):
        dist = dijkstra(V, new_adj, u)

        # Convert back to original weights
        for v in range(V):
            if dist[v] != INF:
                dist[v] = dist[v] - h[u] + h[v]

        all_pairs.append(dist)

    # ------------------------------------------------
    # Print Result
    # ------------------------------------------------
    print("All-Pairs Shortest Distance Matrix:")
    for row in all_pairs:
        print(row)

    return all_pairs


if __name__ == "__main__":

    # Adjacency List Representation
    graph = [
        [(1, 3), (3, 7)],       # 0
        [(0, 8), (2, 2)],       # 1
        [(0, 5), (3, 1)],       # 2
        [(0, 2), (1, -1)]       # 3
    ]

    johnson(graph)