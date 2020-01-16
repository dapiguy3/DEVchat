from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter, os, time, netmap #netmap is a custom library I wrote for this program
from pprint import pprint

print("welcome to DEVchat v1.2.0")

while True: ###server options
	print("Do you want to launch a chat server? (y/n)")
	choice=input()
	
	if choice=="y":
		os.system("start cmd /k python chatserver.py")
		break
		
	elif choice=="n":
		break
		
	else:
		print("invalid choice!\n")
		
while True: ###get ip and port from user, then connect###
	try:
		print("Current IP's on your network")
		pprint(netmap.map())
		HOST=input("IP: ")
		PORT=int(input("Port: "))
		BUFSIZ = 1024
		ADDR = (HOST,PORT)
		client_socket = socket(AF_INET, SOCK_STREAM)
		client_socket.connect(ADDR)
		break
		
	except:
		pass
		
def receive(): ###recieve messages from server ###
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			msg_list.insert(tkinter.END, msg)
			msg_list.see('end')
			
		except OSError:  # Possibly client has left the chat.
			break
			
def send(event=None):  ###send message to server###
	msg = my_msg.get()
	my_msg.set("")
	
	try:
		client_socket.send(bytes(msg, "utf8"))
		
	except ConnectionResetError: #if user loses wifi connection, connection to the server, or the server closes.
		msg_list.insert(tkinter.END,"Uh oh, looks like the server is not responding.")
		msg_list.insert(tkinter.END,"Please try again at another time.")
		msg_list.insert(tkinter.END,"Program closing in 10 seconds.")
		time.sleep(10)
		quit()
		
	if msg == "{quit}":
		client_socket.close()
		root.quit()	
		
def on_closing(event=None): ###clean exit from socket and whatnot###
	my_msg.set("{quit}")
	send()
	
root = tkinter.Tk()  ###tkinter stuff###
root.title("Chatter") 

messages_frame = tkinter.Frame(root) #chat frame
my_msg = tkinter.StringVar()
my_msg.set("")

scrollbar = tkinter.Scrollbar(messages_frame) #scrollbar
msg_list = tkinter.Listbox(messages_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(root, textvariable=my_msg) #chat box
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tkinter.Button(root, text="Send", command=send) #send button
root.bind("<Return>",send) #allows enter key to act as a send button as well
send_button.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
receive_thread = Thread(target=receive) ### threading stuff ###
receive_thread.start() ### threading stuff ###
root.mainloop() #start tk window
