import socket
from threading import Thread

dstIp = ""
dstPort = 0
udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
def recvdata():
    global udpSocket
    while True:
        recvinfo = updSocket.recvfrom(1024)
        print(">>%s,%s \n>>" %(str(recvinfo[1]),recvinfo[0]))

def senddata():
    global udpSocket
    while True:
        sendinfo = raw_input("<<")
        udpSocket.sendto(sendinfo.encode(GB3212),(dstIp,dstPort))

#udpSocket = None

def main():
    global udpSocket
    global dstIp
    global dstPort
    dstIp = raw_input("IP:")
    dstPort = int(raw_input("PORT:"))
    udpSocket.bind(('',65521))
    tr = Thread(target=recvdata)
    ts = Thread(target=senddata)

    tr.start()
    ts.start()

    tr.join()
    ts.join()
if __name__ == '__main__':
    main()
