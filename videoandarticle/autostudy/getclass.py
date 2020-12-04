import os,sys,math,requests,re
from urllib.parse import urlparse
from selenium import webdriver

def toJsUrl(url):
    ln = len(url)
    i = ln - 1
    while i>=0 and url[i] != '/':
        i -= 1
    if i < 0:
        return None
    
    jsUrl = url[:i+1] + "data" + url[i+1:ln-4] + "js"
    return jsUrl

def getUrls(text):
    regex = re.compile(
        r'https://www.xuexi.cn/[0-9a-zA-Z/]*.html', re.IGNORECASE)
    return re.findall(regex, text)


def get(url):
    return requests.get(url).text

if __name__ == "__main__":
    classHome = get(toJsUrl("https://www.xuexi.cn/f547c0f321ac9a0a95154a21485a29d6/1cdd8ef7bfc3919650206590533c3d2a.html"))
    classes = getUrls(classHome)
    for c in classes:
        chapters = getUrls(get(toJsUrl(c)))
        for ch in chapters:
            print(ch)
