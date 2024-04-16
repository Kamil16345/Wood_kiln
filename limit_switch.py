from gpiozero import Servo
import RPi.GPIO as GPIO
import time
    
if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)
    
LEFT_LIMIT_SWITCH_PIN = 27
RIGHT_LIMIT_SWITCH_PIN = 22

GPIO.setup(LEFT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def openHatch():
    GPIO.setmode(GPIO.BCM)
    servo_speed = 0
    servo = Servo(5)
    servo.value=servo_speed
    try:
        while GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            print("Otwieranie klapy...")
            if GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                time.sleep(0.5)
                if servo_speed < 0.9:
                    servo_speed+=0.1
                    servo.value = servo_speed
        while not GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            servo.value=0
            print("Otwarto klapę!")
            break
    except KeyboardInterrupt:
        print("\nExiting the script")
    finally:
        servo.value=0
        GPIO.cleanup()

def closeHatch():
    GPIO.setmode(GPIO.BCM)
    servo_speed = 0
    servo = Servo(5)
    servo.value=servo_speed
    try:
        while GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            print("Zamykanie klapy...")
            if GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                time.sleep(0.5)
                if servo_speed > -0.9:
                    servo_speed -= 0.1
                    servo.value = servo_speed
        while not GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            servo.value=0
            print("Zamknięto klapę!")
            break
    except KeyboardInterrupt:
        print("\nExiting the script")
    finally:
        servo.value=0
        GPIO.cleanup()

def getHatchState():
    if GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH & GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Zamkykanie/otwieranie"
    elif GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Otwarta"
    elif GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Zamknięta"
    else:
        return "Stan niezdefiniowany"