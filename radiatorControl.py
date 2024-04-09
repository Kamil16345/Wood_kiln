import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT) #ENA
GPIO.setup(16, GPIO.OUT) #IN1
GPIO.setup(20, GPIO.OUT) #IN2

radiator = GPIO.PWM(12,800) # Note, 12 is pin, 500 = 500Hz pulse
radiator.start(0)
GPIO.output(16, 0)
GPIO.output(20, 1)

try:
    while True:
        radiator.ChangeDutyCycle(1)
        time.sleep(0.5)

except:
    # radiator.stop()
    GPIO.cleanup()
    print("Ending")