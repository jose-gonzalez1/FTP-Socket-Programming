# 471 FTP Project 
# server.py
# Jose Gonzalez   jose.gonz@csu.fullerton.edu
# Rodney Muniz    rodmuniz1@csu.fullerton.edu
# Jasmine Santoro jasminesantoro@csu.fullerton.edu 

import os
import sys
import time
import socket

if len(sys.argv) > 1:       # Check if user supplied port number
    port = int(sys.argv[1])      
else:
    port = 123              # If not, set port to a default port

# Create a socket object (control link with client)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("hostname = %s\nport = %d" % (socket.gethostname(), port))
print("Server started!")      
print('Waiting for clients...')

server.bind(('', port))                 # Bind to the port
server.listen(1)                        # Wait for client connection
client_control, addr = server.accept()  # Accept connection with client
print('Got connection from', addr)

# Server's get function
def get(filename):
    # Connect to client's data connection
    server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data.bind(('', port+1))
    server_data.listen(1)
    data, addr = server_data.accept()

    # Try to open file to send to client, if can't raise error message
    try:
        with open(filename, "r+") as file:
            bytes_sent = 0
            msg = file.read().encode()

            total_bytes = str(len(msg))          # Count byte length of file
            data.send(total_bytes.encode())      # Send byte length to client

            while bytes_sent < int(total_bytes): # Loop until total is sent
                bytes_sent += data.send(msg[bytes_sent:])

        print("get SUCCESS")                     # Print SUCCESS message 
    except:
        data.send(b"ERROR. File could not be opened.")
        print("get FAILURE")

    # close data connection
    data.close()

# Server's put function
def put(filename):
    # Connect to client's data connection
    server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data.bind(('', port+1))
    server_data.listen(1)
    data, addr = server_data.accept()

    msg = data.recv(1024).decode() # Receive client's message

    if msg[:5] == "ERROR":         # Print FAILURE if its an error message
        print("put FAILURE")
    else:
        total_bytes = int(msg)     # Otherwise save total bytes message
        bytes_recv = 0              
        str = ""

        while bytes_recv < total_bytes:     # Loop until all bytes are received
            str += data.recv(45).decode()
            bytes_recv = len(str)

        newfile = open(filename, "w")       # Open file with given file name
        newfile.write(str)                  # Write into file received bytes
        newfile.close()                     # Close file
        print("put SUCCESS")                # Print SUCCESS message

    # Close data connection
    data.close()

def list():
    # Connect to client's data connection
    server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data.bind(('', port+1))
    server_data.listen(1)
    data, addr = server_data.accept()

    dir_list = os.listdir()     # Create list of all files in same directory
    num_of_files = 0
    for file in dir_list:
        if file.endswith(".txt"):   # Count all files that end with .txt
         num_of_files += 1

    data.send(str(num_of_files).encode())   # Send total number of files 

    for file in dir_list:           # Send all filenames that end with .txt
        if file.endswith(".txt"):
            data.send(file.encode())
            time.sleep(.2)

    # Close data connection
    data.close()

# Loop until client quits
while True:     
    msg = client_control.recv(1024).decode()    # Receive message from client
    print('Received: ' + msg)                   # Print message
    if msg == "quit":                           # Call correct function 
        break
    elif msg == "ls":
        list()
    elif msg == "get file":
        filename = client_control.recv(1024).decode()
        get(filename)
    elif msg == "put file":
        filename = client_control.recv(1024).decode()
        put(filename)
    time.sleep(2)

client_control.close()                # Close the connection
