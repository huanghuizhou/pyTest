import json
import os

import xlrd

fileOutName = './json/'
fileinName = './土耳其家居'
os.mkdir(fileOutName + "土耳其家居")

# 行业
industry = 0



def getXlsFile():
    xlslist = os.listdir(fileinName)
    xlslist.reverse()

    for i in range(0, len(xlslist)):
        xlsPath = os.path.join(fileinName, xlslist[i])
        xlsFile = xlrd.open_workbook(xlsPath)
        exportJson(xlsFile, xlsPath)

        print("_____________________________________________________")


def exportJson(xlsFile, xlsPath):
    out = open(fileOutName + xlsPath.replace('xlsx', 'json').replace('xls', 'json').replace('./', ''), 'w')

    global industry
    #家居
    industry = 28
    table = xlsFile.sheets()[0]
    getDict(table, out)


def getDict(table,out):

    out.write('[')
    for i in range(3,table.nrows):
        dateList = table.row_values(i)
        company = dateList[2]

        if company.replace(' ','')=='':
            continue
        country = dateList[1]
        product = dateList[8]
        tel = dateList[6]
        contact = dateList[3]
        fax = ''
        address = ''
        email = dateList[5]
        position= dateList[4]


        website = dateList[7]

        dataDict = {'company': company, 'country': country, 'product': product, 'tel': str(tel).replace('.0',''), 'contact': contact, 'position': position,
                    'fax': str(fax).replace('.0',''), 'address': address, 'email': email, 'website': website,'requirement_remark':'TK','industry':industry}


        json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
        if (i == table.nrows-1):
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
