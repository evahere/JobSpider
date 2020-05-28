# -*- coding: utf-8 -*-

import os
import time
import pickle
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

from items import LagouJobItemLoader, LagouJobItem
from utils.common import get_md5
from settings import BASE_DIR

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results

    def start_requests(self):
        cookies = []
        if os.path.exists(BASE_DIR + "/cookies/lagou.cookie"):
            cookies = pickle.load(open(BASE_DIR + "/cookies/lagou.cookie", "rb"))

        if not cookies:
            chromeOption = ChromeOptions()
            chromeOption.add_argument("--disable-extensions")
            chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            browser = webdriver.Chrome(executable_path="I:/chromedriver/chromedriver.exe", options=chromeOption)
            try:
                browser.maximize_window()
            except:
                pass

            browser.get("https://passport.lagou.com/login/login.html")
            browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(1) input").send_keys(Keys.CONTROL + "a")
            time.sleep(3)
            browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(1) input").send_keys("13247598671")
            time.sleep(3)
            browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(2) input").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(2) input").send_keys("156416421727av.")
            browser.find_element_by_css_selector(".form-content div:nth-child(2) form div:nth-child(5) .btn_active").click()
            time.sleep(15)

            cookies = browser.get_cookies()
            pickle.dump(cookies, open(BASE_DIR + "/cookies/lagou.cookie", "wb"))

        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True,cookies=cookie_dict)

    def parse_job(self, response):
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        # item_loader.add_css("job_city", ".job_request span:nth-child(2)::text")
        # item_loader.add_css("work_years", ".job_request span:nth-child(3)::text")
        # item_loader.add_css("degree_need", ".job_request span:nth-child(4)::text")
        # item_loader.add_css("job_type", ".job_request span:nth-child(5)::text")
        # item_loader.add_css("tags", ".position-label li::text")
        # item_loader.add_css("publish_time", ".publish_time::text")
        # item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job-detail")
        item_loader.add_css("job_addr", ".work_addr")
        # item_loader.add_css("company_name", "#job_company img::attr(alt)")
        # item_loader.add_xpath("company_url", "//*[@id='job_company']/dt/a/@href")
        # item_loader.add_value("crawl_time", datetime.now())
        job_item = item_loader.load_item()

        return job_item
