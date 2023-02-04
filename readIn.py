# ADADPTED FROM https://www.tutorialspoint.com/opencv-python-how-to-display-the-coordinates-of-points-clicked-on-an-image

# import the required library
import cv2
import tkinter as tk
from Graph import GraphClass, Vertex
from tkinter import simpledialog

ROOT = tk.Tk()

ROOT.withdraw()
Wean5 = GraphClass('Wean-5', 3)
Connections = []
allLines = []
# define a function to display the coordinates of

# of the points clicked on the image
def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
      line = ''
      position = (x,y)
      print(position)
      
      # the input dialog
      room_num = simpledialog.askstring(title="Graph Collection Phase",
                                  prompt="Enter Room number")
      
      cv2.putText(img, room_num, (x, y),
      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

      adjacent_vertices_text = simpledialog.askstring(title="Graph Collection Phase",
                                  prompt="Enter adjacent vertices")

      v = Vertex((x,y), room_num)
      Wean5.addVertex(v)

      adjacent_vertices = adjacent_vertices_text.split(',')
      for a in adjacent_vertices:
         if a != room_num:
            Connections.append((room_num,a))

      # NOW SCAN THROUGH ADJACENT VERTICES
      
      '''
      # put coordinates as text on the image
      cv2.putText(img, f'({x},{y})',(x,y),
      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      '''
      
      # draw point on the image
      cv2.circle(img, (x,y), 3, (0,255,255), -1)

      adjacent_vertices_string = ''
      for a in adjacent_vertices:
         adjacent_vertices_string += 'a' + ' '
      # 
      # ADD TO LINE
      line = room_num + ' ' + f'({x}, {y})' + ' ' + adjacent_vertices_string
      allLines.append(line)
 
# read the input image
img = cv2.imread('WEH-5.png')

# create a window
cv2.namedWindow('Point Coordinates')

# bind the callback function to window
cv2.setMouseCallback('Point Coordinates', click_event)

# display the image
while True:
   cv2.imshow('Point Coordinates',img)
   k = cv2.waitKey(1) & 0xFF
   if k == 27:
      break
cv2.destroyAllWindows()







for connection in Connections:
   node1 = Wean5.findNode(connection[0])
   node2 = Wean5.findNode(connection[1])
   Wean5.addEdge(node1, node2)

# NOW READ TO TEXT FILE
# FIRST GENERATE LINES
'''
allVertices = Wean5.getVertices()
allLines = []
for v in allVertices:
   line = ''
   neighbors = v.getNeighbors()
   room = v.getName()
   coordinates = v.getPosition()
   
   # FIRST ADD NAME
   line += room + ' '
   
   # THEN ADD POSITIONS
   line += (str(coordinates[0]), str(coordinates[1]))
   '''




