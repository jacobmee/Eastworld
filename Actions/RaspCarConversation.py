# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import json
import logging
import time
import PyBaiduYuyin as pby

from os import path
from Actions.Action import Action


class RaspCarConversation(Action):

    def voice_control(self, conversation_request):
        conversation_response = ""

        if "启动" in conversation_request:
            logging.debug("Voice control to move forward")
        elif "糖糖" in conversation_request:
            conversation_response = "你在叫我？"
            self.enable_turing_machine = True
        elif "再见" in conversation_request or "拜拜" in conversation_request:
            if self.enable_turing_machine:
                conversation_response = "再见"
                self.enable_turing_machine = False
        if conversation_response != "":
            logging.debug("Voice control responses: %s" % conversation_response)
        return conversation_response

    def __init__(self):
        super(RaspCarConversation, self).__init__()
        self.in_conversation = True
        self.enable_voice_control = True
        self.enable_turing_machine = False
        self.silent_counts = 0

    def execute(self):
        api_key = "QUQgAhhdfODY9KbaR7928pHN"
        secret_key = "f994c8815ddef688325fe3be89ffc3d5"
        turing_api_key = "64c2b023d27eb2ffe1dcef2ac7b70e1b"

        b_tts = pby.TTS(app_key=api_key, secret_key=secret_key)
        b_tts.say("似乎睡了好久")

        # obtain audio from the microphone
        br = pby.Recognizer()
        # bm = pby.Microphone()

        while True:

            if not self.in_conversation:
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

            os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:0,0 etc/temp.wav')
            audio_file = path.join(path.dirname(path.realpath(__file__)), "/home/pi/Eastworld/etc/temp.wav")
            with pby.WavFile(audio_file) as source:
                audio = br.record(source)  # read the entire audio file

            # recognize speech using Baidu Speech Recognition
            try:
                result = br.recognize(audio)
                conversation_request = result.encode('utf-8').strip()
                logging.debug("Recognized: %s" % conversation_request)
            except LookupError as err:
                logging.info("Baidu Speech Recognition could not understand audio; {0}".format(err))
            except ValueError as err:
                logging.info("Baidu Speech Recognition could not understand audio; {0}".format(err))

            if self.enable_voice_control:
                conversation_response = self.voice_control(conversation_request)

            if conversation_request == "":
                self.silent_counts = self.silent_counts + 1
                if self.silent_counts == 10:
                    self.enable_turing_machine = False
                    conversation_response = "再见"

            # Turn to turing machine for answers.
            if self.enable_turing_machine and conversation_request != "" and conversation_response == "":
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