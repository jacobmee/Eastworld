import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import sys
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import logging
import logging.config
import os
import threading
import time
import argparse
import imutils

from Base.Facepp import API, File
logging.config.fileConfig("/home/pi/Eastworld/etc/logging.conf")

def search_people(image):
    # You need to register your App first, and enter you API key/secret.
    API_KEY = "KwEun0LOHJV1pKKfN6e0NDdpE5RQEeOc"
    API_SECRET = "nrUA33mS7tTh1dZ_HWI4bQoTY1z-hHC9"
    faceset_id = 'mitang'
    api = API(API_KEY, API_SECRET)

    # Local picture location, please fill in the contents before calling demo
    face_search = image
    # delect faceset because it is no longer needed
    ret = api.faceset.getfacesets(outer_id=faceset_id)
    # logging.debug("getting faceset")

    # detect image and search same face
    ret = api.detect(image_file=File(face_search))
    print("Detected face %s" % ret)
    for face in ret["faces"]:
        print("Detected face %s" % face)

        search_result = api.search(face_token=face["face_token"], outer_id=faceset_id)
        # print result
        print("Return face %s" % search_result)
        for result in search_result["results"]:
            print("userid=%s" % result["user_id"])
            print("confidence=%s" % result["confidence"])

        # put people into the people_list
        # self.faces



cx = 160
cy = 120
xdeg = 150
ydeg = 150

# Setup the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(640, 480))

# 2 secs for warm up.
camera.start_preview()
time.sleep(2)

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
        #search_people(image_name)

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    fps.update()
    # stop the camera
    if num > 10 or frame_count > 200:
        break

# stop the timer and display FPS information
fps.stop()
logging.info("Approx. FPS: %.2f in %.2f" % (fps.fps(), fps.elapsed()))

logging.debug("Close camera & CV2")
cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()


