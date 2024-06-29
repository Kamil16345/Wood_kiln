import time
import sys
import random
import PySimpleGUI as sg
from datetime import datetime
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

import kilnAWSConnector

fourDaysMins=345600

# 1 dzień - 86400
# 2 dni - 172800
# 3 dni - 259200
# 4 dni - 345600

def simulateHumidity():
    woodHumidity = 39
    humidityTarget = 8

    start = time.time()
    print("Teraz jest: " + str(start))
    timeElapsed = 0

    timestampList=[]
    woodHumidityList=[]
    woodTemperatureList=[]
    airHumidityList=[]
    airTemperatureList=[]

    currentAirHumidity = 40
    airTemperature = 25
    woodTemperatureOffset = 0
    
    increasing=True
    sendDataToCloud=False
    
    while True:
        if timeElapsed < 43200: # 0-12H
            woodHumidity -= 0.0145
            offset = random.uniform(0, 1.9)
            woodHumidityWithOffset = woodHumidity + offset
            currentTime=datetime.fromtimestamp(start+timeElapsed)
            timestampList.append(currentTime)
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1, 1)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.2, .8)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.2, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)

            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timestamp: " + str(start+timeElapsed) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        # else:
        #     break
        if timeElapsed >= 43200 and timeElapsed < 86400: # 12-24H
            woodHumidity -= 0.0115
            offset = random.uniform(0, 1.7)
            woodHumidityWithOffset = woodHumidity + offset
            currentTime=datetime.fromtimestamp(start+timeElapsed)
            timestampList.append(currentTime)
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-.75, 1.2)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.2, .9)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.2, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timestamp: " + str(start+timeElapsed) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        # else:
        #     break
        if timeElapsed >= 86400 and timeElapsed < 129600: #24H-36H
            woodHumidity -= 0.009
            offset = random.uniform(0, 1.7)
            woodHumidityWithOffset = woodHumidity + offset
            timestampList.append(datetime.fromtimestamp(start+timeElapsed))
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1, .8)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.2, .7)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.1, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        
        if timeElapsed >= 129600 and timeElapsed < 172800: #36H-48H
            woodHumidity -= 0.0065
            offset = random.uniform(0, 1.5)
            woodHumidityWithOffset = woodHumidity + offset
            timestampList.append(datetime.fromtimestamp(start+timeElapsed))
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1.2, .8)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.1, .5)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-1, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        if timeElapsed >= 172800 and timeElapsed < 216000: #48H-60H
            woodHumidity -= 0.0055
            offset = random.uniform(0, 1.4)
            woodHumidityWithOffset = woodHumidity + offset
            timestampList.append(datetime.fromtimestamp(start+timeElapsed))
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1.5, .5)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.1, .4)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.3, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        if timeElapsed >= 216000 and timeElapsed < 259200: #60H-72H
            woodHumidity -= 0.004
            offset = random.uniform(0, 1.2)
            woodHumidityWithOffset = woodHumidity + offset
            timestampList.append(datetime.fromtimestamp(start+timeElapsed))
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1.6, .55)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.15, .25)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.1, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        if timeElapsed >= 259200 and timeElapsed < 302400: #72H-84H
            woodHumidity -= 0.0023
            offset = random.uniform(0, 1.1)
            woodHumidityWithOffset = woodHumidity + offset
            timestampList.append(datetime.fromtimestamp(start+timeElapsed))
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1.22, .85)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.19, .23)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.1, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        if timeElapsed >= 302400 and timeElapsed < 345600 or woodHumidityWithOffset < humidityTarget:
            woodHumidity -= 0.0022
            offset = random.uniform(0, 1.3)
            woodHumidityWithOffset = woodHumidity + offset
            # timestampList.append(int(start+timeElapsed))
            timestampList.append(datetime.fromtimestamp(start+timeElapsed))
            woodHumidityList.append(float(woodHumidityWithOffset))
            woodTemperatureOffset = random.uniform(-1.5, .5)
            woodTemperatureList.append(35 + woodTemperatureOffset)
            airTemperature = 35 + woodTemperatureOffset + random.uniform(0, 2.5)
            airTemperatureList.append(airTemperature)
            if increasing:
                currentAirHumidity += random.uniform(-.3, .2)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity >= 76:
                    increasing = False
            elif not increasing:
                currentAirHumidity-=random.uniform(-.1, 15)
                airHumidityList.append(currentAirHumidity)
                if currentAirHumidity < 40:
                    increasing=True
            if sendDataToCloud:                    
                sendDataToCloud(float(woodHumidityWithOffset), 35 + woodTemperatureOffset, currentAirHumidity, airTemperature, start+timeElapsed)
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            if woodHumidityWithOffset < humidityTarget:
                break
        if timeElapsed > 345600 or woodHumidityWithOffset < humidityTarget:
            print("Minęły 4 dni")
            # print("woodHumidityWithOffset: " + str(woodHumidityWithOffset) + " woodHumidity: " + str(woodHumidity) + " timeElapsed: " + str(timeElapsed) + " offset: " + str(offset))
            break
        # else:
        #     break
        # timeElapsed = timeElapsed + 1 #for every second interval
        timeElapsed = timeElapsed + 60

        datetime1 = datetime.fromtimestamp(start)
        datetime2 = datetime.fromtimestamp(start+timeElapsed)
        time_delta = datetime2 - datetime1
        hours = time_delta.total_seconds()/3600
        # print("timeElapsed: " + str(timeElapsed))
        # print("Czas suszenia: " + str(hours))
        # print(str(len(woodTemperatureList)))
        # print(str(len(airHumidityList)))
        
        # data = {
        #     "woodHumidity": float(woodHumidityWithOffset),
        #     "woodTemperature": 35 + woodTemperatureOffset,
        #     "airHumidity": currentAirHumidity,
        #     "airTemperature": airTemperature,
        #     "timestamp": datetime.fromtimestamp(start+timeElapsed)
        # }
        
        # kilnAWSConnector.publishWoodData(data)
        # timeElapsed = timeElapsed + 1 #for every second interval
        timeElapsed = timeElapsed + 60
        time.sleep(.00001)
    print(woodHumidityList)
    print("woodHumidityLength: " + str(len(woodHumidityList)))

def publish():
        data = {
            "woodHumidity": 22,
            "woodTemperature": 35,
            "airHumidity": 45,
            "airTemperature": 56,
            "timestamp": time.time()
        }
        
        kilnAWSConnector.publishWoodData(data)
def sendDataToCloud(woodHum, woodTemp, airHum, airTemp, timestamp):
    
    data = {
        "woodHumidity": woodHum,
        "woodTemperature": woodTemp,
        "airHumidity": airHum,
        "airTemperature": airTemp,
        "timestamp": timestamp
    }
    
    kilnAWSConnector.publishWoodData(data)
    
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "simulateHumidity":
        simulateHumidity()
    if len(sys.argv) > 1 and sys.argv[1] == "publish":
        publish()