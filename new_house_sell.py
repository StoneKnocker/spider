#!-*- coding:utf-8 -*-
import logging
import os
import re
import time
import requests
import csv

from lxml import etree
from common.config import LOG_FORMAT, DATE_FORMAT, log_dir, set_rand_ua
from bs4 import BeautifulSoup
from mem.all_urls import all_urls

log_name = os.path.basename(os.path.dirname(__file__))
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT,
                    handlers=[logging.FileHandler(filename="{}.log".format(os.path.join(log_dir, log_name)),
                                                  encoding='utf-8', mode='a+')])

first_page = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index.shtml'
# sec_page = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index_1.shtml'
# last_page = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index_91.shtml'
base_page = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index_{}.shtml'


date_pattern = re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日')
day_href_xpath = '//div[@class="main"]/div/ul/li/a/@href'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Cookie': '_trs_uv=lcpkx46p_3394_fe7p; x_host_key=186782393d2-3e8fb818e756ecbc7cc9ffe18d114f709a4d5279'
}

session = requests.Session()

# 数据表格的链接列表
def collect_urls():
    data_urls = []
    for i in range(0, 92):
        url = base_page.format(i)
        if i == 0:
            url = first_page
        logging.info("url: %s", url)
        response = session.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text, etree.HTMLParser())

        href_list = html.xpath(day_href_xpath)
        data_urls.extend(href_list)
        time.sleep(0.5)
    
    return data_urls


# x_path1 = '/html/body/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody/tr[18]/td[2]/font'
# x_path2 = '/html/body/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/table/tbody/tr[18]/td[2]'

# xpath解析有问题，改用beautifulsoup
# table_url = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/202302/t20230221_2156903.shtml'
# response = requests.get(table_url, verify=False)
# response.encoding = 'utf-8'
# table_html = etree.HTML(response.text, etree.HTMLParser())
#
# print(response.text)
#
# table_xpath = '//table[@class="table table-bordered"]/tbody/tr[18]/td[2]'
# num = table_html.xpath(table_xpath)
# print(num)


def get_date_num(url, pattern):
    response = session.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    tables = soup.find_all('table')
    tbody = tables[0].tbody
    
    # 比较新的数据 17行是合计， 也有18行是合计的
    tr_idx = 17
    while tr_idx <= 18:
        tr = tbody.find_all('tr')[tr_idx]
        td0 = tr.find_all('td')[0]
        if td0.text == '合计':
            break
        logging.error("tr_idx: %d, td0: %s", tr_idx, td0.text)
        if tr_idx == 18:
            raise Exception("行错误，不是合计")
        tr_idx += 1
    td1 = tr.find_all('td')[1]
    # 成交数量
    num = td1.text
    
    # 日期
    date = None
    h2s = soup.find_all('h2')
    for h2 in h2s:
        alls = re.search(pattern, h2.text)
        nums = alls.groups()
        if nums is None:
            continue
        logging.info(h2.text)
        date = '{:0>4s}{:0>2s}{:0>2s}'.format(nums[0], nums[1], nums[2])
        break
    return (date, num)


# new_url = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/202302/t20230221_2156903.shtml'
# old_url = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/202001/t20200109_715741.shtml'
# get_date_num(new_url, date_pattern)
# test_url = 'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/202106/t20210606_1714469.shtml'


if __name__ == '__main__':
    # urls = collect_urls()
    # logging.info("all urls: %s", urls)
    urls = all_urls
    
    # get_date_num(test_url, date_pattern)
    
    with open('new_house_sell.csv',mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
    
        for url in urls:
            date, num = get_date_num(url, date_pattern)
            logging.info("date: %s, num: %s", date, num)
            csv_writer.writerow([date, num])
            time.sleep(0.5)
        