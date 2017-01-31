import zmq
import time

myIP='10.0.0.2'
ListenPort = 7004

# server

contextIn = zmq.Context()
serverIn = contextIn.socket(zmq.REP)
print("tcp://%s:%s" % (myIP,ListenPort))
serverIn.bind("tcp://%s:%s" % (myIP,ListenPort))

while 1:
    print('in listen')
    requestIn_bytes = serverIn.recv()
    print('1')
    requestIn=requestIn_bytes.decode('utf-8')
    print('recv')
#    ok='ok'.encode('utf-8')
    serverIn.send_string('ok')
    print('done')
