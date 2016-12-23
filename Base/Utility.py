import os


def speak(filename):
    os.system('mpg123 "%s"' % filename)
