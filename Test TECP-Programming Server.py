from socket import * #Importerer Socket Modulen
def start_server():
    welcome_socket = socket(AF_INET, SOCK_STREAM) #Connecter til sockets hhv. internett og TCP
    welcome_socket.bind(("", 5678)) #Henter IP-addresse og Porten fra clienten
    welcome_socket.listen(1) #1 queue
    print("Server ready for client connections") #Forteller at serveren er klar for å ta imot brukere

    connection_socket, client_address = welcome_socket.accept() #Henter IP-addresse og Porten fra clienten
    print("Client connected from: ",client_address) #Printer sistnevnte

    message = connection_socket.recv(100).decode() #Henter og decoder byte-arrayen fra clienten
    print("Message from client:\n", message) #Printer stringen som ble sendt fra clienten
    response = message.upper() #Lager en respons som er stringen fra clienten bare i blokkbokstaver

    connection_socket.send(response.encode()) #Encoder og sender stringen tilbake til client i form av byte-array

    connection_socket.close() #Avslutter socket for connection
    welcome_socket.close() #Avslutter socket for velkomst
    print("Server shutdown") #Informerer om at serveren er inaktiv


if __name__ == "__main__": #Prox
    start_server()