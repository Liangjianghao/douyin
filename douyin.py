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
import sqlite3
import datetime

importlib.reload(sys)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getRealUrl',methods=['GET'])
def getRealUr():
    conn = sqlite3.connect('douyin.db')
    c = conn.cursor()
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydata = json.loads(request.args.get('mykey'))
    baseUrl=mydata['baseUrl']
    try:
        if len(baseUrl)==0:
            returnData={'realUrl' : '地址有误，请检查格式','title':'逗我？网址呢！'}
            return jsonify(result=returnData)
        # print (baseUrl)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
        pattern = re.compile(r'http.*')
        baseUrls = pattern.findall(baseUrl)
        # print (len(baseUrls))
        if len(baseUrls)==0:
            returnData={'realUrl' : '地址有误，请检查格式','title':'地址有误，请检查格式'}
            c.execute("INSERT INTO douyin (ID,baseUrl,result,realUrl,title,imgUrl,nowtime) VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s' )"%('0',baseUrl,'初始地址错误','0','0','0',nowTime));
            conn.commit()
            conn.close()
            return jsonify(result=returnData)
        print('url'+"---"+baseUrls[0])

        response=requests.get(baseUrls[0],headers=headers).content
        response=response.decode('utf-8')
        pattern = re.compile(r'(?<=uri":")\w{32}')
        realUrls = pattern.findall(response)
        # print(realUrls)
        # print('des')
        descpattern=re.compile(r'(?<=class="desc">).+?(?=</p>)')
        desc = descpattern.findall(response)
        if len(desc)==0:
            description='无标题'
        else:
            description=desc[0]
        coverpattern=re.compile(r'(?<="uri":"large\\/).+?(?="})')
        cover=coverpattern.findall(response)

        coverUrl='https://pb3.pstatp.com/large/%s.jpg'%cover[0]
        if len(realUrls)==0:
            returnData={'realUrl' : '解析失败，请稍后重试！','title':'解析失败，请稍后重试！'}
            c.execute("INSERT INTO douyin (ID,baseUrl,result,realUrl,title,imgUrl,nowtime) VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s' )"%(realUrls[0],baseUrls[0],'解析失败','0','0','0',nowTime));
            conn.commit()
            conn.close()
            return jsonify(result=returnData)
        if 'tiktokv' in baseUrls[0]:
            realUrl='http://api.tiktokv.com/aweme/v1/play/?video_id=%s'%realUrls[0]
        else:
            realUrl='https://aweme.snssdk.com/aweme/v1/play/?video_id=%s'%realUrls[0]

        returnData={'realUrl' : realUrl,'coverUrl':coverUrl,'title':description}
        c.execute("INSERT INTO douyin (ID,baseUrl,result,realUrl,title,imgUrl,nowtime) VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s')"%(realUrls[0],baseUrls[0],'解析成功',realUrl,description,coverUrl,nowTime));
        conn.commit()
        conn.close()
        return jsonify(result=returnData)
    except Exception as e:
        print(e)  
        c.execute("INSERT INTO douyin (ID,baseUrl,result,realUrl,title,imgUrl,nowtime) VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s' )"%('0',baseUrl,'出现异常%s'%e,'0','0','0',nowTime));
        conn.commit()
        conn.close()
    else:
        print('解析成功')

if __name__ == '__main__':

    app.run()
    # getRealUr()