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
    PIN_ROTATION = 36

    def __init__(self, adjustment_events):
        super(RaspUltrasonicScan, self).__init__()
        threading.Thread.__init__(self)
        self.adjustment_events = adjustment_events
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

            #logging.debug("Ultrasonic Scan started")
            count = count + 1
            front_distance = 0
            far_distance = 0
            far_angle = 0

            if count % 5 == 0:

                for i in range(0, 30, 10):
                    cycle = 7 + 6 * i / 30
                    p.ChangeDutyCycle(cycle)
                    time.sleep(0.1)
                    distance = self.checkdist()
                    if cycle == 7:
                        front_distance = distance
                    if distance > far_distance:
                        far_angle = cycle
                        far_distance = distance
                    #logging.debug("i:%d  c:%d d:%d" % (i, cycle, distance))
                for i in range(50, -50, -10):
                    cycle = 7 + 5 * i / 50
                    p.ChangeDutyCycle(cycle)
                    time.sleep(0.1)
                    distance = self.checkdist()
                    if cycle == 7:
                        front_distance = distance
                    if distance > far_distance:
                        far_angle = cycle
                        far_distance = distance
                    #logging.debug("i:%d  c:%d d:%d" % (i, cycle, distance))

                # Calculate the best direction, and give suggestion
                need_to_adjust = (far_distance - front_distance) / front_distance
                logging.debug("Calculated result:  Front: %d and Far: [%d][%d]: Need[%.1f] " %(front_distance, far_distance, far_angle, need_to_adjust))

                if need_to_adjust > 1:
                    direction = 15 * (7 - far_angle)
                    logging.info("We'll move to %d" % direction)
                    self.recommend_direction = direction
                    # File an ADJUSTMENT event.

                    if far_distance - front_distance > 100:
                        event = Event(Event.PRIORITY_HIGH, Event.EVENT_ADJUSTMENT)
                        self.adjustment_events.put(event)
                    else:
                        event = Event(Event.PRIORITY_MEDIUM, Event.EVENT_ADJUSTMENT)
                        self.adjustment_events.put(event)

                    logging.debug("An ADJUSTMENT Event filed by Ultrasonic Scan: %d" % self.recommend_direction)
            else:
                p.ChangeDutyCycle(7)
                time.sleep(0.2)

                for i in range (0, 3):
                    front_distance = front_distance + self.checkdist()

                front_distance = front_distance / 3

                # Calculate the best direction, and give suggestion
                logging.debug(
                    "Calculated result:  Front: %d " % front_distance)

                if front_distance < 30 and front_distance > 0: #60cm
                    self.recommend_direction = Event.TURN_BACKWARD
                    # File a BLOCKER event.
                    event = Event(Event.PRIORITY_HIGH, Event.EVENT_ADJUSTMENT)
                    self.adjustment_events.put(event)
                    logging.debug("An ADJUSTMENT Event filed by Ultrasonic Scan: d[%d] a[%d]" % (front_distance, self.recommend_direction))


    def finish(self):
        super(RaspUltrasonicScan, self).finish()
        #Clean up the GPIO3, set to input.
        GPIO.setup(self.PIN_TRIGGER, GPIO.IN)
        GPIO.setup(self.PIN_ROTATION, GPIO.IN)
        logging.debug("Ultrasonic Scan cleaned: PIN[%d] & PIN[%d]" % (self.PIN_TRIGGER, self.PIN_ROTATION))