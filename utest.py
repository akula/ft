import logging
rawb =b'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,Z316002A8037277\r@@@@@@@@@@@@@,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,'.replace(b'\r',b'')


msg = '508037285.OKT22222,508037296.NGT21212,---,---,---c@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

si = msg.replace('@','').split(',')
for s in si:
    if (s.startswith('---')):
        s = ''
    print(s)


logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='error.log', level=logging.INFO)


def testp():
    try:
        a = 0
        b = 1
        c = b/a
    except Exception as e:
        print(e)
        logger.exception('--some error knock the door ----')
    finally:
        print('working@@@@@@@')


if __name__ == '__main__':
    testp()