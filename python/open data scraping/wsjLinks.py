from bs4 import BeautifulSoup
import urllib, json
## DB connection
import MySQLdb
db = MySQLdb.connect("localhost","root","","ishan")
cursor = db.cursor()
##Main program

url = "http://blogs.wsj.com/personal-technology/2014/05/28/"
page = urllib.urlopen(url)
count=1
soup = BeautifulSoup(page.read(), 'xml')

articleLinks = soup.find_all('h2', class_= "post-title h-main2")
for articleLink in articleLinks :
    link = articleLink.a
    #extract link and article name
    oneUrl = link['href']
    title = json.dumps(link.text)
    uid = "PT280514" + str(count)
    count = count+1
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

db.close()
