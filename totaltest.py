from parse_response import *
from routereq import *
from time import *
from threading import Thread

def total_firsttest():
    while True:
        res = get_firsttest()
        parse_firsttest(res)
        sleep(5)

def total_upassemly():
    while True:
        res = get_upassemly()
        parse_upassemly(res)
        sleep(5)


def total_screw():
    while True:
        res = get_screw()
        parse_screw(res)
        sleep(5)

def total_repeattest():
    while True: 
        res = get_repeattest()
        parse_repeattest(res)
        sleep(5)

def total_ccd():
    while True:
        res = get_ccd()
        parse_ccd(res)
        sleep(5)

def total_remark():
    while True:
        res = get_remark()
        parse_remark(res)
        sleep(5)

def total_check():
    while True:
        res = get_check()
        parse_check(res)
        sleep(5)


if __name__ == '__main__':
    upassemly = Thread(target=total_upassemly)
    firsttest = Thread(target=total_firsttest)
    screw = Thread(target=total_screw)
    repeattest = Thread(target=total_repeattest)
    ccd = Thread(target=total_ccd)
    remark = Thread(target=total_remark)
    check = Thread(target=total_check)

    upassemly.start()
    firsttest.start()
    screw.start()
    repeattest.start()
    ccd.start()
    remark.start()
    check.start()
