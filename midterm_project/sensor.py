import RPi.GPIO as GPIO
import time

def distance():
    GPIO.setmode(GPIO.BCM)
    GPIO_TRI = 23
    GPIO_ECHO = 24
    GPIO.setup(GPIO_TRI,GPIO.OUT)
    GPIO.setup(GPIO_ECHO,GPIO.IN)
    # set Trigger to HIGH
    GPIO.output(23, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(23, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(24) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(24) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    GPIO.cleanup()
    
    return distance