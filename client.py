import socket
import sys
import struct
import time
import ctypes

DestinationPort = 13117
bufferSize = 1024
port=2081
host ='local host'
secondsSleep = 10

def RecievePacket():
    # UDP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print('Client started, listening for offer requests..')

    sock.bind(("",DestinationPort))
    data=None
    while data==None:
        try:
         data, addr = sock.recvfrom(bufferSize)
         break
        except:
         print("error in receieving data from the client")
    print('Received offer from 2081,attempting to connect...%s ' %data)
    sock.close

def SendGruopName(sockTCP):
    GroupName ="EliNof"
    try:
        sockTCP.send(GroupName.encode('ascii'))
    except:
        print("An exception occurred while sending message to server")

def main():
  while True:
    # Create a TCP/IP socket
    sockTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockTCP.connect((host, port))
    
    RecievePacket()
    SendGruopName(sockTCP)
    time.sleep(secondsSleep)
    
    while True:
        try:
          data = sockTCP.recv(bufferSize)
          if data:
            print('received "%s"' % data.decode('assci'))
            break
        except:
          print('error in receieving data from the client')  #connection.close?

    i=0
    while i<10:
        click = input()
        try:
            sockTCP.send(click.encode('ascii'))
        except:
            print("An exception occurred while sending message to client")
        i+=1
   
    print("Server disconnected, listening for offer requests...")


if __name__ == '__main__': 
    main() 
     

