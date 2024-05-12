import twoMotorsControl
import radiatorControl
import sys
import DHT11Sensor
import time
import stemmaSensor
import kilnAWSConnector
import datetime

fan = twoMotorsControl.TwoMotorsControl(20)
openHatch = twoMotorsControl.TwoMotorsControl(20)
closeHatch = twoMotorsControl.TwoMotorsControl(30)

def startDrying(dryingTarget):
    airTemperature = DHT11Sensor.getMockupTemperature()
    airHumidity = DHT11Sensor.getMockupHumidity()
    
    woodTemperature = stemmaSensor.measureTemperature()
    woodHumidity = stemmaSensor.measureHumidity()
    
    if woodHumidity > dryingTarget:
        print("Temperatura powietrza: " + str(airTemperature) + "°C")
        print("Wilgotność powietrza: " + str(airHumidity) + "%")
        
        print("Temperatura drewna: " + str(woodTemperature) + "°C")
        print("Wilgotność drewna: " + str(round(woodHumidity, 2)) + "%")
        print("-----------------------------------------")
        
        dateString = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        
        data = {
            "woodHumidity": woodHumidity,
            "woodTemperature": woodTemperature,
            "airHumidity": airHumidity,
            "airTemperature": airTemperature,
            "timestamp": dateString
        }
        
        kilnAWSConnector.publishWoodData(data)
        
        if woodTemperature is not None and woodTemperature >= 35:
            print("Temperatura drewna >= 35 °C. Grzałki wyłączone.")
            radiatorControl.stopRadiator()
            checkAirHumidity(airHumidity)
            print("-----------------")
        elif woodTemperature is not None and woodTemperature < 34:
            print("Temperatura drewna < 34 °C.")
            radiatorControl.runRadiator()
            checkAirHumidity(airHumidity)
            print("-----------------")
        elif woodTemperature == None or woodTemperature == None:
            print("Błąd podczas odczytu temperatury drewna. Kontynuowanie algorytmu suszenia.")
        startDrying(dryingTarget)
    elif woodHumidity <= dryingTarget:
        print("Osiągnięto cel suszenia: " + str(dryingTarget) + "\n Koniec programu.")
        return
        
def checkAirHumidity(airHumidity):
    if airHumidity is not None and airHumidity >= 75 and airHumidity < 100:
        print("Osiągnięto wilgotność powietrza >= 75%. Wietrzenie makiety.")
        radiatorControl.stopRadiator()
        openHatch.openHatch()
        fan.startTheFan()
    elif airHumidity is not None and airHumidity < 50:
        print("Osiągnięto wilgotność powietrza < 50%. Koniec wietrzenia.")
        radiatorControl.runRadiator()
        openHatch.closeHatch()
        fan.stopTheFan()
    elif airHumidity == None:
        print("Błąd podczas odczytu wilgotności powietrza. Kontynuowanie algorytmu suszenia.")
        
def startWarming():
    while True:
        temperature = DHT11Sensor.getMockupTemperature()
        humidity = DHT11Sensor.getMockupHumidity()
        print("Temperatura powietrza: " + str(temperature))
        print("Wilgotność powietrza: " + str(humidity))
        radiatorControl.runRadiator()
        time.sleep(3)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "startDrying":
        startDrying(1)    
    if len(sys.argv) > 1 and sys.argv[1] == "startWarming":
        startWarming()
        
# 700 - drewno wysuszone