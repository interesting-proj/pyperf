import socket
import time
import sys
from optparse import OptionParser

PORT=55555

def process_server(opt, args):
    print "Entering Server mode"
    print "Listening on port", opt.portnumber
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind((opt.bind_to_host, opt.portnumber))
    if opt.window:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, opt.window)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, opt.window)
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print "Connection from", addr[0], "port", addr[1]
        t = time.time()
        transferred = 0

        while True:
            data = conn.recv(opt.buflen)
            if not data:
                break
            transferred += len(data)
        t_total = time.time() - t
        conn.close()

        print "Received", transferred, "bytes in", t_total, "seconds"
        print "Speed", transferred/t_total, "B/sec", transferred/t_total/1024, "KB/sec",transferred/t_total/(1024*1024), "MB/sec"

def process_client(opt, args):
    print "Entering Client mode"
    print "Connecting to", opt.connect_to_hostname, "port", opt.portnumber
    buf = " " * opt.buflen
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    if opt.window:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, opt.window)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, opt.window)
    s.connect((opt.connect_to_hostname, opt.portnumber))


    t = time.time()
    transferred = 0
    while time.time() - t < opt.time:
        s.send(buf)
        transferred += opt.buflen

    t_total = time.time() - t
    s.close()
    print "Transferred", transferred, "bytes in", t_total, "seconds"
    print "Speed", transferred/t_total, "B/sec", transferred/t_total/1024, "KB/sec",transferred/t_total/(1024*1024), "MB/sec"



parser = OptionParser()
parser.add_option('-s', '--server', action="store_true", dest="server_mode")
parser.add_option('-c', '--client', action="store", type="string", dest="connect_to_hostname")


parser.add_option('-W', '--window', type='int', dest='window')
parser.add_option('-B', '--bind', dest="bind_to_host", type="string", default='')
parser.add_option('-l', '--len', dest="buflen", type="int", default=8192)
parser.add_option('-p', '--port', dest="portnumber", type="int", default=PORT)
parser.add_option('-t', '--time', dest="time", type="int", default=10)
opt,args = parser.parse_args()

if opt.server_mode and opt.connect_to_hostname:
    print "-s and -c are mutually exclusive"
    sys.exit(-1)


if opt.server_mode:
    process_server(opt, args)
    sys.exit(0)

if opt.connect_to_hostname:
    process_client(opt, args)
    sys.exit(0)

print "-s or -c has to be selected"
sys.exit(-1)

