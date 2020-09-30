from socket import * #Importerer Socket Modulen

global connection_socket

def start_server():
    global connection_socket
    server_socket = socket(AF_INET, SOCK_STREAM)  # Connecter til sockets hhv. internett og TCP
    server_socket.bind(("", 666)) #Henter IP-addresse og Porten fra clienten
    server_socket.listen(1) #1 queue
    print("Server ready for client connections") #Forteller at serveren er klar for å ta imot brukere
    connection_socket, client_address = server_socket.accept() #Henter IP-addresse og Porten fra clienten
    print("Client connected from: ",client_address) #Printer sistnevnte

def read_request():
    global connection_socket
    request_client = connection_socket.recv(1000).decode()
    request_decoded = request_client.strip("\n")
    request = request_decoded.strip("+")
    print("Message from server: ",request)
    return request #Returnerer liste med

def send_response(total):
    global connection_socket
    send = str(total)
    response_server = connection_socket.send(send.encode())
    print("Message sent to server")

def server_function():
    request = read_request()
    total = adder(request)
    print("The two integers added sums to:",total)
    send_response(total)

def adder(response):
    total = eval(response)
    return total




if __name__ == "__main__": #Prox
    start_server()
    while True:
        server_function()
#else:
    #print("Something went wrong!")


