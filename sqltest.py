import MySQLdb
import datetime
'''
datetimes = datetime.datetime.strptime("1809221433", "%y%m%d%H%M%S")
db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
c = db.cursor()
c.execute("""insert into cover (product_id, qty, starttime, endtime ) values (%s,%s, %s, %s) """, ("abcdefg", 300, datetimes, datetimes))
db.commit()


import threading
import time

g_num = 0

def work1(num):
    global g_num
    for i in range(num):
        g_num += 1
    print("----in work1, g_num is %d---"%g_num)


def work2(num):
    global g_num
    for i in range(num):
        g_num += 1
    print("----in work2, g_num is %d---"%g_num)

'''
iccid = '8894321a2337'
db=MySQLdb.connect(host="192.168.250.28", user="autoline", passwd="1qa2ws",db="autoline")
c = db.cursor()
c.execute("""select sim from xls_simiccid where iccid = %s order by id desc""" , (iccid,))
simno = c.fetchone()[0]
print(simno)
db.close()