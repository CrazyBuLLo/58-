import json
import base64
from fontTools.ttLib import TTFont
import io
import requests
from lxml import etree
import re
import time
import datetime
import pymysql
import pymysql.cursors



url = 'https://gz.58.com/chuzu/1/pn{}/?PGTID=0d3090a7-0000-39c4-5242-4e4773004e78&ClickID=2'



conn = pymysql.connect('localhost', 'root', '1234', '58tongcheng', charset='utf8', use_unicode=True)
cursor = conn.cursor()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

# all_list = []

def get_proxy():
    return requests.get("http://127.0.0.1:8080/get/").content

# 解除字体加密
def get_list(url):
    resp = requests.get(url, headers=headers)
    if resp:
        base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*)\'\) format\(\'truetype\'\)}',
                                resp.text)

        bin_data = base64.b64decode(base64_str[0])
        fonts = TTFont(io.BytesIO(bin_data))
        bestcmap = fonts.getBestCmap()
        newmap = {}
        for key in bestcmap.keys():
            print(key)
            print(re.findall(r'(\d+)', bestcmap[key]))
            value = int(re.findall(r'(\d+)', bestcmap[key])[0]) - 1
            key = hex(key)
            newmap[key] = value

        print('==========', newmap)
        resp_ = resp.text
        for key, value in newmap.items():
            key_ = key.replace('0x', '&#x') + ';'
            if key_ in resp_:
                resp_ = resp_.replace(key_, str(value))
        parse_index(resp_)



def parse_index(content):
    '''

    //ul[@class = 'listUl']/li[@logr and not(contains(@class,'department'))]
    '''
    html = etree.HTML(content)
    # long_title = html.xpath("//a[@class = 'strongbox']/text()")
    # urls = html.xpath("//a[@class = 'strongbox']/@href")
    urls = html.xpath("//ul[@class = 'listUl']/li[@logr and not(contains(@class,'department'))]/@logr")
    # cost_month = html.xpath("//b[@class = 'strongbox']/text()")
    # parameter = html.xpath("//p[@class = 'room strongbox']/text()")
    # for a, b, c, d in zip(long_title, urls, cost_month, parameter):
    #     print(a.strip() + '---' + b.strip() + '---' + c.strip() + '---' + d.strip())
    base_url = 'https://gz.58.com/zufang/{}x.shtml'
    print(len(urls))
    for url in urls:
        print(url)

        id = re.search(r'.*?_.*?_.*?_(\d+)_.*?', url).group(1)
        parse_detail(base_url.format(id))
        # time.sleep(0.5)
        time.sleep(2)



def parse_detail(url):
    # 先将获取的代理从bytes类型转换为str类型
    proxy = get_proxy().decode('utf-8')
    try:
        print('using proxy %s' % proxy)
        resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
    except Exception:
        print('获取网页信息失败')
        return None

    if resp:
        # print(resp.status_code)
        try:
            base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*)\'\) format\(\'truetype\'\)}',
                                    resp.text)

            bin_data = base64.b64decode(base64_str[0])
            fonts = TTFont(io.BytesIO(bin_data))
            bestcmap = fonts.getBestCmap()
            newmap = {}
            for key in bestcmap.keys():
                # print(key)
                # print(re.findall(r'(\d+)', bestcmap[key]))
                value = int(re.findall(r'(\d+)', bestcmap[key])[0]) - 1
                key = hex(key)
                newmap[key] = value

            # print('==========', newmap)
            resp_ = resp.text
            for key, value in newmap.items():
                key_ = key.replace('0x', '&#x') + ';'
                if key_ in resp_:
                    resp_ = resp_.replace(key_, str(value))

            html = etree.HTML(resp_)

            long_title = html.xpath("//h1[@class = 'c_333 f20 strongbox']/text()")[0]
            cost = html.xpath("//b[@class = 'f36 strongbox']/text()")[0]
            cost = float(cost)
            xiaoqu = html.xpath("//ul[@class = 'f14']/li[4]/span[2]/a/text()")[0]
            house_type = html.xpath("//ul[@class = 'f14']/li[2]/span[2]/text()")[0].strip().replace(' ', '')
            house_type = house_type.split()
            standard = house_type[0]
            square = float(house_type[1].replace('平', ''))

            phone = html.xpath("//span[@class = 'house-chat-txt strongbox']/text()")[0]
            id = re.search(r'.*zufang/(\d+)x\.shtml', url).group(1)
            # print(id, '-------', url, '-------', phone, '-------', long_title, '-------', cost, '-------', xiaoqu, '-------', house_type)


            print({
                'id': id,
                'long_title': long_title,
                'cost': cost,
                'xiaoqu': xiaoqu,
                'standard': standard,
                'square': square,
                'phone': phone,
                'url': url
            })

            return insert_to_mysql(id, long_title, cost, xiaoqu, standard, square, phone, url)

        except Exception:
            print('None')
            return None

def write_to_json(id_list):
    content = json.dumps(id_list, ensure_ascii=False)
    with open('hotel.json', 'w', encoding='utf-8') as fp:
        fp.write(content)
        fp.close()

def insert_to_mysql(id, long_title, cost, xiaoqu, standard, square, phone, url):
    insert_sql = """
        insert into guangzhou(id, long_title, cost, xiaoqu, standard, square, phone, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) on DUPLICATE key UPDATE long_title = VALUES(long_title),
         cost = VALUES(cost), phone = VALUES(phone)
    """
    cursor.execute(insert_sql, (id, long_title, cost, xiaoqu, standard, square, phone, url))
    conn.commit()


if __name__ == '__main__':
    starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for i in range(1, 71):
        url = url.format(i)
        print('正在爬取第%d页' % i)
        get_list(url)

    endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(starttime)
    print(endtime)

    print('finish')


