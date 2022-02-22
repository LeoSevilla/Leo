#!/usr/bin/env python
import socket

HOST = "irc.chathispano.com"
PORT = 6667
NICK = "BotPy"
IDENT = "mi_ident"
REALNAME = "Mi nombre real"
CHANNEL = "#coach"


irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("connecting to: "+HOST)
irc.connect((HOST, PORT))


output = "NICK "+NICK+"\n\n"
output2 = "USER "+IDENT+" "+HOST+" BLA "+REALNAME+" \r\n"

irc.send(output.encode("utf-8"))
irc.send(output2.encode("utf-8"))


while 1:
    text = irc.recv(2040).decode("utf-8")
    print(text)

    if text.find("PING") != -1:
        data_pong = "PONG " + text.split()[1] + "\r\n"
        irc.send(data_pong.encode("utf-8"))

    if text.find('376') != -1:  # :End of message of the day.
        data_join = "JOIN " + CHANNEL + "\n"
        irc.send(data_join.encode("utf-8"))

    if text.find(':!hi') != -1:
        t = text.split(':!hi')  # Si pones el comando !hi te responde con Hello
        to = t[1].strip()
        data = 'PRIVMSG '+CHANNEL+' :Hello '+str(to)+'! \r\n'
        irc.send(data.encode("utf-8"))
