# -*- coding: utf-8 -*-
import json
import operator
from random import randrange

# Class Serpiente -------------------------------------------------------------


class Robar():

    start = False
    puntos = {}
    palabra = ""
    pos1 = 0
    pos2 = 0
    pos3 = 0
    pos4 = 0

# Metodo parar ----------------------------------------------------------------

    def parar(self):

        self.start = False
        self.escribirPuntos()

# Metodo proceso --------------------------------------------------------------

    def proceso(self, socket, sunick, context, info, estado):

        if self.start:
            self.robar(socket, context, sunick, info)
        else:
            self.leerpuntos()
            self.infoAyuda(socket, sunick, context)
            self.setRobar()
            self.start = True

# Metodo escribirPuntos -------------------------------------------------------

    def escribirPuntos(self):
        with open('robarPuntos.txt', 'w') as file:
            file.write(json.dumps(self.puntos))

# Metodo leerpuntos -----------------------------------------------------------

    def leerpuntos(self):
        try:
            with open('robarPuntos.txt', 'r') as file:
                self.puntos = json.load(file)
        except:
            with open('robarPuntos.txt', 'w') as file:
                file.write(json.dumps(self.puntos))

# Metodo infoAyuda ------------------------------------------------------------

    def infoAyuda(self, socket, sunick, context):

        salida = 'PRIVMSG '+context+' :Averigua la combinacion de la caja, se compone de 4 digitos entre 0000 y el 9999\r\n'
        socket.send(salida.encode("utf-8"))
        salida = 'PRIVMSG '+context+' :Color \00307naranja\003 esta pero no es su lugar.\r\n'
        socket.send(salida.encode("utf-8"))
        salida = 'PRIVMSG '+context+' :Color \00304rojo\003 no esta en la combinacion\r\n'
        socket.send(salida.encode("utf-8"))
        salida = 'PRIVMSG '+context+' :Color \00303verde\003 Bingo!! esta y en su lugar\r\n'
        socket.send(salida.encode("utf-8"))
        salida = 'PRIVMSG '+context+' :Para robar: \002!r <codigo>\002 donde codigo son los cuatro digitos\r\n'
        socket.send(salida.encode("utf-8"))

# Metodo setRobar -------------------------------------------------------------

    def setRobar(self):
        self.pos1 = randrange(9)
        self.pos2 = randrange(9)
        self.pos3 = randrange(9)
        self.pos4 = randrange(9)

# Metodo robar ----------------------------------------------------------------

    def robar(self, sock, channel, nick, respuesta):
        respuesta = respuesta.lower()

        if respuesta == "!puntos":
            self.leerPuntos(sock, channel)
            return
        if respuesta == "!ayuda":
            self.infoAyuda(sock, nick, channel)
            return

        try:
            t = respuesta.split('!r')
            info = t[1].strip()
        except:
            return

        str1 = int(info[0])
        str2 = int(info[1])
        str3 = int(info[2])
        str4 = int(info[3])

        if(str1 == self.pos1 and str2 == self.pos2 and str3 == self.pos3 and str4 == self.pos4):
            salida = 'PRIVMSG '+channel+' :Robaste la caja '+nick+' Codigo: \00303'+info+'\003 Enhorabuena!!\r\n'
            sock.send(salida.encode("utf-8"))
            self.addPuntos(sock, channel, nick)
            return

        if(str1 == self.pos1):
            str1 = "[\00303"+str(str1)+"\003]"
        else:
            if(str1 == self.pos2 or str1 == self.pos3 or str1 == self.pos4):
                str1 = "[\00307"+str(str1)+"\003]"
            else:
                str1 = "[\00304"+str(str1)+"\003]"

        if(str2 == self.pos2):
            str2 = "[\00303"+str(str2)+"\003]"
        else:
            if(str2 == self.pos1 or str2 == self.pos3 or str2 == self.pos4):
                str2 = "[\00307"+str(str2)+"\003]"
            else:
                str2 = "[\00304"+str(str2)+"\003]"

        if(str3 == self.pos3):
            str3 = "[\00303"+str(str3)+"\003]"
        else:
            if(str3 == self.pos1 or str3 == self.pos2 or str3 == self.pos4):
                str3 = "[\00307"+str(str3)+"\003]"
            else:
                str3 = "[\00304"+str(str3)+"\003]"

        if(str4 == self.pos4):
            str4 = "[\00303"+str(str4)+"\003]"
        else:
            if(str4 == self.pos1 or str4 == self.pos2 or str4 == self.pos3):
                str4 = "[\00307"+str(str4)+"\003]"
            else:
                str4 = "[\00304"+str(str4)+"\003]"

        salida = 'PRIVMSG '+channel+' :'+nick+' Pista:'+str1+str2+str3+str4+'\r\n'
        sock.send(salida.encode("utf-8"))

# Metodo addPuntos ------------------------------------------------------------

    def addPuntos(self, sock, channel, nick):
        self.setRobar()
        if (self.puntos.get(nick) is not None):
            self.puntos[nick] = self.puntos[nick]+1
            self.leerPuntos(sock, channel)
        else:
            self.puntos[nick] = 1
            self.leerPuntos(sock, channel)

# Metodo leerPuntos -----------------------------------------------------------

    def leerPuntos(self, sock, channel):

        myList = sorted(self.puntos.items(), key=operator.itemgetter(1),reverse = True)
        msg = ""
        for i in myList:
            msg += "\00307"+str(i[0])+"\003->\00306"+str(i[1])+" "
        salida = 'PRIVMSG '+channel+' :Puntos Robar: '+msg+'\r\n'
        sock.send(salida.encode("utf-8"))
