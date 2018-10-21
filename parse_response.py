# FINS connection response parse, the response suppose to be bytearray
from fins_utils import commandflg
import MySQLdb
import datetime
import re
from string import printable
import logging
debug_flg = 0

g_pre_assembly_msg = b''
g_scan_code_msg = b''
g_up_shell_msg = b''
g_readid_msg = b''
g_firsttest_msg = b''
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


def parse_upassemly(response):
    '''
    The 10 PLC parse message
    '''
    global g_pre_assembly_msg
    global g_scan_code_msg
    global g_up_shell_msg
    global g_readid_msg
    global logger

    resp = response
    data = resp[30:]
    pre_ts = data[0:12].hex()
    pre_qty = int(data[12:14].hex(),16)
    scan_ts = data[14:26].hex()
    scan_qty = int(data[26:28].hex(),16)
    scan_ng = int(data[28:30].hex(),16)
    scan_msg = data[30:120].replace(b'\r',b'')
    shell_ts = data[120:132].hex()
    shell_qty = int(data[132:134].hex(), 16)
    read_ts = data[134:146].hex()
    read_qty = int(data[146:148].hex(), 16)
    read_ng = int(data[148:150].hex(), 16)
    read_code = int(data[150:152].hex())
    read_id = data[152:180]
    pre_starttime, pre_endtime = parse_time(pre_ts)
    scan_starttime, scan_endtime = parse_time(scan_ts)
    shell_starttime, shell_endtime = parse_time(shell_ts)
    read_starttime, read_endtime = parse_time(read_ts)

    comm_code, back_code, light_code, _ = str(scan_msg).lstrip('b').replace("'",'').replace('@','').split(',')
    product_id = str(read_id).lstrip('b').replace("'",'').replace('@','')


    '''msg for repeat check '''
    pre_assembly_msg = data[0:14]
    scan_code_msg = data[14:120]
    up_shell_msg = data[120:134]
    readid_msg = data[134:180]

    print(pre_starttime)
    print(pre_endtime)


    ''' insert into database'''
    if pre_assembly_msg != g_pre_assembly_msg:

        g_pre_assembly_msg = pre_assembly_msg
        logger.info('get pre_assembly')
        try:
            pre_start = datetime.datetime.strptime(str(pre_starttime), "%y%m%d%H%M%S")
            pre_end = datetime.datetime.strptime(str(pre_endtime), "%y%m%d%H%M%S")
        except Exception as e1:
            pre_start = datetime.datetime.now()
            pre_end = datetime.datetime.now()
            logger.error('pre_starttime: ' + str(pre_starttime))
            logger.error('pre_endtime: ' + str(pre_endtime))

        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into pre_assemly (qty, starttime, endtime ) values (%s,%s, %s) """, ( pre_qty, pre_start, pre_end))
            db.commit()
        except Exception as e:
            logger.error('pre_assembly: ************' )
            logger.exception(e)
        finally:
            db.close()
    else:
        logger.info('drop assembly')

    if scan_code_msg != g_scan_code_msg:
        g_scan_code_msg = scan_code_msg
        logger.info('get scan_code_msg')
        try:
            scan_start = datetime.datetime.strptime(str(scan_starttime), "%y%m%d%H%M%S")
            scan_end = datetime.datetime.strptime(str(scan_endtime), "%y%m%d%H%M%S")
        except Exception as e1:
            logger.error('scan_starttime: ' + str(scan_startime))
            logger.error('scan_endtime: ' + str(scan_endtime))

        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into scancode (comm_code, back_code, light_code , qty, ng, starttime, endtime ) values (%s,%s, %s, %s, %s, %s ,%s) """, (comm_code, back_code, light_code, scan_qty , scan_ng,  scan_start, scan_end ))
            db.commit()
        except Exception as e:
            logger.exception(e)
        finally:
            db.close()
    else:
        logger.info('drop scan_code_msg')

    if up_shell_msg != g_up_shell_msg:
        g_up_shell_msg = up_shell_msg
        logger.info('get up_shell_msg')
        try:
            shell_start =  datetime.datetime.strptime(str(shell_starttime), "%y%m%d%H%M%S")
            shell_end = datetime.datetime.strptime(str(shell_endtime), "%y%m%d%H%M%S")
        except Exception as e1:
            logger.error('shell_starttime: ' + str(shell_starttime))
            logger.error('shell_endtime: ' + str(shell_endtime))

        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into upshell ( qty,  starttime, endtime ) values (%s, %s, %s) """, ( shell_qty,  shell_start, shell_end ))
            db.commit()
        except Exception as e:
            logger.exception(e)
        finally:
            db.close()
    else:
        logger.info('drop up_shell_msg')

    if readid_msg != g_readid_msg:
        g_readid_msg = readid_msg
        logger.info('get readid_msg')
        try:
            read_start =  datetime.datetime.strptime(str(read_starttime), "%y%m%d%H%M%S")
            read_end =  datetime.datetime.strptime(str(read_endtime), "%y%m%d%H%M%S")
        except Exception as e1:
            logger.error('read_starttime: ' + str(read_starttime))
            logger.error('read_endtime: ' + str(read_endtime))
            read_start = datetime.datetime.now()
            read_end = datetime.datetime.now()
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into readid (product_id, qty, ng, code, starttime, endtime ) values (%s, %s, %s , %s , %s, %s) """, ( product_id, read_qty, read_ng, read_code, read_start, read_end ))
            db.commit()
        except Exception as e:
            logger.exception(e)
        finally:
            db.close()
    else:
        logger.info('drop readid_msg')


def parse_firsttest(response):
    global g_firsttest_msg
    global logger
    res = response
    data = res[30:]
    starttime = parse_stime(res[30:36].hex())
    first_qty = int(res[36:38].hex(), 16)
    first_ng  = int(res[38:40].hex(), 16)
    endtime = parse_stime(res[40:46].hex())
    codemsg = res[46:246]
    codemsg = str(codemsg).lstrip('b').replace("'",'')

    firsttest_msg = data[30:]

    if firsttest_msg != g_firsttest_msg:
        g_firsttest_msg = firsttest_msg
        logger.info('get_firsttest_msg')
        try:
            first_start = datetime.datetime.strptime(str(starttime), "%y%m%d%H%M%S")
            first_end = datetime.datetime.strptime(str(endtime), "%y%m%d%H%M%S")
        except:
            logger.error('first_start: ' + str(starttime))
            logger.error('first_end: ' + str(endtime))
            first_start = datetime.datetime.now()
            first_end = datetime.datatime.now()

        codes = codemsg.replace('@','').split(',')

        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()

            for s in codes:
                if ( not s.startswith('---')):
                    product_id, test_code = s.split('.')
                    c.execute("""insert into firsttest ( product_id, test_code , qty, ng, starttime, endtime ) values (%s, %s, %s, %s,%s,%s) """, ( product_id,  test_code , first_qty, first_ng, first_start, first_end ))
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()
    else:
        logger.info('drop firsttest_msg')



def parse_screw(response):
    '''
    '''
    global g_screw_msg
    global g_firstmat_msg
    global logger
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

    if debug_flg == 1:
        print(screw_starttime)
        print(screw_endtime)
        print(screw_qty)
        print(first_starttime)
        print(first_endtime)
        print(firstmat_qty)
        print(firstmat_ng)
        print(firstmat_id)


def parse_repeattest(response):
    global g_repeattest_msg
    global logger
    res = response
    starttime = parse_stime(res[30:36].hex())
    repeat_qty = int(res[36:38].hex(), 16)
    repeat_ng  = int(res[38:40].hex(), 16)
    endtime = parse_stime(res[40:46].hex())
    codemsg = res[46:246]
    codes = str(codemsg).lstrip('b').lstrip("'").rstrip("'").replace('@','').split(',')


    repeattest_msg = res[30:]

    if debug_flg == 1:
        print(starttime)
        print(repeat_qty)
        print(repeat_ng)
        print(endtime)
        print(codemsg)

    if repeattest_msg != g_repeattest_msg:
        g_repeattest_msg = repeattest_msg
        logger.info('get repeatest_msg')
        start = datetime.datetime.strptime(str(starttime), "%y%m%d%H%M%S")
        end = datetime.datetime.strptime(str(endtime), "%y%m%d%H%M%S")
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            for s in codes:
                if ( not s.startswith('---')):
                    product_id, test_code = s.split('.')
                    c.execute("""insert into retest ( product_id, test_code , qty, ng, starttime, endtime ) values (%s, %s, %s, %s,%s,%s) """, ( product_id,  test_code , repeat_qty, repeat_ng, start, end ))
                    db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()
    else:
        logger.info('drop repeatest_msg')





def parse_ccd(response):
    '''ccd '''

    global g_ccd_msg
    global g_sample_msg
    global g_secmat_msg
    global logger
    res = response
    data = res[30:]
    ccd_ts = data[0:12].hex()
    ccd_qty = int(data[12:14].hex(),16)
    ccd_ng = int(data[14:16].hex(), 16)
    ccd_code = data[16:18].hex()
    ccd_id = data[18:48].decode().replace('@','').replace(',','')
    sample_ts = data[48:60].hex()
    sample_qty = int(data[60:62].hex(),16)
    sample_ng = int(data[62:64].hex(),16)
    sample_code = data[64:124].decode()
    secmat_ts = data[124:136].hex()
    sec_qty = int(data[136:138].hex(),16)
    sec_ng = int(data[138:140].hex(),16)
    sec_id = data[140:170]
    sec_id = str(sec_id).lstrip('b').replace("'",'').replace('@','').replace(',','')
    sec_id =''.join(filter(lambda x: x in printable, sec_id))

    ccd_starttime, ccd_endtime = parse_time(ccd_ts)
    sample_starttime, sample_endtime = parse_time(sample_ts)
    secmat_starttime, secmat_endtime = parse_time(secmat_ts)
    sample_id, test_code = sample_code.replace('@','').replace(',','').split('.')
    test_code = ''.join(filter(lambda x: x in printable, test_code))

    ccd_msg = data[0:48]
    sample_msg = data[48:124]
    secmat_msg = data[124:]

    if debug_flg == 1:
        print(ccd_starttime)
        print(ccd_endtime)
        print(ccd_qty)
        print(ccd_ng)
        print(ccd_id)
        print(ccd_code)
        print(sample_starttime)
        print(sample_endtime)
        print(sample_qty)
        print(sample_ng)
        print(sample_code)
        print(sec_starttime)
        print(sec_endtime)
        print(sec_qty)
        print(sec_ng)
        print(sec_id)

    if ccd_msg != g_ccd_msg:
        g_ccd_msg = ccd_msg
        logger.info('get ccd_msg')
        ccd_start = datetime.datetime.strptime(str(ccd_starttime), "%y%m%d%H%M%S")
        ccd_end =  datetime.datetime.strptime(str(ccd_endtime), "%y%m%d%H%M%S")

        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into ccd (product_id, ccd_code ,qty, ng, starttime, endtime ) values (%s, %s, %s,%s,%s,%s) """, ( ccd_id, ccd_code, ccd_qty, ccd_ng, ccd_start, ccd_end ))
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()
    else:
        logger.info('drop ccd_msg')

    if sample_msg != g_sample_msg :
        g_sample_msg = sample_msg
        logger.info('get sample_msg')
        sample_start = datetime.datetime.strptime(str(sample_starttime), "%y%m%d%H%M%S")
        sample_end = datetime.datetime.strptime(str(sample_endtime), "%y%m%d%H%M%S")
        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            c.execute("""insert into sample (product_id, test_code ,qty, ng, starttime, endtime ) values (%s, %s, %s,%s,%s,%s) """, ( sample_id, test_code, sample_qty, sample_ng, sample_start, sample_end ))
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()
    else:
        logger.info('drop sample_msg')


    if secmat_msg != g_secmat_msg:
        g_secmat_msg = secmat_msg
        logger.info('get secmat_msg')
        secmat_start = datetime.datetime.strptime(str(secmat_starttime), "%y%m%d%H%M%S")
        secmat_end = datetime.datetime.strptime(str(secmat_endtime), "%y%m%d%H%M%S")

        try:
            db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
            c = db.cursor()
            print(sec_id)
            c.execute("""insert into secmat (product_id, qty, ng, starttime, endtime ) values (%s, %s, %s, %s,%s) """, ( sec_id,  sec_qty, sec_ng, secmat_start, secmat_end ))
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()
    else:
        logger.info('drop secmat_msg')




def parse_remark(response):
    global g_remark_msg
    global logger
    res = response
    data = res[30:]
    starttime = parse_stime(data[0:6].hex())
    qty = int(data[6:8].hex(),16)
    endtime = parse_stime(data[8:14].hex())
    id_iccid = data[14:134]
    id_iccid = str(id_iccid).lstrip('b').replace("'",'').replace('@','')
    product_id, iccid , _ = id_iccid.split(',')
    if debug_flg == 1:
        print(starttime)
        print(endtime)
        print(qty)
        print(id_iccid)

    remark_msg = res[30:]

    if remark_msg != g_remark_msg:
        g_remark_msg = remark_msg
        logger.info('get remark_msg')
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
    else:
        logger.info('drop remark_msg')

def parse_check(response):
    '''
    check
    '''
    global g_check_msg
    global g_cover_msg
    global logger
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
    cover_id = data[78:106]
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
