import csv
import random
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


option = webdriver.ChromeOptions()
option.add_argument('--headless')
bs = webdriver.Chrome(chrome_options=option)
bs.set_page_load_timeout(2)

with open('code_site.csv', mode='a', newline='', encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    with open('pre_links.csv', mode='r', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for pre_links in reader:
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
bs.quit()
