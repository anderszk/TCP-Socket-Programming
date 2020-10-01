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
    try:
        global connection_socket
        request_client = connection_socket.recv(1000).decode()
        request = request_client.strip("\n")
        print("Message from server: ",request)
        return request #Returnerer liste med
    except ConnectionResetError:
        print("oops.. something happened")


def send_response(total):
    try:
        global connection_socket
        send = str(total)
        response_server = connection_socket.send(send.encode())
        print("Message sent to Client")


def server_function():
    request = read_request()
    total = adder(request)
    print("The two integers added sums to:",total)
    send_response(total)
    return total

def adder(response):

    try:
        total = eval(response)
        return total
    except (NameError):
        total = "Wrong format, could not add"
        return total
    except (TypeError):
        total = "Wrong format, could not add"
        return total
    except SyntaxError:
        print("Client disconnected from Server!")
        return False


if __name__ == "__main__": #Prox
    start_server()
    while True:
        server_function()
        if adder("nothing") == False:
            break;
    print("Goodbye!")






