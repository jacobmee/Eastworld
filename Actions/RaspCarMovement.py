#! /usr/bin/python

import time
import RPi.GPIO as GPIO
import logging
import Queue

from Queue import PriorityQueue
from Actions.Action import Action
from Actions.Action import Event
from Actions.RaspCarUltrasonicScan import RaspUltrasonicScan
from Actions.RaspCarWallDetect import RaspCarWallDetect


class CarMovement(Action):

    # Take PIN12 (GPIO18), PIN16 (GPIO23), PIN18 (GPIO24) and PIN22 (GPIO25) for 4 INs for chip L298N
    def __init__(self):
        super(CarMovement, self).__init__()
        self.CTRL = {"IN1": 12, "IN2": 16, "IN3": 18, "IN4": 22}
        self.sensor_events = PriorityQueue(5)


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
        self.wall_detection = RaspCarWallDetect(self.sensor_events)
        self.wall_detection.setDaemon(True)
        self.wall_detection.start()

        # Create a thread, and put the detection in.  If the thread already exists, do nothing.
        self.ultrasonic_scan = RaspUltrasonicScan(self.sensor_events)
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


        #while self.running:
        for i in range(0, 5):
            # Working on block events first.
            try:
                sensor_event = self.sensor_events.get(block=True, timeout=10)

                logging.debug("task recv:%d, %s @%d " % (sensor_event.priority, sensor_event.name, sensor_event.time))
                logging.debug("i am working on this sensor event")

                # WALL_TO_STOP; TURN_RIGHT; TURN_LEFT; BACKWARD; TURN_AROUND
                if sensor_event.name == Event.EVENT_BLOCKER:
                    # next_move = evalute_next_move()

                    logging.debug("Into MOVE action :[%d]!!!" % self.wall_detection.recommend_direction)
                    if self.wall_detection.recommend_direction == Event.TURN_RIGHT:
                        self.stop()
                        rasp_turn_right = RaspCarTurnRight()
                        rasp_turn_right.run()
                        logging.debug("TURN right!")
                    elif self.wall_detection.recommend_direction == Event.TURN_LEFT:
                        self.stop()
                        rasp_turn_left = RaspCarTurnLeft()
                        rasp_turn_left.run()
                        logging.debug("TURN left!")
                    elif self.wall_detection.recommend_direction == Event.TURN_AROUND:
                        self.stop()
                        rasp_turn_around = RaspCarTurnAround()
                        rasp_turn_around.run()
                        logging.debug("TURN around!")
                    else:
                        self.stop()
                        logging.debug("So confused...")
                elif sensor_event.name == Event.EVENT_ADJUSTMENT:
                    logging.debug("Requested adjustment: %d", self.ultrasonic_scan.recommend_direction)
                    if self.ultrasonic_scan.recommend_direction == Event.TURN_BACKWARD:
                        self.stop()
                        rasp_move_backward = RaspCarMoveBackward()
                        rasp_move_backward.run()
                        logging.debug("Backward!")
                        rasp_turn_around = RaspCarTurnAround()
                        rasp_turn_around.run()
                        logging.debug("TURN around!")
                    else:
                        if self.ultrasonic_scan.recommend_direction > 0:
                            self.stop()
                            time.sleep(0.5)
                            GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
                            sleep_time = 0.6 + (0.5 * self.ultrasonic_scan.recommend_direction / 90)
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                            logging.debug("TURN right from ultrasonic : %d, T[%.2f]!" % (self.ultrasonic_scan.recommend_direction, sleep_time))
                        elif self.ultrasonic_scan.recommend_direction < 0:
                            self.stop()
                            time.sleep(1)
                            GPIO.output(self.CTRL["IN4"], GPIO.HIGH)

                            sleep_time = 0.6 + (-0.5 * self.ultrasonic_scan.recommend_direction / 90)
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                            logging.debug("TURN left from ultrasonic : %d, T[%.2f]!" % (self.ultrasonic_scan.recommend_direction, sleep_time))

                    self.ultrasonic_scan.recommend_direction = 0

                logging.debug("Next move finished!")

                # Clean data
                self.sensor_events.task_done()
                res = self.sensor_events.qsize()
                while not self.sensor_events.empty():
                    task = self.sensor_events.get()
                    logging.debug(
                        "Clean up everything in sensor Q.  There are still %d tasks to do, next:%s, %d" % (self.sensor_events.qsize(), task.name, task.priority))
                    self.sensor_events.task_done()

                logging.debug(
                    "Clean up everything in sensor Q.  There are still %d tasks to do" % self.sensor_events.qsize())

            except Queue.Empty:
                logging.debug("Too far away, I will stop!")
                break

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