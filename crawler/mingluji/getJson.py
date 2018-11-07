import json
import os
import sys
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

with open('industry.txt') as f:
    industries = set((x.strip() for x in f.readlines()))


# 初始化
def doGetJson():
    # 定义为全局变量，方便其他模块使用
    global url, browser, wait
    # 主页
    url = 'https://purchaser.mingluji.com'
    # 实例化一个chrome浏览器
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # 设置等待超时
    wait = WebDriverWait(browser, 20)

    fileinName = './url'
    global out

    list = os.listdir(fileinName)
    for i in range(0, len(list)):
        path = os.path.join(fileinName, list[i])
        print(path,"开始解析")
        out=open('./json/'+path.split('/')[-1]+'.json','w')
        out.write('[')

        with open(path) as f:
            urls = set((x for x in f.readlines()))

        for companyUrl in urls:
            getCompanyInfo(companyUrl,out,path.split('-')[-1])


        out.write('{}]')
        print(path, '解析完毕')
        print("————————————————————————————————————————————————")
        out.flush()
        out.close()




# 公司列表页
def getCompanyInfo(companyUrl,out,industry):
    global count
    count=0
    # 打开页面
    # https: // purchaser.mingluji.com / Hardware
    browser.get(url+companyUrl)
    sleep(1)
    # 将网页源码转化为能被解析的lxml格式
    soup = BeautifulSoup(browser.page_source, 'lxml')

    try:
        company=soup.find("span",{"itemprop":"name"}).text
        country=soup.find("span",{"itemprop":"location"}).text.split('(')[0].strip()
        products=soup.find('b', string='Category').find_parent().find_parent().find_next_sibling().findAll("a",{"class":"extiw"})
        product=''
        for p in products:
            product +=p.text+'|'

        address=soup.find("span",{"itemprop":"address"}).text
        contact=soup.find('b', string='Contact').find_parent().find_parent().find_next_sibling().text

        telephone=soup.find("span",{"itemprop":"telephone"}).text
        faxNumber=soup.find("span",{"itemprop":"faxNumber"}).text
        email=soup.find("span",{"itemprop":"email"}).text
        website=soup.find('b', string='Website').find_parent().find_parent().find_next_sibling().text

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(telephone).replace('.0', ''),
                    'contact': contact,
                    'fax': str(faxNumber).replace('.0', ''), 'address': address, 'email': email, 'website': website,
                    'requirement_remark': 'CF', 'industry': industry}


        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)

        out.write(json_str+',')
    except Exception as e:
        print(companyUrl,'exportError',file=sys.stderr)






# 主程序
def main():
    doGetJson()



# 程序入口
if __name__ == '__main__':
    main()

