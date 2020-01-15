#python path bs
'''
Python library for launching a simple websocket chat
WARNING: i stole ~90% of this code from the internet so be warned
'''

import netmap
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
	'''multiple client handling'''
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to DEVchat! please enter a name.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    '''Handles a single client connection'''

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'user {}connected. type {quit} to exit.'.format(name)
    client.send(bytes(welcome, "utf8"))
    msg = "{} has joined the chat!".format(name)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("{} has left the chat.".format(name), "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
while True:
	print("Welcome to DEVchat server v1.1.0")
	print("Please enter a valid port number between 1024 and 65535")
	PORT = int(input))
	if PORT>1024 and PORT<65535:
		break
	else:
		print("Please enter a valid port number.\n")
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


SERVER.listen(10)
print("Server launched at {:^15}".format(netmap.get_IPv4))
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()