from threading import Thread
from time import sleep
from socket import *


def connect(serv, msg):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((serv, 20000))
        s.send(msg)
        rmsg = s.recv(8192)
        print(rmsg)
    except Exception:
        raise(Exception)
    finally:
        s.close()

def query_NO2():
    while True:
        connect('127.0.0.1', b'I am NO 10 and sleep 10')
        sleep(10)


def query_NO5():
    while True:
        connect('127.0.0.1', b'I am NO 5 and sleep 5')
        sleep(5)


def query_NO3():
    while True:
        connect('127.0.0.1', b'I am NO 3 and sleep 20')
        sleep(20)


if __name__ == '__main__':
    t1 = Thread(target=query_NO2)
    t2 = Thread(target=query_NO3)
    t3 = Thread(target=query_NO5)
    t2.start()
    t1.start()
    t3.start()

