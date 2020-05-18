from bs4 import BeautifulSoup
import config
import json
import os
import requests
import time


UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
)

session = requests.Session()
session.headers.update({"User-agent": UA})
total_hits = 0
total_investments = 0
for entry in config.LIST_OF_DEVELOPERS:

    url, keyword, identifier = entry

    print("GET", url)
    try:
        html = session.get(url)
        soup = BeautifulSoup(html.text, "lxml")
        hits = len(soup.find_all(text=keyword))

        if hits == 0:
            hits = len(soup.find_all('div', {'class': 'title sale'}))

        total_hits += hits
        total_investments += 1

    except Exception as e:
        print("ERROR", e)
        print("SKIPPING", url)
        continue

    result = {"date": time.strftime("%Y-%m-%d"), "hits": hits}

    data = {}
    if os.path.isfile(config.DATA_FILE):
        data = json.load(open(config.DATA_FILE, "r"))

    if identifier not in data:
        data[identifier] = {}

    data[identifier][result["date"]] = result["hits"]
    with open(config.DATA_FILE, "w+") as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)

    print("%s\t total_hits %s\t%s" % (total_investments, total_hits, identifier))
