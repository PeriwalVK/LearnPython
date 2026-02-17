"""
Cycle Detection in Directed Graph (DFS + Coloring Method)
(https://youtu.be/rKQaZuoUR4M?si=QRxB5EuKxR5dFSq1)
----------------------------------------------------------

Purpose:
--------
Detect whether a directed graph contains a cycle.

Approach Used:
--------------
Depth First Search (DFS) with 3-color marking technique.

Each vertex can be in one of three states:

    WHITE (0) → Not visited yet
    GRAY  (1) → Currently being visited (in recursion stack)
    BLACK (2) → Completely processed

Key Idea:
---------
If during DFS traversal we encounter a GRAY vertex,
it means we found a BACK EDGE.

Back edge ⇒ Cycle exists.

----------------------------------------------------------
Time Complexity:
----------------------------------------------------------
O(V + E)

Why?
- Each vertex is visited once.
- Each edge is explored once.

----------------------------------------------------------
Space Complexity:
----------------------------------------------------------
O(V)

Why?
- 1 color array of size V
"""

WHITE = 0  # Unvisited node
GRAY = 1  # Node is currently in recursion stack
BLACK = 2  # Node completely processed


# ----------------------------------------------------------
# Step 1: Construct Adjacency List
# ----------------------------------------------------------
def construct_adj(V, edges):
    """
    Converts edge list into adjacency list.

    Parameters:
        V     → Number of vertices
        edges → List of directed edges [u, v]

    Returns:
        Adjacency list representation of graph
    """

    adj = [[] for _ in range(V)]

    for u, v in edges:
        adj[u].append(v)

    return adj


# ----------------------------------------------------------
# Step 2: DFS Utility Function
# ----------------------------------------------------------
def dfs_util(u, graph_adj, color):
    """
    Performs DFS traversal and checks for cycle.

    Returns:
        True  → If cycle found
        False → Otherwise
    """

    # Mark current node as visiting (GRAY)
    color[u] = GRAY

    # Explore all neighbours
    for v in graph_adj[u]:
        # Case 1: If neighbour is BLACK → already visited → skip
        if color[v] == BLACK:
            continue

        # Case 2: If neighbour is GRAY → Back Edge → Cycle
        if color[v] == GRAY:
            return True

        # Case 3: If neighbour is unvisited → DFS on it
        if color[v] == WHITE:
            if dfs_util(v, graph_adj, color):
                return True

    # Mark node as completely processed
    color[u] = BLACK

    return False


# ----------------------------------------------------------
# Step 3: Main Function
# ----------------------------------------------------------
def is_cyclic(V, edges):
    """
    Detects cycle in directed graph.

    Returns:
        True  → If graph contains cycle
        False → Otherwise
    """

    # Initially all nodes are WHITE (unvisited)
    color = [WHITE] * V

    # Build adjacency list
    graph_adj = construct_adj(V, edges)

    # Check each vertex (handles disconnected graph)
    for i in range(V):
        if color[i] == WHITE:
            if dfs_util(i, graph_adj, color):
                return True

    return False


# ----------------------------------------------------------
# Driver Code
# ----------------------------------------------------------

"""
Example:
0 → 1
0 → 2
1 → 2
2 → 0   (Cycle)
2 → 3
3 → 3   (Self-loop → Cycle)
"""

V = 4
edges = [
    [0, 1],
    [0, 2],
    [1, 2],
    [2, 0],  # Forms cycle
    [2, 3],
    [3, 3],  # Self-loop (cycle)
]

print("Cycle Found: ", "True" if is_cyclic(V, edges) else "False")
