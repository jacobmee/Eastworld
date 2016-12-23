# ! /usr/bin/python
# -*- coding:utf-8 -*-


class Status(object):
    # Active, Idle, Asleep
    ACTIVE = "Active"
    IDLE = "Idle"
    ASLEEP = "Asleep"


class Mood(object):
    # Joy, Fear, Sadness, Disgust & Anger
    JOY = "Joy"
    FEAR = "Fear"
    SADNESS = "Sadness"
    DISGUEST = "Disgust"
    ANGER = "Anger"


class Believe(object):
    # Father, Mother, Warrior, Maiden, Smith, Crone & Stranger
    FATHER = "Father"
    MOTHER = "Mother"
    WARRIOR = "Warrior"
    MAIDEN = "Maiden"
    SMITH = "Smith"
    CRONE = "Crone"
    STRANGER = "Stranger"


class Rule(object):
    # Follows by Believes
    pass


class Memory(object):
    pass


class LongMemory(Memory):
    pass


class ShortMemory(Memory):
    pass


