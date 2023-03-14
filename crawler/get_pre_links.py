import random
import time

import requests
from lxml import etree
from fake_useragent import UserAgent
import csv

raw_url = 'http://www.baidu.com/s?wd={}'
ua = UserAgent()
# keywords = ['源码超市', '源码市场', '源码交易', '源码集市', '小程序源码', 'app源码', '源码出售', '游戏源码']
keywords = [ 'app源码', '源码出售', '游戏源码']
with open('pre_links.csv', mode='a', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)

    for keyword in keywords:
        url = raw_url.format(keyword)
        headers = {"User-Agent": ua.random}
        # response = requests.get(url, verify=False, headers=headers)
        response = requests.get(url, verify=False)
        print('http code: ', response.status_code)
        html = etree.HTML(response.text, etree.HTMLParser())
        pre_links = html.xpath('//h3[@class="c-title t t tts-title"]/a/@href')
        writer.writerow(pre_links)
        time.sleep(random.randint(10, 30))
