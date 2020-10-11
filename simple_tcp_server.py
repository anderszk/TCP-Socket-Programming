# A Simple TCP server, used as a warm-up exercise for assignment A3
from socket import *
import threading

welcome_socket = None
connection_socket = None

PORT = 10555


def handle_next_client(connection_socket, client_id):
    need_to_run = True
    while need_to_run:
        request = read_request_from_client(client_id)

        if request == "Shutdown":
            pass
        else:
            print("The response back to client #%i: %s" % (client_id, request))
            response = str(request)
            if not send_response_back_to_client(response):
                return "ERROR: Failed to send valid message to client!"


def read_request_from_client(client_id):
    global connection_socket
    request_from_client = connection_socket.recv(100).decode()

    if ("game" and "over" or "Game" and "Over") in request_from_client:
        print("The request from client #%i: %s" % (client_id, request_from_client))
        connection_socket.close()
        print("Client #%i" % client_id, "disconnected")
        print("Server shutdown")
        return "Shutdown"

    else:
        request_from_client_list = []
        request_from_client_list = request_from_client.split("+")
        a = request_from_client_list[0]
        b = request_from_client_list[1]
        print("The request from client #%i: %s" % (client_id, a + "+" + b))

        try:
            sum_client = int(a) + int(b)
            # total = eval(request_client)
            return sum_client
        except TypeError as t:
            print("Wrong format: ", t)
            return "Error"
        except NameError as n:
            print("Wrong format: ", n)
            return "Error"
        except SyntaxError as s:
            print("Wrong format: ", s)
            return "Error"
        except ValueError as v:
            print("Wrong format: ", v)
            return "Error"




def send_response_back_to_client(response):
    global connection_socket

    if response == "":
        pass

    else:
        try:
            connection_socket.send(response.encode())
            return True
        except TypeError as t:
            print("Wrong format", t)
            return False
        except AttributeError as a:
            print("Wrong format", a)
            return False
        except OSError as o:
            return False



def run_server():
    global welcome_socket
    global connection_socket
    global PORT

    print("Starting TCP server...")
    welcome_socket = socket(AF_INET, SOCK_STREAM)

    welcome_socket.bind(("", PORT))
    welcome_socket.listen(1)
    print("Server ready for client connections")

    need_to_run = True
    client_id = 1
    while need_to_run:
        connection_socket, client_address = welcome_socket.accept()
        print("Client #%i connected " % client_id)
        client_thread = threading.Thread(target=handle_next_client, args=(connection_socket, client_id))

        client_id += 1
        client_thread.start()

    welcome_socket.close()
    print("Server shutdown ")


# Main entrypoint of the script
if __name__ == '__main__':
    run_server()
