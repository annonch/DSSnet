import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

socketout = context.socket(zmq.REQ)
socketout.bind("tcp://6.6.6.31:5556")

if os.fork():
    while True:
        
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)
        
        #  Do some 'work'
        time.sleep(1)
        socket.send_string('hi')#line.rstrip("\n"))

while True:

    socketout.send_string('hi')
    s= socketout.recv()
    print s
