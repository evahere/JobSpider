import time
from random import randint

from pynput.mouse import Button, Controller

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

#
# chromeOption = Options()
# chromeOption.add_argument("--disable-extensions")
# chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# browser = webdriver.Chrome(executable_path="I:\chromedriver\chromedriver.exe", chrome_options=chromeOption)

chromeOption = webdriver.ChromeOptions()
chromeOption.add_argument("--disable-extensions")
chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(executable_path="I:\chromedriver\chromedriver.exe", options=chromeOption)


browser.get("https://login.zhipin.com/")

time.sleep(2)

# browser.find_element_by_css_selector(".sign-pwd .sign-content .form-btn button").click()

slide_btn = browser.find_element_by_css_selector('span[class="nc_iconfont btn_slide"]')

time.sleep(2)

# action = ActionChains(browser)
# action.click_and_hold(slide_btn).perform()
# for i in range(200):
#     try:
#         action.move_by_offset(i*2,0).perform()
#     except:
#         break
#     action.reset_actions()
#     time.sleep(0.1)
mouse = Controller()
success = False
count = 1
step_n = 1
while not success:
    time.sleep(2)
    ActionChains(browser).click_and_hold(slide_btn).perform()
    time.sleep(1)
    while count < 300:
        ActionChains(browser).move_by_offset(step_n, 0).perform()
        step_n = randint(0, 10)
        count = count + step_n
        time.sleep(0.001)
    ActionChains(browser).release().perform()
    count = 1
    time.sleep(1)

    try:
        error_tips = browser.find_element_by_class_name("errloading")
    # except selenium.common.exceptions.NoSuchElementException:
    except Exception as e:
        success = True
    else:
        time.sleep(1)
        fresh_location = browser.find_element_by_css_selector(".errloading span a").location
        fresh_x = fresh_location["x"] + 5
        fresh_y = fresh_location["y"] + 105
        mouse.position = (fresh_x, fresh_y)
        time.sleep(1)
        mouse.click(Button.left, 1)



# ActionChains(browser).click_and_hold(slide_btn).perform()
# time.sleep(1)
# for i in range(100):
#     ActionChains(browser).move_by_offset(i*2, 0).perform()
#     time.sleep(0.05)
# time.sleep(3)

# ActionChains(browser).release().perform()

browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys(Keys.CONTROL + "a")
time.sleep(1)
browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys("13247598671")
time.sleep(1)

browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys(Keys.CONTROL + "a")
time.sleep(1)
browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys("156416421727av")
time.sleep(3)

browser.find_element_by_css_selector(".sign-pwd .sign-content .form-btn button").click()

time.sleep(3)

