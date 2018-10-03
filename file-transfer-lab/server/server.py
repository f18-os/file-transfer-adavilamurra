from socket import *
import sys

class Server:
    def __init__(self):
        self.listenerSocket = self.socketListen()  #create listen socket
        self.connSocket, self.addr = None, ""
        self.file_name, self.choice, self.strBuffer = "", "", ""
        self.serverAddr = ("", 0)
        self.acceptConnection()     #accept connection from client
    
    #put method from client   
    def getFileFromClient(self):
        if self.strBuffer == "File not found. Try again.":
            return
        with open(self.file_name, "w") as serverFile:
            serverFile.write(self.strBuffer)
            while True:
                #print("Receiving data...")
                data = self.connSocket.recv(1024).decode()
                if self.strBuffer == "File not found. Try again." or data == "File not found. Try again.":
                    return
                if not data:
                    break
                print("Data Received = ", data)
                # write data to a file
                serverFile.write(data)    
        serverFile.close()
        print("Successfully got file from client.")
        return

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
        return

    def determineChoice(self):
        if(self.choice.lower() == "put"):
            self.getFileFromClient()
        elif(self.choice.lower() == "get"):
            self.sendFileToClient()
        else:
            print("Invalid choice. Choices: PUT or GET.")
        return

    def getNameAndChoice(self):
        while True:
            #print("Getting name and choice...")
            nameChoice = self.connSocket.recv(1024).decode().split(":")
            #print("Name:choice= ", nameChoice)
            self.file_name = nameChoice[0]
            #print("File: ", self.file_name)
            try:
                if(len(nameChoice[1]) > 3):
                    self.choice = nameChoice[1][:3]
                    self.strBuffer = nameChoice[1][3:]
                else:
                    self.choice = nameChoice[1]
                    self.strBuffer = ""
                if (self.choice.lower()) == "put" or (self.choice.lower()) == "get":
                    self.connSocket.send("Done".encode())
                    #print("Choice: ", self.choice)
                    #print("Buff: ", self.strBuffer)
                return
            except:
                print("Error. Data did not arrive correctly.")
                self.connSocket.send("Error".encode())
    
    def acceptConnection(self):
        while True:
            self.connSocket, self.addr = self.listenerSocket.accept()      #establish connection with client.
            print("Got connection from", self.addr)
            return 

    def socketListen(self):
        self.serverAddr = ("127.0.0.1", 50000)      #set host and address
        listenerSocket = socket()              #create a socket object
        listenerSocket.bind(self.serverAddr)        #bind to the port
        listenerSocket.listen(1)               #wait for client connection.
        print("Server listening....")
        return listenerSocket

    def closeConnection(self):
        self.listenerSocket.close()
        self.connSocket.close()
        print("---- Connection closed. ---- \n")

def startServer():
    server = Server()    
    server.getNameAndChoice()
    server.determineChoice()
    server.closeConnection()

startServer()
