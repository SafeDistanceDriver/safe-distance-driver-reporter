# Standard imports
import datetime
import json
import os
import time
import requests

# Third party imports
import RPi.GPIO as GPIO

# Constants
TRIG_PIN = 23
API_HEADER = {'content-type': 'application/json'}
API_URL = 'http://codejam.zrimsek.com/api/stats'
MIN_THROTTLE = 0
MAX_THROTTLE = 1
MIN_SPEED = 0
MAX_SPEED = 60
ROUND_DISTANCE = 1
ROUND_SPEED = 1
ROUND_RATING = 1

# Global variables
lastThrottle = 0

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.output(TRIG_PIN, False)


def getDistance():
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    time.sleep(.1)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    GPIO.setup(TRIG_PIN, GPIO.IN)
    while GPIO.input(TRIG_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(TRIG_PIN) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, ROUND_DISTANCE)


def calculateSpeed(throttle):
    throttleRange = (MAX_THROTTLE - MIN_THROTTLE)
    if throttleRange == 0:
        speed = MIN_SPEED
    else:
        speedRange = (MAX_SPEED - MIN_SPEED)
        speed = (((throttle - MIN_THROTTLE) * speedRange) /
                 throttleRange) + MIN_SPEED
    return round(speed, ROUND_SPEED)


def calculateTimeToStop(speed, distance):
    if(speed == 0):
        speed = 0.001
    timeToStop = 1 / (speed * 5280/3600 / distance)
    return round(timeToStop, 2)


def calculateRating(timeToStop):
    rating = 0
    if(timeToStop > 4):
        rating = 100
    else:
        rating = timeToStop*25
    return round(rating, ROUND_RATING)


def getThrottle():
    global lastThrottle
    throttle = lastThrottle

    # Grab throttle data
    pathToThrottleData = os.path.dirname(
        os.path.realpath(__file__)) + '/throttle-data.txt'
    with open(pathToThrottleData) as throttleFile:
        throttleData = throttleFile.readlines()

    for line in throttleData:
        if(line.startswith('throttle ')):
            startIndex = line.find(' ')
            throttle = float(line[startIndex + 1:-2])
            lastThrottle = throttle

    # Clear file contents
    open(pathToThrottleData, 'w').close()

    return round(throttle, 2)


def startDataCollection():
    time.sleep(1)
    while True:
        # Get distance
        distance = getDistance()

        # Get speed
        throttleValue = '-10'
        while throttleValue == '-10':
            throttleValue = getThrottle()
        speed = round(calculateSpeed(abs(throttleValue)), ROUND_SPEED)

        # Get time
        timeString = datetime.datetime.now().isoformat()

        # Get rating
        rating = round(calculateRating(
            calculateTimeToStop(speed, distance)), ROUND_RATING)

        # Print data
        output = "distance: " + \
            str(distance) + "\tspeed: " + \
            str(speed) + "\trating: " + str(rating)
        print(output.expandtabs(10))

        # Send to API
        body = {
            'distance': distance,
            'speed': speed,
            'time': timeString,
            'rating': rating
        }
        requests.post(API_URL, data=json.dumps(body), headers=API_HEADER)


startDataCollection()
