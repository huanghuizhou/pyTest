from queue import Queue

a=None
if(not a):
    print(1111)
input_queue = Queue(10)

for i in range(1,100):
    input_queue.put(i)

    print(i)

print(111)