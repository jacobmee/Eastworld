import threading
import logging.config
import time
import RPi.GPIO as GPIO

from Actions.Action import Action
from Actions.RaspCarMovement import Event


class RaspCarWallDetect(Action, threading.Thread):
    # HJ-IR2 Pin38 (GPIO20) for left detection and Pin40(GPIO21) for right detection
    PIN_LEFT_DETECTION = 38
    PIN_RIGHT_DETECTION = 40

    def __init__(self, block_events):
        super(RaspCarWallDetect, self).__init__()
        threading.Thread.__init__(self)
        self.block_events = block_events
        self.recommend_direction = 0

    def run(self):
        self.execute()

    def execute(self):
        super(RaspCarWallDetect, self).execute()
        self.running = True
        GPIO.setmode(GPIO.BOARD)

        # Define as GPIO input
        logging.info("GPIO SET: LEFT PIN[%s]" % self.PIN_LEFT_DETECTION)
        logging.info("GPIO SET: RIGHT PIN[%s]" % self.PIN_RIGHT_DETECTION)

        GPIO.setwarnings(False)
        GPIO.setup(self.PIN_LEFT_DETECTION, GPIO.IN)
        GPIO.setup(self.PIN_RIGHT_DETECTION, GPIO.IN)

        while self.running:

            left_detection = False
            right_detection = False
            both_detection = False

            if GPIO.input(self.PIN_LEFT_DETECTION) == 0:
                left_detection = True
                self.recommend_direction = Event.TURN_RIGHT
            if GPIO.input(self.PIN_RIGHT_DETECTION) == 0:
                right_detection = True
                self.recommend_direction = Event.TURN_LEFT
            if left_detection and right_detection:
                both_detection = True
                self.recommend_direction= Event.TURN_AROUND

            if left_detection or right_detection or both_detection:
                event = Event(Event.PRIORITY_MEDIUM, Event.EVENT_BLOCKER)
                self.block_events.put(event)
                logging.debug("An BLOCKER Event filed by wall detector: %d" % self.recommend_direction)

            time.sleep(0.1)

    def finish(self):
        super(RaspCarWallDetect, self).finish()
        self.running = False
        # Both inputs (Pin38 & Pin40) is GPIO.IN, so we don't need to clean up anything
        logging.info("Wall detection, no need to clean anything.")
