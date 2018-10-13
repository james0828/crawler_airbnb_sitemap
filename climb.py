import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import html.parser

def get_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read()
    return html

def get_cities(url):
    count = 1
    while True:
        obj = url + "?page=" + str(count)
        print(obj)
        html = get_html(obj)
        html = html.decode('UTF-8')

        soup = BeautifulSoup(html, 'html.parser')

        # data = soup.find('span', {'class': 'screen-reader-only', 'string': '下一頁'})
        
        data = soup.select(' .col-sm-4 > .list-unstyled > li > a')
        
        for i in data:
            print(i.string)

        inspect = soup.find(attrs={'rel','next'})
        if inspect == None:
            break

        count = count + 1

url = "https://www.airbnb.com.tw"
html = get_html(url + "/sitemaps")
html = html.decode('UTF-8')

soup = BeautifulSoup(html, 'html.parser')
#print(soup)
# print(soup.title)

# get all country 
data = soup.select(' .list-unstyled > li > a')

# data = []
for i in data:
    # print(i.get('href'))
    # print(i.string)
    get_cities(url + i.get('href').lower())




# print(soup.prettify())
#info = requests.get('https://www.airbnb.com.tw/sitemaps')
#info.encoding = 'utf8'

#root = etree.fromstring(info.content, etree.HTMLParser())
#print(info.text)
