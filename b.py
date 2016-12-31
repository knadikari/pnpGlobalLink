# import os
#
# try:
#     path = "/tmp/my_program.fifo"
#     os.mkfifo(path)
# except:
#     print "A"
# while True:
#     fifo = open(path, "w")
#     fifo.write("Message from the sender B!\n")
#     fifo.close()
import time
time.sleep(5)
#for i in range(0,100):
print "MSG"
time.sleep(1)
print "MSG"
time.sleep(1)
time.sleep(10)