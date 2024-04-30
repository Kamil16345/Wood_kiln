import Adafruit_DHT
import RPi.GPIO as GPIO
import sys

if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)
    
sensor = Adafruit_DHT.DHT11
pin = 21

def getMockupTemperature():
    _, temperature = Adafruit_DHT.read_retry(sensor, pin, 2)
    print(temperature)
    return temperature

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "getMockupTemperature":
        getMockupTemperature()
# while True:
#     humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, 2)
#     if humidity is not None and temperature is not None:
#         print('Temp={0}*C  Humidity={1}%'.format(temperature, humidity))
#     else:
#         print('Failed to get reading. Try again!')
