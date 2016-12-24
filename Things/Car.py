from Base.BaseWorld import *
from Thing import Thing
from Storylines.CarStoryline import *

class Car(Thing):
    pass


class RaspCar(Car):
    def load_memory(self):
        super(Car, self).load_memory()

    def load_storylines(self):
        super(Car, self).load_storylines()
        self.storylines.append(RaspCarPatrol())

    def load_believes(self):
            self.believes = [Believe.STRANGER, Believe.WARRIOR]

    def load_mood(self):
            self.mood = [Mood.ANGER, Mood.FEAR]

    def load_status(self):
            self.status = Status.ACTIVE