# -*- coding: utf-8 -*-
import os
import time
import pickle
from datetime import datetime

from items import LiepinJobItemLoader, LiepinJobItem, JobItem, JobItemLoader

from items import BossJobItemLoader, BossJobItem
from utils.common import get_md5
from settings import BASE_DIR

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

from tools.Boss_actionChainsLogin import ActionChainsLogin

class BossSpider(CrawlSpider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://www.zhipin.com/xiaoyuan/']
    # start_urls = ['http://www.zhipin.com/']

    rules = (
        Rule(LinkExtractor(allow=r'job_detail/.*.html'), callback='parse_job', follow=True),
    )

    def start_requests(self):
        cookies = []
        # 若存在本地cookies文件，则直接读取
        if os.path.exists(BASE_DIR + "/cookies/boss.cookie"):
            cookies = pickle.load(open(BASE_DIR + "/cookies/boss.cookie", "rb"))
        # 若本地不存在cookies文件，则模拟登录并获取cookies
        if not cookies:
            # 模拟登录成功返回cookies值
            cookies = ActionChainsLogin()
            # 生成cookies文件保存到本地
            pickle.dump(cookies, open(BASE_DIR + "/cookies/boss.cookie", "wb"))
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        for url in self.start_urls:
            # 把cookie传入到后续的所有url中
            yield scrapy.Request(url, dont_filter=True,cookies=cookie_dict)

    # def parse_job(self, response):
    #     item_loader = BossJobItemLoader(item=BossJobItem(), response=response)
    #     item_loader.add_css("title", ".job-primary .info-primary .name h1::text")
    #     item_loader.add_value("url", response.url)
    #     item_loader.add_value("url_object_id", get_md5(response.url))
    #     item_loader.add_css("salary", ".job-primary .info-primary .name .salary::text")
    #     item_loader.add_css("job_ex", ".job-primary .info-primary p")
    #     item_loader.add_css("job_desc", ".detail-content .job-sec .text")
    #     item_loader.add_css("job_addr", ".job-primary .info-primary p")
    #     # item_loader.add_css("publish_time", "")
    #     item_loader.add_value("crawl_time", datetime.now())
    #     job_item = item_loader.load_item()
    #
    #     return job_item

    def parse_job(self, response):
        item_loader = JobItemLoader(item=JobItem(), response=response)
        item_loader.add_css("title", ".job-primary .info-primary .name h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job-primary .info-primary .name .salary::text")
        item_loader.add_css("job_desc", ".detail-content .job-sec .text")
        item_loader.add_css("job_addr", ".job-primary .info-primary p")
        job_item = item_loader.load_item()

        return job_item     #  返回的job_item将传入pipeline

