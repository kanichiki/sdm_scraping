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

    lists = []

    try:
        lists = ul.find_all(class_="title")
    except:
        pass

    response={}
    for index in lists:
        dic = {}
        dic["string"] = index.a.string
        dic["href"] = index.a.attrs["href"]
        response.append(dic)

    return response