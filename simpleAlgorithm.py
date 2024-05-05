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
        humidity = DHT11_sensor.getMockupHumidity()
        print("Temperatura powietrza: " + str(temp))
        print("Wilgotność powietrza: " + str(humidity))
        
        if humidity is not None and humidity >= 85:
            print("Wietrzenie suszarni")
            radiatorControl.stopRadiator()
            openHatch.openHatch()
            fan.startTheFan()
        if humidity is not None and humidity < 85:
            print("Nagrzewanie suszarni")
            fan.stopTheFan()
            closeHatch.closeHatch()
            radiatorControl.runRadiator()
        if humidity == None:
            print("Błąd pomiaru, kontunuowanie algorytmu suszenia.")
            continue
        time.sleep(1)
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "startDrying":
        startDrying()
        
# 700 - drewno wysuszone