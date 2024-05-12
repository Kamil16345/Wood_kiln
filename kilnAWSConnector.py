import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
from datetime import datetime
import stemmaSensor
import DHT11Sensor

def on_connect(self, client, userdata, flags, rc):
    print("Połączono z AWS IoT: " + str(rc))
    
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.tls_set(ca_certs='./AWS/certs/rootCA.pem', certfile='./AWS/certs/certificate.pem.crt', keyfile='./AWS/certs/private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3brw4p921o1fh-ats.iot.eu-west-1.amazonaws.com", 8883, 60)

def publishWoodData(data):
    while True:
        woodHumidity = stemmaSensor.measureHumidity()
        woodTemperature = stemmaSensor.measureTemperature()
        airHumidity = DHT11Sensor.getMockupHumidity()
        airTemperature = DHT11Sensor.getMockupTemperature()
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")
        
        data = {
            "woodHumidity": woodHumidity,
            "woodTemperature": woodTemperature,
            "airHumidity": airHumidity,
            "airTemperature": airTemperature,
            "timestamp": dt_string
        }
        
        client.publish("kiln/data", payload=json.dumps(data), qos=0, retain=False)
        print(data)
        time.sleep(1)
    # return
        
_thread.start_new_thread(publishWoodData,("Utworzono nowy wątek...",))

client.loop_forever()