from parse_response import *
from routereq import *
from time import *
from threading import Thread

def total_firsttest():
    while True:
        try:
            res = get_firsttest()
        except Exception as e :
            print('get_firstest error')
        if res != '':
            parse_firsttest(res)
        else:
            print('get_first error')
        sleep(5)

def total_upassemly():
    while True:
        try:
            res = get_upassemly()
        except Exception as e:
            print('get_upassemly error')
        if res != '':
            parse_upassemly(res)
        else:
            print('get_upassemly error')
        sleep(5)



def total_screw():
    while True:
        try:
            res = get_screw()
        except Exception as e:
            print('get_screw error')
        if res != '':
            parse_screw(res)
        else:
            print('get_screw error')
        sleep(5)
  

def total_repeattest():
    while True: 
        try:
            res = get_repeattest()
        except Exception as e:
            print('get_repeatest error')
        if res != '':
            parse_repeattest(res)
        else:
            print('repeatest error')
        sleep(5)

def total_ccd():
    while True:
        try:
            res = get_ccd()
        except Exception as e:
            print('get_ccd error')
        if res != '':
            parse_ccd(res)
        else:
            print('ccd error');
        sleep(5)

def total_remark():
    while True:
        try:
            res = get_remark()
        except Exception as e:
            print(e)
        
        if res != '':
            parse_remark(res)
            print('remark ok')
        else:
            print('remark error');
        sleep(5)

def total_check():
    get_check()


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
    check.start()
    remark.start()
