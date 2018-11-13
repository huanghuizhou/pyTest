import json
import logging
import time

import pymysql

# DB_HOST = '192.168.2.203'
# DB_USER = 'greatTao'
# DB_PASSWD = 'greatTao.1314'
# DB_PORT = 3306

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = '123456'
DB_PORT = 3306
gttown_crm_db = pymysql.connect(host=DB_HOST,  # 192.168.100.254
                                          user=DB_USER,
                                          passwd=DB_PASSWD,
                                          db="gttown_crm",
                                          port=DB_PORT,  # 3306
                                          use_unicode=True,
                                          charset="utf8")


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

def insertMysql(data):


    company=data['company']

    address=''
    if 'address' in data:
        address=data['address']

    country=''
    if 'country' in data:
        country=data['country']

    tel=''
    if 'tel' in data:
        tel=data['tel']

    fax=''
    if 'fax' in data:
        fax=data['fax']

    email=''
    if 'email' in data:
        email=data['email']

    email_status=0
    if(email !=''):
        if (is_valid_email(email)):
            email_status=1
        else:
            email_status=2



    website=''
    if 'website' in data:
        website=data['website']

    contact='-'
    if 'contact' in data:
        contact=data['contact']

    position=''
    if 'position' in data:
        position=data['position']

    product=''
    if 'product' in data:
        product=data['product']

    skype = ''
    if 'skype' in data:
        skype = data['skype']

    requirement_remark = ''
    if 'requirement_remark' in data:
        requirement_remark = data['requirement_remark']

    industry = ''
    if 'industry' in data:
        industry = data['industry']


    sql1 = """INSERT INTO channel_customer (company,country,address,company_website,contact_name,requirement_remark,origin,last_update_time,audit_status,distribute_status,account_distribute_status,status,type,role,industry) value(%s,%s,%s,%s,%s,%s,4,now(),2,1,1,1,1,1,%s)"""
    sql2 = """INSERT INTO channel_contact  (customer_id,email,fax,telephone_number,position,email_status,skype) value(%s,%s,%s,%s,%s,%s,%s)"""
    sql3 = """INSERT INTO channel_product  (customer_id,product_content) value(%s,%s)"""
    try:
        cursor = gttown_crm_db.cursor()
        cursor.execute(sql1,
                       (company,getCountry(country),address,website,contact,requirement_remark,industry))
        id =cursor.lastrowid
        cursor.execute(sql2,
                       (id,email, fax, tel, position,email_status,skype))
        cursor.execute(sql3,
                       (id,product))
        gttown_crm_db.commit()
    except Exception as e:
        logger.warning('Failed to insert company %s' % company, e)
        time.sleep(2)



def is_valid_email(email: str)-> bool:
    try:
        # 查询DNS MX记录
        #resolver.query(email.split('@')[-1], 'MX')
        return True
    except Exception:
        return False
    else:
        return True


def doExportDate(jsonPath):
    dataOpen=open(jsonPath)
    dataList = json.loads(dataOpen.read())
    for data in dataList:
        insertMysql(data)



    logger.info(jsonPath+"insert success")



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


def main():
    fileName='./allJson2.json'
    doExportDate(fileName)
    logger.info("export success")



if __name__ == '__main__':
    main()
