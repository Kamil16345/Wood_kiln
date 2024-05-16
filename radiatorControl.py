import time
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) #ENB
GPIO.setup(24, GPIO.OUT) #IN3
GPIO.setup(25, GPIO.OUT) #IN4

radiator = GPIO.PWM(23, 50)
radiator.start(0)
GPIO.output(24, 1)
GPIO.output(25, 0)

door_limit_switch = 11
GPIO.setup(door_limit_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
radiatorValue = 0

def runRadiator():
    global radiatorValue
    try:
        if GPIO.input(door_limit_switch) == GPIO.LOW:
            radiator.ChangeDutyCycle(100)
            radiatorValue = 100
            print("Drzwi zamknięte, grzałki włączone.")
        if GPIO.input(door_limit_switch) == GPIO.HIGH:
            print("Drzwi są otwarte. Zamknij drzwi!")
            radiator.ChangeDutyCycle(0)
            radiatorValue = 0
    except Exception as e:
        print("Wystąpił błąd w metodzie radiatorControl.runRatiator(): ", e)
        
def stopRadiator():
    global radiatorValue
    try:
        radiator.ChangeDutyCycle(0)
        radiatorValue = 0
    except Exception as e:
        print("Wystąpił błąd w metodzie radiatorControl.stopRatiator(): ", e)
        
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "runRadiator":
        runRadiator()