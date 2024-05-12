import RPi.GPIO as GPIO
import time
import twoMotorsControl
    
if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)
    
LEFT_LIMIT_SWITCH_PIN = 27
RIGHT_LIMIT_SWITCH_PIN = 22

GPIO.setup(LEFT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_LIMIT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def openHatch():
    try:
        while GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            print("Otwieranie wywietrznika dachowego...")
            if GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                twoMotorsControl.openHatch()
        while not GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            print("Otwarto wywietrznik dachowy!")
            break
    except Exception as e:
        print("Błąd podczas otwierania wywietrznika dachowego: ", e)
    finally:
        GPIO.cleanup()

def closeHatch():
    try:
        while GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            print("Zamykanie wywietrznika dachowego...")
            if GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
                twoMotorsControl.closeHatch()
        while not GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
            print("Zamknięto wywietrznik dachowy!")
            break
    except Exception as e:
        print("Błąd podczas zamykania wywietrznika dachowego: ", e)
    finally:
        GPIO.cleanup()

def getHatchState():
    if GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH & GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Zamkykanie/otwieranie"
    elif GPIO.input(LEFT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Otwarty"
    elif GPIO.input(RIGHT_LIMIT_SWITCH_PIN) == GPIO.HIGH:
        return "Zamknięty"
    else:
        return "Stan niezdefiniowany"