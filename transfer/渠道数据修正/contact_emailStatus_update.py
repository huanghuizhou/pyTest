#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import threading
from concurrent import CountDownLatch
from queue import Queue, Empty

import pymysql
from dns import resolver
from pymysql.connections import Connection

# MYSQL_HOST = '192.168.2.203'
# MYSQL_PORT = 3306
# MYSQL_USER = 'gt_user'
# MYSQL_PASSWD = 'greatTao1314!@#$'
#


MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'


#################################################################################
WORKER_COUNT = os.cpu_count() * 16



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

        try:

            inserted = update_contact(conn, cid['id'])
            if inserted > 0:
                print(cid['id'], 'done')
            count += 1
            if count % 100 == 0:
                conn.commit()
                print("commit count is",count)
        except Exception as e:
            #print(e)
            print(e, file=sys.stderr)
            continue

        # output_queue.put(ret)


def update_contact(conn: Connection, cid):

    with conn.cursor() as cursor:
        cursor.execute("select email from channel_contact where id=%s", cid)
        data = cursor.fetchone()
        if not data:
            print(cid, 'not found in channel_contact')
            return

        #邮箱验证通过
        if(is_valid_email(data['email'])):
            row_count =cursor.execute("UPDATE channel_contact set email_status=1 where id=%s", cid)
        else:
            row_count =cursor.execute("UPDATE channel_contact set email_status=2 where id=%s", cid)

        insert_count=0
        if row_count != 1:
            print('cannot updtae email_status(', data['email'], ') id(', cid, ')')
        else:
            insert_count += 1
        return insert_count


def is_valid_email(email: str)-> bool:
    try:
        # 查询DNS MX记录
        resolver.query(email.split('@')[-1], 'MX')
        #return True
    except Exception as e:
        return False
    else:
        return True


def main():
    global data_input_done
    conn = new_mysql_conn()
    with conn.cursor() as cursor:
        cursor.execute("select id from channel_contact where email_status=0 or email_status is null")
        cids = cursor.fetchall()
    conn.commit()
    conn.close()
    latch = CountDownLatch(WORKER_COUNT)
    threads = [threading.Thread(target=work, args=(latch,), name='worker' + str(i), daemon=True) for i in range(WORKER_COUNT)]
    for thread in threads:
        thread.start()

    print(len(cids))
    for cid in cids:
        input_queue.put(cid)
    data_input_done = True

    # waiting for thread done
    latch.wait()


if __name__ == '__main__':
    main()
    # conn = new_mysql_conn()
    # update_customer(conn, 'Costco Wholesale Corporation', ['jsinegal@costco.com'])
