# -*- coding: utf-8 -*-

import PyBaiduYuyin as pby
import speech_recognition as sr
import os
from os import path


apiKey = "QUQgAhhdfODY9KbaR7928pHN"
secretKey = "f994c8815ddef688325fe3be89ffc3d5"
GOOGLE_KEY = "AIzaSyAcalCzUvPmmJ7CZBFOEWx2Z1ZSn4Vs1gg"

tts = pby.TTS(app_key=apiKey, secret_key=secretKey)

tts.say("你说")


# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()
m.RATE = 44100
#m.CHUNK = 512

'''with m as source:
    print("Say something!")
    audio = r.listen(source)'''

use_Google = True
use_Baidu = False

while True:

    # Try google first if can't access, always use Baidu
    if use_Google :


        os.system('arecord -r 16000 -d 3 -D plughw:0,0 temp.wav')
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp.wav")
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file

        '''''
        with m as source:
            print("Say something!")
            audio = r.listen(source)'''

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result = r.recognize_google(audio, GOOGLE_KEY, language="zh-CN")
            print("Google Speech Recognition thinks you said " + result)

            tts.say(result.encode('utf-8').strip())

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


    if use_Baidu :
        with m as source:
            r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            audio = r.listen(source)

        # instead of `r.recognize_google(audio, show_all=True)`
        print "Recognize ... "
        resultTmp = r.recognize(audio)
        # print resultTmp[u'alternative'], type(resultTmp[u'alternative'])
        print "Result: %s" %resultTmp
        tts.say(resultTmp.encode('utf-8').strip())

