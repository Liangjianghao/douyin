#-*- coding=utf-8 -*-
from flask import Flask, request, render_template
import re
import requests
from lxml import html
import os
import sys
import json
from flask import jsonify 
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getRealUrl',methods=['GET'])
def getRealUr():
    mydata = json.loads(request.args.get('mykey'))
    baseUrl=mydata['baseUrl']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    pattern = re.compile(r'http.*')
    baseUrls = pattern.findall(baseUrl)
    if len(baseUrls)==0:
        returnData={'realUrl' : '地址有误，请检查格式'}
        return jsonify(result=returnData)
    print('url'+"---"+baseUrls[0])
    response=requests.get(baseUrls[0],headers=headers).content
    response=response.decode('utf-8')
    pattern = re.compile(r'(?<=uri":")\w{32}')
    realUrls = pattern.findall(response)
    print(realUrls)
    if len(realUrls)==0:
        returnData={'realUrl' : '解析失败，请稍后重试！'}
        return jsonify(result=returnData)
    realUrl='https://aweme.snssdk.com/aweme/v1/play/?video_id=%s'%realUrls[0]
    print(realUrl)
    returnData={'realUrl' : realUrl}
    return jsonify(result=returnData)


if __name__ == '__main__':
    app.run()