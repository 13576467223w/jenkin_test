import string  # 修正导入：应该是 string.Template 而不是 from string import Template
from string import Template
import jsonpath
import pytest
import requests
import json
import pandas as pd

# from xToolkit import xfile # 如果没安装这个库，请注释掉或用 pandas 替代

# 读取数据
# 确保 Excel 文件路径正确，且 Sheet1 存在
try:
    data = pd.read_excel(r"D:\files\py_project\PythonProject\PythonProject\autoTest\JK_auto\测试用例.xlsx",
                         sheet_name="Sheet1").to_dict(orient='records')
except Exception as e:
    print(f"读取 Excel 失败: {e}")
    data = []

dic = {}  # 存放公共数据


@pytest.mark.parametrize("case_info", data)
def test_execute(case_info):
    # 1. 处理 URL
    url = case_info.get('接口url', '')
    if "$" in str(url):
        try:
            url = Template(str(url)).safe_substitute(dic)  # 使用 safe_substitute 防止变量缺失报错
        except Exception as e:
            print(f"URL 渲染失败: {e}")

    # 2. 处理 Params (修复 eval 风险)
    params_data = case_info.get('url参数', '')
    params = {}
    if params_data:
        try:
            # 尝试作为 JSON 解析 (推荐)
            if isinstance(params_data, str) and (params_data.startswith('{') or params_data.startswith('[')):
                params = json.loads(params_data)
            else:
                # 如果是旧式的字典字符串 {'k': 'v'}，才用 eval (不推荐但兼容旧数据)
                # 为了安全，建议 Excel 里填 JSON 格式 {"k": "v"}
                params = eval(params_data)
        except Exception as e:
            print(f"⚠️ 参数解析失败: {params_data}, 错误: {e}")
            params = {}

    # 3. 处理 Data/Json
    json_data = {}
    if case_info.get('json参数'):
        try:
            json_data = json.loads(case_info['json参数'])
        except Exception as e:
            print(f"⚠️ JSON 参数解析失败: {e}")

    # 4. 发送请求
    try:
        res = requests.request(
            method=case_info.get('请求方式', 'GET'),
            url=url,
            json=json_data,  # 推荐使用 json 参数自动序列化
            params=params,
            timeout=10
        )

        # 5. 断言
        assert res.status_code == case_info.get(
            '预期状态码'), f"状态码不符: 期望 {case_info.get('预期状态码')}, 实际 {res.status_code}"

        # 6. 提取参数
        if case_info.get('提取参数'):
            try:
                # 确保响应是 JSON
                response_json = res.json()
                # jsonpath 语法修正：通常不需要 "$..key"，除非是递归搜索。如果是特定路径直接用 "$.key"
                # 这里保留你的逻辑，但增加容错
                expr = f"$..{case_info['提取参数']}"
                result = jsonpath.jsonpath(response_json, expr)

                if result:
                    dic[case_info["提取参数"]] = result[0]
                    print(f"✅ 提取成功: {case_info['提取参数']} = {result[0]}")
                else:
                    print(f"⚠️ 未提取到值: {case_info['提取参数']}")
            except Exception as e:
                print(f"⚠️ 参数提取失败: {e}")

    except Exception as e:
        pytest.fail(f"请求执行失败: {str(e)}")


        # 未知原因 main 部分代码并未被执行 可另写一个文件调用此文件或在终端执行
if __name__ == '__main__':
    import os
    import shutil
    print('come')
    allure_dir = "./allure-result"

    # 清理旧结果
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)

    # 运行 Pytest
    # 修正点：-v 和 -s 分开写，确保 allure-pytest 能拦截

    pytest.main([
        "-v",
        "-s",
        "--capture=no",  # 比 --capture=sys 更彻底地显示打印
        "--alluredir=" + allure_dir,
        "--clean-alluredir",
        os.path.abspath(__file__)  # 确保文件名正确
    ])

    # 【重要】自动打开报告提示
    print("\n" + "=" * 30)
    print("✅ 测试执行完毕！")
    print(f"📂 原始数据已生成在: {os.path.abspath(allure_dir)}")
    print("🚀 请在终端运行以下命令查看报告:")
    print(f"   allure serve {allure_dir}")
    print("   或者:")
    print(f"   allure generate {allure_dir} -o report_html --clean")
    print("=" * 30 + "\n")