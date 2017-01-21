import logging
import logging.config
import os
import threading
import time

from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import RPi.GPIO as GPIO
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

from Actions.Action import Action
from Base.Facepp import API, File


class RaspBodyMovingDetect(Action):

    # HC-SR501 Pin011 (GPIO17) for detection
    def execute(self):
        super(RaspBodyMovingDetect, self).execute()
        PIN_DETECTION = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN_DETECTION, GPIO.IN)

        try:
            while True:
                if GPIO.input(PIN_DETECTION) == 1:
                    logging.debug("Some people here!")

                    # Getting images
                    localtime = time.time()
                    os.system('raspistill -t 5000 -tl 750 -ISO 7000 -ss 50000 -o image_num_"%s"_%d.jpg' % localtime)
                else:
                    logging.debug("Nobody!")
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            logging.debug("Clean up")


class RaspCarCamera(Action, threading.Thread):

    def __init__(self, people_list):
        super(RaspCarCamera, self).__init__()
        threading.Thread.__init__(self)
        self.people = people_list

    def execute(self):
        cx = 160
        cy = 120
        xdeg = 150
        ydeg = 150

        # Setup the camera
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 16
        rawCapture = PiRGBArray(camera, size=(640, 480))

        # 2 secs for warmup.
        camera.start_preview()
        time.sleep(2)

        # Start to move the Camera
        camera_rolling = RaspCarCameraRolling()
        camera_rolling.setDaemon(True)
        camera_rolling.start()

        # Load a cascade file for detecting faces
        face_cascade = cv2.CascadeClassifier('/home/pi/Eastworld/etc/frontalface.xml')

        num = 0
        frame_count = 0
        fps = FPS().start()
        # Capture frames from the camera
        stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
        for frame in stream:
            image = frame.array
            frame_count += 1

            # Use the cascade file we loaded to detect faces
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minSize=(48, 48))

            logging.debug("Found %d faces in frame %d" % (len(faces), frame_count))

            # Draw a rectangle around every face and move the motor towards the face
            for (x, y, w, h) in faces:

                cv2.rectangle(image, (x, y), (x + w, y + h), (100, 255, 100), 2)
                cv2.putText(image, "Face No." + str(len(faces)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                num += 1
                # Save the images
                image_name = 'capture_%d.jpg' % num
                cv2.imwrite(image_name, image)
                logging.info("Searching faces %d ..." % num)
                self.search_people(image_name)

            # Clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            fps.update()
            # stop the camera
            if num > 0 or frame_count > 60:
                break

        # stop the timer and display FPS information
        fps.stop()
        logging.info("Approx. FPS: %.2f in %.2f" % (fps.fps(), fps.elapsed()))

        logging.debug("Close camera & CV2")
        cv2.destroyAllWindows()
        stream.close()
        rawCapture.close()
        camera.close()

    def search_people(self, image):
        # You need to register your App first, and enter you API key/secret.
        API_KEY = "KwEun0LOHJV1pKKfN6e0NDdpE5RQEeOc"
        API_SECRET = "nrUA33mS7tTh1dZ_HWI4bQoTY1z-hHC9"
        faceset_id = 'mitang'
        api = API(API_KEY, API_SECRET)

        # Local picture location, please fill in the contents before calling demo
        face_search = image
        ret = api.faceset.getfacesets(outer_id=faceset_id)

        # detect image and search same face
        ret = api.detect(image_file=File(face_search))
        for face in ret["faces"]:
            # logging.debug("Detected face %s" % face)

            search_result = api.search(face_token=face["face_token"], outer_id=faceset_id)
            for result in search_result["results"]:
                # logging.debug("Searched face %s" % result)
                confidence = result["confidence"]
                user_id = result["user_id"]

                if float(confidence) > 50:
                    # put people into the people_list
                    user = {'user_id': user_id, 'confidence': confidence, 'time': time.time()}
                    self.people.insert(0, user)
                    logging.debug("People identified: %s" % user)

class RaspCarCameraRolling(Action, threading.Thread):
    # Rotation engine (PIN35, GPIO19) for Camera.
    PIN_ROTATION = 35

    def __init__(self, ):
        super(RaspCarCameraRolling, self).__init__()
        threading.Thread.__init__(self)

    def execute(self):
        super(RaspCarCameraRolling, self).execute()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_ROTATION, GPIO.OUT)
        logging.debug("RaspCarEyeRolling setup: PIN[%d]" % self.PIN_ROTATION)

        GPIO.output(self.PIN_ROTATION, GPIO.HIGH)
        p = GPIO.PWM(self.PIN_ROTATION, 50)  # 50HZ
        p.start(0)

        start_point = 2.5
        mid_point = 7.5
        length = 10.0

        for i in range(90, 151, 10):
            cycle = start_point + (length * i) / 180
            #logging.debug("Cycle %.2f", cycle)
            p.ChangeDutyCycle(cycle)
            time.sleep(0.02)
            p.ChangeDutyCycle(0)
            time.sleep(0.5)

        for i in range(150, 29, -10):
            cycle = start_point + (length * i) / 180
            #logging.debug("Cycle %.2f", cycle)
            p.ChangeDutyCycle(cycle)
            time.sleep(0.02)
            p.ChangeDutyCycle(0)
            time.sleep(0.5)

        for i in range(30, 91, 10):
            cycle = start_point + (length * i) / 180
            #logging.debug("Cycle %.2f", cycle)
            p.ChangeDutyCycle(cycle)
            time.sleep(0.02)
            p.ChangeDutyCycle(0)
            time.sleep(0.5)

        p.ChangeDutyCycle(mid_point)
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
        time.sleep(0.02)

    def finish(self):
        super(RaspCarCameraRolling, self).finish()
        GPIO.setup(self.PIN_ROTATION, GPIO.IN)
        logging.debug("RaspCarEyeRolling cleaned: PIN[%d]" % self.PIN_ROTATION)