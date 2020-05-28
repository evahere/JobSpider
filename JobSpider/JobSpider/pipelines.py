# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi
from models.es_types import LagouType, LiepinType, BossType
import redis

redis_cli = redis.StrictRedis()


class ZhihuspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'zhihu_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                INSERT INTO zhihu_question(zhihu_id, title, content, url, topics, answer_num, comments_num, watch_user_num)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

        #
        # insert_sql = """
        #         INSERT INTO zhihu_question(zhihu_id, title)
        #         VALUES (%s, %s)
        #         """

        params = list()
        tmp = item["zhihu_id"][0]
        params.append(tmp)
        # params.append(item.get("zhihu_id", ""))
        tmp2 = "".join(item["title"])
        params.append(tmp2)
        # params.append(item.get("title", ""))
        # params.append(item.get("content", ""))
        # params.append(item.get("url", ""))
        # topics = ",".join(item.get("topics", ""))
        # params.append(topics)
        # answer_num = ",".join(item.get("answer_num", ""))
        # params.append(answer_num)
        # comments_num = ",".join(item.get("comments_num", ""))
        # params.append(comments_num)
        # watch_user_num = ",".join(item.get("watch_user_num", ""))
        # params.append(watch_user_num)
        params = tuple(params)
        self.cursor.execute(insert_sql, params)
        # self.conn.commit()
        pass


class LagouJobPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'lagou', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                INSERT INTO lagoujob(
                    title, url, url_object_id, salary, job_city, work_years, degree_need,job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url, tags, crawl_time
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("salary", ""))
        params.append(item.get("job_city", ""))
        params.append(item.get("work_years", ""))
        params.append(item.get("degree_need", ""))
        params.append(item.get("job_type", ""))
        params.append(item.get("publish_time", ""))
        params.append(item.get("job_advantage", ""))
        params.append(item.get("job_desc", ""))
        params.append(item.get("job_addr", ""))
        params.append(item.get("company_name", ""))
        params.append(item.get("company_url", ""))
        params.append(item.get("tags", ""))
        params.append(item.get("crawl_time", ""))
        params = tuple(params)
        self.cursor.execute(insert_sql, params)
        self.conn.commit()

        return item


# 异步插入
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                        INSERT INTO lagoujob(
                            title, url, url_object_id, salary, job_city, work_years, degree_need,job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url, tags, crawl_time
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE salary=VALUES(salary)
                        """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("salary", ""))
        params.append(item.get("job_city", ""))
        params.append(item.get("work_years", ""))
        params.append(item.get("degree_need", ""))
        params.append(item.get("job_type", ""))
        params.append(item.get("publish_time", ""))
        params.append(item.get("job_advantage", ""))
        params.append(item.get("job_desc", ""))
        params.append(item.get("job_addr", ""))
        params.append(item.get("company_name", ""))
        params.append(item.get("company_url", ""))
        params.append(item.get("tags", ""))
        params.append(item.get("crawl_time", ""))
        params = tuple(params)
        cursor.execute(insert_sql, params)


class ElasticsearchPipeline(object):
    # 将数据写入es中

    def process_item(self, item, spider):
        # 将item转换为es数据
        lagou = LagouType()
        lagou.title = item.get("title", "")
        lagou.url = item.get("url", "")
        lagou.url_object_id = item.get("url_object_id", "")
        lagou.salary = item.get("salary", "")
        # lagou.job_city = item.get("job_city", "")
        # lagou.work_years = item.get("work_years", "")
        # lagou.degree_need = item.get("degree_need", "")
        # lagou.job_type = item.get("job_type", "")
        # lagou.publish_time = item.get("publish_time", "")
        # lagou.job_advantage = item.get("job_advantage", "")
        lagou.job_desc = item.get("job_desc", "")
        lagou.job_addr = item.get("job_addr", "")
        # lagou.company_name = item.get("company_name", "")
        # lagou.company_url = item.get("company_url", "")
        # lagou.tags = item.get("tags", "")

        lagou.meta.id = item["url_object_id"]

        lagou.save()

        return item


class LiepinJobPipeline(object):
    # 将数据写入es中
    def process_item(self, item, spider):
        # 将item转换为es数据
        Liepin = LiepinType()       # 生成es实例
        Liepin.title = item.get("title", "")
        Liepin.url = item.get("url", "")
        Liepin.url_object_id = item.get("url_object_id", "")
        Liepin.salary = item.get("salary", "")
        Liepin.job_addr = item.get("job_addr", "")
        Liepin.job_desc = item.get("job_desc", "")
        Liepin.meta.id = Liepin.url_object_id

        Liepin.save()
        redis_cli.incr("liepin_count")  # 数据爬取量

        return item


# class LiepinJobPipeline(object):
#     # 将数据写入es中
#     def process_item(self, item, spider):
#         # 将item转换为es数据
#         Liepin = LiepinType()
#         Liepin.title = item.get("title", "")
#         Liepin.url = item.get("url", "")
#         Liepin.url_object_id = item.get("url_object_id", "")
#         Liepin.salary = item.get("salary", "")
#         Liepin.job_addr = item.get("job_addr", "")
#         Liepin.job_desc = item.get("job_desc", "")
#         Liepin.publish_time = item.get("publish_time", "")
#         Liepin.meta.id = item["url_object_id"]
#
#         Liepin.save()
#         redis_cli.incr("liepin_count")
#
#         return item


class BossJobPipeline(object):
    # 将数据写入es中
    def process_item(self, item, spider):
        # 将item转换为es数据
        Boss = BossType()
        Boss.title = item.get("title", "")
        Boss.url = item.get("url", "")
        Boss.url_object_id = item.get("url_object_id", "")
        Boss.salary = item.get("salary", "")
        Boss.job_addr = item.get("job_addr", "")
        Boss.job_ex = item.get("job_ex", "")
        Boss.job_desc = item.get("job_desc", "")
        # Liepin.publish_time = item.get("publish_time", "")
        Boss.meta.id = item["url_object_id"]

        Boss.save()

        return item


