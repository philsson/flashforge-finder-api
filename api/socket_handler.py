import socket

BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5


def send_and_receive(printer_address, code):
    """Sends and receives data"""

    message_data = '~{0}\r\n'.format(code)

    printer_socket = socket.socket()
    printer_socket.settimeout(TIMEOUT_SECONDS)
    printer_socket.connect((printer_address['ip'], printer_address['port']))
    printer_socket.send(message_data.encode())
    data = printer_socket.recv(BUFFER_SIZE)
    printer_socket.close()

    return data.decode()
