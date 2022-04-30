#!/usr/bin/python3

BNICK   = 'EliteBot'
BIDENT  = 'EliteBot'
BNAME   = 'EliteBot'
BSERVER = 'irc.address.org'
BPORT   = 6697
BHOME   = '#EliteBot'
BADMIN  = 'Admin-nick'
UseSSL  = True

import socket
import sys
import ssl
 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if UseSSL:
    ircsock = ssl.wrap_socket(ircsock)
ircsock.settimeout(240)
connected = False 

print(f'Connecting to {BSERVER} :{BPORT}')
 
ircsock.connect((BSERVER, BPORT))
ircsock.send(bytes(f'NICK {BNICK}\r\n','utf-8'))
ircsock.send(bytes(f'USER {BIDENT} 0 * :{BNAME}\r\n','utf-8'))

while True:
   recvText = ircsock.recv(2048)
   text = recvText.decode('utf-8') 
   line = text.split('\r\n')
   print(text)
   if text.find('PING') != -1:
      pongis = text.split(':')[1]
      ircsock.send(bytes(f'PONG {pongis}\r\n','utf-8'))
      ircsock.send(bytes(f'JOIN {BHOME}\r\n','utf-'))