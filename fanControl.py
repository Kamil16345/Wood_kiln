import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) #ENB
GPIO.setup(24, GPIO.OUT) #IN3
GPIO.setup(25, GPIO.OUT) #IN4

fan = GPIO.PWM(23,50) # Note, 23 is pin, 500 = 500Hz pulse
fan.start(0)
GPIO.output(24, 1)
GPIO.output(25, 0)
try:
    while True:
        fan.ChangeDutyCycle(100)
        time.sleep(1)
except Exception as e:
    GPIO.cleanup()
    print("Wystąpił błąd w module fanControl.py: ", e)