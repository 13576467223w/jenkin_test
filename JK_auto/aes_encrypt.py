# import base64
# import sys
# from Crypto.Cipher import AES
# # from Crypto.Util.Padding import pad, unpad
#
# class EncryptData:
#     def __init__(self,key):
#         self.key = key.encode('utf8') # 初始化密钥
#         self.length = AES.block_size # 初始化数据大小
#         self.aes = AES.new(self.key, AES.MODE_CBC) # 初始化AES,ECB模式的实例
#         # 截断函数，去除填充的字符
#         self.unpad = lambda date: date[0:-ord(date[len(date)-1:])]
#
#     def pad(self,text):
#         '''
#         填充函数，使加密数据的字节码长度是block_size的整数倍
#         '''
#         count = len(text.encode('utf-8'))
#         add = self.length - (count % self.length)
#         entext = text + (chr(add)*add)
#         return entext
#
#     def encrypt(self,encrData): # 加密函数
#         res = self.aes.encrypt(self.pad(encrData).encode('utf8'))
#         msg = str(base64.b64encode(res),encoding='utf8')
#         return msg
#
#     def decrypt(self,drcrData):#解密函数
#         cipher = AES.new(self.key, AES.MODE_CBC)
#         res = base64.decodebytes(drcrData.encode('utf8'))
#         msg = cipher.decrypt(res).decode('utf8')
#         return self.unpad(msg)
#
# if __name__ == '__main__':
#     key = sys.argv[1] # key密钥
#     data = sys.argv[2] # 数据
#     eg = EncryptData(key) # 这里密钥的长度必须是16的倍数
#     result = eg.encrypt(str(data))
#     print(result,end='')


import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
'''
加密解密

'''

class EncryptData:
    def __init__(self, key):
        """
        初始化
        :param key: 密钥字符串
        """
        # 1. 统一的密钥处理逻辑 (关键！)
        # 将密钥转为 bytes
        key_bytes = key.encode('utf-8')

        # AES 要求密钥长度必须是 16, 24, 或 32 字节
        if len(key_bytes) < 16:
            # 如果太短，用 null 字节填充到 16
            self.key = key_bytes.ljust(16, b'\0')
        elif len(key_bytes) > 32:
            # 如果太长，截取前 32 字节 (优先匹配 AES-256)
            self.key = key_bytes[:32]
        else:
            # 如果在 16-32 之间但不是 16/24/32，填充到下一个合法长度
            if len(key_bytes) <= 16:
                self.key = key_bytes.ljust(16, b'\0')
            elif len(key_bytes) <= 24:
                self.key = key_bytes.ljust(24, b'\0')
            else:
                self.key = key_bytes.ljust(32, b'\0')

        # 2. 统一的 IV (初始化向量)
        # 必须固定为 16 字节。
        # 【重要】：加密和解密必须使用完全相同的 IV 字符串！
        self.iv = b'0123456789abcdef'  # 刚好 16 字节

    def _get_cipher(self):
        """
        内部辅助方法：每次返回一个新的 AES 对象
        避免状态污染
        """
        return AES.new(self.key, AES.MODE_CBC, self.iv)

    def encrypt(self, encrData):
        """
        加密
        """
        cipher = self._get_cipher()
        data_bytes = encrData.encode('utf-8')
        padded_data = pad(data_bytes, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, decrData):
        """
        解密
        """
        cipher = self._get_cipher()  # 获取全新的对象

        try:
            # Base64 解码
            ciphertext = base64.b64decode(decrData.encode('utf-8'))

            # AES 解密
            padded_plaintext = cipher.decrypt(ciphertext)

            # 去填充
            plaintext = unpad(padded_plaintext, AES.block_size)

            # 转字符串
            return plaintext.decode('utf-8')
        except Exception as e:
            # 如果解密失败，通常是因为 Key 或 IV 不对
            raise ValueError(f"解密失败：密钥或IV不匹配。原始错误: {e}")


if __name__ == '__main__':
    # --- 自测环节 ---
    test_key = "mysecretkey12345"
    test_data = "huace_xm"

    print(f"测试密钥: {test_key}")
    print(f"测试数据: {test_data}")

    ens = EncryptData(test_key)

    # 1. 加密
    encrypted_str = ens.encrypt(test_data)
    print(f"加密结果: {encrypted_str}")

    # 2. 解密 (使用同一个实例)
    try:
        decrypted_str = ens.decrypt(encrypted_str)
        print(f"解密结果: {decrypted_str}")

        if decrypted_str == test_data:
            print("✅ 测试通过：加解密闭环成功！")
        else:
            print("❌ 测试失败：解密内容与原文不符")
    except Exception as e:
        print(f"❌ 测试报错: {e}")