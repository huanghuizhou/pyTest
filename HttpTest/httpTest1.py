#!/usr/bin/env python3
# coding=utf-8

import logging
import os
import sys

import requests
from bs4 import BeautifulSoup


# sys.path.append(os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/..'))


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
    # s.cookies['PHPSESSID'] = 'in25am0fs33u9c7ju0tt48h3t6'
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        , 'accessToken': '0467563789ae44d28623866a485dd92d'})

    try:
        url = 'http://localhost:8981/user'
        r = s.get(url)
        if r.status_code != 200:
            print('code error')
        html = r.text
        soup = BeautifulSoup(html, "lxml")


    except Exception as e:
        logger.error("line")
        logger.error("{} can not get info")
        print(" can not get info")


# !/usr/bin/env python3
# coding=utf-8
import os
import sys
import threading
from concurrent import CountDownLatch
from queue import Queue, Empty

WORKER_COUNT = 100

count_lock = threading.Lock()


def work(latch: CountDownLatch):
   print(1111)
   latch.count_down()


def main():
    global data_input_done
    latch = CountDownLatch(WORKER_COUNT)
    threads = [threading.Thread(target=work, args=(latch,), name='worker' + str(i), daemon=True) for i in
               range(WORKER_COUNT)]
    for thread in threads:
        thread.start()

    data_input_done = True
    # waiting for thread done
    latch.wait()
    print("11111111111111111111111")


if __name__ == '__main__':
    main()
