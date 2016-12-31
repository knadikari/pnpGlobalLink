#!/usr/bin/python

import random
import os
import time

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from PnpLib import initPnp , pnpinput ,pnpprint


initPnp()
while True:

    msg=pnpinput()

    print msg

    pnpprint(msg+" 100 ")

