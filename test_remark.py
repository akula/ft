
# FINS connection response parse, the response suppose to be bytearray
from fins_utils import commandflg
import MySQLdb
import datetime
import re
from string import printable
import logging
debug_flg = 0
import socket
from tcpclient import *
import logging
from time import sleep

g_pre_assembly_msg = b''
g_scan_code_msg = b''
g_up_shell_msg = b''
g_readid_msg = b''
g_screw_msg = b''
g_firstmat_msg = b''
g_repeattest_msg = b''
g_ccd_msg = b''
g_sample_msg  = b''
g_secmat_msg = b''
g_remark_msg = b''
g_check_msg = b''
g_cover_msg = b''


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='info.log', level=logging.INFO)
clientstring = socket.gethostbyname(socket.gethostname())
_, _, _,client = clientstring.split('.') 

def parse_time(ts):
    starttime = ts[8:12] + ts[4:8]  + ts[0:4]
    endtime = ts[20:24] + ts[16:20] + ts[12:16]
    return (starttime, endtime)

def parse_stime(ts):
    time = ts[8:12] + ts[4:8]  + ts[0:4]
    return time

def parse_res(response):
    client, serv = response[-5], response[-1]
    return (client, serv)



def parse_remark(response):
    global g_remark_msg
    res = response
    data = res[30:]
    starttime = parse_stime(data[0:6].hex())
    qty = int(data[6:8].hex(),16)
    endtime = parse_stime(data[8:14].hex())
    id_iccid = data[14:134]
    id_iccid = str(id_iccid).lstrip('b').replace("'",'').replace('@','')
    product_id, iccid , _ = id_iccid.split(',')


    remark_msg = res[30:]

    if remark_msg != g_remark_msg:
        g_remark_msg = remark_msg

        start = datetime.datetime.strptime(str(starttime), "%y%m%d%H%M%S")
        end = datetime.datetime.strptime(str(endtime), "%y%m%d%H%M%S")
    
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into remark (product_id, iccid, qty, starttime, endtime ) values (%s, %s, %s, %s,%s) """, ( product_id,  iccid, qty,  start, end ))
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()

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


if __name__ == '__main__':
    resp = get_remark()
    parse_remark(resp)




