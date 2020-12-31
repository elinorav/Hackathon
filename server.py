import socket
import struct
import ctypes
import time
from threading import Thread
import threading
import random

clients_lock = threading.Lock()
Counter1Lock = threading.Lock()
Counter2Lock = threading.Lock()
MagicCookie=0xfeedbeef
MessageType=0x2
th=[]
Clients = dict()
Group1 = set()
Group2 = set()
couunter1 =set()
couunter2 =set()
localIP     = '127.0.0.1'
DestinationPort = 2081
Port = 13117
bufferSize = 1024
oneSecondSleep = 1
tenSecondsSleep = 10

def UDPFunc():
    # Create a datagram socket
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPServerSocket.bind((localIP, DestinationPort))

    print("Server started, listening on IP address %s" %localIP)
    Broadcast = struct.pack("!IBH", MagicCookie, MessageType, DestinationPort)
    i=0
    while(i<10):
        UDPServerSocket.sendto(Broadcast, ('<broadcast>', Port))
        time.sleep(1)
        i+=1
    #UDPServerSocket.settimeout(10)

def TCPFunc(Clients,Group1,Group2):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', DestinationPort)
    sock.bind(server_address)
    sock.listen(10)

    while True:
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            while True:
                data = connection.recv(16)
                if not data:
                  break
                else:
                  print('received "%s"' % data)
                  Rand=random.choice([Group1,Group2])
                  Rand.add(data.decode('ascii'))
                  # save the connection
                  with clients_lock:
                    Clients[connection]=Rand
        except:
            print('error')  #connection.close?

def CounterTav1(connection, Counter):
    i=0
    while i<10:
       time.sleep(1)
       try:
            data = connection.recv(bufferSize)
            if not data:
              break  
            else:
              with Counter1Lock:
                Counter.add(len(data))  
       except:
         print('problem')

def CounterTav2(connection, Counter):
    i=0
    while i<10:
       time.sleep(oneSecondSleep)
       try:
            data = connection.recv(bufferSize)
            if not data:
              break  
            else:
              with Counter1Lock:
                Counter.add(len(data))  
       except:
         print('problem')

def CreateMesName(names1,names2):
  for n in Group1:
      names1+=n+"\n"
  
  for n in Group2:
      names2 += n+"\n"
    
  messege = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
  messege += names1
  messege +="\nGroup 2:\n==\n"
  messege += names2
  messege += "\nStart pressing keys on your keyboard as fast as you can!!\n"
  return messege

def CreateMesGameOver(names1,names2):
    num1=0
    for i in couunter1:
        num1 += i
    num2=0
    for i in couunter2:
        num2 += i

    winer=""
    win=-1
    if(num1>num2):
      winer="Group 1" 
      win=1
    else:
      winer="Group 2"
      win=2

    messege  ="Game over! \nGroup 1 typed in "
    messege +=str(num1)
    messege +=" characters. Group 2 typed in "
    messege +=str(num2)
    messege +=" characters.\n"
    messege += winer
    messege +=" wins!\nCongratulations to the winners:\n ==\n"
    if (win==1):
      messege +=names1
    else:
      messege +=names2
    return messege

def main():
  #while True:
    th.append(Thread(target=UDPFunc, args = ()).start())
    th.append(Thread(target=TCPFunc, args = (Clients,Group1,Group2)).start())

    time.sleep(10)
    print("arrived")
    Group1.add("Elinor")
    Group1.add("Rachil")
    Group1.add("Nofet")
    Group2.add("Strange peaople")
    couunter1.add(3)
    couunter1.add(4)
    couunter1.add(5)
    couunter2.add(3)
    couunter2.add(3)
    
    names1=""
    names2=""
    #send division of groups
    mes=CreateMesName(names1,names2)
    for c in Clients:
       try:
          c[0].send(mes.encode('ascii'))
       except:
          print("An exception occurred")
    
    #start the game
    for c in Clients:
       if (c[1]==Group1):
           th.append(Thread(target=CounterTav1, args = (c[0],couunter1)).start()) 
       else:
           th.append(Thread(target=CounterTav2, args = (c[0],couunter2)).start())
     
    mes=CreateMesGameOver(names1,names2)
  
    #Send GameOver
    for c in Clients:
       try:
          c[0].send(mes.encode('ascii'))
          c[0].close()
       except:
          print("An exception occurred")
    
    print("Game over, sending out offer requests...")
    
if __name__ == '__main__': 
    main() 
     