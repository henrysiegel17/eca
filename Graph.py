class Vertex(object):

    def __init__(self, name, position):
        self.adjacentVertices = []
        self.position = position
        self.name = name

    def getNeighbors(self):
        return self.adjacentVertices

    def getPosition(self):
        return self.position

    def addNeighbor(self, u):
        self.adjacentVertices.append(u)

    def getName(self):
        return self.name

    def getPosition(self):
        return self.position

    
class GraphClass(object):
    def __init__(self, name, speed):
        self.name = name
        self.vertices = []
        self.speed = speed

    def getVertices(self):
        return self.vertices

    def addVertex(self, u):
        self.vertices.append(u)

    def addEdge(self, u,v):
        u.addNeighbor(v)
        v.addNeighbor(u)

    def getEdge(self, u,v):
        pos1 = v.getPosition()
        pos2 = u.getPosition()
        x1= pos1[0]
        x2 = pos2[0]
        y1 = pos1[1]
        y2 = pos2[1]

        return self.speed*(abs(x2-x1) + abs(y2-y1))

    def findNode(self, text):
        for i in range(len(self.vertices)):
            if text == self.vertices[i].getName():
                return self.vertices[i]
        return None