#! /usr/bin/python

import time
import RPi.GPIO as GPIO
import logging
import Queue
import collections
import threading

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

    # Stop everything
    def stop(self):
        super(CarMovement, self).finish()
        for key in self.CTRL:
            port = self.CTRL[key]
            GPIO.output(port, GPIO.LOW)

        logging.info("MOTER cleaned & stopped")

    # Stop everything
    def finish(self):
        super(CarMovement, self).finish()
        self.stop()


class RaspCarMove(CarMovement):
    """MAIN class to move - It should be able to accomplish following:
        #1. Able to move forward and
        #    a) Using the Wall Detect to know stop
        #    b) Using the Ultrasonic Scan to change the direction
        #    c) If it's too close to wall, backward and turn around
        #2. Continue to move forward"""

    def __init__(self):
        super(RaspCarMove, self).__init__()
        self.ultrasonic_data = collections.OrderedDict()
        # Create a thread, and put the detection in.  If the thread already exists, do nothing.
        self.wall_detection = RaspCarWallDetect(self.sensor_events)
        self.wall_detection.setDaemon(True)
        self.wall_detection.start()

        # Create a thread, and put the detection in.  If the thread already exists, do nothing.
        self.ultrasonic_scan = RaspUltrasonicScan(self.sensor_events, self.ultrasonic_data)
        self.ultrasonic_scan.setDaemon(True)
        self.ultrasonic_scan.start()

    def begin(self):
        super(RaspCarMove, self).begin()
        GPIO.setmode(GPIO.BOARD)
        for key in self.CTRL:
            port = self.CTRL[key]
            GPIO.setup(port, GPIO.OUT)
            logging.info("MOTER SET GPIO PIN[%s]" % port)

    # Stop everything
    def finish(self):
        super(CarMovement, self).finish()
        if self.wall_detection.isAlive():
            self.wall_detection.finish();
        if self.ultrasonic_scan.isAlive():
            self.ultrasonic_scan.finish();

    def execute(self):
        super(RaspCarMove, self).execute()

        #  while self.running:
        for i in range(0, 20):
            # Working on block events first.

            # Get Ultrasonic data  & Adjust direction
            recent_scan_data = {}
            moving = False
            moving_distance = 1 # one step forward
            while True:

                if len(self.ultrasonic_data) == 0:
                    time.sleep(0.2)
                else:
                    for item in self.ultrasonic_data:
                        recent_scan_data = self.ultrasonic_data[item]
                        logging.debug("Getting most recent Ultrasonic data(%d)" % len(self.ultrasonic_data))
                        break
                    self.ultrasonic_data.clear()

                    print_scan = sorted(recent_scan_data.iteritems(), key=lambda d: d[0], reverse=True)
                    logging.debug("Analysing UltraScan data: %s" % print_scan)

                    go_angle = 0
                    go_range = 0
                    for point in range(90, 31, -15):

                        # Always right first
                        if recent_scan_data[point] > 100:
                            go_angle = point
                            go_range = recent_scan_data[point]
                            break

                        # Check left if possible
                        left_point = 180 - point
                        if recent_scan_data[left_point] > 100:
                            go_angle = left_point
                            go_range = recent_scan_data[left_point]
                            break

                    logging.debug("Go: %d, %d" % (go_angle, go_range))

                    if go_angle == 0 and go_range == 0: # Blocked
                        left_distance = recent_scan_data[150]
                        right_distance = recent_scan_data[30]
                        if right_distance >= left_distance:
                            GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
                            turn_time = 0.5
                            logging.debug("Ultrascan (nowhere) Turn Right: %d, %d, %0.1f" % (go_angle, go_range, turn_time))
                            time.sleep(turn_time)
                            self.stop()
                        else:
                            GPIO.output(self.CTRL["IN4"], GPIO.HIGH)
                            turn_time = 0.5
                            logging.debug("Ultrascan (nowhere) Turn Right: %d, %d, %0.1f" % (go_angle, go_range, turn_time))
                            time.sleep(turn_time)
                            self.stop()
                        break
                    elif go_angle < 90: # The target is on the right
                        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
                        turn_time = 0.2 + 0.3 * (90 - go_angle) / 90
                        logging.debug("Ultrascan Turn Right: %d, %d, %0.1f" % (go_angle, go_range, turn_time))
                        time.sleep(turn_time)
                        self.stop()
                        break
                    elif go_angle > 90: # The target is the left
                        GPIO.output(self.CTRL["IN4"], GPIO.HIGH)
                        turn_time = 0.2 + 0.3 * (go_angle - 90) / 90
                        time.sleep(turn_time)
                        logging.debug("Ultrascan Turn left: %d, %d, %0.1f" % (go_angle, go_range, turn_time))
                        self.stop()
                        break
                    elif go_angle == 90: # Complete the adjustment
                        logging.debug("Correct direction, adjustment completed")
                        moving = True
                        if go_range > 200:
                            moving_distance = 2
                        break

            # Resume forward
            if moving:
                # Move forward for the direction
                GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
                GPIO.output(self.CTRL["IN4"], GPIO.HIGH)
                step_second = moving_distance * 0.5
                logging.debug("Move forward: %d" %step_second)

                count_time = 0
                while count_time < step_second:

                    # Stop if there is any event!
                    try:
                        sensor_event = self.sensor_events.get(block=False)

                        logging.debug(
                            "EVENT recv:%d, %s @%d " % (sensor_event.priority, sensor_event.name, sensor_event.time))

                        # WALL_TO_STOP; TURN_RIGHT; TURN_LEFT; BACKWARD; TURN_AROUND
                        if sensor_event.name == Event.EVENT_BLOCKER:

                            logging.debug("Into MOVE action :[%d]!!!" % self.wall_detection.recommend_direction)
                            if self.wall_detection.recommend_direction == Event.TURN_RIGHT:
                                self.stop()
                                rasp_turn_right = RaspCarTurnRight()
                                rasp_turn_right.run()
                                logging.debug("TURN RIGHT EVENT!")
                                self.stop()
                            elif self.wall_detection.recommend_direction == Event.TURN_LEFT:
                                self.stop()
                                rasp_turn_left = RaspCarTurnLeft()
                                rasp_turn_left.run()
                                logging.debug("TURN LEFT EVENT!")
                                self.stop()
                            elif self.wall_detection.recommend_direction == Event.TURN_AROUND:
                                self.stop()
                                rasp_turn_around = RaspCarTurnAround()
                                rasp_turn_around.run()
                                logging.debug("TURN AROUND EVENT!")
                                self.stop()
                            else:
                                logging.debug("BLOCK EVENT, BUT DON'T KNOW WHY EXACTLY...")

                            # Clean data
                            self.sensor_events.task_done()
                            res = self.sensor_events.qsize()
                            while not self.sensor_events.empty():
                                task = self.sensor_events.get()
                                logging.debug(
                                    "Clean up everything in sensor Q.  There are still %d tasks to do, next:%s, %d" % (
                                    self.sensor_events.qsize(), task.name, task.priority))
                                self.sensor_events.task_done()

                            moving = False

                    except Queue.Empty:
                        pass
                        #logging.debug("Empty queue, that's good!")

                    count_time = count_time + 0.1
                    time.sleep(0.1)

                self.stop()

            else:
                time.sleep(1)

            self.running = True

        self.stop()


class RaspCarTurnRight(CarMovement):
    def execute(self):
        super(RaspCarTurnRight, self).execute()
        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
        time.sleep(0.5)


class RaspCarTurnLeft(CarMovement):
    def execute(self):
        super(RaspCarTurnLeft, self).execute()
        GPIO.output(self.CTRL["IN4"], GPIO.HIGH)
        time.sleep(0.5)


class RaspCarMoveForward(CarMovement):
    def execute(self):
        super(RaspCarMoveForward, self).execute()
        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
        GPIO.output(self.CTRL["IN4"], GPIO.HIGH)
        time.sleep(0.5)


class RaspCarMoveBackward(CarMovement):
    def execute(self):
        super(RaspCarMoveBackward, self).execute()
        GPIO.output(self.CTRL["IN2"], GPIO.HIGH)
        GPIO.output(self.CTRL["IN3"], GPIO.HIGH)
        time.sleep(0.5)


class RaspCarTurnAround(CarMovement):
    def execute(self):
        super(RaspCarTurnAround, self).execute()
        GPIO.output(self.CTRL["IN1"], GPIO.HIGH)
        GPIO.output(self.CTRL["IN3"], GPIO.HIGH)
        time.sleep(0.5)


class RaspCarStop(CarMovement):
    def execute(self):
        super(RaspCarStop, self).execute()
        self.stop()