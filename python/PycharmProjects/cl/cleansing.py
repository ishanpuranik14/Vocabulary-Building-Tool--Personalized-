__author__ = 'Ishan Puranik'

import MySQLdb
from os import listdir

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = "SELECT UID FROM ARTICLEMETA;"
cursor.execute(sql)
articles = cursor.fetchall()

print len(articles)

mypath = "D:/articlesncf/"
onlyfiles = [f.strip(".txt") for f in listdir(mypath)]

mypath1 = "D:/articles/"
onlyfiles1 = [f.strip(".txt") for f in listdir(mypath1)]

print str(len(onlyfiles1) + len(onlyfiles))
faulty = []
for article in articles :
    uid = article[0]
    if uid in onlyfiles :
        continue
    if uid in onlyfiles1 :
        continue
    faulty.append(uid)

print len(faulty)