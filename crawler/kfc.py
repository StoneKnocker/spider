import csv
import random
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from lxml import etree
from fake_useragent import UserAgent

huge_sites = ['baidu', 'zhihu', 'jianshu', '163.com']

option = webdriver.ChromeOptions()
option.add_argument('--headless')
bs = webdriver.Chrome(chrome_options=option)
bs.set_page_load_timeout(2)

raw_url = 'http://www.baidu.com/s?wd={}&rn=50'
# ua = UserAgent()
keywords = ['肯德基优惠', '肯德基折扣']
with open('kfc.csv', mode='a', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)

    for keyword in keywords:
        url = raw_url.format(keyword)
        # headers = {"User-Agent": ua.random}
        response = requests.get(url, verify=False)
        print('http code: ', response.status_code)
        html = etree.HTML(response.text, etree.HTMLParser())
        pre_links = html.xpath('//h3[@class="c-title t t tts-title"]/a/@href')

        for pre_link in pre_links:
            print("pre_link: ", pre_link)
            try:
                bs.get(pre_link)
            except TimeoutException:  # 超时有可能已经拿到url
                pass
            except WebDriverException as e:
                print("", e.msg)
                continue
            if not bs.current_url:
                print("timeout, pre_link: ", pre_link)
                continue
            for huge_site in huge_sites:
                if huge_site in bs.current_url:
                    break
            else:
                print(bs.title, bs.current_url)
                writer.writerow([bs.title, bs.current_url])
            time.sleep(random.randint(3, 8))
        time.sleep(30)
bs.quit()
