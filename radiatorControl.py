import time
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) #ENB
GPIO.setup(24, GPIO.OUT) #IN3
GPIO.setup(25, GPIO.OUT) #IN4

fan = GPIO.PWM(23, 50)
fan.start(0)
GPIO.output(24, 1)
GPIO.output(25, 0)

door_limit_switch = 6
GPIO.setup(door_limit_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def runRadiator():
    try:
        if GPIO.input(door_limit_switch) == GPIO.LOW:
            fan.ChangeDutyCycle(100)
        if GPIO.input(door_limit_switch) == GPIO.HIGH:
            print("Drzwi są otwarte. Zamknij drzwi!")
    except Exception as e:
        print("Error occurred: ", e)
        
def stopRadiator():
    try:
        fan.ChangeDutyCycle(0)
    except Exception as e:
        print("Error occurred: ", e)
        
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "runRadiator":
        runRadiator()