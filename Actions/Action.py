import time

class Action(object):

    def __init__(self):
        self.running = False

    def execute(self):
        self.running = True

    def begin(self):
        pass

    def finish(self):
        self.running = False

    def run(self):
        self.begin()
        self.execute()
        self.finish()


class Event(object):

    EVENT_BLOCKER = "EVENT_BLOCKER"
    EVENT_ADJUSTMENT = "EVENT_ADJUSTMENT"
    TURN_RIGHT = 90
    TURN_LEFT = -90
    TURN_BACKWARD = 360
    TURN_AROUND = 180

    PRIORITY_HIGH = 2
    PRIORITY_MEDIUM = 5
    PRIORITY_LOW = 8

    def __init__(self, priority, name):
        super(Event, self).__init__()
        self.priority = priority
        self.name = name
        self.time = time.time()
