#!/usr/bin/env python3
# coding=utf-8

import logging
import os
import sys

import requests
from bs4 import BeautifulSoup

#sys.path.append(os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/..'))


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


def doHttp():
    s = requests.Session()
    #s.cookies['PHPSESSID'] = 'in25am0fs33u9c7ju0tt48h3t6'
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    ,'accessToken':'0467563789ae44d28623866a485dd92d'})

    try:
        url = 'http://localhost:8981/user'
        r = s.get(url)
        if r.status_code != 200:
            print('code error')
        html = r.text
        soup = BeautifulSoup(html, "lxml")


    except Exception as e:
        logger.error("line" )
        logger.error("{} can not get info")
        print( " can not get info")





#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import threading
from concurrent import CountDownLatch
from queue import Queue, Empty


WORKER_COUNT = 10



input_queue = Queue(2)
count_lock = threading.Lock()
done_thread_count = 0
data_input_done = False


def work(latch: CountDownLatch):
    global done_thread_count
    while True:
        while True:
            try:
                cid = input_queue.get(timeout=5)
                print(cid,end="\n")
            except Empty:
                if data_input_done:
                    with count_lock:
                        done_thread_count += 1
                    latch.count_down()
                    print('[worker thread', threading.current_thread().name, 'done]')
                    return
                else:
                    continue
            else:
                break

        #print('[worker thread', threading.current_thread().name, 'doing]')


def main():
    global data_input_done
    latch = CountDownLatch(WORKER_COUNT)
    threads = [threading.Thread(target=work, args=(latch,), name='worker' + str(i), daemon=True) for i in range(WORKER_COUNT)]
    for thread in threads:
        thread.start()

    cids=[1,2,3,4,5,6,9,1]
    #print(len(cids))
    for cid in cids:
        input_queue.put(cid)
    data_input_done=True
    # waiting for thread done
    latch.wait()
    print("11111111111111111111111")

if __name__ == '__main__':
    main()
