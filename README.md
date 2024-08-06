# bachelor-project
The project works on Dijkstra’s algorithm, which is an algorithm that solves the single-source shortest-paths 
problem on a weighted, directed graph G = (V, E) for the case in which all edge weights are nonnegative.
In other words, the algorithm finds the shortest path from a certain vertex in a given graph to each of the 
other vertices. The graph in question could be entered either as a matrix or as a linked list.

In theory, when the graph is sparse, entering the graph as a linked list is more time efficient than entering it 
as a matrix, while for a dense graph the running time in both cases is approximately the same. 

In this project, we try to find the point at which a graph becomes dense enough such that the running time 
when the graph is entered as a matrix is (almost) equal to the running time when the graph is entered as a 
linked list.
