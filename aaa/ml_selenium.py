# coding=utf-8
import datetime
import logging
import os
import traceback
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 日志
def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Standard output handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter('%(levelname)s - %(name)s:%(lineno)s: %(message)s'))
    log.addHandler(sh)
    return log


logger = get_logger(__file__)


# 测试用例执行函数
def work(browser):
    url = 'http://www.mi.com/a/h/5969.html'
    browser.get(url)
    myCookie = {'domain': '.mi.com',
        'path': '/',
        'expires': None,'name': 'cUserId', 'value': '-LU0ce7rIlKd3WIexYeWv-0bXlI'}
    browser.add_cookie(myCookie)

    myCookie1 = {'domain': '.mi.com',
        'path': '/',
        'expires': None,'name': 'client_id', 'value': '180100041086'}
    browser.add_cookie(myCookie1)

    myCookie2= {'domain': '.mi.com',
                 'path': '/',
                 'expires': None, 'name': 'mUserId', 'value': 'unBRa32X8cfGuA74QIltO4QfHOcC9s8Jo4SuBUBwXag%3D'}
    browser.add_cookie(myCookie2)


    myCookie3= {'domain': '.mi.com',
        'path': '/',
        'expires': None,'name': 'euid', 'value': '8V%2Bu%2BD6sN4jWqtc6E1hOkA%3D%3D'}
    browser.add_cookie(myCookie3)

    myCookie4 = {'domain': '.mi.com',
                 'path': '/',
                 'expires': None, 'name': 'serviceToken', 'value': 'jT8okI3f7t3m27IQX%2F2QWO6J0KyfYE28Dnb00%2Blc7kNP8dYUr10tsCM1uA6u0yQLalXV0d7bQ%2BXMKMzlLUh2rnfMQMW6taprofOJpyrZuOQrcDJ1Wozc%2BINVsZZQR9Xvv7dv3asLXP%2FyGaJIuCe6Iwv04SPvXqJ9m4RVEuu8NgI%3D'}
    browser.add_cookie(myCookie4)
    browser.get(url)
    sleep(3)
    while True:
        browser.find_element_by_id('J_chatContent').send_keys('orz 我的 我的 都是我的！！')
        browser.find_element_by_id('J_sendChatBtn').click()
        sleep(1)



def writeLog():
    # 组合日志文件名（当前文件名+当前时间）.比如：case_login_success_20150817192533
    basename = os.path.splitext(os.path.basename(__file__))[0]
    logFile = basename + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
    logging.basicConfig(filename=logFile)
    s = traceback.format_exc()
    logging.error(s)
    browser.get_screenshot_as_file("./" + logFile + "-screenshot_error.png")



if __name__ == "__main__":
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options)  # Chrome界面
    # browser = webdriver.PhantomJS()  # 无界面
    work(browser)
    browser.quit()
