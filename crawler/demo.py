huge_sites = ['baidu', 'zhihu', 'jianshu', '163.com']

url = 'baidu.com'
for huge_site in huge_sites:
    if huge_site in url:
        break
else:
    print(url)
