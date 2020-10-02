from socket import * #Importerer Socket Modulen

global connection_socket

def start_server(): #Function to start the server and let the client connects
    global connection_socket #Global type makes it available for use in functions as a local variable
    server_socket = socket(AF_INET, SOCK_STREAM)  # Connects to sockets: internett and TCP
    server_socket.bind(("", 6666)) #Binds the client to the server
    server_socket.listen(1) #1 spot in queue
    print("Server ready for client connections")
    connection_socket, client_address = server_socket.accept() #Accepts the 3-way handshake
    print("Client connected from: ",client_address) #Prints clients stats

def read_request():
    try:
        global connection_socket #Global type makes it available for use in functions as a local variable
        request_client = connection_socket.recv(1000).decode() #Receives the data from the client
        request = request_client.strip("\n") #Strips newline
        print("Message from server: ",request)
        return request #Returns the list with data from the client
    except ConnectionResetError: #Excepts the connectionreseterror
        print("oops.. something happened")


def send_response(total): #Function to send a respons back to the client
    global connection_socket #Global type makes it available for use in functions as a local variable
    send = str(total) #Changes the datatype from integer to string
    response_server = connection_socket.send(send.encode()) #Sends and encodes the message as byte-array
    print("Message sent to Client: ",send)


def adder(response): #Function to both determine if the response was integers and to detect errors, will always return total
    try:
        total = eval(response) #Uses the eval()-function to determine the integers and mathematical operations.
        #I had problems with splitting the integers and operators, explained in README.
        return total
    except (NameError): #If the input is not accepted in the eval()-function. In other words, the request from the server was not integers
        total = "Wrong format, could not add"
        return total
    except (TypeError): #The same as above?
        total = "Wrong format, could not add"
        return total
    except SyntaxError: #The error that will occur if the client is no longer connected, important!
        print("Client disconnected from Server!")
        return False


def server_function(): #Function to assemble all the other functions #habit from arduino
    request = read_request() #Reads the request from the client
    total = adder(request) #Checks and add the data from the server
    if total == False: ##! If the adder function gets the error that occurs if the client is no longer connected it will return False
        return False #If the client is disconnected this function will return False
    else:
        send_response(total) #Sends the response to the client if it is still connected
        return True






if __name__ == "__main__": #trigger
    start_server()
    while True: #To keep the server check for responses
        check = server_function() #Runs the server-function
        if check == False:#If the client is not connected the server will break.
            print("No contact to Client, closing down the server")
            break
    print("Goodbye!") #Control print to check if it breaks






