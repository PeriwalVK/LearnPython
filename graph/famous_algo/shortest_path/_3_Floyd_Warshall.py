"""
Floyd–Warshall Algorithm
------------------------

Purpose:
--------
Find shortest distances between ALL pairs of vertices.

Unlike:
    - Dijkstra → Single Source Shortest Path
    - Bellman-Ford → Single Source (handles negative edges)

Floyd–Warshall:
    - Works for all pairs
    - Works with negative edges
    - Does NOT work if there is a negative cycle

------------------------------------------------------------
Time Complexity:
------------------------------------------------------------
O(V^3)

Why?
We use 3 nested loops, each running V times.

basically the idea is:

>>> dist[i][j][k] = (shortest distance from i to j using intermediate vertex among 0 to k)
>>>     min(
>>>         dist[i][j][k-1],                    # don't use k (i.e. minimum found till now)
>>>         dist[i][k][k-1] + dist[k][j][k-1]   # use k
>>>     )

we don't need to have 3d array as value in K-th itr is dependednt on its previous iteration only
and dist[i][j] was updated in the same iteration k
    -> it can not improve within same iteration further unless there is a negative cycle
    which is a limitation of Floyd-Warshall

    i.e. Because improving dist[i][k] using vertex k would mean:
            i → k → k
            means => dist[i][k] > dist[i][k] + dist[k][k]
            means => dist[k][k] < 0
            means => there's a negative cycle at k.

------------------------------------------------------------
Space Complexity:
------------------------------------------------------------
O(V^2)

We store distances in a V x V matrix.

------------------------------------------------------------
When to Use?
------------------------------------------------------------
- Dense graphs (for sparse -> Johnson's Algorithm is better)
- When we need distance between EVERY pair of nodes
- When V is small (typically <= 400)

-----------------------------------------
What we try to do (in simple language)
-----------------------------------------
1) for every vertix as intermediate vertex (k)
    2) for every vertix as source vertex (i)
        3) for every vertix as destination vertex (j)
            # If going through k improves distance between i and j, then update it
            4) if distance[i][k] != INF and distance[k][j] != INF and distance[i][j] > distance[i][k] + distance[k][j]:
                distance[i][j] = distance[i][k] + distance[k][j]
                parents[i][j] = parents[k][j]




+=================+====================+=====================+======================+========================+
| Property        | Dijkstra           | Bellman-Ford        | Floyd-Warshall       | Johnson's Algo         |
|                 | (all nodes)        |                     |                      |                        |
+=================+====================+=====================+======================+========================+
| Allows -ve      | ❌                 | ✔                   | ✔                   | ✔                      |
| Edges           |                    |                     |                      |                        |
+-----------------+--------------------+---------------------+----------------------+------------------------+
| Detects -ve     | ❌                 | ✔                   | ✔                   | ✔ (via BF)             |
| Cycles          |                    |                     |                      |                        |
+-----------------+--------------------+---------------------+----------------------+------------------------+
| Works properly  | ❌                 | ❌                  | ❌                  | ❌                     |
| for -ve cycles  |                    | (detects only)      | (detects only)       | (fails if cycle exists)|
+=================+====================+=====================+======================+========================+
| Best Use Case   | Single src         | Single src → all    | All-pairs (APSP)     | Sparse APSP            |
| (shortest path) | (V times for APSP) | nodes               |                      |                        |
+=================+====================+=====================+======================+========================+
| Graph Type      | Adj List (heap)    | Edge List           | VxV Matrix           | Adj List + reweight    |
+=================+====================+=====================+======================+========================+
| Time Complexity | O(V·E log V)       | O(V·E)              | O(V³)                | O(V·E log V)           |
+-----------------+--------------------+---------------------+----------------------+------------------------+
| Space           | O(V + E)           | O(V)                | O(V²)                | O(V + E)               |
+=================+====================+=====================+======================+========================+
| Dense Graph     | ✔                  | ❌                  | ✔✔ (best)           | ❌                     |
+-----------------+--------------------+---------------------+----------------------+------------------------+
| Sparse Graph    | ✔✔                 | ✔✔                 | ❌                   | ✔✔ (best)             |
+=================+====================+=====================+======================+========================+
| Avoid When      | -ve weights        | Large dense graphs  | Large sparse graphs  | Dense graphs           |
+=================+====================+=====================+======================+========================+
| Algo Type       | Greedy             | DP                  | DP                   | Hybrid (BF + Dijkstra) |
+=================+====================+=====================+======================+========================+
| Relaxation      | Priority queue     | Repeated relaxation | DP via intermediates | Reweight + Dijkstra    |
+=================+====================+=====================+======================+========================+



"""

INF = float("inf")


def floyd_warshall(graph):
    """
    graph: adjacency matrix
           graph[i][j] = weight from i to j
           Use float('inf') if no direct edge exists
    """

    n = len(graph)

    # Create a copy of graph so original is not modified
    # (works here because nested object are immutable)
    distance = [row[:] for row in graph]
    parents = [
        [None if graph[i][j] == INF or i == j else i for j in range(n)]
        for i in range(n)
    ]
    # parents[i][j] stores predecessor of j in shortest path from i to j

    # Step 1: Pick every vertex as intermediate vertex
    for k in range(n):
        # Step 2: Pick every source vertex
        for i in range(n):
            # Step 3: Pick every destination vertex
            for j in range(n):
                # If going through k improves distance, update it
                # if distance[i][k] != INF and distance[k][j] != INF and distance[i][j] > distance[i][k] + distance[k][j]:
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    parents[i][j] = parents[k][j]
                    # Since shortest path i->j now goes through k,
                    # the predecessor of j becomes the predecessor used in k->j.

                    # Note: k may be equal to i or j.
                    # In such cases no update occurs unless distance[k][k] < 0,
                    # which would indicate a negative cycle.
                    # and floyd warshall does not work properly for negative cycles

    print("All-Pairs Shortest Distance Matrix:")
    for row in distance:
        print(row)
    print("All-Pairs Parents Matrix:")
    for row in parents:
        print(row)

    # Step 3: Detect negative weight cycle
    # If any diagonal value becomes negative,
    # a negative cycle is reachable from that vertex.
    for i in range(n):
        if distance[i][i] < 0:
            print("Graph contains a negative weight cycle")
            return None

    ##############################################################################
    # Step 4: Print shortest paths
    def print_path(source, destination):
        if distance[source][destination] == INF:
            print(f"from {source} to {destination}:\t UNREACHABLE")
            return

        curr_path = []
        curr_node = destination
        while curr_node is not None:
            curr_path.append(curr_node)
            curr_node = parents[source][curr_node]

        curr_path.reverse()
        path = " -> ".join(str(i) for i in curr_path)
        print(
            f"from {source} to {destination}:\t LENGTH: {distance[source][destination]},\t PATH: {path}"
        )

    for src in range(n):
        for dst in range(n):
            print_path(src, dst)
        print()

    return distance


if __name__ == "__main__":
    # graph = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, INF, INF, 0]]
    # graph = [
    #     [0, 3, INF, 7],
    #     [8, 0, 2, INF],
    #     [5, INF, 0, 1],
    #     [2, -1, INF, 0]
    # ]
    graph = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, -1, INF, 0]]

    floyd_warshall(graph)
