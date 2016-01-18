__author__ = 'Ishan Puranik'

import MySQLdb
import json

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = "SELECT * FROM ARTICLESINTERESTS;"
cursor.execute(sql)
articles = cursor.fetchall()    # Fetching all articles

sql = "SELECT * FROM SATWORDMAP;"
cursor.execute(sql)
words = cursor.fetchall()       # Getting all words ( with wid and levels) in a list
wordList=[]
levelList = []
widList = []
widDict = dict()
widLevelDict = dict()
for word in words :
    wordList.append(word[1].lower())
    levelList.append(word[2])
    widList.append(word[0])
    widLevelDict[word[0]] = word[2]

widInterest = dict()
for article in articles :
    uid = article[0]
    iid = article[1]        # put this in a dictionary maybe?
    widInterest[uid] = iid
    f = open('D:/articles/'+uid+'.txt','r')
    sentences = f.read()
    sentenceList = json.loads(sentences)
    sentenceno=1
    wordsDone = []          # words that are included in wordstats for this already
    for sentence in sentenceList :
        sentence = sentence.lower()
        for word,level,wid in zip(wordList, levelList, widList):
            if word in sentence :
                sql="SELECT * FROM ARTICLEWORDSTATS WHERE UID='"+ uid +"' AND LEVEL="+str(level)
                cursor.execute(sql)
                resultData = cursor.fetchall()
                if len(resultData) == 0:
                    sql = "INSERT INTO ARTICLEWORDSTATS VALUES('"+uid+"',"+str(level)+",1,0,0);"
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except :
                        print " failed to store in articlewordstats for word + " + word + "in uid : " + uid
                        db.rollback()
                else :
                    wordCount = 0
                    if wid not in wordsDone :
                        for data in resultData:
                            wordCount = data[2] + 1
                        sql = "UPDATE ARTICLEWORDSTATS SET NOWORDSLEFT="+str(wordCount)+" WHERE UID='"+ uid +"' AND LEVEL="+str(level)
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except :
                            print " failed to update in articlewordstats for  word : " + word + ", wid: "+str(wid)+" and uid : " + uid
                            db.rollback()

                if wid not in wordsDone :
                    wordsDone.append(wid)

                sql2 = "INSERT INTO ARTICLEWORDMETA VALUES('"+uid+"',"+str(wid)+","+str(sentenceno)+", 0);"
                try:
                    cursor.execute(sql2)
                    db.commit()
                except :
                    print " failed to store in articlewordmeta for  word + " + word + "in uid : " + uid
                    db.rollback()

                sql4 = "SELECT WORDSLEFT FROM ARTICLESENTENCEMETA WHERE UID='"+uid+"' AND SENTENCE="+str(sentenceno)+" AND LEVEL="+str(level)
                cursor.execute(sql4)
                results = cursor.fetchall()
                if len(results) == 0 :
                    sql4 = "INSERT INTO ARTICLESENTENCEMETA VALUES('"+uid+"',"+str(sentenceno)+","+str(level)+",1,0,0);"
                    try:
                        cursor.execute(sql4)
                        db.commit()
                    except :
                        print " failed to store in articlesentencemeta for  word + " + word + "in uid : " + uid
                        db.rollback()
                else :
                    wordsLeft=0
                    for result in results :
                        wordsLeft=result[0]+1
                    sql4  = "UPDATE ARTICLESENTENCEMETA SET WORDSLEFT="+str(wordsLeft)+" WHERE UID='"+uid+"' AND SENTENCE="+str(sentenceno)+" AND LEVEL="+str(level)
                    try:
                        cursor.execute(sql4)
                        db.commit()
                    except :
                        print " failed to update in articlesentencemeta for  word + " + word + "in uid : " + uid
                        db.rollback()
        sentenceno+=1
    for wid in wordsDone :
        if wid not in widDict.keys() :
            widDict[wid] = [0,0,0,0,0,0,0]
            widDict[wid][iid-1] = 1
        else :
            widDict[wid][iid-1]+=1

for wid in widDict.keys() :
    for iid in range(1,8) :
        sql = "INSERT INTO WORDSTATS VALUES("+str(wid)+","+str(widDict[wid][iid-1])+","+str(iid)+");"
        try:
            cursor.execute(sql)
            db.commit()
        except :
            print " failed to store in wordstats for wid : " + str(wid)
            db.rollback()

sql = "SELECT * FROM ARTICLEWORDMETA"
cursor.execute(sql)
resultData = cursor.fetchall()
wordsDone={1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
articlesDone = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[]}
tempTable = {1:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],2:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],3:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],4:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],5:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],6:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],7:[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]}
for result in resultData :
    uid = result[0]
    wid = result[1]
    level = widLevelDict[wid]
    iid = widInterest[uid]
    if uid not in articlesDone[level] and wid not in wordsDone[iid] :
        tempTable[iid][level-1][0]+=1
        tempTable[iid][level-1][1]+=1
        wordsDone[iid].append(wid)
        articlesDone[level].append(uid)
    elif uid in articlesDone[level] and wid not in wordsDone[iid]:
        tempTable[iid][level-1][0]+=1
        wordsDone[iid].append(wid)
    elif uid not in articlesDone[level] and wid in wordsDone[iid] :
        tempTable[iid][level-1][1]+=1
        articlesDone[level].append(uid)
    else :
        pass

for iid in tempTable.keys() :
    for level in range(1,11) :
        sql = "INSERT INTO INTERESTSTATS VALUES("+str(iid)+","+str(level)+","+str(tempTable[iid][level-1][0])+","+str(tempTable[iid][level-1][1])+");"
        try:
            cursor.execute(sql)
            db.commit()
        except :
            print " failed to store in intereststats for interest : " + str(iid) + " and level : " + str(level)
            db.rollback()

cursor.close()
db.close()