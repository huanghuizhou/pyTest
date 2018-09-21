# import threading
# import time
# exitFlag = 0
#
#
# class myThread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         print("Starting " + self.name)
#         print_time(self.name, self.counter, 5)
#         print("Exiting " + self.name)
#
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threading.Thread.exit()
#         time.sleep(delay)
#         print("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
#
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # 开启线程
# thread1.start()
# thread2.start()
#
# print("Exiting Main Thread")


import  datetime
import time
import pymysql


# 打开数据库链接
db = pymysql.connect(host="localhost",  # 192.168.100.254
                     user="root",
                     passwd="12345678",
                     db="boss_pbc",
                     port=3306,  # 3306
                     use_unicode=True,
                     charset="utf8")

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') )
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) )

cursor=db.cursor()
sql1="""select * from test0326"""

aaa=cursor.execute(sql1)

sql_save2 = """INSERT INTO test0326\
                                 values\
                                (%s,%s,%s,%s,%s)"""

cursor.execute(sql_save2, (1,"23",3,"123",datetime.datetime.now()))
db.commit()
print("ok")
