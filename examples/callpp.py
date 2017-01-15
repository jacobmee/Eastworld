#-*- coding: utf-8 -*-


# 您需要先注册一个App，并将得到的API key和API secret写在这里。
# You need to register your App first, and enter you API key/secret.
API_KEY = "KwEun0LOHJV1pKKfN6e0NDdpE5RQEeOc"
API_SECRET = "nrUA33mS7tTh1dZ_HWI4bQoTY1z-hHC9"

# 网络图片的URL地址,调用demo前请填上内容
# The url of network picture, please fill in the contents before calling demo
face_one = 'http://www.mitang.me/grandma.jpg'

# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
#face_two = './demo.jpeg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_search = './demo.jpeg'


# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
from pprint import pformat


def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))


# First import the API class from the SDK
# 首先，导入SDK中的API类
from Base.Facepp import API, File

api = API(API_KEY, API_SECRET)
faceset_id='mitang'

# 创建一个Faceset用来存储FaceToken
# create a Faceset to save FaceToken
# delect faceset because it is no longer needed
ret = api.faceset.getfacesets(outer_id=faceset_id)
print_result("faceset get", ret)

# 对图片进行检测
# detect image
'''Face = {}
user_id = 'grandma'
res = api.detect(image_url=face_one)
print_result(user_id, res)
face_token = res["faces"][0]["face_token"]
Face[user_id] = face_token

res = api.face.setuserid(face_token=face_token, user_id=user_id)
print_result(user_id, res)



# 将得到的FaceToken存进Faceset里面
# save FaceToken in Faceset
api.faceset.addface(outer_id=faceset_id, face_tokens=Face.itervalues())
'''

# 对待比对的图片进行检测，再搜索相似脸
# detect image and search same face
ret = api.detect(image_file=File(face_search))
print_result("detect", ret)
search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id=faceset_id)

# 输出结果
# print result
print_result('search', search_result)


# 删除无用的人脸库
# delect faceset because it is no longer needed
#api.faceset.delete(outer_id=faceset_id, check_empty=0)

# 恭喜！您已经完成了本教程，可以继续阅读我们的API文档并利用Face++ API开始写您自
# 己的App了！
# 旅途愉快 :)
# Congratulations! You have finished this tutorial, and you can continue
# reading our API document and start writing your own App using Face++ API!
# Enjoy :)