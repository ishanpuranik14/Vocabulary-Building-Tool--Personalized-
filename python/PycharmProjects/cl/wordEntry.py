__author__ = 'Ishan Puranik'

from bs4 import BeautifulSoup

import MySQLdb
db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

f = open('sampleWordlist.html')
soup = BeautifulSoup(f)

tables = soup.findAll('table')
wordid = 1
tableno = 1
for table in tables :
    trs = table.findAll('tr')
    for tr in trs :
        word = tr.th.text
        sql = "INSERT INTO SATWORDMAP VALUES("+str(wordid)+", '"+word+"',"+str(tableno)+" );"
        try:
            cursor.execute(sql)
            db.commit()
        except :
            print "failed to store : "+word
            db.rollback()
        meanings = tr.td.text.split(';')
        mno = 1
        for meaning in meanings :
            sql = 'INSERT INTO WORDMEANINGS VALUES('+str(wordid)+','+str(mno)+',"'+meaning+'");'
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print "failed to store meaning: "+word
                db.rollback()
            mno+=1
        wordid+=1
    tableno+=1