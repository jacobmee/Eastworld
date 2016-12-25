import os

from Actions.Action import Action


class RaspCarSurveillance(Action):

    def execute(self):
        super(RaspCarSurveillance, self).execute()
        os.system('sh /home/pi/Eastworld/etc/mjpg.sh')
