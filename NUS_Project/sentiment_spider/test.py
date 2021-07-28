import requests


url = 'https://guba.eastmoney.com/list,600519_9.html'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko'}
try:
    r = requests.get(url, headers=header)
    r.raise_for_status()
    r.encoding = 'utf-8'
    print(r.text)

except:
    # return getHtml(url)
    print("ero")