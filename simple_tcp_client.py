# A Simple TCP client, used as a warm-up exercise for socket programming assignment.
# Course IELEx2001, NTNU

import random
import time
from socket import *

# Hostname of the server and TCP port number to use
#HOST = "datakomm.work"
#PORT = 1301

#HOST = input()
#PORT = int(input())

HOST = "localhost"
PORT = 10555

# The socket object (connection to the server and data exchange will happen using this variable)
client_socket = None


def connect_to_server():
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    global client_socket
    global HOST
    global PORT

    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        return True
    except IOError as e:
        print("Error happened:", e)
        return False



def close_connection():
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    global client_socket

    try:
        client_socket.close()
        return True
    except IOError as e:
        print("Error happened:", e)
        return False


def send_request_to_server(request):
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    global client_socket

    try:
        client_socket.send((request.strip("\n")).encode())
        return True
    except IOError as e:
        print("Error happened:", e)
        return False


def read_response_from_server():
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    global client_socket

    try:
        value = client_socket.recv(100).decode()
        return value
    except IOError as e:
        print("Error happened:", e)
        value = None
    return value


def run_client_tests():
    print("Simple TCP client started")
    if not connect_to_server():
        return "ERROR: Failed to connect to the server"

    print("Connection to the server established")
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    request = str(a) + "+" + str(b)

    if not send_request_to_server(request):
        return "ERROR: Failed to send valid message to server!"

    print("Sent ", request, " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)
    # seconds_to_sleep = 2 + random.randint(0, 5)
    # print("Sleeping %i seconds to allow simulate long client-server connection..." % seconds_to_sleep)
    time.sleep(5)

    request = "bla+bla"
    if not send_request_to_server(request):
        return "ERROR: Failed to send invalid message to server!"

    print("Sent " + request + " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)
    if not (send_request_to_server("game over") and close_connection()):
        return "ERROR: Could not finish the conversation with the server"

    time.sleep(5)
    print("Game over, connection closed")
    # When the connection is closed, try to send one more message. It should fail.
    if send_request_to_server("2+2"):
        return "ERROR: sending a message after closing the connection did not fail!"

    print("Sending another message after closing the connection failed as expected")
    return "Simple TCP client finished"



# Main entrypoint of the script
if __name__ == '__main__':
    result = run_client_tests()
    print(result)
