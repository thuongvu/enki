import signal
import socket
import sys

ACK = 'ACK'.encode('utf-8')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = '0.0.0.0'
try:
    port = int(sys.argv[1])
except IndexError:
    port = 8000
sock.bind((address, port))
try:
    server_address = sys.argv[2]
except IndexError:
    server_address = '0.0.0.0'
try:
    server_port = sys.argv[3]
except IndexError:
    server_port = 9000

def timeout_handler(signum, frame):
    raise TimeoutError()

def send(msg):
    response = None
    while response != ACK:
        sock.sendto(msg.encode('utf-8'), (server_address, server_port))
        print('sent: {}'.format(msg))
        response, _ = sock.recvfrom(1024)
        print('response: {}'.format(response))

while True:
    msg = input('text input: ')
    retry = True
    while retry:
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(3)
            send(msg)
        except TimeoutError:
            continue
        retry = False
        signal.alarm(0)
    
