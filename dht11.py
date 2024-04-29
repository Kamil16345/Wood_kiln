import Adafruit_DHT
import RPi.GPIO as GPIO

if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)
    
sensor = Adafruit_DHT.DHT11

pin = 21

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, 2)
    if humidity is not None and temperature is not None:
        print('Temp={0}*C  Humidity={1}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
