from socket import *
import sys, os

class Server:
    def __init__(self):
        self.listenerSocket = self.socketListen()  #create listen socket
        self.connSocket, self.addr = None, ""
        self.file_name, self.choice, self.restOfBuffer = "", "", ""
        self.numClients, self.serverAddr = 0, ("", 0)
        self.acceptConnection()     #accept connection from client
        self.getNumberOfClients()   #get the number of clients
        self.connectToClients()
        
    #put method from client   
    def getFileFromClient(self):
        if self.restOfBuffer == "File not found. Try again.":
            return
        if os.path.exists(self.file_name):
            print("This file already exists. Overwriting...")
        with open(self.file_name, "w") as serverFile:
            serverFile.write(self.restOfBuffer)
            while True:
                print("Receiving data...")
                data = self.connSocket.recv(1024).decode()
                if self.restOfBuffer == "File not found. Try again." or data == "File not found. Try again.":
                    return
                if not data:
                    break
                print("Data Received = ", data)
                # write data to a file
                serverFile.write(data)    
        serverFile.close()
        print("Successfully got file from client.")

    #get method from client
    def sendFileToClient(self):
        try:
            with open(self.file_name, "r") as serverFile:
                print("Sending file...")
                data = serverFile.read()
                self.connSocket.send(data.encode())
                serverFile.close()
        except IOError as e:
            print("No such file or directory. Try again.")
            self.connSocket.send("File not found. Try again.".encode())
            self.connSocket.close()
            return
        print("Successfuly sent file to client.")

    def determineChoice(self):
        if(self.choice.lower() == "put"):
            self.getFileFromClient()
        elif(self.choice.lower() == "get"):
            self.sendFileToClient()
        else:
            print("Invalid choice.")

    def getNameAndChoice(self):
        while True:
            nameChoice = self.connSocket.recv(1024).decode().split(":")
            if self.numClients == 0:
                self.file_name = nameChoice[0]
            else:
                self.file_name = nameChoice[0][1:]
            try:
                if(len(nameChoice[1]) > 3):
                    self.choice = nameChoice[1][:3]
                    self.restOfBuffer = nameChoice[1][3:]
                else:
                    self.choice = nameChoice[1]
                    self.restOfBuffer = ""
                if self.choice.lower() == "put" or self.choice.lower() == "get":
                    self.connSocket.send("Done".encode()) 
                return
            except:
                print("Error. Data did not arrive correctly.")
                self.connSocket.send("Error".encode())
                return

    def forkClient(self, client):
        rc = os.fork()
        if rc < 0:       # fork failed
            print("Fork failed, returning ", rc)
        elif rc == 0:      # child
            if client > 0:
                self.acceptConnection()
            self.getNameAndChoice()
            self.determineChoice()
        else:          # parent
            os.wait()
        
    def connectToClients(self):
        # check for connections depending on the number of clients
        if self.numClients < 1:
            print("You need at least one client.")
            sys.exit()
        elif self.numClients == 1:
            self.getNameAndChoice()
            self.determineChoice()
        else:
            for client in range(self.numClients):
                self.forkClient(client)
    
    def getNumberOfClients(self):
        self.numClients = int(self.connSocket.recv(1).decode())

    def acceptConnection(self):
        while True:
            self.connSocket, self.addr = self.listenerSocket.accept()      #establish connection with client.
            print("Got connection from", self.addr)
            return

    def socketListen(self):
        self.serverAddr = ("127.0.0.1", 50001)      #set host and address
        listenerSocket = socket()              #create a socket object
        listenerSocket.bind(self.serverAddr)        #bind to the port
        listenerSocket.listen(1)               #wait for client connection.
        print("Server listening....")
        return listenerSocket

    def closeConnection(self):
        self.listenerSocket.close()
        self.connSocket.close()
        print("---- Connection closed. ----")

def startServer():
    server = Server()
    server.closeConnection()

startServer()
