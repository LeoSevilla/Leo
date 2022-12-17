import re
import sys
import juegos
import comandos
import palabras
from threading import Timer

# Class Procesos --------------------------------------------------------------


class Procesos():

    comuntador = None
    estJuegos = False

# Metodo inicio ---------------------------------------------------------------

    def inicio(self):

        self.ahorca = juegos.Juegos("ahorcado")
        self.serpi = juegos.Juegos("serpiente")
        self.robar = juegos.Juegos("robar")
        self.comandos = comandos.Comandos()
        self.palabras = palabras.Palabras()

# Metodo imprimir -------------------------------------------------------------

    def imprimir(self, pre, msg, imp):

        self.comuntador = imp
        if self.comuntador:
            print(pre, msg)

# Metodo limpiar --------------------------------------------------------------

    def limpiar(self, line):

        line = re.sub("\x03\d\d?,\d\d?","",line) 
        line = re.sub("\x03\d\d?","",line) 
        line = re.sub("[\x01-\x1F]","",line)
        return line

# Metodo msgRecibido ----------------------------------------------------------

    def msgRecibido(self, socket, mensaje, Master):

        linea = re.match(r"^:(.*?)\!(.*?)\s+(.*?)\s+(.*?)\s+:(.*?)$", mensaje)
        if linea:
            sunick = linea.group(1)
            event = linea.group(3)
            context = linea.group(4)
            info = self.limpiar(linea.group(5))
            if context.find('#') != -1:
                self.respuestaCanal(socket, sunick, context, info.rstrip())
            else:
                return self.respuestaPrivado(socket, sunick, info.rstrip(), Master)

# Metodo respuestaPrivado -----------------------------------------------------

    def respuestaPrivado(self, socket, sunick, info, Master):

        switch = ""
        if info == "!quit" and sunick == Master:
            salida = 'PRIVMSG '+sunick+' :Voy saliendo Master '+Master+'\r\n'
            socket.send(salida.encode("utf-8"))
            # socket.close()
            sys.exit()
        if Master == sunick and info.find("!cmd") != -1:
            t = info.split('!cmd')
            switch = t[1].strip()
            return switch

# Metodo respuestaCanal -------------------------------------------------------

    def respuestaCanal(self, socket, sunick, context, info):

# ------------- Ayuda del bot
        if info == "!help":
            salida = 'PRIVMSG '+context+' :Para info ponga !ayuda\r\n'
            socket.send(salida.encode("utf-8"))

# ------------- Config ahorcado
        elif info == "!ahorcado" and self.estJuegos is False:
            self.estJuegos = "ahorcado"

# ------------- Config serpiente
        elif info == "!serpiente" and self.estJuegos is False:
            self.estJuegos = "serpiente"

# ------------- Config robarº
        elif info == "!robar" and self.estJuegos is False:
            self.estJuegos = "robar"

# ------------- Detener juego
        elif info == "!stop":
            if self.estJuegos == "ahorcado":
                self.ahorca.stop(socket, sunick, context, self.estJuegos)
            elif self.estJuegos == "serpiente":
                self.serpi.stop(socket, sunick, context, self.estJuegos)
            elif self.estJuegos == "robar":
                self.robar.stop(socket, sunick, context, self.estJuegos)
            self.estJuegos = False

# ------------- Procesar otras opciones
        else:
            if info[0] == "!":
                self.comandos.respuesta(socket, sunick, context, info)

# ------------- Procesar respuestas

        if self.estJuegos is not False:
            if self.estJuegos == "ahorcado":
                self.ahorca.procResp(socket, sunick, context, info, self.estJuegos)
            elif self.estJuegos == "serpiente":
                self.serpi.procResp(socket, sunick, context, info, self.estJuegos)
            elif self.estJuegos == "robar":
                self.robar.procResp(socket, sunick, context, info, self.estJuegos)
        else:
            self.palabras.respuesta(socket, sunick, context, info)

# Clase RepeatableTimer--------------------------------------------------------


class RepeatableTimer(object):

    def __init__(self, interval, function, args=[], kwargs={}):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def start(self):
        self.t = Timer(self._interval, self._function, *self._args, **self._kwargs)
        self.t.start()

    def cancel(self):
        self.t.cancel()
