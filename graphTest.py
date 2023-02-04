import PySimpleGUI as sg

point_from=(None,None)
point_to=(None,None)
# point_from=(50,-300)
# point_to=(500,-300)

layout2 = [
           [sg.Graph((1328,600),(0,-600),(1328,0),key='graph',enable_events=True)]
        ]

window2 = sg.Window("Route Finder", layout2, margins=(0, 0), finalize=True)
graph = window2['graph']
graph.draw_image(filename = r'C:\Users\1234l\Documents\Documents\CMU\Tartanhacks\maps\wean5.png', location = (0, 0))

while True:
    event, values = window2.read()

    if event==sg.WIN_CLOSED:
        break
    if event=='graph':
        mouse=values['graph']
        if mouse==(None,None): 
                continue
        elif point_from==(None,None):
                point_from=mouse
        elif point_from!=(None,None) and point_to==(None,None):
                point_to=mouse
                for i in range(0,1,0.01):
                    graph.draw_line(point_from,point_to, color = "red", width = 2)
        elif point_from!=(None,None) and point_to!=(None,None):
                point_from=mouse
                point_to=(None,None)

        
window2.close() 

