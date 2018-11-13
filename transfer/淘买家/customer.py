#!/usr/bin/env python3
# coding=utf-8
import json
import os
import sys
import threading
import time
from queue import Queue, Empty
from typing import TextIO

import pymongo
import pymysql
from dns import resolver
from pymongo.database import Database
from pymysql.connections import Connection
from pymysql.cursors import Cursor

# MYSQL_HOST = '192.168.2.203'
# MYSQL_PORT = 3306
# MYSQL_USER = 'gt_user'
# MYSQL_PASSWD = 'greatTao1314!@#$'
#
# MONGO_HOST = '192.168.2.203'
# MONGO_PORT = 27017
# MONGO_USER = 'gt_rw'
# MONGO_PASSWD = 'greattao5877'

MYSQL_HOST = '192.168.2.203'
MYSQL_PORT = 3308
MYSQL_USER = 'greattao'
MYSQL_PASSWD = 'greatTao.5877'

MONGO_HOST = '192.168.2.203'
MONGO_PORT = 27019
MONGO_USER = 'gt_rw'
MONGO_PASSWD = 'greattao5877'

#################################################################################
WORKER_COUNT = os.cpu_count() * 16
BUYERS_COLLECTION = 'Buyers'
TRADE_WOW_COLLECTION = 'TradeWow'

mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT, username=MONGO_USER, password=MONGO_PASSWD,
                                   authSource='dadaoDb',
                                   authMechanism='SCRAM-SHA-1')
input_queue = Queue(WORKER_COUNT)
output_queue = Queue(WORKER_COUNT)
count_lock = threading.Lock()
done_thread_count = 0
data_input_done = False


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


def work():
    global done_thread_count
    conn = new_mysql_conn()

    while True:
        while True:
            try:
                cid = input_queue.get(timeout=5)
            except Empty:
                if data_input_done:
                    with count_lock:
                        done_thread_count += 1
                    conn.close()
                    return
                else:
                    continue
            else:
                break
        mongo_db = mongo_client['dadaoDb']

        with conn.cursor() as my_cursor:
            try:
                ret = fetch_data(cid, my_cursor, mongo_db)
                if not ret:
                    continue
            except Exception as e:
                print(e, file=sys.stderr)
                continue

        output_queue.put(ret)


def fetch_data(cid: int, my_cursor: Cursor, mongo_db: Database):
    ret = {}
    # customer
    my_cursor.execute("select * from channel_customer where id = %s", cid)
    customer = my_cursor.fetchone()
    if not customer:
        return None
    name = customer['company']
    my_cursor.execute("select * from channel_contact where customer_id = %s limit 1", cid)

    # email
    contact = my_cursor.fetchone()
    buyer_in_mongo = None
    if contact:
        email = contact['email']
    else:
        email = None
    if not email:
        collection = mongo_db[BUYERS_COLLECTION]
        buyer_in_mongo = collection.find_one({'full_name': name})
        email = fetch_email_from_mongo(mongo_db, buyer_in_mongo)
        if not email:
            return None

    # product
    my_cursor.execute("select product_content from channel_product where customer_id = %s", cid)
    db_products = my_cursor.fetchall()
    if db_products:
        products = [x['product_content'] for x in db_products]
    else:
        if not buyer_in_mongo:
            collection = mongo_db[BUYERS_COLLECTION]
            buyer_in_mongo = collection.find_one({'full_name': name})
        if buyer_in_mongo:
            products = fetch_products_from_mongo(mongo_db, buyer_in_mongo)
        else:
            products = None
    ret['customer_id'] = customer['id']
    ret['country'] = customer['country']
    ret['name'] = name
    ret['industry'] = customer['industry']
    ret['email'] = email
    ret['flag6c_grade'] = customer['flag6c_grade']
    if products:
        products = list(set(products))
    elif products is None:
        products = []
    ret['products'] = products
    ret['today_max'] = 0
    ret['life_max'] = 0
    ret['replied'] = 0
    ret['unsubscribe'] = 0
    ret['email_valid'] = 0
    return ret


def fetch_products_from_mongo(mongo_db: Database, buyer_in_mongo: dict):
    name = buyer_in_mongo['name']
    collection = mongo_db[TRADE_WOW_COLLECTION]
    products = collection.find({'consigneeName': name}, {'productDesc': 1})
    return [x['productDesc'] for x in products]


def fetch_email_from_mongo(mongo_db: Database, buyer_in_mongo: dict):
    email = None
    if not (buyer_in_mongo and 'emails' in buyer_in_mongo and len(buyer_in_mongo['emails']) > 0):
        return None
    for email in buyer_in_mongo['emails']:
        if not email:
            continue
        try:
            # 查询DNS MX记录
            resolver.query(email.split('@')[-1], 'MX')
        except Exception:
            continue
        else:
            break
    return email


def data_writer(out: TextIO):
    while True:
        data = output_queue.get()
        print("id(%d) done" % data['customer_id'])
        out.write(json.dumps(data, ensure_ascii=False))
        out.write(",\n")


def main():
    global data_input_done
    conn = new_mysql_conn()
    with conn.cursor() as id_cursor:
        id_cursor.execute('select id from channel_customer where role = 1')
        cids = [x['id'] for x in id_cursor.fetchall()]
    conn.close()

    out_file = open('data.json', 'w')
    out_file.write("[\n")

    threads = [threading.Thread(target=work, name='worker' + str(i), daemon=True) for i in range(WORKER_COUNT)]
    threads.append(threading.Thread(target=data_writer, args=(out_file,), name="data_writer", daemon=True))
    for thread in threads:
        thread.start()

    for cid in cids:
        input_queue.put(cid)
    data_input_done = True
    while done_thread_count != WORKER_COUNT:
        print('waiting for thread done(%d/%d)' % (done_thread_count, WORKER_COUNT))
        time.sleep(5)

    out_file.write("]")
    out_file.flush()
    out_file.close()


if __name__ == '__main__':
    main()
    # data = work(343344, conn.cursor(), mongo_client['dadaoDb'])
    # print(data)
