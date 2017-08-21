#!/usr/bin/env python
# coding=utf-8
import os
import getopt
import sys
import binascii
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import tqdm


class Encryptiong():  # 功能主类
    def __init__(self, generate=None, public=None, filepath=None, decrypt=None, private=None, generateNum=None):
        self.generate = generate
        self.filepath = filepath
        self.decrypt = decrypt
        self.private = private
        self.public = public
        if generateNum:
            self.generateNum = int(generateNum)
        else:
            self.generateNum = 1024

    def encryp(self):  # 生成公钥、私钥文件
        random_generator = Random.new().read  # 伪随机数生成器
        rsa = RSA.generate(self.generateNum, random_generator)  # rsa算法生成
        private_pem = rsa.exportKey()  # 私钥生成
        with open('private.pem', 'w') as f:  # 生成私钥文件
            f.write(private_pem)
        public_pem = rsa.publickey().exportKey()  # 公钥生成
        with open('public.pem', 'w') as f:   # 生成公钥文件
            f.write(public_pem)

    def encryption(self):  # 加密功能
        res = []
        if self.generateNum == 1024:
            length = 100  # 1024bit每次加密的长度
        elif self.generateNum == 2048:
            length = 200  # 2048bit每次加密的长度
        else:
            length = 100
        with open(self.public) as f:  # 读取公钥文件
            key = f.read()
        rsakey = RSA.importKey(key)  # 加载公钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        if self.filepath[-1] == "\\":  # Windows
            result = self.getinfo(self.filepath)  # 获取加密目录下所有文件信息
            while True:
                try:
                    file_name, name, cipher_text = result.next()
                    for i in tqdm.tqdm(range(0, len(cipher_text), length), desc=name.decode('gbk') + " is being encrypted:"):
                        res.append(cipher.encrypt(binascii.b2a_hex(cipher_text)[i:i+length]))
                    with open(file_name, 'wb') as f:
                        f.write("".join(res))
                        res = []
                except StopIteration:
                    break
        elif self.filepath[-1] == "/":  # Linux
            result = self.getinfo(self.filepath)  # 获取加密目录下所有文件信息
            while True:
                try:
                    file_name, name, cipher_text = result.next()
                    for i in tqdm.tqdm(range(0, len(cipher_text), length),
                                       desc=name.decode('gbk') + " is being encrypted:"):
                        res.append(cipher.encrypt(binascii.b2a_hex(cipher_text)[i:i + length]))
                    with open(file_name, 'wb') as f:
                        f.write("".join(res))
                        res = []
                except StopIteration:
                    break
        else:
            name = self.filepath.split("\\")[-1]
            file_name = self.filepath
            with open(file_name, 'rb') as f:
                cipher_text = f.read()
            for i in tqdm.tqdm(range(0, len(cipher_text), length), desc=name.decode('gbk') + " is being encrypted:"):
                res.append(cipher.encrypt(binascii.b2a_hex(cipher_text)[i:i+length]))
            with open(file_name, 'wb') as f:
                f.write("".join(res))

    def decrypted(self):  # 解密功能
        res = []
        if self.generateNum == 1024:
            length = 128  # 1024bit每次解密的长度
        elif self.generateNum == 2048:
            length = 256  # 2048bit每次解密的长度
        else:
            length = 100
        with open(self.private) as f:  # 读取私钥文件
            key = f.read()
        rsakey = RSA.importKey(key)  # 加载私钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read  # 伪随机数生成器
        if self.decrypt[-1] == "\\":  # Windows
            result = self.getinfo(self.decrypt)  # 获取解密目录下所有文件信息
            while True:
                try:
                    file_name, name, cipher_text = result.next()
                    for i in tqdm.tqdm(range(0, len(cipher_text), length), desc=name.decode('gbk') + " is being decrypted:"):
                            res.append(cipher.decrypt(cipher_text[i:i+length], random_generator))
                    with open(file_name, 'wb') as f:
                        f.write(binascii.a2b_hex("".join(res)))
                        res = []
                except StopIteration:
                    break
        elif self.decrypt[-1] == "/":  # Linux
            result = self.getinfo(self.decrypt)  # 获取解密目录下所有文件信息
            while True:
                try:
                    file_name, name, cipher_text = result.next()
                    for i in tqdm.tqdm(range(0, len(cipher_text), length),
                                       desc=name.decode('gbk') + " is being decrypted:"):
                        res.append(cipher.decrypt(cipher_text[i:i + length], random_generator))
                    with open(file_name, 'wb') as f:
                        f.write(binascii.a2b_hex("".join(res)))
                        res = []
                except StopIteration:
                    break
        else:
            name = self.decrypt.split("\\")[-1]
            file_name = self.decrypt
            with open(file_name, 'rb') as f:
                cipher_text = f.read()
            for i in tqdm.tqdm(range(0, len(cipher_text), length), desc=name.decode('gbk') + " is being decrypted:"):
                res.append(cipher.decrypt(cipher_text[i:i+length], random_generator))
            with open(file_name, 'wb') as f:
                f.write(binascii.a2b_hex("".join(res)))

    def getinfo(self, filepath):  # 获取文件夹所有文件信息
        get_file_list = []
        for root, dirs, files in os.walk(filepath):
            for name in files:
                get_file_list.append(os.path.join(root, name))
                with open(os.path.join(root, name), 'rb') as f:
                    yield [os.path.join(root, name), name, f.read()]


def main():
    print """
     _        _   _      _  _    __    _  __________  _           _
    | |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
    | |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
    |  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
    | |      | |    \  /   | |_| || |_| || |         | |         | |
    | |      | |    |  |    \   /  \   / | |________ | |________ | |________
    |_|      |_|    |__|     \_/    \_/  |__________||__________||__________|

        """
    try:
        encryptor = None  # 生成公、秘钥的开关
        generate = False  # 加密功能的开关
        decrypt = False  # 解密功能的开关
        keyfile = None  # 公钥或密钥文件路径
        file = None  # 加密或解密文件目录
        opts, args = getopt.getopt(sys.argv[1:], "-h-e-g-d-k:-f:",
                                   ["help", "encryptor", "generate", "decrypt", "keyfile=", "file="])
        for opt_name, opt_value in opts:
            if opt_name in ('-h', '--help'):
                print "python encrypto.py -k=D:\\private.pem(private path)"
                exit()
            if opt_name in ('-e', '--encryptor'):
                encryptor = True
            if opt_name in ('-g', '--generate'):
                generate = True
            if opt_name in ('-d', '--decrypt'):
                decrypt = True
            if opt_name in ('-k', '--keyfile'):
                keyfile = opt_value[1:]
            if opt_name in ('-f', '--file'):
                file = opt_value[1:]
        if encryptor:  # 调用生成公、密钥功能
            Encryptiong(generate=True).encryp()
        elif generate:  # 调用加密功能
            if file and keyfile:
                Encryptiong(public=keyfile, filepath=file).encryption()
            elif file is None:
                print 'Place input encrypto file path!'
                print 'Example:python Encryptiong.py -g -f=D:\\encryptoFilePath\\ -k=D:\\public.pem'
                exit()
            elif keyfile is None:
                print 'Place input public file path!'
                print 'Example:python Encryptiong.py -g -f=D:\\encryptoFilePath\\ -k=D:\\public.pem'
                exit()
        elif decrypt:  # 调用解密功能
            if keyfile and file:
                Encryptiong(decrypt=file, private=keyfile).decrypted()
            elif file is None:
                print 'Place input decrypt file path!'
                print 'Example:python Encryptiong.py -d -r=D:\\decryptedFilPath\\ -k=D:\\private.pem'
                exit()
            elif keyfile is None:
                print 'Place input private file path!'
                print 'Example:python Encryptiong.py -d -r=D:\\decryptedFilePath\\ -k=D:\\private.pem'
                exit()
        else:
            print 'Example1:python Encryptiong.py -e'
            print 'Example2:python Encryptiong.py -g -f=D:\\encryptoFilePath\\ -k=D:\\public.pem'
            print 'Example3:python Encryptiong.py -d -f=D:\\decryptedFilePath\\ -k=D:\\private.pem'

    except getopt.GetoptError:
        print 'Example1:python Encryptiong.py -e'
        print 'Example2:python Encryptiong.py -g -f=D:\\encryptoFilePath\\ -k=D:\\public.pem'
        print 'Example3:python Encryptiong.py -d -f=D:\\decryptedFilePath\\ -k=D:\\private.pem'

if __name__ == '__main__':
    main()
