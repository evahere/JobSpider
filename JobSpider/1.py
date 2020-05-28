import time
from random import randint

from pynput.mouse import Button, Controller

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


chromeOption = webdriver.ChromeOptions()
chromeOption.add_argument("--disable-extensions")
chromeOption.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(executable_path="I:\chromedriver\chromedriver.exe", options=chromeOption)
browser.get("https://login.zhipin.com/")

time.sleep(2)



time.sleep(2)
# browser.find_element_by_css_selector(".SignFlow-tabs div:nth-child(2)").click()
# time.sleep(1)
browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys(Keys.CONTROL + "a")
time.sleep(1)
browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='tel']").send_keys("13247598671")
time.sleep(1)

browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys(Keys.CONTROL + "a")
time.sleep(1)
browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").send_keys("156416421727av")
time.sleep(3)


initLocation = browser.find_element_by_css_selector("form .form-row .ipt-wrap input[type='password']").location
slider_x = initLocation["x"] + 10
slider_y = initLocation["y"] + 42 + 30 + 100 + 20
mouse = Controller()
success = False
count = 1
ran = 1
while not success:
    time.sleep(1)
    mouse.position = (slider_x, slider_y)
    time.sleep(1)
    mouse.press(Button.left)
    time.sleep(1)
    while count < 300:
        mouse.move(ran, 0)
        ran = randint(0, 10)
        count = count + ran
        time.sleep(0.01)
    time.sleep(1)
    mouse.release(Button.left)
    count = 1

    try:
        error_tips = browser.find_element_by_class_name("errloading")
    # except selenium.common.exceptions.NoSuchElementException:
    except Exception as e:
        success = True
    else:
        # time.sleep(1)
        # fresh_location = browser.find_element_by_css_selector(".errloading span a").location
        # fresh_x = fresh_location["x"] + 5
        # fresh_y = fresh_location["y"] + 105
        # mouse.position = (fresh_x, fresh_y)
        # time.sleep(0.5)
        # mouse.click(Button.left, 1)
        browser.refresh()


time.sleep(1)

browser.find_element_by_css_selector(".sign-pwd .sign-content .form-btn button").click()


time.sleep(5)

# browser.quit()

