# A Simple TCP server, used as a warm-up exercise for assignment A3
from socket import * #Importerer Socket Modulen

def string_to_int(string, n):  # n = hvilket tall du vil ha, første tallet i stringen? n = 1!
    numbers = [int(i) for i in string.split() if i.isdigit()]
    return numbers[n - 1]



def run_server():
    # TODO - implement the logic of the server, according to the protocol.
    # Take a look at the tutorial to understand the basic blocks: creating a listening socket,
    # accepting the next client connection, sending and receiving messages and closing the connection
    print("Starting TCP server...")
    welcome_socket = socket(AF_INET, SOCK_STREAM) #Connecter til sockets hhv. internett og TCP
    welcome_socket.bind(("localhost", 1300)) #Henter IP-addresse og Porten fra clienten
    welcome_socket.listen(1) #1 queue
    print("Server ready for client connections") #Forteller at serveren er klar for å ta imot brukere


    connection_socket, client_address = welcome_socket.accept() #Henter IP-addresse og Porten fra clienten
    print("Client connected from: ",client_address) #Printer sistnevnte

    # message = connection_socket.recv(100).decode() #Henter og decoder byte-arrayen fra clienten
    # print("Message from client:\n", message) #Printer stringen som ble sendt fra clienten
    # response = message.upper() #Lager en respons som er stringen fra clienten bare i blokkbokstaver
    # connection_socket.send(response.encode()) #Encoder og sender stringen tilbake til client i form av byte-array

    while True:
        matte = connection_socket.recv(100).decode() #Henter og decoder byte-arrayen fra clienten
        print("Message from client:\n", matte) #Printer stringen som ble sendt fra clienten
        resultat = "Server: " + str(string_to_int(matte, 1) + string_to_int(matte, 2))
        connection_socket.send(resultat.encode()) #Encoder og sender stringen tilbake til client i form av byte-array



    if 0 > 1: #TODO legg ved condition.
        connection_socket.close() #Avslutter socket for connection
        welcome_socket.close() #Avslutter socket for velkomst
        print("Server shutdown") #Informerer om at serveren er inaktiv


# Main entrypoint of the script
if __name__ == '__main__':
    run_server()