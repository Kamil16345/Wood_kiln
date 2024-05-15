import time
from board import SCL, SDA
import busio
import sys
from adafruit_seesaw.seesaw import Seesaw

i2c_bus=busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

counter = 0
humidityAccumulated=0


def measureHumidity():
    woodHumidity = ss.moisture_read()
    convertedWoodHumidity = (woodHumidity*40)/1015
    # print("Wilgotnosc_drewna: " + str(touch))
    return convertedWoodHumidity
    
def measureTemperature():
    temp = ss.get_temp()
    return round(temp,2)
    
def other():
    while True:
        touch = ss.moisture_read()
        temp = ss.get_temp()
        print("Temperatura drewna: " + str(temp) + ", wilgotność drewna: " + str(touch))
        humidityAccumulated = humidityAccumulated + touch
        counter=counter + 1
        
        if counter > 60:
            counter=0
            file1 = open("stemma_sensor_data.txt", "a")
            file1.write(str(humidityAccumulated/60) + '\n')
            humidityAccumulated = 0
            
        file1 = open("MyFile.txt", "w")
        time.sleep(1)
        
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "measureHumidity":
        measureHumidity()
    if len(sys.argv) > 1 and sys.argv[1] == "measureTemperature":
        measureTemperature()