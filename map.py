MIN_THROTTLE = 0
MAX_THROTTLE = 1
MIN_SPEED = 0
MAX_SPEED = 60

def calculateSpeed(throttle):
    throttleRange = (MAX_THROTTLE - MIN_THROTTLE)
    if throttleRange == 0:
        speed = MIN_SPEED
    else:
        speedRange = (MAX_SPEED - MIN_SPEED)  
        speed = (((throttle - MIN_THROTTLE) * speedRange) / throttleRange) + MIN_SPEED
    return speed

speed = calculateSpeed(0.5)
print(speed)