# TCP File Transfer Protocol

I created a transfer protocol to send files using TCP. It is multithreaded and the server accepts multi clients.

## Getting Started

In order to run this project successfully you will have to run the server file (server.py) located in the folder /server/ and then the client file (client.py) located in the folder /client/.

### Prerequisites

To run this protocol you will need:
* Python 3.6
* Command Line Terminal

### Files Included

The following are all the files that are included in the protocol.

```
client/
    file.txt        % text file
    client.py    % client
    README.md       % more info about the client
server/
    file.txt        % text file
    server.py    % server
    README.md       % more info about the server
README.md      % more info about the protocol (This file)
```

#### Disclaimer
I am not a graduate student. I added the GET as a challenge. The GET only works on the last client (it hangs with other clients)
