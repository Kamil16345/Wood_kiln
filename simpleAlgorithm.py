import twoMotorsControl
import radiatorControl
import sys
import DHT11_sensor
import time
import stemma_sensor

fan = twoMotorsControl.TwoMotorsControl(20)
openHatch = twoMotorsControl.TwoMotorsControl(20)
closeHatch = twoMotorsControl.TwoMotorsControl(30)

def startDrying(dryingTarget):
    air_temperature = DHT11_sensor.getMockupTemperature()
    air_humidity = DHT11_sensor.getMockupHumidity()
    
    wood_temperature = stemma_sensor.measureTemperature()
    wood_humidity = stemma_sensor.measureHumidity()
    
    if wood_humidity > dryingTarget:
        print("Temperatura powietrza: " + str(air_temperature) + "°C")
        print("Wilgotność powietrza: " + str(air_humidity) + "%")
        
        print("Temperatura drewna: " + str(wood_temperature) + "°C")
        print("Wilgotność drewna: " + str(wood_humidity) + "%")
        print("-----------------------------------------")
        
        if wood_temperature is not None and wood_temperature >= 35:
            print("Temperatura drewna >= 35 °C. Grzałki wyłączone.")
            radiatorControl.stopRadiator()
            checkAirHumidity(air_humidity)
            print("-----------------")
        elif wood_temperature is not None and wood_temperature < 34:
            print("Temperatura drewna < 34 °C. Grzałki włączone.")
            radiatorControl.runRadiator()
            checkAirHumidity(air_humidity)
            print("-----------------")
        elif wood_temperature == None:
            print("Błąd podczas odczytu temperatury drewna. Kontynuowanie algorytmu suszenia.")
        startDrying(dryingTarget)
    else:
        print("Osiągnięto cel suszenia: " + dryingTarget + "\n Koniec programu.")
        return
        
def checkAirHumidity(air_humidity):
    if air_humidity is not None and air_humidity >= 75 and air_humidity < 100:
        print("Osiągnięto wilgotność powietrza >= 75%. Wietrzenie makiety.")
        radiatorControl.stopRadiator()
        openHatch.openHatch()
        fan.startTheFan()
    elif air_humidity is not None and air_humidity < 50:
        print("Osiągnięto wilgotność powietrza < 50%. Koniec wietrzenia.")
        radiatorControl.stopRadiator()
        openHatch.closeHatch()
        fan.stopTheFan()
    elif air_humidity == None:
        print("Błąd podczas odczytu wilgotności powietrza. Kontynuowanie algorytmu suszenia.")
        
        
        
def startWarming():
    while True:
        temp = DHT11_sensor.getMockupTemperature()
        humidity = DHT11_sensor.getMockupHumidity()
        print("Temperatura powietrza: " + str(temp))
        print("Wilgotność powietrza: " + str(humidity))
        radiatorControl.runRadiator()
        time.sleep(3)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "startDrying":
        startDrying(10)    
    if len(sys.argv) > 1 and sys.argv[1] == "startWarming":
        startWarming()
        
        
# 700 - drewno wysuszone