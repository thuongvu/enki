import random
import socket
import sys
import threading

ACK = 'ACK'.encode('utf-8')

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = '0.0.0.0'
try:
	port = int(sys.argv[1])
except IndexError:
	port = 9000
sock.bind((address, port))
try:
	drop_rate = float(sys.argv[2])
except IndexError:
	drop_rate = 0.3

queue = []

def handle_queue():
    if len(queue):
        queue.pop(0)

while True:
    set_interval(handle_queue, 1)
    msg, client_address = sock.recvfrom(1024)
    decoded_msg = msg.decode('utf-8')
    print('Received: {}'.format(decoded_msg))
    queue.append(decoded_msg)
    if len(queue) > 3:
        print('Dropped datagram b/c queue: {}'.format(decoded_msg))
        continue
    print('Sending ack for {}'.format(decoded_msg))
    sock.sendto(ACK, client_address)

