import sys
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

with open('industry_1.txt') as f:
    industries = set((x.strip() for x in f.readlines()))


# 初始化
def init():
    # 定义为全局变量，方便其他模块使用
    global url, browser, wait
    # 主页
    url = 'https://purchaser.mingluji.com/'
    # 实例化一个chrome浏览器
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # 设置等待超时
    wait = WebDriverWait(browser, 20)
    global out
    for industry in industries:
        out=open('./url/'+industry+'.txt','w')
        print(industry,'开始解析')
        getCompanyList(industry.split('-')[0])
        print(industry,'解析完毕')
        print("————————————————————————————————————————————————")
        out.flush()
        out.close()


# 公司列表页
def getCompanyList(industry):
    global count
    count=0
    # 打开页面
    # https: // purchaser.mingluji.com / Hardware
    browser.get(url+industry)
    sleep(1)
    # 查找页数
    page=browser.find_element_by_xpath("//*[contains(text(), 'Index Page No')]")
    pageNum=page.text.split(',')[-1].replace('.','')

    for i in range(0, int(pageNum)+1):
        getCompanyListByPage(industry+"/"+str(i))


#公司列表 带页数
def getCompanyListByPage(industryAndPage):
    global count
    browser.get(url + industryAndPage)
    sleep(1)
    # 将网页源码转化为能被解析的lxml格式
    soup = BeautifulSoup(browser.page_source, 'lxml')
    tbody = soup.find('tbody')
    lis = tbody.find('ol').find_all('li')
    for li in lis:
        try:
            count += 1
            href = li.find('a')['href']
            out.write(href+'\n')
            print(href, count)
        except Exception as e:
            print(industryAndPage, li, 'cant get href', file=sys.stderr)



# 主程序
def main():
    # 初始化
    init()


# 程序入口
if __name__ == '__main__':
    main()

