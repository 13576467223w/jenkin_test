import jsonpath
import requests

from JK_auto.aes_encrypt import EncryptData

'''
所有的接口发送请求，都需要
url地址
请求方式 method
用户参数 params data 
'''
# 用户登录接口
res_login = requests.request(url="http://shop-xo.hctestedu.com/index.php?s=api/user/login",
                       method="post", params={"application":"app",
                                              "application_client_type":"weixin"},
                       data={"accounts":"huace_xm","pwd":"123456","type":"username"}) # 发送请求
print(res_login.json())  # 应答

# 对结果做校验--断言 assert
assert "登录成功" == res_login.json()["msg"]
assert "28" == res_login.json()["data"]["id"]
assert "huace_xm" == res_login.json()["data"]["username"]


'''
# 接口关联问题  后面的接口的成功执行需要借助前面接口的返回值，从前面接口返回结果获取返回的值存变量
1、获取值得方式：用json数据的key获取
2、jsonpath获取【实际工作中常用的写法】
    知道在哪里  $.key
    不知在那层  $..key
'''
token = res_login.json()["data"]["token"]
token1 = jsonpath.jsonpath(res_login.json(), "$.data.token")[0] # 返回的是一个列表
print(token1)
# 商品收藏、取消接口
res = requests.request(url="http://shop-xo.hctestedu.com/index.php?s=api/goods/favor&token="+token1,
                       method="post", params={"application":"app",
                                              "application_client_type":"weixin"},
                       data={"id":12}) # 发送请求
print(res.json())  # 应答


'''
加密接口问题
https---网络传输过程中加密
加密接口---先把明文变成密文，再传输

加密算法有多种，工作中，遇到加密接口，问开发，密钥是什么，加密算法用了什么

'''
ens = EncryptData('1234567812345678') # 参数：密钥
username = ens.encrypt("tony")
password = ens.encrypt("123456")
print(username)
print(password)
#解密
u = ens.decrypt(username)
print(u)


'''
框架化这套体系  根据情况封装----自定义封装
设计动作--通用化我们的自动化测试
'''