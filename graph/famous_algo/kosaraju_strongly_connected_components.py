"""
Kosaraju's Algorithm (Strongly Connected Components)
(https://youtu.be/RpgcYiky7uw?si=aXDKyroG5lnNhHHn)
------------------------------------------------

# NOTE:
# This algorithm works only for directed graphs.
# It finds all Strongly Connected Components (SCCs).
#
# A Strongly Connected Component (SCC) is a group of vertices
# where every vertex is reachable from every other vertex
# in that group.


# Even If graph is disconnected, it will still correctly find
# SCCs in all components.

We assume vertices are numbered from 0 to n-1.
Graph is represented using an adjacency list.

------------------------------------------------
Time Complexity Discussion (Accurate Version)
------------------------------------------------

We use:
    - Adjacency List
    - DFS (Depth First Search)

There are three major steps:

1) First DFS to compute finishing order
   → Each vertex visited once
   → Each edge explored once
   → Cost: O(V + E)

2) Reverse (Transpose) the graph
   → Iterate over all vertices and edges
   → Cost: O(V + E)

3) Second DFS on reversed graph
   → Again each vertex visited once
   → Each edge explored once
   → Cost: O(V + E)

Total Time Complexity:
    O(V + E)

------------------------------------------------
Space Complexity
------------------------------------------------

Visited array      → O(V)
Stack              → O(V)
Reversed graph     → O(V + E)

Total Space:
    O(V + E)
"""

from typing import List


class Kosaraju:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    # -----------------------------------------
    # Add directed edge
    # -----------------------------------------
    def add_edge(self, u, v):
        self.graph[u].append(v)

    # -----------------------------------------
    # Step 1:
    # Perform DFS and push nodes into stack
    # according to finishing time
    # -----------------------------------------
    def _dfs_fill_order(self, node, visited, stack: List):

        visited[node] = True

        for neighbor in self.graph[node]:
            if not visited[neighbor]:
                self._dfs_fill_order(neighbor, visited, stack)

        # Push after exploring all neighbors
        stack.append(node)

    # -----------------------------------------
    # Step 2:
    # Reverse (transpose) the graph
    # -----------------------------------------
    def _get_transpose(self):

        reversed_graph = Kosaraju(self.V)

        for node in range(self.V):
            for neighbor in self.graph[node]:
                reversed_graph.add_edge(neighbor, node)

        return reversed_graph

    # -----------------------------------------
    # Step 3:
    # DFS on reversed graph to collect one SCC
    # -----------------------------------------
    def _dfs_collect_scc(self, node, visited, component: List[int]):

        visited[node] = True
        component.append(node)

        for neighbor in self.graph[node]:
            if not visited[neighbor]:
                self._dfs_collect_scc(neighbor, visited, component)

    # -----------------------------------------
    # Main Function
    # -----------------------------------------
    def find_sccs(self):

        stack = []
        visited = [False] * self.V

        # STEP 1: Fill stack using DFS
        for i in range(self.V):
            if not visited[i]:
                self._dfs_fill_order(i, visited, stack)

        # STEP 2: Reverse the graph
        reversed_graph = self._get_transpose()

        # STEP 3: Process nodes in stack order
        visited = [False] * self.V
        scc_list: List[List[int]] = []

        while stack:
            node = stack.pop()

            if not visited[node]:
                new_component = []
                reversed_graph._dfs_collect_scc(node, visited, new_component)
                scc_list.append(new_component)

        return scc_list


# -----------------------------------------
# Example Usage
# -----------------------------------------

if __name__ == "__main__":
    # Directed Graph Representation
    #
    #       0 <----- 2             4              7 ---------> 8
    #       \       ^             ^   \           ^            |
    #        \     /             /     \          |            |           11
    #         v   /             /       v         |            v
    #           1 <---------- 3 <------ 5 <------ 6 <--------- 9 --------> 10

    g = Kosaraju(12)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(3, 1)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)
    g.add_edge(6, 5)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 6)
    g.add_edge(9, 10)

    sccs = g.find_sccs()

    print("Strongly Connected Components:")
    for scc in sccs:
        print(scc)
