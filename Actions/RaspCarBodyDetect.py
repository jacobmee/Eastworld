import os
import time

from Actions.Action import Action


class RaspBodyMovingDetect(Action):

    #HC-SR501 Pin011 (GPIO17) for detection
    def execute(self):
        super(RaspBodyMovingDetect, self).execute()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN)

        try:
            while True:
                if GPIO.input(11) == 1:
                    print "Some people here!"

                    # Getting images
                    localtime = time.time()
                    os.system('raspistill -t 5000 -tl 750 -ISO 7000 -ss 50000 -o image_num_"%s"_%d.jpg' % localtime)
                else:
                    print "Nobody!"
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print "All Cleanup!"