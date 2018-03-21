import RPi.GPIO as GPIO
import time
import datetime

import requests
import json

headers = {'content-type': 'application/json'}
url = 'http://codejam.zrimsek.com/api/stats'

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

TRIG = 23

print "Distance Measurement in Progress"
GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,False)
print "Waiting for sensor to settle"
time.sleep(1)

while True:
        print "Distance Measurement in Progress"
        GPIO.setup(TRIG,GPIO.OUT)
        print "Waiting for sensor to settle"
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
        print "Distance:",distance,"cm"
        timeString = datetime.datetime.now().isoformat()
        data = {'distance': distance, 'speed': 30, 'time': timeString}
        requests.post(url, data=json.dumps(data), headers=headers)
