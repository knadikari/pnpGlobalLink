import os


class inputDaemonHandle:
    def __init__(self):
        self.path = "/tmp/inpFifo"
        self.makeFiFo()

    def makeFiFo(self):
        try:
            os.mkfifo(self.path)
        except Exception as e:
            print e

    def writeData(self,msg):
        fifo = open(self.path, "w")
        fifo.write(msg)
        fifo.close()


