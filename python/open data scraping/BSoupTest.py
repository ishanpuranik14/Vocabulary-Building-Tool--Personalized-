from bs4 import BeautifulSoup
import urllib

url = "http://www.utexas.edu/world/univ/alpha/"
page = urllib.urlopen(url)

soup = BeautifulSoup(page.read())

universities = soup.find_all('a',class_='institution')

lis = soup.find_all('li')

for li in lis :
    a = li.find('a')
    string = ""
    try :
        string = a['href'] + "," + str(a.text) + "," + str(li.text)
    except :
        print "NA"
    print string

'''for university in universities :
    print university['href']+","+university.string
'''
