import urllib.request, urllib.error
from bs4 import BeautifulSoup

def load_site(url):
    # URLにアクセスする htmlが帰ってくる
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    return soup


def find_by_id(soup,id):
    ul = soup.find(id=id)

    lists = ""

    try:
        lists = ul.find_all('li')
    except:
        pass

    response=[]
    for index in lists:
        dic = {}
        dic["date"] = index.div.find(class_="date").text
        dic["string"] = index.div.find(class_="title").a.string
        dic["href"] = index.a.attrs["href"]
        response.append(dic)

    return response

def find_by_id_2(soup,id):
    ul = soup.find(id=id)

    lists = ""

    try:
        lists = ul.find_all('li')
    except:
        pass

    response=[]
    for index in lists:
        dic = {}
        p = index.div.find(class_="date").text
        p = p.strip('共通E＆ESDMPSI')
        dic["date"] = p
        dic["course"] = index.div.find(class_="date").strong.string
        dic["string"] = index.div.find(class_="title").a.string
        dic["href"] = index.a.attrs["href"]
        response.append(dic)

    return response