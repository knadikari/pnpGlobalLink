# import os
#
# try:
#     path = "/tmp/my_program.fifo"
#     os.mkfifo(path)
# except:
#     print "A"
#
# while True:
#     fifo = open(path, "w")
#     fifo.write("Message from the sender A!\n")
#     fifo.close()

#import subprocess

#p = subprocess.Popen(['python','/home/nrv/PycharmProjects/PnpGlobalLink/b.py'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
#p.stdin.write('one\ntwo\nthree\nfour\nfive\nsix\n')
#print p.communicate()
#p.stdin.close()


import subprocess

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
        print "YoYO"
        break



    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# Example
for path in execute(['python','/home/nrv/PycharmProjects/PnpGlobalLink/b.py']):
    print path
