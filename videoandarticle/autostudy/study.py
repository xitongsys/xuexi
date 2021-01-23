import os,sys,math,requests,re,time,datetime,random,json
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver import ActionChains
import schedule

STUDY_LIST_FILE = 'list.txt'
FINISHED_LIST_FILE = 'finished.txt'
STUDY_NUMBER_EVERYDAY = 6
HOME_URL = "https://xuexi.cn"
COOKIE_FILE = "cookies.json"

finishedPages = set()
videoPages, articlePages = [], []
#opts = webdriver.ChromeOptions()
#opts.add_argument('--no-sandbox')
#browser = webdriver.Chrome(options=opts)
browser = None
cookies = None

def restartBrowser():
    global browser, cookies, HOME_URL
    try:
        browser.quit()
        #browser = webdriver.Chrome()
        browser = webdriver.Firefox()
        browser.get(HOME_URL)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            browser.add_cookie(cookie)
    except:
        time.sleep(2)
        restartBrowser()

def moveMouseRandom():
    try:
        elements = browser.find_elements_by_tag_name("div")
        idx = random.randint(0, len(elements)-1)
        element = elements[idx]
        if element is not None:
            hover = ActionChains(browser).move_to_element(element)
            hover.perform()
    except:
        pass
    
def studyOne(url):
    global browser, cookies
    try:
        browser.get(url)
        html = browser.page_source
        elements = browser.find_elements_by_tag_name("div")
        for i in range(0, int(60 * 3.5)):
            element = elements[(i%len(elements))]
            if element is not None:
                try:
                    hover = ActionChains(browser).move_to_element(element)
                    hover.perform()
                except:
                    pass
            time.sleep(1)

        finishedPages.add(url)
        f = open(FINISHED_LIST_FILE, "a+")
        f.write(url + "\n")
        f.close()

    except Exception as e:
        print(e)
        restartBrowser()

def loadPages(file):
    f = open(file)
    for line in f.readlines():
        t, url = line[0], line[2:-1]
        if t == "a":
            articlePages.append(url)
        else:
            videoPages.append(url)

def loadFinishedPages(file):
    f = open(file, "r")
    for line in f.readlines():
        finishedPages.add(line[:-1])
    f.close()

def loadCookies():
    global cookies, browser
    if os.path.exists(COOKIE_FILE):
        f = open(COOKIE_FILE, "r")
        s = f.read()
        f.close()
        cookies = json.loads(s)
    else:
        input("no cookies.json found, please login first")
        cookies = browser.get_cookies()
        f = open(COOKIE_FILE, "w+")
        f.write(json.dumps(cookies))
        f.close()


def study():
    global cookies, browser
    try:
        browser = webdriver.Firefox()
        loadPages(STUDY_LIST_FILE)
        loadFinishedPages(FINISHED_LIST_FILE)

        loadCookies()
        print(cookies)

        restartBrowser()
        ai, vi = 0, 0
        an, vn = 0, 0
        while vn < STUDY_NUMBER_EVERYDAY and vi < len(videoPages):
            url = videoPages[vi]
            vi += 1
            if url in finishedPages:
                continue
            studyOne(url)
            print("study video: ", url)
            vn += 1

        print("video study finished")

        while an < STUDY_NUMBER_EVERYDAY and ai < len(articlePages):
            url = articlePages[ai]
            ai += 1
            if url in finishedPages:
                continue
            studyOne(url)
            print("study article: ", url)
            an += 1

        print("article study finished")
        browser.quit()
    except Exception as err:
        print(err)
        if browser is not None:
            browser.quit()
       
if __name__ == '__main__':
    schedule.every().day.at("21:10").do(study)
    while True:
        schedule.run_pending()
        time.sleep(1)
