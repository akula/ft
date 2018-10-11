import struct
import re
import socket
from parse_response import parse_res


def asciitohex(ascstr):
    if ascstr == '':
        return bytearray(''.encode())
    else:
        return bytearray(ascstr.encode())


def FINSHEAD():
    return bytearray('FINS'.encode())


def commandflg(hexstr):
    return bytearray.fromhex(hexstr)


def finsconn(client):
    requestframe = FINSHEAD() + commandflg('0000000C') + \
                   commandflg('00000000') + \
                   commandflg('00000000')+ commandflg(
        setclient(client))  # commandflg('00000066')

    ## bytearray.fromhex(hex(client)[2:])
    return requestframe


def setclient(clientip):
    return format(clientip, '08x')


def getclient(respstr):
    return respstr[-1]


def getserv(respstr):
    return respstr[-5]


def composeaddr(serv, client):
    ''' compose serv and client address'''
    return commandflg(format(serv, '02x') + '0000' + format(client, '02x'))


def readcommand(start, readcnt):
    ''' read command frame'''
    return commandflg(format(start, '04x') + format(readcnt, '06x'))


def finscommand(serv, client, startaddr, readcnt):
    ''' generate  the finscommand frame'''
    return commandflg('00000000') + commandflg('80000200') + composeaddr(serv, client) + commandflg('00FF0101') + commandflg(
        '82') + readcommand(startaddr, readcnt)


def finshead():
    ''' fins commuicate head frame , all same '''
    '''Need fix the length problem '''
    return commandflg('46494E53 0000001A 00000002')


def requestframe(serv, client, startadd, readcnt):
    return finshead() + finscommand(serv, client, startadd, readcnt)


def get_errormsg(res):
    pass


def parseerror(response):
    '''parse the error msg from the PLC '''
    ''' Need to be done '''
    err_msg = {
        '0x0000000': None,
        '0x0000001': 'The header is not FINS (ASCII code)',
        '0x0000002': 'The data length is too long.',
        '0x0000003': 'The command is not supported.',
        '0x0000020': 'All connections are in use.',
        '0x0000021': 'The specified node is already connected.',
        '0x0000022': 'Attempt to access a protected node from an unspecified IP',
        '0x0000023': 'The client FINS node address is out of range.',
        '0x0000024': 'The same FINS node address is being used by the client and server',
        '0x0000025': 'All the node addresses available for allocation have been used.',
    }
    errmsg = get_errormsg(response)
    return err_msg[errmsg]
'''
example DM01 DM02 read
          0000 001A 0000 0002 0000 0000 8000 0200 0300 0071 00ff 0101 2300 6400 0001
4649 4E53 0000 001A 0000 0002 0000 0000 8000 0200 2100 00C0 0000 0101 8200 0000 0002
FINS      0000 001a 0000 0002 0000 0000 8000 0200 !00  00c0 00ff 0101 8200 0000 0002
          0000 001a 0000 0002 0000 0000 8000 0200 !00  00c0 00ff 0101 8200 0000 0002
FINS      0000 001a 0000 0002 0000 0000 8000 0200 1000 00d  00ff 0101 821f @00  0014
'''


if __name__ == '__main__':
    '''sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.250.16',9600))
    sock.send(finsconn(100))
    resp = sock.recv(16)
    print(requestframe(serv, client, 8000,20))
    sock.close()
    '''


if __name__ == '__main__':
    print(repr(requestframe(16, 100, 8000, 20)))
