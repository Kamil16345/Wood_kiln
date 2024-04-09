# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

def warmUpServo():
    GPIO.setup(29,GPIO.OUT)
    servo = GPIO.PWM(29,50) # Note 29 is pin, 50 = 50Hz pulse
    servo.start(0) #start PWM running, but with value of 0 (pulse off)

    print ("Waiting for 2 seconds")
    time.sleep(2)

    #Let's move the servo!
    print ("Rotating 180 degrees in 10 steps")

    # Define variable duty
    duty = 2

    # Wait a couple of seconds
    time.sleep(2)

    # Turn back to 90 degrees
    print ("Turning back to 90 degrees for 2 seconds")
    servo.ChangeDutyCycle(7)
    time.sleep(2)

    #turn back to 0 degrees
    print ("Turning back to 0 degrees")
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

    #Clean things up at the end
    servo.stop()
    GPIO.cleanup()
    print ("Goodbye")

def moveServo(servo, acceleration, flag):
    if flag == True:
        servo.start(0)
        duty=1
        # duty = 2
        # while duty <= 3:
        #     print("Moving the servo, duty: ", duty)
        #     servo.ChangeDutyCycle(acceleration)
        #     duty = duty + 1
    elif flag == False:
        servo.stop()
    else:
        servo.stop()