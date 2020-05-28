# -*- coding: utf-8 -*-

import os
import time
import pickle
from datetime import datetime


from items import ZhilianJobItemLoader, ZhilianJobItem
from utils.common import get_md5
from settings import BASE_DIR

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader


class ZhilianSpider(CrawlSpider):
    name = 'zhilian'
    allowed_domains = ['campus.liepin.com']
    start_urls = ['http://campus.liepin.com/']

    rules = (
        # Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
        Rule(LinkExtractor(allow=r'job/.*'), callback='parse_job', follow=True),
    )

    # def start_requests(self):
    #     cookies = []
    #     if os.path.exists(BASE_DIR + "/cookies/lagou.cookie"):
    #         cookies = pickle.load(open(BASE_DIR + "/cookies/lagou.cookie", "rb"))
    #
    #     if not cookies:
    #         chromeOption = Options()
    #         chromeOption.add_argument("--disable-extensions")
    #         chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #
    #         browser = webdriver.Chrome(executable_path="I:/chromedriver/chromedriver.exe",
    #                                    chrome_options=chromeOption)
    #         try:
    #             browser.maximize_window()
    #         except:
    #             pass
    #
    #         browser.get("https://passport.lagou.com/login/login.html")
    #         browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(1) input").send_keys(Keys.CONTROL + "a")
    #         time.sleep(3)
    #         browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(1) input").send_keys("13247598671")
    #         time.sleep(3)
    #         browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(2) input").send_keys(Keys.CONTROL + "a")
    #         browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(2) input").send_keys("156416421727av.")
    #         browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(5) .btn_active").click()
    #         time.sleep(15)
    #
    #         cookies = browser.get_cookies()
    #         pickle.dump(cookies, open(BASE_DIR + "/cookies/lagou.cookie", "wb"))
    #
    #     cookie_dict = {}
    #     for cookie in cookies:
    #         cookie_dict[cookie["name"]] = cookie["value"]
    #
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, dont_filter=True,cookies=cookie_dict)

    def parse_job(self, response):
        item_loader = ZhilianJobItemLoader(item=ZhilianJobItem(), response=response)
        item_loader.add_css("title", ".job-title.clearfix .job-name::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job-brief .job-info .salary::text")

        item_loader.add_value("crawl_time", datetime.now())
        job_item = item_loader.load_item()

        return job_item
