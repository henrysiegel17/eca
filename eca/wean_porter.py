from Graph import GraphClass, Vertex
import Dijkstra 


def main():
    Wean5 = GraphClass('Wean5', 3)
    floorPlan = open("myfile.txt", 'r')
    floorPlan.readline() 
    connections = []
    for line in floorPlan:
        # line = room_num + ' ' + f'{x}, {y}' + ' ' + adjacent_vertices_string
        components = line.split(' ')
        location = components[2].split(',')
        coordinates = (int(location[0]), int(location[1])) 
        v = Vertex(components[1], coordinates)
        Wean5.add(v)
        for i in range(3, len(components)):
            connections.append((components[1], components[i]))
        

    for connection in len(connections):
        node1 = Wean5.findNode(connection[0])
        node2 = Wean5.findNode(connection[1])
        Wean5.addEdge(node1, node2)


        # NOW USE DIJKSTRA'S ALGORITHM
        source = ??
        end = ??
        dist, prev = Dijkstra(Wean5, source, end)
        endCoordinates = []
        u = end
        while prev[u].getName() != source.getName():
            endCoordinates.append(prev[end].getPosition())
            u = prev[end]
        # DONE



if "__main__" == __name__:
    main()