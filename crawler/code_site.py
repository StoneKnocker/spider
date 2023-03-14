import csv
import random
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from lxml import etree
from fake_useragent import UserAgent


option = webdriver.ChromeOptions()
option.add_argument('--headless')
bs = webdriver.Chrome(chrome_options=option)
bs.set_page_load_timeout(2)

raw_url = 'http://www.baidu.com/s?wd={}'
ua = UserAgent()
keywords = ['源码超市', '源码市场', '源码交易', '源码集市', '小程序源码', 'app源码', '源码出售', '游戏源码']
with open('code_site.csv', mode='a', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)

    for keyword in keywords:
        url = raw_url.format(keyword)
        headers = {"User-Agent": ua.random}
        response = requests.get(url, verify=False, headers=headers)
        print('http code: ', response.status_code)
        html = etree.HTML(response.text, etree.HTMLParser())
        pre_links = html.xpath('//h3[@class="c-title t t tts-title"]/a/@href')

        for pre_link in pre_links:
            print("pre_link: ", pre_link)
            try:
                bs.get(pre_link)
            except TimeoutException:  # 超时有可能已经拿到url
                pass
            if not bs.current_url:
                print("timeout, pre_link: ", pre_link)
                continue
            print(bs.title, bs.current_url)
            writer.writerow([bs.title, bs.current_url])
            time.sleep(random.randint(10, 30))
        time.sleep(30)
bs.quit()
