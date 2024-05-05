import twoMotorsControl
import radiatorControl
import sys
import DHT11_sensor
import time

fan = twoMotorsControl.TwoMotorsControl(20)
openHatch = twoMotorsControl.TwoMotorsControl(20)
closeHatch = twoMotorsControl.TwoMotorsControl(30)

def startDrying():
    while True:
        temp = DHT11_sensor.getMockupTemperature()
        print("Temperatura: " + str(temp))
        if temp is not None and temp >= 27:
            print("Wietrzenie suszarni")
            radiatorControl.stopRadiator()
            openHatch.openHatch()
            fan.startTheFan()
        if temp is not None and temp < 27:
            print("Nagrzewanie suszarni")
            fan.stopTheFan()
            closeHatch.closeHatch()
            radiatorControl.runRadiator()
        if temp == None:
            print("Błąd pomiaru, kontunuowanie algorytmu suszenia.")
            continue
        time.sleep(15)
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "startDrying":
        startDrying()