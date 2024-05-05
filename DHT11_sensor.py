import Adafruit_DHT
import RPi.GPIO as GPIO
import sys

if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)
    
sensor = Adafruit_DHT.DHT11
pin = 21

def getMockupTemperature():
    _, temperature = Adafruit_DHT.read_retry(sensor, pin, 2)
    # print("Temperatura powietrza w suszarni: " + str(temperature))
    return temperature

def getMockupHumidity():
    humidity, _ = Adafruit_DHT.read_retry(sensor, pin, 2)
    # print("Wilgotność powietrza w suszarni: " + str(humidity))
    return humidity

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "getMockupTemperature":
        getMockupTemperature()
    if len(sys.argv) > 1 and sys.argv[1] == "getMockupHumidity":
        getMockupHumidity()
