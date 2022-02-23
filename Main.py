#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

HOST = "irc.chathispano.com"
PORT = 6667
NICK = "BotPy"
IDENT = "mi_ident"
REALNAME = "Mi nombre real"
CHANNELS = ['#aaabbb', '#coach']

# Class Irc --------------------------------------------------------------------


class Irc():

    socket = None
    connected = False
    channels = []
    nickname = ""

# Metodo constructor -----------------------------------------------------------

    def __init__(self, host, port, nick, ident, realname, canales):
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.channels = canales
        self.nickname = nick
        self.send("NICK %s" % nick)
        self.send("USER "+ident+" "+host+" BLA "+realname)

        opcion = True
        while opcion == True:  # noqa: E712

            buf = self.socket.recv(4096).decode()
            if buf == '':
                continue
            print("<<<", buf)

            if buf.find('PING') != -1:
                n = buf.split(':')[1]
                self.send('PONG :' + n)
                if self.connected == False:  # noqa: E712
                    self.connected = True
                    opcion = False

# Metodo demonio ---------------------------------------------------------------

    def demonio(self):
        while True:
            buf = self.socket.recv(4096).decode()
            if buf == '':
                continue
            print("<<<", buf)
            # server ping/pong?
            if buf.find('PING') != -1:
                n = buf.split(':')[1]
                self.send('PONG :' + n)

            if buf.find('376') != -1 and self.connected:
                self.entrarCanales()
                self.connected = False

# Metodo send ------------------------------------------------------------------

    def send(self, msg):
        print(">>>", msg)
        msg = msg+"\r\n"
        self.socket.send(msg.encode("utf-8"))

# Metodo say -------------------------------------------------------------------

    def say(self, msg, to):
        self.send("PRIVMSG %s :%s" % (to, msg))

# Metodo entrarCanales ---------------------------------------------------------        

    def entrarCanales(self):
        # self.send("MODE %s +x" % self.nickname)
        for c in self.channels:
            self.send("JOIN %s" % c)
            self.say('hola!', c)

# Fin Class Irc ----------------------------------------------------------------


mi_chat = Irc(HOST, PORT, NICK, IDENT, REALNAME, CHANNELS)
mi_chat.demonio()
