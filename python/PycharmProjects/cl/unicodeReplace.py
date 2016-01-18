__author__ = 'Ishan Puranik'

import MySQLdb

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = "SELECT * FROM ARTICLESINTERESTS;"
cursor.execute(sql)
articles = cursor.fetchall()    # Fetching all articles

for article in articles :
    uid = article[0]
    f = open('D:/articles/'+uid+'.txt','r')
