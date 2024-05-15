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

header = [[sg.Text('Zarządzanie suszarnią')]]
leftColumn = [[sg.Button('Uruchom wiatrak')],
          [sg.Button('Zatrzymaj wiatrak')],
          [sg.Button('Włącz grzałkę')],
          [sg.Button('Wyłącz grzałkę')],
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
        if dryingAlgorithm.stopThread:
            print("Drying thread nie działa...")
            woodHum = str(round(dryingAlgorithm.woodHumidity, 2))
            woodTemp = str(round(dryingAlgorithm.woodTemperature, 2))
            airHum = str(round(dryingAlgorithm.airHumidity, 2))
            airTemp = str(round(dryingAlgorithm.airTemperature, 2))
        else:
            print("Drying thread działa...")
            woodHum = str(round(stemmaSensor.measureHumidity(), 2))
            woodTemp = str(round(stemmaSensor.measureTemperature(), 2))
            airHum = str(round(DHT11Sensor.getMockupHumidity(), 2))
            airTemp = str(round(DHT11Sensor.getMockupTemperature(), 2))

        print("Refresh thread działa...")
        window['woodHumidity'].update(value = "Wilgotność drewna: " + woodHum + "%")
        window['woodTemperature'].update(value = "Temperatura drewna: " + woodTemp + "°C")
        window['airHumidity'].update(value = "Wilgotność powietrza w suszarni: " + airHum + "%")
        window['airTemperature'].update(value = "Temperatura powietrza w suszarni: " + airTemp + "°C")
        window['hatchState'].update(value = "Wywietrznik dachowy: " + limitSwitch.getHatchState())
        window['fanState'].update(value = "Wiatrak: " + "Wyłączony" if twoMotorsControl.fanValue == 0 else "Wiatrak: Włączony")
        window['radiatorState'].update(value = "Grzałki: " + "Wyłączone" if radiatorControl.radiatorValue == 0 else "Grzałki: Włączone")
        window['doorState'].update(value = "Drzwi: " + "Zamknięte" if GPIO.input(radiatorControl.door_limit_switch) == GPIO.LOW else "Drzwi: Otwarte")
        time.sleep(2)
    
refreshThread = threading.Thread(target=keepRefresh, daemon=True)
refreshThread.start()

while True:
    event, values = window.Read()
    window.refresh()
    if event == 'Uruchom wiatrak':
        fan = twoMotorsControl.TwoMotorsControl(4)
        fan.startTheFan()
        print("Uruchomiono wiatrak")
    if event == 'Zatrzymaj wiatrak':
        fan = twoMotorsControl.TwoMotorsControl(0)
        fan.stopTheFan()
        print("Zatrzymano wiatrak")
    if event == 'Włącz grzałkę':
        # if GPIO.input(radiatorControl.door_limit_switch) == GPIO.HIGH:
        #     sg.popup("Drzwi są otwarte. Zamknij drzwi!")
        # elif GPIO.input(radiatorControl.door_limit_switch) == GPIO.LOW:
            radiatorControl.runRadiator()
            print("Włączono grzałkę")
    if event == 'Wyłącz grzałkę':
        print("Wyłączono grzałkę")
        radiatorControl.stopRadiator()
    if event == 'Otwórz wywietrznik':
        hatch = twoMotorsControl.TwoMotorsControl(20)
        hatch.openHatch()
        print("Otwieranie klapy")
    if event == 'Zamknij wywietrznik':
        hatch = twoMotorsControl.TwoMotorsControl(30)
        hatch.closeHatch()
        print("Zamykanie klapy")
    if event == 'Start':
        woodHumidity = values['woodHumidityValue']
        if not woodHumidity.isdigit or float(woodHumidity) < 8 or float(woodHumidity) > 40:
            sg.popup("Dozwolone tylko liczby z zakresu 8 ÷ 40")
        else:
            if dryingAlgorithm.stopThread == True:
                dryingAlgorithm.stopThread = False
            window['Start'].update(disabled=True)
            dryingThread = threading.Thread(target=dryingAlgorithm.startDrying, args=(float(values['woodHumidityValue']),), daemon=True)
            dryingThread.start()
            print("Trwa automatyczny proces suszenia drewna.")
            window['Start'].update(disabled=False)
    if event == 'Stop':
        window['Stop'].update(disabled=True)
        dryingAlgorithm.stopThread = True
        window['Stop'].update(disabled=False)
    if event in (None, 'Exit'):
        print("Event: None, exit")
        dryingAlgorithm.resetWholeKiln()
        GPIO.cleanup()
        break
    if event == sg.WIN_CLOSED or event == 'Zakończ':
        print("Zakończ")
        dryingAlgorithm.resetWholeKiln()
        GPIO.cleanup()
        window.close()
    time.sleep(.5)