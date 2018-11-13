#!/usr/bin/env python3
# coding=utf-8
import json
import logging
import os
import sys
import threading
import time
from concurrent import CountDownLatch
from queue import Queue, Empty

import pymysql
from dns import resolver
from pymysql.connections import Connection

# MYSQL_HOST = '192.168.2.203'
# MYSQL_PORT = 3306
# MYSQL_USER = 'gt_user'
# MYSQL_PASSWD = 'greatTao1314!@#$'


# stage
# MYSQL_HOST = '192.168.2.203'
# MYSQL_PORT = 3308
# MYSQL_USER = 'greattao'
# MYSQL_PASSWD = 'greatTao.5877'
#
# dev
# MYSQL_HOST = '192.168.2.203'
# MYSQL_USER = 'greatTao'
# MYSQL_PASSWD = 'greatTao.1314'
# MYSQL_PORT = 3306


MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_PORT = 3306

#################################################################################
WORKER_COUNT = os.cpu_count() * 16

input_queue = Queue(WORKER_COUNT)
# output_queue = Queue(WORKER_COUNT)
count_lock = threading.Lock()
done_thread_count = 0
data_input_done = False


# domains has MX record
# with open('domain.txt') as f:
#     mx_domains = set((x.strip() for x in f.readlines()))


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

def new_mysql_conn() -> Connection:
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWD,
        db='gttown_crm',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def work(latch: CountDownLatch):
    global done_thread_count
    conn = new_mysql_conn()

    count = 0
    while True:
        while True:
            try:
                data = input_queue.get(timeout=5)
            except Empty:
                if data_input_done:
                    with count_lock:
                        done_thread_count += 1

                    conn.commit()
                    conn.close()
                    latch.count_down()
                    print('[worker thread', threading.current_thread().name, 'done]')
                    return
                else:
                    continue
            else:
                break

        try:

            insertMysql(conn, data)
            count += 1
            if count % 50 == 0:
                conn.commit()
                print("commit count is", count)
        except Exception as e:
            print(data, e, file=sys.stderr)
            continue

        # output_queue.put(ret)


def main():
    global data_input_done

    latch = CountDownLatch(WORKER_COUNT)
    threads = [threading.Thread(target=work, args=(latch,), name='worker' + str(i), daemon=True) for i in
               range(WORKER_COUNT)]
    for thread in threads:
        thread.start()

    fileName = './data.json'
    dataOpen = open(fileName)
    dataList = json.loads(dataOpen.read())
    for data in dataList:
        input_queue.put(data)
    data_input_done = True

    # waiting for thread done
    latch.wait()


def insertMysql(db, data):
    company = ''
    if 'company' in data:
        company = data['company']

    if (company.strip() == ''):
        return

    address = ''
    if 'address' in data:
        address = data['address']

    country = ''
    if 'country' in data:
        country = data['country']

    tel = ''
    if 'tel' in data:
        tel = data['tel']
        if (len(str(tel)) > 20):
            tel = tel[0:20]

    fax = ''
    if 'fax' in data:
        fax = data['fax']

    email = ''
    if 'email' in data:
        email = data['email']

    email_status = 0
    if (email != ''):
        if (is_valid_email(email)):
            email_status = 1
        else:
            email_status = 2

    website = ''
    if 'website' in data:
        website = data['website']
        if (len(str(website)) > 50 or website == 'N.A.' or website == 'n/a'):
            website = ''

    contact = '-'
    if 'contact' in data:
        contact = data['contact']
        if contact == 'N.A.':
            contact = '-'

    position = ''
    if 'position' in data:
        position = data['position']

    products = ''
    if 'products' in data:
        products = data['products']

    skype = ''
    if 'skype' in data:
        skype = data['skype']

    requirement_remark = ''
    if 'requirement_remark' in data:
        requirement_remark = data['requirement_remark']

    industry = ''
    if 'industry' in data:
        industry = data['industry']

    extra_data = ''
    if 'extra_data' in data:
        extra_data = json.dumps(data['extra_data'])

    sql1 = """INSERT INTO channel_customer (company,country,address,company_website,contact_name,requirement_remark,extra_data,origin,last_update_time,audit_status,distribute_status,account_distribute_status,status,type,role,industry) value(%s,%s,%s,%s,%s,%s,%s,4,now(),2,1,1,1,1,1,%s)"""
    sql2 = """INSERT INTO channel_contact  (customer_id,email,fax,telephone_number,position,email_status,skype) value(%s,%s,%s,%s,%s,%s,%s)"""
    sql3 = """INSERT INTO channel_product  (customer_id,product_content) value(%s,%s)"""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql1,
                           (company, getCountry(country), address, website, contact, requirement_remark, extra_data,
                            industry))
            id = cursor.lastrowid
            cursor.execute(sql2,
                           (id, email, fax, tel, position, email_status, skype))
            for product in products:
                cursor.execute(sql3, (id, product))
            print(id, 'inserted')
    except Exception as e:
        logger.warning('Failed to insert  %s' % data, e)
        time.sleep(2)


def is_valid_email(email: str) -> bool:
    try:
        # 查询DNS MX记录
        resolver.query(email.split('@')[-1], 'MX')
        # return True
    except Exception:
        return False
    else:
        return True


dataOpen = open('./country.json')
dataList = json.loads(dataOpen.read())
countryDict = {}
for data in dataList:
    countryDict[data['Name_zh']] = data['_id']
countryEnDict = {}
for data in dataList:
    countryEnDict[data['Name_en']] = data['_id']


def getCountry(country):
    if country in countryEnDict:
        return countryEnDict[country]

    if country.replace(' ', '').find('香港') != -1 or country.find('Hong Kong') != -1:
        return "HK"

    if country.replace(' ', '').find('澳门') != -1:
        return "MO"

    if country.replace(' ', '').find('台湾') != -1 or country.find('Taiwan') != -1:
        return "TW"

    if is_ustr(country.replace(' ', '')) in countryDict:
        return countryDict[is_ustr(country)]

    return ''


def is_ustr(in_str):
    out_str = ''
    for i in range(len(in_str)):
        if is_uchar(in_str[i]):
            out_str = out_str + in_str[i]
        else:
            out_str = out_str + ''
    return out_str


# 去除中文外字符
def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    return False


if __name__ == '__main__':
    print(time.localtime())
    main()
    # conn = new_mysql_conn()
    # update_customer(conn, 'Costco Wholesale Corporation', ['jsinegal@costco.com'])
