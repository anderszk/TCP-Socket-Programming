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

# Were using inputs in case you want to connect to a different port (:
SERVER_HOST = input("Enter the name of the server here: ")  # Server name: datakomm.work
TCP_PORT = int(input("Enter the port you want to connect to: "))  # TCP port: 1300


current_state = "disconnected"  # The current state of the system
# When this variable will be set to false, the application will stop
must_run = True
# Use this variable to create socket connection to the chat server
# Note: the "type: socket" is a hint to PyCharm about the type of values we will assign to the variable
client_socket = None  # type: socket
username = " "


def quit_application(): #TODO ferdig
    global must_run
    must_run = False


def send_command(command, arguments):  # This function will send all the commands from the Client

    global client_socket  # Includes the variable from the global variables
    try:  # Try/Except in case of unwanted errors
        message_to_send = (command + " " + arguments + "\n")  # Formats the command so the server can interpret it
        client_socket.send(
            message_to_send.encode())  # Convert the command to a byte-array and forwards it to the server
        print(message_to_send.encode())  # Prints the command
    except OSError:  # Excepts the OSError in case of unexpected errors; disconnected from server
        print("You're not connected to the server!")
    return None


def read_one_line(sock):  # oppgitt fra girts

    newline_received = False  # Triggers the while-loop
    message = ""  # Sets a local variable to empty
    while not newline_received:
        character = sock.recv(1).decode()  # Recieves and decodes the message from ther server
        if character == '\n':  # Stops the reading when newline appears
            newline_received = True  # Breaks the loop
        elif character == '\r':
            return None
        else:
            message += character  # Adds character to the local function
    return message  # Returns the message-variable when the loop breaks


def get_servers_response():  # Function the read the server response
    try:
        response = client_socket.recv(1024).decode()  # Receives and decodes the message
        return response
    except InterruptedError:  # Excepts the InterruptedError
        print("The reading of the message was interrupted, please try again!")


def connect_to_server():  # This function connects the Client to the Server
    # Includes these global variables to this scope
    global client_socket
    global current_state

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)  # binds the socket stats to a variable, internet,tcp
        client_socket.settimeout(3)  # If the client does not connect to the server within x seconds, it will time out
        client_socket.connect((SERVER_HOST, TCP_PORT))  # Tries to connect to the given Server and Port
        current_state = "connected"  # If connected, change the state to "connected"

        client_socket.send("sync\n".encode())  # Sets the server to sync mode, important to communicate in the right order
        sync_mode_confirmation = get_servers_response()  # Gets response from the server to confirm
        print(sync_mode_confirmation)

    except IOError:  # Excepts the input/output error
        print("Failed to connect to server")
        current_state = "disconnected"  # Sets the state to disconnected as the client has failed to connect


def disconnect_from_server():  # This function disconnects the Client from the Server
    # includes these global variables to the scope
    global client_socket
    global current_state

    client_socket.close()  # Closes the connection to the server
    current_state = "disconnected"  # Sets the state to disconnected
    return None  # Returns nothing


def login():  # Function to login/get authorized/choose username
    # Includes these global variables in the scope
    global current_state
    global username

    username = input("Choose a username: ")  # Input to chose your username

    send_command("login", username)  # Sends the command to the server
    login_response = get_servers_response()  # Server gives you a response
    login_response.strip("\n")

    # If statements to compare the response to expected answers,
    # "loginok" is the only response that will authorize the user to use the server
    s = login_response
    if s == "loginok":
        print("Login successful!")
        current_state = "authorized"  # Sets the state to authorized as you are now able to use the server
    elif s == "loginerr username already in use":
        print("The username is already in use, please try again.. ")
        login()  # Restarts the function if it fails
    elif s == "loginerr incorrect username format":
        print("Try using normal characters, not the weird norwegian ones.. ")
        login()  # Restarts the function if it fails

    return None  # The function will return nothing


def send_public_message(): #TODO Ferdig?
    message = input("Writing to (Public): ")
    send_command("msg", message)
    #print(get_servers_response)
    return None


def send_private_message(): #TODO Har endret mye her på tekstene, FERDIG!
    print(f"You are logged in as: '{username}'")
    user_to_send_to = input("Choose recipient: ")
    message = input(f"Writing to ({user_to_send_to}): ")
    send_command("privmsg", f"{user_to_send_to} has recieved message from '{username}': {message}")
    #print(get_servers_response())
    return None


def get_user_list(): #TODO kan gjøres mer original
    client_socket.send("users\n".encode())
    print("Online users: ")
    user_list = (get_servers_response())
    print(user_list.replace(" ", "\n"))
    return None


#TODO inbox <N>
#TODO msg <sender> <msg 1>
#TODO ...
#TODO [priv]msg <sender> <msg N>

def read_inbox(): #TODO ignorer denne..
    client_socket.send("inbox\n".encode())
    lines = []
    var = 0
    try:
        while True:
            reply = read_one_line(client_socket)
            if reply == "msgok 1":
                var += 1

            lines.append(reply)
    except:
        print(f"Dette er lines listen: {lines}")
        inbox_reply = lines[1].strip("inbox")
        print(f"Number of messages in inbox: {inbox_reply}")

        for i in range(2, len(lines)):
            line = lines[i].replace("msg", "(Public): ")
            line = lines[i].replace("privmsg", "(Private): ")
            print(f"{line}\n")



    return None


def joke():
    send_command("joke", "")
    joke_ans = get_servers_response()
    print(joke_ans.replace("joke", "Here is the joke:\n\n" ))


#TODO =================================================
#TODO       ALT UNDER HER ER OPPGITT MENER JEG..
#TODO =================================================

"""
The list of available actions that the user can perform
Each action is a dictionary with the following fields:
description: a textual description of the action
valid_states: a list specifying in which states this action is available
function: a function to call when the user chooses this particular action. The functions must be defined before
            the definition of this variable
"""
available_actions = [
    {
        "description": "Connect to a chat server",
        "valid_states": ["disconnected"],
        "function": connect_to_server
    },
    {
        "description": "Disconnect from the server",
        "valid_states": ["connected", "authorized"],
        "function": disconnect_from_server
    },
    {
        "description": "Authorize (log in)",
        "valid_states": ["connected", "authorized"],
        # TODO Step 5 - implement login
        # Hint: you will probably want to create a new function (call it login(), or authorize()) and
        # reference that function here.
        # Hint: you can ask the user to enter the username with input("Enter username: ") function.
        # Hint: the login function must be above this line, otherwise the available_actions will complain that it can't
        # find the function
        # Hint: you can reuse the send_command() function to send the "login" command
        # Hint: you probably want to change the state of the system: update value of current_state variable
        # Hint: remember to tell the function that you will want to use the global variable "current_state".
        # Hint: if the login was unsuccessful (loginerr returned), show the error message to the user
        "function": login

    },
    {
        "description": "Send a public message",
        "valid_states": ["connected", "authorized"],
        # TODO Step 6 - implement sending a public message
        # Hint: ask the user to input the message from the keyboard
        # Hint: you can reuse the send_command() function to send the "msg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not
        "function": send_public_message
    },
    {
        "description": "Send a private message",
        "valid_states": ["authorized"],
        # TODO Step 8 - implement sending a private message
        # Hint: ask the user to input the recipient and message from the keyboard
        # Hint: you can reuse the send_command() function to send the "privmsg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not
        "function": send_private_message
    },
    {
        "description": "Read messages in the inbox",
        "valid_states": ["connected", "authorized"],
        # TODO Step 9 - implement reading messages from the inbox.
        # Hint: send the inbox command, find out how many messages there are. Then parse messages
        # one by one: find if it is a private or public message, who is the sender. Print this
        # information in a user friendly way
        "function": read_inbox
    },
    {
        "description": "See list of users",
        "valid_states": ["connected", "authorized"],
        # TODO Step 7 - Implement getting the list of currently connected users
        # Hint: use the provided chat client tools and analyze traffic with Wireshark to find out how
        # the user list is reported. Then implement a function which gets the user list from the server
        # and prints the list of usernames
        "function": get_user_list
    },
    {
        "description": "Get a joke",
        "valid_states": ["connected", "authorized"],
        # TODO - optional step - implement the joke fetching from the server.
        # Hint: this part is not described in the protocol. But the command is simple. Try to find
        # out how it works ;)
        "function": joke
    },
    {
        "description": "Quit the application",
        "valid_states": ["disconnected", "connected", "authorized"],
        "function": quit_application
    },
]


def run_chat_client():
    """ Run the chat client application loop. When this function exists, the application will stop """

    while must_run:
        print_menu()
        action = select_user_action()
        perform_user_action(action)
    print("Thanks for watching. Like and subscribe! 👍")


def print_menu():
    """ Print the menu showing the available options """
    print(current_state)
    print("==============================================")
    print("What do you want to do now? ")
    print("==============================================")
    print("Available options:")
    i = 1
    for a in available_actions:
        if current_state in a["valid_states"]:
            # Only hint about the action if the current state allows it
            print("  %i) %s" % (i, a["description"]))
        i += 1
    print()


def select_user_action():
    """
    Ask the user to choose and action by entering the index of the action
    :return: The action as an index in available_actions array or None if the input was invalid
    """
    number_of_actions = len(available_actions)
    hint = "Enter the number of your choice (1..%i):" % number_of_actions
    choice = input(hint)
    # Try to convert the input to an integer
    try:
        choice_int = int(choice)
    except ValueError:
        choice_int = -1

    if 1 <= choice_int <= number_of_actions:
        action = choice_int - 1
    else:
        action = None

    return action


def perform_user_action(action_index):
    """
    Perform the desired user action
    :param action_index: The index in available_actions array - the action to take
    :return: Desired state change as a string, None if no state change is needed
    """
    if action_index is not None:
        print()
        action = available_actions[action_index]
        if current_state in action["valid_states"]:
            function_to_run = available_actions[action_index]["function"]
            if function_to_run is not None:
                function_to_run()
            else:
                print("Internal error: NOT IMPLEMENTED (no function assigned for the action)!")
        else:
            print("This function is not allowed in the current system state (%s)" % current_state)
    else:
        print("Invalid input, please choose a valid action")
    print()
    return None


# Entrypoint for the application. In PyCharm you should see a green arrow on the left side.
# By clicking it you run the application.
if __name__ == '__main__':
    run_chat_client()