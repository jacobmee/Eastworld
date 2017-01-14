import time
import threading
import Queue
import math
import RPi.GPIO as GPIO
import logging.config

from Actions.Action import Action
from Actions.RaspCarMovement import *

class RaspUltrasonicScan(Action, threading.Thread):
    # HC-SR04, the farest it can get is 4.5m.  Pin03 (GPIO02) for "Trig" and Pin05 (GPIO03) for "Echo"
    PIN_TRIGGER = 3
    PIN_ECHO = 5
    PIN_ROTATION = 36

    def __init__(self, adjustment_events, data):
        super(RaspUltrasonicScan, self).__init__()
        threading.Thread.__init__(self)
        self.adjustment_events = adjustment_events
        self.ultrasonic_data = data

    def checkdist(self):

        # Set trigger
        #logging.debug("Ultrasonic checkdist")
        GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
        # Wait for 15us
        time.sleep(0.000015)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        while not GPIO.input(self.PIN_ECHO):
            pass

        # Start counting
        t1 = time.time()
        while GPIO.input(self.PIN_ECHO):
            pass

        # Stop counting
        t2 = time.time()

        # Return cm
        distance = ((t2 - t1) * 34000 / 2)

        # Anything more than 450, means too far.
        if distance > 450:
            distance = 450

        #logging.debug("Ultrasonic checkdist: %d", distance)
        return distance

    def execute(self):
        super(RaspUltrasonicScan, self).execute()

        logging.debug('Ultrasonic scan initialize...')
        GPIO.setmode(GPIO.BOARD)
        # PIN3 for trigger
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT, initial=GPIO.LOW)
        # PIN5 for Echo
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.setup(self.PIN_ROTATION, GPIO.OUT)
        GPIO.output(self.PIN_ROTATION, GPIO.HIGH)
        p = GPIO.PWM(36, 50)  # 50HZ
        p.start(0)

        logging.info("GPIO SET: TRIGGER PIN[%s]" % self.PIN_TRIGGER)
        logging.info("GPIO SET: ECHO PIN[%s]" % self.PIN_ECHO)


        count = 0
        while self.running:

            scanning_data = {}
            #logging.debug("Ultrasonic Scan started")

            start_point = 2.5
            length = 10.0

            if count % 2 == 0:
                for i in range(30, 151, 15):
                    cycle = start_point + (length * (i)) / 180
                    p.ChangeDutyCycle(cycle)
                    time.sleep(0.02)

                    distance = 0
                    for j in range(0, 3):
                        distance = distance + self.checkdist()

                    scanning_data[i] = round(distance / 3)

                    p.ChangeDutyCycle(0)
                    time.sleep(0.02)
            else:
                for i in range(150, 29, -15):
                    cycle = start_point + (length * (i)) / 180
                    p.ChangeDutyCycle(cycle)
                    time.sleep(0.02)
                    distance = 0
                    for j in range(0, 3):
                        distance = distance + self.checkdist()

                    scanning_data[i] = round(distance / 3)

                    p.ChangeDutyCycle(0)
                    time.sleep(0.02)

            count += 1
            logging.debug("One ultrasonic scan finished")

            self.ultrasonic_data[time.time()] = scanning_data.copy()

            time.sleep(0.3)

    def finish(self):
        super(RaspUltrasonicScan, self).finish()

        #  Clean up the GPIO3, set to input.
        GPIO.setup(self.PIN_TRIGGER, GPIO.IN)
        GPIO.setup(self.PIN_ROTATION, GPIO.IN)
        logging.debug("Ultrasonic Scan cleaned: PIN[%d] & PIN[%d]" % (self.PIN_TRIGGER, self.PIN_ROTATION))