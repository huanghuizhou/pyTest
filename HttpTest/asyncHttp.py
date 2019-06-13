from threading import Condition, Thread
import time


import logging


import requests

fail_num = 0

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



class CountDownLatch:
    def __init__(self, count):
        self.count = count
        self.condition = Condition()

    def wait(self):
        try:
            self.condition.acquire()
            while self.count > 0:
                self.condition.wait()
        finally:
            self.condition.release()

    def countDown(self):
        try:
            self.condition.acquire()
            self.count -= 1
            self.condition.notifyAll()
        finally:
            self.condition.release()




def doHttp():
    global fail_num
    s = requests.Session()
    # s.cookies['PHPSESSID'] = 'in25am0fs33u9c7ju0tt48h3t6'
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        , 'accessToken': '0467563789ae44d28623866a485dd92d'})

    try:
        url = 'http://localhost:8981/user'
        r = s.get(url)
        if r.status_code != 200:
            print('error1111111111111111111111111')
            fail_num +=1

        #html = r.text
        #soup = BeautifulSoup(html, "lxml")


    except Exception as e:
        fail_num += 1
        print("error2222222222222222222222222")


def main():
    class SubThread(Thread):
        def __init__(self, name, latch):
            Thread.__init__(self)
            self.name = name;
            self.latch = latch

        def run(self):
            doHttp()
            #time.sleep(1)
            self.latch.countDown()

    global fail_num

    print(time.time())
    a=50
    latch = CountDownLatch(a)
    print("start main thread")
    for i in range(a):
        thread1 = SubThread("thread first"+str(i), latch)
        thread1.start()
    print(time.time())
    time.sleep(5)
    latch.wait()
    print(time.time())
    print(fail_num)
    print("stop main thread")


if __name__ == '__main__':
    main()