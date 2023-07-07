import socket

port = 12340

servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind( ("", port) )

server_address=('192.168.0.19',10001)
print('connecting to {} port {}'.format(*server_address))
servidor.connect(server_address)

try:

    # Send data
    #message = b'This is the message.  It will be repeated.'
    message = 'Este es el mensaje'
    codigo = bytes(message, 'utf-8')
    print('sending {!r}'.format(message))
    servidor.sendall(codigo)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = servidor.recv(port)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    servidor.close()
