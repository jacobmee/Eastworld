from Storylines.Storyline import StoryLine
from Actions.RaspCarMovement import *
from Actions.RaspCarSurveillance import RaspCarSurveillance


class CarStoryLine(StoryLine):
    pass


# This is for Dance: Move 1cm, turn around, move another around
class RaspCarDance(CarStoryLine):

    def begin(self):
        super(RaspCarDance, self).begin()
        self.actions.append(RaspCarMoveForward())
        self.actions.append(RaspCarTurnAround())
        self.actions.append(RaspCarTurnLeft())
        self.actions.append(RaspCarTurnAround())
        self.actions.append(RaspCarTurnRight())
        self.actions.append(RaspCarMoveForward())


# Move forward until block, then turn back, until another block.
class RaspCarPatrol(CarStoryLine):

    def begin(self):
        super(RaspCarPatrol, self).begin()
        self.actions.append(RaspCarMoveForward())


# Move forward until block, then turn back, until another block.
class RaspCarWatching(CarStoryLine):
    def begin(self):
        super(RaspCarWatching, self).begin()
        self.actions.append(RaspCarSurveillance())