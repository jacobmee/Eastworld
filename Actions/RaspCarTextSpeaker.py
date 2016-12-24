import json
import os
import sys
import urllib2

from Actions.Action import Action


class RaspToSpeak(Action):
    def execute(self):
        reload(sys)  # reload 才能调用 setdefaultencoding 方法
        sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

        apiKey = "QUQgAhhdfODY9KbaR7928pHN"
        secretKey = "f994c8815ddef688325fe3be89ffc3d5"
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;
        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        token = json.loads(json_data)['access_token']

        message = "大家好，让你们久等了！"

        url = "http://tsn.baidu.com/text2audio?tex=" + message + "&lan=zh&per=0&pit=1&spd=7&cuid=7519663&ctp=1&tok=" + token
        print url
        os.system('mpg123 "%s"' % (url))