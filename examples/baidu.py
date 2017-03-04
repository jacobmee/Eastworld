#!/usr/bin/env python
# coding: utf-8
import urllib2
import json
import base64
import  os
from os import path

#设置应用信息
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "QUQgAhhdfODY9KbaR7928pHN" #填写API Key
client_secret = "f994c8815ddef688325fe3be89ffc3d5" #填写Secret Key

#合成请求token的URL
url = baidu_server+"grant_type="+grant_type+"&client_id="+client_id+"&client_secret="+client_secret

#获取token
res = urllib2.urlopen(url).read()
data = json.loads(res)
token = data["access_token"]
print token

#设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
VOICE_RATE = 16000
USER_ID = "hail_hydra" #用于标识的ID，可以随意设置
WAVE_TYPE = "wav"

#打开音频文件，并进行编码
os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:1,0 temp.wav')
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp.wav")

f = open(AUDIO_FILE, "r")
speech = base64.b64encode(f.read())
size = os.path.getsize(AUDIO_FILE)
print size
update = json.dumps({"format":WAVE_TYPE, "rate":VOICE_RATE, 'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size})
headers = { 'Content-Type' : 'application/json' }
url = "http://vop.baidu.com/server_api"
req = urllib2.Request(url, update, headers)
print req
r = urllib2.urlopen(req)


t = r.read()
result = json.loads(t)
print result
if result['err_msg']=='success.':
    word = result['result'][0].encode('utf-8')
    if word!='':
        if word[len(word)-3:len(word)]=='，':
            print word[0:len(word)-3]
        else:
            print word
    else:
        print "音频文件不存在或格式错误"
else:
    print "错误"