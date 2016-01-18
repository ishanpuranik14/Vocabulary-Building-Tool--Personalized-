# To get data from WSJs rss feed
from bs4 import BeautifulSoup, CData
import urllib, json
## DB connection
import MySQLdb
db = MySQLdb.connect("localhost","root","","ishan")
cursor = db.cursor()
##Main program
for year in range(2014, 2015) :
    for month in range(5,6) :
        for date in range(28,29) :
            url = "http://blogs.wsj.com/personal-technology/" + str(year) + "/" + str(month) + "/" + str(date) + "/feed"
            page = urllib.urlopen(url)
            count = 1
            soup = BeautifulSoup(page.read(), 'xml')
            # find multiple news items and iterate over them
            items = soup.find_all('item')
            for item in items :
                #extract data about item
                link = item.link.text
                title = json.dumps(item.title.text)
                uid = "WSJ" + "PT" + str(date) + str(month) + str(year) + str(count)
                count+=1
                pubDate = item.pubDate.text #refine this
                creator = item.find("category").previousSibling.previousSibling #use .text
                #now get all categories and put different data in appropriate tables
                categories = item.findAll('category')
                #listCat = []
                for category in categories :
                    artTag = category.text
                    #do stuff after this - store

                    #Done with doing stuff on categories
                #if there is no content, put it in another table. otherwise do what follows
                if '<dc:content>' not in repr(item) :
                    sql = 'INSERT INTO NOCONTENTRSS VALUES("'+uid+'","' + "Personal tech" + '","' + link + '",' + title + ');'
                    try :
                        cursor.execute(sql)        
                        db.commit()
                    except:
                        print "uid : " + uid
                        print "url : " + link
                        print "title : " + title
                        print "Failed to store, rolling back"
                        db.rollback()
                    continue
                #else,grab the content - grab from CDATA
                content = item.description.nextSibling.nextSibling
                artContent = content.text       #Some may not have a content tag. for them content has to be scraped from source maybe?
                #now strip not needed info and store

                #Done with storing articles
'''
                sql = 'INSERT INTO LINKS VALUES("'+uid+'","'+oneUrl+'",'+title+');'
                try :
                    cursor.execute(sql)        
                    db.commit()
                except:
                    print "uid : " + uid
                    print "url : " + oneUrl
                    print "title : " + title
                    print "Failed to store, rolling back"
                    db.rollback()
'''
db.close()
