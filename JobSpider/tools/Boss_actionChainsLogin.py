import time
from random import randint

from pynput.mouse import Button, Controller

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


def ActionChainsLogin():
    chromeOption = ChromeOptions()
    chromeOption.add_argument("--disable-extensions")
    chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    browser = webdriver.Chrome(executable_path="I:/chromedriver/chromedriver.exe", options=chromeOption)
    try:
        # 首先把网页最大化便于后续操作
        browser.maximize_window()
    except:
        pass
    browser.get("https://login.zhipin.com/")
    time.sleep(3)

    slide_btn = browser.find_element_by_css_selector('span[class="nc_iconfont btn_slide"]')
    time.sleep(1)

    success = False
    count = 1
    step_n = 1
    # 移动滑块
    while not success:
        time.sleep(1)
        ActionChains(browser).click_and_hold(slide_btn).perform()
        time.sleep(1)
        while count < 300:
            ActionChains(browser).move_by_offset(step_n, 0).perform()
            step_n = randint(0, 10)
            count = count + step_n
            time.sleep(0.001)
        ActionChains(browser).release().perform()
        time.sleep(1)
        try:
            browser.find_element_by_class_name("errloading")
        except Exception as e:
            success = True
        else:
            time.sleep(1)
            browser.refresh()

    time.sleep(1)

    # 清空输入框
    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys(Keys.CONTROL + "a")
    # 输入账号
    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys("13247598671")

    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys(Keys.CONTROL + "a")
    # 输入密码
    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys("156416421727av")
    time.sleep(3)
    # 点击登录
    browser.find_element_by_css_selector(".sign-pwd .sign-content .form-btn button").click()
    time.sleep(3)

    # 获取cookies并返回
    cookies = browser.get_cookies()
    return cookies

if __name__ == "__main__":
    ActionChainsLogin()