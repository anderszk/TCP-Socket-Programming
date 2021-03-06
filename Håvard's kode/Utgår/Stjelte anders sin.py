# A Simple TCP client, used as a warm-up exercise for socket programming assignment.
# Course IELEx2001, NTNU

import random
import time
from socket import *

# Hostname of the server and TCP port number to use
HOST = "datakomm.work" #input("Enter the name of the server you want to join: ")  #"datakomm.work"
PORT = 1301 #int(input("Enter your port here: "))  #1301

# The socket object (connection to the server and data exchange will happen using this variable)
client_socket = socket(AF_INET, SOCK_STREAM)


def connect_to_server(HOST, PORT):
    global client_socket
    try:
        client_socket.connect((HOST, PORT))  # Connecter til Sockets med inputs som ble spurt om tidligere
        client_socket.settimeout(3)
        return True
    except:
        return False


def close_connection():
    global client_socket
    try:
        client_socket.close()  # Stenger/Avslutter tilkoblingen
        return True
    except:
        return False

    #if not connect_to_server():
    #    return True
    #else:
    #    return False


def send_request_to_server(request):

    is_request_int = request.split("+")

    if is_request_int[0].isdigit() == True:  #x > 0:
        request_strip = request.strip(" ")
        split = request_strip.split()
        split_send = []
        #print("agurk!!!!!")
        for i in split:
            split_send.append(i+'\n')

        try:
            for u in split_send:
                client_socket.send(u.encode())

            return True
        except:
            return False
    else:
        try:
            print("Var ikke tall i request")
            client_socket.send(request.encode())
            return True
        except:
            print("send_request to server, was not number and did not send message. exception: line 63.")
            return False



def read_response_from_server():
    global client_socket
    response_encoded = client_socket.recv(1000)
    response_decoded = response_encoded.decode()
    response = response_decoded.strip("\n")

    if response is None:
        return False
    else:
        return response


def run_client_tests():
    """
    Runs different "test scenarios" from the TCP client side
    :return: String message that represents the result of the operation
    """
    print("Simple TCP client started")
    if not connect_to_server(HOST, PORT):
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
    seconds_to_sleep = 2 + random.randint(0, 5)
    print("Sleeping %i seconds to allow simulate long client-server connection..." % seconds_to_sleep)
    time.sleep(seconds_to_sleep)

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