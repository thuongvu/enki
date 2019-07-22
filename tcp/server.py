import random
import socket
import sys

ACK = 'ACK'.encode('utf-8')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = '0.0.0.0'
try:
	port = int(sys.argv[1])
except IndexError:
	port = 9000
sock.bind((address, port))
try:
	drop_rate = float(sys.argv[1])
except IndexError:
	drop_rate = 0.3

while True:
    msg, client_address = sock.recvfrom(1024)
    decoded_msg = msg.decode('utf-8')
    if random.random() < drop_rate:
        print('Dropped datagram: {}'.format(decoded_msg))
        continue
    print('Received: {}'.format(decoded_msg))
    sock.sendto(ACK, client_address)

