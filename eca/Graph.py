class Vertex(object):

    def __init__(self, adjacent, position, name):
        self.adjacentVertices = adjacent
        self.position = position
        self.name = name

    def getNeighbors(self):
        return self.adjacent_vertices

    def getPosition(self):
        return self.position

    
class Graph(object):
    def __init__(self, name, vertices, speed):
        self.name = name
        self.vertices = vertices
        self.speed = speed

    def getVertices(self):
        return self.vertices

    def getEdge(self, u,v):
        pos1 = v.getPosition()
        pos2 = u.getPosition()
        x1= pos1[0]
        x2 = pos2[0]
        y1 = pos1[1]
        y2 = pos2[1]

        return self.speed*(abs(x2-x1) + abs(y2-y1))
