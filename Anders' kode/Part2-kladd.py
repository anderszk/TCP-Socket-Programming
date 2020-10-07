#############################################
# A3 - TCP-Programming, Group 11, IELET2001 #
#############################################

from socket import *
import time


states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]

#Were using inputs in case you want to connect to a different port (:
SERVER_HOST = input("Enter the name of the server here: ") #Server name: datakomm.work
TCP_PORT = int(input("Enter the port you want to connect to: "))  #TCP port: 1300


current_state = "disconnected"  # The current state of the system
# When this variable will be set to false, the application will stop
must_run = True
# Use this variable to create socket connection to the chat server
# Note: the "type: socket" is a hint to PyCharm about the type of values we will assign to the variable
client_socket = None  # type: socket
username = " "


def quit_application(): #This function will disconnect the client from the server
    global must_run #Includes must_run from the global variables
    must_run = False #Sets the boolean value to False


def send_command(command, arguments): #This function will send all the commands from the Client

    global client_socket #Includes the variable from the global variables
    try: #Try/Except in case of unwanted errors
        message_to_send = (command + " " + arguments + "\n") #Formats the command so the server can interpret it
        client_socket.send(message_to_send.encode()) #Convert the command to a byte-array and forwards it to the server
        print(message_to_send.encode()) #Prints the command
    except OSError: #Excepts the OSError in case of unexpected errors; disconnected from server
        print("You're not connected to the server!")
    return None


def read_one_line(sock): # oppgitt fra girts

    newline_received = False #Triggers the while-loop
    message = "" #Sets a local variable to empty
    while not newline_received:
        character = sock.recv(1).decode() #Recieves and decodes the message from ther server
        if character == '\n': #Stops the reading when newline appears
            newline_received = True #Breaks the loop
        elif character == '\r':
            return None
        else:
            message += character #Adds character to the local function
    return message #Returns the message-variable when the loop breaks


def get_servers_response(): #Function the read the server response
    try:
        return client_socket.recv(1024).decode() #Receives and decodes the message
    except InterruptedError: #Excepts the InterruptedError
        print("The reading of the message was interrupted, please try again!")


def connect_to_server(): #This function connects the Client to the Server
    #Includes these global variables to this scope
    global client_socket
    global current_state

    try:
        with client_socket as s:
        s = socket(AF_INET, SOCK_STREAM) #binds the socket stats to a variable, internet,tcp
        s.settimeout(3) #If the client does not connect to the server within x seconds, it will time out
        s.connect((SERVER_HOST, TCP_PORT)) #Tries to connect to the given Server and Port
        current_state = "connected" #If connected, change the state to "connected"

        s.send("sync\n".encode()) #Sets the server to sync mode, important to communicate in the right order
        sync_mode_confirmation = get_servers_response() #Gets response from the server to confirm
        print(sync_mode_confirmation)

    except IOError: #Excepts the input/output error
        print("Failed to connect to server")
        current_state = "disconnected" #Sets the state to disconnected as the client has failed to connect


def disconnect_from_server(): #This function disconnects the Client from the Server
    #includes these global variables to the scope
    global client_socket
    global current_state

    client_socket.close() #Closes the connection to the server
    current_state = "disconnected" #Sets the state to disconnected
    return None #Returns nothing


def login_to_server(): #Function to login/get authorized/choose username
    #Includes these global variables in the scope
    global current_state
    global username

    username = input("Choose a username: ") #Input to chose your username

    send_command("login", username) #Sends the command to the server
    login_answer = get_servers_response() #Server gives you a response
    login_answer.strip("\n")

    #If statements to compare the response to expected answers, "loginok" is the only response that will authorize the user to use the server
    with login_answer as s:
        if s == "loginok":
            print("Login successful!")
            current_state = "authorized" #Sets the state to authorized as you are now able to use the server
        elif s == "loginerr username already in use":
            print("The username is already in use, please try again.. ")
            login_to_server() #Restarts the function if it fails
        elif s == "loginerr incorrect username format":
            print("Try using normal characters, not the weird norwegian ones.. ")
            login_to_server() #Restarts the function if it fails

    return None #The function will return nothing