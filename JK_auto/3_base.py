# 测试开发

'''
代码质量是否合格---是否需要白盒测试能力？  【借助代码扫描工具--sonar】

'''

# sonar
# pip install pysonar

'''
关于在jenkins上执行sonar代码扫描工具
Build Steps：--Execute SonarQube Scanner
sonar.projectName=java_demo  # 名称
sonar.projectKey=test1 # key
sonar.exclusions=src/test/** #跳过此路径下test目录的文件
sonar.language=java # 代码语言
sonar.login=admin  # sonar用户名
sonar.password=Admin123456.  # sonar用户密码

需要扫描git中的代码
Triggers（触发器）--Generic Webhook Trigger（有人上传代码时触发）--token（随便什么）
有人git上传代码调用jenkins的程序，需要先在git仓库设置中设置web钩子
推送地址：对应的jenkins地址  http：//JENKINS_URL/generic-webhook-trigger/invoke？token=... 替换JENKINS_URL
'''