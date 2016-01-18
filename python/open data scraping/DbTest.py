import MySQLdb

db = MySQLdb.connect("localhost","root","","ishan")

cursor = db.cursor()

sql = """CREATE TABLE LINKS(
         ID VARCHAR(20),
         URL VARCHAR(300),
         NAME VARCHAR(1000));"""

try :
    cursor.execute(sql)
    db.commit()
    
except :
    db.rollback()

db.close()
