from Base.BaseWorld import Believe, Mood, Status, Rule
from Storylines.Storyline import StoryLine


class Thing(object):
    def __init__(self, name):
        self.name = name
        self.load_status()
        self.load_memory()
        self.load_believes()
        self.load_mood()
        self.load_rules()
        self.load_storylines()

    def load_memory(self):
        pass

    def load_believes(self):
        self.believes = [Believe.STRANGER]

    def load_mood(self):
        self.mood = [Mood.ANGER]

    def load_status(self):
        self.status = Status.ACTIVE

    def load_rules(self):
        self.rules = []

    def load_storylines(self):
        self.storylines = []

    def alive(self):
        for storyline in self.storylines:
            storyline.begin()
            storyline.execute()
            storyline.finish()