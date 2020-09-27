# Pseudokode for TCP-Programmering Warm-up exercise

from socket import * #Importerer Socket Modulen

HOST = input("What is the Host you want to connect to?: ") #Input for hostname du vil connecte til
PORT = int(input("What is the Port you want to connect to?: ")) #Input for portnummer du vil connecte til


def read_one_line(client_socket):
    newline_received = False
    message = ""
    while newline_received == False:
        character = client_socket.recv(1).decode()
        if character == "\n":
            newline_received = True
        elif character == "\r":
            pass
        else:
            message += character
    return message


def process_response(one_line):
    print("Server response:\n", one_line)


def start_client(name_host, name_port):
    client_socket = socket(AF_INET, SOCK_STREAM) #Setter sockets hhv. internett og TCP.
    client_socket.connect((name_host, name_port)) #Connecter til Sockets med inputs som ble spurt om tidligere

    command_to_send = input("Message to send: ") #Sender en string til serveren
    cmd_as_bytes = command_to_send.encode() #Encoder stringen til byte-array
    client_socket.send(cmd_as_bytes) #Sender byte-arrayen til serveren


    one_line = "Invalid"
    while one_line != "":
        one_line = read_one_line(client_socket)
        if one_line != "":
            process_response(one_line)
    client_socket.close()  # Stenger/Avslutter tilkoblingen

    #response = client_socket.recv(1000) #Etter serveren har svart henter denne funksjonen responsen i form av byte-array
    #response_string = response.decode() #Decoder byte-arrayen til string
    #print("The response from the server:\n", response_string) #Printer stringer i console




start_client(HOST, PORT) #Prox

#Printen fungerer ikke fra server response
