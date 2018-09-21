import os
import shutil
a = 1
while (True):

    a += 1
    my_file = 'G:/aaa/asdadsa'+str(a)
    if os.path.exists(my_file):
        shutil.rmtree("G:/aaa/asdadsa"+str(a))
        print(a)

