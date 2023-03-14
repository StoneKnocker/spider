import csv

from lxml import etree

with open('kfc优惠.html', encoding='utf-8') as f:
    text = f.read()
    html = etree.HTML(text, etree.HTMLParser())
    href_xpath= '//*[@id="pcReference"]/div/div/div[3]/div/div[3]/table/tbody/tr/td[2]/div/div/a[1]/@href'
    # href_xpath= '//*[@id="pcReference"]/div/div/div[3]/div/div[3]/table/tbody/tr/td[2]/div/div/a[1]/@href'
    links = html.xpath(href_xpath)
    print(links)
    with open('kdc优惠.csv',mode='w', encoding='utf-8', newline='') as outf:
        writer = csv.writer(outf)
        for link in links:
            writer.writerow((link,))

