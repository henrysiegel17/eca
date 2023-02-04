from Graph import GraphClass, Vertex
from Dijkstra import dijkstraAlgorithm


def weanPorter(source,end):
    Wean5 = GraphClass('Wean5', 3)
    floorPlan = open("myfile.txt", 'r')
    floorPlan.readline() 
    connections = []
    for line in floorPlan:
        # line = room_num + ' ' + f'{x}, {y}' + ' ' + adjacent_vertices_string
        components = line.split(' ')
        location = components[1].split(',')
        coordinates = (int(location[0]), int(location[1])) 
        v = Vertex(components[0], coordinates)
        Wean5.addVertex(v)
        for i in range(2, len(components)-1):
            connections.append((components[0], components[i]))
        

    for connection in connections:
        node1 = Wean5.findNode(connection[0])
        node2 = Wean5.findNode(connection[1])
        Wean5.addEdge(node1, node2)


        # NOW USE DIJKSTRA'S ALGORITHM
        # source = ??
        # end = ??
        source_vertex = Wean5.findNode(source)
        end_vertex = Wean5.findNode(end)

        dist, prev = dijkstraAlgorithm(Wean5, source_vertex, end_vertex)
        endCoordinates = []
        u = end
        while prev[u] != source_vertex.getName():
            node = Wean5.findNode(u)
            endCoordinates.append(node.getPosition())
            u = prev[u]
        # DONE
    return endCoordinates



if "__main__" == __name__:
    main()