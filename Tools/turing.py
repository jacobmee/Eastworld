# -*- coding: utf-8 -*-

import urllib2
import sys
import json


words = "上海天气如何？"
url = "http://apis.baidu.com/turing/turing/turing?"

key = "879a6cb3afb84dbf4fc84a1df2ab7319"
userid = "1000"
api_key = "64c2b023d27eb2ffe1dcef2ac7b70e1b"
#words = urllib2.Parse.quote(words)
url = url + "key=" + key + "&info=" + words + "&userid=" + userid

req = urllib2.Request(url)
req.add_header("apikey", api_key)

print("robot start request")
resp = urllib2.urlopen(req)
print("robot stop request")
content = resp.read()
if content:
    data = json.loads(content.decode("utf-8"))
    print(data["text"])

