# Standard imports
import datetime
import json
import os
import time
import requests

# Third party imports
import RPi.GPIO as GPIO

# Constants
MIN_THROTTLE = 0
MAX_THROTTLE = 1
MIN_SPEED = 0
MAX_SPEED = 60

# Global variables
lastValue = 0

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIG = 23
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, False)

# API setup
headers = {'content-type': 'application/json'}
url = 'http://codejam.zrimsek.com/api/stats'


def calculateSpeed(throttle):
    throttleRange = (MAX_THROTTLE - MIN_THROTTLE)
    if throttleRange == 0:
        speed = MIN_SPEED
    else:
        speedRange = (MAX_SPEED - MIN_SPEED)
        speed = (((throttle - MIN_THROTTLE) * speedRange) /
                 throttleRange) + MIN_SPEED
    return speed


def calculateTimeToStop(speed, distance):
    if(speed == 0):
        speed = 0.001
    timeToStop = 1 / (speed * 5280/3600 / distance)
    return timeToStop


def calculateRating(timeToStop):
    rating = 0
    if(timeToStop > 4):
        rating = 100
    else:
        rating = timeToStop*25
    return rating


def getThrottleSpeed():
    global lastValue
    returnValue = lastValue
    path_to_data = os.path.dirname(
        os.path.realpath(__file__)) + '/throttle-data.txt'
    with open(path_to_data) as file:
        content = file.readlines()
    for line in content:
        if(line.startswith('throttle ')):
            startIndex = line.find(' ')
            returnValue = float(line[startIndex + 1:-2])
            lastValue = returnValue
    open(path_to_data, 'w').close()
    return returnValue


def startDataCollection():
    time.sleep(1)
    while True:
        GPIO.setup(TRIG, GPIO.OUT)
        time.sleep(.1)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        GPIO.setup(TRIG, GPIO.IN)
        while GPIO.input(TRIG) == 0:
            pulse_start = time.time()
        while GPIO.input(TRIG) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        timeString = datetime.datetime.now().isoformat()
        throttleValue = '-10'
        while throttleValue == '-10':
            throttleValue = getThrottleSpeed()
        speed = calculateSpeed(abs(throttleValue))
        rating = calculateRating(calculateTimeToStop(speed, distance))
        data = {
            'distance': distance,
            'speed': speed,
            'time': timeString,
            'rating': rating
        }
        print("distance: " + str(distance) + "\t\tspeed: " +
              str(speed) + "\t\trating: " + str(rating))
        requests.post(url, data=json.dumps(data), headers=headers)


startDataCollection()
