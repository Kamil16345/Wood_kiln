# Import libraries
import RPi.GPIO as GPIO
import time

def moveServo(servo, acceleration, flag):
    if flag == True:
        # servo.start(0)
        # duty = 2
        # while duty <= 3:
            # print("Moving the servo, duty: ", duty)
        servo.ChangeDutyCycle(acceleration)
            # duty = duty + 1
    elif flag == False:
        servo.stop()
    else:
        servo.stop()