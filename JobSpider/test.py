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
    time.sleep(2)

    slide_btn = browser.find_element_by_css_selector('span[class="nc_iconfont btn_slide"]')
    success = False
    count = 1
    step_n = 1
    while not success:
        # 通过css选择器找到滑块slide_btn后操控鼠标按住左键
        ActionChains(browser).click_and_hold(slide_btn).perform()
        while count < 300:
            ActionChains(browser).move_by_offset(step_n, 0).perform()
            # step_n为相对于原地向右移动多少距离，这里设置成随机数每次移动距离在[0,10)之间
            step_n = randint(0, 10)
            # 当count大于300即证明滑块已经滑动到最右边
            count = count + step_n
            time.sleep(0.001)
        # 滑块移动到最右边后释放鼠标左键
        ActionChains(browser).release().perform()
        try:
            browser.find_element_by_class_name("errloading") # 滑动失败报错
        except Exception as e:
            success = True  #滑动成功退出循环
        else:
            browser.refresh()

    time.sleep(1)
    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys(Keys.CONTROL + "a")
    time.sleep(1)

    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys("13247598671")

    time.sleep(1)
    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys("156416421727av")

    # 通过css选择器找到“登录”按钮并点击
    browser.find_element_by_css_selector(".sign-pwd .sign-content .form-btn button").click()

    cookies = browser.get_cookies()
    return cookies

if __name__ == "__main__":
    ActionChainsLogin()






