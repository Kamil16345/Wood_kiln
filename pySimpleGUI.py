import PySimpleGUI as sg
import RPi.GPIO as GPIO
import limit_switch

header = [[sg.Text('Zarządzanie suszarnią')]]
leftColumn = [[sg.Button('Uruchom wiatrak')],
          [sg.Button('Zatrzymaj wiatrak')],
          [sg.Button('Włącz grzałkę')],
          [sg.Button('Wyłącz grzałkę')],
          [sg.Button('Otwórz klapę')],
          [sg.Button('Zamknij klapę')]]

middleColumn = [[sg.Text("----------------------------------------------------------------")],
                [sg.Text("Wilgotność drewna: 100%", k='woodHumidity')],
                [sg.Text("Temperatura drewna: 100°C", k='woodTemperature')],
                [sg.Text("Wilgotność powietrza w suszarni: 100%", k='airHumidity')],
                [sg.Text("Temperatura powietrza w suszarni: 100°C", k='airTemperature')],
                [sg.Text("Klapa: Otwarta", k='hatchOpened')],
                [sg.Text("Wiatrak: Włączony", k='fanStatus')],
                [sg.Text("Drzwi: Otwarte", k='doorStatus')]]

rightColumn = [[sg.Button('Sosna')],
               [sg.Button('Brzoza')]]

layout = [[sg.Column(header, vertical_alignment='center', justification='center', k='-H-')],
          [sg.Text("Tryb ręczny:", pad=((7, 0), None), background_color='#ede264', text_color='black'),
           sg.Text("Aktualne parametry:", pad=((195, 0), None), background_color='#ede264', text_color='black'),
           sg.Text("Dostępne programy suszenia:", pad=((80, 0), None), background_color='#ede264', text_color='black')],
          [sg.Column(leftColumn, vertical_alignment='top', pad=(None, None), k='-L-'),
           sg.Column(middleColumn, vertical_alignment='top', pad=((40, 0), None), k='-M-'),
           sg.Column(rightColumn, vertical_alignment='top', pad=((20, 0), None), k='-R-')],
          [sg.Push(), sg.Button('Zakończ',  vertical_alignment='bottom')]]

window = sg.Window('Suszarnia', layout, size=(700,400))

while True:
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == 'Otwórz klapę':
        print("Otwieranie klapy")
        limit_switch.openHatch()
    if event == 'Zamknij klapę':
        print("Zamykanie klapy")
        limit_switch.closeHatch()
    if event == sg.WIN_CLOSED or event == 'Zakończ': # if user closes window or clicks cancel
        break
window.close()
