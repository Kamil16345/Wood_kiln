import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) #ENB
GPIO.setup(24, GPIO.OUT) #IN3
GPIO.setup(25, GPIO.OUT) #IN4

fan = GPIO.PWM(23, 50)
fan.start(0)
GPIO.output(24, 1)
GPIO.output(25, 0)

def runRadiator():    
    try:
        while True:
            fan.ChangeDutyCycle(100)
            time.sleep(0.5)
    except Exception as e:
        print("Error occurred: ", e)
    finally:
        GPIO.cleanup()
        
def stopRadiator():    
    try:
        while True:
            fan.ChangeDutyCycle(0)
            time.sleep(0.5)
    except Exception as e:
        print("Error occurred: ", e)
    finally:
        GPIO.cleanup()