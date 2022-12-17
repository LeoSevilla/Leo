#!/usr/bin/python3
# -*- coding: utf-8 -*-
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#       _              ____             _ _ _             #
#      | |    ___  ___/ ___|  _____   _(_) | | __ _       #
#      | |   / _ \/ _ \___ \ / _ \ \ / / | | |/ _` |      #
#      | |__|  __/ (_) |__) |  __/\ V /| | | | (_| |      #
#      |_____\___|\___/____/ \___| \_/ |_|_|_|\__,_|      #
#                                                         #
#        Email: leosevilla50[at]gmail.com                 #
#       Nombre: Francisco J. Perez                        #  
#      Codigo : Main.py v. 0.1                            #
#  Descripcion: Bot en python                             #
#          Uso: En privado usar el comando !cmd para      #
#               enviar comandos bajo protocolo irc        #
#      Ejemplo: !cmd nick otroNick:contraseña             #
#               !cmd join #Coach                          #
#               !cmd privmsg #Coach :Hola amigos          #
#  Desconectar: !quit                                     #
#   Configurar: MASTER con tu nick                        #
#               IMPRIME si o no salida por consola        #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

import socket
import process

HOST = "irc.chathispano.com"
PORT = 6667
NICK = "BotPy"
IDENT = "mi_ident"
REALNAME = "Mi nombre real"
CHANNELS = ['#aaabbb', '#coach']
MASTER = "LeoSevilla"
IMPRIME = False

# Class Irc --------------------------------------------------------------------


class Irc():

    socket = None
    connected = False
    channels = []
    nickname = ""
    proc = None

# Medoto constructor-----------------------------------------------------------

    def __init__(self, host, port, nick, ident, realname, canales):
        self.proc = process.Procesos()
        self.proc.inicio()
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
            self.proc.imprimir("<<<", buf, IMPRIME)

            if buf.find('PING') != -1:
                n = buf.split(':')[1]
                self.send('PONG :' + n)
                if self.connected == False:  # noqa: E712
                    self.connected = True
                    opcion = False

# Metodo demonio ---------------------------------------------------------------

    def demonio(self):
        while True:
            buf = self.socket.recv(4096).decode("utf-8",errors='ignore')
            if buf == '':
                continue
            self.proc.imprimir("<<<", buf, IMPRIME)
            #print("<<<", buf)
            # server ping/pong?
            if buf.find('PING') != -1:
                n = buf.split(':')[1]
                self.send('PONG :' + n)

            if buf.find('376') != -1 and self.connected:
                self.entrarCanales()
                self.connected = False

            proceder = self.proc.msgRecibido(self.socket, buf, MASTER)
            if proceder != None:
                self.send(proceder)

# Metodo send ------------------------------------------------------------------

    def send(self, msg):
        self.proc.imprimir(">>>", msg, IMPRIME)
        msg = str(msg)+"\r\n"
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
