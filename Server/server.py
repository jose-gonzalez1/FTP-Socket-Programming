import os
import time
import sys
import socket

if len(sys.argv) > 1:       # Check if user supplied port number
    port = int(sys.argv[1])      # Set port to supplied port number
else:
    port = 123              # Set port to a default port



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("hostname = %s\nport = %d" % (socket.gethostname(), port))
print("Server started!")      
print('Waiting for clients...')

server.bind(('', port))          # Bind to the port
server.listen(1)                 # Now wait for client connection.
c, addr = server.accept()        # Establish connection with client.
print('Got connection from', addr)
print(addr[0])

#===================================#
#=== Implement get and put funcs ===#
#===================================#

def get(filename):
    # connect to client's data connection
    server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data.bind(('', port+1))
    server_data.listen(1)
    data, addr = server_data.accept()

    try:
        with open(filename, "r+") as file:
            bytes_sent = 0
            msg = file.read().encode()

            total_bytes = str(len(msg))                   # Count byte length of file
            data.send(total_bytes.encode())               # Send byte length to client

            while bytes_sent < int(total_bytes):
                bytes_sent += data.send(msg[bytes_sent:])
        print("get SUCCESS")
    except:
        data.send(b"ERROR. File could not be opened.")
        print("get FAILURE")

    

    # close data connection
    data.close()

def put(filename):
    # connect to client's data connection
    server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data.bind(('', port+1))
    server_data.listen(1)
    data, addr = server_data.accept()

    msg = data.recv(1024).decode()
    if msg[:5] == "ERROR":
        print("put FAILURE")
    else:
        total_bytes = int(msg)
        bytes_recv = 0
        str = ""
        while bytes_recv < total_bytes:
            str += data.recv(45).decode()
            bytes_recv = len(str)

        newfile = open(filename, "w")
        newfile.write(str)
        newfile.close()
        print("put SUCCESS")


    # close data connection
    data.close()

def list():
    # connect to client's data connection
    server_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data.bind(('', port+1))
    server_data.listen(1)
    data, addr = server_data.accept()

    dir_list = os.listdir()
    print(dir_list)
    num_of_files = 0
    for file in dir_list:
        if file.endswith(".txt"):
         num_of_files += 1

    data.send(str(num_of_files).encode())

    for file in dir_list:
        if file.endswith(".txt"):
            data.send(file.encode())
            time.sleep(.2)
    # close data connection
    data.close()


while True:
    msg = c.recv(1024).decode()
    print('Received: ' + msg)
    if msg == "quit":
        break
    elif msg == "ls":
        list()
    elif msg == "get file":
        filename = c.recv(1024).decode()
        get(filename)
    elif msg == "put file":
        filename = c.recv(1024).decode()
        put(filename)
    #===================================#
    #=== Implement get and put funcs ===#
    #===================================#
    time.sleep(2)
c.close()                # Close the connection