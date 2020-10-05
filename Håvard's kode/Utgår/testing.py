import random
import time
from socket import *



def send_request_to_server(request):

    is_request_int = request_strip.split("+")
    is_request_int2 = is_request_int.split()

    if isinstance(is_request_int2[0], int) == True:  #x > 0:
        request_strip = request.strip(" ")
        split = request_strip.split()
        split_send = []
        #print(split)
        for i in split:
            split_send.append(i+'\n')

        try:
            for u in split_send:
                client_socket.send(u.encode())

            return True
        except:
            return False
    else:
        try:
            client_socket.send(request.encode())
            return True
        except:
            print("send_request to server, was not number and did not send message. exception: line 63.")
            return False



a = random.randint(1, 20)
b = random.randint(1, 20)
request = str(a) + "+" + str(b)

is_request_int = request.split("+")
#is_request_int2 = is_request_int.split()

print(f"Request før tull: {request}")
print(is_request_int)
print(is_request_int[0].isdigit())


#send_request_to_server(request)
