__author__ = 'Ishan Puranik'

from bs4 import BeautifulSoup
import urllib,json,re,MySQLdb
from os import listdir

def stripAllTags(html) :
    if html is None :
        return None
    return "".join(BeautifulSoup(html).findAll( text = True))

db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()

sql = "SELECT * FROM NOCONTENTFOUND;"
cursor.execute(sql)
articles = cursor.fetchall()
writeCount = count=0

mypath = "D:/articlesncf/"
onlyfiles = [f.strip(".txt") for f in listdir(mypath)]

for article in articles :
    pid=1               #right now
    uid = article[0]
    iid = article[1]
    if iid!=4 :
        continue
    link = article[2]
    creator = article[3]
    title = article[4]
    pubDate = article[5]
    try:
        sql = "INSERT INTO ARTICLEMETA VALUES('"+uid+"','" + title + "','" + link + "','" + creator + "','" + pubDate + "');"
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO ARTICLESINTERESTS VALUES('"+uid+"'," + str(iid) + "," + str(pid) + ");"
        cursor.execute(sql)
        db.commit()
        count+=1
        print uid
    except :
        print "couldnt store it to articleMeta or articlesinterests for : " + uid
        db.rollback()

    try :
        page = urllib.urlopen(link)
        soup = BeautifulSoup(page.read(), 'html')
        div = soup.find('div', 'post-content')
        try:
            paragraphs = div.findAll('p')
        except :
            print "div is NoneType for uid : " + uid
        content = "".join(paragraph.text for paragraph in paragraphs)
        sentenceList = re.split('[.?;!]', stripAllTags(content))
        f = open('D:/articlesncf/'+uid+'.txt','w')
        try:
            f.write(json.dumps(sentenceList))
            writeCount+=1
        except:
            print "Failed to write for : " + uid
        f.close()
    except :
        print "Couldn't store article for uid = " + uid
print count
print writeCount