import json

dataOpen = open('./country.json')
dataList = json.loads(dataOpen.read())
countryDict = {}
for data in dataList:
    countryDict[data['Name_zh']] = data['_id']
countryEnDict = {}
for data in dataList:
    countryEnDict[data['Name_en']] = data['_id']
def getCountry(country):

    if country.find('中国')!=-1:
        country='中国'

    if is_ustr(country) in countryDict:
        return countryDict[is_ustr(country)]

    if country in countryEnDict:
        return countryEnDict[country]

    return ''


def is_ustr(in_str):
    out_str=''
    for i in range(len(in_str)):
        if is_uchar(in_str[i]):
            out_str=out_str+in_str[i]
        else:
            out_str=out_str+''
    return out_str

#去除中文外字符
def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
    return False


aaa=getCountry('加   拿   大.')
print(aaa)