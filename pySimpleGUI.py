import PySimpleGUI as sg
import RPi.GPIO as GPIO
# import time
import limit_switch

layout = [[sg.Text('Zarządzanie suszarnią')],
          [sg.Button('Uruchom wiatrak')],
          [sg.Button('Zatrzymaj wiatrak')],
          [sg.Button('Włącz grzałkę')],
          [sg.Button('Wyłącz grzałkę')],
          [sg.Button('Uchyl klapę')],
          [sg.Button('Zamknij klapę')],
          [sg.Button('Rozpocznij suszenie')],
          [sg.Button('Zakończ')]]

window = sg.Window('Suszarnia', layout, size=(600,300))

while True:
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == 'Uchyl klapę':
        print("Otwieranie klapy")
        limit_switch.openHatch()
    if event == 'Zamknij klapę':
        print("Zamykanie klapy")
        limit_switch.closeHatch()
    if event == sg.WIN_CLOSED or event == 'Zakończ': # if user closes window or clicks cancel
        break
# led1=21

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(led1, GPIO.OUT)

# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED:
#         break
#     if event == 'Uruchom wiatrak':
#         while True:
#             GPIO.output(led1, True)
#             time.sleep(.1)
#             GPIO.output(led1, False)
#             time.sleep(.1)
#     if event == "Zatrzymaj wiatrak":
#         break
# window.close()



# Create the Window
# window = sg.Window('Window Title', layout)

# Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()

#     print('You entered ', values[0])

window.close()