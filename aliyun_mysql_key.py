#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib
import urllib2
import base64
import hmac
import urllib
import time
import uuid
import random
from hashlib import sha1
import datetime
import sys
import os

dbinstanceid="junjie"
Format='json'
Version=str("2014-08-15")
SignatureMethod="HMAC-SHA1" #签名方式
SignatureVersion=str("1.0")
AccessKeyId="123456" #阿里云颁发给用户的访问服务所用的密钥ID
AccessKeySecret="789789"
PageSize=str(100) #每页记录数
pagenum=1

#url中所需参数
#SignatureNonce 阿里云要求每次请求api中此值不一致，本文用如下方法生成
SignatureNonce=str(uuid.uuid1())
PageNumber=str(pagenum) #定义返回第几页
now_time = datetime.datetime.now()
yesterday = now_time + datetime.timedelta(minutes= -485)
StartTime=yesterday.strftime("%Y-%m-%dT%H:%MZ")
EndTime=now_time.strftime("%Y-%m-%dT%H:%MZ")
SignatureNonce=str(uuid.uuid1())
Timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
parameters = {
        "Action": "DescribeSlowLogRecords",
        "DBInstanceId": dbinstanceid ,
        "StartTime": StartTime ,
        "EndTime": EndTime ,
        "PageSize":PageSize,
        "PageNumber":PageNumber,
        "Format": Format ,
        "Version": Version,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureNonce": SignatureNonce ,
        "SignatureVersion": "1.0" ,
        "AccessKeyId": AccessKeyId ,
        "Timestamp": Timestamp
    }

    #处理参数
def url_connect(parameters):
    #sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for k in parameters.keys():
        canonicalizedQueryString += '&' + k + '=' + parameters[k]
    return canonicalizedQueryString[1:]
def sign(accessKeySecret, parameters):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
    h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    signature = percent_encode(signature)
    return signature
'''转码'''
def percent_encode(encodeStr):
    encodeStr = str(encodeStr)
    res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    res = res.replace('=', '%3D')
    res = res.replace('/', '%2F')
    return res

if __name__ == "__main__":
    #生成签名字符串
    Signature = sign(AccessKeySecret, parameters)
    #将签名字符串放入url连接中，url_connect有问题请自己构造url，后面加上Signature
    url_parameter=url_connect(parameters)
    url="https://rds.aliyuncs.com/?"+url_parameter+"&Signature="+Signature 
    print(url)



