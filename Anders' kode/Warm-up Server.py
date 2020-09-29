from socket import * #Importerer Socket Modulen
server_socket = socket(AF_INET, SOCK_STREAM) #Connecter til sockets hhv. internett og TCP

def start_server():
    global server_socket
    server_socket.bind(("", 5678)) #Henter IP-addresse og Porten fra clienten
    server_socket.listen(1) #1 queue
    print("Server ready for client connections") #Forteller at serveren er klar for å ta imot brukere
    connection_socket, client_address = server_socket.accept() #Henter IP-addresse og Porten fra clienten
    print("Client connected from: ",client_address) #Printer sistnevnte

def read_request():
    global server_socket
    request_client = server_socket.recv(1000).decode()
    request_decoded = request_client.strip("\n")
    request = request_decoded.strip("+")
    return request #Returnerer liste med

def send_response(total):
    global server_socket
    try:
        response_server = server_socket.send(total.encode())
    except:
        "Failed to send response"


def server_function():
    request = read_request()
    total = add_or_quit(request)
    print("The two integers added sums to: ",add)
    send_response(total)



if __name__ == "__main__": #Prox
    start_server()
    while True:
        server_function()
else:
    print("Something went wrong!")


