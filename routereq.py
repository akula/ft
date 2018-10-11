import socket
from tcpclient import *

clientstring = socket.gethostbyname(socket.gethostname())
_, _, _,client = clientstring.split('.') 



def get_firsttest():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.11',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(11, int(client), 8000,216)
        sock.send(req)
        resp = sock.recv(8192)
        
    finally:
        sock.close()
    return resp

def get_upassemly():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.10',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        print(resp)
        req = requestframe(10, int(client), 8000,182)
        sock.send(req)
        resp = sock.recv(8192)
        
    finally:
        sock.close()
    return resp


def get_screw():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.12',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(12, int(client), 8000,60)
        sock.send(req)
        resp = sock.recv(8192)
        
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
        
    finally:
        sock.close()
    return resp


def get_remark():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.15',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(15, int(client), 8000,72)
        sock.send(req)
        resp = sock.recv(8192)
        
    finally:
        sock.close()
    return resp

def get_check():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.16',9600))
        sock.send(finsconn(int(client)))
        resp = sock.recv(1024)
        
        req = requestframe(16, int(client), 8000,108)
        sock.send(req)
        resp = sock.recv(8192)
        
    finally:
        sock.close()
    return resp