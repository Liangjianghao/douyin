#-*- coding=utf-8 -*-
import sqlite3
import datetime

# 抖音去水印数据库
# conn = sqlite3.connect('douyin.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE douyin
#        (ID               INT      NOT NULL,
#        baseUrl           TEXT    NOT NULL,
#        result            TEXT     NOT NULL,
#        realUrl        TEXT,
#        title         TEXT,
#        imgUrl         TEXT,
#        nowtime     TEXT );''')
# conn.commit()
# conn.close()
# 抖音批量去水印用户数据库
def creatDouyinTable():
    conn = sqlite3.connect('User.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE douyinPL
           (jiqima            TEXT      NOT NULL,
           useTime           TEXT    NOT NULL,
           status            TEXT );''')
    conn.commit()
    conn.close()
creatDouyinTable()

def selectUseTime(jiqima):
    conn = sqlite3.connect('User.db')
    c = conn.cursor()
    selectJiqima = c.execute("SELECT * from douyinPL where jiqima=%s"%jiqima)
    selectJiqimaData = selectJiqima.fetchall()
    print(len(selectJiqimaData))
    tomorrowTime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')#明天
    if len(selectJiqimaData)==0:
        print('插入一天试用期')
        insertStr="INSERT INTO douyinPL (jiqima,useTime,status) VALUES ('%s', '%s','试用')"%(jiqima,tomorrowTime)
        print(insertStr)
        insertTime=c.execute("INSERT INTO douyinPL (jiqima,useTime,status) VALUES ('%s', '%s','试用')"%(jiqima,tomorrowTime))
        conn.commit()
        conn.close()
        return tomorrowTime
    else:
        print('取得时间')
        # print(selectJiqimaData[0])
        conn.close()
        return selectJiqimaData[0][1]
# print selectUseTime('234')

