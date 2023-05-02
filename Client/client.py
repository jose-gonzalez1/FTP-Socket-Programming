# 471 FTP Project 
# client.py
# Jose Gonzalez   jose.gonz@csu.fullerton.edu
# Rodney Muniz    rodmuniz1@csu.fullerton.edu
# Jasmine Santoro jasminesantoro@csu.fullerton.edu

import os
import sys
import time
import socket

# Checks if server and port number are provided by user, if not use default
if len(sys.argv) == 3: 
    host = sys.argv[1]
    port = int(sys.argv[2])
else:                  
    host = socket.gethostname() # Get local machine name
    port = 123                  # Set a default port

# Create a socket object  (control link with server)
client_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        

# Print connecting message
print('Connecting to ', host, port)

# Try to connect, if can't raise error message and exit code
try:
    client_control.connect((socket.gethostbyname(host), port))
except ConnectionRefusedError:
    print("Could not Connect to Server.")
    exit()

# Client's get function 
def get(filename): 
    # Create a data link with server
    client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Try to connect, if can't raise error message and return to loop
    try:
        client_data.connect((host, port+1))
    except ConnectionRefusedError:
        print("Could not Connect to Server's Data Connection.")
        return
    
    msg = client_data.recv(1024).decode() # Receive server's response

    if msg[:5] == "ERROR":  # Print response if it is an Error message
        print(msg)
    else:
        total_bytes = int(msg) # Otherwise server sent total bytes of file
        bytes_recv = 0         # Initialize bytes received to 0
        str = ""               # Initialize an empty string

        while bytes_recv < total_bytes:     # Loop until all bytes are received
            str += client_data.recv(45).decode()
            bytes_recv = len(str)

        newfile = open(filename, "w")   # Create a file with given name
        newfile.write(str)              # Write data from server into file
        newfile.close()                 # Close file

    # Wait then close server's data connection
    time.sleep(1)
    client_data.close()
    # Print File stats
    FileStats(filename)

# Client's put function
def put(filename):
    # Create a data link with server
    client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Try to connect, if can't raise error message and return to loop
    try:
        client_data.connect((host, port+1))
    except ConnectionRefusedError:
        print("Could not Connect to Server's Data Connection.")
        return
    
    # Try to open file to send to server, if can't raise error message
    try:
        with open(filename, "r+") as file:
            bytes_sent = 0              # Initialize bytes sent to 0
            msg = file.read().encode()  # Read file contents and encode it

            total_bytes = str(len(msg))            # Count byte length of file
            client_data.send(total_bytes.encode()) # Send byte length to server

            while bytes_sent < int(total_bytes):   # Loop until all bytes sent
                bytes_sent += client_data.send(msg[bytes_sent:])
    except:
        client_data.send(b"ERROR. File could not be opened.")
        print("File could not be opened.")

    # Wait then close server's data connection
    time.sleep(1)
    client_data.close()
    # Print File stats
    FileStats(filename)

# Client's list function
def list(): 
    # Create a data link with server
    client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Try to connect, if can't raise error message and return to loop
    try:
        client_data.connect((host, port+1))
    except ConnectionRefusedError:
        print("Could not Connect to Server's Data Connection.")
        return

    # Server's first message in this case will be number of files to receive
    num_of_files = client_data.recv(1024).decode()  
    num = int(num_of_files)
    while num > 0:                      # Loop until all files are received
        num -= 1
        msg = client_data.recv(1024)
        print("\t", msg.decode())       # Print filename to client user
    
    # Close server's data connection
    client_data.close()

# Function to return file stats after successful transfer
def FileStats(filename):
    try:   
        bytes_trans = os.stat(filename).st_size
        print("%s [%d / %d] bytes transferred"%(filename, bytes_trans, bytes_trans))
    except :
        pass

# Loop until client requests to quit 
while True:
    text = input("ftp> ")   
    msg = text.split()      # Seperate arguments by whitespace

    # Call correct function based off the first argument
    if len(msg) == 0:       # If no message is sent then pass
        pass
    elif msg[0] == "quit":
        client_control.send(msg[0].encode())    # Tell server client is quitting 
        break
    elif msg[0] == "ls":
        client_control.send(msg[0].encode())    # Tell server to list files
        list()
    elif msg[0] == "get":       
        if len(msg) == 2:   # If get and filename is included let server know
            client_control.send(b'get file')
            time.sleep(.1)
            client_control.send(msg[1].encode())
            get(msg[1])
        else:               # If filename is not provided let user know
            print("No filename provided.")
    elif msg[0] == "put":   # If put and filename is included let server know
        if len(msg) == 2:
            client_control.send(b'put file')
            time.sleep(.1)
            client_control.send(msg[1].encode())
            put(msg[1])
        else:               # If filename is not provided let user know
            print("No filename provided.")    
    else:
        pass
        # Uncomment the following line to allow other messages to be sent
        # client_control.send(text.encode())

# Close the socket when done
print("Closing Connection to Server now.")
client_control.close()  
