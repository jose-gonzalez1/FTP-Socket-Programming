# FTP-Socket-Programming 

**Jose Gonzalez**

*Programming Language : Python*

### To run program using localhost:
  1. Open two terminals on your computer.
  2. Change one terminal's directory to the folder named, 'Client'.
  3. Change the other terminal's directory to the folder named, 'Server'.
  4. Run Server's terminal first, then run Client's server second.

### To run program with two unique hosts:
  1. Firstly, turn your device's firewall off momentarily OR allow Python communication through your device's firewall.
  2. Open a terminal on the intended Server host and set directory to the folder named, 'Server'.
  3. Open a terminal on the intended Client host and set directory to the folder named, 'Client'.
  4. Run Server host first, then run Client host second.

### To run Server:
  1. Run server.py with, `python server.py <Intended Port Number>` for example, `python server.py 12345`
  2. OR run server.py with, `python server.py`. The default port of 123 would be used in this case.
  
### To run Client:
  1. Run client.py with, `python client.py <Intended Host Name or IP address> <Intended Port Number>`.
  
     An example could be, `python client.py 192.168.23.29 12345` which uses an IP address. 
     
     Another example could be, `python client.py JoseComputer 12345` which uses a computer host's name.
  2. If the connection is successful the client is then able to use four commands.
  
### Client Commands:
  1. `get <filename>`    -   asks the server to send one of its files and downloads it to the 'Client' folder.
  2. `put <filename>`    -   uploads a file from the client to the server and saves it in the 'Server' folder.
  3. `ls`                -   asks the server to return all available files to download, displays files in client's window
  4. `quit`              -   safely exits out of the program
  
  
