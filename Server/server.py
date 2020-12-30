import socket
import struct
import ctypes
import time
#import threading
from threading import Thread
import threading
#from _thread import *
import random

clients_lock = threading.Lock()
Counter1Lock = threading.Lock()
Counter2Lock = threading.Lock()

def UDPFunc():
    localIP     = "127.0.0.1" 
    localPort   = 2081
  
    # Create a datagram socket
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    print("Server started, listening on IP address 127.0.0.1")
   
    Broadcast =struct.pack("!IBH",0xfeedbeef, 0x2, localPort)
    i=0
    while(i<10):
        UDPServerSocket.sendto(Broadcast, ('<broadcast>', 13117))
        print("message sent!")
        time.sleep(1)
        i+=1
    #UDPServerSocket.settimeout(10)

def TCPFunc(Clients,Group1,Group2):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 2081)
    sock.bind(server_address)
    sock.listen(10)

    while True:
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                if not data:
                  break
                else:
                  print('received "%s"' % data)
                  t=random.choice([Group1,Group2])
                  t.add(data.decode('ascii'))
                  with clients_lock:
                    Clients[connection]=t
        finally:
            print('')  #connection.close?
            print(Group1)
            print(Group2)

def CounterTav1(connection, Counter):
    for i in range (0,10):
       try:
            data = connection.recv(16)
            if not data:
              break  #??
            else:
              with Counter1Lock:
                Counter.add(len(data))  
       finally:
            print('')  #connection.close?

def CounterTav2(connection, Counter):
   for i in range (0,10):
       try:
            data = connection.recv(16)
            if not data:
              break
            else:
              with Counter2Lock:
                 Counter.add(len(data))  
       finally:
            print('')  #connection.close?

def main():
    th=[]
    Clients = dict()
    Group1 = set()
    Group2 = set()
    couunter1 =set()
    couunter2 =set()
    
    th.append(Thread(target=UDPFunc, args = ()).start())
    th.append(Thread(target=TCPFunc, args = (Clients,Group1,Group2)).start())

    time.sleep(12)
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
    for n in Group1:
        names1+=n+"\n"
  
    for n in Group2:
        names2 += n+"\n"
    
    messege1 = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    messege1 += names1
    messege1 +="\nGroup 2:\n==\n"
    messege1 += names2
    messege1 += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    print(messege1)
   # for c in Clients:
    #   try:
    #      c[0].sendall(messege1)
    #   except:
     #     print("An exception occurred")
 
    #for c in Clients:
    #   if (c[1]==Group1):
    #       th.append(Thread(target=CounterTav1, args = (c[0],couunter1)).start()) #add timout
    #   else:
    #       th.append(Thread(target=CounterTav2, args = (c[0],couunter2)).start())
     
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

    messege2  ="Game over! \nGroup 1 typed in "
    messege2 +=str(num1)
    messege2 +=" characters. Group 2 typed in "
    messege2 +=str(num2)
    messege2 +=" characters.\n"
    messege2 += winer
    messege2 +=" wins!\nCongratulations to the winners:\n ==\n"
    if (win==1):
      messege2 +=names1
    else:
      messege2 +=names2

    #for c in Clients:
    #   try:
    #      c[0].sendall(messege2)
    #      c[0].close()
    #   except:
    #      print("An exception occurred")
    
    #print(messege2)

if __name__ == '__main__': 
    main() 
     
     
     
  
     
     
     
     
      #   if data:
        #        print('sending data back to the client')
          #      connection.sendall(data)
 #else:
         #       print('no more data from', client_address)
          #      break

#finally:
        # Clean up the connection
     #   connection.close()


 #g=random.uniform(0,1)
    #           if(g<=0.5):
      #           Group1.add(data)
       #        else:
        #         Group2.add(data)