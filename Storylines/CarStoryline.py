from Storylines.Storyline import StoryLine
from Actions.RaspCarMovement import *


class CarStoryLine(StoryLine):
    pass


# This is for Dance: Move 1cm, turn around, move another around
class RaspCarDance(CarStoryLine):

    def start(self):
        super(CarStoryLine, self).start()
        self.actions.append(RaspCarMoveForward())
        self.actions.append(RaspCarTurnAround())
        self.actions.append(RaspCarTurnLeft())
        self.actions.append(RaspCarTurnAround())
        self.actions.append(RaspCarTurnRight())
        self.actions.append(RaspCarMoveForward())


# Move forward until block, then turn back, until another block.
class RaspCarPatrol(CarStoryLine):

    def start(self):
        super(CarStoryLine, self).start()
        self.actions.append(RaspCarMoveForward())
        self.actions.append(RaspCarTurnAround())
        self.actions.append(RaspCarMoveForward())
