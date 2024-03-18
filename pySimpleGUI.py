import PySimpleGUI as sg
import RPi.GPIO as GPIO
import time

layout = [[sg.Text('Zarządzanie suszarnią')],
          [sg.Button('Uruchom wiatrak')],
          [sg.Button('Zatrzymaj wiatrak')],
          [sg.Button('Włącz grzałkę')],
          [sg.Button('Wyłącz grzałkę')],
          [sg.Button('Uchyl klapę')],
          [sg.Button('Zamknij klapę')],
          [sg.Button('Rozpocznij suszenie')],
          [sg.Button('Ok')]]

window = sg.Window('Suszarnia', layout)
led1=21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Uruchom wiatrak':
        while True:
            GPIO.output(led1, True)
            time.sleep(.1)
            GPIO.output(led1, False)
            time.sleep(.1)
    if event == "Zatrzymaj wiatrak":
        break
window.close()