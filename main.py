import PySimpleGUI as sg
import math
import wean_porter

sg.theme('Dark Teal 2')

def getLocation(location,destination):
        imgfile=None
        location=location.split(' ')
        destination=destination.split(' ')
        room=location[4]
        if room.isdigit():
                room=int(room)
        else: room=5000


        if location[3]=='Wean':
                floor= room//1000
                
                if floor==5:
                        imgfile=r'C:\Users\1234l\Documents\Documents\CMU\Tartanhacks\maps\wean5.png'
                if floor==8:
                        imgfile=r'C:\Users\1234l\Documents\Documents\CMU\Tartanhacks\maps\wean8.png'

                #Turn room number into a point
                # line = room_num + ' ' + f'{x}, {y}' + ' ' + adjacent_vertices_string
                room=str(room)
                goal = str(destination[4])
                
        return (imgfile,wean_porter.weanPorter(room, goal))


layout = [[sg.Text("Hello from the Contrapositives")], 
        [sg.Text('Enter Your Current Location', size =(30, 1))],
        [sg.Combo(values=['Porter','Wean'], size=(10, 2), key='-Location_Building-'), sg.InputText(key='-Location-')],
        [sg.Text('Enter Your Desired Destination', size =(30, 1))],
        [sg.Combo(values=['Porter','Wean'], size=(10, 2), key='-Destination_Building-'), sg.InputText(key='-Destination-')],
        [sg.Submit(), sg.Cancel()]
        ]


# Create the window
window = sg.Window("Route Finder", layout, margins=(300, 300))
while True:
    event, values = window.read()

    if event in (None,'Cancel','Submit') or event==sg.WIN_CLOSED:
        Location = 'Your location is ' + values['-Location_Building-'] 
        Location+= ' ' + values['-Location-']
        Destination = 'Your destination is ' + values['-Destination_Building-'] 
        Destination += ' ' + values['-Destination-']
        break


window.close() 

# print(repr(Location))
# print(repr(Destination))
(file,points) = getLocation(Location,Destination)
# (point_from,file)=getLocation(Location)
# (point_to,fileLast)=getLocation(Destination)


layout2 = [[sg.Text(text=Location),sg.Text(text=Destination),sg.Button('Continue')],
           [sg.Graph((1328,600),(0,-600),(1328,0),key='graph',enable_events=True)]
        ]

window2 = sg.Window("Route Finder", layout2, margins=(0, 0), finalize=True)
graph = window2['graph']
graph.draw_image(filename = file, location = (0, 0))

for point in range(len(points)-1):
        point_from=point
        point_to=point+1
        graph.draw_line(point_from,point_to, color = "red", width = 2)
        


while True:
    event, values = window2.read()

    if event==sg.WIN_CLOSED or event=='Continue':
        break
    if event=='graph':
        pass

window2.close() 

