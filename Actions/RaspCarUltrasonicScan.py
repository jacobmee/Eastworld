import time
import threading
import Queue
import RPi.GPIO as GPIO
import logging.config

from Actions.Action import Action
from Actions.RaspCarMovement import *

class RaspUltrasonicScan(Action, threading.Thread):

    # HC-SR04, the farest it can get is 4.5m.  Pin03 (GPIO02) for "Trig" and Pin05 (GPIO03) for "Echo"
    PIN_TRIGGER = 3
    PIN_ECHO = 5

    def __init__(self, block_events):
        super(RaspUltrasonicScan, self).__init__()
        threading.Thread.__init__(self)
        self.block_events = block_events
        self.recommend_direction = 0

    def run(self):
        self.execute()

    def checkdist(self):

        # Set trigger
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
        distance = (t2 - t1) * 34000 / 2

        # Anything more than 450, means too far.
        if distance > 450:
            distance = 10000

        return distance

    def execute(self):
        super(RaspUltrasonicScan, self).execute()

        logging.debug('Ultrasonic scan initialize...')
        GPIO.setmode(GPIO.BOARD)
        # PIN3 for trigger
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT, initial=GPIO.LOW)
        # PIN5 for Echo
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        logging.info("GPIO SET: TRIGGER PIN[%s]" % self.PIN_TRIGGER)
        logging.info("GPIO SET: ECHO PIN[%s]" % self.PIN_ECHO)

        while self.running:

            distance = 0
            for i in range(0, 2):
                # Move the motor in right place
                distance = distance + self.checkdist()
                logging.debug('Distance: %0.1f cm' % distance)
                time.sleep(0.2)

            # Calculate the best direction, and give suggestion
            logging.debug('Calculating...')

            if distance < 120: #60cm
                self.recommend_direction = MovementEvent.TURN_BACKWARD
                # File a BLOCKER event.
                event = MovementEvent(MovementEvent.EVENT_BLOCKER)
                self.block_events.put(event)
                logging.debug("An BLOCKER Event filed by Ultrasonic Scan: %d" % self.recommend_direction)

    def finish(self):
        super(RaspUltrasonicScan, self).finish()
        #Clean up the GPIO3, set to input.
        GPIO.setup(self.PIN_TRIGGER, GPIO.IN)
        logging.debug("Ultrasonic Scan cleaned: PIN[%d]" % self.PIN_TRIGGER)