__author__ = 'Prof. Sonalde Desai'

import MySQLdb

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = "select uid, level from articlewordstats;"
cursor.execute(sql)
results = cursor.fetchall()

for result in results :
    uid = result[0]
    level = result[1]
    sql1 = "select count(distinct(wid)) from articlewordmeta where uid='"+uid+"' and level="+str(level)+";"
    cursor.execute(sql1)
    result1 = cursor.fetchone()
    sql2 = "update articlewordstats set nowordsleft="+str(result1[0])+" where uid='"+uid+"' and level="+str(level)+";"
    cursor.execute(sql2)