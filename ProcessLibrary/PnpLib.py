import os



pnpinpath = "/tmp/inpFifo"
pnpoutpath = "/tmp/outFifo"

def initPnp():
    try:
        os.mkfifo(pnpinpath)
    except:
        print "file is exsist"

    try:
        os.mkfifo(pnpoutpath)
    except:
        print "file is exsist"


def pnpinput():
    fifoin = open(pnpinpath, 'r')
    msg = fifoin.read()
    fifoin.close()
    return msg

def pnpprint(msg):
    fifoout = open(pnpoutpath, 'w')
    fifoout.write(msg)
    fifoout.close()



