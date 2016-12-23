import unittest
from Things.Car import *
from Things.Thing import Thing


class TestBaseWorld(unittest.TestCase):

    def test_init(self):
        thing = Thing("TEST")
        self.assertTrue(len(thing.believes) > 0)
        self.assertTrue(len(thing.mood) > 0)
        self.assertTrue(thing.status)
        self.assertTrue(thing.name)

    def test_RaspCar(self):
        rasp_car = RaspCar("Tang")
        rasp_car.alive()