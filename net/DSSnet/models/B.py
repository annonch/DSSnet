import time
import zmq

es_IP = '10.0.0.2'
es_port = 7004

contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
print("tcp://%s:%s" % (es_IP,es_port))
clientOut.connect("tcp://%s:%s" % (es_IP,es_port))


def send_es(msg):
    print('sending %s' % msg)
    msg_bytes=msg.encode('utf-8')
    clientOut.send_string(msg)
    print('sent')
    result=clientOut.recv()
    logging.debug('send: %s at time %s' % (msg,time.time()))

while 1:
    send_es('howdy')
