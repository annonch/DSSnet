import time
import zmq
import sys
import pipe

my_IP = sys.argv[1]
my_port = sys.argv[2]
interval = sys.argv[3]

# q pipeworks


# networking
contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
print("tcp://%s:%s" % (my_IP,my_port))
clientOut.connect("tcp://%s:%s" % (my_IP,my_port))

# function to send data
def send_to_server(msg):
    print('sending %s' % msg)
    msg_bytes=msg.encode('utf-8')
    clientOut.send_string(msg)
    print('sent')
    result=clientOut.recv()
    logging.debug('send: %s at time %s' % (msg,time.time()))

def get_data():
    pass


# easy lets may a loop, the loop will be nice

# sleep for a while
# get sensor value from dssnet
# send result to server to do whatever with

while True:
    time.sleep(interval)
    data = get_data()
    send_to_server(data)
