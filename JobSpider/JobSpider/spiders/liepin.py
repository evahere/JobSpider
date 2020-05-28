# -*- coding: utf-8 -*-
import os
import time
import pickle
from datetime import datetime


from items import LiepinJobItemLoader, LiepinJobItem, JobItem, JobItemLoader
from utils.common import get_md5
from settings import BASE_DIR

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader


class LiepinSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['campus.liepin.com']
    start_urls = ['http://campus.liepin.com/']

    rules = (
        # 用正则表达式限制spider只采集http://campus.liepin.com/job/下的页面
        Rule(LinkExtractor(allow=r'job/\d+/'), callback='parse_job', follow=True),
        # Rule(LinkExtractor(deny=r'sojob/.*'), callback = 'parse_job', follow = True),
        # Rule(LinkExtractor(deny=r'xycompany/.*'), callback = 'parse_job', follow = True),
        # Rule(LinkExtractor(deny=r'broadcast/.*'), callback='parse_job', follow=True),
        # Rule(LinkExtractor(deny=r'xycompany/.*'), callback='parse_job', follow=True),
    )

    # def parse_job(self, response):
    #     item_loader = LiepinJobItemLoader(item=LiepinJobItem(), response=response)
    #     item_loader.add_css("title", ".job-title.clearfix .job-name::text")
    #     item_loader.add_value("url", response.url)
    #     item_loader.add_value("url_object_id", get_md5(response.url))
    #     item_loader.add_css("salary", ".job-brief .job-info .salary::text")
    #     item_loader.add_css("job_desc", ".job-desc")
    #     item_loader.add_css("job_addr", ".job-brief .job-info .where::text")
    #     item_loader.add_css("publish_time", ".time-info .create-time::text")
    #     item_loader.add_value("crawl_time", datetime.now())
    #     job_item = item_loader.load_item()
    #
    #     return job_item


    def parse_job(self, response):
        item_loader = JobItemLoader(item=JobItem(), response=response)
        item_loader.add_css("title", ".job-title.clearfix .job-name::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job-brief .job-info .salary::text")
        item_loader.add_css("job_desc", ".job-desc")
        item_loader.add_css("job_addr", ".job-brief .job-info .where::text")
        job_item = item_loader.load_item()

        return job_item     # 返回的job_item将传入pipeline



