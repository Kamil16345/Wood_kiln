import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT) #ENA
GPIO.setup(16, GPIO.OUT) #IN1
GPIO.setup(20, GPIO.OUT) #IN2


def openControllerOutput():
    try:
        radiator = GPIO.PWM(12,50) # Note, 12 is pin, 500 = 500Hz pulse
        radiator.start(0)
        GPIO.output(16, 1)
        GPIO.output(20, 0)
    except:
        GPIO.cleanup()
        print("Ending")
        
def openHatch():
    try:
        print("Hello world")
    except:
        GPIO.cleanup()
        print("Ending")
try:
    while True:
        radiator.ChangeDutyCycle(20)
except:
    GPIO.cleanup()
    print("Ending")