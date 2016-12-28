from Base.BaseWorld import *
from Thing import Thing
from Storylines.CarStoryline import *

class Car(Thing):
    pass

class RaspCar(Car):
    def __init__(self, name, mode):
        super(RaspCar, self).__init__(name, mode)

    SILENT_MODE = "silent"  # Silent means do nothing
    SPORTS_MODE = "sports"  # Moving, driving, scan sensors on
    WATCHING_MODE = "watching"  # In alarm, anything passed or in room, will be filing alerts.
    PARTY_MODE = "party"  # Behavior like DJ, able to play music or movies

    def load_memory(self):
        super(RaspCar, self).load_memory()

    def load_storylines(self):
        super(RaspCar, self).load_storylines()

        logging.debug("Into [%s] mode" % self.mode)
        if self.mode == self.SPORTS_MODE:
            self.storylines.append(RaspCarPatrol())
        elif self.mode == self.WATCHING_MODE:
            self.storylines.append(RaspCarWatching())
        elif self.mode == self.PARTY_MODE:
            pass
        else:
            self.mode = self.SILENT_MODE

        logging.debug("Into [%s] mode" % self.mode)

    def load_believes(self):
            self.believes = [Believe.STRANGER, Believe.WARRIOR]

    def load_mood(self):
            self.mood = [Mood.ANGER, Mood.FEAR]

    def load_status(self):
            self.status = Status.ACTIVE