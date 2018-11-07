import json
import os
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup

with open('industry.txt') as f:
    industries = set((x.strip() for x in f.readlines()))


# 初始化
def doGetJson():
    # 定义为全局变量，方便其他模块使用
    global url,s
    # 主页
    url = 'https://purchaser.mingluji.com'
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'})
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
    r = s.get(url+companyUrl.replace('\n',''))
    #r = s.get('https://purchaser.mingluji.com/WESTERN_POLYMERS_DE_MEXICO_SA_DE_CV')
    if r.status_code != 200:
        print(companyUrl,'code error',file=sys.stderr)
        sleep(5)
        s.get('https://purchaser.mingluji.com/Main_Page')
        sleep(30)
        getCompanyInfo(companyUrl, out, industry)
        return
    html = r.text
    #sleep(1)
    # 将网页源码转化为能被解析的lxml格式
    soup = BeautifulSoup(html, 'lxml')

    try:
        companyTag=soup.find("span",{"itemprop":"name"})
        company=companyTag.text if companyTag!=None else ''

        countryTag=soup.find("span",{"itemprop":"location"})
        country=countryTag.text.split('(')[0].strip() if countryTag!=None else ''

        addressTag=soup.find("span",{"itemprop":"address"})
        address=addressTag.text if addressTag!=None else ''

        telephoneTag=soup.find("span",{"itemprop":"telephone"})
        telephone=telephoneTag.text if telephoneTag!=None else ''

        faxNumberTag=soup.find("span",{"itemprop":"faxNumber"})
        faxNumber=faxNumberTag.text if faxNumberTag!=None else ''


        emailTag=soup.find("span",{"itemprop":"email"})
        email=emailTag.text if emailTag!=None else ''

        website=soup.find('b', string='Website').find_parent().find_parent().find_next_sibling().text
        contact=soup.find('b', string='Contact').find_parent().find_parent().find_next_sibling().text
        products=soup.find('b', string='Category').find_parent().find_parent().find_next_sibling().findAll("a",{"class":"extiw"})
        product = ''
        for p in products:
            product += p.text + '|'


        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(telephone).replace('.0', ''),
                    'contact': contact,
                    'fax': str(faxNumber).replace('.0', ''), 'address': address, 'email': email, 'website': website,
                    'requirement_remark': 'MLJ', 'industry': industry}


        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)

        out.write(json_str+',')
    except Exception as e:
        print(e,file=sys.stderr)
        print(companyUrl,'exportError',file=sys.stderr)






# 主程序
def main():
    doGetJson()



# 程序入口
if __name__ == '__main__':
    main()

