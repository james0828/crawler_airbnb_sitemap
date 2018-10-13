import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import html.parser
import csv
from fake_useragent import UserAgent

def get_html(url):
    ua =  UserAgent()
    req = Request(url, headers={'User-Agent': ua.random})
    page = urlopen(req)
    html = page.read()
    return html

def get_cities(num, url):
    count = 1
    while True:
        obj = url + "?page=" + str(count)
        html = get_html(obj)
        html = html.decode('UTF-8')

        soup = BeautifulSoup(html, 'html.parser')

        data = soup.select(' .col-sm-4 > .list-unstyled > li > a')

        with open('citys.csv', 'a') as w:
            writer = csv.writer(w)
            rows = ['id', 'country_id', 'city_name']
            writer.writerow(rows)
            for i in data:
                global city_num
                city_num += 1
                cities = [city_num, num, i.string]
                writer.writerow(cities)
                print(i.string)

        inspect = soup.find(attrs={'rel','next'})

        if inspect == None:
            break

        count = count + 1

url = "https://www.airbnb.com.tw"
html = get_html(url + "/sitemaps")
html = html.decode('UTF-8')

soup = BeautifulSoup(html, 'html.parser')

global city_num
city_num = 0
# get all country 
data = soup.select(' .list-unstyled > li > a')

# save in csv
with open('countriess.csv', 'a') as w:
    writer = csv.writer(w)
    rows = ['id', 'country_name']
    for num,i in enumerate(data):    
        country = [num, i.string]
        writer.writerow(country)
        get_cities(num, url + i.get('href').lower())
