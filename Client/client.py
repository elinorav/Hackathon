import socket
import sys
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

# Enable broadcasting mode 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#Connect the socket to the port where the server is listening
print('Client started, listening for offer requests..')

sock.bind(("",13117))
data=None
while data==None:
    try:
     data, addr = sock.recvfrom(1024)
     break
    # check magick number, encode decode
    #mes=struct.unpack("!IBH",data)
    except:
      print("error")
print('Received offer from 2081,attempting to connect...%s ' %data)

sock.close
port=2081
host ='127.0.0.1'
# Create a TCP/IP socket
sockTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sockTCP.connect((host, port))
messege ="EliNof"
try:
    sockTCP.send(messege.encode('ascii'))
except:
    print("problem")