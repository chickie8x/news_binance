import json
import time
from datetime import datetime
from dotenv import dotenv_values
import requests
from slugify import slugify

# init states
config = dict(dotenv_values('.env'))
url = config['BASE_URL']
post_url = config["POST_URL"]
record_url = config["RECORD_URL"]

while True:
    saved_id = []
    list_news = []
    data_write = {}
    new_fetch = []
    with open('data.json', 'r', encoding='utf8') as file:
        read_data = file.read()
        json_data = json.loads(read_data)
        saved_id = json_data["savedId"]
        exist_news = json_data["record"]
        new_fetch =[]

    data = requests.get(url)
    jdata = json.loads(data.text)
    for item in jdata["data"]["catalogs"]:
        if item["catalogId"] == 49:
            if item["articles"].__len__():
                for record in item["articles"]:
                    if record["id"] not in saved_id:
                        obj = {}
                        saved_id.append(record["id"])
                        obj["title"] = record["title"]
                        print(slugify(record["title"]))
                        obj["url"] = record_url + slugify(record["title"]) + "-" + str(record["code"]) + "_nguyentran"
                        obj["published_date"] = str(datetime.fromtimestamp(int(record["releaseDate"])//1000))
                        new_fetch.append(obj)
                if new_fetch.__len__():
                    r = requests.post(post_url, json=new_fetch)
                    print(r.status_code)
    data_write["savedId"] = saved_id
    data_write["record"] = exist_news + new_fetch
    with open('data.json', 'w', encoding='utf') as file:
        json.dump(data_write, file, indent=4, ensure_ascii=False)

    time.sleep(10)
