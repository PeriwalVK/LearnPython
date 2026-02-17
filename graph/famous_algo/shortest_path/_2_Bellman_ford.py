"""
Bellman-Ford Algorithm
(https://youtu.be/-mOEd_3gTK0?si=HdaQxTAxOEvEuuWi)
-----------------------------------------
Used to find the shortest path from a
single source to all other vertices.

Key Features:
    - Works with negative edge weights
    - Can detect negative weight cycles

We assume:
    - Vertices are numbered from 0 to V-1
    - Graph is represented as an edge list

-----------------------------------------
Time Complexity Discussion
-----------------------------------------

We relax all edges (V - 1) times.

If:
    V = number of vertices
    E = number of edges

Then:
    Time Complexity = O(V * E)
    Space Complexity = O(V)
"""


def bellman_ford(n, edges, source):
    """
    vertices : int
        Number of vertices (V)

    edges : list of tuples
        Each tuple is (u, v, weight)

    source : int
        Starting vertex
    """

    # Step 1: Initialize distance array
    distance = [float("inf")] * n
    distance[source] = 0

    parents = [None] * n

    # Step 2: Relax all edges (V - 1) times
    for _ in range(n - 1):
        _updated = False

        for u, v, weight in edges:
            # if distance[u] + weight < distance[v]:
            if distance[u] != float("inf") and distance[u] + weight < distance[v]:
                # could have simply removed <distance[u] != float("inf")>
                # but Bellman Ford says apply it only when distance[u] != float("inf")
                # i.e. only when u is already reached -> then try updating distance of v
                distance[v] = distance[u] + weight
                parents[v] = u
                _updated = True

        if not _updated:
            # that means nothing is achieved in this iteration,
            # and nothing will be achieved in successive iterations,
            # hence we better break
            #
            # and there are no negative cycles for sure ->
            #   hence no need to check for negative weight cycles in next for loop
            #   but still a good practice to explicitly check for negative cycles just for safety.
            break

    # Step 3: Detect negative weight cycle by doing the same one more time (i.e. nth time)
    for u, v, weight in edges:
        # if distance[u] + weight < distance[v]:
        if distance[u] != float("inf") and distance[u] + weight < distance[v]:
            print("Graph contains a negative weight cycle")
            return None

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
    # Edge list: (source, destination, weight)
    edges = [
        (0, 1, -1),
        (0, 2, 1),
        (1, 2, 3),
        (1, 3, 2),
        (1, 4, 2),
        (3, 2, 5),
        (3, 1, 1),
        (4, 3, -3),
        (5, 6, 7),  # unreachable
    ]
    n = 1 + max(
        max(edge[0], edge[1]) for edge in edges
    )  # vertices: 0, 1, 2, 3, .... n-1

    # Directed Weighted Graph
    #
    #                  (2)
    #           ,----------------> 4
    #          /                   |
    #         /                    | (-3)
    #        /                     |
    #       /      (2)             v
    #      1 --------------------> 3
    #      ^ \ <------------------ |
    #      |  \        (1)         |
    # (-1) |   \                   | (5)
    #      |    \ (3)              |
    #      |     \                 v
    #      |      \--------------> 2
    #      |                       ^
    #      |                       |
    #      0 ----------------------'
    #                 (1)
    #
    #                 (7)
    #       5----------------------> 6

    source = 0

    shortest_paths = bellman_ford(n, edges, source)
