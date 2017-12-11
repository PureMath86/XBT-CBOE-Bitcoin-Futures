from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime as dt


TEN_MIN = 10*60.0

class RequestSoup_spider():

    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url)
        self.data = self.r.text
        self.soup = BeautifulSoup(self.data, "html.parser")

    def list_data(self, tag):
        self._list = []
        for item in self.soup.find_all(tag):
            self._list.append(item.contents)

        return self._list


url = r"http://cfe.cboe.com/cfe-products/xbt-cboe-bitcoin-futures"

while ((dt.now().hour >=2) and (dt.now().hour <= 16)):
    spider = RequestSoup_spider(url)

    orig_df = pd.read_csv(r'.\scrape\CBOE.csv', header=0)
    first_df = pd.read_html(spider.data, header=0)[0]
    first_df['time'] = dt.now()
    dfs = pd.read_html(spider.data)[1:]

    orig_df = orig_df.append(first_df)

    for df in dfs:
        df['time'] = dt.now()
        df.columns = first_df.columns
        orig_df = orig_df.append(df)

    orig_df.to_csv(r'.\scrape\CBOE.csv', index=False)

    time.sleep(TEN_MIN)
