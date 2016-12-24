
class StoryLine(object):
    def __init__(self):
        self.actions = []

    def execute(self):
        for action in self.actions:
            action.begin()
            action.execute()
            action.finish()

    def begin(self):
        pass

    def finish(self):
        pass