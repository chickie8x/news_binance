import json
import time
from datetime import datetime
from dotenv import dotenv_values
import requests

# init states
config = dict(dotenv_values('.env'))
first_run_flag = True
pages = 6
pageNo = 1
count = 1
post_url = config["POST_URL"]
news_url = config["NEWS_LINK"]

while True:
    print(count)
    saved_id = []
    list_news = []
    data_write = {}
    new_fetch = []
    with open('data.json', 'r', encoding='utf8') as file:
        read_data = file.read()
        json_data = json.loads(read_data)
        saved_id = json_data["savedId"]
        list_news = json_data["news"]

    if not first_run_flag:
        pages = 1
    for i in range(1, pages + 1):
        url = config['BASE_URL'] + str(i) + config['API_CONF']
        data = requests.get(url)
        jdata = json.loads(data.text)
        for item in jdata["data"]["contents"]:
            obj = {}
            if item["id"] not in saved_id:
                new_fetch.append(item["id"])
                saved_id.append(item["id"])
                obj["id"] = item["id"]
                obj["title"] = item["title"]
                obj["content"] = item["body"]
                obj["date_created"] = str(datetime.fromtimestamp((int(item["createTime"])) / 1000))
                obj["url"] = news_url + str(item["id"])
                # r = requests.post(post_url, data=obj)
                # print(r.status_code)
                list_news.append(obj)
    data_write["savedId"] = saved_id
    data_write["news"] = list_news
    with open('data.json', 'w', encoding='utf') as file:
        json.dump(data_write, file, indent=4, ensure_ascii=False)
    new_fetch = []
    first_run_flag = False
    count += 1
    time.sleep(10)
