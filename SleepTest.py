import os
import time

a = 1
while (True):
    a += 1
    print(a)
    # os.mkdir("G:/aaa/asdadsa2")
    time.sleep(1)
    os.mkdir("G:/aaa/asdadsa" + str(a))