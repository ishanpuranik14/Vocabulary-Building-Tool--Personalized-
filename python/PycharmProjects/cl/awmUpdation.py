__author__ = 'Ishan Puranik'
import MySQLdb

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = "SELECT WID, LEVEL FROM SATWORDMAP"
cursor.execute(sql)
wordLevels = cursor.fetchall()
wlDict = {}

for wl in wordLevels :
    wlDict[wl[0]] = wl[1]

aiDict = {}
sql = "SELECT UID, IID FROM ARTICLESINTERESTS"
cursor.execute(sql)
articleInterests = cursor.fetchall()

for ai in articleInterests :
    aiDict[ai[0]] = ai[1]

sql = "SELECT UID, WID, SENTENCE FROM ARTICLEWORDMETA"
cursor.execute(sql)
uidWids = cursor.fetchall()
for uw in uidWids :
    iid = aiDict[uw[0]]
    level = wlDict[uw[1]]
    sql = "UPDATE ARTICLEWORDMETA SET IID="+str(iid)+", LEVEL="+str(level)+" WHERE UID='"+uw[0]+"' AND WID="+str(uw[1])+" AND SENTENCE="+str(uw[2])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print "couldn't update articlewordmeta for uid : " + uw[0] + " and sentence : " + str(uw[2]) + " and wid : " + str(uw[1])
        db.rollback()