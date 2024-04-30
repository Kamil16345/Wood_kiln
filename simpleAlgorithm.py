import twoMotorsControl
import radiatorControl
import sys
import dht11

fan = twoMotorsControl.TwoMotorsControl(10)
openHatch = twoMotorsControl.TwoMotorsControl(20)
closeHatch = twoMotorsControl.TwoMotorsControl(30)

def startDrying():
    temp = dht11.getMockupTemperature()
    while True:
        print("Temperatura: " + str(temp))
        if  temp >= 30:
            print("Wietrzenie suszarni")
            radiatorControl.stopRadiator()
            openHatch.openHatch()
            fan.startTheFan()
        if temp < 30:
            print("Nagrzewanie suszarni")
            fan.stopTheFan()
            radiatorControl.runRadiator()
            closeHatch.closeHatch()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "startDrying":
        startDrying()