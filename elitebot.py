#!/usr/bin/python3

BNICK   = 'EliteBot'
BIDENT  = 'EliteBot'
BNAME   = 'EliteBot'
BSERVER = 'irc.address.org'
BHOME   = '#EliteBot'
BADMIN  = 'Admin-nick'
UseSSL  = True

import socket
import sys
 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if usessl:
    ircsock = ssl.wrap_socket(ircsock)
ircsock.settimeout(240) # Set socket timeout.
connected = False 

print(f'Connecting to {server}')
 
irc.connect((server, 6667))
irc.send(bytes(f'NICK {botnick}\r\n','utf-8'))
irc.send(bytes(f'USER {botident} 0 * :{botname}\r\n','utf-8'))

while True:
   recvText = irc.recv(2048)
   text = recvText.decode('utf-8') 
   line = text.split('\r\n')
   print(text)
   if text.find('PING') != -1:
      irc.send(bytes(f'PONG {text}[4:]\r\n','utf-8'))
