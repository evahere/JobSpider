# -*- coding: utf-8 -*-

import re
import time
import json
import pickle
import base64
import datetime
from urllib import parse

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from mouse import move, click
from zheye import zheye
from tools.YDMHTTPDemo import YDMHttp
from scrapy.loader import ItemLoader
from ZhihuSpider.items import ZhihuQuestionItem, ZhihuAnswerItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    # question的每一页answer
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&platform=desktop&sort_by=default'

    # start_urls = ["https://www.zhihu.com/question/32019460/answer/875114975"]

    # def start_requests(self):
    #     cookies = pickle.load(open("C:/Users/Administrator/ZhihuSpider/cookies/zhihu.cookie", "rb"))
    #     cookie_dict = {}
    #     for cookie in cookies:
    #         cookie_dict[cookie["name"]] = cookie["value"]
    #
    #     return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
    #
    #     # chromeOption = Options()
    #     # chromeOption.add_argument("--disable-extensions")
    #     # chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #     #
    #     # browser = webdriver.Chrome(executable_path="D:/Chromedriver/chromedriver.exe",
    #     #                            chrome_options=chromeOption)
    #     # # browser.get("https://www.zhihu.com/signin")
    #     # # browser.find_element_by_css_selector(".SignFlow-tabs div:nth-child(2)").click()
    #     # #
    #     # # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
    #     # # time.sleep(3)
    #     # # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13247598671")
    #     # # browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
    #     # # time.sleep(3)
    #     # # browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys("156416421727av")
    #     # #
    #     # # time.sleep(3)
    #     # # # move(600,540)
    #     # # # click()
    #     # # browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
    #     # browser.get("https://www.zhihu.com/")
    #     cookies = browser.get_cookies()
    #     print(cookies)
    #     import pickle
    #     pickle.dump(cookies, open("C:/Users/Administrator/ZhihuSpider/cookies/zhihu.cookie", "wb"))
    #     cookie_dict = {}
    #     for cookie in cookies:
    #         cookie_dict[cookie["name"]] = cookie["value"]
    #     #
    #     # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
    #
    # def parse(self, response):
    #     pass

    def start_requests(self):

        # cookies = pickle.load(open("C:/Users/Administrator/ZhihuSpider/cookies/zhihu.cookie", "rb"))
        # cookie_dict = {}
        # for cookie in cookies:
        #     cookie_dict[cookie["name"]] = cookie["value"]

        chromeOption = Options()
        chromeOption.add_argument("--disable-extensions")
        chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        browser = webdriver.Chrome(executable_path="I:/chromedriver/chromedriver.exe",
                                   chrome_options=chromeOption)
        try:
            browser.maximize_window()
        except:
            pass

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-tabs div:nth-child(2)").click()
        time.sleep(2)
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
        time.sleep(2)
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13247598671")
        browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
        time.sleep(2)
        browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys("156416421727av.")
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(10)
        logon_success = False       # 登录状态
        while not logon_success:
            # 登陆成功
            try:
                # notify_ele = browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
                notify_ele = browser.find_element_by_id("Popover17-toggle")
                logon_success = True
            except:
                pass

            # 登录失败出现中文验证码
            try:
                chinese_captcha_ele = browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_ele = None

            # 登录失败出现英文验证码
            try:
                english_captcha_ele = browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_ele = None

            # 处理中文验证码
            if chinese_captcha_ele:
                ele_postion = chinese_captcha_ele.location
                x_relative = ele_postion["x"]
                y_relative = ele_postion["y"]
                js = "return (window.outerHeight - window.innerHeight);"
                browser_navigation_panel_height = browser.execute_script(js)

                # 获取中文验证码图片（base64）解码，并写入二进制文件
                base64_text = chinese_captcha_ele.get_attribute("src")
                code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
                f = open("captcha_cn.jpeg", "wb")
                f.write(base64.b64decode(code))
                f.close()

                # 自动识别中文验证码
                z = zheye()
                positions = z.Recognize('captcha_cn.jpeg')
                last_position = []
                # 有两个倒立文字
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        last_position.append([positions[1][1], positions[1][0]])
                        last_position.append([positions[0][1], positions[0][0]])
                    else:
                        last_position.append([positions[0][1], positions[0][0]])
                        last_position.append([positions[1][1], positions[1][0]])

                    first_pos = [int(last_position[0][0]) / 2, int(last_position[0][1]) / 2]
                    second_pos = [int(last_position[1][0]) / 2, int(last_position[1][1]) / 2]

                    move(x_relative + first_pos[0], y_relative + first_pos[1] + browser_navigation_panel_height)
                    click()
                    time.sleep(3)

                    move(x_relative + second_pos[0], y_relative + second_pos[1] + browser_navigation_panel_height)
                    click()
                # 只有一个倒立文字
                else:
                    last_position.append([positions[0][1], positions[0][0]])
                    first_pos = [int(last_position[0][0]) / 2, int(last_position[0][1]) / 2]
                    move(x_relative + first_pos[0], y_relative + first_pos[1] + browser_navigation_panel_height)
                    click()

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13247598671")
                browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys("156416421727av")
                browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()


            # 处理英文验证码
            if english_captcha_ele:
                base64_text = english_captcha_ele.get_attribute("src")
                code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
                f = open("captcha_en.jpeg", "wb")
                f.write(base64.b64decode(code))
                f.close()

                # 使用在线云打码
                yundama = YDMHttp('swartz2324', '156416421727av.', 9561, 'd9acf25c4e7f52926f4008a55b4080a3')
                captcha_result = yundama.decode('captcha_en.jpeg', 5000, 60)
                while True:
                    time.sleep(1)
                    if captcha_result == '':
                        captcha_result = yundama.decode('captcha_en.jpeg', 5000, 60)
                    else:
                        break
                browser.find_element_by_css_selector(".Captcha.SignFlow-captchaContainer .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".Captcha.SignFlow-captchaContainer .SignFlowInput .Input-wrapper input").send_keys(captcha_result)

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "13247598671")
                browser.find_element_by_css_selector(
                    ".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(
                    ".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys("156416421727av")
                browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
            time.sleep(3)

        # 登录成功后把cookies保存到本地
        cookies = browser.get_cookies()
        pickle.dump(cookies, open("C:/Users/Administrator/ZhihuSpider/cookies/zhihu.cookie", "wb"))
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

    def parse(self, response):
        time.sleep(7)
        # 获取首页问题url
        all_urls = response.css("div a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            result = re.match("(.*zhihu.com/question/(\d+)).*", url)
            if result:
                # 如果提取到question相关页面
                question_url = result.group(1)
                question_id = result.group(2)
                yield scrapy.Request(question_url, callback=self.question_detail)
            # else:
            #     # 如果不是question相关页面
            #     yield scrapy.Request(url, callback=self.parse)

    def question_detail(self, response):
        if "zh-question-title" not in response.text:
            # 处理知乎新版本

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            result = re.match("(.*zhihu.com/question/(\d+)).*", response.url)
            if result:
                question_id = int(result.group(2))
                item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            # item_loader.add_css("click_num", "")
            # item_loader.add_css("create_time", "")
            # item_loader.add_css("update_time", "")
            # item_loader.add_css("crawl_time", "")
            # item_loader.add_css("crawl_update_time", "")
            question_item = item_loader.load_item()

            t = type(question_item)

            yield scrapy.Request(self.start_answer_url.format(question_item["zhihu_id"][0], 5, 0), callback=self.answer_detail)
            yield question_item

        # else:
        #     # 处理知乎旧版本
        #     pass


    def answer_detail(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        totals = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["next"]
        answer_item = ZhihuAnswerItem()
        for answer in ans_json["data"]:
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"]
            answer_item["content"] = answer["content"]
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, callback=self.answer_detail)



