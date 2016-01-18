__author__ = 'Ishan Puranik'
import MySQLdb

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = " SELECT DISTINCT(UID) FROM ARTICLESENTENCEMETA;"
cursor.execute(sql)
dataSet3 = cursor.fetchall()

for uid in dataSet3 :
    sql = "SELECT DISTINCT(SENTENCE) FROM ARTICLESENTENCEMETA WHERE UID='" + uid[0] + "'"
    cursor.execute(sql)
    sentences = cursor.fetchall()
    for sentence in sentences :
        sql = "SELECT * FROM ARTICLESENTENCEMETA WHERE (UID='" + uid[0] + "' AND SENTENCE=" + str(sentence[0]) + ")"
        cursor.execute(sql)
        results = cursor.fetchall()
        levelList = [0,0,0,0,0,0,0,0,0,0]
        scoreList = [0,0,0,0,0,0,0,0,0,0]
        for result in results :
            levelList[result[2]-1] = result[3]
        for level in range(0,10) :
            if levelList[level] !=0 :
                scoreList[level]+= 10*levelList[level]
                for i in range(level+1, 10) :
                    scoreList[level]-= (i-level)*levelList[i]
                sql = "UPDATE ARTICLESENTENCEMETA SET SCORE=" + str(scoreList[level]) + " WHERE UID='" + uid[0] + "' AND SENTENCE=" + str(sentence[0]) + " AND LEVEL="+str(level+1)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    print "couldn't update articlesentencemeta for uid : " + uid[0] + " and sentence : " + str(sentence[0]) + " and level : " + str(level+1)
                    db.rollback()

