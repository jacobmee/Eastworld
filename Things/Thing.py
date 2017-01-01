from Base.BaseWorld import Believe, Mood, Status, Rule
from Storylines.Storyline import StoryLine


class Thing(object):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

        self.status = Status.ACTIVE
        self.believes = [Believe.STRANGER]
        self.mood = [Mood.ANGER]
        self.rules = []
        self.storylines = []

        self.load_status()
        self.load_believes()
        self.load_mood()
        self.load_memory()
        self.load_rules()
        self.load_storylines()

    def load_memory(self):
        pass

    def load_believes(self):
        pass

    def load_mood(self):
        pass

    def load_status(self):
        pass

    def load_rules(self):
        pass

    def load_storylines(self):
        pass

    def alive(self):
        for storyline in self.storylines:
            storyline.begin()
            storyline.execute()
            storyline.finish()