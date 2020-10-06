from socket import *
from datetime import datetime
datetime.now().strftime('%Y-%m-%d %H:%M:%S')

TCP_PORT = 1300  # TCP port used for communication
SERVER_HOST = "datakomm.work"  # Set this to either hostname (domain) or IP address of the chat server

current_state = "disconnected"  # The current state of the system
client_socket = None  # type: socket


def connect_to_server():

    global client_socket
    global current_state

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.settimeout(3)
        client_socket.connect((SERVER_HOST, TCP_PORT))
        current_state = "connected"
        client_socket.send("async\n".encode())
        sync_mode_confirmation = get_servers_response()
        #print(sync_mode_confirmation)
        print("================================\n\tReading chat from server\n================================")

    except IOError:
        print("Failed to connect to server")
        current_state = "disconnected"

def get_servers_response():
    return client_socket.recv(1000).decode()

def read_one_line(sock):

    newline_received = False
    message = ""
    while not newline_received:
        character = sock.recv(1).decode()
        if character == '\n':
            newline_received = True
        elif character == '\r':
            pass
        else:
            message += character
    return message


if __name__ == '__main__':
    connect_to_server()
    if current_state == "connected":
        while True:
            try:
                message = read_one_line(client_socket)
                print(message.replace("msg", f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: "))
            except IOError:
                agurk_paa_pizza = "fyfy"

