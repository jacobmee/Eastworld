# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import json
import logging
import time
import PyBaiduYuyin as pby
import speech_recognition as sr

from os import path
from Actions.Action import Action
from Actions.RaspCarEyeRolling import RaspCarEyeRolling
from Actions.RaspCarMovement import RaspCarMove


class RaspCarConversation(Action):

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

            if "音乐" in conversation_request or  "唱歌" in conversation_request:
                    logging.debug("VOICE: Music")
                    conversation_response = "来点我的最爱"

                    # Create a thread and make eye rolling action.
                    os.system('sh /home/pi/Eastworld/etc/music.sh start')
                    self.is_listening = False
                    time.sleep(300)
                    os.system('sh /home/pi/Eastworld/etc/music.sh stop')
                    self.is_listening = True

            if "电台" in conversation_request:
                    logging.debug("VOICE: Radio")
                    conversation_response = "电台这么老掉牙的你也听？"

                    # Create a thread and make eye rolling action.
                    os.system('sh /home/pi/Eastworld/etc/radio.sh start')
                    self.is_listening = False
                    time.sleep(300)
                    os.system('sh /home/pi/Eastworld/etc/radio.sh stop')
                    self.is_listening = True

            elif "再见" in conversation_request or "拜拜" in conversation_request:
                if self.is_interactive:
                    logging.debug("VOICE: Bye")
                    conversation_response = "再见"
                    self.is_interactive = False

        # Actions for wake up or surprising
        if not self.is_interactive:
            if "DOLORES" in conversation_request:
                logging.debug("VOICE: Wake me up")
                conversation_response = "你在叫我？"
                self.is_interactive = True
                self.silent_counts = 0

                # Create a thread and make eye rolling action.
                eye_rolling = RaspCarEyeRolling()
                eye_rolling.setDaemon(True)
                eye_rolling.start()

        if conversation_response != "":
            logging.debug("VOICE RES: %s" % conversation_response)

        return conversation_response

    def __init__(self):
        super(RaspCarConversation, self).__init__()
        self.is_listening = True
        self.is_interactive = False
        self.silent_counts = 0

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
                time.sleep(3)  # Wait for 3 seconds, in case conversion is stopped, and it goes to a different action
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
            os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:1,0 /home/pi/Eastworld/etc/temp.wav')

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
                with pby.WavFile(audio_file) as source:
                    audio = br.record(source)  # read the entire audio file

                # recognize speech using Baidu Speech Recognition
                try:
                    result = br.recognize(audio)
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
                url = "http://apis.baidu.com/turing/turing/turing?"
                key = "879a6cb3afb84dbf4fc84a1df2ab7319"
                user_id = "1000"

                # words = urllib2.Parse.quote(words)
                url = url + "key=" + key + "&info=" + conversation_request + "&userid=" + user_id

                try:
                    req = urllib2.Request(url)
                    req.add_header("apikey", turing_api_key)

                    resp = urllib2.urlopen(req)
                    content = resp.read()

                    if content:
                        data = json.loads(content.decode("utf-8"))
                        conversation_response = data["text"].encode('utf-8').strip()
                        self.silent_counts = 0
                except ValueError as err:
                    logging.error("Baidu Turing could not do the service; {0}".format(err))

                logging.debug("Turing answered: %s" % conversation_response)

            try:
                if conversation_response != "":
                    b_tts.say(conversation_response)
            except ValueError as err:
                logging.error("Baidu Text to Speak could not do the service; {0}".format(err))