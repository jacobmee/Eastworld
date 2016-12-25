#!/usr/bin/python
import sys
import logging.config
from Things.Car import *

# The world starts with a raspberry car.  It's named "Tang"
if __name__ == "__main__":
    logging.config.fileConfig("/home/pi/Eastworld/etc/logging.conf")

    logging.debug("Welcome to East World!")

    if len(sys.argv) > 1:
        rasp_car = RaspCar("Tang", sys.argv[1])
        rasp_car.alive()
    else:
        rasp_car = RaspCar("Tang", RaspCar.WATCHING_MODE)
        rasp_car.alive()


    logging.debug("Bye, our noble guest!")