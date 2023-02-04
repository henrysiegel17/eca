from matplotlib import pyplot as plt
import numpy as np

grid=[[1,2,3],[4,5,6],[7,8,9]]
grid = np.reshape(grid, (3,3))
fig, ax = plt.subplots()
ax.matshow(grid, cmap ="Blues")
plt.draw()
'''
#new window
layout2=[
        [sg.Text(text=Location),sg.Text(text=Destination)], 
        [sg.Image(r'C:\Users\1234l\Pictures\memes\xkcd\selection_bias.png', size=(200, 200))],
        #[sg.DrawImage(filename = r'C:\Users\1234l\Pictures\memes\xkcd\selection_bias.png', location = (100, 100))]
        ]
window2 = sg.Window("Map", layout2, margins=(300, 300))
event2, values2 = window2.read()'''

'''
#Should have a variable specific to amount of steps
for i in range(4):
        layoutMap=[
                [sg.Text(text=Location),sg.Text(text=Destination),sg.Button('Continue')],
                [sg.Graph((1328,600),(0,-600),(1328,0),key='graph',enable_events=True)]
        ]

        #Gets correct image file corrsponding to input
        #file = getImage(Location)


        windowMap = sg.Window("Route Finder", layoutMap, margins=(0, 0), finalize=True)
        graph = windowMap['graph']
        graph.draw_image(filename = r'C:\Users\1234l\Documents\Documents\CMU\Tartanhacks\wean8.png', location = (0, 0))

        while True:
                event, values = windowMap.read()

                if event==sg.WIN_CLOSED or event=='Continue':
                        #UPDATE LOCATION
                        break
        windowMap.close()
'''