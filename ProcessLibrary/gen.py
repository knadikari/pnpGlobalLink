
import random
import os
import time

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from PnpLib import initPnp , pnpinput ,pnpprint


def gen():
    num = random.randint(0, 9)
    return num

def send():
    data = {}
    number = gen()
    data["num"]= number
    pnpprint(json.dumps(data));
    print number
    # should send as json.dumps(data)


    

while True:
    send()
