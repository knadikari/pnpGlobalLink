import json
import random
import os
import time

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from PnpLib import initPnp , pnpinput ,pnpprint




def add():
    data=pnpinput()
    recv_data = json.loads(data)
    number = recv_data["num"] + 10
    print number


while 1:
    add()


