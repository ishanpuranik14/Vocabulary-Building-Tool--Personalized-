__author__ = 'Ishan Puranik'
import MySQLdb

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql ="SELECT * FROM ARTICLEWORDSTATS"
cursor.execute(sql)
rows=cursor.fetchall()
'''
for row in rows :
    uid = row[0]
    level = row[1]
    nowords = row[2]
    sql = "SELECT WID, SENTENCE FROM ARTICLEWORDMETA WHERE UID='"+uid+"' AND LEVEL="+str(level)
    cursor.execute(sql)
    wordSentences = cursor.fetchall()
    if len(wordSentences) == 0 :
        continue
    elif len(wordSentences) == 1 :
        score = 0
        for ws in wordSentences :
            sql = "SELECT SCORE FROM ARTICLESENTENCEMETA WHERE UID='"+uid+"' AND SENTENCE="+str(ws[1])
            cursor.execute(sql)
            wss = cursor.fetchone()
            score+=wss[0]
            sql = "SELECT SCORE FROM ARTICLESENTENCEMETA WHERE UID='"+uid+"' AND SENTENCE="+str(ws[1]-1)+" AND LEVEL="+str(level)
            cursor.execute(sql)
            wss = cursor.fetchone()
            try :
                score+=(wss[0]/2)
            except:
                pass
            sql = "SELECT SCORE FROM ARTICLESENTENCEMETA WHERE UID='"+uid+"' AND SENTENCE="+str(ws[1]+1)+" AND LEVEL="+str(level)
            cursor.execute(sql)
            wss = cursor.fetchone()
            try:
                score+=(wss[0]/2)
            except:
                pass
    else:
        score = 0
        for ws in wordSentences :
            sql = "SELECT SCORE FROM ARTICLESENTENCEMETA WHERE UID='"+uid+"' AND SENTENCE="+str(ws[1])
            cursor.execute(sql)
            wss = cursor.fetchone()
            score+=wss[0]
    sql = "UPDATE ARTICLEWORDSTATS SET SCORE="+str(score)+" WHERE UID='"+uid+"' AND LEVEL="+str(level)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print "couldn't update articlewordstats for uid : " + uid[0] + " and level : " + str(level)
        db.rollback()

print "First step done"
'''
sql ="SELECT DISTINCT(UID) FROM ARTICLEWORDSTATS"
cursor.execute(sql)
rows=cursor.fetchall()
for row in rows :
    uid=row[0]
    levelList = [0,0,0,0,0,0,0,0,0,0]
    scoreList = [0,0,0,0,0,0,0,0,0,0]
    sql = "SELECT LEVEL, NOWORDSLEFT FROM ARTICLEWORDSTATS WHERE UID='"+uid+"'"
    cursor.execute(sql)
    levelWords = cursor.fetchall()
    for lw in levelWords :
        levelList[lw[0]-1]=int(lw[1])
    for level in range(0,10) :
        if levelList[level] !=0 :
            scoreList[level]+= 10*levelList[level]
            for i in range(level+1, 10) :
                scoreList[level]-= (i-level)*levelList[i]
            sql = "INSERT INTO ARTICLEBIRDSEYE VALUES('"+uid+"',"+str(level+1)+","+str(scoreList[level])+");"
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print "couldn't insert into articlebirdseye for uid : " + uid + " and level : " + str(level+1)
                db.rollback()

print "second step done"

sql = "SELECT * FROM ARTICLEWORDSTATS"
cursor.execute(sql)
aws = cursor.fetchall()

probability = 0.3       # of reading the article, can be variable

for al in aws :
    uid=al[0]
    level=al[1]
    score = al[4]
    sql = "SELECT SCORE FROM ARTICLEBIRDSEYE WHERE UID='"+uid+"' AND LEVEL="+str(level)
    cursor.execute(sql)
    scoreList = cursor.fetchone()
    beScore=0
    try:
        beScore = scoreList[0]
    except :
        print "None type for uid : "+uid+" and level : "+str(level)
    fscore = score + probability*beScore
    sql = "UPDATE ARTICLEWORDSTATS SET FSCORE="+str(fscore)+" WHERE UID='"+uid+"' AND LEVEL="+str(level)
    try:
        cursor.execute(sql)
        db.commit()
    except :
        print "failed to update articlewordstats where uid : "+uid+" and level : "+str(level)
        db.rollback()

print "third step done"