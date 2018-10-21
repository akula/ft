
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

clientstring = socket.gethostbyname(socket.gethostname())
_, _, _,client = clientstring.split('.') 

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='info.log', level=logging.INFO)


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


def parse_screw(response):
    '''
    '''
    global g_screw_msg
    global g_firstmat_msg
    res = response 
    data = res[30:]
    time_ts = data[0:12].hex()
    screw_qty = int(data[12:14].hex(),16)
    firstmat_ts = data[14:26].hex()
    firstmat_qty = int(data[26:28].hex(),16)
    firstmat_ng = int(data[28:30].hex(),16)
    firstmat_id = data[30:60]
    firstmat_id = str(firstmat_id).lstrip('b').replace("'",'').replace('@','').replace(',','')

    screw_starttime, screw_endtime = parse_time(time_ts)
    first_starttime, first_endtime = parse_time(firstmat_ts)

    screw_msg = data[0:14]
    firstmat_msg = data[14:60]

    if screw_msg != g_screw_msg:
        g_screw_msg = screw_msg
        logger.info('get screw_msg')
        screw_start = datetime.datetime.strptime(str(screw_starttime), "%y%m%d%H%M%S")
        screw_end = datetime.datetime.strptime(str(screw_endtime), "%y%m%d%H%M%S")
        
        try:
            logger.info('screw_starttime: ' + screw_starttime)
            logger.info('screw_endtime: ' + screw_endtime)
            logger.info('screw_qty: ' + str(screw_qty) )
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into screw ( qty,  starttime, endtime ) values (%s, %s, %s) """, ( screw_qty,  screw_start, screw_end ))
            db.commit()
        except Exception as e:
            print(e)
        finally:    
            db.close()
    else:
        logger.info('drop screw_msg')

    if firstmat_msg != g_firstmat_msg:
        g_firstmat_msg = firstmat_msg
        logger.info('get firstmat_msg')
        firstmat_start = datetime.datetime.strptime(str(first_starttime), "%y%m%d%H%M%S")
        firstmat_end = datetime.datetime.strptime(str(first_endtime), "%y%m%d%H%M%S")
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into firstmat (product_id, qty, ng, starttime, endtime ) values (%s, %s, %s, %s,%s) """, ( firstmat_id, firstmat_qty, firstmat_ng, firstmat_start, firstmat_end ))
            db.commit()
        except Exception as e :
            print(e)
        finally:
            db.close()
    else:
        logger.info('drop firstmat_msg')




def get_screw():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.12',9600))
        sock.send(finsconn(int(client)))
        fresp = sock.recv(1024)
        req = requestframe(12, int(client), 8000,60)
        while True:
            sock.send(req)
            resp = sock.recv(8192)
            parse_screw(resp)
            sleep(10)
    except Exception :
        logger.exception("---------------Fatal error in get_screw------------")
    finally:
        sock.close()


if __name__ == '__main__':
    get_screw()
