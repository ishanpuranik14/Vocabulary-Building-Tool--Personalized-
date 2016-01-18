# To get data from WSJs rss feed
from bs4 import BeautifulSoup
import urllib, json
import re

def stripAllTags(html) :
    if html is None :
        return None
    return "".join(BeautifulSoup(html).findAll( text = True))

# DB connection
import MySQLdb
db = MySQLdb.connect("localhost","root","","cl-master")
cursor = db.cursor()
# Main program
# get provider and interest links from db
sql1 = "select * from interestsource;"
sql2 = "select url, pcode from providers where pid = "
sql3 = "select icode from interestmap where iid = "
cursor.execute(sql1)
dids = cursor.fetchall()
for row in dids :
    iid = row[0]
    pid = row[1]
    cursor.execute(sql2+str(pid)+";")
    providerData = cursor.fetchone()
    mainurl = providerData[0]
    pcode = providerData[1]
    extraurl = row[2]
    cursor.execute(sql3+str(iid))
    icode = cursor.fetchone()[0]
    for year in range(2014, 2015) :
        for month in range(5,6) :
            for date in range(28,29) :
                url = mainurl+extraurl+ str(year) + "/" + str(month) + "/" + str(date) + "/feed"
                page = urllib.urlopen(url)
                count = 1                                   # used in forming unique article id
                soup = BeautifulSoup(page.read(), 'xml')
                # find multiple news items and iterate over them
                items = soup.findAll('item')
                for item in items :
                    # extract data about item
                    link = item.link.text
                    title = json.dumps(item.title.text)
                    uid = pcode + icode + str(date) + str(month) + str(year) + str(count)
                    count+=1
                    pubDate = item.pubDate.text
                    creator = repr(item.find("category").previousSibling.previousSibling)
                    # now get all categories and put different data in appropriate tables
                    categories = item.findAll('category')
                    for category in categories :
                        artTag = category.text
                        # search if tag is already there if not get max-id,
                        # assign new tag id and add to the list. also add details to tag article table
                        # for each tag irrespective of whether it was already in tagmap or not
                        sql = "SELECT * FROM TAGMAP WHERE tname = '" + artTag + "';"
                        tid=1  # dummy value
                        try:
                            cursor.execute(sql)
                            testData = cursor.fetchall()
                            if len(testData) == 0 :
                                try :
                                    sql = "SELECT MAX(TID) FROM TAGMAP;"
                                    cursor.execute(sql)
                                    tid = cursor.fetchone()[0] + 1
                                    try:
                                        sql = "INSERT INTO TAGMAP VALUES("+str(tid)+",'"+artTag+"');"    #store new tid in tagmap
                                        cursor.execute(sql)
                                        db.commit()
                                    except:
                                        print "couldn't store in tagmap"
                                        db.rollback()
                                        print 1/0 #throwing exception
                                except :
                                    print "couldnt get max tid"
                                    print 1/0 #throwing exception
                            else:
                                tid = cursor.fetchone()[0]
                            try:
                                sql = "INSERT INTO TAGARTICLE VALUES("+str(tid)+","+ uid +","+str(iid)+");"
                                cursor.execute(sql)
                                db.commit()
                            except:
                                print "failed to store in tagarticle"
                                db.rollback()
                        except :
                            print "failed for category : "+ artTag
                        # Done with doing stuff on categories
                    # if there is no content, put it in another table. otherwise do what follows
                    if '<content:encoded>' not in repr(item) :
                        sql = 'INSERT INTO NOCONTENTFOUND VALUES("'+uid+'",' + str(iid) + ',"' + link + '","' + creator + '","' + title + '","' + pubDate + '");'
                        try :
                            cursor.execute(sql)
                            db.commit()
                        except :
                            print "uid : " + uid
                            print "url : " + link
                            print "title : " + title
                            print "Failed to store in NoContentFound, rolling back"
                            db.rollback()
                        continue
                    # else,grab the content - grab from CDATA
                    try:
                        sql = 'INSERT INTO ARTICLEMETA VALUES("'+uid+'","' + title + '","' + link + '","' + creator + '","' + pubDate + '");'
                        cursor.execute(sql)
                        db.commit()
                        sql = 'INSERT INTO ARTICLESINTERESTS VALUES("'+uid+'",' + str(iid) + ',' + str(pid) + ');'
                        cursor.execute(sql)
                        db.commit()
                    except :
                        print "couldnt store it to articleMeta or articlesinterests for : " + uid
                        db.rollback()
                    content = item.description.nextSibling.nextSibling
                    artContent = content.text
                    # Some may not have a content tag.for them content has to be scraped from source maybe?
                    # now strip not needed info and store as a list of sentences..
                    strippedSentenceList = re.split('[.?;!]', stripAllTags(artContent))
                    f = open('D:/articles/'+uid+'.txt','w')
                    try:
                        f.write(json.dumps(strippedSentenceList))
                    except:
                        print "Failed to write for : " + uid
                    f.close()
                    # Code for storing articles(list of sentences) ends here
                print count
cursor.close()
db.close()
