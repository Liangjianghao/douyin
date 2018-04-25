#-*- coding=utf-8 -*-
import sqlite3

conn = sqlite3.connect('douyin.db')
c = conn.cursor()
c.execute('''CREATE TABLE douyin
       (ID               INT      NOT NULL,
       baseUrl           TEXT    NOT NULL,
       result            TEXT     NOT NULL,
       realUrl        TEXT,
       title         TEXT,
       imgUrl         TEXT,
       videoNumber     INT );''')
conn.commit()
conn.close()