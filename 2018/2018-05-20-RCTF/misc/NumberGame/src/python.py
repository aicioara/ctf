import argparse
import itertools
import string
import hashlib
import base64
import re
import socket

import time

socket.setdefaulttimeout(2.0)

from masterminder import MastermindGame as MM

# f="""
# sha256(****+OFO8jRfI9LVeT40U) == 7ae9f3e7ec804c19139e713d644da2b55282884f849a8bdda02853a940bab1e9
# """.strip()




def get_suffix_and_end(f):
    # fd = open("/home/aicioara/Downloads/foo.txt", 'r')
    # f = "".join([line for line in fd.readlines()])
    suffix = re.search(r'\*\*\*\*\+([^\)]*)', f).group(1)
    end = re.search(r'== ([^ \n]*)', f).group(1)
    return suffix, end


def crack(suffix, end):
    sample = string.uppercase + string.lowercase + "0123456789"

    for prefix in itertools.product(sample, repeat=4):
        candidate = "".join(prefix) + suffix
        h = hashlib.sha256(candidate).hexdigest()
        if h == end:
            return "".join(prefix)
            break


def prepare():
    host = '149.28.139.172'
    port = 10002

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    f = s.recv(10000)
    print (f)
    print (s.recv(10000))

    suffix, end = get_suffix_and_end(f)
    code = crack(suffix, end)
    print ("Code found {}".format(code))

    s.send(code + "\n")
    print (s.recv(100000))

    return s

class AndreiError(Exception):
    pass

def interact(s, a, b, c, d):
    to_send = "{} {} {} {}\n".format(a, b, c, d)
    print (to_send)
    s.send(to_send)

    while True:
        try:
            resp = s.recv(10000)
            print (resp)

            if resp.find("round") != -1:
                raise AndreiError('a')

            reds = re.search(r'(\d),', resp).group(1)
            blacks = re.search(r', (\d)', resp).group(1)
            return int(reds), int(blacks)
        except AndreiError as e:
            print e
            time.sleep(0.1)
            raise
        except Exception as e:
            print e
            time.sleep(0.5)


def play(s):
    mm = MM()

    guess = tuple(list(mm.start_game()))
    print (guess)
    while True:
        mm.validate(guess)
        red, black = interact(s, *guess)
        print (red, black)
        guess = mm.guess(red, black)
        guess = tuple(list(guess))
        print (guess)
        # import sys; sys.stdin = open('/dev/tty'); import pdb; pdb.set_trace();






if __name__ == "__main__":
    # mm = MM()
    # guess = mm.start_game()
    # print (guess)
    # mm.validate(guess)

    # new_guess = mm.guess(2, 1)
    # print (new_guess)

    s = prepare()
    s.settimeout(1.0)
    print ("Waiting")
    print (s.recv(100000)) # Hello

    while True:
        try:
            play(s)
        except:
            pass
    # pass
    # suffix, end = get_suffix_and_end()
    # creck(suffix, end)
