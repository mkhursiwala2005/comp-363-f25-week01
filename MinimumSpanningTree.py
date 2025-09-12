def reachability_of(s: int, G: list[list[int]]) -> list[int]:
    """
    Compute the vertices reachable from a given starting vertex
    in a directed graph represented by an adjacency matrix.

    Parameters
    ----------
    s : int
        Starting vertex index.
    G : list[list[int]]
        Adjacency matrix representation of the graph, where
        G[i][j] is the edge weight (or a sentinel `no_edge` value).

    Returns
    -------
    list[int]
        Vertices reachable from `s`.
    """

    # Grab what the input graph uses to indicate absence of an edge.
    # We can always expect that for a non trivial graph, ie a graph
    # with one or more vertices, there will be at least one diagonal
    # elemennt (where the no-edge value is present), so we grab the
    # first element of the diagonal.
    no_edge: int = G[0][0]
    # Initialize a list to return
    reach: list[int] = []
    # List to remember which vertices to try next. Start from the
    # given vertex.
    visit_next: list[int] = [s]

    # Explore vertices that we need to visit next. The algorithm stops
    # when the list of vertices to visit next is empty.
    while visit_next:  # shorcut to while len(...) > 0
        # Grab some vertex that we wish to visit next
        v: int = visit_next.pop()
        # Check to see if the vertex we just grabed is already
        # in the list of vertices reachable from s.
        if v not in reach:
            # The vertex we just grabed is not in the list, of
            # vertices accessible from s so let's add it.
            reach.append(v)
            # Now, find all of the neighbors of the vertex we just
            # added to the reach list. We do this by considering
            # every vertex in the graph (loop with u) and asking
            # if there is an edge between u and v. If there is an
            # edge, we add u to the list of vertices to visit next.
            for u in range(len(G)):
                if G[v][u] != no_edge:
                    visit_next.append(u)
    # Done
    return reach


def report_reachability(s: int, graph: list[list[int]]) -> None:
    """Helper method to produce nice reports from the reachability method."""
    print(
        f"\nThe set of vertices reachable from {s} is: {reachability_of(s, graph)}")
    
    
def count_and_label(graph: list[list[int]]) -> tuple[int, list[int]]:
    n = len(graph)
    visited: list[int] = []
    compLabels: list[int] = [None] * n
    count: int = 0
    
    for u in range(n):
        if u not in visited: 
            count += 1
            reachable = reachability_of(u, graph)
            for v in reachable: 
                compLabels[v] = count
            visited.extend(reachable)
    return count, compLabels

    
def min_span_tree(G: list[list[int]]) -> list[list[int]]:
    n = len(G)
    no_edge = G[0][0]
    
    # Create an edgeless copy of G
    T = [[no_edge for _ in range(n)] for _ in range(n)]
    
    #  Count initial components in T
    comp_count, compLabels = count_and_label(T)
    
    # Grow MST until all vertices are connected 
    while comp_count > 1: 
        cheapest: list[tuple[int, int] | None] = [None] * (comp_count + 1)
        
        # For each pair (u, v) check if it connects two different components
        for u in range(n):
            for v in range(n):
                if G[u][v] != no_edge and compLabels[u] != compLabels[v]:
                    cu = compLabels[u]
                    cv = compLabels[v]
                    if cheapest[cu] is None or G[u][v] < G[cheapest[cu][0]][cheapest[cu][1]]:
                        cheapest[cu] = (u, v)
                    if cheapest[cv] is None or G[u][v] < G[cheapest[cv][0]][cheapest[cv][1]]:
                        cheapest[cv] = (u, v)
        
    return T
