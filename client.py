import os
import time
import sys
import socket

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    host = socket.gethostname() # Get local machine name
    port = 123                  # Reserve a port for your service.

client_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a socket object

print('Connecting to ', host, port)
try:
    client_control.connect((host, port))
except ConnectionRefusedError:
    print("Could not Connect to Server.")
    exit()

def get(filename): 
    client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_data.connect((host, port+1))
    except ConnectionRefusedError:
        print("Could not Connect to Server's Data Connection.")
        return
    
    msg = client_data.recv(1024).decode()
    if msg[:5] == "ERROR":
        print(msg)
    else:
        total_bytes = int(msg)
        bytes_recv = 0
        str = ""
        while bytes_recv < total_bytes:
            str += client_data.recv(45).decode()
            bytes_recv = len(str)

        newfile = open(filename, "w")
        newfile.write(str)
        newfile.close()


    # wait and then close server's data connection
    time.sleep(1)
    client_data.close()
    FileStats(filename)

def put(filename): # upload file to server, filename >> send to server, server should save file
    client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_data.connect((host, port+1))
    except ConnectionRefusedError:
        print("Could not Connect to Server's Data Connection.")
        return
    
    try:
        with open(filename, "r+") as file:
            bytes_sent = 0
            msg = file.read().encode()

            total_bytes = str(len(msg))                   # Count byte length of file
            client_data.send(total_bytes.encode())        # Send byte length to client

            while bytes_sent < int(total_bytes):
                bytes_sent += client_data.send(msg[bytes_sent:])
    except:
        client_data.send(b"ERROR. File could not be opened.")
        print("File could not be opened.")


    # wait and then close server's data connection
    time.sleep(1)
    client_data.close()
    FileStats(filename)

def list(): # ask server to return directory
    # set up data connection for server to connect to
    client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_data.connect((host, port+1))
    except ConnectionRefusedError:
        print("Could not Connect to Server's Data Connection.")
        return

    num_of_files = client_data.recv(1024).decode()
    num = int(num_of_files)
    while num > 0:
        num -= 1
        msg = client_data.recv(1024)
        print("\t", msg.decode())
    
    # close server's data connection
    # time.sleep(1)
    client_data.close()

def FileStats(filename):
    try:   
        bytes_trans = os.stat(filename).st_size
        print("%s [%d / %d] bytes transferred" %(filename, bytes_trans, bytes_trans))
    except :
        pass


while True:
    text = input("ftp> ")
    # parse msg, seperate arguments by ' ' (space)
    msg = text.split()

    # check if first argument is get, put, ls or quit
    # call correct function depending on argument
    if msg[0] == "quit":
        client_control.send(msg[0].encode())
        break
    elif msg[0] == "ls":
        client_control.send(msg[0].encode())
        list()
    elif msg[0] == "get":
        if len(msg) == 2:
            client_control.send(b'get file')
            time.sleep(.1)
            client_control.send(msg[1].encode())
            get(msg[1])
        else:
            print("No filename provided.")
    elif msg[0] == "put":
        if len(msg) == 2:
            client_control.send(b'put file')
            time.sleep(.1)
            client_control.send(msg[1].encode())
            put(msg[1])
        else:
            print("No filename provided.")    
    else:
        client_control.send(text.encode())

print("Closing Connection to Server now.")
client_control.close()  # Close the socket when done

# ask server for file, filename >> open and save new file
    # create new data socket
    # connect to server's new data connection 
    # (client connects to server)
    # (server sends bytes to client)
    # implement a way to receive and check bytes were received correctly
    # server must try to open filename sent by client
    #   if opens == send bytes of text file
    #   else send error message 
    # if successful send SUCCESS message, server prints success
    #   client will print filename and bytes transferred