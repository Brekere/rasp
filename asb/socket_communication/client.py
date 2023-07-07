import socket
import random


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind( ("", 1234) )

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.19', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

#part_info_data = b"id:1,id_machine:15"
working_time = random.randint(150,3000)
status = random.randint(0,1)
data_str = "'status':{}, 'working_time':{}".format(status, working_time)
if status == 1:
    rework = random.randint(0,1)
    data_str += ", 'rework':{}".format(rework)
    if rework == 1:
        status = random.randint(0,1)
        working_time = random.randint(150,3000)
        data_str += ", 'rework_status':{}, 'reworking_time':{}".format(status, working_time)
data_str = "{"+data_str+"}"

#part_info_data b"{\'status\':0,\'working_time\':100}"
part_info_data =  bytes(data_str, 'utf-8')

try:

    # Send data
    #message = b'This is the message.  It will be repeated.'
    message = part_info_data
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1234)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()