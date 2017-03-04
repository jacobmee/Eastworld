# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import json
import logging
import time
import speech_recognition as sr
import RPi.GPIO as GPIO
import logging.config


from os import path
from Base import BDYY as pby
from Actions.Action import Action
from Actions.RaspCarEyeRolling import RaspCarEyeRolling
from Actions.RaspCarMovement import RaspCarMove
from Actions.RaspCarBodyDetect import RaspCarCamera


class RaspCarConversation(Action):
    # LED color
    PIN_LED_RED = 33
    PIN_LED_GREEN = 31
    PIN_LED_BLUE = 29

    # color
    color_listening = [0, 0, 125]  # Blue
    color_speaking = [0, 125, 0]  # Green
    color_thinking = [125, 0, 0]  # Red
    color_sleeping = [0, 0, 0]  # Dark

    def voice_control(self, conversation_request):
        conversation_response = ""

        # Actions require already in interaction mode.
        if self.is_interactive:
            if "运动" in conversation_request:
                logging.debug("VOICE: Move forward")
                conversation_response = "来追我啊"

                # Create a thread and make eye rolling action.
                raspcar_move = RaspCarMove(steps=5)
                raspcar_move.setDaemon(True)
                raspcar_move.start()
            elif "音乐" in conversation_request or  "唱歌" in conversation_request:
                logging.debug("VOICE: Music")
                conversation_response = "来点我的最爱"

                # Create a thread and make eye rolling action.
                os.system('sh /home/pi/Eastworld/etc/music.sh start')
                self.is_listening = False
                time.sleep(300)
                os.system('sh /home/pi/Eastworld/etc/music.sh stop')
                self.is_listening = True
            elif "电台" in conversation_request:
                logging.debug("VOICE: Radio")
                conversation_response = "电台这么老掉牙的你也听？"

                # Create a thread and make eye rolling action.
                os.system('sh /home/pi/Eastworld/etc/radio.sh start')
                self.is_listening = False
                time.sleep(300)
                os.system('sh /home/pi/Eastworld/etc/radio.sh stop')
                self.is_listening = True
            elif "是谁" in conversation_request or "认识" in conversation_request:
                logging.debug("VOICE: who am I")

                # user = {'user_id': user_id, 'confidence': confidence, 'time': time.time()}
                if len(self.people_list) > 0:
                    user = self.people_list[0]
                    user_id = user['user_id']
                    if float(user['confidence']) > 7.0:
                        conversation_response += "我认识你啊，你是"
                    elif float(user['confidence']) > 5.0:
                        conversation_response += "我不太看得清，是不是"

                    if "jacob" in user_id:
                        conversation_response += "大宓啊"
                    elif "lily" in user_id:
                        conversation_response += "丽丽啊"
                    elif "max" in user_id:
                        conversation_response += "宓宓啊"
                    elif "grandma" in user_id:
                        conversation_response += "奶奶啊"
                    elif "grandpa" in user_id:
                        conversation_response += "爷爷啊"
                    else:
                        conversation_response += user_id.encode('utf-8').strip()
            elif "你睡吧" in conversation_request:
                if self.is_interactive:
                    logging.debug("VOICE: Go sleep")

                    conversation_response = "正好好久没休息了，让我好好睡一觉！"

                    self.is_interactive = False
                    self.is_listening = False
                    self.sleep_time = 3*60*60  # Sleep for three hours.
            elif "再见" in conversation_request or "拜拜" in conversation_request:
                if self.is_interactive:
                    logging.debug("VOICE: Bye")
                    conversation_response = "再见"
                    self.is_interactive = False

        # Actions for wake up or surprising
        if not self.is_interactive:
            if "HI DOLORES" in conversation_request:
                logging.debug("VOICE: Wake me up")
                conversation_response = "你在叫我？"
                self.is_interactive = True
                self.silent_counts = 0

                # Create a thread and make eye rolling action.
                # eye_rolling = RaspCarEyeRolling()
                # eye_rolling.setDaemon(True)
                # eye_rolling.start()

                raspcar_camera = RaspCarCamera(self.people_list)
                raspcar_camera.setDaemon(True)
                raspcar_camera.start()

        if conversation_response != "":
            logging.debug("VOICE RES: %s" % conversation_response)

        return conversation_response

    def finish(self):
        super(RaspCarConversation, self).finish()
        GPIO.setup(self.PIN_LED_BLUE, GPIO.IN)
        GPIO.setup(self.PIN_LED_GREEN, GPIO.IN)
        GPIO.setup(self.PIN_LED_RED, GPIO.IN)
        logging.debug("LED cleaned: PIN[%d], PIN[%d], PIN[%d]" % (self.PIN_LED_RED, self.PIN_LED_GREEN, self.PIN_LED_BLUE))

    def __init__(self):
        super(RaspCarConversation, self).__init__()
        self.is_listening = True
        self.sleep_time = 3
        self.is_interactive = False
        self.silent_counts = 0
        self.people_list = []

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_LED_RED, GPIO.OUT)
        GPIO.setup(self.PIN_LED_GREEN, GPIO.OUT)
        GPIO.setup(self.PIN_LED_BLUE, GPIO.OUT)

        self.led_red = GPIO.PWM(self.PIN_LED_RED, 50)
        self.led_red.start(0)
        self.led_green = GPIO.PWM(self.PIN_LED_GREEN, 50)
        self.led_green.start(0)
        self.led_blue = GPIO.PWM(self.PIN_LED_BLUE, 50)
        self.led_blue.start(0)

    def set_color(self, color):
        self.led_red.ChangeDutyCycle(color[0] / 2.55)
        self.led_green.ChangeDutyCycle(color[1] / 2.55)
        self.led_blue.ChangeDutyCycle(color[2] / 2.55)

    def execute(self):
        api_key = "QUQgAhhdfODY9KbaR7928pHN"
        secret_key = "f994c8815ddef688325fe3be89ffc3d5"
        turing_api_key = "64c2b023d27eb2ffe1dcef2ac7b70e1b"

        b_tts = pby.TTS(app_key=api_key, secret_key=secret_key)
        b_tts.say("似乎睡了好久")

        # obtain audio from the microphone
        gr = sr.Recognizer()
        br = pby.Recognizer()
        # bm = pby.Microphone()

        while True:

            if not self.is_listening:
                logging.info("I'm going to sleep for [%d]s" % self.sleep_time)
                self.set_color(self.color_sleeping)
                time.sleep(self.sleep_time)
                self.is_listening = True
                self.set_color(self.color_listening)
                continue

            conversation_request = ""
            conversation_response = ""
            # Disable the listen function because it doesn't work well with current USB audio.
            # My guess is the bug from pyAudio module.
            # with bm as source:
            #    listen for 1 second to calibrate the energy threshold for ambient noise levels
            #    br.adjust_for_ambient_noise(source)
            #    audio = br.listen(source)

            # Use the system record to save as wav file, then read to Baidu.
            self.set_color(self.color_listening)
            os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:1,0 /home/pi/Eastworld/etc/temp.wav')
            self.set_color(self.color_thinking)

            if not self.is_interactive:
                AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "/home/pi/Eastworld/etc/temp.wav")
                with sr.AudioFile(AUDIO_FILE) as source:
                    audio = gr.record(source)  # read the entire audio file]\

                # recognize speech using Sphinx
                try:
                    conversation_request = gr.recognize_sphinx(audio)
                    logging.debug("Sphinx: Recognized: %s" % conversation_request)
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))

            else:
                audio_file = path.join(path.dirname(path.realpath(__file__)), "/home/pi/Eastworld/etc/temp.wav")

                # recognize speech using Baidu Speech Recognition
                try:
                    result = br.recognize_WAV(audio_file)
                    conversation_request = result.encode('utf-8').strip()
                    logging.debug("Baidu: Recognized: %s" % conversation_request)
                except LookupError as err:
                    logging.info("Baidu Speech Recognition Lookup {0}, %d".format(err) % self.silent_counts)
                except ValueError as err:
                    logging.info("Baidu Speech Recognition Value {0}".format(err))

            # Goes into voice control
            conversation_response = self.voice_control(conversation_request)

            # if nothing to say in 30 seconds, say good bye.
            if conversation_request == "":
                self.silent_counts += 1
                if self.silent_counts == 10 and self.is_interactive:
                    self.is_interactive = False
                    conversation_response = "再见"
                    logging.debug("IDLE: Bye")

            # Turn to turing machine for answers.
            if self.is_interactive and conversation_request != "" and conversation_response == "":
                url = "http://www.tuling123.com/openapi/api?"
                key = "45fa933f47bb45fb8e7746759ba9b24a"
                user_id = "10000"

                # words = urllib2.Parse.quote(words)
                url = url + "key=" + key + "&info=" + conversation_request + "&userid=" + user_id

                try:
                    req = urllib2.Request(url)
                    req.add_header("apikey", turing_api_key)

                    resp = urllib2.urlopen(req)
                    content = resp.read()

                    if content:
                        data = json.loads(content.decode("utf-8"))
                        #logging.debug("Baidu Turing: %s" %data)
                        conversation_response = data["text"].encode('utf-8').strip()
                        self.silent_counts = 0
                except ValueError as err:
                    logging.error("Baidu Turing could not do the service; {0}".format(err))
                    conversation_response = "我都惊呆了"
                except KeyError as err:
                    logging.error("Baidu Turing could not do the service; {0}".format(err))
                    conversation_response = "让我静一静"

                logging.debug("Turing answered: %s" % conversation_response)

            try:
                if conversation_response != "":
                    if len(conversation_response) > 1024:
                        conversation_response = conversation_response[0:1024]

                    self.set_color(self.color_speaking)
                    b_tts.say(conversation_response)
                    self.set_color(self.color_thinking)
            except ValueError as err:
                logging.error("Baidu Text to Speak could not do the service; {0}".format(err))