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
    # while True:
    touch = ss.moisture_read()
    print("wilgotnosc_drewna: " + str(touch))
    return touch
    
def measureTemperature():
    # while True:
    temp = ss.get_temp()
    return round(temp,1)
    
def other():
    while True:
        touch = ss.moisture_read()
        temp = ss.get_temp()
        print("temp: " + str(temp) + " moisture: " + str(touch))
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