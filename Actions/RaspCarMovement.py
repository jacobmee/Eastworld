#! /usr/bin/python
# -*- coding:utf-8 -*-

from Actions.Movements import *


class RaspCarTurnRight(TurnRight):
    def execute(self):
        super(TurnRight, self).execute()


class RaspCarTurnLeft(TurnLeft):
    def execute(self):
        super(TurnLeft, self).execute()


class RaspCarMoveForward(MoveForward):
    def execute(self):
        super(MoveForward, self).execute()


class RaspCarMoveBackward(MoveBackward):
    def execute(self):
        super(MoveBackward, self).execute()


class RaspCarTurnAround(TurnAround):
    def execute(self):
        super(TurnAround, self).execute()


