from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import csv

class HotelSpider(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://zs.58.com/chuzu/pn1/?PGTID=0d3090a7-0030-3e26-490e-b2c956dd45d2&ClickID=2'
        self.wait = WebDriverWait(self.browser, 10)

    def run(self):
        self.browser.get(self.url)
        source = self.browser.page_source
        print(source)


if __name__ == '__main__':
    hotel = HotelSpider()
    hotel.run()