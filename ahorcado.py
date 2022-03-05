# -*- coding: utf-8 -*-
from random import randrange
import re
import json
import operator

# Class Ahorcado --------------------------------------------------------------


class Ahorcado():

    start = False
    respuestaParcial = ""
    respuesta = ""
    pregunta = ""
    intentos = {}
    puntos = {}
    N_LIN_FILE = 10     # El archivo original tiene 67803 lineas o preguntas

# Metodo parar ----------------------------------------------------------------

    def parar(self):

        self.start = False

# Metodo proceso --------------------------------------------------------------

    def proceso(self, socket, sunick, context, info, estado):

        if self.start:
            self.ahorcado(socket, sunick, info, context)
        else:
            self.topic(socket, context)
            self.leerpuntos()
            self.leerpregunta(socket, context)
            self.start = True

# Metodo replace_at -----------------------------------------------------------

    def replace_at(self, texto, pos, car):

        lista = list(texto)
        lista[pos] = car
        return "".join(lista)

# Metodo leerpregunta ---------------------------------------------------------

    def leerpregunta(self, socket, channel):

        self.intentos.clear()
        repe = ""
        filesize = self.N_LIN_FILE
        offset = randrange(filesize)
        count = 0
        with open('preguntas') as lineas:
            for linea in lineas:
                if count == offset:
                    break
                count += 1

        m = re.match(r"(.*?)\*(.*?)$", linea)
        self.respuesta = m.group(2).lower()
        self.pregunta = m.group(1)
        res = 0
        self.respuestaParcial = self.respuesta
        for i in self.respuesta:
            if repe == i:
                res += 1
            res = self.respuesta.find(i, res)
            if i != ' ':
                self.respuestaParcial = self.replace_at(self.respuestaParcial, res, '*')
            repe = i
        salida = 'PRIVMSG '+channel+' :\00304<Pregunta>\00312'+self.pregunta+'\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+channel+' :\00303Pista: '+self.respuestaParcial+'\r\n'
        socket.send(salida.encode("utf-8"))
        # sock.send('NOTICE '+Master+' :'+self.respuesta+'\r\n')

# Metodo jugadas --------------------------------------------------------------

    def jugadas(self, nick, socket, channel):

        if self.intentos.get(nick) is not None:
            cpuntos = self.intentos[nick]
            self.intentos[nick] = cpuntos + 1
            if cpuntos >= 10:
                salida = 'PRIVMSG '+channel+' :\00304'+nick+'\003. \002\0030,04 Limite de letras 10\r\n'
                socket.send(salida.encode("utf-8"))
                return 1
            return 0
        else:
            self.intentos[nick] = 1
            return 0

# Metodo aadPuntos ------------------------------------------------------------

    def addPuntos(self, nick):

        if self.puntos.get(nick) is not None:
            self.puntos[nick] = self.puntos[nick]+1
        else:
            self.puntos[nick] = 1

# Metodo leerpuntos -----------------------------------------------------------

    def leerpuntos(self):
        try:
            with open('puntosHispano.txt', 'r') as file:
                self.puntos = json.load(file)
        except IOError as e:
            pass

# Metodo writepuntos ----------------------------------------------------------

    def writepuntos(self, sock, nick, channel):

        with open('puntosHispano.txt', 'w') as file:
            file.write(json.dumps(self.puntos))

        myList = sorted(self.puntos.items(), key=operator.itemgetter(1), reverse = True)
        msg = ""
        for i in myList:
            msg += "\00307"+str(i[0])+"\003->\00306"+str(i[1])+" "
        salida = 'PRIVMSG '+channel+' :Puntos: '+msg+'\r\n'
        sock.send(salida.encode("utf-8"))

# Metodo topic ----------------------------------------------------------------

    def topic(self, sock, channel):

        myList = sorted(self.puntos.items(), key=operator.itemgetter(1), reverse = True)
        msg = "Los tres primeros puestos para el ahorcado son: "
        count = 0
        for i in myList:
            msg += "\002"+str(i[0])+"\002->\002"+str(i[1])+" "
            count += 1
            if count == 3:
                break
        msg += "  !!!A por ellos!!!"
        salida = 'TOPIC '+channel+' :'+msg+'\r\n'
        sock.send(salida.encode("utf-8"))

# Metodo ahorcado -------------------------------------------------------------

    def ahorcado(self, socket, sunick, info, channel):

        repe = ""
        infoNormal = info
        info = info.lower()
        if len(info) == 1:
            if self.respuestaParcial.find(info) != -1:
                return
            if self.jugadas(sunick, socket, channel) == 1:
                return
            if self.respuesta.find(info) != -1:
                res = 0
                for i in self.respuesta:
                    if repe == i:
                        res += 1
                    res = self.respuesta.find(i, res)
                    if info == i:
                        self.respuestaParcial = self.replace_at(self.respuestaParcial,res,i)
                        if self.respuestaParcial.find('*') == -1:
                            salida = 'PRIVMSG '+channel+' :Acertada por \00304'+sunick+'\003. \002\0030,01 '+self.respuesta+'\r\n'
                            socket.send(salida.encode("utf-8"))
                            self.addPuntos(sunick)
                            self.writepuntos(socket, sunick, channel)
                            self.leerpregunta(socket, channel)
                            return
                    repe = i
                salida = 'PRIVMSG '+channel+' :\00303Pista: '+self.respuestaParcial+'\r\n'
                socket.send(salida.encode("utf-8"))
        else:
            if self.respuesta == info:
                salida = 'PRIVMSG '+channel+' :Acertada por \00304'+sunick+'\003. \002\0030,01 '+self.respuesta+'\r\n'
                socket.send(salida.encode("utf-8"))
                self.addPuntos(sunick)
                self.writepuntos(socket, sunick, channel)
                self.leerpregunta(socket, channel)
            if infoNormal[0] == "!":
                if infoNormal.find('!puntos') != -1:
                    self.puntaje(socket, sunick, infoNormal, channel)

# Metodo puntaje --------------------------------------------------------------

    def puntaje(self, socket, nick, info, channel):

        t = info.split('!puntos')
        to = t[1].strip()

        if self.puntos.get(to) is not None:
            salida = 'PRIVMSG '+channel+' :\00303Puntos '+to+': '+str(self.puntos[to])+'\r\n'
            socket.send(salida.encode("utf-8"))
        else:
            if to == "":
                salida = 'PRIVMSG '+channel+' :\00303Puntos '+nick+': '+str(self.puntos[nick])+'\r\n'
                socket.send(salida.encode("utf-8"))
            else:
                salida = 'PRIVMSG '+channel+' :\00304Escriba bien el nick '+to+'\r\n'
                socket.send(salida.encode("utf-8"))
