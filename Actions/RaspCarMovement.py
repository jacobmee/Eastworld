#! /usr/bin/python

import time
import Queue
import RPi.GPIO as GPIO
import logging

from Actions.Action import Action
from Actions.Action import MovementEvent
from Actions.RaspCarUltrasonicScan import RaspUltrasonicScan
from Actions.RaspCarWallDetect import RaspCarWallDetect


class CarMovement(Action):

    # Take PIN12 (GPIO18), PIN16 (GPIO23), PIN18 (GPIO24) and PIN22 (GPIO25) for 4 INs for chip L298N
    def __init__(self):
        super(CarMovement, self).__init__()
        self.CTRL = {"IN1": 12, "IN2": 16, "IN3": 18, "IN4": 22}
        self.block_events = Queue.Queue(3)

    # Initialize the moter
    def begin(self):
        super(CarMovement, self).begin()
        GPIO.setmode(GPIO.BOARD)
        for key in self.CTRL:
            port = self.CTRL[key]
            GPIO.setup(port, GPIO.OUT)
            logging.info("MOTER SET GPIO PIN[%s]" % port)

    # Stop everything
    def stop(self):
        super(CarMovement, self).finish()
        for key in self.CTRL:
            port = self.CTRL[key]
            GPIO.output(port, GPIO.LOW)
            logging.info("MOTER Clean GPIO PIN[%s]" % port)

    # Stop everything
    def finish(self):
        super(CarMovement, self).finish()
        self.stop()

'''
MAIN class to move - It should be able to accomplish following:
#1. Able to move forward and
    a) Using the Wall Detect to know stop
    b) Using the Ultrasonic Scan to change the direction
    c) If it's too close to wall, backward and turn around
#2. Continue to move forward
#3. Until'''
class RaspCarMoveForward(CarMovement):

    def __init__(self):
        super(RaspCarMoveForward, self).__init__()
        # Create a thread, and put the detection in.  If the thread already exists, do nothing.
        self.wall_detection = RaspCarWallDetect(self.block_events)
        self.wall_detection.setDaemon(True)
        self.wall_detection.start()

        # Create a thread, and put the detection in.  If the thread already exists, do nothing.
        self.ultrasonic_scan = RaspUltrasonicScan(self.block_events)
        self.ultrasonic_scan.setDaemon(True)
        self.ultrasonic_scan.start()

    # Stop everything
    def finish(self):
        super(CarMovement, self).finish()
        if self.wall_detection.isAlive():
            self.wall_detection.finish();
        if self.ultrasonic_scan.isAlive():
            self.ultrasonic_scan.finish();

    def execute(self):
        super(RaspCarMoveForward, self).execute()
        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
        GPIO.output(self.CTRL["IN4"], GPIO.HIGH)

        while self.running:

            logging.debug("waiting for task")
            try:
                movement_event = self.block_events.get(block=True, timeout=10)
            except Queue.Empty:
                logging.debug("Too far away, I will stop!")
                break

            logging.debug("task recv:%s " % movement_event.name)
            logging.debug("task raised time %d" % movement_event.time)
            logging.debug("i am working on this request")

            # WALL_TO_STOP; TURN_RIGHT; TURN_LEFT; BACKWARD; TURN_AROUND
            if movement_event.name == MovementEvent.EVENT_BLOCKER:
                #next_move = evalute_next_move()

                logging.debug("Into MOVE action :[%d]!!!" % self.wall_detection.recommend_direction)
                if self.wall_detection.recommend_direction == MovementEvent.TURN_RIGHT:
                    self.stop()
                    rasp_turn_right = RaspCarTurnRight()
                    rasp_turn_right.run()
                    logging.debug("TURN right!")
                elif self.wall_detection.recommend_direction == MovementEvent.TURN_LEFT:
                    self.stop()
                    rasp_turn_left = RaspCarTurnLeft()
                    rasp_turn_left.run()
                    logging.debug("TURN left!")
                elif self.ultrasonic_scan.recommend_direction == MovementEvent.TURN_BACKWARD:
                    self.stop()
                    rasp_move_backward = RaspCarMoveBackward()
                    rasp_move_backward.run()
                    logging.debug("Backward!")
                    time.sleep(1)
                    rasp_turn_around = RaspCarTurnAround()
                    rasp_turn_around.run()
                    logging.debug("TURN around!")
                elif self.wall_detection.recommend_direction == MovementEvent.TURN_AROUND:
                    self.stop()
                    rasp_turn_around = RaspCarTurnAround()
                    rasp_turn_around.run()
                    logging.debug("TURN around!")
                else :
                    self.stop()
                    logging.debug("So confused...")

                logging.debug("Next move finished!")

                self.block_events.task_done()
                res = self.block_events.qsize()
                while not self.block_events.empty():
                    task = self.block_events.get()
                    self.block_events.task_done()
                    logging.debug("Clean up everything in Q.  There are still %d tasks to do" % self.block_events.qsize())


            # Resume forward
            self.running = True
            GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
            GPIO.output(self.CTRL["IN4"], GPIO.HIGH)

        self.stop()


class RaspCarTurnRight(CarMovement):
    def execute(self):
        super(RaspCarTurnRight, self).execute()
        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
        time.sleep(1)


class RaspCarTurnLeft(CarMovement):
    def execute(self):
        super(RaspCarTurnLeft, self).execute()
        GPIO.output(self.CTRL["IN4"], GPIO.HIGH)
        time.sleep(1)


class RaspCarMoveBackward(CarMovement):
    def execute(self):
        super(RaspCarMoveBackward, self).execute()
        GPIO.output(self.CTRL["IN2"], GPIO.HIGH)
        GPIO.output(self.CTRL["IN3"], GPIO.HIGH)
        time.sleep(1)


class RaspCarTurnAround(CarMovement):
    def execute(self):
        super(RaspCarTurnAround, self).execute()
        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
        GPIO.output(self.CTRL["IN3"], GPIO.HIGH)
        time.sleep(1)


class RaspCarStop(CarMovement):
    def execute(self):
        super(RaspCarStop, self).execute()
        self.stop()