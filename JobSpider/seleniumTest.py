# -*- coding: utf-8 -*-

import time
import pickle
from urllib import parse

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup



# chromeOption = Options()
# chromeOption.add_argument("--disable-extensions")
# chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#
# browser = webdriver.Chrome(executable_path="D:/Chromedriver/chromedriver.exe",
#                            chrome_options=chromeOption)
# browser.get("https://www.zhihu.com/signin")
#
# browser.find_element_by_css_selector(".SignFlow-tabs div:nth-child(2)").click()
#
#
# browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
# browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13794058740")
# browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
# browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys("156416421727av")
# time.sleep(2)
# browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
# time.sleep(2)


# cookies = browser.get_cookies()
#
# # pickle.dump(cookies, open("C:/Users/Administrator/ZhihuSpider/cookies/zhihu.cookie", "wb"))
# cookie_dict = {}
# for cookie in cookies:
#     cookie_dict[cookie["name"]] = cookie["value"]

cookies = pickle.load(open("C:/Users/Administrator/ZhihuSpider/cookies/zhihu.cookie", "rb"))
cookie_dict = {}
for cookie in cookies:
    cookie_dict[cookie["name"]] = cookie["value"]

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

t = requests.get("https://www.zhihu.com", headers=header, cookies=cookie_dict).content.decode()

# print(t.content.decode("utf-8"))
print(t)

soup = BeautifulSoup(t)

# a = soup.select(".Card.TopstoryItem.TopstoryItem-isRecommend")
#
# print(a)

all_urls = soup.select(".ContentItem-title div a::attrs['href'][0]")
# all_urls = [parse.urljoin(soup.url, url) for url in all_urls]
print(all_urls)
for url in all_urls:
    print(url)

# # browser.find_element_by_css_selector(".SignFlowInput .Input-wrapper input").click()
# browser.find_element_by_css_selector(".Captcha.SignFlow-captchaContainer .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
# browser.find_element_by_css_selector(".Captcha.SignFlow-captchaContainer .SignFlowInput .Input-wrapper input").send_keys("4444")
# # browser.find_element_by_xpath("//div/main/div/div/div[1]/div/form/div[4]/div/div/label/input").send_keys(Keys.CONTROL + "a")
# # browser.find_element_by_xpath("//div/main/div/div/div[1]/div/form/div[4]/div/div/label/input").send_keys("4444")
# browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
# browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13794058740")
# browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys(Keys.CONTROL + "a")
# browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys("156416421727av")
# time.sleep(2)
# browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
# time.sleep(2)

