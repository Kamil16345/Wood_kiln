import time
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT) #ENA
GPIO.setup(16, GPIO.OUT) #IN1
GPIO.setup(20, GPIO.OUT) #IN2

LEFT_LIMIT_SWITCH_PIN = 27
RIGHT_LIMIT_SWITCH_PIN = 22

motors = GPIO.PWM(12,50) # Note, 12 is pin, 50 = 50Hz pulse
motors.start(0)
GPIO.output(16, 1)
GPIO.output(20, 0)

left_rotate_dc_motor=26
right_rotate_dc_motor=18

power_on_dc_motors=19
power_on_fan=13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(right_rotate_dc_motor, GPIO.OUT)
GPIO.setup(left_rotate_dc_motor, GPIO.OUT)
GPIO.setup(power_on_dc_motors, GPIO.OUT)
GPIO.setup(power_on_fan, GPIO.OUT)
GPIO.setup(LEFT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class TwoMotorsControl:
    try:
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
    except:
        # GPIO.cleanup()
        print("Ending")
            
    def __init__(self, pwm):
        self.pwm=pwm
        
    def closeAllRelays():
        GPIO.output(left_rotate_dc_motor, True)
        GPIO.output(right_rotate_dc_motor, True)
        GPIO.output(power_on_dc_motors, True)
        GPIO.output(power_on_fan, True)
                    
    def openHatch(self):
        try:
            motors.ChangeDutyCycle(self.pwm)
            while GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                GPIO.output(power_on_dc_motors, False)
                GPIO.output(left_rotate_dc_motor, False)
                time.sleep(1)
        except Exception as e:
            print("Error occurred: ", e)
        finally:
            TwoMotorsControl.closeAllRelays()
            
    def closeHatch(self):
        try:
            motors.ChangeDutyCycle(self.pwm)
            while GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                GPIO.output(power_on_dc_motors, False)
                GPIO.output(right_rotate_dc_motor, False)
                time.sleep(1)
        except Exception as e:
            print("Error occurred: ", e)
        finally:
            TwoMotorsControl.closeAllRelays()

    def startTheFan(self):
        try:
            motors.ChangeDutyCycle(5)
            GPIO.output(power_on_dc_motors, False)
            GPIO.output(power_on_fan, False)
        except Exception as e:
            print("Error occurred: ", e)
            
    def stopTheFan(self):
        try:
            motors.ChangeDutyCycle(self.pwm)
            GPIO.output(power_on_dc_motors, True)
            GPIO.output(power_on_fan, True)
        except Exception as e:
            print("Error occurred: ", e)

    if __name__ == "__main__":
        if len(sys.argv) > 1 and sys.argv[1] == "closeHatch":
            closeHatch()
        if len(sys.argv) > 1 and sys.argv[1] == "openHatch":
            openHatch()
        if len(sys.argv) > 1 and sys.argv[1] == "startTheFan":
            startTheFan()
