import PySimpleGUI as sg
import RPi.GPIO as GPIO
import time
import radiatorControl
import twoMotorsControl
import stemma_sensor
import DHT11_sensor
import limit_switch

twoMotorsControl.TwoMotorsControl.closeAllRelays()

header = [[sg.Text('Zarządzanie suszarnią')]]
leftColumn = [[sg.Button('Uruchom wiatrak')],
          [sg.Button('Zatrzymaj wiatrak')],
          [sg.Button('Włącz grzałkę')],
          [sg.Button('Wyłącz grzałkę')],
          [sg.Button('Otwórz wyłaz')],
          [sg.Button('Zamknij wyłaz')]]

middleColumn = [[sg.Text("----------------------------------------------------------------")],
                [sg.Text("Wilgotność drewna: " + str(stemma_sensor.measureHumidity()), k='woodHumidity')],
                [sg.Text("Temperatura drewna: " + str(stemma_sensor.measureTemperature()) + "°C", k='woodTemperature')],
                [sg.Text("Wilgotność powietrza w suszarni: " + str(DHT11_sensor.getMockupHumidity()) + "%", k='airHumidity')],
                [sg.Text("Temperatura powietrza w suszarni: " + str(DHT11_sensor.getMockupTemperature()) + "°C", k='airTemperature')],
                [sg.Text("Wyłaz dachowy: " + limit_switch.getHatchState(), k='hatchState')],
                [sg.Text("Wiatrak: " , k='fanState')],
                [sg.Text("Grzałka: Wyłączona" , k='fanState')],
                [sg.Text("Drzwi: Otwarte", k='doorState')]]

rightColumn = [[sg.Button('Sosna')],
               [sg.Button('Brzoza')]]

layout = [[sg.Column(header, vertical_alignment='center', justification='center', k='-H-')],
          [sg.Text("Tryb ręczny:", pad=((7, 0), None), background_color='#ede264', text_color='black'),
           sg.Text("Aktualne parametry:", pad=((195, 0), None), background_color='#ede264', text_color='black'),
           sg.Text("Dostępne programy suszenia:", pad=((80, 0), None), background_color='#ede264', text_color='black')],
          [sg.Column(leftColumn, vertical_alignment='top', pad=(None, None), k='-L-'),
           sg.Column(middleColumn, vertical_alignment='top', pad=((40, 0), None), k='-M-'),
           sg.Column(rightColumn, vertical_alignment='top', pad=((20, 0), None), k='-R-')],
          [sg.Push(), sg.Button('Zakończ')]]

window = sg.Window('Suszarnia', layout, size=(700,400))
# boolVal=1
# event, values = window.Read()
# while boolVal == 1:
#     print("1")
#     window['woodHumidity'].Update("Wilgotność drewna: " + stemma_sensor.measureHumidity())
#     time.sleep(1)
    
while True:
    print("111")
    event, values = window.Read()
    window.refresh()
    # hatchState=limit_switch.getHatchState()
    # window['hatchState'].update(hatchState)
    if event == 'Uruchom wiatrak':
        fan = twoMotorsControl.TwoMotorsControl(4)
        fan.startTheFan()
        print("Uruchomiono wiatrak")
    if event == 'Zatrzymaj wiatrak':
        fan = twoMotorsControl.TwoMotorsControl(0)
        fan.stopTheFan()
        print("Zatrzymano wiatrak")
    if event == 'Włącz grzałkę':
        print("Włączono grzałkę")
        radiatorControl.runRadiator()
    if event == 'Wyłącz grzałkę':
        print("Wyłączono grzałkę")
        radiatorControl.stopRadiator()
    if event == 'Otwórz wyłaz':
        hatch = twoMotorsControl.TwoMotorsControl(20)
        hatch.openHatch()
        print("Otwieranie klapy")
    if event == 'Zamknij wyłaz':
        hatch = twoMotorsControl.TwoMotorsControl(30)
        hatch.closeHatch()
        print("Zamykanie klapy")
    if event in (None, 'Exit'):
        print("None, exit")
        # twoMotorsControl.TwoMotorsControl.closeAllRelays()
        GPIO.cleanup()
        break
    if event == sg.WIN_CLOSED or event == 'Zakończ': # if user closes window or clicks cancel
        print("Zakoncz")
        twoMotorsControl.TwoMotorsControl.closeAllRelays()
        GPIO.cleanup()
        window.close()
    time.sleep(.5)
    

