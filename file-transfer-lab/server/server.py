from socket import *
import sys

class Server:
    def __init__(self):
        self.listenerSocket = listenerSocket = self.socketListen()  # create listen socket
        self.connSocket, self.addr = connSocket, addr = None, ""
        self.file_name, self.restOfBuffer = file_name, restOfBuffer = "", ""
        self.serverAddr = serverAddr = ("", 0)
        self.acceptConnection()     # accept connection from client
        self.getFileName()
        self.getFileFromClient()
        self.closeConnection()

    #put method from client   
    def getFileFromClient(self):
        if self.restOfBuffer == "File not found. Try again.":
            return
        with open(self.file_name, "w") as serverFile:
            serverFile.write(self.restOfBuffer)
            while True:
                print("Receiving data...")
                data = self.connSocket.recv(100).decode()
                if self.restOfBuffer == "File not found. Try again." or data == "File not found. Try again.":
                    return
                if not data:
                    break
                print("Data Received = ", data)
                # write data to a file
                serverFile.write(data)    
        serverFile.close()
        print("Successfully get file from client.")
    
    def getFileName(self):
        while True:
            name = self.connSocket.recv(255).decode().split()
            self.file_name = name[0]
            try:
                if(len(name) > 1):
                    self.restOfBuffer = ''.join(name[1:])
                self.connSocket.send("Done".encode())
                break
            except:
                print("Error. Data did not arrive correctly")
                self.connSocket.send("Error".encode())
        print(name)
    
    def acceptConnection(self):
        while True:
            self.connSocket, self.addr = self.listenerSocket.accept()      # establish connection with client.
            print("Got connection from", self.addr)
            return 

    def socketListen(self):
        self.serverAddr = ("127.0.0.1", 50000)      # set host and address
        listenerSocket = socket()              # create a socket object
        listenerSocket.bind(self.serverAddr)        # bind to the port
        listenerSocket.listen(1)               # wait for client connection.
        print("Server listening....")
        return listenerSocket

    def closeConnection(self):
        self.listenerSocket.close()
        self.connSocket.close()
        print("---- Connection closed. ---- \n")
        return

def startServer():
    server = Server()
    #server.acceptConnection()
    #server.getFileName()
    #server.getFileFromClient()
    #server.closeConnection()

startServer()
