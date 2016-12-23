### Imports ###################################################################

from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import cv2
from Actions.Action import Action


class RaspToSpeak(Action):

    def execute(self):
        cx = 160
        cy = 120
        xdeg = 150
        ydeg = 150

        # Setup the camera
        camera = PiCamera()
        camera.resolution = (320, 240)
        camera.framerate = 20
        rawCapture = PiRGBArray( camera, size=(320, 240))

        # Load a cascade file for detecting faces
        face_cascade = cv2.CascadeClassifier( '/home/pi/frontalface.xml' )

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