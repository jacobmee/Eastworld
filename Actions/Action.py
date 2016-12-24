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


class MovementEvent(object):

    EVENT_BLOCKER = "EVENT_BLOCKER"
    TURN_RIGHT = 90
    TURN_LEFT = -90
    TURN_BACKWARD = 360
    TURN_AROUND = 180

    def __init__(self, name):
        super(MovementEvent, self).__init__()
        self.name = name
        self.time = time.time()
