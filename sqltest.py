import MySQLdb
import datetime

datetimes = datetime.datetime.strptime("1809221433", "%y%m%d%H%M%S")
db=MySQLdb.connect(host="127.0.0.1", user="autoline", passwd="1qa2ws",db="autoline")
c = db.cursor()
c.execute("""insert into cover (product_id, qty, starttime, endtime ) values (%s,%s, %s, %s) """, ("abcdefg", 300, datetimes, datetimes))
db.commit()

'''
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