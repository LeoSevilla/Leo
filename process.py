import re
import sys

# Class Procesos --------------------------------------------------------------


class Procesos():

    comuntador = None

# Metodo constructor ----------------------------------------------------------

    def __init__(self):
        pass

# Metodo imprimir -------------------------------------------------------------

    def imprimir(self, pre, msg, imp):
        self.comuntador = imp
        if self.comuntador:
            print(pre, msg)

# Metodo msgRecibido ----------------------------------------------------------

    def msgRecibido(self, socket, mensaje, Master):
        linea = re.match(r"^:(.*?)\!(.*?)\s+(.*?)\s+(.*?)\s+:(.*?)$", mensaje)
        if linea:
            sunick = linea.group(1)
            event = linea.group(3)
            context = linea.group(4)
            info = linea.group(5)
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
            sys.exit()
        if Master == sunick and info.find("!cmd") != -1:
            t = info.split('!cmd')
            switch = t[1].strip()
            return switch

# Metodo respuestaCanal --------------------------------------------------------

    def respuestaCanal(self, socket, sunick, context, info):
        if info == "!help":
            salida = 'PRIVMSG '+context+' :Metodo para hacer funciones\r\n'
            socket.send(salida.encode("utf-8"))
