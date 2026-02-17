"""
Dijkstra's Algorithm (Single Source Shortest Path)

------------------------------------------------
What it does?
------------------------------------------------
Finds shortest distance from a given source to all other nodes in a graph.

------------------------------------------------
IMPORTANT CONDITIONS
------------------------------------------------
1. Graph can be directed or undirected.
2. must NOT contain negative edges.
3. Vertices numbered 0 to n-1.
4. adjacency list.

------------------------------------------------
Time Complexity Discussion (Accurate Version)
------------------------------------------------

We use:
    - Adjacency List
    - Binary Min Heap (priority queue)

For V vertices and E edges:

Each vertex is pushed into heap at most once
Each edge is relaxed once

Time Complexity:
    O((V + E) log V)

For dense graph:
    O(E log V)

Space Complexity:
    O(V + E)
"""

import heapq
from typing import List, Tuple


def to_adj(edges: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int]]]:
    n = 1 + max(
        max(edge[0], edge[1]) for edge in edges
    )  # vertices: 0, 1, 2, 3, .... n-1

    graph: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    # graph[u] = [(v, weight)]

    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return graph


def dijkstra(n, graph, source):
    """
    n       : number of vertices
    graph   : adjacency list
              graph[u] = [(v, weight), ...]
    source  : starting vertex
    """

    # Step 1: Initialize distance array
    distance = [float("inf")] * n
    distance[source] = 0

    parents = [None] * n

    # Step 2: Min Heap (distance, node)
    min_heap = [(0, source)]

    while min_heap:
        current_dist, node = heapq.heappop(min_heap)

        # If we already found a better path, skip
        # bcz already neighbours have been considered using that better path
        if current_dist > distance[node]:
            continue

        # Step 3: Explore neighbors
        for neighbor, weight in graph[node]:
            new_distance = current_dist + weight

            # Relaxation step
            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance
                parents[neighbor] = node
                heapq.heappush(min_heap, (new_distance, neighbor))

    print(parents)

    ##############################################################################
    # Step 4: Print shortest paths
    print(f"All Shortest paths from {source} are: ")
    for node in range(n):
        curr_node = node
        curr_path = []
        while curr_node is not None:
            curr_path.append(curr_node)
            curr_node = parents[curr_node]
        curr_path.reverse()
        if distance[node] == float("inf"):
            print(f"""DESTINATION: {node}\t UNREACHABLE""")
            continue
        else:
            print(
                f"""DESTINATION: {node}\t LENGTH: {distance[node]}\t PATH: {" -> ".join(str(i) for i in curr_path)}"""
            )

    return distance


if __name__ == "__main__":
    edges = [
        # (u, v, weight)
        (1, 0, 4),
        (3, 0, 1),
        (3, 1, 3),
        (2, 1, 1),
        (3, 2, 1),
        (3, 4, 6),
        (2, 4, 5),
        (2, 5, 4),
        (4, 5, 2),
        (0, 2, 4),
        (3, 5, 1),
        (6, 7, 8),  # unreachable
    ]

    # Undirected Weighted Graph with no negative edge
    # Else it will fail bcz we are using min-heap to find min edge
    #
    #       (1)         (6)
    #  0 --------- 3 --------- 4
    #  | \       / | \       / |
    #  |  \(4)  /  |  \(1)  /  |
    # (4)  \   /  (1)  \   /  (2)
    #  |    \ /    |    \ /    |
    #  |     X     |     X     |
    #  |    / \    |    / \    |
    #  |   /   \   |   /   \   |
    #  |  /(3)  \  |  /(5)  \  |
    #  | /       \ | /       \ |
    #  1 --------- 2 --------- 5
    #       (1)         (4)
    #
    #             (8)
    #  6 -------------------------> 7

    graph = to_adj(edges)
    # graph[u] = [(v, weight)]

    n = len(graph)

    source = 0

    distances = dijkstra(n, graph, source)

    print("Shortest distances from source:", distances)
