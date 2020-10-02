# A Simple TCP client, used as a warm-up exercise for socket programming assignment.
# Course IELEx2001, NTNU

import random #Importing the random module to get random integers
import time #Importing the time module
from socket import * #Importing the socket module the use the commands and library

# Hostname of the server and TCP port number to use
HOST = input("Enter the name of the server you want to join: ")  #User enter the hostname of the server, in this case "datakomm.work"
PORT = int(input("Enter your port here: "))  #User enter the port of the socket, in this case 1301

# The socket object (connection to the server and data exchange will happen using this variable)
client_socket = socket(AF_INET, SOCK_STREAM) #This needs to be a global variable because its used in several functions


def connect_to_server(HOST, PORT): #Function for the client to connect to the server, with input entered then the program is started.
    global client_socket #includes a global variable in the function
    try:
        client_socket.connect((HOST, PORT))  # Connecter til Sockets med inputs som ble spurt om tidligere
        client_socket.settimeout(3) #Gives an error if the client fails to connect to the server within 3 seconds
        return True #Return the boolean value True if it manages to connect
    except:
        return False #Return False if the client fails to connect to the server


def close_connection(): #Function to disconnect the client from the server.
    global client_socket #includes a global variable in the function
    try: #Tries to do the following
        client_socket.close() #Command from the socket module to disconnect
        return True
    except IOError: #If the following error occurs, it prevents the error the stop the program, but will do this instead:
        print("Something went wrong")
        return False




def send_request_to_server(request):
    global client_socket #includes a global variable in the function
    #request_strip = request.strip("+")
    split_send = request.split()
    try:
        if any('game' and 'over' in s for s in split_send) == True: #Uses the find function to decide if the list contains certain words
            close_connection() #Triggers the close function
            print("You typed: Game over, you have been disconnected from the server")
            return False
        else:
            for u in split_send: #Sends the message to the server
                client_socket.send(u.encode()) #Encodes the message to a byte.array
            return True
    except OSError:
        "Youre not connected to the server"



def read_response_from_server():
    global client_socket #includes a global variable in the function
    response_encoded = client_socket.recv(1000) #Receive-function, the argument is how many bits you want to receive
    response_decoded = response_encoded.decode() #Decodes the byte-array to a string
    response = response_decoded.strip("\n") #Strip-function that removes (argument) from the string

    if response is None: #Returns false if the client does not receive any messages from the server
        return False
    else:
        return response #If it does, it will return the response


def run_client_tests(): #Function to test the different functions.
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

    time.sleep(1)  # Delay added to analyze the response and prints
    print("Server responded with: ", response)



#Same as the function over, just to check consistency of the request/response
#-------------------------------------------------------------------------------------------------------------------------------------


    a = random.randint(1, 20)
    b = random.randint(1, 20)
    request = str(a) + "+" + str(b)

    if not send_request_to_server(request):
        return "ERROR: Failed to send valid message to server!"

    print("Sent ", request, " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    time.sleep(1)  # Delay added to analyze the response and prints
    print("Server responded with: ", response)




    a = random.randint(1, 20)
    b = random.randint(1, 20)
    request = str(a) + "+" + str(b)

    if not send_request_to_server(request):
        return "ERROR: Failed to send valid message to server!"

    print("Sent ", request, " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    time.sleep(1)  # Delay added to analyze the response and prints
    print("Server responded with: ", response)


# -------------------------------------------------------------------------------------------------------------------------------------



    seconds_to_sleep = 2 + random.randint(0, 5)
    print("Sleeping %i seconds to allow simulate long client-server connection..." % seconds_to_sleep)
    time.sleep(seconds_to_sleep)

    print("Pause done")

    time.sleep(1) #Delay added to analyze the response and prints

    request = "bla+bla"
    if not send_request_to_server(request):
        return "ERROR: Failed to send invalid message to server!"

    time.sleep(1) #Delay added to analyze the response and prints

    print("Sent " + request + " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)

    time.sleep(1) #Delay added to analyze the response and prints

    send_request_to_server("game over")

    time.sleep(1) #Delay added to analyze the response and prints

    print("Game over, connection closed")
    # When the connection is closed, try to send one more message. It should fail.
    if send_request_to_server("2+2"):
        return "ERROR: sending a message after closing the connection did not fail!"

    time.sleep(2) #Delay added to analyze the response and prints

    print("Sending another message after closing the connection failed as expected")
    return "Simple TCP client finished"


# Main entrypoint of the script
if __name__ == '__main__':
    result = run_client_tests()
    print(result)