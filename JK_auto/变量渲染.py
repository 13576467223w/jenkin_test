from string import Template

"""
Template:模板替换
规则如下：
字符串特殊字符 ${文字}  字典：{文字：xxx}
特殊字符串中${}内部的文字 与 字典的key相同，
就会自动拿value换掉 ${}
"""

ss = {"token":"111111"}
str = "${token}是一串神奇号码"
print(Template(str).substitute(ss))