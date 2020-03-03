import os,sys,math,requests,re,time
from urllib.parse import urlparse
from selenium import webdriver

STUDY_LIST_FILE = 'list.txt'
FINISHED_LIST_FILE = 'finished.txt'
STUDY_NUMBER_EVERYDAY = 10

finishedPages = set()
videoPages, articlePages = [], []
browser = webdriver.Firefox()
cookies = None

def studyOne(url):
    global browser, cookies
    try:
        browser.get(url)
        html = browser.page_source
        time.sleep(10)
        finishedPages.add(url)
        f = open(FINISHED_LIST_FILE, "a+")
        f.write(url + "\n")
        f.close()

    except Exception:
        browser.quit()
        browser = webdriver.Firefox()
        for cookie in cookies:
            browser.add_cookie(cookie)

def loadPages(file):
    f = open(file)
    for line in f.readlines():
        if "id=" not in line:
            continue
        
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


def study():
    global cookies, browser
    loadPages(STUDY_LIST_FILE)
    loadFinishedPages(FINISHED_LIST_FILE)
    cookies = browser.get_cookies()

    ai, vi = 0, 0
    while True:
        an, vn = 0, 0
        while an < STUDY_NUMBER_EVERYDAY and ai < len(articlePages):
            url = articlePages[ai]
            ai += 1
            if url in finishedPages:
                continue
            studyOne(url)
            an += 1

        while vn < STUDY_NUMBER_EVERYDAY and vi < len(videoPages):
            url = videoPages[vi]
            vi += 1
            if url in finishedPages:
                continue
            studyOne(url)
            vn += 1
        
        time.sleep(3600*20)

if __name__ == '__main__':
    input("Please login first")
    study()