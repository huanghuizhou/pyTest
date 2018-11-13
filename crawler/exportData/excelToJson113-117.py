import json
import os

import xlrd

fileOutName = './json/'
fileinName = './历届广交会名单-113-117'
os.mkdir(fileOutName+"历届广交会名单-113-117")

#行业
industry=-1



def getXlsFile():

    #初始化下行业
    global industry
    industry=-1

    list = os.listdir(fileinName)
    list.reverse()

    for i in range(0, len(list)):
        path = os.path.join(fileinName, list[i])
        #xxx届广交会
        if os.path.isdir(path):

            os.mkdir(fileOutName + path.replace('./',''))

            xlslist = os.listdir(path)
            xlslist.reverse()
            #遍历每届
            for j in range(0, len(xlslist)):
                xlsPath = os.path.join(path, xlslist[j])
                if os.path.isfile(xlsPath):
                    xlsFile = xlrd.open_workbook(xlsPath)
                    try:
                        exportJson(xlsFile,xlsPath)
                        print(xlsPath+" export success")
                    except Exception as e:
                        print(xlsPath+" export fail")
        print(path+" export ok")
        print("_____________________________________________________")



def exportJson(xlsFile,xlsPath):
    out = open(fileOutName +xlsPath.replace('xlsx','json').replace('xls','json').replace('./',''), 'w')

    global industry
    industry=xlsPath.split('_')[1].replace('.xlsx','').replace('.xls','')
    industry=int(industry)
    table = xlsFile.sheets()[0]
    type =table.row_values(5)[0]
    dataDict=None
    if(type=='公司名称'):
        getDict1(table,out)
    elif(type=='来自国家'):
        getDict2(table,out)
    elif(type == '公司名'):
        if table.row_values(5)[8].replace(' ','')=='网址':
            getDict7(table,out)
        else:
            getDict3(table,out)
    elif (type == 'company'):
        getDict4(table,out)
    elif (type == 'company'):
        getDict4(table,out)
    elif (type == 'CompanyName公司名称'):
        getDict5(table,out)
    elif (type == '类型'):
        getDict6(table,out)


#第一种excel
def getDict1(table,out):

    out.write('[')
    for i in range(6,table.nrows):
        dateList = table.row_values(i)
        company = dateList[0]
        country = dateList[1]
        product = dateList[2]
        tel = dateList[5]
        contact = dateList[6]
        fax = dateList[7]
        address = dateList[8]
        email = dateList[9]

        website=''
        if (len(dateList) > 10):
            website = dateList[10]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': str(contact),
                    'fax': str(fax).replace('.0',''), 'address':  str(address), 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        if (len(dateList) > 11):
            # msn = dateList[11]
            skype = dateList[12]
            dataDict['skype'] = skype

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows-1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')
    out.flush()
    out.close()

# 第二种excel
def getDict2(table,out):
    out.write('[')

    for i in range(6, table.nrows):
        dateList = table.row_values(i)
        company = dateList[2]
        country = dateList[0]
        product = dateList[1]
        tel = dateList[5]
        contact = dateList[3]
        fax = dateList[6]
        address = dateList[7]
        email = dateList[4]
        website = dateList[8]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows-1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')
    out.flush()
    out.close()


# 第三种excel
def getDict3(table,out):
    out.write('[')

    for i in range(6, table.nrows):
        dateList = table.row_values(i)
        company = dateList[0]
        country = dateList[6]
        product = '家具'
        tel = dateList[2]
        contact = dateList[5]
        fax = dateList[3]
        address = dateList[4]
        email = dateList[1]
        website = dateList[7]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if(i==table.nrows-1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')

    out.flush()
    out.close()


# 第四种excel
def getDict4(table,out):
    out.write('[')

    for i in range(6, table.nrows):
        dateList = table.row_values(i)
        company = dateList[0]
        country = dateList[1]
        product = dateList[2]
        tel = dateList[4]
        contact = dateList[3]
        fax = dateList[5]
        address = dateList[7]
        email = dateList[6]
        website = dateList[8]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows-1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')
    out.flush()
    out.close()


# 第五种excel
def getDict5(table,out):
    out.write('[')

    for i in range(6, table.nrows):
        dateList = table.row_values(i)
        company = dateList[0]
        country = dateList[1]
        product = dateList[2]
        tel = dateList[3]
        contact = ''
        fax = dateList[4]
        address = dateList[5]
        email = dateList[7]
        website = dateList[6]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows-1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')
    out.flush()
    out.close()


# 第六种excel
def getDict6(table,out):
    out.write('[')

    for i in range(6, table.nrows):
        dateList = table.row_values(i)
        company = dateList[1]
        country = dateList[2]
        product = dateList[0]
        tel = dateList[6]
        contact = dateList[3]
        fax = dateList[7]
        address = dateList[4]
        email = dateList[8]
        website = dateList[9]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows-1):
            out.write(json_str)
            out.write(']')
        else:
            out.write(json_str + ',')
    out.flush()
    out.close()

# 第七种excel
def getDict7(table,out):
    out.write('[')

    for i in range(6, table.nrows):
        dateList = table.row_values(i)
        company = dateList[0]
        country = dateList[6]
        product = dateList[7]
        tel = dateList[2]
        contact = dateList[5]
        fax = dateList[3]
        address = dateList[4]
        email = dateList[1]
        website = dateList[8]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'CF','industry':industry}

        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if(i==table.nrows-1):
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
