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

HOST = "Cambiar por ip o dominio ZNC"
PORT = 8585 # Cambiar al puerto de la ZNC
NICK = "BotPy" # No necesario, toma el de la znc
IDENT = "mi_ident" # No necesario, toma el de la znc
REALNAME = "Mi nombre real" # No necesario, toma el de la znc
MASTER = "LeoSevilla"
PASS="PASS UsuarioZnc/Network:password";
IMPRIME = True

# Class Irc --------------------------------------------------------------------


class Irc():

    socket = None
    nickname = ""
    proc = None

# Medoto constructor-----------------------------------------------------------

    def __init__(self, host, port, nick, ident, realname):
        self.proc = process.Procesos()
        self.proc.inicio()
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.nickname = nick
        self.send(PASS)
        self.send("NICK %s" % nick)
        self.send("USER "+ident+" "+host+" BLA "+realname)


# Metodo demonio ---------------------------------------------------------------

    def demonio(self):
        while True:
            buf = self.socket.recv(4096).decode("utf-8",errors='ignore')
            if buf == '':
                continue
            self.proc.imprimir("<<<", buf, IMPRIME)
            if buf.find('PING') != -1:
                n = buf.split(':')[1]
                self.send('PONG :' + n)

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

# Fin Class Irc ----------------------------------------------------------------


mi_chat = Irc(HOST, PORT, NICK, IDENT, REALNAME)
mi_chat.demonio()
