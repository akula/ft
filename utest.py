'''
b = str(rawb).lstrip('b').replace("'",'')
x, y, z,_ = b.split(',')
print(x.replace('@',''))
print(y.replace('@',''))
print(z.replace('@',''))



rawp = b'508037277@@@@@@@@@@@@@@@@@@@'
c = str(rawp).lstrip('b').replace("'",'').replace('@','')
print(c)


msg = '508037285.OKT22222,508037296.NGT21212,---,---,---c@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

si = msg.replace('@','').split(',')
for s in si:
    if (s.startswith('---')):
        s = ''
    print(s)
'''


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

clientstring = socket.gethostbyname(socket.gethostname())
_, _, _,client = clientstring.split('.') 

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
  

def parse_check(response):
    '''
    check 
    '''
    global g_check_msg
    global g_cover_msg
    res = response
    data = res[30:]
    check_starttime = parse_stime(data[0:6].hex())
    check_qty = int(data[6:8].hex(),16)
    check_ng = int(data[8:10].hex(), 16)
    check_endtime = parse_stime(data[10:16].hex())
    check_code = data[16:18].hex()
    check_id = data[18:38]
    check_id = str(check_id).lstrip('b').replace("'",'').replace('@','').replace(',','')
    check_sn = data[38:64]
    check_sn = str(check_sn).lstrip('b').replace("'",'').replace('@','').replace(',','')
    cover_starttime = parse_stime(data[64:70].hex())
    cover_qty = int(data[70:72].hex(),16)
    cover_endtime = parse_stime(data[72:78].hex())
    cover_id = data[78:138]
    cover_id = str(cover_id).lstrip('b').replace("'",'').replace('@','').replace(',','')
    cover_id = ''.join(filter(lambda x: x in printable, cover_id))
    check_msg = data[0:64]
    cover_msg = data[64:]

    print('check ok')
    print('---check_sn---')
    print(check_sn)
    print('---check id---')
    print(check_id)
    print('---check starttime---')
    print('check_starttime')
    print(check_starttime)
    print('check_endtime')
    print(check_endtime)



    if check_msg != g_check_msg:
        g_check_msg = check_msg
        logger.info('get check_msg')
        check_start = datetime.datetime.strptime(str(check_starttime), "%y%m%d%H%M%S")
        print(check_endtime)
        check_end = datetime.datetime.strptime(str(check_endtime), "%y%m%d%H%M%S")
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            logger.info('product_id: '  + check_id )
            logger.info('sn: ' + check_sn )
            logger.info('check_code: ' + check_code)
            logger.info('starttime: ' + check_start)
            logger.info('endtime: ' + check_end)
            c.execute("""insert into checks (product_id, sn, check_code, qty,ng, starttime, endtime ) values (%s, %s, %s, %s,%s, %s,%s) """, ( check_id,  check_sn, check_code, check_qty, check_ng, check_start, check_end ))
            db.commit()
        except Exception as e:
            print(e)

        finally:
            db.close()
    else:
        logger.info('drop check_msg')
    
    if cover_msg != g_cover_msg:
        g_cover_msg = cover_msg
        logger.info('get cover_msg')
        cover_start = datetime.datetime.strptime(str(cover_starttime), "%y%m%d%H%M%S")
        cover_end = datetime.datetime.strptime(str(cover_endtime), "%y%m%d%H%M%S")
        print(cover_start)
        print(cover_end)
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            print(cover_start)
            print(cover_end)
            c.execute("""insert into cover (product_id,  qty, starttime, endtime ) values (%s, %s,  %s,%s) """, ( cover_id,   cover_qty,  cover_start, cover_end ))
            db.commit()
        except Exception as e:
            print(e)    
        finally:
            db.close()
    else:
        logger.info('drop cover_msg')


def get_check():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:   
        sock.connect(('192.168.250.16',9600))
        sock.send(finsconn(int(client)))
        fresp = sock.recv(1024)
        req = requestframe(16, int(client), 8000,108)
        while True:
            sock.send(req)
            resp = sock.recv(8192)
            parse_check(resp)
            sleep(10)
    except Exception:
        logger.exception("----------Fatal error in get_check-------------")
    finally:
        sock.close()  


if __name__ == '__main__' :
    get_check()



    



