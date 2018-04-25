#-*- coding=utf-8 -*-

#!/usr/bin/python

import sqlite3
import importlib
import sys
importlib.reload(sys)

conn = sqlite3.connect('douyin.db')
c = conn.cursor()
print("Opened database successfully")

# cursorCount = c.execute("SELECT count(*) from douyin")
# total = cursorCount.fetchone()
# print('共解析%s条数据'%total[0])
wrongCursor = c.execute("SELECT * from douyin where ID=0")
wrongData = wrongCursor.fetchall()
print(len(wrongData))

allCursor = c.execute("SELECT * from douyin")
allData=allCursor.fetchall()
for x in wrongData:
	print (x[1])
	print (x[2])
print('共解析%s条数据,解析失败%s条数据'%(len(allData),len(wrongData)))
conn.close()