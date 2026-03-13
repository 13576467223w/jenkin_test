import os
import shutil

import pytest


# 测试框架的主入口
def run():
    allure_dir = "./v1/allure-result"
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
    pytest.main([
        "-v",
        "-s",
        "--capture=no", # 比 --capture=sys 更彻底地显示打印
        "--alluredir=" + allure_dir,
        "--clean-alluredir",
        "./v1/test.py" # 确保文件名正确
    ])


if __name__ == "__main__":
    run()
    os.system("allure generate allure-result -o ./v1/report_allure --clean") # 生成的index.html文件需在pycharm中点击查看 或者命令行输入 allure open +报告路径