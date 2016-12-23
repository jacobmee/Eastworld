from Actions.Action import Action


class StoryLine(object):
    def __init__(self):
        self.actions = []

    def execute(self):
        for action in self.actions:
            action.start()
            action.execute()
            action.done()

    def start(self):
        pass

    def done(self):
        pass