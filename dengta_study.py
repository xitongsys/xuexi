#%%

# web address: https://gbwlxy.dtdjzx.gov.cn/content#/personalCenter
# 1855316****,591655943kk

#%% cookie
import requests
import json
import threading,os,sys,math,time
import threadpool
import pandas as pd

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7,et;q=0.6,zh-TW;q=0.5,ru;q=0.4",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/json;",
    "Cookie": "sajssdk_2015_cross_new_user=1; Hm_lvt_b1b8902d5017be113d38ecbd55fe8e46=1702778149; X-SESSION=b416660a-6381-4345-81cd-4b7b3332acec; Hm_lvt_d652361e289e90df5f0bacaa8bf8cf2b=1702778208; Hm_lpvt_d652361e289e90df5f0bacaa8bf8cf2b=1702778245; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%222da4093494ac45f8b547e946fed18cb8%22%2C%22first_id%22%3A%2218c757c98a23ab-02d1ff4c33f8fa-26001951-2073600-18c757c98a3287%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThjNzU3Yzk4YTIzYWItMDJkMWZmNGMzM2Y4ZmEtMjYwMDE5NTEtMjA3MzYwMC0xOGM3NTdjOThhMzI4NyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjJkYTQwOTM0OTRhYzQ1ZjhiNTQ3ZTk0NmZlZDE4Y2I4In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%222da4093494ac45f8b547e946fed18cb8%22%7D%2C%22%24device_id%22%3A%2218c757c98a23ab-02d1ff4c33f8fa-26001951-2073600-18c757c98a3287%22%7D; _cs=38046f81-5368-4c1d-bda9-da90cfacbffe; Hm_lpvt_b1b8902d5017be113d38ecbd55fe8e46=1702778333",
    "Host": "gbwlxy.dtdjzx.gov.cn",
    "Referer": "https://gbwlxy.dtdjzx.gov.cn/content",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
}


#%% list

url = 'https://gbwlxy.dtdjzx.gov.cn/__api/api/portal/course/recommend'
body = {"pagenum": 1, "pagesize": 30, "recommendation": "new",
        "name": "", "idCardHash": "fjQVtf9PVAKnHIS92AjcUnqA6EU="}

rows = []
for i in range(1, 60):
    body["pagenum"] = i
    body_str = json.dumps(body)
    res = requests.post(url=url, headers=headers, data=body_str)
    datalist = json.loads(res.text)["datalist"]
    rows = rows + datalist

df = pd.DataFrame(rows)
df.to_pickle("ids.pkl")


#%% study

df = pd.read_pickle("ids.pkl")
df = df[(df.examStatus == "0") & (df.showStatusMsg == "未学习") & (df.resourceType == "VIDEO") & (df.assessementType == "1")]
df['key'] = df['courseDuration'] / df['creditHour']
df = df.sort_values('key')



for i in range(len(df)):
    row = df.iloc[i]
    id, duration = int(row['id']), int(row['courseDuration']*60 + 50)
    
    course_url = f"https://gbwlxy.dtdjzx.gov.cn/content#/commend/coursedetail?courseId={id}"
    res = requests.get(url=course_url, headers=headers)
    
    
    
    start_url = 'https://gbwlxy.dtdjzx.gov.cn/__api/api/study/start'
    progress_url = 'https://gbwlxy.dtdjzx.gov.cn/__api/api/study/progress'
    end_url = 'https://gbwlxy.dtdjzx.gov.cn/__api/api/study/v2/end'

    start_body = {
        "courseId": id, "idCardHash": "fjQVtf9PVAKnHIS92AjcUnqA6EU=", "studyType": "VIDEO"
    }

    progress_body = {
        "courseId": id, "idCardHash": "fjQVtf9PVAKnHIS92AjcUnqA6EU=", "studyTimes": 11
    }

    end_body = {
        "courseId": id, "idCardHash": "fjQVtf9PVAKnHIS92AjcUnqA6EU="
    }

    start_body_str = json.dumps(start_body)
    res = requests.post(url=start_url, headers=headers, data=start_body_str)
    print("start: ", id, res.text)

    for t in range(10, duration + 10, 10):
        progress_body["studyTimes"] = t
        progress_body_str = json.dumps(progress_body)
        res = requests.post(
            url=progress_url, headers=headers, data=progress_body_str)
        time.sleep(8)
        print("progress: ", id, t, res.text)
        

    end_body_str = json.dumps(end_body)
    res = requests.post(url=end_url, headers=headers, data=end_body_str)
    print("end: ", id, res.text)


