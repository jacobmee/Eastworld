import time
import threading
import Queue
import math
import RPi.GPIO as GPIO
import logging.config

from Actions.Action import Action
from Actions.RaspCarMovement import *

class RaspCarEyeRolling(Action, threading.Thread):
    # HC-SR04, the farest it can get is 4.5m.  Pin03 (GPIO02) for "Trig" and Pin05 (GPIO03) for "Echo"
    PIN_ROTATION = 36

    def __init__(self, ):
        super(RaspCarEyeRolling, self).__init__()
        threading.Thread.__init__(self)

    def execute(self):
        super(RaspCarEyeRolling, self).execute()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_ROTATION, GPIO.OUT)
        logging.debug("RaspCarEyeRolling setup: PIN[%d]" % (self.PIN_ROTATION))

        GPIO.output(self.PIN_ROTATION, GPIO.HIGH)
        p = GPIO.PWM(36, 50)  # 50HZ
        p.start(0)

        start_point = 2.5
        mid_point = 7
        length = 10.0

        for i in range(30, 151, 15):
            cycle = start_point + (length * (i)) / 180
            p.ChangeDutyCycle(cycle)
            time.sleep(0.02)
        for i in range(150, 29, -15):
            cycle = start_point + (length * (i)) / 180
            p.ChangeDutyCycle(cycle)
            time.sleep(0.02)

        p.ChangeDutyCycle(mid_point)
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
        time.sleep(0.02)

    def run(self):
        super(RaspCarEyeRolling, self).run()

    def finish(self):
        super(RaspCarEyeRolling, self).finish()
        GPIO.setup(self.PIN_ROTATION, GPIO.IN)
        logging.debug("RaspCarEyeRolling cleaned: PIN[%d]" % (self.PIN_ROTATION))