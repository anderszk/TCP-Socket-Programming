#################################################
# GRUPPE 11,    A3 - TCP-PROGRAMMING,   PART: 2 #
#################################################

import time
import random
from socket import *

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------


# The states that the application can be in
states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]


SERVER_HOST = input("Please enter the name of the server you want to connect to: ") # Set this to either hostname (domain) or IP address of the chat server
TCP_PORT = int(input("Please enter the Port you want to connect to: ")) # TCP port used for communication


# ------------------------------------------------------------
# State variables
# ------------------------------------------------------------


current_state = "disconnected"  # The current state of the system
# When this variable will be set to false, the application will stop
must_run = True
# Use this variable to create socket connection to the chat server
# Note: the "type: socket" is a hint to PyCharm about the type of values we will assign to the variable
client_socket = None  # type: socket


def quit_application():
    """ Update the application state so that the main-loop will exit """
    # Make sure we reference the global variable here. Not the best code style,
    # but the easiest to work with without involving object-oriented code
    global must_run
    must_run = False

def login(a, b):
    global client_socket
    global current_state
    a = login #Default command to indicate login
    b = int(input("Enter your username here: "))



    print("You have chosen the username: ", arguments)
    print("Checking if username is available...")
    username_control = command + arguments
    controlprint_login = client_socket.send(username_control.encode())
    print("Message sent to server: ")


def send_command(command, arguments): #Can be used given that the current_state == "Authorized"
    global client_socket
    try:
        if "msg" in command:
            #
        elif "privmsg" in command:
            #
        elif "help" in command:
            #
        elif "inbox" in command:
            #
        else:
            print("cmderr command not supported")

    except NameError:
        print("Invalid format, please try again!")
    except TypeError:
        print("Invalid format, please try again!")
    except OSError:
        print("Failed to execute your command, client is not connected")


def read_one_line(sock):
    """
    Read one line of text from a socket
    :param sock: The socket to read from.
    :return:
    """
    newline_received = False
    message = ""
    while not newline_received:
        character = sock.recv(1).decode()
        if character == '\n':
            newline_received = True
        elif character == '\r':
            pass
        else:
            message += character
    return message


def get_servers_response():
    """
    Wait until a response command is received from the server
    :return: The response of the server, the whole line as a single string
    """
    # TODO Step 4: implement this function
    # Hint: reuse read_one_line (copied from the tutorial-code)
    return None


def connect_to_server(SERVER_HOST,TCP_PORT):
    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state

    try:
        client_socket.connect((SERVER_HOST, TCP_PORT))  # Connecter til Sockets med inputs som ble spurt om tidligere
        client_socket.settimeout(3)  # Gives an error if the client fails to connect to the server within 3 seconds
        current_state = "connected"
        print("You have connected to the server, waiting for Authorization...")

    except IOError:
        current_state = "disconnected"
        print("Something went wrong!")
        time.sleep(1)


    if current_state = "connected":
        #send_command(sync)?

    authorization_response = get_servers_response()

    if authorization_response == "modeok":
        print("You are now Authorized and can send commands to the server")
        current_state = "Authorized"
        #send_command(async)?


def disconnect_from_server():
    #Global variables
    global client_socket
    global current_state

    try:
        client_socket.close()
        print("You have now disconnected from the server")
        current_state = "disconnected"

    except:
        print("Something went wrong")


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
        "function": None
    },
    {
        "description": "Send a public message",
        "valid_states": ["connected", "authorized"],
        # TODO Step 6 - implement sending a public message
        # Hint: ask the user to input the message from the keyboard
        # Hint: you can reuse the send_command() function to send the "msg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not
        "function": None
    },
    {
        "description": "Send a private message",
        "valid_states": ["authorized"],
        # TODO Step 8 - implement sending a private message
        # Hint: ask the user to input the recipient and message from the keyboard
        # Hint: you can reuse the send_command() function to send the "privmsg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not
        "function": None
    },
    {
        "description": "Read messages in the inbox",
        "valid_states": ["connected", "authorized"],
        # TODO Step 9 - implement reading messages from the inbox.
        # Hint: send the inbox command, find out how many messages there are. Then parse messages
        # one by one: find if it is a private or public message, who is the sender. Print this
        # information in a user friendly way
        "function": None
    },
    {
        "description": "See list of users",
        "valid_states": ["connected", "authorized"],
        # TODO Step 7 - Implement getting the list of currently connected users
        # Hint: use the provided chat client tools and analyze traffic with Wireshark to find out how
        # the user list is reported. Then implement a function which gets the user list from the server
        # and prints the list of usernames
        "function": None
    },
    {
        "description": "Get a joke",
        "valid_states": ["connected", "authorized"],
        # TODO - optional step - implement the joke fetching from the server.
        # Hint: this part is not described in the protocol. But the command is simple. Try to find
        # out how it works ;)
        "function": None
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
