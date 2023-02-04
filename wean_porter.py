from Graph import GraphClass, Vertex

def main():
    Wean5 = GraphClass('Wean5', 3)
    floorPlan = open("myfile.txt", 'r')
    floorPlan.readline() 
    connections = []
    for line in floorPlan:
        # line = room_num + ' ' + f'{x}, {y}' + ' ' + adjacent_vertices_string
        components = line.split(' ')
        coordinates = (int(components[2][0]), int(components[2][1])) 
        v = Vertex(components[1], coordinates)
        Wean5.add(v)
        for i in range(3, len(components)):
            connections.append((components[1], components[i]))
        

    for connection in len(connections):
        node1 = Wean5.findNode(connection[0])
        node2 = Wean5.findNode(connection[1])
        Wean5.addEdge(node1, node2)

if "__main__" == __name__:
    main()