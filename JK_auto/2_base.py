import os
from string import Template

import jsonpath
import pytest
import requests
import json
import pandas as pd
from xToolkit import xfile
# 接口自动化封装

'''
框架封装
'''
# data = xfile.read(r"D:\files\py_project\PythonProject\PythonProject\autoTest\JK_auto\测试用例.xlsx").excel_to_dict()
data = pd.read_excel(r"D:\files\py_project\PythonProject\PythonProject\autoTest\JK_auto\测试用例.xlsx",sheet_name="Sheet1").to_dict(orient='records')
dic = {} # 存放公共数据
# 发送
@pytest.mark.parametrize("case_info",data) # 和for循环作用一样 函数名要test开头
def test_excute(case_info):
    url = case_info['接口url']
    if "$" in url: # 变量渲染
        url = Template(url).substitute(dic)
    res = requests.request(method=case_info['请求方式'], url=url, data=json.loads(case_info['json参数']), params=eval(case_info['url参数']))# 转格式  json 或者 eval
    # print(res.json())
    assert res.status_code == case_info['预期状态码']
    '''
    判断是否要提取返回结果的值,存到公共容器中
    '''
    if case_info["提取参数"]:
        param = jsonpath.jsonpath(res.json(),"$.."+case_info['提取参数'])
        dic[case_info["提取参数"]] = param[0]
        # print(dic)

    '''
    测试报告  allure生成（纯命令）allure-comand-line
    allure generate 本次测试结果的文件夹位置（e://XXX ） -o 测试报告的路径（自动生成） --clean
    '''

# 未知原因 main 部分代码并未被执行 可另写一个文件调用此文件执行    或在终端执行
# if __name__ == '__main__':
#     # 以下命令需要先下载alluer 并配置环境变量,若没生成测试结果，则尝试终端pytest 2_base.py -v -s --alluredir=./allure-result --clean-alluredir
#     # pytest.main(["-vs",
#     #              "--capture=sys", # 捕获输出
#     #              "2_base.py",
#     #             "--clean-alluredir",# 执行前清除上次执行的结果
#     #             "--alluredir=allure-result" # 本次结果存放位置
#     #              ])
#     allure_dir = "allure-result"
#     pytest.main([
#         "-v",
#         "-s",
#         "--capture=no", # 比 --capture=sys 更彻底地显示打印
#         "--alluredir=" + allure_dir,
#         "--clean-alluredir",
#         "2_base.py" # 确保文件名正确
#     ])
#     os.system("allure generate allure-result -o ./report_allure --clean") # 生成测试报告




# 调用函数 执行登录 ---- 工具化--- jar包war包 ---exe文件
# excute(url="http://shop-xo.hctestedu.com/index.php?s=api/user/login",
#                        method="post", params={"application":"app","application_client_type":"weixin"},
#                        data={"accounts":"huace_xm","pwd":"123456","type":"username"})

# 打包exe文件  终端执行 pyinstaller -F + 要打包的文件名
# 执行文件与数据文件分离  读取指定路径的数据文件，做到通过修改数据文件，访问不同的接口
# 数据文件 -- 有格式---yaml文件，excel文件，数据库，redis都可以用
# 核心思路：读数据--执行测试--断言--生成报告  DDT数据驱动测试 传入参数去访问不同的个接口进行测试

# for item in data:
#     excute(url=item["接口url"],
#            method=item['请求方式'], params=json.loads(item['url参数']), # 转格式  json 或者 eval
#            data=eval(item['json参数']))


# jenkins 是纯命令行的辅助工具