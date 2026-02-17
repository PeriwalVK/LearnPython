"""
Python Program to count cycles of length n in a given graph.
https://www.geeksforgeeks.org/dsa/cycles-of-length-n-in-an-undirected-and-connected-graph/

"""

# Number of vertices
V = 5
count = 0


def DFS(graph, visited, n, curr_vert, start):
    global count
    # marking curr_vert visited temporarily
    visited[curr_vert] = True

    # if the path of length (n-1) is found
    if n == 0:
        # Check if vertex vert can end with vertex start
        if graph[curr_vert][start] == 1:
            count += 1

    else:
        # For searching every possible path of length (n-1)
        for i in range(V):
            if (not visited[i]) and graph[curr_vert][i] == 1:
                # DFS for searching path by decreasing length by 1
                DFS(graph, visited, n - 1, i, start)

    # making curr_vert usable again.
    visited[curr_vert] = False


# Counts cycles of length N in an undirected and connected graph.
def countCycles(graph, n):

    # all vertex are marked un-visited initially.
    visited = [False] * V

    # Searching for cycle by using v-(n-1) vertices count = 0
    # bcz we start from all cycle that contains 0,
    # then in next iteration we calculate all cycle that includes 1 but not 0
    #
    # so going on we in final iteration include all cycle which include the vertex `V-1 - (n-1)`` 
    #   and we are left with vertices V-1 - (n-1), V-1 - (n-2), V-1 - (n-3) and so on upto v-1
    #
    # and in next iteration, no sufficient number of vertices are left to query

    for i in range(V - (n - 1)):
        DFS(graph, visited, n - 1, curr_vert=i, start=i)

        # ith vertex is marked permanently visited and will not be visited again.
        # because all cycles of length 4 containing i has already been considered
        visited[i] = True

    return count // 2
    # because 1->2->3->4 and 1->4->3->2 are same cycles considered twice


# main :
graph = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
]

n = 4

print("Total cycles of length ", n, " are ", countCycles(graph, n))
