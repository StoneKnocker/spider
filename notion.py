from config.logging_config import log
import requests
import time

page_size=100
url = 'https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId=186596&from={start}&size={page_size}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36',
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Accept-Language": "en-US,en;q=0.9",
    'Cookie': '_pxvid=01724340-1a7c-11ee-9809-55776f8a8ca1; _gcl_au=1.1.1405802488.1688483040; _rdt_uuid=1688483040507.cc7dbd15-61fc-470a-a20d-deb67f361fb3; seerid=e43e9162-172e-470d-9e39-b6fe142a00ce; ELOQUA=GUID=20FB7C64EB504CEEB705427A60DB74AE;  experimentSessionId=727f4083-1473-434c-bf35-f1fc662632aa; _gid=GA1.2.12390067.1694592187; device=Desktop; country_code=HK; _capterra2_session=48d064a64d0a377fe96e202ef5be777b; rt_var=prd; seerses=e; pxcts=fcade0e9-520b-11ee-b475-80c4fe78d01a; ln_or=eyIyNjk3MCI6ImQifQ%3D%3D; AMCVS_04D07E1C5E4DDABB0A495ED1%40AdobeOrg=1; AMCV_04D07E1C5E4DDABB0A495ED1%40AdobeOrg=-637568504%7CMCIDTS%7C19614%7CMCMID%7C00834426191076131590266291835566472477%7CMCAAMLH-1695196996%7C11%7CMCAAMB-1695196996%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1694599396s%7CNONE%7CMCSYNCSOP%7C411-19621%7CvVersion%7C5.1.1; _ga=GA1.2.1708775659.1688483037; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Sep+13+2023+16%3A03%3A57+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _uetsid=fd949980520b11ee8f8933ce9ec02b78; _uetvid=01cabad01a7c11eea8f847ed21034f48; fs_lua=1.1694592238527; fs_uid=#18VAT4#fe9a9630-c2f5-4971-a370-ede9997c242e:a8ea7153-fa7b-4f04-a1e1-462b4f9c1504:1694592196795::3#/1720019043; _px3=756632a3bf7664ad431e7a38ddb75e081c32e3f60d29e6e5cbb37ce9a3265731:m2nP+bAM7uENSCzwtS0NgYVhwJsFYK2h6H8po45ZKagS6+ainYYfdpLmnw6qXOwcFgwaU5oV/x2nWpNDFd/f8Q==:1000:fivnTJxhQqAUyC6r0s9eYVscBZi4OIQpCHP2hB4ygQP+LVu7OkgoYfJdl1IWVWycfKD2SYzSgyRJKJGdKTHoYqSNvhW3L9UD6Wvpppksy8jquAMgyF3MNpLU2aYhGdidpZb+aQZy4yMbKv1oEuDK6v7IglQx37Es4zV9iKWzIhfI/3oECkQrHSXQ6cteSxLbkIH1P0TMzWrn9FIFPQ/RdcHTnAs+crJ/qPCAOyTiByQ=; _pxde=958cf91de6a1c153d9599373dc119c19f5cbd0f31eb62c83228ba5c850ec0799:eyJ0aW1lc3RhbXAiOjE2OTQ1OTIyODI0MzEsImZfa2IiOjAsImlwY19pZCI6W119; _gat_UA-126190-1=1; _ga_T9V61700R6=GS1.1.1694592191.6.1.1694592337.60.0.0; _ga_M5DGBDHG2R=GS1.1.1694592191.5.1.1694592349.60.0.0'
}


with open('output_files/capterra.txt', mode='w', encoding='utf-8') as f:
    i = 0
    while True:
        log.info(f'page {i}')
        u = url.format(start=i*100, page_size=page_size)
        log.info(u)
        response = requests.get(u, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            log.error('error occured: code: %d, msg: %s', response.status_code, response.text)
            break
        
        data = response.json()
        if not data.get('hits'):
            log.info("hits is empty, exit")
            break
        log.info("hits size: %s", data['hits'])

        count = 0
        for hit in data['hits']:
            prosText = hit.get('prosText')
            consText = hit.get('consText')
            generalComments = hit.get('generalComments')
            f.write(f"i: {i}, count: {count}\n")
            if generalComments:
                f.write(f"Overall: {generalComments}\n")
                f.write("\n")
            f.write(f"Pros: {prosText}\n")
            f.write("\n")
            f.write(f"Cons: {consText}\n")
            f.write("\n")
            count += 1


        i += 1
        time.sleep(3)

        
