import os,sys,math,requests,re
from urllib.parse import urlparse
from selenium import webdriver

pages = set()
stack = []
browser = webdriver.Firefox()

def urlCheck(url: str) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def urlToJsonUrl(url: str) -> str:
    res = urlparse(url)
    if not res.path.endswith(".html"):
        return None
    jsonPath = "/lgdata" + res.path[:-5] + ".json"
    jsonUrl = res.scheme + "://" + res.netloc + jsonPath
    return jsonUrl
    
def getJson(url):
    try:
        return requests.get(url).json()
    except:
        return None

def dfsJson(jsonObject, output):
    jsonObjectStack = [jsonObject]
    while len(jsonObjectStack) > 0:
        jsonObject = jsonObjectStack[-1]; jsonObjectStack.pop()

        items = []
        if type(jsonObject) is dict:
            items = jsonObject.items()
        elif type(jsonObject) is list or type(jsonObject) is tuple:
            items = jsonObject

        for v in items:
            if type(v) is dict or type(v) is list or type(v) is tuple:
                jsonObjectStack.append(v)
            elif type(v) is str and urlCheck(v) and v not in pages:
                jsonUrl = urlToJsonUrl(v)
                if jsonUrl is None:
                    continue
                pages.add(v)
                t = tag(v)
                if t is not None:
                    output.write(t + " " + v + "\n")
                stack.append(jsonUrl)

def tag(url):
    global browser
    try:
        #browser = webdriver.Firefox()
        browser.get(url)
        html = browser.page_source
        #browser.quit()

        if "系统正在维护中" in html:
            return None
        elif "\"prism-player\"" in html:
            return "v"
        return "a"

    except Exception:
        browser.quit()
        browser = webdriver.Firefox()
        return None


def getAllLinks(url, output):
    stack.append(url)            
    while len(stack)>0:
        ln = len(stack)
        jsonUrl = stack[-1]; stack.pop()
        jsonDict = getJson(jsonUrl)
        if jsonDict is not None:
            dfsJson(jsonDict, output)


if __name__ == '__main__':
    # print(tag("https://www.xuexi.cn/lgpage/detail/index.html?id=17532310632353996301"))
    output = open("list.txt", "w+", buffering=1)
    getAllLinks("http://www.xuexi.cn/lgdata/index.json", output)
    output.close()