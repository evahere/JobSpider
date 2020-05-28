# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from w3lib.html import remove_tags


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()


class LagouJobItemLoader(ItemLoader):
    # 自定义itemLoader
    default_input_processor = TakeFirst()

def remove_splash(value):
    # 去掉数据中的斜杠
    return value.replace("/", "")

def remove_enter(value):
    # 去掉\n
    return "".join(value).replace("\n", "").replace(" ", "").replace("查看地图", "")

def remove_xa0(value):
    # 去掉\xa0 ---> &nbsp 不间断空白符
    return value.replace("\xa0", "")

class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    # job_city = scrapy.Field(
    #     input_processor=MapCompose(remove_splash),
    #     # output_processor=Join(),      Join()函数把输出的数据清洗，相当于''.join() ----> 列表转字符串
    # )
    # work_years = scrapy.Field(
    #     input_processor=MapCompose(remove_splash),
    #     # output_processor=Join(),
    # )
    # degree_need = scrapy.Field(
        # input_processor=MapCompose(remove_splash),
        # output_processor=Join(),
    # )
    # job_type = scrapy.Field()
    # publish_time = scrapy.Field(
    #     input_processor=MapCompose(remove_xa0),
    # )
    # job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_enter),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_enter),
    )
    # company_name = scrapy.Field()
    # company_url = scrapy.Field()
    # tags = scrapy.Field()
    # crawl_time = scrapy.Field()


class ZhilianJobItemLoader(ItemLoader):
    # 自定义itemLoader
    default_input_processor = TakeFirst()


class ZhilianJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_desc = scrapy.Field()
    publish_time = scrapy.Field()
    crawl_time = scrapy.Field()


class LiepinJobItemLoader(ItemLoader):
    # 自定义itemLoader
    default_input_processor = TakeFirst()


class LiepinJobItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=Join(),
    )
    url = scrapy.Field(
        output_processor=Join(),
    )
    url_object_id = scrapy.Field()
    salary = scrapy.Field(
        output_processor=Join(),
    )
    job_addr = scrapy.Field(
        output_processor=Join(),
    )
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_enter),
        output_processor=Join(),
    )
    publish_time = scrapy.Field(
        output_processor=Join(),
    )
    crawl_time = scrapy.Field()


class BossJobItemLoader(ItemLoader):
    # 自定义itemLoader
    default_input_processor = TakeFirst()


class BossJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_ex = scrapy.Field()
    job_addr = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_enter),
    )
    publish_time = scrapy.Field()
    crawl_time = scrapy.Field()


class JobItemLoader(ItemLoader):
    # 自定义itemLoader
    default_input_processor = TakeFirst()

class JobItem(scrapy.Item):
    title = scrapy.Field()  # 职位名称
    url = scrapy.Field()    # 职位url
    url_object_id = scrapy.Field()  # 职位url通过md5加密算法加密，缩短保存长度
    salary = scrapy.Field()     # 薪资
    job_addr = scrapy.Field()   # 工作地址

    # 职位描述，remove_tags()函数除去描述中的html标签，remove_enter()函数除去换行符
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_enter),
    )

