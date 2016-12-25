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


class RaspCarCamera(Action):

    def execute(self):
        super(RaspCarCamera, self).execute()
        cx = 160
        cy = 120
        xdeg = 150
        ydeg = 150

        # Setup the camera
        camera = PiCamera()
        camera.framerate = 20
        rawCapture = PiRGBArray( camera)

        # Load a cascade file for detecting faces
        face_cascade = cv2.CascadeClassifier( '/home/pi/Eastworld/frontalface.xml' )

        num = 0
        # Capture frames from the camera
        for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):

            image = frame.array

            # Use the cascade file we loaded to detect faces
            gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
            faces = face_cascade.detectMultiScale( gray )

            print "Found " + str( len( faces ) ) + " face(s)"

            # Draw a rectangle around every face and move the motor towards the face
            for ( x, y, w, h ) in faces:

                cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 100, 255, 100 ), 2 )
                cv2.putText( image, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

                # Save the images
                cv2.imwrite('%s.jpg' % (str(num)), image)
                num = num + 1

            # Clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            # stop the carema
            if num > 0:
                break

        cv2.destroyAllWindows()