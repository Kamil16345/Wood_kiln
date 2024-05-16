import PySimpleGUI as sg
import RPi.GPIO as GPIO
import time
import radiatorControl
import twoMotorsControl
import stemmaSensor
import DHT11Sensor
import limitSwitch
import dryingAlgorithm
import threading

twoMotorsControl.TwoMotorsControl.closeAllRelays()

GPIO.setmode(GPIO.BCM)

header = [[sg.Text('Zarządzanie suszarnią')]]
leftColumn = [[sg.Button('Uruchom wiatrak')],
          [sg.Button('Zatrzymaj wiatrak')],
          [sg.Button('Włącz grzałki')],
          [sg.Button('Wyłącz grzałki')],
          [sg.Button('Otwórz wywietrznik')],
          [sg.Button('Zamknij wywietrznik')]]

middleColumn = [[sg.Text("----------------------------------------------------------------")],
                [sg.Text("Wilgotność drewna: " + str(round(stemmaSensor.measureHumidity(), 2)) + "%", k='woodHumidity')],
                [sg.Text("Temperatura drewna: " + str(stemmaSensor.measureTemperature()) + "°C", k='woodTemperature')],
                [sg.Text("Wilgotność powietrza w suszarni: " + str(DHT11Sensor.getMockupHumidity()) + "%", k='airHumidity')],
                [sg.Text("Temperatura powietrza w suszarni: " + str(DHT11Sensor.getMockupTemperature()) + "°C", k='airTemperature')],
                [sg.Text("Wywietrznik dachowy: " + limitSwitch.getHatchState(), k='hatchState')],
                [sg.Text("Wiatrak: " + "Wyłączony" if twoMotorsControl.fanValue == 0 else "Włączony", k='fanState')],
                [sg.Text("Grzałki: " + "Wyłączone" if radiatorControl.radiatorValue == 0 else "Włączone", k='radiatorState')],
                [sg.Text("Drzwi: " + "Zamknięte" if GPIO.input(radiatorControl.door_limit_switch) == GPIO.LOW else "Drzwi: Otwarte", k='doorState')]]

rightColumn = [[sg.Text('Docelowa wilgotność: 8 ÷ 40%')],
               [sg.Input('', enable_events=True, key='woodHumidityValue', font=('Arial Bold', 10), expand_x=True, justification='left')],
               [sg.Button('Start'), sg.Button('Stop')]]

layout = [[sg.Column(header, vertical_alignment='center', justification='center', k='-H-')],
          [sg.Text("Tryb ręczny:", pad=((7, 0), None), background_color='#ede264', text_color='black'),
           sg.Text("Aktualne parametry:", pad=((195, 0), None), background_color='#ede264', text_color='black'),
           sg.Text("Tryb automatyczny:", pad=((80, 0), None), background_color='#ede264', text_color='black')],
          [sg.Column(leftColumn, vertical_alignment='top', pad=(None, None), k='-L-'),
           sg.Column(middleColumn, vertical_alignment='top', pad=((40, 0), None), k='-M-'),
           sg.Column(rightColumn, vertical_alignment='top', pad=((20, 0), None), k='-R-')],
          [sg.Push(), sg.Button('Zakończ')]]

window = sg.Window('Suszarnia', layout, size=(700,400))


event, values = window.Read()
window.refresh()

def keepRefresh():
    while True:
        woodHum = stemmaSensor.measureHumidity()
        woodTemp = stemmaSensor.measureTemperature()
        airHum = DHT11Sensor.getMockupHumidity()
        airTemp = DHT11Sensor.getMockupTemperature()
        
        woodHumVar = dryingAlgorithm.woodHumidity
        woodTempVar = dryingAlgorithm.woodTemperature
        airHumVar = dryingAlgorithm.airHumidity
        airTempVar = dryingAlgorithm.airTemperature
        
        if dryingAlgorithm.stopThread:
            print("Drying thread nie działa...")
            woodHumStr = str(round(woodHumVar, 2)) if not woodHumVar == None else str(0)
            woodTempStr = str(round(woodTempVar, 2)) if not woodTempVar == None else str(0)
            airHumStr = str(round(airHumVar, 2)) if not airHumVar == None else str(0)
            airTempStr = str(round(airTempVar, 2)) if not airTempVar == None else str(0)
        else:
            print("Drying thread działa...")            
            woodHumStr = str(round(woodHum, 2)) if not woodHum == None else str(0)
            woodTempStr = str(round(woodTemp, 2)) if not woodTemp == None else str(0)
            airHumStr = str(round(airHum, 2)) if not airHum == None else str(0)
            airTempStr = str(round(airTemp, 2)) if not airTemp == None else str(0)

        print("Refresh thread działa...")
        window['woodHumidity'].update(value = "Wilgotność drewna: " + woodHumStr + "%")
        window['woodTemperature'].update(value = "Temperatura drewna: " + woodTempStr + "°C")
        window['airHumidity'].update(value = "Wilgotność powietrza w suszarni: " + airHumStr + "%")
        window['airTemperature'].update(value = "Temperatura powietrza w suszarni: " + airTempStr + "°C")
        window['hatchState'].update(value = "Wywietrznik dachowy: " + limitSwitch.getHatchState())
        window['fanState'].update(value = "Wiatrak: " + "Wyłączony" if twoMotorsControl.fanValue == 0 else "Wiatrak: Włączony")
        window['radiatorState'].update(value = "Grzałki: " + "Wyłączone" if radiatorControl.radiatorValue == 0 else "Grzałki: Włączone")
        window['doorState'].update(value = "Drzwi: " + "Zamknięte" if GPIO.input(radiatorControl.door_limit_switch) == GPIO.LOW else "Drzwi: Otwarte")
        time.sleep(.5)
    
def disableButtons(buttonsToDisable):
    for i in range(0, len(buttonsToDisable)):
        window[buttonsToDisable[i]].update(disabled=True)
        
def enableButtons(buttonsToEnable):
    for i in range(0, len(buttonsToEnable)):
        window[buttonsToEnable[i]].update(disabled=False)
        
refreshThread = threading.Thread(target=keepRefresh, daemon=True)
refreshThread.start()
dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)

disableButtons(['Zatrzymaj wiatrak', 'Wyłącz grzałki', 'Stop'])

while True:
    event, values = window.Read()
    window.refresh()
    
    if event == 'Uruchom wiatrak':
        dryingAlgorithm.stopThread == True
        fan = twoMotorsControl.TwoMotorsControl(4)
        fan.startTheFan()
        print("Uruchomiono wiatrak.")
        enableButtons(['Zatrzymaj wiatrak'])
        disableButtons(['Uruchom wiatrak', 'Włącz grzałki', 'Wyłącz grzałki', 'Otwórz wywietrznik', 'Zamknij wywietrznik', 'Start', 'Stop'])
        dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)
    if event == 'Zatrzymaj wiatrak':
        dryingAlgorithm.stopThread == True
        fan = twoMotorsControl.TwoMotorsControl(0)
        fan.stopTheFan()
        print("Zatrzymano wiatrak.")
        disableButtons(['Zatrzymaj wiatrak', 'Wyłącz grzałki', 'Stop'])
        enableButtons(['Uruchom wiatrak', 'Włącz grzałki', 'Otwórz wywietrznik', 'Zamknij wywietrznik', 'Start'])
        dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)
    if event == 'Włącz grzałki':
        if GPIO.input(radiatorControl.door_limit_switch) == GPIO.HIGH:
            sg.popup("Drzwi są otwarte. Zamknij drzwi!")
        elif GPIO.input(radiatorControl.door_limit_switch) == GPIO.LOW:
            dryingAlgorithm.stopThread == True
            radiatorControl.runRadiator()
            print("Włączono grzałki.")
            disableButtons(['Uruchom wiatrak', 'Zatrzymaj wiatrak', 'Włącz grzałki', 'Otwórz wywietrznik', 'Zamknij wywietrznik', 'Start', 'Stop'])
            enableButtons(['Wyłącz grzałki'])
            dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)
    if event == 'Wyłącz grzałki':
        radiatorControl.stopRadiator()
        print("Wyłączono grzałki")
        disableButtons(['Zatrzymaj wiatrak', 'Wyłącz grzałki', 'Stop'])
        enableButtons(['Uruchom wiatrak', 'Włącz grzałki', 'Otwórz wywietrznik', 'Zamknij wywietrznik', 'Start'])
        dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)
    if event == 'Otwórz wywietrznik':
        dryingAlgorithm.stopThread = True
        hatch = twoMotorsControl.TwoMotorsControl(20)
        hatch.openHatch()
        print("Otwarto wywietrznik.")
        dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)
    if event == 'Zamknij wywietrznik':
        dryingAlgorithm.stopThread = True
        hatch = twoMotorsControl.TwoMotorsControl(35)
        hatch.closeHatch()
        print("Zamknięto wywietrznik.")
        dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(9),), daemon=True)
    if event == 'Start':
        woodHumidity = values['woodHumidityValue']
        if not woodHumidity.isdigit or float(woodHumidity) < 8 or float(woodHumidity) > 40:
            sg.popup("Dozwolone tylko liczby z zakresu 8 ÷ 40")
        else:
            if dryingAlgorithm.stopThread == True:
                dryingAlgorithm.stopThread = False
            dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(woodHumidity),), daemon=True)
            dryingThread.start()
            print("Trwa automatyczny proces suszenia drewna.")
            disableButtons(['Uruchom wiatrak', 'Zatrzymaj wiatrak', 'Włącz grzałki', 'Wyłącz grzałki', 'Otwórz wywietrznik', 'Zamknij wywietrznik', 'Start'])
            enableButtons(['Stop'])
    if event == 'Stop':
        dryingAlgorithm.stopThread = True
        disableButtons(['Stop', 'Zatrzymaj wiatrak', 'Wyłącz grzałki'])
        enableButtons(['Uruchom wiatrak', 'Włącz grzałki', 'Otwórz wywietrznik', 'Zamknij wywietrznik', 'Start'])
    if event in (None, 'Exit'):
        print("Event: None, exit")
        dryingAlgorithm.resetWholeKiln()
        dryingAlgorithm.stopThread == True
        GPIO.cleanup()
        break
    if event == sg.WIN_CLOSED or event == 'Zakończ':
        print("Zakończ")
        dryingAlgorithm.resetWholeKiln()
        dryingAlgorithm.stopThread == True
        GPIO.cleanup()
        window.close()
    time.sleep(.5)
