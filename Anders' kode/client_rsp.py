#############################################
# A3 - TCP-Programming, Group 11, IELET2001 #
#############################################

from socket import *
import random
import time


looper = True
run = True
randint = 0
computer_command = ""
r = "ROCK"
s = "SCISSORS"
p = "PAPER"


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


def computers_choice():
  global computer_command
  random_integer = random.randint(1,3)
  if random_integer == 1:
    computer_command = "Rock"
  elif random_integer == 2:
    computer_command = "Scissors"
  elif random_integer == 3:
    computer_command = "Paper"
  else:
    print("Something went wrong!")

def game():
  global looper, run, computer_command, r, s, p
  print("================================\n\tGAME RULES!\n================================")
  print('Enter "Rock" if you have to play as rock')
  print('Enter "Scissors" if you want to play as scissors')
  print('Enter "Paper" if you want to play as paper')
  print('Enter "Quit" if you want to quit the game\n')

  while run == True:
    command = input("Enter you command here!: ")
    command_check = command.upper()

    if command_check in ["ROCK", "SCISSORS", "PAPER"]:
      computers_choice()

      if command_check == computer_command.upper():
        print("\nIts a Draw!".upper())
        print("\nYou chose:",command,"\nThe computer chose:",computer_command,"\n")
      elif (command_check in "ROCK" and computer_command.upper() in "SCISSORS") or (command_check in "PAPER" and computer_command.upper() in "ROCK") or (command_check in "SCISSORS" and computer_command.upper() in "PAPER"):
        print("\nYou won the game!".upper())
        print("\nYou chose:",command,"\nThe computer chose:",computer_command,"\n")
      elif (computer_command.upper() in "ROCK" and command_check in "SCISSORS") or (computer_command.upper() in "PAPER" and command_check in "ROCK") or (computer_command.upper() in "SCISSORS" and command_check in "PAPER"):
        print("\nYou lost the game!".upper())
        print("\nYou chose:",command,"\nThe computer chose:",computer_command,"\n")

    elif command_check == 'QUIT':
      run = False

    else:
      pass

def rock_scissors_paper():
  global run, looper
  run = True
  game()
  while looper == True:
    restart = input('\nEnter: "Play game" if you want to play again!\nor "Back to server" if you want to go back to the server!: ')
    restart_check = restart.upper()
    if restart_check == "PLAY GAME":
      run = True
      game()
    elif restart_check == "BACK TO SERVER":
      break
    else:
      pass


def quit_application(): #TODO ferdig
    global must_run
    must_run = False


def send_command(command, arguments):  # This function will send all the commands from the Client

    global client_socket  # Includes the variable from the global variables
    try:  # Try/Except in case of unwanted errors
        message_to_send = (command + " " + arguments + "\n")  # Formats the command so the server can interpret it
        client_socket.send(
            message_to_send.encode())  # Convert the command to a byte-array and forwards it to the server
        #print(message_to_send.encode())  # Prints the command
    except OSError:  # Excepts the OSError in case of unexpected errors; disconnected from server
        print("You're not connected to the server!")
    return None


def read_one_line(sock): #TODO Oppgitt fra girts, trur æ..

    try:
        newline_received = False # Triggers the while-loop
        message = "" # Sets a local variable to empty
        while not newline_received:
            character = sock.recv(1).decode() # Recieves and decodes the message from ther server
            if character == '\n': # Stops the reading when newline appears
                newline_received = True # Breaks the loop
            elif character == '\r':
                pass
            else:
                message += character # Adds character to the local function
        return message # Returns the message-variable when the loop breaks

    except:
        return False #alerts that it timed-out.


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
    s = login_response.strip("\n")

    # If statements to compare the response to expected answers,
    # "loginok" is the only response that will authorize the user to use the server
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


def send_public_message():
    message = input("Writing to (Public): ")
    send_command("msg", message)
    #print(get_servers_response)
    return None


def send_private_message():
    print(f"You are logged in as: '{username}'")
    user_to_send_to = input("Choose recipient: ")
    message = input(f"Writing to ({user_to_send_to}): ")
    send_command("privmsg", f"{user_to_send_to} has recieved message from '{username}': {message}")
    #print(get_servers_response())
    return None


def get_user_list():
    client_socket.send("users\n".encode())
    print("Online users: ")
    user_list = (get_servers_response())
    print(user_list.replace(" ", "\n"))
    return None

def read_inbox():
    client_socket.send("inbox\n".encode())
    lines = []
    reply = True
    while reply is not False:
        reply = read_one_line(client_socket)
        if 'msgok' in str(reply) or reply == False:
            pass
        else:
            lines.append(reply)
    boarder = "=" * 25 + "<INBOX>" + "=" * 25
    inbox_reply = lines[0].strip("inbox")
    print(f"{boarder} \n| Number of messages in inbox: {inbox_reply} \n|")

    for i in range(1, len(lines)):
        line = lines[i].replace("privmsg", "| (Private): ")
        print(f'{line.replace("msg", "| (Public): ")}')
    print(boarder)
    return None

def joke():
    send_command("joke", "")
    joke_ans = get_servers_response()
    print(joke_ans.replace("joke", "Here is the joke:\n"))


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
{
        "description": "Play Rock/Paper/Scissors with bot!",
        "valid_states": ["disconnected", "connected", "authorized"],
        "function": rock_scissors_paper
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
