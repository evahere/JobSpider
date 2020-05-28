from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# 连接Elasticsearch服务器
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class BossType(DocType):
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    salary = Text()
    job_addr = Text()
    job_ex = Text()
    job_desc = Text(analyzer="ik_max_word")

    class Meta:
        index = "boss"
        doc_type = "job"


# class LiepinType(DocType):
#     suggest = Completion(analyzer=ik_analyzer)
#     title = Text(analyzer="ik_max_word")    # 该字段用于后台检索
#     url = Keyword()
#     url_object_id = Keyword()
#     salary = Text()
#     job_desc = Text(analyzer="ik_max_word") # 该字段用于检索
#     job_addr = Text()
#     publish_time = Text()
#
#     class Meta:
#         index = "liepin"
#         doc_type = "job"


class LiepinType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")    # 该字段用于检索
    url = Keyword()
    url_object_id = Keyword()
    salary = Text()
    job_desc = Text(analyzer="ik_max_word") # 该字段用于检索
    job_addr = Text()

    class Meta:
        index = "liepin"    # 在Elasticsearch中创建索引liepin（相当于sql中的数据库）
        doc_type = "job"    # 在索引liepin下创建类型job（相当于在数据库liepin下创建一个job表）


class LagouType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    salary = Text()
    # job_city = Text()
    # work_years = Text()
    # degree_need = Text()
    # job_type = Text()
    publish_time = Text()
    # job_advantage = Text()
    job_desc = Text(analyzer="ik_max_word")
    job_addr = Text()
    # company_name = Text()
    # company_url = Keyword()
    # tags = Text()

    class Meta:
        index = "lagou"
        doc_type = "job"

if __name__ == "__main__":
    # LagouType.init()
    BossType.init()
