'''# *************************************************************
#                           2018
# *************************************************************
#
#                           CLIENT
#
# *************************************************************'''


# Import function from socket module
# from socket import *
import socket
import sys


# FUNCTION: Receive from the socket and return decode the message
def commRX(socket):
    message = socket.recv(bufsize)
    coded = message.decode(code)
    return coded


# FUNCTION: Transmision of any message
def commTX(message, socket):
    coded = message.encode(code)
    socket.send(coded)


code = "utf-8"
host = socket.gethostname()
port = 6666
address = (host, port)
bufsize = 1024
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(address)
except OSError:
    print("Error open socket")
    server.close()
    sys.exit(1)
else:
    while True:
        print("\n\n", "_"*70, "\n\n")
        message = commRX(clientSocket)
        if(message == "6"):
            print("Disconnecting from server ... ")
            print("\n\n", "_"*70, "\n")
            break
        else:
            print(message)
            message = input("")
            if(message == ""):
                message = "<EnterKey>"
            commTX(message, clientSocket)
    clientSocket.close()
