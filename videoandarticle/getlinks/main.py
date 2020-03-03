import os,sys,math,requests,re
from urllib.parse import urlparse

pages = set()
stack = ['http://www.xuexi.cn/lgdata/index.json']

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

def dfsJson(jsonObject):
    jsonObjectStack = [jsonObject]

    while len(jsonObjectStack) > 0:
        jsonObject = jsonObjectStack[-1]; jsonObjectStack.pop()
        if type(jsonObject) is dict:
            for (k,v) in jsonDict.items():
                if type(v) is dict or type(v) is list:
                    jsonObjectStack.append(v)
                elif type(v) is str and k == "link" and urlCheck(v) and v not in pages:
                    jsonUrl = urlToJsonUrl(v)
                    if jsonUrl is None:
                        continue
                    pages.add(v)
                    print(v)
                    stack.append(jsonUrl)

        if type(jsonObject) is list:
            for v in jsonObject:
                jsonObjectStack.append(v)

if __name__ == '__main__':            
    while len(stack)>0:
        ln = len(stack)
        jsonUrl = stack[-1]; stack.pop()
        jsonDict = getJson(jsonUrl)
        if jsonDict is not None:
            dfsJson(jsonDict)

