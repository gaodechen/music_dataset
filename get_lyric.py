#! /usr/bin/python
# coding='utf-8'
import requests
import math
import random
# pycrypto
from Crypto.Cipher import AES
import codecs
import base64
import csv

# 生成16个随机字符
def generate_random_strs(length):
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 控制次数参数i
    i = 0
    # 初始化随机字符串
    random_strs = ""
    while i < length:
        e = random.random() * len(string)
        # 向下取整
        e = math.floor(e)
        random_strs = random_strs + list(string)[e]
        i = i + 1
    return random_strs


# AES加密
def AESencrypt(msg, key):
    # 如果不是16的倍数则进行填充(paddiing)
    padding = 16 - len(msg) % 16
    # 这里使用padding对应的单字符进行填充
    msg = msg + (padding * chr(padding))
    # 用来加密或者解密的初始向量(必须是16位)
    iv = b'0102030405060708'
    key = key.encode('utf-8')
    msg = msg.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 加密后得到的是bytes类型的数据
    encryptedbytes = cipher.encrypt(msg)
    # 使用Base64进行编码,返回byte字符串
    encodestrs = base64.b64encode(encryptedbytes)
    # 对byte字符串按utf-8进行解码
    enctext = encodestrs.decode('utf-8')

    return enctext


# RSA加密
def RSAencrypt(randomstrs, key, f):
    # 随机字符串逆序排列
    string = randomstrs[::-1]
    # 将随机字符串转换成byte类型数据
    text = bytes(string, 'utf-8')
    seckey = int(codecs.encode(text, encoding='hex'),
                 16)**int(key, 16) % int(f, 16)
    return format(seckey, 'x').zfill(256)


# 获取参数
def get_params(songid):
    # id为歌曲的id号,后面的lv和tv都是固定值
    msg = '{id: ' + str(songid) + ', lv: -1, tv: -1}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)

    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey

'''
def write_to_csv(items, artist_name):

    with open("music163_songs.csv", "a", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        for item in items:
            writer.writerow([item.a['href'].replace('/song?id=', ''), item.b['title']])
    csvfile.close()
'''

def read_csv():

    with open("music163_songs.csv", "r", encoding='utf-8') as csvfile:

        reader = csv.reader(csvfile)
        for row in reader:
            songid, songname = row
            if str() is "artist_id":
                continue
            else:
                yield songid, songname

def main():
    for readcsv in read_csv():
        songid, songname = readcsv
        params, encSecKey = get_params(songid)
        data = {'params': params, 'encSecKey': encSecKey}
        url = 'https://music.163.com/weapi/song/lyric?csrf_token='
        r = requests.post(url, data=data)
        print(r.status_code)
        print(r.json())


if __name__ == "__main__":
    main()
