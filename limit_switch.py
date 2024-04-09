import RPi.GPIO as GPIO
import time
import servo_control

GPIO.cleanup()

if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BOARD)

LEFT_LIMIT_SWITCH_PIN = 13
RIGHT_LIMIT_SWITCH_PIN = 15

GPIO.setup(LEFT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(29, GPIO.OUT)
servo = GPIO.PWM(29,5000)

def openHatch():
    try:
        while GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            time.sleep(.5)
            print("Otwieranie klapy...")
            if GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                servo_control.moveServo(servo, 6.5, True)
        while not GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            servo_control.moveServo(servo, 0, False)
            print("Otwarto klapę!")
            break
    except KeyboardInterrupt:
        print("\nExiting the script")
    finally:
        servo_control.moveServo(servo, 0, False)

def closeHatch():
    try:
        while GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            time.sleep(.5)
            print("Zamykanie klapy...")
            if GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                servo_control.moveServo(servo, 7.5, True)
        while not GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            servo_control.moveServo(servo, 0, False)
            print("Zamknięto klapę!")
            break
    except KeyboardInterrupt:
        print("\nExiting the script")
    finally:
        servo_control.moveServo(servo, 0, False)

def getHatchState():
    if GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH & GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Zamkykanie/otwieranie"
    elif GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Otwarta"
    elif GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Zamknięta"
    else:
        return "Stan niezdefiniowany"