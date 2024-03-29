#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import threading
from concurrent import CountDownLatch
from queue import Queue, Empty
from typing import List

import pymongo
import pymysql
from pymysql.connections import Connection

MYSQL_HOST = '192.168.2.203'
MYSQL_PORT = 3306
MYSQL_USER = 'gt_user'
MYSQL_PASSWD = 'greatTao1314!@#$'

MONGO_HOST = '192.168.2.203'
MONGO_PORT = 27017
MONGO_USER = 'gt_rw'
MONGO_PASSWD = 'greattao5877'

# MYSQL_HOST = '192.168.2.203'
# MYSQL_PORT = 3308
# MYSQL_USER = 'greattao'
# MYSQL_PASSWD = 'greatTao.5877'
#
# MONGO_HOST = '192.168.2.203'
# MONGO_PORT = 27019
# MONGO_USER = 'gt_rw'
# MONGO_PASSWD = 'greattao5877'

#################################################################################
WORKER_COUNT = os.cpu_count() * 16
MONGO_DB = 'dadaoDb'
BUYERS_COLLECTION = 'Buyers'
TRADE_WOW_COLLECTION = 'TradeWow'

mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT, username=MONGO_USER, password=MONGO_PASSWD,
                                   authSource='dadaoDb',
                                   authMechanism='SCRAM-SHA-1')
input_queue = Queue(WORKER_COUNT)
# output_queue = Queue(WORKER_COUNT)
count_lock = threading.Lock()
done_thread_count = 0
data_input_done = False

# domains has MX record
with open('domain.txt') as f:
    mx_domains = set((x.strip() for x in f.readlines()))


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
                cid = input_queue.get(timeout=5)
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
        # mongo_db = mongo_client[MONGO_DB]
        collection = mongo_client[MONGO_DB][BUYERS_COLLECTION]

        try:
            doc = collection.find_one({
                '_id': cid
            }, {
                'full_name': 1,
                'emails':    1
            })
            inserted = update_customer(conn, doc['full_name'], doc['emails'])
            if inserted > 0:
                print(doc['full_name'], 'done')
            count += 1
            if count % 100 == 0:
                conn.commit()
        except Exception as e:
            # print(e, file=sys.stderr)
            continue

        # output_queue.put(ret)


def update_customer(conn: Connection, full_name: str, emails: List[str]):
    with conn.cursor() as cursor:
        cursor.execute("select id from channel_customer where company = %s", (full_name,))
        data = cursor.fetchone()
        if not data:
            # print(full_name, 'not found in channel_customer')
            return
        cid = data['id']
        cursor.execute("select email from channel_contact where customer_id = %s for update", (cid,))
        emails_in_db = [x['email'] for x in cursor.fetchall()]
        emails_to_insert = set(emails) - set(emails_in_db)
        insert_count = 0
        for email in emails_to_insert:
            if not is_valid_email(email):
                continue

            row_count = cursor.execute(
                "insert into channel_contact(customer_id, email, creater_account_id, creater, real_name, creater_source) values(%s, %s, 0, 'BOSS自建', '-', 1)",
                (cid, email)
            )
            if row_count != 1:
                print('cannot insert cid(', cid, ') email(', email, ')', file=sys.stderr)
            else:
                insert_count += 1
        return insert_count


# def is_valid_email(email: str) -> bool:
#     try:
#         # 查询DNS MX记录
#         resolver.query(email.split('@')[-1], 'MX')
#     except Exception:
#         return False
#     else:
#         return True

def is_valid_email(email: str) -> bool:
    domain = email.split('@')[-1]
    return domain and domain.lower() in mx_domains


def main():
    global data_input_done
    collection = mongo_client['dadaoDb'][BUYERS_COLLECTION]
    data = collection.find({
        'emails': {
            '$gt': []
        }
    }, {
        '_id': 1
    })

    latch = CountDownLatch(WORKER_COUNT)
    threads = [threading.Thread(target=work, args=(latch,), name='worker' + str(i), daemon=True) for i in range(WORKER_COUNT)]
    for thread in threads:
        thread.start()

    for cid in (x['_id'] for x in data):
        input_queue.put(cid)
    data_input_done = True

    # waiting for thread done
    latch.wait()


if __name__ == '__main__':
    main()
    # conn = new_mysql_conn()
    # update_customer(conn, 'Costco Wholesale Corporation', ['jsinegal@costco.com'])
