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
2. must NOT contain NEGATIVE EDGES.
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

-----------------------------------------
What we try to do (in simple language)
-----------------------------------------

1) Initialize distance array
2) Initialize min-heap with (0, source)
3) While min-heap is not empty:
    3a) Pop min from min-heap
    3b) If this is best path to this popped node till now -> then Relax all edges of this popped node
4) Return distance array


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
        dist_of_node, node = heapq.heappop(min_heap)

        # If we already have had a better one than this, then skip this,
        # bcz heap has already considered and processed this node using that best path till now
        #     and its neighbours have already been considered using that better path
        if distance[node] < dist_of_node:
            continue

        # Step 3: Explore neighbors
        for neighbor, weight in graph[node]:
            # new potential distance of neighbour
            new_distance = dist_of_node + weight

            # Relaxation step: if we just found a new best path for a neighbour
            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance  # recorded this new best
                parents[neighbor] = node  # recorded current parent as per this new best
                heapq.heappush(min_heap, (new_distance, neighbor))

    print(parents)

    ##############################################################################
    # Step 4: Print shortest paths
    print(f"All Shortest paths from {source} are: ")
    for node in range(n):
        if distance[node] == float("inf"):
            print(f"""DESTINATION: {node}\t UNREACHABLE""")
            continue

        curr_node = node
        curr_path = []
        while curr_node is not None:
            curr_path.append(curr_node)
            curr_node = parents[curr_node]

        curr_path.reverse()
        path = " -> ".join(str(i) for i in curr_path)
        print(f"""DESTINATION: {node}\t LENGTH: {distance[node]}\t PATH: {path}""")

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
