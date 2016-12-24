#!/usr/bin/python
import logging.config
from Things.Car import *

# The world starts with a raspberry car.  It's named "Tang"
if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")

    logging.debug("Welcome to East World!")
    rasp_car = RaspCar("Tang")
    rasp_car.alive()
    logging.debug("Bye, our noble guest!")
