import socket
from tcpclient import *
import logging

clientstring = socket.gethostbyname(socket.gethostname())
_, _, _,client = clientstring.split('.') 

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='error.log', level=logging.INFO)



def get_firsttest():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.11',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        req = requestframe(11, int(client), 8000,216)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception:
        logger.exception("-----------Fatal error in get_firsttest--------")
    finally:
        sock.close()
    return resp


def get_upassemly():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.10',9600))
        sock.send(finsconn(int(client)))
        fresp = sock.recv(1024)
        logger.info(fresp + b'  @@get_upassemly@@  ')
        req = requestframe(10, int(client), 8000, 182)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception :
        logger.exception("--------Fatal error in get_upassemly-------------")
    finally:
        sock.close()
    return resp


def get_screw():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.12',9600))
        sock.send(finsconn(int(client)))
        fresp = sock.recv(1024)
        logger.info(fresp + b'  @@get_screw  ')
        req = requestframe(12, int(client), 8000,60)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception :
        logger.exception("---------------Fatal error in get_screw------------")
    finally:
        sock.close()
    return resp


def get_repeattest():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.13',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(13, int(client), 8000,216)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception:
        logger.exception("--------Fatal error in get_repeattest---------------")
    finally:
        sock.close()
    return resp


def get_ccd():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.14',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(14, int(client), 8000,170)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception:
        logger.exception("----------Fatal error in get_ccd-----------------")
    finally:
        sock.close()
    return resp


def get_remark():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.15', 9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(15, int(client), 8000, 72)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception :
        logger.exception("----------Fatal error in get_remark-------------")
    finally:
        sock.close()
    return resp


def get_check():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.16',9600))
        sock.send(finsconn(int(client)))
        fresp = sock.recv(1024)
        logger.info(fresp + b'  @@get_check@@')
        req = requestframe(16, int(client), 8000,108)
        sock.send(req)
        resp = sock.recv(8192)
    except Exception:
        logger.exception("----------Fatal error in get_check-------------")
    finally:
        sock.close()
    return resp