import csv
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

import requests
from lxml import etree
import datetime

# 自动采集互站源码求购需求
# 生成表格发送到邮箱
# 定时每日早上8:00运行

# 求代码url
url_buy_code = 'https://demand.huzhan.com/code/'
# 任务url
url_deploy_task = 'https://task.huzhan.com/menu/%401_2/order/time'

# 前天
now = datetime.datetime.now()
outfilename = 'huzhan_{}.csv'.format(now.strftime('%Y-%m-%d'))


def crawler_buy_code():
    title_xpath = '//dl/dt/a/@title'
    href_xpath = '//dl/dt/a/@href'
    price_xpath = '//dl//dt/em/*/text() | //dl//dt/em/text()'
    time_xpath = '//div[@class="alist"]/dl/dd[@class="d1"]/text()'

    response = requests.get(url_buy_code, verify=False)

    html = etree.HTML(response.text, etree.HTMLParser())

    title = html.xpath(title_xpath)
    href = html.xpath(href_xpath)
    price = html.xpath(price_xpath)
    deploy_time = html.xpath(time_xpath)
    total = len(title)

    before_yesterday = (now + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
    with open(outfilename, mode='a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        for idx in range(total):
            t = deploy_time[idx].strip()
            # 只采集前天之后发布的
            if t < before_yesterday:
                continue
            writer.writerow([title[idx], price[idx], t, href[idx]])
        writer.writerow([])


def crawler_deploy_task():
    title_xpath = '//div[@class="tlist"]/div[@class="items"]/dl/dt/p/a/@title'
    href_xpath = '//div[@class="tlist"]/div[@class="items"]/dl/dt/p/a/@href'
    price_xpath = '//div[@class="tlist"]/div[@class="items"]/dl/dt/p/b/text()'

    response = requests.get(url_deploy_task, verify=False)

    html = etree.HTML(response.text, etree.HTMLParser())

    title = html.xpath(title_xpath)
    href = html.xpath(href_xpath)
    price = html.xpath(price_xpath)
    total = len(title)

    base_href = "https://task.huzhan.com"
    with open(outfilename, mode='a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        for idx in range(total):
            writer.writerow([title[idx], price[idx], None, base_href + href[idx]])
        writer.writerow([])


def crawler_sale_item():
    url_sale = 'https://www.huzhan.com/code/order/time'

    item_xpath = '//div[@class="clist"]/div[@class="list_items"]/dl/dd/'
    title_xpath = item_xpath + 'p[@class="title"]/a/@title'
    href_xpath = item_xpath + 'p[@class="title"]/a/@href'
    price_xpath = item_xpath + 'p[@class="attr"]/em/strong/text()'
    tag_xpath = item_xpath + 'p[@class="attr"]/span/text()'

    response = requests.get(url_sale, verify=False)

    html = etree.HTML(response.text, etree.HTMLParser())

    title = html.xpath(title_xpath)
    href = html.xpath(href_xpath)
    price = html.xpath(price_xpath)
    tag = html.xpath(tag_xpath)
    total = len(title)

    base_href = "https://www.huzhan.com"
    with open(outfilename, mode='a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        for idx in range(total):
            writer.writerow([title[idx], price[idx], tag[idx], base_href + href[idx]])
        writer.writerow([])

    # 广告推广
    href_xpath = '//div[@class="right_rec"]/dl/dd/a/@href'
    title_xpath = '//div[@class="right_rec"]/dl/dd/a/@title'
    price_xpath = '//div[@class="right_rec"]/dl/dd/div/em/strong/text()'
    title = html.xpath(title_xpath)
    href = html.xpath(href_xpath)
    price = html.xpath(price_xpath)
    total = len(title)

    with open(outfilename, mode='a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        for idx in range(total):
            writer.writerow([title[idx], price[idx], None, base_href + href[idx]])


def send_mail(subject, content, filename, send_to):
    user = '417706248@qq.com'
    password = 'frjjstajsretbicb'

    # 邮件对象
    msg = MIMEMultipart()
    # 邮件主题
    msg['Subject'] = Header(subject)
    # 发送方
    msg['From'] = Header('python crawler<417706248@qq.com>')
    # 接收方
    msg['To'] = Header('击石')
    # 正文
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 附件
    attatch = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    attatch["Content-Type"] = 'application/octet-stream'
    attatch["Content-Disposition"] = 'attachment; filename="{}"'.format(outfilename)
    msg.attach(attatch)
    with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
        # 登录发送邮件服务器
        smtp.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=user, to_addrs=send_to, msg=msg.as_string())


crawler_buy_code()
time.sleep(1)
crawler_deploy_task()
time.sleep(1)
crawler_sale_item()
send_mail('互站需求统计', 'data from python crawler', outfilename, '417706248@qq.com')
print('mail sent')
