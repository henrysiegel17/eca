def Dijkstra(G, s, f):
    # make all distances in G infinite
    dist = {}
    prev = {}
    Q = []
    vertices = G.getVertices()
    for v in vertices:
        dist[v] = float('inf')
        prev[v] = None
        Q.append(v)
    dist[s] = 0

    while len(Q) > 0:
        u = min(dist, key=dist.get)
        if u == f:
            break
        Q.pop(u)

        neighbors = u.getNeighbors()

        for v in neighbors:
            alt = dist[u] + G.getEdge(u,v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


