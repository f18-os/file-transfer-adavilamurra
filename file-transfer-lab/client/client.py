from socket import *
import sys

class Client:
    def __init__(self, file_name):
        self.sAddr = ("127.0.0.1", 50000)                # set address and reserve port
        self.file_name = file_name
        self.clientSock = socket(AF_INET, SOCK_STREAM)      # create client socket
        try:
            self.clientSock.connect(self.sAddr)          # connect to Server
            print("Connected to server.")
        except error:
            print("Error. Server not found.")
            sys.exit()
        self.sendFileNameToServer()         # send file name
        self.sendFileToServer()             # send file from client to server
        self.closeConnection()              # close socket connection

    def sendFileToServer(self):
        try:
            with open(self.file_name, "r") as clientFile:
                print("Sending file... ", self.file_name)
                data = clientFile.read()
                print("Data: ", data)
                self.clientSock.send(data.encode())
                clientFile.close()
        except IOError as e:
            print("No such file or directory. Try again.")
            self.clientSock.send("File not found. Try again.".encode)
            return
        print("Successfuly sent file to server.")
    
    def sendFileNameToServer(self):
        while True:
            print("Sending file name...")
            # send file name and if the ack is not received, send again
            self.clientSock.send(self.file_name.encode())
            ack = self.clientSock.recv(4).decode()
            print("Ack: ", ack)
            if ack == "Done":
                print("File Name sent.")
                break
    
    def closeConnection(self):
        self.clientSock.close()
        print("--- Connection closed. --- \n")

def startClient():
    file_name = input('Enter file name: ')
    client = Client(file_name)
    #client.sendFileNameToServer()
    #client.sendFileToServer()
        
startClient()
