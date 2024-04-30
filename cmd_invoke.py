import optparse
import twoMotorsControl

fan = twoMotorsControl.TwoMotorsControl(4)
openHatch = twoMotorsControl.TwoMotorsControl(20)
closeHatch = twoMotorsControl.TwoMotorsControl(30)

parser = optparse.OptionParser()
parser.add_option('-f', dest="f", action=fan, default=False)
options, remainder = parser.parse_args()
print ("Flag={}".format(options.f)) 