from twoMotorsControl import TwoMotorsControl
import radiatorControl
import sys
import DHT11Sensor
import time
import stemmaSensor
import kilnAWSConnector
from datetime import datetime

fan = TwoMotorsControl(20)
openHatch = TwoMotorsControl(20)
closeHatch = TwoMotorsControl(30)

counter = 0
aggAirTemperature = 0
aggAirHumidity = 0
aggWoodTemperature = 0
aggWoodHumidity = 0

stopThread = False

def startDrying(dryingTarget):
    global counter
    airTemperature = DHT11Sensor.getMockupTemperature()
    airHumidity = DHT11Sensor.getMockupHumidity()
    
    woodTemperature = stemmaSensor.measureTemperature()
    woodHumidity = stemmaSensor.measureHumidity()
    
    if stopThread == True:
        print("Przerwano automatyczny proces suszenia.")
        emptyCounters()
        radiatorControl.stopRadiator()
        fan.stopTheFan()
        openHatch.closeHatch()
        return
    if woodHumidity > dryingTarget:
        counter += 1
        
        print("Wilgotność drewna: " + str(round(woodHumidity, 2)) + "%")
        print("Temperatura drewna: " + str(woodTemperature) + "°C")
        
        print("Wilgotność powietrza: " + str(airHumidity) + "%")
        print("Temperatura powietrza: " + str(airTemperature) + "°C")
        
        print("-----------------------------------------")
        
        aggregateAndPublishData(woodHumidity, woodTemperature, airHumidity, airTemperature, counter)
            
        if woodTemperature is not None and woodTemperature >= 35:
            print("Temperatura drewna >= 35 °C. Grzałki wyłączone.")
            radiatorControl.stopRadiator()
            checkAirHumidity(airHumidity)
            print("-----------------")
        elif woodTemperature is not None and woodTemperature < 34:
            print("Temperatura drewna < 34 °C. Grzałki włączone.")
            radiatorControl.runRadiator()
            checkAirHumidity(airHumidity)
            print("-----------------")
        elif woodTemperature == None or woodTemperature > 100:
            print("Błąd podczas odczytu temperatury drewna. Kontynuowanie algorytmu suszenia.")
    
        print("aggWoodHumidity: " + str(aggWoodHumidity))
        print("aggWoodTemperature: " + str(aggWoodTemperature))
        print("aggAirHumidity: " + str(aggAirHumidity))
        print("aggAirTemperature: " + str(aggAirTemperature))
        print("--------------------------")
        
        if counter == 10:
            emptyCounters()
            
        startDrying(dryingTarget)
    elif woodHumidity <= dryingTarget:
        print("Osiągnięto cel suszenia: " + str(dryingTarget) + "\n Koniec programu.")
        return
        
def checkAirHumidity(airHumidity):
    if airHumidity is not None and airHumidity >= 75 and airHumidity < 100:
        print("Wilgotność powietrza >= 75%. Wywietrznik otwarty.")
        radiatorControl.stopRadiator()
        openHatch.openHatch()
        fan.startTheFan()
    elif airHumidity is not None and airHumidity < 50:
        print("Wilgotność powietrza < 50%. Wywietrznik zamknięty.")
        # radiatorControl.runRadiator()
        openHatch.closeHatch()
        fan.stopTheFan()
    elif airHumidity == None or airHumidity > 100:
        print("Błąd podczas odczytu wilgotności powietrza. Kontynuowanie algorytmu suszenia.")
        
def aggregateAndPublishData(woodHumidity, woodTemperature, airHumidity, airTemperature, counter):
    global aggWoodHumidity, aggWoodTemperature, aggAirHumidity, aggAirTemperature
    
    if woodHumidity == None:
        aggWoodHumidity +=  aggWoodHumidity/counter
    else:
        aggWoodHumidity += woodHumidity
        
    if woodTemperature == None:
        aggWoodTemperature +=  aggWoodTemperature/counter
    else:
        aggWoodTemperature += woodTemperature
        
    if airHumidity == None:
        aggAirHumidity +=  aggAirHumidity/counter
    else:
        aggAirHumidity += airHumidity
    
    if airTemperature == None:
        aggAirTemperature +=  aggAirTemperature/counter
    else:
        aggAirTemperature += airTemperature
        
    print("Licznik: " + str(counter))
    
    if counter == 10:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d/%m/%Y, %H:%M:%S")
        date_struct_object = datetime.strptime(formatted_datetime, "%d/%m/%Y, %H:%M:%S")
        timestamp = time.mktime(date_struct_object.timetuple())
        
        data = {
            "woodHumidity": round(aggWoodHumidity/counter, 2),
            "woodTemperature": round(aggWoodTemperature/counter, 2),
            "airHumidity": round(aggAirHumidity/counter, 2),
            "airTemperature": round(aggAirTemperature/counter, 2),
            "timestamp": timestamp
        }
        
        kilnAWSConnector.publishWoodData(data)
    
def emptyCounters():
    global aggWoodHumidity, aggWoodTemperature, aggAirHumidity, aggAirTemperature, counter
    counter = 0
    aggAirTemperature = 0
    aggAirHumidity = 0
    aggWoodTemperature = 0
    aggWoodHumidity = 0

def startWarming():
    while True:
        temperature = DHT11Sensor.getMockupTemperature()
        humidity = DHT11Sensor.getMockupHumidity()
        print("Temperatura powietrza: " + str(temperature))
        print("Wilgotność powietrza: " + str(humidity))
        radiatorControl.runRadiator()
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "startDrying":
        startDrying(1)    
    if len(sys.argv) > 1 and sys.argv[1] == "startWarming":
        startWarming()
        
# 700 - drewno wysuszone