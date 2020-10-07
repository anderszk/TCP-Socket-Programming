#################################################################################
# A Chat Client application. Used in the course IELEx2001 Computer networks, NTNU
#################################################################################

from socket import *
import time

# --------------------
# Constants
# --------------------
# The states that the application can be in
states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]
TCP_PORT = 1300  # TCP port used for communication
SERVER_HOST = "datakomm.work"  # Set this to either hostname (domain) or IP address of the chat server

# --------------------
# State variables
# --------------------
current_state = "disconnected"  # The current state of the system
# When this variable will be set to false, the application will stop
must_run = True
# Use this variable to create socket connection to the chat server
# Note: the "type: socket" is a hint to PyCharm about the type of values we will assign to the variable
client_socket = None  # type: socket
username = " "


def quit_application():
    """ Update the application state so that the main-loop will exit """
    # Make sure we reference the global variable here. Not the best code style,
    # but the easiest to work with without involving object-oriented code
    global must_run
    must_run = False


def send_command(command, arguments):
    """
    Send one command to the chat server.
    :param command: The command to send (login, sync, msg, ...(
    :param arguments: The arguments for the command as a string, or None if no arguments are needed
        (username, message text, etc)
    :return:
    """
    global client_socket
    message_to_send = (command + " " + arguments + "\n")
    client_socket.send(message_to_send.encode())
    print(message_to_send.encode())
    # TODO: Implement this (part of step 3)
    # Hint: concatenate the command and the arguments
    # Hint: remember to send the newline at the end
    pass


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
    return client_socket.recv(1000).decode()


def connect_to_server():
    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state

    # TODO Step 1: implement connection establishment
    # Hint: create a socket, connect, handle exceptions, then change current_state accordingly

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.settimeout(3)
        client_socket.connect((SERVER_HOST, TCP_PORT))
        current_state = "connected"

        # TODO Step 3: switch to sync mode
        # Hint: send the sync command according to the protocol
        # Hint: create function send_command(command, arguments) which you will use to send this and all other commands
        # to the server
        client_socket.send("sync\n".encode())
        sync_mode_confirmation = get_servers_response()
        print(sync_mode_confirmation)

    except IOError:
        print("Failed to connect to server")
        current_state = "disconnected"

    # TODO Step 4: wait for the servers response and find out whether the switch to SYNC mode was successful
    # Hint: implement the get_servers_response function first - it should wait for one response command from the server
    # and return the server's response (we expect "modeok" response here). This get_servers_response() function
    # will come in handy later as well - when we will want to check the server's response to login, messages etc
    #print("CONNECTION NOT IMPLEMENTED!")


def disconnect_from_server():
    # TODO Step 2: Implement disconnect
    # Hint: close the socket, handle exceptions, update current_state accordingly

    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state
    client_socket.close()
    current_state = "disconnected"
    pass


def login_to_server():
    global current_state
    global username
    username = input("Choose a username: ")
    # send_command(None, "login" + username)
    # login_message = "login " + username + "\n"
    send_command("login", username)
    login_answer = get_servers_response()
    new_login_answer = login_answer.replace("\n", "")
    print(login_answer)

    if new_login_answer == "loginok":
        print("Login succesful!")
        current_state = "authorized"
    if new_login_answer == "loginerr username already in use":
        print("The username is allready in use, try another one.. ")
        login_to_server()
    if new_login_answer == "loginerr incorrect username format":
        print("Try using normal characters, not the weird norwegian ones.. ")
        login_to_server()

    return None


def send_public_message():
    message = input("Writing to (Public): ")
    send_command("msg", message)
    print(get_servers_response)
    return None


def send_private_message():
    print(f"You are logged in as: '{username}'")
    user_to_send_to = input("Choose recipient: ")
    message = input(f"Writing to ({user_to_send_to}): ")
    send_command("privmsg", f"{user_to_send_to} <-- has recieved message from '{username}': {message}")
    print(get_servers_response())
    return None


def get_user_list():
    client_socket.send("users\n".encode())
    print("Online users: ")
    user_list = (get_servers_response())
    print(user_list.replace(" ", "\n"))
    return None




def read_inbox():
    client_socket.send("inbox\n".encode())
    #    number_of_messages = inbox_reply.replace("inbox ", "").replace("\n", "")
    #    print("Number of messages: ", number_of_messages)
    message_reply = "123"
    while message_reply != "":
        message_reply = read_one_line(client_socket)
        print(message_reply)
        if "inbox 0" in message_reply:
            print("No messages")
            return None

        message_reply = read_one_line(client_socket)
        if "privmsg" in message_reply:
            private_messages = message_reply.replace("privmsg", "")
            print("Private message:")
            print(private_messages)
            return None
        if "privmsg" not in message_reply:
            public_message = message_reply.replace("msg", "")
            print("Public message:")
            print(public_message)
            return None

    return None


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
        "function": login_to_server

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
