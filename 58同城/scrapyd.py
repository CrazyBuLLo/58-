import requests

# 启动爬虫，post请求
def start_spider():
    url = 'http://localhost:6800/schedule.json'
    data = {
        'project': 'jianshu_spider',
        'spider': 'js'
    }
    response = requests.post(url, data=data)
    print(response.text)


# 查看日志，get请求
def catch_log():
    myproject = 'jianshu_spider'
    url = "http://localhost:6800/listjobs.json?project=" + myproject
    response = requests.get(url)
    print(response.text)


# 停止一个爬虫
def stop_spider():
    url = 'http://localhost:6800/cancel.json'
    data = {
        'project': 'jianshu_spider',
        'job': '76a94146188c11e9871dac2b6ef72b45'
    }
    response = requests.post(url, data=data)
    print(response.text)
    print('停止爬虫')

def delete_spider():
    url = 'http://127.0.0.1:6800/delproject.json'
    data = {
        'project': 'jianshu_spider'
    }
    response = requests.post(url, data=data)
    print(response.text)
    print('删除爬虫')

# 获取项目列表
def get_spider_list():
    url = 'http://127.0.0.1:6800/listprojects.json'
    response = requests.get(url)
    print(response.text)

if __name__ == '__main__':
    # start_spider()
    stop_spider()
    # catch_log()