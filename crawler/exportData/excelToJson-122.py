import json
import os

import xlrd

fileOutName = './json/'
fileinName = './历届广交会名单-122'
os.mkdir(fileOutName + "历届广交会名单-122")

# 行业
industry = -1



def getXlsFile():
    # 初始化下行业
    global industry
    industry = -1

    list = os.listdir(fileinName)
    list.reverse()

    for i in range(0, len(list)):
        path = os.path.join(fileinName, list[i])
        # xxx届广交会
        if os.path.isdir(path):

            os.mkdir(fileOutName + path.replace('./', ''))

            xlslist = os.listdir(path)
            xlslist.reverse()
            # 遍历每届
            for j in range(0, len(xlslist)):
                xlsPath = os.path.join(path, xlslist[j])
                if os.path.isfile(xlsPath):
                    xlsFile = xlrd.open_workbook(xlsPath)
                    try:
                        exportJson(xlsFile, xlsPath)
                        print(xlsPath + " export success")
                    except Exception as e:
                         print(xlsPath + " export fail")
        print(path + " export ok")
        print("_____________________________________________________")


def exportJson(xlsFile, xlsPath):
    out = open(fileOutName + xlsPath.replace('xlsx', 'json').replace('xls', 'json').replace('./', ''), 'w')

    global industry
    industry = xlsPath.split('_')[1].replace('.xlsx', '').replace('.xls', '')
    industry = int(industry)
    table = xlsFile.sheets()[0]
    getDict(table, out)


def getDict(table, out):
    out.write('[')

    # 定义key
    companyNum = -1
    countryNum = -1
    productNum = -1
    contactNum = -1
    faxNum = -1
    emailNum = -1
    addressNum = -1
    telNum = -1
    websiteNum = -1
    skypeNum = -1
    for j in range(0, table.ncols):
        dateList = table.row_values(0)
        key = dateList[j].replace(' ','')
        if key == '公司名' or key=='公司名称' or key=='名称':
            companyNum = j
        elif key.find('国家') != -1 or key=='地区':
            countryNum = j
        elif key == '采购产品类别' or key=='所属行业' or key=='业务':
            productNum = j
        elif key == '联系人' or key== '姓名':
            contactNum = j
        elif key == '传真':
            faxNum = j
        elif key.find('邮箱') != -1 or key=='电子邮件' or key=='Email':
            emailNum = j
        elif key == '联系地址' or key=='地址':
            addressNum = j
        elif key == '电话' or key == '联系电话' or key=='联系':
            telNum = j
        elif key == '网址':
            websiteNum = j

        elif key == 'SKYPE':
            skypeNum = j

    for i in range(1, table.nrows):
        dateList = table.row_values(i)

        company = ''
        if (companyNum != -1):
            company = dateList[companyNum]

        country = ''
        if (countryNum != -1):
            country = dateList[countryNum]

        product = ''
        if (productNum != -1):
            product = dateList[productNum]

        tel = ''
        if (telNum != -1):
            tel = dateList[telNum]

        contact = ''
        if (contactNum != -1):
            contact = dateList[contactNum]

        fax = ''
        if (faxNum != -1):
            fax = dateList[faxNum]

        address = ''
        if (addressNum != -1):
            address = dateList[addressNum]

        email = ''
        if (emailNum != -1):
            email = dateList[emailNum]

        website = ''
        if (websiteNum!=-1):
            website = dateList[websiteNum]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''),
                    'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website, 'requirement_remark': 'CF',
                    'industry': industry}

        if (skypeNum!=-1):
            # msn = dateList[11]
            skype = dateList[skypeNum]
            dataDict['skype'] = skype

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows- 1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')
    out.flush()
    out.close()



def main():
    getXlsFile()


if __name__ == '__main__':
    main()
