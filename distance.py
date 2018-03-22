import RPi.GPIO as GPIO
import time
import datetime

import requests
import json
import os


def getThrottleSpeed():
        maxValue = -1
        path_to_tub_folders = os.path.dirname(os.path.realpath(__file__)) + '/data/'
        maxFolder = ''
        for root, dirs, files in os.walk(path_to_tub_folders, topdown=False):
            for name in dirs:
                if(name.startswith('tub_')):
                    startIndex = name.find('_')
                    endIndex = name.find('_', startIndex +1)
                    currentValue = int(name[startIndex + 1:endIndex])
                    if(currentValue > maxValue):
                        maxValue = currentValue
                        maxFolder = name
                        
        path_to_json = path_to_tub_folders + maxFolder + '/'
        maxJsonValue = -1
        maxJsonFile = ''
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

        for name in json_files:
                if(name.startswith('record_')):
                    startIndex = name.find('_')
                    currentValue = int(name[startIndex + 1:-5])
                    if(currentValue > maxJsonValue):
                        maxJsonValue = currentValue
                        maxJsonFile = name

        path_to_data = path_to_json + maxJsonFile
        json_data = open(path_to_data).read()

        data = json.loads(json_data)
        print("speed=",data["user/throttle"])
        return data["user/throttle"]

headers = {'content-type': 'application/json'}
url = 'http://codejam.zrimsek.com/api/stats'

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

TRIG = 23

print("Distance Measurement in Progress")
GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,False)
print("Waiting for sensor to settle")
time.sleep(1)

while True:
        print("Distance Measurement in Progress")
        GPIO.setup(TRIG,GPIO.OUT)
        print("Waiting for sensor to settle")
        time.sleep(.1)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)
        GPIO.setup(TRIG,GPIO.IN)
        while GPIO.input(TRIG)==0:
                pulse_start = time.time()
        while GPIO.input(TRIG)==1:
                pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance:",distance,"cm")
        timeString = datetime.datetime.now().isoformat()
        maxThrottleSpeed = getThrottleSpeed()
        data = {'distance': distance, 'speed': maxThrottleSpeed, 'time': timeString}
        requests.post(url, data=json.dumps(data), headers=headers)

                




















                
