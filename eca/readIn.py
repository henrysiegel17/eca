# ADADPTED FROM https://www.tutorialspoint.com/opencv-python-how-to-display-the-coordinates-of-points-clicked-on-an-image

# import the required library
import cv2
import tkinter as tk
from tkinter import simpledialog

ROOT = tk.Tk()

ROOT.withdraw()

# define a function to display the coordinates of

# of the points clicked on the image
def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
      position = (x,y)
      print(position)
      
      # the input dialog
      room_num = simpledialog.askstring(title="Graph Collection Phase",
                                  prompt="Enter Room number")
      
      '''
      # put coordinates as text on the image
      cv2.putText(img, f'({x},{y})',(x,y),
      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      '''
      
      # draw point on the image
      cv2.circle(img, (x,y), 3, (0,255,255), -1)
 
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
