# -*- coding: utf-8 -*-
import os
from gtts import gTTS
import PyBaiduYuyin as pby

text="我今天运气真不错，没有摔跤。"

use_google = False
if use_google:
    audio_file = "temp.mp3"
    tts = gTTS(text, lang="zh-cn")
    tts.save(audio_file)
    os.system('mpg123 "%s"' % audio_file)
else :
    apiKey = "QUQgAhhdfODY9KbaR7928pHN"
    secretKey = "f994c8815ddef688325fe3be89ffc3d5"
    tts = pby.TTS(app_key=apiKey, secret_key=secretKey)
    tts.say(text)
