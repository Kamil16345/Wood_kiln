import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
from datetime import datetime
import stemma_sensor
import DHT11_sensor

def on_connect(self, client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))
    


# client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.tls_set(ca_certs='./AWS/certs/rootCA.pem', certfile='./AWS/certs/certificate.pem.crt', keyfile='./AWS/certs/private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3brw4p921o1fh-ats.iot.eu-west-1.amazonaws.com", 8883, 60)

def publishWoodData(txt):
    ctr = 1
    while True:
        woodHumidity = stemma_sensor.measureHumidity()
        woodTemperature = stemma_sensor.measureTemperature()
        airHumidity = DHT11_sensor.getMockupHumidity()
        airTemperature = DHT11_sensor.getMockupTemperature()
        
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        data = {
            "woodHumidity": woodHumidity,
            "woodTemperature": woodTemperature,
            "airHumidity": airHumidity,
            "airTemperature": airTemperature,
            "date": dt_string
        }
        
        client.publish("raspi/data", payload=json.dumps(data), qos=0, retain=False)
        print(data)
        time.sleep(1)
        
_thread.start_new_thread(publishWoodData,("Spin-up new Thread...",))

client.loop_forever()