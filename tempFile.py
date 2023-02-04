import PySimpleGUI as sg

sg.theme('Dark Teal 2')

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
        Destination+= ' ' + values['-Destination-']
        break


window.close() 

layout2 = [[sg.Text(text=Location),sg.Text(text=Destination),sg.Button('Continue')],
           [sg.Graph((1328,600),(0,-600),(1328,0),key='graph',enable_events=True)]
        ]

window2 = sg.Window("Route Finder", layout2, margins=(0, 0), finalize=True)
graph = window2['graph']
graph.draw_image(filename = r'C:\Users\1234l\Documents\Documents\CMU\Tartanhacks\maps\wean5.png', location = (0, 0))
graph.draw_line((50,-400),(500,-400), color = "red", width = 2)

while True:
    event, values = window2.read()

    if event==sg.WIN_CLOSED or event=='Continue':
        break
    if event=='graph':
        pass

window2.close() 