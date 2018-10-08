from socket import *
import sys

class Client:
    def __init__(self, file_name, choice, numClients):
        self.sAddr = ("127.0.0.1", 50001)                #set address and reserve port
        self.numClients, self.file_name, self.choice = numClients, file_name, choice
        self.clientSock = socket(AF_INET, SOCK_STREAM)      #create client socket
        try:
            self.clientSock.connect(self.sAddr)          #connect to Server
            print("Connected to server.")
        except error:
            print("Error. Server not found.")
            sys.exit()
        self.sendNumClients()               #send number of clients to server
        self.sendBasicInfoToServer()        #send file name and choice to server
        self.determineChoice()              #determine if put or get
        self.closeConnection()              #close socket connection

    #get method                  
    def getFileFromServer(self):
        with open(self.file_name, "w") as clientFile:
            while True:
                print("Receiving data...")
                data = self.clientSock.recv(1024).decode()
                if data == "File not found. Try again.":
                    print(data)
                    return
                if not data:
                    break
                print("Data received =", data)
                # write data to a file
                clientFile.write(data)    
        clientFile.close()
        print("Successfully got file from server.")

    #put method
    def sendFileToServer(self):
        try:
            with open(self.file_name, "r") as clientFile:
                print("Sending file...")
                data = clientFile.read()
                self.clientSock.send(data.encode())
                clientFile.close()
        except IOError as e:
            print("No such file or directory. Try again.")
            self.clientSock.send("File not found. Try again.".encode)
            return
        print("Successfuly sent file to server.")

    def determineChoice(self):
        if(self.choice == "PUT" or self.choice == "put"):
            self.sendFileToServer()
        elif(self.choice == "GET" or self.choice == "get"):
            self.getFileFromServer()
        else:
            print("Invalid choice. Choices: PUT or GET.")
    
    def sendBasicInfoToServer(self):
        while True:
            #send file name and choice and if the ack is not received, send again
            self.clientSock.send((self.file_name + ":" + self.choice).encode())     #send file name and choice to server
            ack = self.clientSock.recv(4).decode()
            if ack == "Done":
                return

    def sendNumClients(self):
        self.clientSock.send(str(self.numClients).encode())     #send number of Clients to server
    
    def closeConnection(self):
        self.clientSock.close()
        print("--- Connection closed. --- \n")

def startClient():
    numClients = input('Enter the number of clients: ')
    clients = []
    #iterate with the number of clients
    for i in range(int(numClients)):
        print("Client ", str(i+1))
        file_name = input('Enter file name: ')
        choice = input('Enter choice (PUT or GET): ')
        clients.append(Client(file_name, choice, numClients))
        
startClient()
