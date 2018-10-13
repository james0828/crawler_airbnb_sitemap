import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import html.parser
from fake_useragent import UserAgent
import pymysql

def get_html(url):
    ua =  UserAgent()
    req = Request(url, headers={'User-Agent': ua.random})
    page = urlopen(req)
    html = page.read()
    return html

def get_cities(num, url, cursor):
    city_str = "INSERT INTO CITIES(ID, COUNTRY_ID, CITY_NAME) VALUES (%s, %s, %s)"
    count = 1
    while True:
        obj = url + "?page=" + str(count)
        print(obj)
        html = get_html(obj)
        html = html.decode('UTF-8')

        soup = BeautifulSoup(html, 'html.parser')

        data = soup.select(' .col-sm-4 > .list-unstyled > li > a')
        for i in data:
            global city_num
            city_num += 1
            cursor.execute(city_str, (city_num, num, i.string))
            print(i.string)

        inspect = soup.find(attrs={'rel','next'})
        
        if inspect == None:
            break

        count = count + 1

url = "https://www.airbnb.com.tw"
html = get_html(url + "/sitemaps")
html = html.decode('UTF-8')

soup = BeautifulSoup(html, 'html.parser')

#connect to db 
#set your db info
db = pymysql.connect("localhost","root","123456","test_db" )

cursor = db.cursor()

#create table in db
cursor.execute("DROP TABLE IF EXISTS COUNTRIES")
cursor.execute("DROP TABLE IF EXISTS CITIES")
sql = """CREATE TABLE COUNTRIES (
        ID CHAR(10) NOT NULL,
        COUNTRY_NAME CHAR(50) NOT NULL
        )"""

cursor.execute(sql)

sql = """CREATE TABLE CITIES (
        ID CHAR(10) NOT NULL,
        COUNTRY_ID CHAR(10) NOT NULL,
        CITY_NAME CHAR(100) NOT NULL
        )"""

cursor.execute(sql)
# ----------------------

db_str = "INSERT INTO COUNTRIES(ID, COUNTRY_NAME) VALUES (%s, %s)"

global city_num
city_num = 0
# get all country 
data = soup.select(' .list-unstyled > li > a')

# save in db
for num,i in enumerate(data):
    cursor.execute(db_str, (num, i.string))
    get_cities(num, url + i.get('href').lower(), cursor)
    db.commit()

