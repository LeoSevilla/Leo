# -*- coding: utf-8 -*-
import json
import operator
import subprocess
from random import randrange
import re


# Class Serpiente -------------------------------------------------------------


class Serpiente():

    start = False
    puntos = {}
    palabra = ""

# Metodo parar ----------------------------------------------------------------

    def parar(self):

        self.start = False
        self.escribirPuntos()

# Metodo proceso --------------------------------------------------------------

    def proceso(self, socket, sunick, context, info, estado):

        if self.start:
            self.serpiente(socket, context, sunick, self.palabra, info)
        else:
            self.leerpuntos()
            self.infoAyuda(socket, sunick, context)
            self.primeraPalabra(socket, context)
            self.start = True

# Metodo escribirPuntos -------------------------------------------------------

    def escribirPuntos(self):
        with open('serpientePuntos.txt', 'w') as file:
            file.write(json.dumps(self.puntos))

# Metodo leerpuntos -----------------------------------------------------------

    def leerpuntos(self):
        try:
            with open('serpientePuntos.txt', 'r') as file:
                self.puntos = json.load(file)
        except:
            with open('serpientePuntos.txt', 'w') as file:
                file.write(json.dumps(self.puntos))

# Metodo infoAyuda ------------------------------------------------------------

    def infoAyuda(self, socket, sunick, context):

        salida = 'PRIVMSG '+context+' :Para jugar ponga \002!r <palabra>\002. Tiene que empezar con las dos ultimas letras de la palabra en curso \r\n'
        socket.send(salida.encode("utf-8"))

# Metodo primeraPalabra -------------------------------------------------------

    def primeraPalabra(self, socket, channel):

        numLineas = subprocess.check_output(['wc', '-l', 'diccionario.txt']).decode('utf-8')
        offset = randrange(int(numLineas.split()[0]))
        count = 0
        with open('diccionario.txt') as lineas:
            for linea in lineas:
                if count == offset:
                    linea = linea.lower().rstrip()
                    break
                count += 1
        self.palabra = linea
        salida = 'PRIVMSG '+channel+' :\00303Palabra : \00304'+linea+'\r\n'
        socket.send(salida.encode("utf-8"))

# Metodo serpiente ------------------------------------------------------------

    def serpiente(self, sock, channel, nick, palabra, respuesta):
        respuesta = respuesta.lower()

        if respuesta == "!puntos":
            self.leerPuntos(sock, channel)
            return

        try:
            t = respuesta.split('!r')
            toResp = t[1].strip()
        except:
            return
#        if t[0].strip()!="!r":
#            return
        parar = 0
        with open('diccionario.txt') as lineas:
            for linea in lineas:
                linea = linea.lower().rstrip()
                if toResp == linea:
                    parar = 1
                    break
        if parar == 1:
            m1 = re.match(r"^(\w{2}).*", toResp)
            m2 = re.match(r".*(\w{2})$", self.palabra)
            parar = 0
            if m1 and m2:
                if m1.group(1) == m2.group(1):
                    self.palabra = toResp
                    punt = len(toResp)
                    self.addPuntos(sock, channel, nick, punt)
                    salida = 'PRIVMSG '+channel+' :\00303Palabra : \00304'+toResp+'\r\n'
                    sock.send(salida.encode("utf-8"))
                else:
                    salida = 'PRIVMSG '+channel+' :'+nick+' \00304Error : No coincide la serpiente\r\n'
                    sock.send(salida.encode("utf-8"))
        else:
            salida = 'PRIVMSG '+channel+' :'+nick+' \00304Error : No se encuentra en el diccionario\r\n'
            sock.send(salida.encode("utf-8"))

# Metodo addPuntos ------------------------------------------------------------

    def addPuntos(self, sock, channel, nick, punt):
        if (self.puntos.get(nick) is not None):
            self.puntos[nick] = self.puntos[nick]+punt
            salida = 'PRIVMSG '+channel+' :'+nick+' \00303Puntos obtenidos: \00304'+str(punt)+' \003Total:\00304'+str(self.puntos[nick])+'\r\n'
            sock.send(salida.encode("utf-8"))
        else:
            self.puntos[nick] = punt
            salida = 'PRIVMSG '+channel+' :'+nick+' \00303Puntos obtenidos: \00304'+str(punt)+'\r\n'
            sock.send(salida.encode("utf-8"))

# Metodo leerPuntos -----------------------------------------------------------

    def leerPuntos(self, sock, channel):

        myList = sorted(self.puntos.items(), key=operator.itemgetter(1),reverse = True)
        msg = ""
        for i in myList:
            msg += "\00307"+str(i[0])+"\003->\00306"+str(i[1])+" "
        salida = 'PRIVMSG '+channel+' :Puntos: '+msg+'\r\n'
        sock.send(salida.encode("utf-8"))
