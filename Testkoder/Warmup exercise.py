#Warm-up exercise Gruppe 11
#@anderszk 27.10.2020

import random
import time

from socket import * #Importerer Socket Modulen
client_socket = socket(AF_INET, SOCK_STREAM) #Setter sockets hhv. internett og TCP.

bool_connected = False #Brukes til fremtidige funksjoner som sjekker om clienten fortsatt er koblet til

HOST = input("Hva er navnet på server vi du koble til?: ") #"datakomm.work"
PORT = int(input("Hvilken port vil du koble til?: ")) #1301


def connect_to_server():
    x = 1
    client_socket.connect((HOST, PORT)) #Connecter til Sockets med inputs som ble spurt om tidligere

    while x < 5: #Looper login til du har tastet riktig passord
        username = input("Enter you username here: ") #Skriv inn brukernavn
        password = input("Enter the password for the server") #Som her er 123, sender feilmelding tilbake if password != 123
        authorization_request = [username, password]  # Sender en string til serveren
        authorization_request_bytes = authorization_request.encode()  # Encoder stringen til byte-array
        client_socket.send(authorization_request_bytes)  # Sender byte-arrayen til serveren
        #Nå må vi sjekke om vi fikk koblet til serveren:
        authorization_response_bytes = client_socket.recv(100)
        authorization_response = authorization_response_bytes.decode()
        if authorization_response == "Authorized":
            print("Connection established")
            bool_connected = True
            break;
        else:
            print("Failed to connect to the server, try again!")



def close_connection():
    confirmation = input('Are you sure you want to quit the connection?: ')
    bool_confirmation = False #Brukes til fremtidige funksjoner som sjekker om clienten fortsatt er koblet til
    if confirmation in ["YES","Yes","yes"]:
        client_socket.close()  # Stenger/Avslutter tilkoblingen
        print("You have disconnected from the server:",HOST)
        bool_confirmation = True
        return bool_confirmation
    else:
        print("You are still connected to ",HOST,"!")
        bool_confirmation = False
        return bool_confirmation



def send_request_to_server(): #While løkke i hovedfunksjon
    action_go = ""
    print("Please enter 2 integers or type 'Game over' if you want to disconnect")
    first_int = input("First digit") #Convert to int in server
    second_int = input("Second digit") #Convert to int in server
    if first_int or second_int in ["game over", "Game over", "Game Over"]:
        close_connection()

    action = ("What do you want to do? (add, multiply, merge): ") #If-statement in servercode

    if (first_int or second_int) not in ["game over", "Game over", "Game Over"]:
        command_to_send = [first_int, second_int, action]  # Sender en liste til serveren
        cmd_as_bytes = command_to_send.encode()  # Encoder stringen til byte-array
        client_socket.send(cmd_as_bytes)  # Sender byte-arrayen til serveren

    else:
        print("Error: Can not reach: ",HOST) #Sier ifra at du koblet fra serveren som ble gjort med close_connection()

    #Function to send data to server
    #Function to get response from server



    :return: True when message successfully sent, false on error.

     TODO - implement this method
    return False


def read_response_from_server():



def run_client_tests():p
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
    time.sleep(seconds_to_sleep * 1000)

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

