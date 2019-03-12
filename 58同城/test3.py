import json
import base64
from fontTools.ttLib import TTFont
import io
import requests
from lxml import etree
import re
import time
import datetime

url = 'https://zs.58.com/chuzu/pn1/?PGTID=0d3090a7-0030-3501-551d-e56a391e6773&ClickID=2'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}


# proxy = get_proxy().decode('utf-8')
# print(proxy)
# resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
#
# print(resp.headers)
# time.sleep(2)

# proxy = get_proxy()
# print(type(proxy))
# proxies = {"http": "http://{}".format(proxy)}
# print(proxies)
#
# proxy = get_proxy().decode()
# print(type(proxy))
# proxies = {"http": "http://{}".format(proxy)}
# print(proxies)

def parse():
    while True:
        print('yes')
        return


def get_list(url):
    resp = requests.get(url, headers=headers)
    if resp:
        base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*)\'\) format\(\'truetype\'\)}',
                                resp.text)
        bin_data = base64.b64decode(base64_str[0])
        fonts = TTFont(io.BytesIO(bin_data))
        bestcmap = fonts.getBestCmap()
        print(bestcmap)

        newmap = {}
        for key in bestcmap.keys():
            print(key)
            print(re.findall(r'(\d+)', bestcmap[key]))
            value = int(re.findall(r'(\d+)', bestcmap[key])[0]) - 1
            key = hex(key)
            newmap[key] = value
        print('==========', newmap)

if __name__ == '__main__':
    get_list(url)




