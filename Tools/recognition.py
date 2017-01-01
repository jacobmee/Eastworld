# -*- coding: utf-8 -*-

import PyBaiduYuyin as pby
from gtts import gTTS
import speech_recognition as sr
import os
from os import path


apiKey = "QUQgAhhdfODY9KbaR7928pHN"
secretKey = "f994c8815ddef688325fe3be89ffc3d5"
GOOGLE_KEY = "AIzaSyAcalCzUvPmmJ7CZBFOEWx2Z1ZSn4Vs1gg"

btts = pby.TTS(app_key=apiKey, secret_key=secretKey)
btts.say("你说")

# obtain audio from the microphone
gr = sr.Recognizer()
gm = sr.Microphone(sample_rate=16000)
#gm.RATE = 16000
#m.CHUNK = 512

br = pby.Recognizer()
bm = pby.Microphone()

use_Google_recognize = True
use_Google_TTS = False
use_Baidu_recognize = False
use_Baidu_TTS = True



while True:

    text = "没听到"
    # Try google first if can't access, always use Baidu
    if use_Google_recognize :



        os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:0,0 temp.wav')
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp.wav")
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = gr.record(source)  # read the entire audio file

        '''
        with gm as source:
            print("Say something!")
            audio = gr.listen(source)'''

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result = gr.recognize_google(audio, GOOGLE_KEY, language="zh-CN")
            print("Google Speech Recognition thinks you said " + result)

            text = result.encode('utf-8').strip()

        except sr.UnknownValueError:
            print("Google Speech Recogni/tion could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if use_Baidu_recognize :

        with bm as source:
            br.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            audio = br.listen(source)

        # instead of `r.recognize_google(audio, show_all=True)`
        print "Recognize ... "
        result = br.recognize(audio)
        text = result.encode('utf-8').strip()

    print "Result: %s" % text

    if use_Google_TTS:
        audio_file = "temp.mp3"
        gtts = gTTS(text, lang="zh-cn")
        gtts.save(audio_file)
        os.system('mpg123 "%s"' % audio_file)

    if use_Baidu_TTS:
        # print resultTmp[u'alternative'], type(resultTmp[u'alternative'])
        btts.say(text)