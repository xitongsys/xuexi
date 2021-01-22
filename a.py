import requests, qrcode, time, logging

def retry(times: int, interval: int):
    def wrapper(func):
        def inner(*args, **kwarys):
            v = None
            for _ in range(times):
                try:
                    v = func(*args, **kwarys)
                except Exception as err:
                    logging.error(str(err))
                    time.sleep(interval)
                    continue
                break;
            return v
        return inner
    return wrapper

session = requests.Session()

@retry(times = 100, interval = 1)
def getQrcode():
    qr = session.get('https://login.xuexi.cn/user/qrcode/generate').json()['result']
    url = "https://login.xuexi.cn/login/qrcommit?showmenu=false&code={qr}&appId=dingoankubyrfkttorhpou".format(qr = qr)
    img = qrcode.make(url)
    img.save("a.png")
    return qr

@retry(times=100, interval=1)
def getTmpCode(qrcode: str):
    url = 'https://login.xuexi.cn/login/login_with_qr'
    res = session.post(url, data={
        "qrCode": qrcode,
        "goto": "https://oa.xuexi.cn",
        "pdmToken": ""
    }).json()
    if not res['success']:
        raise Exception(str(res))
    data = res['data']
    key = "loginTmpCode="
    tmpCode = data[data.index(key) + len(key):]
    return tmpCode

@retry(times=100, interval=1)
def getCookies(tmpCode: str):
    url = 'https://pc-api.xuexi.cn/login/secure_check?code={tmpCode}&state=06d81817e84a430fRn3K4e9Temmx7XsXcJVvnBCy7b8DrBR0vkAIQQtA0wCDp0owW5W1o9XkX7aUUZ16'.format(tmpCode=tmpCode)
    res = session.get(url)
    cookies = res.cookies
    res = res.json()
    if not res['success']:
        raise Exception(str(res))
    return [{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path} for c in cookies]

@retry(times=100000, interval=1)
def login():
    qr = getQrcode()
    tmpCode = getTmpCode(qr)
    cookies = getCookies(tmpCode)
    return cookies

cookies = login()
print(cookies)