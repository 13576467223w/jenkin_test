'''
重要性
自动化测试---把人力解放出来---更稳定---人工实行会有问题


把手工测试的流程，用代码再去复现一次
效验结果数据对或者不对

接口测试：
url地址
请求参数
请求方式
应答结果
一般情况下不需要加上请求头，如有需要，另加即可


发起测试的几个动作
发送
接收

自动化：用代码实现怎么发，怎么接

'''

import os
import sys



def create_folder_in_exe_dir(folder_name):
    # 1. 获取 exe 所在目录
    base_dir = os.path.dirname(sys.executable)

    # 2. 拼接新文件夹的完整路径
    new_folder_path = os.path.join(base_dir, folder_name)

    # 3. 创建文件夹 (exist_ok=True 表示如果文件夹已存在则不报错)
    try:
        os.makedirs(new_folder_path, exist_ok=True)
        print(f"成功在以下路径创建文件夹: {new_folder_path}")
        return new_folder_path
    except Exception as e:
        print(f"创建文件夹失败: {e}")
        return None

if __name__ == '__main__':
    for i in range(1,51):
        create_folder_in_exe_dir(str(i))